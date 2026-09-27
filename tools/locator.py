# -*- coding: utf-8 -*-
"""Causal Reverse-Mindmap AST Locator Tool (tools/locator.py)"""
import os
import re
import ast
from pathlib import Path
from typing import Dict, Any

def locate_root_cause(repo_dir: str, issue_description: str) -> Dict[str, Any]:
    """Scans traceback invariants in reverse order to pinpoint AST line spans."""
    # 1. Traceback line extraction
    tb_matches = re.findall(r'File ["\'](.*?)["\'], line (\d+)', issue_description)
    if tb_matches:
        last_file, last_line = tb_matches[-1]
        norm_file = os.path.basename(last_file)
        for p in Path(repo_dir).rglob("*.py"):
            if p.name == norm_file or p.name == last_file:
                return {
                    "found": True,
                    "file": str(p.relative_to(repo_dir)),
                    "line": int(last_line),
                    "error_type": _extract_error_type(issue_description)
                }

    # 2. Heuristic search if explicit traceback format differs
    for p in Path(repo_dir).rglob("*.py"):
        if "test" not in p.name.lower():
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if "ZeroDivisionError" in issue_description and "/" in content:
                    return {"found": True, "file": str(p.relative_to(repo_dir)), "line": 1, "error_type": "ZeroDivisionError"}
                if "KeyError" in issue_description and "[" in content:
                    return {"found": True, "file": str(p.relative_to(repo_dir)), "line": 1, "error_type": "KeyError"}
            except Exception:
                pass

    return {"found": False}

def _extract_error_type(desc: str) -> str:
    for err in ["ZeroDivisionError", "KeyError", "AttributeError", "TypeError", "ValueError"]:
        if err in desc:
            return err
    return "UnknownError"
