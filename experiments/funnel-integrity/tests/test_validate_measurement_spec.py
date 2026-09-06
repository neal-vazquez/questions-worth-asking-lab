import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from validate_measurement_spec import load_spec, validate_spec  # noqa: E402


class MeasurementSpecTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = load_spec(HERE / "funnel_spec.json")

    def test_checked_in_spec_is_valid(self) -> None:
        self.assertEqual(validate_spec(self.spec), [])

    def test_duplicate_event_name_is_rejected(self) -> None:
        mutated = json.loads(json.dumps(self.spec))
        mutated["events"][1]["event_name"] = mutated["events"][0]["event_name"]
        errors = validate_spec(mutated)
        self.assertTrue(any("duplicate event_name" in error for error in errors))

    def test_pii_property_is_rejected(self) -> None:
        mutated = json.loads(json.dumps(self.spec))
        mutated["events"][0]["required_properties"].append("email")
        errors = validate_spec(mutated)
        self.assertTrue(any("sensitive properties" in error for error in errors))

    def test_missing_stage_coverage_is_rejected(self) -> None:
        mutated = json.loads(json.dumps(self.spec))
        mutated["events"] = [
            event for event in mutated["events"] if event["stage"] != "assisted"
        ]
        errors = validate_spec(mutated)
        self.assertTrue(any("missing: assisted" in error for error in errors))

    def test_ui_coupled_event_name_is_rejected(self) -> None:
        mutated = json.loads(json.dumps(self.spec))
        mutated["events"][0]["event_name"] = "gold_button_clicked"
        errors = validate_spec(mutated)
        self.assertTrue(any("coupled to UI implementation" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
