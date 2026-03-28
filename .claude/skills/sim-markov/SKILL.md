---
name: sim-markov
description: Markov chain simulation with the scenario-engine. Models state transitions for processes, phases, and lifecycles (Churn, disease progression, project phases, credit risk). Trigger when the user wants to simulate state transitions, transition probabilities, or phase models.
---

You run a Markov chain simulation with the scenario-engine MCP.

## Your Approach

1. **Clarify context** – Ask the user for:
   - Which states exist? (e.g. Active, At-risk, Churned)
   - Which transitions are possible? (from which state to which)
   - Transition probabilities per step?
   - Are there absorbing end states (no exit)?
   - Time scale (1 step = 1 day / week / month)?

2. **Model the states** – Two variants:
   - **Single entity:** `flags` for current state (exactly one true)
   - **Population:** `resources` for number of entities per state

3. **Set up the simulation** – `create_simulation`, then initial values via `apply_action`

4. **Define transition rules** – One rule per possible transition:
   - Condition: current state + triggering metric
   - Action: deactivate current state, activate new state
   - For population: `adjust_resource` with percentage rate

5. **Simulate** – `step` until equilibrium or horizon, `get_state` for time series

6. **Stationary distribution** – After many steps: what fraction stays in which state?

7. **Scenarios** – `fork_timeline` for comparison with/without intervention (e.g. retention measure)

8. **Evaluate** – Transition matrix, stationary distribution, absorption time, save in `results/`

## Mapping to Engine Schema

| Markov Chain | scenario-engine |
|---|---|
| State (single entity) | `flags` (exactly one true) |
| Population per state | `resources` |
| Transition probability | Rule condition + rate |
| Absorbing state | Flag without outgoing rule |
| Period | `time` (1 step = 1 transition period) |

## Transition Pattern (Population)
```
Rule "active_to_atrisk":
  Condition: customers_active > 0
  Action: customers_active -= customers_active * 0.05    (5% switch)
           customers_atrisk += customers_active * 0.05
```

## Typical Scenarios
- Customer Churn: stationary distribution, break-even retention cost?
- Disease progression: expected disease duration, mortality rate?
- Project phases: P(successful completion), expected duration?
- Credit risk: default probability over N periods (rating migration)?