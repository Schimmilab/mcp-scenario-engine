---
name: sim-agenten
description: Agent-based simulation (ABM) with the scenario-engine. Models autonomous agents whose local interactions generate emergent system phenomena (markets, opinion formation, ecosystems, diffusion). Trigger when the user wants to simulate emergent phenomena, heterogeneous actors, or bottom-up dynamics.
---

You run an agent-based simulation (ABM) with the scenario-engine MCP.

## Your Approach

1. **Clarify context** – Ask the user for:
   - Which agent types exist? How many per type?
   - What properties does each type have?
   - Which interactions / rules apply to each type?
   - What should be observed at the system level (emergent metric)?
   - Time scale (1 step = 1 tick)?

2. **Model agent types**:
   - `entities`: one entry per agent type with properties
   - `resources`: population sizes per type (`count_<type>`)
   - `metrics`: system-level KPIs (equilibrium price, Gini, saturation level)
   - `flags`: system states (market open, crisis, intervention active)

3. **Set up the simulation** – `create_simulation`, initial values via `apply_action`

4. **Define interaction rules** – For each agent type:
   - Growth/shrinkage rule (selection)
   - Interaction rule with other types (competition, cooperation)
   - Resource consumption rule
   - System-level emergence rule (how does population change the metric?)

5. **Simulate** – `step` for N ticks, regularly `get_state` for time series of populations

6. **Observe emergence** – When do patterns arise? Tipping points? Equilibria?

7. **Scenarios** – `fork_timeline` for shocks (remove agents, change parameters)

8. **Evaluate** – Population dynamics, emergent metrics, stability analysis → `results/`

## Mapping to Engine Schema

| ABM | scenario-engine |
|---|---|
| Agent type | `entities` entry with properties |
| Population size | `resources` (`count_<type>`) |
| Agent property | Field in entity dict |
| Emergent system metric | `metrics` |
| System state / shock | `flags` |
| Tick | `time` (1 step = all agents act once) |

## Typical Interaction Rules
```
Growth with resource surplus:
  Condition: resource_pool > threshold
  Action: count_type_a *= 1.05

Competition dampens growth:
  Condition: count_type_a > capacity
  Action: count_type_a -= count_type_a * 0.03

Price adjustment (market):
  Condition: count_buyers > count_sellers * 5
  Action: equilibrium_price += 2
```

## Typical Scenarios
- Market dynamics: price discovery, monopoly formation, market failure?
- Opinion formation: consensus or polarization at which level of connectivity?
- Epidemic: diffusion at R0 > 1, herd immunity?
- Ecosystem: stable predator-prey equilibrium or collapse?
- Traffic: at which density does congestion emerge?