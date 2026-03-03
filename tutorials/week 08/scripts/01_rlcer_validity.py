#!/usr/bin/env python3
# Example: Demonstrates RLCER-style rubric validity filtering and CoT reward shaping.
"""Tutorial 01: RLCER rubric validity filter on toy rollouts."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Rubric:
    name: str
    score: float
    satisfaction: List[int]


def pearson_binary(x: List[int], y: List[int]) -> float:
    """Pearson correlation for short binary vectors."""
    if len(x) != len(y) or not x:
        return 0.0
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    # Pearson numerator: sum_i (x_i - mean(x)) * (y_i - mean(y)).
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    # Pearson denominator: sqrt(sum_i (x_i-mean(x))^2) * sqrt(sum_i (y_i-mean(y))^2).
    den_x = math.sqrt(sum((a - mx) ** 2 for a in x))
    den_y = math.sqrt(sum((b - my) ** 2 for b in y))
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)


def minmax_normalize(values: List[float]) -> List[float]:
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0 for _ in values]
    # Min-max normalization: v' = (v - min) / (max - min).
    return [(v - lo) / (hi - lo) for v in values]


def main() -> None:
    # +1 means correct answer, -1 means incorrect answer.
    correctness = [1, 1, -1, -1]
    correct_as_binary = [1 if z == 1 else 0 for z in correctness]
    alpha = 0.2

    rubrics = [
        Rubric("handles carry correctly", +3.0, [1, 1, 0, 0]),
        Rubric("introduces irrelevant tangent", -2.0, [0, 0, 1, 1]),
        Rubric("always present boilerplate", +1.0, [1, 1, 1, 1]),
    ]

    print("=== Rubric validity (corr > alpha and non-saturated) ===")
    valid: Dict[str, bool] = {}
    for r in rubrics:
        corr = pearson_binary(r.satisfaction, correct_as_binary)
        saturated = len(set(r.satisfaction)) == 1
        # Valid rubric rule: corr(v, correctness) > alpha and std(v) > 0.
        is_valid = (corr > alpha) and (not saturated)
        valid[r.name] = is_valid
        print(
            f"- {r.name:32s} corr={corr:+.3f} saturated={saturated} valid={is_valid}"
        )

    raw_cot_rewards: List[float] = []
    for i in range(len(correctness)):
        reward = 0.0
        for r in rubrics:
            if valid[r.name] and r.satisfaction[i] == 1:
                reward += r.score
        raw_cot_rewards.append(reward)

    norm_cot_rewards = minmax_normalize(raw_cot_rewards)
    # Combined reward: r_total = r_outcome + r_cot.
    reasoner_rewards = [z + c for z, c in zip(correctness, norm_cot_rewards)]

    print("\n=== Reward signals per rollout ===")
    for i, (z, raw, norm, total) in enumerate(
        zip(correctness, raw_cot_rewards, norm_cot_rewards, reasoner_rewards), start=1
    ):
        print(
            f"rollout {i}: outcome={z:+.1f} cot_raw={raw:+.1f} cot_norm={norm:.2f} total={total:+.2f}"
        )


if __name__ == "__main__":
    main()
