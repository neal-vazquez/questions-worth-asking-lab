# Questions Worth Asking Lab

An AI-assisted public research lab and book-development workbench exploring data science, artificial intelligence, philosophy, responsible AI, and the questions connecting them.

## What this is

This repository is a living workbench for small experiments, research notes, analytical patterns, technical sketches, and ideas that emerge from ongoing work at the intersection of data, AI, and philosophy.

The goal is not to present every entry as a finished product. The goal is to document useful thinking in public, accumulate reusable artifacts over time, and make the process of inquiry visible.

## Areas of work

- **Data science**: analytical methods, evaluation patterns, synthetic examples, measurement design, and small technical experiments.
- **Artificial intelligence**: model behavior, LLM evaluation, human-in-the-loop systems, retrieval, prompting, and practical AI workflows.
- **Responsible AI**: transparency, uncertainty, review boundaries, automation design, and the social consequences of deploying AI systems.
- **Philosophy of technology**: epistemology, agency, cognition, consciousness, interpretation, and the relationship between humans and machines.
- **Research notes**: concise working notes on concepts, methods, and questions worth revisiting.

## Repository structure

```text
ai-workflows/       Reusable AI workflow and evaluation patterns
book/               Questions Worth Asking editorial workflow and source tools
daily/              Dated lab notes and working observations
data-notes/         Data science and analytics notes
docs/               Living documentation map
experiments/        Small executable experiments and synthetic examples
```

## Questions Worth Asking: the book

The [book workstream](book/README.md) supports the living anthology, including Neal's LinkedIn posts and his own follow-up comments on those posts. It preserves source wording, tracks observations and revisions, links comments to their root posts, and prepares private review packets for editorial selection.

GitHub now directs the book through reconciled state, decisions, and open items. Protected manuscript and source content remain in the minimal Drive archive pending private GitHub transfer. Start with the [next-edition plan](book/planning/NEXT_EDITION.md). New live LinkedIn capture and manuscript incorporation are tracked separately from repository implementation.

Start with [AGENTS.md](AGENTS.md) and the [documentation map](docs/README.md) before continuing work.

## Current experiment

[`experiments/funnel-integrity/`](experiments/funnel-integrity/) turns a decision-first analytics funnel into a machine-readable contract. It includes a Python validator, regression tests, and GitHub Actions CI that checks event semantics, stage coverage, duplicate names, and privacy-sensitive fields.

The experiment extends [`data-notes/decision-first-portfolio-analytics.md`](data-notes/decision-first-portfolio-analytics.md).

## AI-assisted workflow

This repository is intentionally AI-assisted. Generative AI may be used to help draft, structure, critique, test, or refine material. Neal Vazquez directs the work, selects what is worth pursuing, evaluates outputs, edits and curates public artifacts, and remains responsible for what is published here.

AI assistance is treated as part of the methodology rather than disguised as invisible labor. Entries should not claim experiments were run, sources were reviewed, or results were observed unless that actually occurred.

## Working principles

1. Prefer small substantive contributions over performative complexity.
2. Distinguish observation, inference, hypothesis, and opinion.
3. Use synthetic or public data for lightweight examples unless a source is explicitly documented.
4. Do not publish confidential, private, identifying, or security-sensitive information.
5. Do not fabricate results for the sake of maintaining activity.
6. Let the repository become more useful through accumulation.

## Status

This is an active public lab notebook. Expect frequent small updates and occasional larger experiments.

## Rights and permissions

See [RIGHTS.md](RIGHTS.md) for copyright scope, AI-authorship limitations, existing licenses, and reuse permissions.
