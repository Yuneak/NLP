#!/usr/bin/env python3
# Example: Computes critical-step latency and compares single-agent vs swarm scaling.
"""Tutorial 13: Critical-steps metric and parallel speedup intuition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Stage:
    main_steps: int
    subagent_steps: List[int]


def critical_steps(episode: List[Stage]) -> int:
    # CriticalSteps = sum_t (S_main^(t) + max_i S_sub,i^(t)).
    total = 0
    for stage in episode:
        max_sub = max(stage.subagent_steps) if stage.subagent_steps else 0
        total += stage.main_steps + max_sub
    return total


def main() -> None:
    # Toy plans to show how the critical-path metric favors balanced parallelization.
    sequential_plan = [
        Stage(main_steps=1, subagent_steps=[12]),
        Stage(main_steps=1, subagent_steps=[11]),
        Stage(main_steps=1, subagent_steps=[10]),
        Stage(main_steps=1, subagent_steps=[9]),
    ]
    swarm_plan = [
        Stage(main_steps=1, subagent_steps=[5, 6, 4]),
        Stage(main_steps=1, subagent_steps=[4, 5, 3]),
        Stage(main_steps=1, subagent_steps=[3, 4, 3]),
        Stage(main_steps=1, subagent_steps=[2, 3, 2]),
    ]

    seq_cs = critical_steps(sequential_plan)
    swarm_cs = critical_steps(swarm_plan)
    print("=== Critical-steps comparison (toy episode) ===")
    print(f"- single-agent-style critical steps: {seq_cs}")
    print(f"- swarm-style critical steps:        {swarm_cs}")
    print(f"- speedup factor from critical path: {seq_cs / swarm_cs:.2f}x")

    # Paper-reported trend ranges for WideSearch latency:
    # single-agent grows about 1.8x -> >7.0x while swarm stays around 0.6x -> 1.6x.
    target_item_f1 = [30, 40, 50, 60, 70]
    single_time = [1.8, 2.8, 4.0, 5.6, 7.0]
    swarm_time = [0.6, 0.9, 1.1, 1.3, 1.55]

    print("\n=== Latency scaling (range-consistent toy curve) ===")
    for f1, t_single, t_swarm in zip(target_item_f1, single_time, swarm_time):
        speedup = t_single / t_swarm
        print(
            f"- target Item-F1={f1:2d}% | single={t_single:.2f}x | swarm={t_swarm:.2f}x | speedup={speedup:.2f}x"
        )
    print("\nUse case: show why critical-step optimization can yield 3x-4.5x latency gains.")


if __name__ == "__main__":
    main()
