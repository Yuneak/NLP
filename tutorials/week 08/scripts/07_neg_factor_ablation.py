#!/usr/bin/env python3
# Example: Compares inference behavior with and without explicit negation linkage.
"""Tutorial 07: NEG-factor ablation for modus tollens intuition."""

from __future__ import annotations


def posterior_a_given_not_b(prior_a: float, p_b_given_a: float, p_b_given_not_a: float) -> float:
    # Bayes formula: P(A|not B) = P(not B|A) * P(A) / P(not B).
    p_not_b_given_a = 1.0 - p_b_given_a
    p_not_b_given_not_a = 1.0 - p_b_given_not_a
    num = p_not_b_given_a * prior_a
    den = num + p_not_b_given_not_a * (1.0 - prior_a)
    return num / den if den else prior_a


def main() -> None:
    prior_a = 0.50
    p_b_given_a = 0.95      # strong rule A -> B
    p_b_given_not_a = 0.10  # small leak

    # Without NEG linkage, many pipelines cannot propagate not-B back to not-A.
    without_neg = prior_a

    # With NEG factor + backward message, we update from evidence not-B.
    with_neg = posterior_a_given_not_b(prior_a, p_b_given_a, p_b_given_not_a)

    print("=== NEG factor ablation ===")
    print(f"P(A) prior:                {prior_a:.3f}")
    print(f"P(A | not B) without NEG:  {without_neg:.3f}  (no backward update)")
    print(f"P(A | not B) with NEG:     {with_neg:.3f}")
    print(f"Inferred P(not A | not B): {1.0 - with_neg:.3f}")
    print("Use case: demonstrate why explicit negation links matter for contrapositive reasoning.")


if __name__ == "__main__":
    main()

