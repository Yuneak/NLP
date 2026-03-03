#!/usr/bin/env python3
# Example: Compiles simple controlled-language sentences into logical forms.
"""Tutorial 08: Grammar-first parser for a micro logical domain."""

from __future__ import annotations

import re
from typing import Optional


def compile_sentence(text: str) -> Optional[str]:
    text = text.strip().lower()
    m = re.fullmatch(r"([a-z]+) is parent of ([a-z]+)", text)
    if m:
        return f"parent({m.group(1)},{m.group(2)})"

    m = re.fullmatch(r"if ([a-z]+) is parent of ([a-z]+), then ([a-z]+) is ancestor of ([a-z]+)", text)
    if m:
        a, b, c, d = m.groups()
        if a == c and b == d:
            return f"parent({a},{b}) -> ancestor({a},{b})"
    return None


def main() -> None:
    samples = [
        "Alice is parent of Bob",
        "If Alice is parent of Bob, then Alice is ancestor of Bob",
        "Alice likes Bob",
    ]
    print("=== Grammar-first compilation ===")
    for s in samples:
        lf = compile_sentence(s)
        print(f"{s!r} -> {lf if lf else 'UNPARSED'}")
    print("Use case: deterministic logical form generation after disambiguation.")


if __name__ == "__main__":
    main()
