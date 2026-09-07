# Source contract, version 1

The supported input is UTF-8 JSONL: one complete JSON object per line, using the exact fields below. Blank lines and an initial UTF-8 BOM are allowed. Unknown or duplicate JSON keys are rejected. Every record is an observation of a source, not a manuscript edit or a publication approval.

## Record fields

| Field | Meaning |
| --- | --- |
| `source_id` | Stable platform ID or durable archive-local ID. Never generate a new ID merely because text was edited. Normalize aliases before ingest. |
| `kind` | `post` or `comment`. This first tool does not ingest articles or media binaries. |
| `author_key` | Stable attributed author key. Neal is `neal-vazquez`. Account ownership alone does not establish human authorship. |
| `authorship` | `verified`, `unverified`, or `third_party`. |
| `authorship_evidence` | Nonempty evidence note when verified; otherwise a note or null. A declared flag is not independent verification by the tool. |
| `parent_post_id` | Root post ID for every comment; null for posts. A root may be absent from the current batch, but its comment is held until the store has an eligible root. |
| `reply_to_comment_id` | Immediate comment ID when observed; null for a direct root comment or genuinely unresolved context. |
| `reply_context` | Posts: `not_applicable`. Comments: `direct_root`, `reply`, or `unresolved`. A `reply` requires an immediate ID; unresolved context is held. |
| `source_url` | Credential-free HTTPS source/permalink or null. Preserve comment-identifying queries. No URLs are fetched by the tool. |
| `source_locator` | Nonempty private archive reference precise enough to retrieve the captured source. A missing permalink is not a reason to invent one. |
| `capture_method` | `official_export`, `authorized_capture`, `author_supplied`, `archive`, or `synthetic`. |
| `captured_at` | Exact observation time, ISO 8601 including seconds and timezone. For archival recaptures, record the actual new inspection time and identify the historical capture in the locator. |
| `published_at` | Grounded exact publication timestamp with timezone, or null. It cannot be later than capture. |
| `published_label` | Original display label such as `2d` or a known date without an exact time, or null. Never convert it to a guessed exact timestamp. |
| `text` | Original nonempty source text, without cleanup, truncation, hashtag removal, or editorial framing. JSON escaping is only a transport representation. |
| `completeness` | `complete` or `partial`. Expand truncated text or mark it partial. If source images carry unrecovered prose required for meaning, do not claim that the text capture is complete. |
| `comment_scan` | Posts: `not_checked`, `partial`, or `complete_at_capture`. Comments: `not_applicable`. Coverage is per observed root at a stated time, not a guarantee of account-wide or future completeness. |

Use the [synthetic fixture](examples/synthetic-intake.jsonl) for an executable example. All of its prose and links are invented test material.

## Store and reconciliation

The JSON store has `schema_version: 1`, `owner_key: "neal-vazquez"`, and an `observations` array containing the validated records. Its latest view selects by capture time for each source ID. Older observations remain recoverable, even if imported after newer ones.

An identical observation is a no-op. A later capture is retained. A later textual or provenance change is a new revision under the same source ID; it does not erase the old text. `revision_sha256` is computed from canonical JSON of every field except `captured_at`, using sorted keys, UTF-8, and compact separators. It pins provenance as well as prose. It is an integrity identifier, not proof of authorship or a cryptographic signature from LinkedIn.

Changing kind, author key, or root under an existing ID is an identity conflict and rejects the import. Reconcile a mistaken identity explicitly with the archive and a recorded correction; do not mint a new ID to disguise the problem. Immediate reply context and verification evidence can be resolved in later observations. Conflicting revisions at the same capture instant are rejected, including equivalent timezone representations of that instant.

Imports validate completely before replacing the store. A temporary file, atomic replacement, and exclusive import lock protect an existing store from partial writes and concurrent imports through this tool. If a process dies leaving a lock, verify that no import is active before removing that lock. These local safeguards do not replace durable Drive backups or native manuscript revision history.

## Candidate eligibility

An eligible root must be a complete post with author key `neal-vazquez` and verified authorship evidence. An eligible comment must meet those same authorship/completeness conditions and have that eligible root. When an immediate reply ID is present, the known ancestor chain must stay in the same root, be cycle-free, and have eligible author context. Missing or third-party reply context is held for separate editorial review. Third-party content is never rendered as Neal's prose.

The packet groups eligible comments under their root, includes source IDs/revision hashes/timing/coverage, and escapes source text for HTML display. It never renders held prose. Missing exact publication times remain visible and do not by themselves block otherwise grounded text. Sorting uses exact publication time when available, otherwise capture time with a visible warning that this does not establish chronology.

Eligible means ready for source review, not approved for the book. The packet does not apply selections, fact-check claims, verify evidence independently, audit an entire account, or change the canonical manuscript. Use the private [selection template](templates/edition-selection.json) manually to pin reviewed revisions and avoid reincorporating pieces already in an edition.

## Boundaries and diagnostics

- Offline only, no dependencies, paid calls, account actions, or background schedule.
- Inputs and outputs are limited to 50 MiB; a store or input is limited to 20,000 observations. Split larger archives deliberately without losing cross-batch root context.
- Output paths inside this repo must resolve under ignored `private-work/`; paths outside it must be in an appropriate private workspace. The tool cannot verify an external folder's sharing state.
- Public CI runs synthetic data and structural tests only. Command diagnostics show counts and bounded error categories, not prose or private locators.
- Counts distinguish observations, unique latest sources, posts, comments, eligible sources, and held sources. A source may have multiple hold reasons, so reason totals can exceed held-source totals.
- Preserve raw exports and original screenshots separately. Normalization is an explicit preparation step, not a claim that a native LinkedIn export was parsed here.
