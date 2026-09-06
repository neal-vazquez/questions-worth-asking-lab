#!/usr/bin/env python3
"""Validate the lab's analytics measurement contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

UI_TOKENS = {"red", "blue", "green", "gold", "button", "div", "modal", "left", "right"}


def validate_spec(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    funnel = spec.get("funnel", {})
    stages = funnel.get("stages", [])
    events = spec.get("events", [])

    if not stages or len(stages) != len(set(stages)):
        errors.append("funnel stages must be non-empty and unique")
        return errors
    if not isinstance(events, list) or not events:
        return errors + ["events must be a non-empty list"]

    names: list[str] = []
    counts = {stage: 0 for stage in stages}
    blocked = {str(x).lower() for x in spec.get("privacy", {}).get("sensitive_property_names", [])}

    for i, event in enumerate(events):
        prefix = f"events[{i}]"
        name = event.get("event_name", "")
        stage = event.get("stage")
        trigger = event.get("trigger", "")
        entity = event.get("entity", "")
        props = event.get("required_properties", [])

        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix}.event_name is required")
        else:
            names.append(name)
            tokens = set(name.lower().replace("-", "_").split("_"))
            if tokens & UI_TOKENS:
                errors.append(f"{prefix}.event_name is coupled to UI implementation")

        if stage not in counts:
            errors.append(f"{prefix}.stage is invalid")
        else:
            counts[stage] += 1
        if not isinstance(trigger, str) or len(trigger.strip()) < 12:
            errors.append(f"{prefix}.trigger must describe the semantic trigger")
        if not isinstance(entity, str) or not entity.strip():
            errors.append(f"{prefix}.entity is required")
        if not isinstance(props, list) or not all(isinstance(x, str) and x for x in props):
            errors.append(f"{prefix}.required_properties must be a list of names")
        else:
            if len(props) != len(set(props)):
                errors.append(f"{prefix}.required_properties contains duplicates")
            leaked = sorted({x.lower() for x in props} & blocked)
            if leaked and not spec.get("privacy", {}).get("pii_allowed", False):
                errors.append(f"{prefix} requires disallowed sensitive properties: {', '.join(leaked)}")

    dupes = sorted({name for name in names if names.count(name) > 1})
    if dupes:
        errors.append("duplicate event_name values: " + ", ".join(dupes))

    missing = [stage for stage, count in counts.items() if count == 0]
    if missing:
        errors.append("every funnel stage needs an event; missing: " + ", ".join(missing))
    return errors


def load_spec(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("spec root must be a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    try:
        spec = load_spec(args.spec)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID: {exc}")
        return 2
    errors = validate_spec(spec)
    if errors:
        print("INVALID measurement spec")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"VALID measurement spec: {len(spec['events'])} events across {len(spec['funnel']['stages'])} stages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
