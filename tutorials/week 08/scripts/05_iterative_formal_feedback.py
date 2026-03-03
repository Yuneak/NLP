#!/usr/bin/env python3
# Example: Demonstrates multi-round plan repair using formalized feedback messages.
"""Tutorial 05: Iterative formal feedback and repair loop."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import List, Tuple


@dataclass
class Plan:
    has_flight: bool
    arrival_day: int
    checkin_day: int
    total_cost: int
    budget: int


def verify(plan: Plan) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    # Constraint formula: total_cost <= budget.
    if plan.total_cost > plan.budget:
        issues.append("Reduce cost to be <= budget.")
    # Constraint formula: has_flight => (checkin_day == arrival_day).
    if plan.has_flight and plan.checkin_day != plan.arrival_day:
        issues.append("Set checkin_day equal to arrival_day when flight exists.")
    return len(issues) == 0, issues


def apply_feedback(plan: Plan, issues: List[str]) -> Plan:
    updated = plan
    for issue in issues:
        if "Reduce cost" in issue:
            updated = replace(updated, total_cost=updated.budget)
        if "Set checkin_day equal" in issue:
            updated = replace(updated, checkin_day=updated.arrival_day)
    return updated


def run_refinement(initial: Plan, rounds: int = 3) -> None:
    current = initial
    for r in range(1, rounds + 1):
        ok, issues = verify(current)
        print(f"round {r}: {'SAFE' if ok else 'UNSAFE'} | plan={current}")
        if ok:
            break
        for i in issues:
            print(f"  feedback: {i}")
        current = apply_feedback(current, issues)


def main() -> None:
    start = Plan(has_flight=True, arrival_day=3, checkin_day=5, total_cost=930, budget=800)
    run_refinement(start, rounds=3)
    print("Use case: model-critic loops where formal checks produce actionable repair signals.")


if __name__ == "__main__":
    main()
