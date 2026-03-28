# Release Notes v1.2.0

**Feature Release — Engine Improvements, New Tools & Claude Code Workspace** 🚀

This release brings significant engine fixes, four new tools, a complete Claude Code workspace with seven simulation skills, and improved persistence.

## 🔧 Engine Fixes

### `step(steps=N)` now fires world rules N times
Previously, calling `step` with `steps: 5` advanced time by 5 but only applied world rules once. Now rules fire once per sub-step, making multi-step simulation dynamics correct.

```json
// World rules now accumulate properly across all 10 steps
{"action": "step", "params": {"steps": 10}}
```

### Persistence now saves timeseries & constraints
- Timeseries snapshots are saved to disk and fully restored on `load_simulation`
- `NonNegativeResourceConstraint` and `MaxResourceConstraint` are serialized and restored

### Timeseries records manual interventions
Non-step actions (`set_resource`, `adjust_metric`, `initialize`, etc.) that change state now also record a timeseries snapshot — making the full state history visible.

---

## ✨ New Actions

### `adjust_metric`
Adjust a metric by a delta value. Accepts both `delta` and `amount` as parameter name.

```json
{"action": "adjust_metric", "params": {"metric": "score", "delta": 5.0}}
```

### `initialize`
Batch-initialize resources, metrics, flags, entities, and metadata in a single call.

```json
{
  "action": "initialize",
  "params": {
    "resources": {"budget": 10000, "energy": 100},
    "metrics": {"output": 0, "efficiency": 1.0},
    "flags": {"active": true}
  }
}
```

---

## 🛠️ New Tools

### `get_timeseries`
Query time-series snapshots recorded at each step. Filter by variable names and time range.

```json
{"variables": ["budget", "output"], "from_time": 0, "to_time": 20}
```

### `batch_apply_actions`
Apply multiple actions in a single MCP call — reduces round-trips for initialization and batch updates.

```json
{
  "actions": [
    {"action": "initialize", "params": {"resources": {"budget": 1000}}},
    {"action": "step", "params": {"steps": 5}}
  ]
}
```

---

## 🌍 World Rule Enhancements

New action types in world rules:
- `adjust_resource` / `adjust_metric` / `adjust_metadata` — relative changes (`amount` param)
- `clamp_resource` / `clamp_metric` — keep values within bounds (`min`, `max` params)

New value types in world rule formulas:
- `min` / `max` — minimum/maximum from a list of values
- `clamp` — constrain a value: `{type: "clamp", value: {...}, min: {...}, max: {...}}`

`add_world_rule` now exposes `priority` and `description` parameters.

---

## 🔄 API Improvements

| Tool | New Parameter | Description |
|---|---|---|
| `reset_simulation` | `keep_rules` | Preserve world rules after reset |
| `fork_timeline` | `activate` | Make the fork the active simulation immediately |
| `adjust_resource` | `amount` | Alias for `delta` (both accepted) |
| `adjust_metric` | `amount` | Alias for `delta` (both accepted) |

---

## 🧠 Claude Code Workspace

This release includes a complete Claude Code workspace for simulation work.

### 7 Simulation Skills (Slash Commands)

| Skill | Domain |
|---|---|
| `/sim-spieltheorie` | Game theory — Nash equilibrium, Prisoner's Dilemma, Tit-for-Tat |
| `/sim-monte-carlo` | Risk & probability — uncertainty quantification via forks |
| `/sim-systemdynamik` | System dynamics — Stocks & Flows, SIR, Lotka-Volterra |
| `/sim-markov` | Markov chains — churn, health states, project phases |
| `/sim-agenten` | Agent-based models — markets, opinion dynamics, emergence |
| `/sim-optimierung` | Optimization — grid search, portfolio, resource allocation |
| `/sim-orchestrator` | Multi-agent — orchestrator + sub-agents for coupled simulations |

### Usage

Use the `mcp-scenario-engine` directory as your Claude Code workspace to get all skills automatically, or copy `workspace/` and `.claude/` to your own project.

### Included Examples

- `workspace/results/example_spieltheorie.md` — Tit-for-Tat vs Always Defect
- `workspace/results/example_sir_epidemie.md` — SIR epidemic model (R₀=6)
- `workspace/results/example_volkswirtschaft.md` — 3-agent Keynesian economy

---

## 📦 What's Included

- 30 files changed, 2042 insertions
- 7 new Claude Code skill files
- 3 workspace templates
- 3 example simulation results
- Complete engine source updates (actions, dynamic_rules, persistence, server, simulation)
