# AI Test Case Generator (POC)

Generate **structured test cases** from natural language and render **pytest** tests automatically.

## What it does
- Takes a feature description (YAML or text)
- Uses an LLM to produce **JSON** test cases conforming to a strict **Pydantic** schema
- Renders the suite into an executable **pytest** file
- Works **offline** (mock mode) for demos

## Quickstart
```bash
python -m venv .venv && . .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -e .
cp .env.example .env   # add your OPENAI_API_KEY
make quickstart        # generates sample tests from examples/login.feature.yaml
pytest -q
