# -*- coding: utf-8 -*-
"""Execution & Memory Profiler Tool (tools/perf_profiler.py)"""
import time
from typing import Dict, Any
from contextlib import contextmanager

class ExecutionProfiler:
    """Profiles execution latency and tracks resource consumption."""
    def __init__(self):
        self.sections: Dict[str, float] = {}

    @contextmanager
    def profile_section(self, name: str):
        t0 = time.perf_counter()
        try:
            yield
        finally:
            t1 = time.perf_counter()
            self.sections[name] = round((t1 - t0) * 1000, 3)

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "latencies_ms": dict(self.sections),
            "total_ms": sum(self.sections.values())
        }
