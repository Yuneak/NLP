#!/usr/bin/env python3
# Example: Integrates decomposition, verification, scoring, and iterative correction.
"""Tutorial 10: End-to-end decompose -> verify -> evolve toy pipeline."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, List, Tuple


@dataclass
class Attempt:
    reasoning: str
    answer: int
    expected: int
    has_flight: bool
    arrival_day: int
    checkin_day: int
    total_cost: int
    budget: int


def rubric_atoms(a: Attempt) -> Dict[str, int]:
    return {
        "mentions_carry": int("carry" in a.reasoning.lower()),
        "no_tangent": int("by the way" not in a.reasoning.lower()),
    }


def verify_global_constraints(a: Attempt) -> Tuple[bool, List[str]]:
    issues = []
    # Constraint formulas:
    # answer == expected
    # total_cost <= budget
    # has_flight => (checkin_day == arrival_day)
    if a.answer != a.expected:
        issues.append("final answer incorrect")
    if a.total_cost > a.budget:
        issues.append("budget violated")
    if a.has_flight and a.checkin_day != a.arrival_day:
        issues.append("date consistency violated")
    return len(issues) == 0, issues


def score(a: Attempt) -> float:
    atoms = rubric_atoms(a)
    ok, issues = verify_global_constraints(a)
    # Score formula: outcome + cot + safety_penalty.
    outcome = 1.0 if a.answer == a.expected else -1.0
    # CoT term formula: 1[mentions_carry] + 1[no_tangent].
    cot = atoms["mentions_carry"] + atoms["no_tangent"]
    # Safety penalty formula: -0.5 * number_of_violations.
    safety_penalty = -0.5 * len(issues)
    return outcome + cot + safety_penalty


def evolve(a: Attempt, issues: List[str]) -> Attempt:
    nxt = a
    if "final answer incorrect" in issues:
        nxt = replace(nxt, answer=nxt.expected)
    if "budget violated" in issues:
        nxt = replace(nxt, total_cost=nxt.budget)
    if "date consistency violated" in issues:
        nxt = replace(nxt, checkin_day=nxt.arrival_day)
    if "carry" not in nxt.reasoning.lower():
        nxt = replace(nxt, reasoning=nxt.reasoning + " I checked carry handling.")
    return nxt


def main() -> None:
    attempt = Attempt(
        reasoning="I computed quickly. By the way this reminds me of travel.",
        answer=40,
        expected=42,
        has_flight=True,
        arrival_day=4,
        checkin_day=5,
        total_cost=920,
        budget=800,
    )

    print("=== Capstone loop ===")
    for step in range(1, 4):
        ok, issues = verify_global_constraints(attempt)
        s = score(attempt)
        print(f"step {step}: score={s:+.2f} ok={ok} issues={issues}")
        if ok:
            break
        attempt = evolve(attempt, issues)
    print("Use case: combine process atoms, formal checks, and iterative correction.")


if __name__ == "__main__":
    main()
