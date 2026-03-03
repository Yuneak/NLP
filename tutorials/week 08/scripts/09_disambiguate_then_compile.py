#!/usr/bin/env python3
# Example: Resolves local ambiguity first, then applies deterministic LF compilation.
"""Tutorial 09: Disambiguate first, then compile deterministically."""

from __future__ import annotations


def disambiguate_pp_attachment(sentence: str, hint: str) -> str:
    # hint simulates an external disambiguator (rule-based or LLM).
    # "instrument" => with telescope modifies "saw"
    # "noun" => with telescope modifies "man"
    sentence = sentence.strip().lower()
    if sentence != "i saw the man with a telescope":
        raise ValueError("This toy script expects one sentence.")
    if hint == "instrument":
        return "see(i, man) & using(i, telescope)"
    if hint == "noun":
        return "see(i, man_with_telescope)"
    raise ValueError("hint must be 'instrument' or 'noun'")


def main() -> None:
    s = "I saw the man with a telescope"
    lf1 = disambiguate_pp_attachment(s, "instrument")
    lf2 = disambiguate_pp_attachment(s, "noun")
    print("=== Disambiguation then compilation ===")
    print(f"sentence: {s}")
    print(f"instrument reading -> {lf1}")
    print(f"noun reading       -> {lf2}")
    print("Use case: keep ambiguity handling local, keep final compiler deterministic.")


if __name__ == "__main__":
    main()
