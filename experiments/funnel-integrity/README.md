# Funnel integrity experiment

A small, executable experiment for keeping a portfolio analytics implementation aligned with the decisions it is supposed to support.

This builds on the decision-first analytics note in [`../../data-notes/decision-first-portfolio-analytics.md`](../../data-notes/decision-first-portfolio-analytics.md).

## Question

How do you prevent a conversion funnel from quietly degrading into a pile of implementation-specific click events?

The working answer here is to treat the measurement plan as a versioned data contract and validate it automatically.

## Funnel

The checked-in contract models:

```text
targeted
  -> exposed
  -> interaction
  -> assisted
  -> conversion
```

Each stage must have at least one semantically named event. The validator also rejects duplicate event names, missing triggers, invalid stages, UI-coupled event names, and disallowed sensitive properties.

## Files

- `funnel_spec.json` is the machine-readable measurement contract.
- `validate_measurement_spec.py` validates the contract with the Python standard library only.
- `tests/test_validate_measurement_spec.py` contains regression tests for failure modes.

## Run

```bash
python experiments/funnel-integrity/validate_measurement_spec.py \
  experiments/funnel-integrity/funnel_spec.json

python -m unittest discover \
  -s experiments/funnel-integrity/tests \
  -p 'test_*.py'
```

Expected validator output:

```text
VALID measurement spec: 5 events across 5 stages
```

## Why this matters

Analytics taxonomies fail in mundane ways. Event names get tied to button colors, personally identifying fields leak into telemetry, multiple events start meaning the same thing, or a funnel stage is represented in slides but not in instrumentation.

A lightweight contract test catches those failures before dashboard interpretation begins.

This is deliberately a synthetic framework. It does not claim that any production events were collected or that the funnel reflects observed user behavior.
