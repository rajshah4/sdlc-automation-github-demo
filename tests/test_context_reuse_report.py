from __future__ import annotations

from pathlib import Path

from scripts.build_context_reuse_report import build_report, main


ROOT = Path(__file__).resolve().parents[1]


def test_context_reuse_report_includes_all_memory_sources() -> None:
    report = build_report(
        ROOT,
        fixture=ROOT / "tests" / "fixtures" / "github_issue_labeled_context.json",
    )

    assert "AGENTS.md" in report
    assert "sdlc-context-reuse" in report
    assert "Existing Logs And Evidence" in report
    assert "Targeted GitHub Repo Search" in report
    assert "Previous Agent Runs" in report
    assert "Low-cost model" in report or "low-cost model" in report
    assert "Terraform Analogy" in report


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
    assert "Cost-Aware Context Reuse Report" in text
    assert "Token Reuse Estimate" in text
