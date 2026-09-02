# Human Review Gate for AI-Assisted Publishing

## Purpose

A lightweight pattern for using generative AI to prepare public-facing material without treating model output as automatically publishable.

## Core idea

Separate **generation** from **authorization**.

The model can draft, summarize, restructure, classify, or propose changes. Publication occurs only after an explicit review step evaluates whether the output is appropriate for the intended audience and context.

## Minimal workflow

```text
source material
      |
      v
AI transformation
      |
      v
candidate artifact
      |
      v
review gate
   /      \
reject    approve
  |          |
revise    publish
```

## Review dimensions

A practical review gate can ask five questions:

1. **Accuracy**: Does the artifact claim anything that has not been established?
2. **Privacy**: Does it expose personal, identifying, confidential, or unnecessary information?
3. **Attribution**: Are sources, authorship, and AI assistance represented accurately?
4. **Context**: Could the artifact become misleading when separated from the conversation or workflow that produced it?
5. **Utility**: Does publishing this create genuine value, or is it merely output for output's sake?

## Automation boundary

Low-risk automation can handle repetitive preparation and repository maintenance. The system should become more conservative as consequences increase.

A useful heuristic is:

```text
required_review_intensity ~ consequence_of_error
```

This is not a calibrated equation. It is a design principle: the greater the plausible cost of a bad output, the stronger the review requirement should be.

## Why this matters

Human-in-the-loop design is sometimes framed as a temporary limitation of current AI systems. It can also be understood as an architectural choice about accountability. Even if model quality improves, separating recommendation from authorization can remain valuable when publication affects people, institutions, or public records.

## Status

Working pattern. Future notes may extend this into risk tiers, evaluation criteria, or implementation examples.
