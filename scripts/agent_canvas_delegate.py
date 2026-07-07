#!/usr/bin/env python3
# Forwards the legacy delegate-helper path to the packaged Agent Canvas script.
"""Compatibility wrapper for the Agent Canvas API helper."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "agent-canvas" / "scripts" / "agent_canvas_delegate.py"
sys.path.insert(0, str(TARGET.parent))
runpy.run_path(str(TARGET), run_name="__main__")
