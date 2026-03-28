# Workspace – Project Context

This workspace uses the **scenario-engine MCP** for deterministic simulations and scenario planning.

## Scenario-Engine – Overview

The engine runs locally via MCP server. Simulations are saved under:
`~/.mcp-scenario-engine/simulations/<name>.json`

### State Schema
```
simulation_id  – UUID (auto)
time           – Integer time step (0, 1, 2, …)
seed           – Random seed for reproducibility
entities       – Dict: free objects (persons, systems, …)
metrics        – Dict[str, float]: KPIs / measurements
resources      – Dict[str, float]: resources (budget, energy, …)
flags          – Dict[str, bool]: state switches
metadata       – Dict: free metadata (description, tags, …)
```

### Core Actions (via `apply_action`)
| Action | Params | Description |
|---|---|---|
| `step` | `steps` (int) | Advance time steps |
| `set_resource` | `resource`, `value` | Set resource |
| `adjust_resource` | `resource`, `amount` | Change resource relatively |
| `set_metric` | `metric`, `value` | Set metric |
| `set_flag` | `flag`, `value` | Set flag |
| `add_entity` | `entity_id`, `data` | Add entity |
| `remove_entity` | `entity_id` | Remove entity |
| `simulate_load` | `intensity` (0-100) | Simulate load |

### World Rules
Rules that are automatically executed with every `step`.
Structure: `condition` → `actions`

Condition types:
- `always` – always trigger
- `comparison` – compare two values
- `time_modulo` – every N steps

Action types in rules:
- `set_metric`, `set_resource`, `set_flag`
- `increment` / `decrement` (as value type)

## Workflow Patterns

### Starting a New Simulation
1. `create_simulation` (name, description, seed)
2. Set initial `entities`, `resources`, `metrics` via `apply_action`
3. Define `world_rules` (automatic dynamics)
4. Simulate with `step`, evaluate with `get_state`
5. Save with `save_simulation` → `fork_timeline` for scenarios

### Scenario Comparison
- Load base → `fork_timeline` → simulate variant under different conditions
- Compare states via `get_state` on both forks

## Engine Status (tested 2026-03-28, fixes deployed)

| What | Status | Note |
|---|---|---|
| `adjust_resource` / `adjust_metric` as World Rule action | ✓ works | Parameter: `amount` |
| `set_metric` with `{type: 'increment'}` in rules | ✓ works | Alternative: `adjust_metric` with `amount` |
| `step` with `steps: N` (N>1) | ✓ time jumps by N, World Rules fire **N times** | One snapshot per sub-step |
| `adjust_resource` / `adjust_metric` via `apply_action` | ✓ works | Parameter: `delta` |
| `initialize` action | ✓ batch init for resources/metrics/flags/entities | Saves multiple individual calls |
| `get_timeseries` | ✓ time series query with variable filter | Parameters: `variables`, `from_time`, `to_time` |
| `fork_timeline` with name | ✓ `name` parameter for fork label | – |
| `batch_apply_actions` | ✓ multiple actions in one MCP call | Parameters: `actions[]`, `stop_on_failure` |
| Timeseries persistence | ✓ snapshots are saved and loaded | – |
| Constraints persistence | ✓ NonNegative + Max Constraints are restored | – |
| `clamp_resource` / `clamp_metric` as World Rule action | ✓ keep values within bounds | Parameters: `min`, `max` |
| `priority` in `add_world_rule` | ✓ order controllable | Higher = runs first |

### Available World Rule Actions
- `set_resource`, `set_metric`, `set_flag`, `set_metadata` (absolute)
- `adjust_resource`, `adjust_metric`, `adjust_metadata` (relative, parameter: `amount`)
- `clamp_resource`, `clamp_metric` (bounds, parameters: `min`, `max`)

### Available Value Types in World Rules (for `_compute_value`)
- `value` – constant: `{type: "value", value: 42}`
- `resource`, `metric`, `flag`, `metadata`, `time` – state references
- `add`, `subtract`, `multiply`, `divide` – arithmetic
- `min`, `max` – minimum/maximum from list: `{type: "min", values: [...]}`
- `clamp` – clamp: `{type: "clamp", value: {...}, min: {...}, max: {...}}`

## Directory Structure
```
workspace/
├── CLAUDE.md               – Project context & engine reference
│
├── templates/              – Reusable simulation templates
│   ├── health.md           – Health / body composition
│   ├── project.md          – Project / resource planning
│   └── system.md           – System / load simulation
│
├── designs/                – Simulation designs before creation
│   └── new_simulation.md   – Blank template
│
├── data/                   – Input data & reference values
│                             e.g. measurements (CSV/JSON), benchmarks,
│                             historical data as calibration basis
│
├── results/                – Simulation results & snapshots
│                             e.g. exported states, time series,
│                             fork comparisons (Markdown/JSON)
│
├── analysis/               – Evaluations & insights
│                             e.g. diagrams, summaries,
│                             interpretations of simulation runs
│
├── .claude/skills/         – Callable simulation skills (slash commands)
│   ├── sim-spieltheorie/   – /sim-spieltheorie:  Nash, Tit-for-Tat, payoff matrices
│   ├── sim-monte-carlo/    – /sim-monte-carlo:   risk estimation, forks, distributions
│   ├── sim-systemdynamik/  – /sim-systemdynamik: stocks & flows, SIR, Lotka-Volterra
│   ├── sim-markov/         – /sim-markov:        state transitions, Churn, rating migration
│   ├── sim-agenten/        – /sim-agenten:       ABM, emergence, market dynamics
│   ├── sim-optimierung/    – /sim-optimierung:   grid search, portfolio, allocation
│   └── sim-orchestrator/   – /sim-orchestrator:  multi-agent: orchestrator + sub-agents
│       ├── agents/
│       │   ├── sub-agent.md      – prompt template for subsystem agents
│       │   └── synthesizer.md    – synthesis agent for coupling calculation
│       └── references/
│           └── kopplungsplan.md  – format & examples for system couplings
│
└── scripts/                – Helper scripts
                              e.g. data preparation, batch runs,
                              evaluation scripts (Python)
```

## Typical File Flow
```
data/ → designs/ → [scenario-engine MCP] → results/ → analysis/
         (plan)        (execute)            (save)      (evaluate)
```
