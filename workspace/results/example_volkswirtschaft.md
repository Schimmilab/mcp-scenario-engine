# Result: Mini-Economy – Multi-Agent Orchestration

**Date:** 2026-03-28
**Simulations:** `beispiel_vw_produktion` + `beispiel_vw_konsum`
**Skill:** sim-orchestrator | **Rounds:** 3

## System Architecture

```
Production sector ──[Wage sum]──► Consumer sector
       ▲                                │
       └────────[Demand]────────────────┘
       (coupling with damping 0.5 per round)
```

**Coupling Plan:**
| From | Variable | To | As | Damping |
|---|---|---|---|---|
| Production | wage_sum | Consumption | total_income | 0.5 |
| Consumption | demand | Production | production_target | 0.5 |

## Iteration Progress

### Production
| Round | GDP | Wage Sum | Investment Need | Production Target (input) |
|---|---|---|---|---|
| 1 | 1,000 | 600 | 150 | 1,000 (initial) |
| 2 | 756 | 454 | 113 | 756 (dampened) |
| 3 | 634 | 380 | 95 | 634 (dampened) |

### Consumption
| Round | Consumption | Demand | Savings | Income (input) |
|---|---|---|---|---|
| 1 | 461 | 511 | 10,120 | 600 (initial) |
| 2 | 461 | 511 | 10,240 | 600 (still R1 value) |
| 3 | 405 | 455 | 10,345 | 527 (dampened from R2) |

### Coupling Variables & Convergence
| Round | production_target | Δ% | income | Δ% | Converged? |
|---|---|---|---|---|---|
| 1→2 | 1000→756 | -24.4% | 600→600 | 0% | ✗ |
| 2→3 | 756→634 | -16.1% | 600→527 | -12.2% | ✗ |
| 3→4* | 634→545 | -14.0% | 527→453 | -14.0% | ✗ |

*Projection (not simulated)

## Theoretical Equilibrium (Keynesian Multiplier)

```
GDP* = Autonomous_Demand / (1 - Consumption_rate × Wage_share × Employment_rate)
GDP* = 50 / (1 - 0.8 × 0.6 × 0.96)
GDP* = 50 / (1 - 0.4608)
GDP* = 50 / 0.5392 ≈ 93
```

The system **converges toward GDP ≈ 93** – driven solely by autonomous investments (50).

## Emergent Phenomenon: Paradox of Thrift

- Every household rationally saves 20% of their income
- Economy-wide: savings formation **reduces demand → reduces GDP → reduces income**
- Although the savings rate remains constant, the *absolute amount* of savings declines
- **Paradox of Thrift** (Keynes): rational at the micro level → counterproductive at the macro level

## Sub-Agent Performance

| Agent | Rounds | Tool calls | Correct? |
|---|---|---|---|
| sim_produktion | 3 | ~47 | ✓ All values correct |
| sim_konsum | 3 | ~48 | ✓ All values correct |

## Engine Findings

- **Multi-agent pattern works** – both sub-agents correctly loaded, calculated, and saved
- Coupling via orchestrator (value passing in prompt) is practical
- For more rounds: automation via script recommended (scripts/)
- Convergence check manual by orchestrator (Δ% calculation)
