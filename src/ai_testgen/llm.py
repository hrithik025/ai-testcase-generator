import json
import os
import re
from typing import Any, Dict, List

from openai import OpenAI  # Official SDK
# Chat Completions / Responses APIs: see OpenAI docs.  :contentReference[oaicite:3]{index=3}

JSON_RE = re.compile(r"\{.*\}", re.DOTALL)

class OpenAILLM:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI()

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Ask the model to return strict JSON. We request JSON mode; if output
        wraps code fences, we still robustly extract the JSON object.
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            # JSON response mode where supported
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        content = resp.choices[0].message.content or ""
        m = JSON_RE.search(content)
        return json.loads(m.group(0)) if m else json.loads(content)

class OfflineMockLLM:
    """Deterministic offline generator for demos / CI without API keys."""
    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        return {
            "feature": "User Login",
            "cases": [
                {
                    "id": "TC-001",
                    "title": "Successful login",
                    "description": "Valid user reaches dashboard.",
                    "preconditions": ["User exists", "Account active"],
                    "steps": [
                        {"action": "Open /login", "expected": "Login form visible"},
                        {"action": "Enter valid email & password", "expected": "Fields accept input"},
                        {"action": "Click Login", "expected": "Redirect to /dashboard"},
                    ],
                    "priority": "P0",
                    "tags": ["happy", "login"],
                    "negative": False,
                },
                {
                    "id": "TC-002",
                    "title": "Lockout after 5 failures",
                    "description": "Brute-force protection.",
                    "preconditions": ["Account not locked"],
                    "steps": [
                        {"action": "Enter wrong password 5 times", "expected": "Account locked"},
                        {"action": "Try valid creds", "expected": "Login blocked with lockout message"},
                    ],
                    "priority": "P1",
                    "tags": ["security", "lockout"],
                    "negative": True,
                },
            ],
        }
