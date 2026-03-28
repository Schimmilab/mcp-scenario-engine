---
name: sim-systemdynamik
description: System dynamics simulation (stocks and flows) with the scenario-engine. Models feedback loops, stocks and flows for dynamically complex systems. Trigger for epidemic models, population dynamics, capital accumulation, supply chain, or similar systems with feedback loops.
---

You run a system dynamics simulation (stocks and flows) with the scenario-engine MCP.

## Your Approach

1. **Clarify context** – Ask the user for:
   - Which system? (epidemic, population, economy, inventory, …)
   - Which stocks exist?
   - Which flows connect them?
   - Are there reinforcing (+) or dampening (−) feedback loops?
   - Time scale and step size (1 day? 1 month?)

2. **Structure the simulation** – Identify the causal diagram:
   - Stocks → `resources` (accumulate over time)
   - Flow parameters → `metrics` (rates that change stocks)
   - External drivers → `flags` (interventions on/off)
   - System state → `metadata`

3. **Set up the simulation** – `create_simulation`, then set initial values via `apply_action`

4. **Define feedback rules** – One rule per flow:
   - Reinforcing: stock grows proportionally to itself
   - Dampening: growth slows down at saturation
   - Delayed: effect occurs after N steps (via time_modulo)
   - Intervention: flag-controlled interruption of flows

5. **Simulate** – `step` for N steps, regularly `get_state` for time series

6. **Scenarios** – `fork_timeline` for policy comparisons (e.g. intervention yes/no)

7. **Evaluate** – Time series of stocks, identify equilibrium / tipping point, save in `results/`

## Mapping to Engine Schema

| System Dynamics | scenario-engine |
|---|---|
| Stock | `resources` |
| Flow rate (parameter) | `metrics` |
| Feedback rule | `world_rule` |
| External intervention | `flags` |
| Time step | `time` (1 step = 1 period) |

## Classic Models

**SIR epidemic:** S → I → R with β (transmission) and γ (recovery)
**Predator-prey (Lotka-Volterra):** Prey grows, predator decimates prey, predator dies without prey
**Capital accumulation:** Investment increases capital, depreciation reduces it
**Bullwhip effect:** Demand signal amplifies through inventory stages

## Typical Scenarios
- Epidemic: peak infections, herd immunity threshold?
- Population: stable equilibrium or collapse?
- Supply chain: which inventory parameters minimize bullwhip?
- Economy: when does capital accumulation break down?