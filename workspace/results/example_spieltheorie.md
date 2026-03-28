# Result: Prisoner's Dilemma – Tit-for-Tat vs. Always Defect

**Date:** 2026-03-28
**Simulation:** `beispiel_spieltheorie_gefangenendilemma`
**Skill:** sim-spieltheorie | **Seed:** 42

## Setup

| Parameter | Value |
|---|---|
| Player A | Alice (Tit-for-Tat) |
| Player B | Bob (Always Defect) |
| Rounds | 5 |
| Payoff matrix | Standard Prisoner's Dilemma |

**Payoff Matrix:**
| A \ B | Cooperates | Defects |
|---|---|---|
| Cooperates | +3 / +3 | **-1 / +5** |
| Defects | +5 / -1 | **+1 / +1** |

## Time Series

| Round | Alice | Bob | A cooperates? | B cooperates? |
|---|---|---|---|---|
| 1 | -1 | +5 | ✓ Yes | ✗ No |
| 2 | +1 | +1 | ✗ No (retaliation) | ✗ No |
| 3 | +1 | +1 | ✗ No | ✗ No |
| 4 | +1 | +1 | ✗ No | ✗ No |
| 5 | +1 | +1 | ✗ No | ✗ No |
| **Total** | **3** | **9** | | |

## Interpretation

- **Always Defect dominates** in the short game (5 rounds): Bob achieves 9 vs. Alice's 3
- **Tit-for-Tat loses round 1** by cooperating initially (-1 instead of +1)
- From **round 2** onward both converge to Nash equilibrium (both defect, +1/+1)
- **Missed cooperation:** Had both cooperated → +3/round each = 15 total (Pareto optimum)
- **Social dilemma:** Individually rational (defecting) → collectively suboptimal (6 total instead of 30)

## Scenario Comparison (theoretical)

| Strategy pairing | A total | B total | Total |
|---|---|---|---|
| Tit-for-Tat vs. Always Defect | 3 | 9 | 12 |
| Always Defect vs. Always Defect | 5 | 5 | 10 |
| Tit-for-Tat vs. Tit-for-Tat | 15 | 15 | **30** ← Pareto optimum |
| Always Cooperate vs. Always Defect | -5 | 25 | 20 |

## Engine Findings

> **Limitation:** World Rules only support `set_flag` and `set_resource` (absolute) as action types.
> `adjust_resource` and `set_metric` with `increment` value do not work in rules.
> → Accumulation logic must be implemented manually via `apply_action: adjust_resource` (with `delta` parameter).
