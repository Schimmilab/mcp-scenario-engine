# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install with dev dependencies
make install

# Run tests with coverage
make test

# Run a single test file
pytest tests/test_simulation.py -v

# Run a single test
pytest tests/test_simulation.py::TestSimulationEngine::test_apply_action -v

# Lint (ruff + mypy)
make lint

# Format (black + ruff)
make format

# Run demo scenarios
python examples/demo_scenario_a.py
```

## Architecture

This is an MCP (Model Context Protocol) server exposing a **deterministic simulation engine** — AI agents use it to query/mutate simulation state and model complex systems reproducibly.

### Core Data Flow

1. MCP client calls a tool in `server.py` → 2. `SimulationEngine` validates constraints → 3. Action applied atomically (rollback on violation) → 4. Event appended to immutable history

### Key Modules

- **`models.py`** — Pydantic v2 models: `SimulationState` (schema v1), `ActionResult`, `HistoryEvent`, `ConstraintViolation`
- **`simulation.py`** — `SimulationEngine`: central orchestrator; `apply_action()` runs constraint checks + rollback, `fork()` branches timelines, `reset()` is deterministic via seed
- **`actions.py`** — 8 registered actions (`step`, `set_resource`, `adjust_resource`, `set_metric`, `set_flag`, `add_entity`, `remove_entity`, `simulate_load`); registry pattern for extensibility
- **`constraints.py`** — Protocol-based constraint system; built-ins: `NonNegativeResourceConstraint`, `MaxResourceConstraint`, `TimeMonotonicConstraint`
- **`dynamic_rules.py`** — JSON-defined `DynamicRule`s with recursive condition evaluation (comparison, and, or, not, always) and formula actions (add/subtract/multiply/divide); value sources: resource, metric, flag, metadata, time, literal
- **`world_rules.py`** — `WorldRuleEngine` that applies dynamic rules after each action
- **`persistence.py`** — Save/load to `~/.mcp-scenario-engine/simulations/`; persists state + rules + history
- **`server.py`** — 16 MCP tools across four groups: state management, action execution, world rules CRUD, persistence

### State Schema (v1)

`SimulationState` fields: `schema_version`, `simulation_id`, `created_at`, `updated_at`, `seed`, `time` (int step counter), `resources` (Dict[str, float]), `metrics` (Dict[str, float]), `flags` (Dict[str, bool]), `entities` (Dict[str, Dict]), `metadata` (Dict[str, Any])

### Design Constraints

- **Determinism:** same seed → identical results; never use non-seeded randomness
- **Immutability:** history events are append-only; constraint violations trigger rollback, not partial state
- **Strict typing:** `mypy` strict mode is enforced — annotate all new code
- **Line length:** 100 characters (black + ruff)