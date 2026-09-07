# From LinkedIn writing to the next edition

## 1. Establish the baseline

Read the GitHub state, decisions, active items, and actual anthology before selecting new material. Preserve the current edition and its manual edits. Carry over source IDs already incorporated, including comments attached to earlier pieces, so a repeat capture cannot masquerade as a new essay.

General lessons carried forward from the website work are a discoverable documentation hierarchy, an explicit source of truth, small coherent changes, validation before release, preserved recovery points, and accurate reporting of what actually shipped.

## 2. Capture original text and its context

Use the existing archive, author-provided text/screenshots, an official export, or a bounded authorized read of the source. Preserve the original capture in Drive and record its locator. Do not make the workflow depend on a scheduled crawler, account engagement, or guessing an unavailable API. Do not infer native export column names before inspecting the actual export.

Capture Neal-authored posts plus Neal-authored comments on those posts. Revisit older post threads because new commentary may appear there after the original post date. Record which posts were checked, the capture time, and whether comments were expanded fully, partially, or not checked. A complete-at-capture flag applies only to that observation, never to all future comments or the entire account.

Verify the human author separately from the posting account, and verify each parent post's owner. A feed appearance or display-name match is insufficient. Third-party replies may supply context but are not Neal's prose. Describe needed third-party context in a separate, anonymized editorial note. Do not silently insert another person's writing into the author passage.

Preserve source text, emoji, hashtags, spelling, and line breaks exactly. Record a post ID, a stable comment ID or durable archive-local identifier, its root post ID, and immediate reply ID when known. Retain supplied permalink query parameters that identify a comment. Do not invent comment IDs, permalinks, missing replies, or exact dates.

## 3. Normalize and reconcile

Follow [SOURCE_CONTRACT.md](SOURCE_CONTRACT.md), then validate and ingest privately. Map alternate URLs/IDs for the same platform object to the same source ID before importing. Text equality alone does not make two posts identical. An edit to an existing ID becomes a retained observation, never an overwrite of original wording.

Read the generated packet and held-record counts. Resolve truncated text, attribution uncertainty, missing roots, or inconsistent reply relationships before including their prose. A held record remains in the private store. Fixing its provenance produces a later observation with supporting evidence.

Exact publication times are optional when unavailable. Preserve the displayed relative label and the capture timestamp separately. Compare available comments by grounded publication time, and label capture-order fallback when dates are unknown. Do not claim a complete account history from a partial pass.

## 4. Place and annotate

Keep the existing architecture:

| Part | Question | Editorial use |
| --- | --- | --- |
| I | How should we live? | Life, meaning, practice, and personal reflection |
| II | How should we treat one another? | Relationships, ethics, institutions, and care |
| III | What should we believe? | Knowledge, evidence, religion, and interpretation |
| IV | What are we becoming? | AI, technology, culture, and human change |

These are placement aids, not automatic classifications. Choose each piece's primary home by its question. Avoid duplicating it across parts just because it spans several themes.

Use [templates/edition-selection.json](../templates/edition-selection.json) as a private selection ledger. Pin every selected source to its revision hash and record include, hold, exclude, or already-incorporated status. Explain exclusions without deleting their source observations. Identify the existing piece by heading plus source IDs, not its current number alone.

Default treatment: original post, then clearly labeled author follow-ups. A comment can clarify, extend, correct, complicate, or add an aside. Preserve those distinctions without rewriting either passage. If a later comment changes the position, make chronology visible. Use a standalone comment piece only when it has enough context to be intelligible and its sources remain traceable.

## 5. Update the manuscript when authorized

Preserve a native backup, apply the selected additions in the canonical Google Doc, and compare source prose exactly. Keep assistant-authored introductions, factual qualifications, anonymized context, and references visibly separate. Preserve prior AI-assistance disclosures rather than reclassifying assisted text as wholly original prose.

Check sequential piece numbers, TOC destinations and indentation, existing images and emphasis, references and cross-links, established typography, and counts in framing. Preserve front matter: Introduction, About Neal Vazquez by ChatGPT, Back Cover, TOC, standalone Dedication, Part I. Preserve back matter: References, Special Thanks, Changelog, Legal.

## 6. Record the actual result

Update the book's concise changelog and the GitHub state and edition history with source additions, author-comment additions, revisions, placement, checks, gaps, and backup reference. Keep repository tooling notes in [CHANGELOG.md](../CHANGELOG.md).

Report capture, incorporation, validation, and publication separately. A working packet is not a released book. Neal handles PDF export unless explicitly requested in the current task. Record public release only after actual distribution or Neal's confirmation. No LinkedIn writing, messaging, engagement, or scheduled action is implied by this workflow.
