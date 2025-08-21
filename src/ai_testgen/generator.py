import json
from pathlib import Path
from typing import Dict, Any

import yaml

from .llm import OpenAILLM, OfflineMockLLM
from .schemas import load_and_validate, TestSuite

def build_user_prompt(yaml_text: str, cases: int) -> str:
    return (
        f"Feature description:\n{yaml_text}\n\n"
        f"Generate ~{cases} diverse test cases (mix of P0..P3, positive+negative)."
        f" Use concise language; IDs like TC-001."
    )

def read_input(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    # Accept .yaml, .yml, .txt – we pass verbatim to LLM
    return text

def generate_suite(
    feature_file: Path,
    cases: int = 8,
    offline: bool = False,
    system_path: Path | None = None,
    user_path: Path | None = None,
) -> TestSuite:
    system_prompt = (
        (system_path or Path(__file__).with_name("../..") / "prompts" / "system.md")
        .resolve().read_text(encoding="utf-8")
    )
    # If a custom user prompt is supplied, append it after the constructed one
    base_yaml = read_input(feature_file)
    user_prompt = build_user_prompt(base_yaml, cases)
    if user_path:
        user_prompt += "\n\n" + Path(user_path).read_text(encoding="utf-8")

    llm = OfflineMockLLM() if offline else OpenAILLM()
    raw = llm.generate_json(system_prompt, user_prompt)
    suite = load_and_validate(raw)
    return suite

def save_json(suite: TestSuite, out_path: Path) -> None:
    out_path.write_text(suite.model_dump_json(indent=2), encoding="utf-8")
