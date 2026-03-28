# Result: SIR Epidemic Model

**Date:** 2026-03-28
**Simulation:** `beispiel_sir_epidemie`
**Skill:** sim-systemdynamik | **Seed:** 99

## Parameters

| Parameter | Value | Meaning |
|---|---|---|
| N | 10,000 | Total population |
| I₀ | 100 | Infected at start |
| β | 0.30 | Daily transmission rate |
| γ | 0.05 | Daily recovery rate |
| R₀ | **6.0** | β/γ – basic reproduction number |
| Herd immunity | **83.3%** | 1 − 1/R₀ |

## Time Series (Euler method, Δt = 1 day)

| Day | Susceptible (S) | Infected (I) | Recovered (R) | I% |
|---|---|---|---|---|
| 0 | 9,900 | 100 | 0 | 1.0% |
| 5 | 9,661 | 299 | 40 | 3.0% |
| 10 | 8,987 | 853 | 160 | 8.5% |
| 15 | 7,367 | 2,148 | 485 | 21.5% |
| 20 | 4,648 | 4,135 | 1,217 | 41.4% |
| **26** | **1,794** | **5,522** | **2,683** | **55.2% ← Peak** |
| 30 | ~870 | ~5,340 | ~3,790 | ~53.4% |

## Key Findings

### Peak (Day 26)
- **55% of the population infected simultaneously** (5,522 of 10,000)
- Herd immunity threshold at S = N/R₀ = 1,667 → not reached until day ~26
- After that I decreases because S < 1/R₀ × N (too few susceptible for growth)

### Growth Phases
- **Day 0–10:** Exponential growth (I doubles every ~3 days)
- **Day 10–20:** Accelerated growth, S notably depleting
- **Day 20–26:** Slowdown, approaching peak
- **Day 26+:** Declining phase (I decreases slowly)

### Comparison: Intervention (fork scenario, theoretical)
| Scenario | β | Peak I | Peak day | Total duration |
|---|---|---|---|---|
| Base (R₀=6) | 0.30 | 55.2% | ~day 26 | ~60 days |
| Moderate measures (R₀=3) | 0.15 | ~35% | ~day 40 | ~100 days |
| Hard lockdown (R₀=1.5) | 0.075 | ~10% | ~day 80 | ~200 days |

## Stocks & Flows Structure

```
S ──[New infections: β·S·I/N]──► I ──[Recovery: γ·I]──► R
     (dampening feedback)          (decay)
```

## Engine Findings

Continuous differential equations can only be represented in the scenario-engine
as **manual snapshots** (World Rules do not support accumulating calculations).
Recommendation: calculate externally (Python/Excel)
→ save key states as `set_resource` snapshots in the engine.
