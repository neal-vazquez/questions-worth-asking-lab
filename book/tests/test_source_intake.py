import copy
import html
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


BOOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("source_intake", BOOK / "tools/source_intake.py")
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class SourceIntakeTests(unittest.TestCase):
    def setUp(self):
        self.records = intake.read_jsonl(BOOK / "examples/synthetic-intake.jsonl")
        self.post, self.comment, self.reply = copy.deepcopy(self.records)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = self.root / "store.json"

    def write_input(self, records):
        path = self.root / "input.jsonl"
        path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
        return path

    def test_old_post_with_new_author_comments_is_eligible(self):
        report = intake.summary(self.records)
        self.assertEqual((report["posts"], report["comments"], report["held_sources"]), (1, 2, 0))
        output = intake.packet(self.records)
        self.assertLess(output.index(html.escape(self.post["text"])), output.index(html.escape(self.comment["text"])))
        self.assertLess(output.index(html.escape(self.comment["text"])), output.index(html.escape(self.reply["text"])))

    def test_identical_import_does_not_rewrite_store(self):
        source = self.write_input(self.records)
        self.assertEqual(intake.ingest(source, self.store)["added_observations"], 3)
        before = (self.store.read_bytes(), self.store.stat().st_mtime_ns)
        self.assertEqual(intake.ingest(source, self.store)["added_observations"], 0)
        self.assertEqual((self.store.read_bytes(), self.store.stat().st_mtime_ns), before)

    def test_revision_retains_old_prose_and_packet_uses_latest(self):
        old_text = "[Synthetic original] exact old wording"
        self.post["text"] = old_text
        intake.ingest(self.write_input([self.post]), self.store)
        updated = copy.deepcopy(self.post)
        updated.update(text="[Synthetic revision] new wording", captured_at="2026-09-08T00:00:00Z")
        intake.ingest(self.write_input([updated]), self.store)
        stored = intake.read_store(self.store)
        self.assertEqual(len(stored), 2)
        self.assertEqual(stored[0]["text"], old_text)
        self.assertNotEqual(intake.revision(stored[0]), intake.revision(stored[1]))
        output = intake.packet(stored)
        self.assertIn(updated["text"], output)
        self.assertNotIn(old_text, output)

    def test_out_of_order_capture_does_not_roll_back_latest(self):
        newer = copy.deepcopy(self.post)
        newer.update(text="[Synthetic later]", captured_at="2026-09-08T00:00:00Z")
        result = intake.latest([newer, self.post])
        self.assertEqual(result[self.post["source_id"]]["text"], newer["text"])

    def test_same_revision_later_capture_retains_observation(self):
        newer = copy.deepcopy(self.post)
        newer["captured_at"] = "2026-09-08T00:00:00Z"
        self.assertEqual(intake.revision(newer), intake.revision(self.post))
        self.assertEqual(len(intake.reconcile([self.post, newer])), 2)

    def test_source_text_preserved_including_unicode_line_separators(self):
        text = "[Synthetic]  MiXeD  text\r\n\n💙💛 #Tag <b>bold?</b>\u2028next\u2029last  "
        self.post["text"] = text
        intake.ingest(self.write_input([self.post]), self.store)
        stored = intake.read_store(self.store)
        self.assertEqual(stored[0]["text"], text)
        self.assertIn("<pre>" + html.escape(text) + "</pre>", intake.packet(stored))

    def test_unverified_author_is_held_and_not_rendered(self):
        self.post["authorship"] = "unverified"
        output = intake.packet([self.post])
        self.assertNotIn(html.escape(self.post["text"]), output)
        self.assertEqual(intake.summary([self.post])["held_sources"], 1)

    def test_verified_flag_without_evidence_is_invalid(self):
        self.post["authorship_evidence"] = None
        with self.assertRaises(intake.IntakeError):
            intake.validate_record(self.post)

    def test_third_party_root_holds_author_comments(self):
        self.post["author_key"] = "another-author"
        records = [self.post, self.comment]
        self.assertEqual(intake.summary(records)["held_sources"], 2)
        self.assertNotIn(html.escape(self.comment["text"]), intake.packet(records))

    def test_third_party_comment_not_rendered_as_author_prose(self):
        self.comment["author_key"] = "another-author"
        output = intake.packet([self.post, self.comment])
        self.assertNotIn(html.escape(self.comment["text"]), output)
        self.assertIn(html.escape(self.post["text"]), output)

    def test_orphan_comment_held_then_resolved_by_later_root_import(self):
        self.assertEqual(intake.summary([self.comment])["hold_reasons"], {"missing_root": 1})
        self.assertEqual(intake.summary([self.comment, self.post])["held_sources"], 0)

    def test_partial_text_is_held(self):
        self.post["completeness"] = "partial"
        self.assertEqual(intake.summary([self.post, self.comment])["held_sources"], 2)

    def test_missing_immediate_reply_is_held(self):
        report = intake.summary([self.post, self.reply])
        self.assertEqual(report["hold_reasons"], {"unresolved_reply": 1})

    def test_unknown_reply_context_is_not_treated_as_direct_root(self):
        self.comment["reply_context"] = "unresolved"
        report = intake.summary([self.post, self.comment])
        self.assertEqual(report["held_sources"], 1)

    def test_later_reply_context_resolution_retains_old_observation(self):
        old = copy.deepcopy(self.reply)
        old["reply_context"] = "unresolved"
        old["reply_to_comment_id"] = None
        self.reply["captured_at"] = "2026-09-08T00:00:00Z"
        records = [self.post, self.comment, old, self.reply]
        self.assertEqual(len(intake.reconcile(records)), 4)
        self.assertEqual(intake.summary(records)["held_sources"], 0)

    def test_reply_cycle_is_held(self):
        self.comment.update(reply_to_comment_id=self.reply["source_id"], reply_context="reply")
        self.assertEqual(intake.summary([self.post, self.comment, self.reply])["hold_reasons"], {"reply_cycle": 2})

    def test_cross_thread_reply_is_held(self):
        other = copy.deepcopy(self.post)
        other["source_id"] = "example-other-post"
        self.comment["parent_post_id"] = other["source_id"]
        report = intake.summary([self.post, other, self.comment, self.reply])
        self.assertEqual(report["hold_reasons"], {"unresolved_reply": 1})

    def test_same_time_conflict_rejected_even_with_timezone_alias(self):
        changed = copy.deepcopy(self.post)
        changed.update(text="[Synthetic conflicting observation]", captured_at="2026-09-06T21:00:00-07:00")
        with self.assertRaises(intake.IntakeError):
            intake.reconcile([self.post, changed])

    def test_identity_reassignment_rejected(self):
        for field, replacement in (("author_key", "someone-else"), ("parent_post_id", "another-post")):
            changed = copy.deepcopy(self.comment)
            changed[field] = replacement
            changed["captured_at"] = "2026-09-08T00:00:00Z"
            with self.subTest(field=field), self.assertRaises(intake.IntakeError):
                intake.reconcile([self.comment, changed])

    def test_invalid_timestamps_rejected(self):
        for value in ("2d", "2026-09-01", "2026-09-01T12:00:00", "2026-02-30T12:00:00Z", "2026-09-08T12:00:00Z"):
            changed = copy.deepcopy(self.post)
            changed["published_at"] = value
            with self.subTest(value=value), self.assertRaises(intake.IntakeError):
                intake.validate_record(changed)

    def test_unknown_time_label_is_preserved(self):
        output = intake.packet(self.records)
        self.assertIn("Unknown exact time; platform label: 1h", output)
        self.assertIsNone(intake.latest(self.records)[self.reply["source_id"]]["published_at"])

    def test_source_markup_cannot_execute(self):
        self.post["text"] = '[Synthetic] <script>alert("source")</script><img src=x onerror=alert(1)>'
        output = intake.packet([self.post])
        self.assertNotIn("<script>", output)
        self.assertIn(html.escape(self.post["text"]), output)
        self.assertIn("Content-Security-Policy", output)

    def test_unsafe_source_urls_rejected(self):
        for url in ("javascript:alert(1)", "https://user:secret@example.com/x", "http://example.com/x", "https://example.com/\nfoo"):
            changed = copy.deepcopy(self.post)
            changed["source_url"] = url
            with self.subTest(url=url), self.assertRaises(intake.IntakeError):
                intake.validate_record(changed)

    def test_comment_permalink_parameters_preserved(self):
        self.assertIn("https://example.com/posts/001?comment=001", intake.packet(self.records))

    def test_failed_import_leaves_store_unchanged(self):
        intake.ingest(self.write_input([self.post]), self.store)
        before = self.store.read_bytes()
        bad = copy.deepcopy(self.comment)
        bad["unexpected"] = "not allowed"
        with self.assertRaises(intake.IntakeError):
            intake.ingest(self.write_input([self.reply, bad]), self.store)
        self.assertEqual(before, self.store.read_bytes())

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(intake.IntakeError):
            intake.parse_json('{"text":"first", "text":"second"}')

    def test_public_output_path_rejected(self):
        with self.assertRaises(intake.IntakeError):
            intake.private_output(BOOK / "leaked.json")
        with self.assertRaises(intake.IntakeError):
            intake.private_output(intake.REPO / "private-work/../leaked.json")

    def test_import_lock_prevents_overlapping_writes(self):
        lock = self.store.with_name("store.json.lock")
        lock.write_text("", encoding="utf-8")
        with self.assertRaises(intake.IntakeError):
            intake.ingest(self.write_input(self.records), self.store)
        self.assertFalse(self.store.exists())
        self.assertTrue(lock.exists())

    def test_empty_store_does_not_claim_no_platform_comments(self):
        output = intake.packet([self.post])
        self.assertIn("does not establish that the post has no comments", output)
        self.assertIn("partial", output)
        self.assertEqual(intake.summary([])["sources"], 0)


if __name__ == "__main__":
    unittest.main()
