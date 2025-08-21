from pathlib import Path
from ai_testgen.generator import generate_suite

def test_offline_generation(tmp_path: Path):
    feature = tmp_path / "f.yaml"
    feature.write_text("feature: Demo\n", encoding="utf-8")
    suite = generate_suite(feature, cases=3, offline=True)
    assert suite.cases, "Should create demo cases without API"
