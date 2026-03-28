---
name: sim-monte-carlo
description: Monte Carlo simulation with the scenario-engine. Estimates probabilities and risks through many forks with different seeds. Trigger when the user wants to estimate risks, quantify uncertainties, or calculate probabilities.
---

You run a Monte Carlo simulation with the scenario-engine MCP.

## Your Approach

1. **Clarify context** – Ask the user for:
   - What should be estimated? (target variable)
   - Which input values are uncertain? What range?
   - How many runs? (at least 10, better 20–50 for a clear distribution)
   - How many steps per run?

2. **Set up the base simulation** – `create_simulation` with a fixed seed, then:
   - `resources`: all uncertain variables with expected values
   - `metrics`: target variable + volatility parameters
   - `flags`: control for shocks / extreme events
   - `metadata`: document uncertainty ranges (`min`, `max`, `std`)

3. **Define stochastic rules** – Uncertainty via:
   - `simulate_load` action as a randomness proxy
   - Rules that react differently to high/low load
   - Volatility rules: `adjust_resource` with variable amounts

4. **Execute the fork loop** – For each run i=1..N:
   - `fork_timeline` with a new seed → run simulation → `get_state` → record result
   - Collect all target values

5. **Evaluate the distribution** – Calculate from the N results:
   - Expected value (mean)
   - Confidence interval P10–P90
   - Value at Risk (P5) – worst 5%
   - Min / Max

6. **Save result** – Distribution table + interpretation in `results/`

## Mapping to Engine Schema

| Monte Carlo | scenario-engine |
|---|---|
| Random variable | `resources` with stochastic rules |
| Simulation run | Fork with different seed |
| Target variable | one `metric` that is evaluated |
| Uncertainty range | Rule parameters (min/max amount) |
| Step | 1 time period (day, month, year) |

## Fork Workflow
```
Base (Seed=0)
  → fork (seed=1)  → N steps → TargetValue_1
  → fork (seed=2)  → N steps → TargetValue_2
  …
  → fork (seed=N)  → N steps → TargetValue_N
→ Distribution: [Min, P5, P10, Median, P90, P95, Max]
```

## Typical Scenarios
- Project cost risk: costs ±20% uncertainty → P90 budget?
- Business forecast: revenue with seasonal volatility → range?
- Health trajectory: weight with variable adherence → corridor in 6 months?
- Portfolio: asset returns with volatility → Value at Risk?
