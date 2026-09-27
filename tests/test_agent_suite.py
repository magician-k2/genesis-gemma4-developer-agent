# -*- coding: utf-8 -*-
"""Real E2E Integration Test Suite for Gemma 4 Agent (tests/test_agent_suite.py)"""
import os
import sys
import unittest
import tempfile
from pathlib import Path

# Add parent to path
PKG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PKG_ROOT))

from src.agent_core import Gemma4Agent

class TestGemma4DeveloperAgent(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        # Create a sample buggy Python file
        self.bug_file = self.repo / "math_utils.py"
        with open(self.bug_file, "w", encoding="utf-8") as f:
            f.write("def divide(a, b):\n    return a / b\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_solve_zero_division(self):
        agent = Gemma4Agent()
        desc = """Traceback (most recent call last):
  File "math_utils.py", line 2, in divide
    return a / b
ZeroDivisionError: division by zero"""
        result = agent.solve_issue(str(self.repo), desc)
        self.assertEqual(result["status"], "RESOLVED")
        self.assertTrue(result["ast_audit"])
        self.assertIn("if b == 0:", result["patch"])

if __name__ == "__main__":
    unittest.main()
