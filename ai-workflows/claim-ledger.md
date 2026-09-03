# Claim Ledger for AI-Assisted Research

## Purpose

A claim ledger is a structured record of what an AI-assisted research workflow believes it knows, why it believes it, and what still requires verification.

The ledger separates fluent output from evidentiary status. It is useful whenever source material is being summarized, compared, retrieved, or transformed into public-facing work.

## Minimal schema

| Field | Meaning |
|---|---|
| `claim_id` | Stable identifier for the claim |
| `claim_text` | Concise proposition being evaluated |
| `claim_type` | Fact, inference, hypothesis, opinion, or instruction |
| `source_refs` | Exact source identifiers supporting or contradicting the claim |
| `support_status` | Supported, mixed, unsupported, or not yet checked |
| `confidence` | Workflow confidence, not objective probability |
| `verification` | None, secondary-source check, or primary-source check |
| `scope` | Context in which the claim is intended to hold |
| `risk_level` | Low, medium, or high consequence if wrong |
| `review_status` | Draft, reviewed, approved, rejected, or superseded |
| `updated_at` | Timestamp of the latest material assessment |
| `notes` | Uncertainty, conflicts, or next verification step |

## Synthetic JSONL example

```json
{"claim_id":"C-001","claim_text":"The evaluation dataset contains 500 synthetic records.","claim_type":"fact","source_refs":["dataset_manifest_v1.json"],"support_status":"supported","confidence":0.99,"verification":"primary-source check","scope":"evaluation dataset v1","risk_level":"low","review_status":"reviewed","updated_at":"2026-09-03T00:00:00Z","notes":"Count verified against the manifest."}
{"claim_id":"C-002","claim_text":"The revised prompt reduces unsupported answers.","claim_type":"hypothesis","source_refs":["experiment_plan_v2.md"],"support_status":"not yet checked","confidence":0.50,"verification":"none","scope":"planned synthetic benchmark","risk_level":"medium","review_status":"draft","updated_at":"2026-09-03T00:00:00Z","notes":"Requires a preregistered comparison before publication as a result."}
```

The records are synthetic and illustrate state representation only. They do not report a completed experiment.

## Validation rules

1. Every factual claim must identify at least one source or remain unsupported.
2. A source reference must point to a recoverable item, not a vague description.
3. Confidence must never replace support status or verification level.
4. Inferences must identify the facts from which they were derived.
5. Contradictory evidence must remain attached to the same claim record.
6. High-risk claims require primary-source verification before approval.
7. Superseded claims remain traceable rather than silently disappearing.
8. Public outputs must not exceed the scope recorded in the ledger.

## Useful evaluations

A ledger can support simple quality measures:

```text
source_coverage = claims_with_source_refs / factual_claims
primary_verification_rate = primary_verified_claims / high_risk_claims
unsupported_claim_rate = unsupported_factual_claims / factual_claims
review_completion_rate = reviewed_or_approved_claims / all_claims
```

These measures are workflow diagnostics. They do not prove that an individual claim is true.

## Relationship to the human review gate

The claim ledger supplies structured evidence to the review gate:

- the ledger tracks epistemic status;
- the gate makes the publication decision;
- neither component should silently upgrade an inference into a verified fact.

This separation makes review more inspectable and gives later corrections a stable target.

## Status and provenance

Working pattern for future extension into code, tests, or a small validation utility. This note was developed through an AI-assisted workflow under Neal Vazquez's direction and is published as methodology, not as evidence of completed empirical research.
