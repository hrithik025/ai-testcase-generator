from pathlib import Path
from typing import Optional

import typer
from rich import print

from .generator import generate_suite
from .renderer import render_pytest

app = typer.Typer(help="AI Test Case Generator")

@app.command("generate")
def generate(
    in_: Path = typer.Option(..., "--in", help="Feature .yaml/.txt"),
    out: Path = typer.Option(..., "--out", help="Output pytest file"),
    cases: int = typer.Option(8, "--cases", help="Approx number of cases"),
    model: Optional[str] = typer.Option(None, "--model", help="Override OPENAI_MODEL"),
    offline: bool = typer.Option(False, "--offline", help="Skip API; use mock generator"),
):
    if model:
        import os
        os.environ["OPENAI_MODEL"] = model

    suite = generate_suite(in_, cases=cases, offline=offline)
    code = render_pytest(suite)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(code, encoding="utf-8")
    print(f"[green]Wrote[/green] {out}")

if __name__ == "__main__":
    app()
