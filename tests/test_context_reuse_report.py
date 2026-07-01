from __future__ import annotations

from pathlib import Path

from scripts.build_context_reuse_report import build_report, main


ROOT = Path(__file__).resolve().parents[1]


def test_context_reuse_report_includes_all_memory_sources() -> None:
    report = build_report(
        ROOT,
        fixture=ROOT / "tests" / "fixtures" / "github_issue_labeled_context.json",
    )

    assert "Context Scout Issue Brief" in report
    assert "Customers are seeing pets that are not available" in report
    assert "Existing Code Or New PR?" in report
    assert "Cited Handoff Material" in report
    assert "do not open a code PR" in report
    assert 'assert "Nova" not in {pet.name for pet in pets}' in report
    assert "app/petstore_app/catalog.py" in report
    assert "app/web/app.js" in report
    assert "AGENTS.md" in report
    assert "docs/repo-memory/petstore-intelligence.md" in report
    assert "lower-cost model" in report
    assert "Targeted GitHub Repo Search" not in report
    assert "Search terms:" not in report


def test_context_reuse_cli_writes_report(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "report.md"
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_context_reuse_report.py",
            "--fixture",
            str(ROOT / "tests" / "fixtures" / "github_issue_labeled_context.json"),
            "--output",
            str(output),
        ],
    )

    assert main() == 0
    text = output.read_text(encoding="utf-8")
    assert "Context Scout Issue Brief" in text
    assert "Existing Code Or New PR?" in text
    assert "Cost Routing" in text
