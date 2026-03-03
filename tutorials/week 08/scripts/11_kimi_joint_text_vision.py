#!/usr/bin/env python3
# Example: Recreates Kimi K2.5 text-vision ablation and cross-modal transfer summaries.
"""Tutorial 11: Joint text-vision training insights from Kimi K2.5."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class JointTrainingStrategy:
    name: str
    vision_injection_timing: str
    vision_text_ratio: str
    vision_knowledge: float
    vision_reasoning: float
    ocr: float
    text_knowledge: float
    text_reasoning: float
    code: float

    def avg_score(self) -> float:
        metrics = [
            self.vision_knowledge,
            self.vision_reasoning,
            self.ocr,
            self.text_knowledge,
            self.text_reasoning,
            self.code,
        ]
        return sum(metrics) / len(metrics)


def print_joint_training_ablation(strategies: List[JointTrainingStrategy]) -> None:
    print("=== Joint text-vision strategy comparison (Table-1 style) ===")
    ranked = sorted(strategies, key=lambda s: s.avg_score(), reverse=True)
    for s in ranked:
        print(
            f"- {s.name:5s} | timing={s.vision_injection_timing:5s} | ratio={s.vision_text_ratio:7s}"
            f" | avg={s.avg_score():.2f}"
        )

    late = next(s for s in strategies if s.name == "Late")
    early = next(s for s in strategies if s.name == "Early")
    print("\nEarly-vs-Late deltas:")
    print(f"- Vision knowledge: {early.vision_knowledge - late.vision_knowledge:+.1f}")
    print(f"- Vision reasoning: {early.vision_reasoning - late.vision_reasoning:+.1f}")
    print(f"- OCR: {early.ocr - late.ocr:+.1f}")
    print(f"- Text knowledge: {early.text_knowledge - late.text_knowledge:+.1f}")
    print(f"- Text reasoning: {early.text_reasoning - late.text_reasoning:+.1f}")
    print(f"- Code: {early.code - late.code:+.1f}")


def print_cross_modal_transfer(before_after: Dict[str, Tuple[float, float]]) -> None:
    print("\n=== Cross-modal transfer (vision RL -> text metrics) ===")
    gains: List[float] = []
    for benchmark, (before, after) in before_after.items():
        gain = after - before
        gains.append(gain)
        print(f"- {benchmark:14s}: {before:.1f} -> {after:.1f} (gain {gain:+.1f})")
    avg_gain = sum(gains) / len(gains)
    print(f"- Average gain across listed text benchmarks: {avg_gain:+.2f}")


def main() -> None:
    # Values are copied from the Kimi K2.5 technical report tables.
    strategies = [
        JointTrainingStrategy("Early", "Early", "10:90", 25.8, 43.8, 65.7, 45.5, 58.5, 24.8),
        JointTrainingStrategy("Mid", "Mid", "20:80", 25.0, 40.7, 64.1, 43.9, 58.6, 24.0),
        JointTrainingStrategy("Late", "Late", "50:50", 24.2, 39.0, 61.5, 43.1, 57.8, 24.0),
    ]

    before_after = {
        "MMLU-Pro": (84.7, 86.4),
        "GPQA-Diamond": (84.3, 86.4),
        "LongBench v2": (56.7, 58.9),
    }

    print_joint_training_ablation(strategies)
    print_cross_modal_transfer(before_after)
    print("\nUse case: explain why early fusion and joint multimodal RL are central in Kimi K2.5.")


if __name__ == "__main__":
    main()
