# Python Tutorial Scripts (Based on Feb 26 Papers)

This folder contains 13 runnable tutorial examples derived from `deep-research-report.md` and the four papers in `Feb 26 Papers`.

## Requirements

- Python 3.10+
- Optional: `z3-solver` for solver-backed checks in script 03

Install optional dependency:

```bash
pip install z3-solver
```

## Scripts, Run Commands, and Use Cases

1. `01_rlcer_validity.py`
- Run: `python .\scripts\01_rlcer_validity.py`
- Use case: understand correlation-based rubric validity and normalized CoT reward.

2. `02_rlcer_training_sim.py`
- Run: `python .\scripts\02_rlcer_training_sim.py`
- Use case: compare `outcome_only`, `rubric_only`, and `combined` training signals.

3. `03_formal_judge_lite.py`
- Run: `python .\scripts\03_formal_judge_lite.py`
- Use case: build atomic facts and verify budget/date constraints with optional Z3.

4. `04_extraction_error_study.py`
- Run: `python .\scripts\04_extraction_error_study.py`
- Use case: quantify deterministic extraction vs noisy semantic extraction errors.

5. `05_iterative_formal_feedback.py`
- Run: `python .\scripts\05_iterative_formal_feedback.py`
- Use case: show iterative correction rounds driven by formal feedback.

6. `06_bp_logical_graph.py`
- Run: `python .\scripts\06_bp_logical_graph.py`
- Use case: do transparent forward reasoning over weighted logical rules.

7. `07_neg_factor_ablation.py`
- Run: `python .\scripts\07_neg_factor_ablation.py`
- Use case: show how explicit negation links enable contrapositive-style updates.

8. `08_grammar_first_parser.py`
- Run: `python .\scripts\08_grammar_first_parser.py`
- Use case: deterministic grammar-first compilation into logical form.

9. `09_disambiguate_then_compile.py`
- Run: `python .\scripts\09_disambiguate_then_compile.py`
- Use case: disambiguate local ambiguity first, then compile deterministically.

10. `10_capstone_decompose_verify_evolve.py`
- Run: `python .\scripts\10_capstone_decompose_verify_evolve.py`
- Use case: combine decomposition, verification, and iterative evolution in one loop.

11. `11_kimi_joint_text_vision.py`
- Run: `python .\scripts\11_kimi_joint_text_vision.py`
- Use case: inspect Kimi K2.5 joint text-vision ablations and cross-modal transfer gains.

12. `12_kimi_parl_reward.py`
- Run: `python .\scripts\12_kimi_parl_reward.py`
- Use case: simulate PARL reward shaping and auxiliary-term annealing in swarm orchestration.

13. `13_kimi_critical_steps.py`
- Run: `python .\scripts\13_kimi_critical_steps.py`
- Use case: compute critical-step latency and compare single-agent vs swarm speed scaling.

## Suggested Teaching Order

`01 -> 03 -> 07 -> 10 -> 11 -> 12 -> 13`, then use `02/04/05/06/08/09` as labs.

## Material Coverage Map (Report -> Example)

- RLCER validity and CoT reward formulas -> `01_rlcer_validity.py`
- RLCER training regimes and ablations -> `02_rlcer_training_sim.py`
- FormalJudge pipeline and constraint verification -> `03_formal_judge_lite.py`
- Atomic extraction error bottleneck -> `04_extraction_error_study.py`
- Formal feedback and iterative refinement -> `05_iterative_formal_feedback.py`
- LBN forward inference (AND/OR, weighted propagation) -> `06_bp_logical_graph.py`
- NEG factor and contrapositive behavior -> `07_neg_factor_ablation.py`
- Typed/grammar-first logical compilation -> `08_grammar_first_parser.py`
- LLM-style disambiguation then deterministic compile -> `09_disambiguate_then_compile.py`
- Cross-paper unification (decompose -> verify -> evolve) -> `10_capstone_decompose_verify_evolve.py`
- Kimi K2.5 joint text-vision strategy + transfer effects -> `11_kimi_joint_text_vision.py`
- PARL reward and anti-collapse training dynamics -> `12_kimi_parl_reward.py`
- Critical-step metric and swarm latency scaling -> `13_kimi_critical_steps.py`
