# Questions Worth Asking

GitHub is the working home for the book's direction, decisions, state, plans, and tools. The former Drive instruction layer is retired.

## Read in order

1. [Current state](STATE.md)
2. [Standing decisions](DECISIONS.md)
3. [Open items](OPEN_ITEMS.jsonl)
4. [Next edition](planning/NEXT_EDITION.md)
5. The relevant [editorial workflow](workflows/EDITORIAL.md), [source contract](workflows/SOURCE_CONTRACT.md), or [source map](sources/README.md)

The existing four-part anthology remains the baseline. New posts and Neal's own comments on his posts extend it without changing verified prose.

## Organization

| Location | Contents |
| --- | --- |
| This directory | Current state, decisions, active items, and tooling changelog |
| `planning/` | Next edition, structural decisions, and publishing work |
| `workflows/` | Editorial procedure and source contract |
| `sources/` | Source navigation and protected-transfer status |
| `history/` | Editions, completed items, and migration reconciliation |
| `tools/`, `tests/`, `examples/`, `templates/` | Intake, synthetic tests, and editorial forms |

The repo is public. Full manuscript text, unpublished drafts, private strategy, and raw captures remain protected in Drive pending a private GitHub destination. This is an explicit remaining migration item. The native manuscript retains its formatting and identity during transition.

## Offline tools

Python 3.10 or later, standard library only. From the repo root:

```bash
python book/tools/source_intake.py validate book/examples/synthetic-intake.jsonl
python book/tools/source_intake.py ingest book/examples/synthetic-intake.jsonl --store private-work/demo-store.json
python book/tools/source_intake.py packet --store private-work/demo-store.json --output private-work/demo-review.html
python -m unittest discover -s book/tests -p 'test_*.py'
```

These use invented examples. Actual captures follow the source contract and remain private. The store retains observations and revisions; packets group eligible comments with verified root posts. A packet does not edit or publish the book.

See [edition history](history/EDITION_HISTORY.md) for the book and [CHANGELOG.md](CHANGELOG.md) for repo changes.
