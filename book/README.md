# Questions Worth Asking

This public directory contains reusable book tools, synthetic fixtures, and shared workflow documentation. The [private book workspace](https://github.com/neal-vazquez/questions-worth-asking-lab-private) is authoritative for manuscript content, current editorial decisions, active tasks, and publishing preparation. The former Drive instruction layer is retired.

## Public reference map

1. [Current state](STATE.md)
2. [Standing decisions](DECISIONS.md)
3. [Active book tasks in the private workspace](https://github.com/neal-vazquez/questions-worth-asking-lab-private/blob/main/book/OPEN_ITEMS.jsonl)
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

The protected transfer is complete. All 56 inventoried Drive files are represented in the private repo, with original stored bytes, rich native exports, source mapping, and checksums. Drive retains native originals for recovery. `OPEN_ITEMS.jsonl` here is intentionally empty: the seven active book tasks moved to the private workspace, and their handoff is recorded in the public closed-item history.

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
