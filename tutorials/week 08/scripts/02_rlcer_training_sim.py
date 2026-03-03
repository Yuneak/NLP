#!/usr/bin/env python3
# Example: Compares outcome-only, rubric-only, and combined learning signals in a toy loop.
"""Tutorial 02: Mini RLCER-style training simulation."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Policy:
    # Probability of choosing "good reasoning" per problem.
    p_good: float = 0.5


def sample_rollout(policy: Policy) -> Tuple[int, Dict[str, int]]:
    """Return (correctness, rubric_satisfaction)."""
    good = 1 if random.random() < policy.p_good else 0
    correct = 1 if (good and random.random() < 0.9) or ((not good) and random.random() < 0.2) else -1

    rubrics = {
        "step_consistency": 1 if (good and random.random() < 0.9) else 0,
        "irrelevant_tangent": 1 if ((not good) and random.random() < 0.8) else 0,
    }
    return correct, rubrics


def validity_for_rubric(samples: List[Tuple[int, Dict[str, int]]], name: str, alpha: float = 0.2) -> bool:
    zs = [1 if s[0] == 1 else 0 for s in samples]
    vs = [s[1][name] for s in samples]
    if len(set(vs)) == 1:
        return False
    # Simple covariance / variance based correlation for small vectors.
    mz = sum(zs) / len(zs)
    mv = sum(vs) / len(vs)
    # Covariance: sum_i (z_i - mean(z)) * (v_i - mean(v)).
    cov = sum((z - mz) * (v - mv) for z, v in zip(zs, vs))
    # Variances: sum_i (z_i - mean(z))^2 and sum_i (v_i - mean(v))^2.
    vz = sum((z - mz) ** 2 for z in zs)
    vv = sum((v - mv) ** 2 for v in vs)
    # Correlation: corr = cov / sqrt(vz * vv).
    corr = cov / ((vz * vv) ** 0.5) if vz > 0 and vv > 0 else 0.0
    return corr > alpha


def train(regime: str, epochs: int = 120, batch_size: int = 10) -> List[float]:
    policy = Policy(0.5)
    history = []
    rubric_scores = {"step_consistency": 1.0, "irrelevant_tangent": -1.0}

    for _ in range(epochs):
        batch = [sample_rollout(policy) for _ in range(batch_size)]
        avg_acc = sum(1 if z == 1 else 0 for z, _ in batch) / batch_size
        history.append(avg_acc)

        if regime == "outcome_only":
            # Outcome-only reward: r = mean(z_i).
            reward = sum(z for z, _ in batch) / batch_size
        elif regime == "rubric_only":
            valid = {
                r: validity_for_rubric(batch, r) for r in rubric_scores
            }
            reward = 0.0
            for _, rb in batch:
                # Rubric-only reward: r = mean(sum_k s_k * 1[valid_k and satisfied_k]).
                reward += sum(rubric_scores[k] for k, v in rb.items() if valid[k] and v == 1)
            reward /= batch_size
        elif regime == "combined":
            valid = {
                r: validity_for_rubric(batch, r) for r in rubric_scores
            }
            cot_reward = 0.0
            out_reward = 0.0
            for z, rb in batch:
                out_reward += z
                cot_reward += sum(rubric_scores[k] for k, v in rb.items() if valid[k] and v == 1)
            # Combined reward: r = mean(outcome + cot_score).
            reward = (out_reward + cot_reward) / batch_size
        else:
            raise ValueError(f"Unknown regime: {regime}")

        # Policy update rule: p_good <- clip(p_good + lr * reward).
        policy.p_good += 0.03 * reward
        policy.p_good = max(0.01, min(0.99, policy.p_good))

    return history


def summarize(name: str, history: List[float]) -> None:
    early = sum(history[:20]) / 20
    late = sum(history[-20:]) / 20
    print(f"{name:12s} early_acc={early:.3f} late_acc={late:.3f} gain={late - early:+.3f}")


def main() -> None:
    random.seed(42)
    out = train("outcome_only")
    rub = train("rubric_only")
    combo = train("combined")

    print("=== Mini training comparison ===")
    summarize("outcome_only", out)
    summarize("rubric_only", rub)
    summarize("combined", combo)
    print("\nTip: run several times with different seeds for variance checks.")


if __name__ == "__main__":
    main()
