#!/usr/bin/env python3
# Example: Shows atomic fact extraction and formal safety checks with optional Z3.
"""Tutorial 03: FormalJudge-lite with optional Z3 verification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

try:
    from z3 import BoolVal, IntVal, If, Implies, Solver, sat  # type: ignore
    HAS_Z3 = True
except Exception:
    HAS_Z3 = False


@dataclass
class Plan:
    has_flight: bool
    arrival_day: int
    checkin_day: int
    total_cost: int
    budget: int


def extract_atomic_facts(plan: Plan) -> Dict[str, int]:
    return {
        "has_flight": int(plan.has_flight),
        "arrival_day": plan.arrival_day,
        "checkin_day": plan.checkin_day,
        "total_cost": plan.total_cost,
        "budget": plan.budget,
    }


def verify_with_python(f: Dict[str, int]) -> Tuple[bool, List[str]]:
    failures: List[str] = []
    # Constraint formula: total_cost <= budget.
    if not (f["total_cost"] <= f["budget"]):
        failures.append("budget violated")
    # Constraint formula: has_flight => (checkin_day == arrival_day).
    if f["has_flight"] == 1 and not (f["checkin_day"] == f["arrival_day"]):
        failures.append("flight implies same-day hotel checkin violated")
    return len(failures) == 0, failures


def verify_with_z3(f: Dict[str, int]) -> Tuple[bool, List[str]]:
    s = Solver()
    has_flight = BoolVal(f["has_flight"] == 1)
    arrival_day = IntVal(f["arrival_day"])
    checkin_day = IntVal(f["checkin_day"])
    total_cost = IntVal(f["total_cost"])
    budget = IntVal(f["budget"])

    # Safe iff these formulas hold:
    # c_budget: total_cost <= budget
    # c_dates:  has_flight => (checkin_day == arrival_day)
    c_budget = total_cost <= budget
    c_dates = Implies(has_flight, checkin_day == arrival_day)
    s.add(If(c_budget, 1, 0) == 1)
    s.add(If(c_dates, 1, 0) == 1)
    ok = s.check() == sat

    failures = []
    if not (f["total_cost"] <= f["budget"]):
        failures.append("budget violated")
    if f["has_flight"] == 1 and not (f["checkin_day"] == f["arrival_day"]):
        failures.append("flight implies same-day hotel checkin violated")
    return ok, failures


def run_case(name: str, plan: Plan) -> None:
    facts = extract_atomic_facts(plan)
    if HAS_Z3:
        ok, failures = verify_with_z3(facts)
        engine = "z3"
    else:
        ok, failures = verify_with_python(facts)
        engine = "python_fallback"

    print(f"\n{name} ({engine})")
    print(f"- facts: {facts}")
    print(f"- verdict: {'SAFE' if ok else 'UNSAFE'}")
    if failures:
        for f in failures:
            print(f"  reason: {f}")


def main() -> None:
    safe_plan = Plan(True, 5, 5, 780, 800)
    unsafe_plan = Plan(True, 5, 6, 840, 800)
    run_case("safe_case", safe_plan)
    run_case("unsafe_case", unsafe_plan)
    if not HAS_Z3:
        print("\nInstall z3-solver for solver-backed verification: pip install z3-solver")


if __name__ == "__main__":
    main()
