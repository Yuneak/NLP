#!/usr/bin/env python3
# Example: Demonstrates PARL reward tradeoffs and auxiliary-term annealing.
"""Tutorial 12: PARL reward shaping for parallel orchestrator training."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class PolicyStats:
    name: str
    r_parallel: float
    r_finish: float
    r_perf: float


def parl_reward(stats: PolicyStats, lambda_1: float, lambda_2: float) -> float:
    # PARL reward formula:
    # r_PARL = lambda_1 * r_parallel + lambda_2 * r_finish + r_perf
    return lambda_1 * stats.r_parallel + lambda_2 * stats.r_finish + stats.r_perf


def lambda_schedule(step: int, total_steps: int, start: float) -> float:
    # Linear anneal to zero over training:
    # lambda(step) = start * (1 - step/total_steps).
    ratio = max(0.0, 1.0 - (step / total_steps))
    return start * ratio


def rank_policies(
    policies: List[PolicyStats], lambda_1: float, lambda_2: float
) -> List[Tuple[str, float]]:
    scores = [(p.name, parl_reward(p, lambda_1, lambda_2)) for p in policies]
    return sorted(scores, key=lambda x: x[1], reverse=True)


def main() -> None:
    policies = [
        PolicyStats("serial_collapse", r_parallel=0.0, r_finish=0.95, r_perf=0.58),
        PolicyStats("spurious_parallelism", r_parallel=1.00, r_finish=0.20, r_perf=0.42),
        PolicyStats("balanced_decomposition", r_parallel=0.75, r_finish=0.88, r_perf=0.79),
    ]

    total_steps = 6
    lambda_1_start = 0.45
    lambda_2_start = 0.45

    print("=== PARL reward with annealed auxiliary terms ===")
    print("Columns: step, lambda_1, lambda_2, top policy")
    for step in range(total_steps + 1):
        lambda_1 = lambda_schedule(step, total_steps, lambda_1_start)
        lambda_2 = lambda_schedule(step, total_steps, lambda_2_start)
        ranked = rank_policies(policies, lambda_1, lambda_2)
        top_name, top_score = ranked[0]
        print(
            f"- step={step} | lambda_1={lambda_1:.2f} lambda_2={lambda_2:.2f}"
            f" | top={top_name} score={top_score:.3f}"
        )

    print("\nFinal-step ranking (auxiliary terms fully annealed):")
    for name, score in rank_policies(policies, 0.0, 0.0):
        print(f"- {name:20s} -> {score:.3f}")
    print("\nUse case: illustrate how PARL avoids serial collapse and spurious parallelism.")


if __name__ == "__main__":
    main()
