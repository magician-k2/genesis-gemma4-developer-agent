# -*- coding: utf-8 -*-
"""Multi-File Dependency DAG Resolver Tool (tools/dag_resolver.py)"""
import os
import ast
from pathlib import Path
from typing import Dict, List, Any

class DependencyDAGResolver:
    """Builds and queries the import DAG across repository files to prevent regression."""
    def __init__(self):
        pass

    def resolve_dependencies(self, repo_dir: str, target_file: str) -> Dict[str, Any]:
        target_stem = Path(target_file).stem
        dependents: List[str] = []

        for p in Path(repo_dir).rglob("*.py"):
            if str(p.relative_to(repo_dir)) == target_file:
                continue
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            if target_stem in name.name:
                                dependents.append(str(p.relative_to(repo_dir)))
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and target_stem in node.module:
                            dependents.append(str(p.relative_to(repo_dir)))
            except Exception:
                pass

        return {
            "target": target_file,
            "dependents": list(set(dependents))
        }
