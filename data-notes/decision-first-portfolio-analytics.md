# Decision-first analytics for a professional portfolio

**Date:** 2026-09-05  
**Area:** Data science / digital analytics  
**Status:** Proposed measurement framework, not observed performance data

## Question

How can a portfolio dashboard measure progress toward real outcomes without becoming a collection of vanity metrics?

## Start with decisions

A useful metric should change a decision. For a professional portfolio, the core decisions are usually:

1. Which work deserves more visibility?
2. Which visitor paths produce meaningful engagement?
3. Where does interest fail to become contact, support, or subscription?
4. Which acquisition sources bring qualified attention rather than raw traffic?

This suggests a hierarchy instead of a flat event list.

## Measurement hierarchy

| Layer | Purpose | Examples |
|---|---|---|
| Outcome | Represent value created | qualified contact, service inquiry, paid subscription |
| Intent | Show serious consideration | résumé download, case-study depth, return visit |
| Engagement | Explain movement toward intent | section views, project opens, meaningful reading depth |
| Acquisition | Describe how attention arrived | source, campaign, landing page |
| Guardrail | Detect misleading success | form errors, immediate exits, duplicate events |

Outcome metrics answer whether the site is working. The other layers help explain why.

## Funnel model

A compact portfolio funnel can be modeled as:

```text
qualified sessions
  -> meaningful engagement
  -> high-intent action
  -> completed outcome
```

Each transition should have an explicit denominator:

```text
engagement rate = meaningfully engaged sessions / qualified sessions
intent rate     = sessions with high-intent action / engaged sessions
outcome rate    = completed outcomes / high-intent sessions
```

The denominators matter because an increase in raw traffic can coexist with a weaker audience and fewer valuable outcomes.

## Event design rule

Track semantic actions, not interface accidents. An event such as `service_inquiry_submitted` survives a button redesign. An event named `gold_button_clicked` does not.

A minimal event record might include:

```json
{
  "event_name": "portfolio_item_opened",
  "content_type": "research_note",
  "content_id": "decision_first_analytics",
  "entry_surface": "data_dashboard"
}
```

Avoid sending names, email addresses, message text, or other personally identifying form fields into analytics events.

## Interpretation discipline

Dashboard labels should separate:

- **measurement**, what the instrumentation directly recorded;
- **inference**, what the pattern may indicate;
- **decision**, what action the evidence supports;
- **uncertainty**, what remains unknown.

For example, repeated résumé downloads are evidence of download activity. They are not, by themselves, evidence of recruiter interest. The dashboard becomes more credible when that distinction remains visible.

## Practical release test

Before adding a metric, ask:

1. What decision can this change?
2. What is its denominator?
3. How could instrumentation inflate it?
4. What privacy cost does it introduce?
5. What companion metric prevents misinterpretation?

If those questions have no clear answers, the metric probably does not belong on the primary dashboard.
