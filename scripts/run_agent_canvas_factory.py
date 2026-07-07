#!/usr/bin/env python3
# Forwards the legacy orchestrator path to the packaged Agent Canvas script.
"""Compatibility wrapper for the Agent Canvas factory orchestrator."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "agent-canvas" / "scripts" / "run_agent_canvas_factory.py"
sys.path.insert(0, str(TARGET.parent))
runpy.run_path(str(TARGET), run_name="__main__")
