# Questions Worth Asking: book workstream

The book grows from Neal Vazquez's writing, including the additional thinking he publishes in comments on his own LinkedIn posts. This workstream makes those relationships and later revisions inspectable while preserving the original prose.

The existing native Google Doc is the canonical anthology. This public lab provides the working method and tools; the private source archive and manuscript stay in the book's Drive project.

## Start here

- [Next edition](NEXT_EDITION.md): current scope, baseline, and remaining work.
- [Editorial workflow](EDITORIAL_WORKFLOW.md): acquisition, author follow-ups, selection, and edition checks.
- [Source map](SOURCE_MAP.md): how to find the current manuscript and earlier captures.
- [Source contract](SOURCE_CONTRACT.md): exact input and output behavior.
- [Changelog](CHANGELOG.md): changes to the tooling, distinct from published book editions.

## Offline intake and review

Requires Python 3.10 or later and the standard library. Run from the repo root:

```bash
python book/tools/source_intake.py validate book/examples/synthetic-intake.jsonl
python book/tools/source_intake.py ingest book/examples/synthetic-intake.jsonl --store private-work/demo-store.json
python book/tools/source_intake.py packet --store private-work/demo-store.json --output private-work/demo-review.html
python -m unittest discover -s book/tests -p 'test_*.py'
```

These commands use invented demonstration text. They do not retrieve LinkedIn content or represent a real book intake. For actual work, normalize a verified capture to the [source contract](SOURCE_CONTRACT.md) and substitute its private file path. Existing raw exports are retained separately in Drive; this tool does not claim compatibility with an uninspected LinkedIn CSV format.

The store retains every distinct observation, rejects conflicting identities, and treats an identical import as a no-op. The review packet groups each eligible post with its eligible author comments. Incomplete or unresolved records are counted as held and do not contribute prose to the packet. Every rendered item carries its source ID, revision hash, timestamp status, and source link when available. Packet text is escaped so source markup remains text.

Review packets are candidates for editorial work, not approved editions. Save actual stores and review packets back to the book's existing Drive project after processing. Never commit them or attach them to public CI. All commands report counts rather than source text.
