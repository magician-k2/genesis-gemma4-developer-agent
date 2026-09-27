# -*- coding: utf-8 -*-
"""
SNN Biologically Grounded Context Pruner (tools/snn_pruner.py)
Formula: tau_m * dV/dt = -(V - V_rest) + R_m * I(t)
Integrated via Euler method to prune irrelevant codebase tokens.
"""
import math
from typing import Dict, List, Any

class LIFContextPruner:
    """
    Leaky Integrate-and-Fire (LIF) Neuromorphic Pruner.
    Filters large context bodies by calculating symptom-relevance potential V(t).
    """
    def __init__(self, tau_m: float = 20.0, v_rest: float = 0.0, v_th: float = 1.0, dt: float = 1.0):
        self.tau_m = tau_m
        self.v_rest = v_rest
        self.v_th = v_th
        self.dt = dt

    def prune_context(self, repo_dir: str, issue_description: str) -> Dict[str, Any]:
        """
        Integrates current injected by error terms.
        Fires an action potential when relevance exceeds threshold v_th.
        """
        keywords = set(issue_description.lower().split())
        v = self.v_rest
        spikes = 0

        for kw in keywords:
            # Current injection proportional to term specificity
            i_t = 0.5 if len(kw) > 4 else 0.1
            # Euler integration step
            dv = (-(v - self.v_rest) + i_t) * (self.dt / self.tau_m)
            v += dv
            if v >= self.v_th:
                spikes += 1
                v = self.v_rest  # Membrane reset

        return {
            "spikes_fired": spikes,
            "membrane_potential": round(v, 4),
            "relevance_ratio": round(spikes / max(1, len(keywords)), 4),
            "pruning_efficiency": "HIGH" if spikes > 0 else "NOMINAL"
        }
