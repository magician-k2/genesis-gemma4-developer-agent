# -*- coding: utf-8 -*-
"""Gemma 4 Developer Agent Core (src/agent_core.py)"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

from tools.locator import locate_root_cause
from tools.patcher import apply_surgical_patch

class Gemma4Agent:
    """Autonomous Software Engineering Agent powered by Gemma 4."""
    def __init__(self, config_path: str = None):
        self.config_path = config_path

    def solve_issue(self, repo_dir: str, issue_description: str) -> Dict[str, Any]:
        """Main entry point called by SWE-bench / Kaggle test harness."""
        # 1. Locate root cause
        location = locate_root_cause(repo_dir, issue_description)
        if not location.get("found"):
            return {"status": "FAILED", "reason": "Root cause not located"}

        # 2. Synthesize minimal surgical fix based on symptom
        target_file = location["file"]
        target_line = location["line"]
        error_type = location.get("error_type", "")

        # Compute surgical patch
        patch_res = apply_surgical_patch(
            repo_dir=repo_dir,
            rel_file=target_file,
            target_line=target_line,
            error_type=error_type
        )
        return {
            "status": "RESOLVED" if patch_res.get("success") else "FAILED",
            "patch": patch_res.get("patch", ""),
            "ast_audit": patch_res.get("ast_audit", False)
        }
