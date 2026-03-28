---
name: sim-spieltheorie
description: Game theory simulation with the scenario-engine. Models strategic decisions between rational actors (Prisoner's Dilemma, Nash equilibrium, Tit-for-Tat). Trigger when the user wants to simulate or analyze a game-theoretic scenario.
---

You run a game theory simulation with the scenario-engine MCP.

## Your Approach

1. **Clarify context** – Ask the user for:
   - Which actors / players? How many?
   - Which strategies are available?
   - One-shot game or repeated game (how many rounds)?
   - Which payoff matrix / objective?

2. **Set up the simulation** – Create the simulation with `create_simulation`, then set via `apply_action`:
   - `entities`: one entry per player with `strategy`, `type`, `info`
   - `metrics`: `utility_<player>` for each player (accumulate payoffs)
   - `flags`: `<player>_cooperates` for current round strategy
   - `metadata`: document the payoff matrix

3. **Define World Rules** – Implement the game logic:
   - Payoff rules based on flag combinations
   - Strategy-switch rules (Tit-for-Tat, Always Defect, etc.)
   - One rule per player combination

4. **Simulate** – Run the rounds (`apply_action: step`), after each round `get_state` for interim results

5. **Compare scenarios** – Use `fork_timeline` to test different strategies against each other

6. **Evaluate** – Report:
   - Cumulative payoffs per player
   - Whether cooperation emerged
   - Identify Nash equilibrium
   - Save result in `results/` as Markdown

## Mapping to Engine Schema

| Game Theory | scenario-engine |
|---|---|
| Player | `entities` |
| Strategy (this round) | `flags` |
| Cumulative utility | `metrics` |
| Payoff rate | `resources` |
| Game round | `time` (1 step = 1 round) |

## Payoff Matrix: Prisoner's Dilemma (Standard)
| A \ B | Cooperates | Defects |
|---|---|---|
| **Cooperates** | +3 / +3 | -1 / +5 |
| **Defects** | +5 / -1 | +1 / +1 |

## Typical Scenarios
- One-shot game → Nash equilibrium
- Repeated game → does cooperation emerge?
- Tit-for-Tat vs. Always Defect → which strategy dominates?
- Asymmetric information → advantage for whom?
