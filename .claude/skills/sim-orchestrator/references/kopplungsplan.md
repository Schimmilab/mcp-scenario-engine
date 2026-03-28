# Coupling Plan Reference

The Coupling Plan defines how sub-simulations interact with each other.
The orchestrator creates it in Phase 1 together with the user.

## Format

```yaml
couplings:
  - from: "<sub_sim_name>"
    variable: "<output_variable>"
    to: "<sub_sim_name>"
    as: "<input_variable>"
    factor: 1.0          # scaling (default: 1.0)
    damping: 0.5         # smoothing across rounds (0=none, 1=full)
    delay: 0             # rounds of delay (0=immediate)
```

## Examples

### Economy
```yaml
couplings:
  - from: "sim_production"
    variable: "output_gdp"
    to: "sim_consumption"
    as: "total_income"
    factor: 0.7          # 70% of GDP flows into consumption
    damping: 0.4

  - from: "sim_consumption"
    variable: "output_demand"
    to: "sim_production"
    as: "production_target"
    factor: 1.0
    damping: 0.5

  - from: "sim_labor_market"
    variable: "output_employment_rate"
    to: "sim_consumption"
    as: "propensity_to_consume"
    factor: 0.8
    damping: 0.3
```

### Ecosystem
```yaml
couplings:
  - from: "sim_plants"
    variable: "output_biomass"
    to: "sim_herbivores"
    as: "food_supply"
    factor: 1.0
    damping: 0.6

  - from: "sim_herbivores"
    variable: "output_population"
    to: "sim_carnivores"
    as: "prey_population"
    factor: 1.0
    damping: 0.5

  - from: "sim_carnivores"
    variable: "output_predation_pressure"
    to: "sim_herbivores"
    as: "mortality_rate"
    factor: 0.3
    damping: 0.4
```

### Smart City
```yaml
couplings:
  - from: "sim_traffic"
    variable: "output_congestion_level"
    to: "sim_economy"
    as: "productivity_loss"
    factor: 0.15
    damping: 0.5

  - from: "sim_economy"
    variable: "output_jobs"
    to: "sim_population"
    as: "migration_rate"
    factor: 0.002
    damping: 0.3

  - from: "sim_population"
    variable: "output_population_size"
    to: "sim_traffic"
    as: "base_traffic_volume"
    factor: 0.4
    damping: 0.6
```

## Damping & Stability

| Damping | Effect | When to use |
|---|---|---|
| 0.0 | No smoothing (immediate adoption) | Stable systems |
| 0.3–0.5 | Moderate smoothing | Standard |
| 0.7–0.9 | Strong smoothing | Volatile systems, convergence problems |
| 1.0 | Variable freezes | Debug / sensitivity test |

## Identifying Feedback Loops

**Reinforcing (+):** A → B → A with same sign
→ Exponential growth or collapse possible → increase damping

**Dampening (−):** A → B → A with opposite sign
→ Self-regulation → stable, tends toward equilibrium

**Delayed:** A → B (delay k) → A
→ Oscillations possible → reduce delay or increase damping