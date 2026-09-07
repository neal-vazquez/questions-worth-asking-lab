# Lab and book operating rules

Read this file, `docs/README.md`, and the affected workstream before changing the lab. Neal's current explicit instruction takes priority. Living contracts follow these rules; dated notes describe historical checks, not current guarantees.

## Startup and source ownership

1. Inspect current remote `main`, branches, open PRs, and the relevant next-work document. Do not substitute an old conversation summary for repository state.
2. GitHub is the authoritative project workspace. For book work read `book/README.md`, `book/STATE.md`, `book/DECISIONS.md`, `book/OPEN_ITEMS.jsonl`, then `book/planning/NEXT_EDITION.md` and the relevant workflow. Neal's migration instruction supersedes Drive-first startup rules. Archived instructions do not regain authority because they use words such as mandatory or immutable.
3. Distinguish project authority from content custody. Rules, state, decisions, plans, and tooling live here. The native anthology and protected sources remain in the book Drive project until a private GitHub destination is established and a complete transfer is verified. That remaining transfer is tracked, not presumed complete. Do not rebuild the old Drive instruction layer.
4. Keep the website source and all private implementation details in their private repository. Carry over general working methods only.

## Preserve the writer

- Verified Neal-authored posts, comments, captions, articles, and unpublished drafts are immutable source prose. Preserve wording, punctuation, capitalization, emoji, hashtags, line breaks, and deliberate emphasis. Do not polish, sanitize, shorten, or ghostwrite them without a specific instruction.
- AI may organize, compare, research, sequence, format, and write visibly labeled editorial framing. Keep that framing separate from Neal's prose. Preserve existing AI-assistance disclosures.
- A fact-check qualification belongs in a separate source/editorial note. Incorrect authorship must be corrected, not protected as author prose.
- Appearance in an activity feed, a matching display name, or posting from a shared account is insufficient proof of human authorship. Record the actual verification evidence.
- For the current intake, include Neal's own comments on Neal's own posts. Verify both relationships. Retain the root post ID and immediate reply ID where known; mark unknown relationships honestly.
- Comments on older posts may be new material. Recheck existing post threads as well as new posts. Never restrict discovery solely to new post dates.

## Work and validation

Use one coherent change per branch: understand, inspect impact, implement, validate, document, review, commit, verify remote state. Routine repo changes requested by Neal may be committed and integrated in the same session after these checks. A repo update is not a book publication or website deployment.

Before changing book tools, consider prose integrity, attribution, thread context, duplicate/revision behavior, uncertain dates, source coverage, publication scope, and existing-manuscript compatibility. Keep the tools offline unless an authorized integration is deliberately added. Never add background LinkedIn sending, engagement, or scheduling as part of book intake.

Public files must contain no raw account exports, private archive identifiers/links, unpublished prose, third-party conversation dumps, credentials, or private project material. A public branch or PR has the same exposure as public `main`. Use synthetic fixtures and review the complete file list before pushing. `.gitignore` is an accident-prevention aid, not a confidentiality guarantee.

Follow `book/sources/README.md` for protected material. Until private GitHub custody is verified, retain durable sources and private packets in the book Drive archive. `private-work/` is ignored temporary processing space, not a backup. Do not upload private inputs or packets to public CI artifacts or logs.

Run the relevant source-integrity tests when ingestion, revision handling, or packet construction changes. Run the existing analytics checks if their files change. State exactly what was tested and what was only recorded in an earlier index. Do not fabricate counts, import completion, publication dates, or results to create daily activity.

## Edition discipline

Preserve the existing four-part anthology and current manual edits. Inspect `book/planning/NEXT_EDITION.md`, the source map, and the actual manuscript before incorporating anything. Use source IDs and revision hashes for an edition selection; do not rely on piece numbers alone because numbering can change. Follow `book/DECISIONS.md` for reconciled editorial rules.

Keep original posts and dated author follow-ups distinguishable. Label contextual framing as assistant-generated. Never invent a missing parent comment or treat approximate platform labels as exact timestamps.

Before an authorized manuscript edit, preserve a native backup. Check added prose against its source, existing prose against the baseline, numbering, TOC targets, source notes, references, and layout. Preserve the established type styles, with no accidental Arial. Keep final back matter in this order: References, Special Thanks, Changelog, Legal. Legal remains last.

New material goes into a new working edition unless Neal asks for a direct correction. Keep concise newest-first book release notes distinct from repo changes and retrieval history. Neal handles PDF export unless the current request explicitly asks for a PDF. Only report publication after the actual upload or Neal's confirmation.
