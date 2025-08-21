import json
from ai_testgen.schemas import load_and_validate

def test_schema_ok():
    data = {
        "feature": "Sample",
        "cases": [{
            "id": "TC-001",
            "title": "ok",
            "description": "",
            "preconditions": [],
            "steps": [{"action": "do", "expected": "see"}],
            "priority": "P2",
            "tags": [],
            "negative": False
        }]
    }
    suite = load_and_validate(data)
    assert suite.feature == "Sample"
    assert suite.cases[0].id == "TC-001"
