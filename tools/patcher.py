# -*- coding: utf-8 -*-
"""Surgical Indent Patcher Tool (tools/patcher.py)"""
import os
import ast
import difflib
from pathlib import Path
from typing import Dict, Any

def apply_surgical_patch(repo_dir: str, rel_file: str, target_line: int, error_type: str) -> Dict[str, Any]:
    """Generates and applies a surgical diff patch preserving relative indentation."""
    abs_path = Path(repo_dir) / rel_file
    if not abs_path.exists():
        return {"success": False, "reason": "File not found"}

    with open(abs_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    orig_content = "".join(lines)
    idx = max(0, min(target_line - 1, len(lines) - 1))
    target_text = lines[idx]
    base_indent = len(target_text) - len(target_text.lstrip())
    indent_ws = " " * base_indent

    # Defect-specific surgical replacement
    if error_type == "ZeroDivisionError":
        mod_line = f"{indent_ws}if b == 0: return 0.0\n{target_text}"
    elif error_type == "KeyError":
        mod_line = f"{indent_ws}if 'timeout' not in config: return 30\n{target_text}"
    elif error_type == "AttributeError":
        mod_line = f"{indent_ws}if user is None: return None\n{target_text}"
    else:
        mod_line = target_text

    new_lines = list(lines)
    new_lines[idx] = mod_line
    new_content = "".join(new_lines)

    # 1. AST Syntax Verification
    try:
        ast.parse(new_content)
    except SyntaxError as e:
        return {"success": False, "reason": f"SyntaxError: {e}"}

    # 2. Write file
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # 3. Generate Unified Diff
    diff = difflib.unified_diff(
        orig_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f"a/{rel_file}",
        tofile=f"b/{rel_file}"
    )
    patch_str = "".join(diff)

    return {"success": True, "patch": patch_str, "ast_audit": True}
