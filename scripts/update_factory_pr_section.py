#!/usr/bin/env python3
# Forwards the legacy PR-section updater path to the packaged Canvas script.
"""Compatibility wrapper for the Agent Canvas PR section updater."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "agent-canvas" / "scripts" / "update_factory_pr_section.py"
sys.path.insert(0, str(TARGET.parent))
runpy.run_path(str(TARGET), run_name="__main__")
