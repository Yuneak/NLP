#!/usr/bin/env python3
# Example: Measures deterministic parsing vs noisy semantic extraction accuracy.
"""Tutorial 04: Deterministic vs noisy semantic extraction error study."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Example:
    text: str
    label_budget_ok: int


def deterministic_extract_cost_budget(text: str) -> Tuple[int, int]:
    cost = re.search(r"cost\s*=\s*(\d+)", text)
    budget = re.search(r"budget\s*=\s*(\d+)", text)
    if not cost or not budget:
        raise ValueError("missing structured fields")
    return int(cost.group(1)), int(budget.group(1))


def noisy_semantic_extract_budget_ok(text: str, noise: float = 0.2) -> int:
    cost, budget = deterministic_extract_cost_budget(text)
    # Budget label formula: y = 1[cost <= budget].
    truth = 1 if cost <= budget else 0
    if random.random() < noise:
        return 1 - truth
    return truth


def evaluate(samples: List[Example]) -> None:
    det_correct = 0
    noisy_correct = 0
    for e in samples:
        cost, budget = deterministic_extract_cost_budget(e.text)
        # Deterministic predictor: y_hat = 1[cost <= budget].
        det_pred = 1 if cost <= budget else 0
        noisy_pred = noisy_semantic_extract_budget_ok(e.text, noise=0.25)
        det_correct += int(det_pred == e.label_budget_ok)
        noisy_correct += int(noisy_pred == e.label_budget_ok)

    n = len(samples)
    # Accuracy formula: correct / n.
    print("=== Extraction accuracy on toy set ===")
    print(f"deterministic parser accuracy: {det_correct}/{n} = {det_correct/n:.2%}")
    print(f"noisy semantic extractor accuracy: {noisy_correct}/{n} = {noisy_correct/n:.2%}")
    print("Use case: show that formal composition is only as strong as atomic extraction quality.")


def main() -> None:
    random.seed(7)
    dataset = [
        Example("trip id=1 cost=780 budget=800", 1),
        Example("trip id=2 cost=810 budget=800", 0),
        Example("trip id=3 cost=650 budget=700", 1),
        Example("trip id=4 cost=920 budget=900", 0),
        Example("trip id=5 cost=500 budget=500", 1),
        Example("trip id=6 cost=1000 budget=950", 0),
    ]
    evaluate(dataset)


if __name__ == "__main__":
    main()
