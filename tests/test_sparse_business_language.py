from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "skills" / "sdlc-story" / "scripts" / "extract_acceptance_criteria.py"


def extract(title: str, body: str = "") -> dict:
    result = subprocess.run(
        [sys.executable, str(EXTRACT), title],
        input=body,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_budget_language_maps_to_adoption_fee_filter() -> None:
    data = extract(
        "Families need to find pets in their budget",
        "Adoption counselors say families keep asking to see pets they can afford before they visit.",
    )

    assert data["has_sparse_issue_shape"] is True
    assert "Catalog search accepts an optional max adoption fee in cents." in data["inferred_acceptance_criteria"]


def test_ambiguous_pet_price_language_does_not_infer_a_fix() -> None:
    data = extract("People are confused by pet prices", "This came up in the intake review. Can we fix it?")

    assert data["has_sparse_issue_shape"] is False
    assert data["inferred_acceptance_criteria"] == []
