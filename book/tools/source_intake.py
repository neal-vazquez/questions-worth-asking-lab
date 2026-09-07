"""Offline source observations and private book-review packets. Standard library only."""

import argparse
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import re
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlsplit


OWNER = "neal-vazquez"
REPO = Path(__file__).resolve().parents[2]
MAX_BYTES = 50 * 1024 * 1024
MAX_RECORDS = 20_000
FIELDS = {
    "source_id", "kind", "author_key", "authorship", "authorship_evidence",
    "parent_post_id", "reply_to_comment_id", "reply_context", "source_url", "source_locator",
    "capture_method", "captured_at", "published_at", "published_label", "text",
    "completeness", "comment_scan",
}


class IntakeError(ValueError):
    """A bounded diagnostic that does not echo private source text."""


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def timestamp(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", value
    ):
        raise IntakeError("timestamp requires an ISO 8601 time with timezone")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        raise IntakeError("invalid calendar timestamp") from None


def validate_record(record):
    if not isinstance(record, dict) or set(record) != FIELDS:
        raise IntakeError("record must contain exactly the source-contract fields")
    for field in ("source_id", "author_key", "source_locator", "text"):
        if not nonempty(record[field]):
            raise IntakeError(f"{field} must be nonempty text")
    for field in ("source_id", "author_key", "parent_post_id", "reply_to_comment_id"):
        value = record[field]
        if value is not None and (not isinstance(value, str) or not re.fullmatch(r"\S{1,500}", value)):
            raise IntakeError(f"{field} must be a stable ID without whitespace")
    for field, choices in {
        "kind": ("post", "comment"),
        "authorship": ("verified", "unverified", "third_party"),
        "capture_method": ("official_export", "authorized_capture", "author_supplied", "archive", "synthetic"),
        "completeness": ("complete", "partial"),
        "comment_scan": ("not_checked", "partial", "complete_at_capture", "not_applicable"),
        "reply_context": ("direct_root", "reply", "unresolved", "not_applicable"),
    }.items():
        if record[field] not in choices:
            raise IntakeError(f"invalid {field}")
    for field in ("authorship_evidence", "published_label"):
        if record[field] is not None and not nonempty(record[field]):
            raise IntakeError(f"{field} must be nonempty text or null")
    if record["authorship"] == "verified" and not nonempty(record["authorship_evidence"]):
        raise IntakeError("verified authorship requires recorded evidence")
    captured = timestamp(record["captured_at"])
    if record["published_at"] is not None and timestamp(record["published_at"]) > captured:
        raise IntakeError("publication cannot be later than capture")
    if record["kind"] == "post":
        if record["parent_post_id"] is not None or record["reply_to_comment_id"] is not None:
            raise IntakeError("post cannot have a parent or reply ID")
        if record["comment_scan"] == "not_applicable":
            raise IntakeError("post must record comment-scan coverage")
        if record["reply_context"] != "not_applicable":
            raise IntakeError("post has no reply context")
    else:
        if not nonempty(record["parent_post_id"]):
            raise IntakeError("comment requires a root post ID")
        if record["source_id"] in (record["parent_post_id"], record["reply_to_comment_id"]):
            raise IntakeError("comment cannot parent itself")
        if record["comment_scan"] != "not_applicable":
            raise IntakeError("comment scan belongs to the root post")
        if record["reply_context"] == "not_applicable":
            raise IntakeError("comment must record reply context")
        if record["reply_context"] == "reply" and record["reply_to_comment_id"] is None:
            raise IntakeError("reply requires an immediate comment ID")
        if record["reply_context"] == "direct_root" and record["reply_to_comment_id"] is not None:
            raise IntakeError("direct root comment cannot have an immediate comment ID")
    url = record["source_url"]
    if url is not None:
        if not isinstance(url, str):
            raise IntakeError("source_url must be HTTPS or null")
        try:
            parts = urlsplit(url)
            valid = parts.scheme == "https" and bool(parts.hostname) and not parts.username and not parts.password
        except ValueError:
            valid = False
        if not valid or any(c.isspace() or ord(c) < 32 for c in url):
            raise IntakeError("source_url must be a credential-free HTTPS URL")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def revision(record):
    """Pin text AND provenance; repeat observations can share one revision."""
    return digest({key: value for key, value in record.items() if key != "captured_at"})


def read_text(path):
    with Path(path).open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise IntakeError("input exceeds the 50 MiB processing limit")
    return data.decode("utf-8-sig")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise IntakeError("duplicate JSON object key")
        result[key] = value
    return result


def parse_json(text):
    try:
        return json.loads(text, object_pairs_hook=unique_keys)
    except json.JSONDecodeError:
        raise IntakeError("invalid JSON") from None


def read_jsonl(path):
    records = []
    for number, line in enumerate(read_text(path).split("\n"), 1):
        if not line.strip():
            continue
        try:
            record = parse_json(line)
            validate_record(record)
        except IntakeError as exc:
            raise IntakeError(f"row {number}: {exc}") from None
        records.append(record)
        if len(records) > MAX_RECORDS:
            raise IntakeError("input exceeds the 20,000 observation limit")
    return records


def reconcile(records):
    """Reject identity collisions and ambiguous recaptures; never guess a winner."""
    if len(records) > MAX_RECORDS:
        raise IntakeError("store exceeds the 20,000 observation limit")
    identities, observations, versions = {}, {}, {}
    for record in records:
        validate_record(record)
        identity = (record["kind"], record["author_key"], record["parent_post_id"])
        source_id = record["source_id"]
        if source_id in identities and identities[source_id] != identity:
            raise IntakeError("source identity conflict; reconcile IDs before importing")
        identities[source_id] = identity
        observed = timestamp(record["captured_at"])
        key = (source_id, observed)
        if key in versions and versions[key] != revision(record):
            raise IntakeError("conflicting observations at the same capture time")
        versions[key] = revision(record)
        observations[digest(record)] = copy.deepcopy(record)
    return sorted(observations.values(), key=lambda r: (timestamp(r["captured_at"]), r["source_id"], digest(r)))


def read_store(path):
    value = parse_json(read_text(path))
    if not isinstance(value, dict) or set(value) != {"schema_version", "owner_key", "observations"}:
        raise IntakeError("invalid store envelope")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1 or value["owner_key"] != OWNER:
        raise IntakeError("unsupported store version or owner")
    if not isinstance(value["observations"], list):
        raise IntakeError("observations must be a list")
    return reconcile(value["observations"])


def latest(records):
    return {r["source_id"]: r for r in reconcile(records)}


def holds(record, current):
    reasons = []
    if record["author_key"] != OWNER or record["authorship"] != "verified":
        reasons.append("authorship")
    if record["completeness"] != "complete":
        reasons.append("incomplete_text")
    if record["kind"] == "comment":
        if record["reply_context"] == "unresolved":
            reasons.append("unresolved_reply")
        parent = current.get(record["parent_post_id"])
        if parent is None or parent["kind"] != "post":
            reasons.append("missing_root")
        elif holds(parent, current):
            reasons.append("root_not_eligible")
        # An immediate parent is optional for a direct root comment. If supplied,
        # its chain must exist, stay in this thread, and contain eligible text.
        seen = {record["source_id"]}
        reply_id = record["reply_to_comment_id"]
        while reply_id is not None:
            if reply_id in seen:
                reasons.append("reply_cycle")
                break
            seen.add(reply_id)
            reply = current.get(reply_id)
            if reply is None or reply["kind"] != "comment" or reply["parent_post_id"] != record["parent_post_id"]:
                reasons.append("unresolved_reply")
                break
            if reply["author_key"] != OWNER or reply["authorship"] != "verified" or reply["completeness"] != "complete" or reply["reply_context"] == "unresolved":
                reasons.append("reply_context_requires_review")
                break
            reply_id = reply["reply_to_comment_id"]
    return reasons


def summary(records):
    current = latest(records)
    result = {"observations": len(reconcile(records)), "sources": len(current), "posts": 0, "comments": 0,
              "eligible_sources": 0, "held_sources": 0, "hold_reasons": {}}
    for record in current.values():
        result["posts" if record["kind"] == "post" else "comments"] += 1
        reasons = holds(record, current)
        result["held_sources" if reasons else "eligible_sources"] += 1
        for reason in reasons:
            result["hold_reasons"][reason] = result["hold_reasons"].get(reason, 0) + 1
    return result


def private_output(path):
    path = Path(path).resolve()
    if path.is_relative_to(REPO) and not path.is_relative_to(REPO / "private-work"):
        raise IntakeError("outputs inside this public repo must be under private-work/")
    return path


def atomic_write(path, content):
    path = private_output(path)
    data = content.encode("utf-8")
    if len(data) > MAX_BYTES:
        raise IntakeError("output exceeds the 50 MiB processing limit")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".intake-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def ingest(input_path, store_path):
    path = private_output(store_path)
    if Path(input_path).resolve() == path:
        raise IntakeError("input and store must be different files")
    incoming = read_jsonl(input_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise IntakeError("store is locked by another import; inspect before retrying") from None
    try:
        os.close(fd)
        previous = read_store(path) if path.exists() else []
        merged = reconcile(previous + incoming)
        added = len(merged) - len(previous)
        if added or not path.exists():
            envelope = {"schema_version": 1, "owner_key": OWNER, "observations": merged}
            atomic_write(path, json.dumps(envelope, ensure_ascii=False, indent=2) + "\n")
        return {"added_observations": added, **summary(merged)}
    finally:
        lock.unlink()


def packet(records):
    current = latest(records)
    safe = [r for r in current.values() if not holds(r, current)]
    counts = summary(records)
    comments_by_root = {}
    for record in safe:
        if record["kind"] == "comment":
            comments_by_root.setdefault(record["parent_post_id"], []).append(record)
    e = html.escape
    parts = ["<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">",
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'">',
             "<title>Questions Worth Asking: private source review</title>",
             "<style>body{max-width:70ch;margin:2rem auto;padding:0 1rem;color:#182c45;background:#fffdf8;font:18px/1.6 Georgia,serif}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}small{overflow-wrap:anywhere}article{border-top:2px solid #a9833c;margin-top:2rem}aside{padding-left:1rem;border-left:3px solid #a9833c}a{color:#245587}</style>",
             "<h1>Questions Worth Asking</h1><p>Private source review. This is a candidate packet, not an approved edition. All framing below is tool-generated; source prose is preserved separately.</p>",
             f'<p>{counts["posts"]} posts and {counts["comments"]} comments observed. {counts["held_sources"]} sources held. Held prose is omitted; records remain in the private store.</p>',
             "<p>Order uses publication time when known, otherwise capture time. This fallback is not proof of chronology. Unresolved reply context is held for review.</p>"]

    def order(record):
        return (timestamp(record["published_at"] or record["captured_at"]), record["source_id"])

    def render(record, label):
        time = record["published_at"] or ("Unknown exact time; platform label: " + (record["published_label"] or "not recorded"))
        result = f'<h3>{label}</h3><small>Source: {e(record["source_id"])}<br>Revision: {revision(record)}<br>Published: {e(time)}<br>Captured: {e(record["captured_at"])}</small>'
        if record["reply_to_comment_id"]:
            result += f'<p>Reply to: {e(record["reply_to_comment_id"])}</p>'
        if record["capture_method"] == "synthetic":
            result += "<p><strong>Synthetic example. Invented text, not Neal's writing.</strong></p>"
        if record["source_url"]:
            result += f'<p><a href="{e(record["source_url"], quote=True)}" rel="noreferrer noopener">Original source</a></p>'
        result += f'<p><small>Private locator: {e(record["source_locator"])}</small></p>'
        result += f'<pre>{e(record["text"])}</pre>'
        return result

    for post in sorted((r for r in safe if r["kind"] == "post"), key=order):
        parts += ["<article>", render(post, "Original post"), f'<p>Comment coverage at capture: {e(post["comment_scan"])}. Future comments are not covered by this observation.</p>']
        comments = sorted(comments_by_root.get(post["source_id"], []), key=order)
        if not comments:
            parts.append("<p>No eligible author comments in this store. This does not establish that the post has no comments.</p>")
        for comment in comments:
            parts += ["<aside>", render(comment, "Author follow-up"), "</aside>"]
        parts.append("</article>")
    parts.append("</html>")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("input", type=Path)
    imp = commands.add_parser("ingest")
    imp.add_argument("input", type=Path)
    imp.add_argument("--store", type=Path, required=True)
    review = commands.add_parser("packet")
    review.add_argument("--store", type=Path, required=True)
    review.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            result = summary(read_jsonl(args.input))
        elif args.command == "ingest":
            result = ingest(args.input, args.store)
        else:
            if args.store.resolve() == args.output.resolve():
                raise IntakeError("packet output cannot replace the source store")
            records = read_store(args.store)
            atomic_write(args.output, packet(records))
            result = summary(records)
        print(json.dumps(result, sort_keys=True))
    except (IntakeError, OSError, UnicodeError) as exc:
        # File errors may contain private paths. Only contract diagnostics are echoed.
        parser.exit(2, "Intake failed: " + (str(exc) if isinstance(exc, IntakeError) else type(exc).__name__) + "\n")


if __name__ == "__main__":
    main()
