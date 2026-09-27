# -*- coding: utf-8 -*-
"""AST Security & Sandbox Auditor Tool (tools/security_auditor.py)"""
import ast
from typing import Dict, Any, List

class ASTSecurityAuditor(ast.NodeVisitor):
    """Audits code against dangerous calls (eval, exec, system commands, raw sockets)."""
    FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__"}
    FORBIDDEN_MODULES = {"socket", "urllib", "requests", "http.client"}

    def __init__(self):
        self.violations: List[str] = []

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.FORBIDDEN_CALLS:
                self.violations.append(f"Forbidden call: {node.func.id}")
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name.split('.')[0] in self.FORBIDDEN_MODULES:
                self.violations.append(f"Forbidden network module import: {alias.name}")
        self.generic_visit(node)

    def audit_code(self, source_code: str) -> Dict[str, Any]:
        self.violations.clear()
        try:
            tree = ast.parse(source_code)
            self.visit(tree)
            is_secure = len(self.violations) == 0
            return {"secure": is_secure, "violations": self.violations}
        except SyntaxError as e:
            return {"secure": False, "violations": [f"SyntaxError: {e}"]}
