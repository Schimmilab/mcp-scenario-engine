---
name: sim-optimierung
description: Optimization simulation with the scenario-engine. Finds optimal decisions under constraints through fork-based parameter search (Grid Search, Greedy). Trigger when the user wants to optimize a decision, maximize/minimize an objective function, or allocate resources optimally.
---

You run an optimization simulation with the scenario-engine MCP.

## Your Approach

1. **Clarify the problem** – Ask the user for:
   - What should be optimized? (objective function: maximize or minimize)
   - Which decision variables exist? What value ranges?
   - Which constraints must be satisfied?
   - How fine should the search be? (number of grid points)

2. **Model the problem**:
   - `resources`: decision variables (to be varied)
   - `metrics`: objective function + derived KPIs
   - `flags`: constraint indicators (`constraint_ok`, `solution_valid`)
   - `metadata`: document the search space

3. **Set up the base simulation** – `create_simulation`, initial values via `apply_action`

4. **Define objective function rules** – Rules that compute the objective function from decision variables:
   - Direct relationships (linear, threshold-based)
   - Map constraint violations to `flags`

5. **Choose and execute search strategy**:

   **Grid Search** (for ≤ 3 variables):
   ```
   For each grid point: fork → set variables → simulate → measure objective
   Identify best result
   ```

   **Greedy / Hill Climbing** (for more variables):
   ```
   Starting point → try neighbors (±Δ) → take best → repeat
   ```

6. **Fine search** – Refine around the best result with smaller Δ

7. **Evaluate** – Optimum + sensitivity analysis (how much does the objective change at ±10%?)
   Save result in `results/`

## Mapping to Engine Schema

| Optimization | scenario-engine |
|---|---|
| Decision variable | `resources` (varied per fork) |
| Objective function | `metrics` (1 target metric) |
| Constraint | `flags` (constraint_ok = true/false) |
| Candidate solution | Fork with specific resource values |
| Evaluation step | `step` + `get_state` |

## Fork Search Schema
```
Base setup
  → fork_A: var_1 = 0.2 → step → measure objective
  → fork_B: var_1 = 0.4 → step → measure objective  ← best
  → fork_C: var_1 = 0.6 → step → measure objective
→ Fine search around 0.4: fork_B1 = 0.35, fork_B2 = 0.45 …
```

## Typical Scenarios
- Budget allocation: distribution across N channels → maximize ROI
- Portfolio optimization: asset weighting → maximize Sharpe ratio
- Price optimization: price points → maximize contribution margin
- Staff planning: shift coverage → minimize cost while meeting SLA
- Inventory optimization: order quantities → minimize total cost