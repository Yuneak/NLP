#!/usr/bin/env python3
# Example: Runs weighted forward rule propagation on a tiny logical graph.
"""Tutorial 06: Tiny belief update on logical rule graph (forward reasoning)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Rule:
    premises: List[str]
    conclusion: str
    weight: float  # confidence in rule


def and_activation(premises: List[str], beliefs: Dict[str, float]) -> float:
    # AND activation formula: prod_i belief(premise_i).
    act = 1.0
    for p in premises:
        act *= beliefs.get(p, 0.0)
    return act


def noisy_or(incoming: List[float]) -> float:
    # Noisy-OR formula: 1 - prod_j (1 - m_j).
    prod = 1.0
    for x in incoming:
        prod *= (1.0 - x)
    return 1.0 - prod


def infer(rules: List[Rule], evidence: Dict[str, float], iterations: int = 6) -> Dict[str, float]:
    beliefs = dict(evidence)
    for _ in range(iterations):
        contributions: Dict[str, List[float]] = {}
        for rule in rules:
            act = and_activation(rule.premises, beliefs)
            # Weighted message formula: m = activation * rule_weight.
            msg = act * rule.weight
            contributions.setdefault(rule.conclusion, []).append(msg)
        for node, msgs in contributions.items():
            beliefs[node] = max(beliefs.get(node, 0.0), noisy_or(msgs))
    return beliefs


def main() -> None:
    rules = [
        Rule(["A"], "B", 0.9),
        Rule(["B"], "C", 0.8),
        Rule(["A", "B"], "D", 0.7),
    ]
    evidence = {"A": 1.0}
    beliefs = infer(rules, evidence)

    print("=== Forward logical-probabilistic inference ===")
    for k in sorted(beliefs):
        print(f"{k}: {beliefs[k]:.3f}")
    print("Use case: transparent rule-level reasoning for retrieval/ranking pipelines.")


if __name__ == "__main__":
    main()
