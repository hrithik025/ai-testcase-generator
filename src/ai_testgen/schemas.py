from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ValidationError

class Step(BaseModel):
    action: str = Field(..., min_length=1)
    expected: str = Field(..., min_length=1)

class TestCase(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: Optional[str] = ""
    preconditions: List[str] = []
    steps: List[Step]
    priority: Literal["P0", "P1", "P2", "P3"] = "P2"
    tags: List[str] = []
    negative: bool = False

class TestSuite(BaseModel):
    feature: str
    cases: List[TestCase]

def load_and_validate(json_obj: dict) -> TestSuite:
    try:
        return TestSuite.model_validate(json_obj)
    except ValidationError as e:
        # Make the error message friendly for CLI
        raise SystemExit(f"[SchemaError]\n{e}") from e
