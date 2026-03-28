"""Core simulation engine with deterministic execution."""

import copy
import random
import sys
from datetime import datetime, UTC
from typing import Any
from uuid import UUID

import structlog

from .actions import ACTION_REGISTRY, Action
from .constraints import ConstraintEngine
from .models import ActionResult, EventType, HistoryEvent, SimulationState
from .world_rules import WorldRuleEngine

# Configure logging to stderr for MCP compatibility
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
)

logger = structlog.get_logger()


def compute_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Compute delta between two state dictionaries."""
    delta: dict[str, Any] = {}

    # Find changed/added keys
    for key in after:
        if key not in before:
            delta[key] = {"added": after[key]}
        elif before[key] != after[key]:
            delta[key] = {"before": before[key], "after": after[key]}

    # Find removed keys
    for key in before:
        if key not in after:
            delta[key] = {"removed": before[key]}

    return delta


class SimulationEngine:
    """Core simulation engine with state management, constraints, and history."""

    def __init__(self, initial_state: SimulationState | None = None, seed: int | None = None):
        """Initialize simulation engine."""
        self.state = initial_state or SimulationState(seed=seed)
        if seed is not None:
            self.state.seed = seed

        self.constraint_engine = ConstraintEngine()
        self.world_rule_engine = WorldRuleEngine()
        self.history: list[HistoryEvent] = []
        self.snapshots: list[dict] = []  # Time-series snapshots recorded at each step
        self.rng = random.Random(seed)

        # Initialize with creation event
        self._add_event(
            EventType.SIMULATION_CREATED,
            reason=f"Simulation created with seed {seed}",
        )

        logger.info(
            "simulation_created",
            simulation_id=str(self.state.simulation_id),
            seed=seed,
        )

    def get_state(self) -> SimulationState:
        """Get current simulation state."""
        return self.state.model_copy()

    def get_timeseries(
        self,
        variables: list[str] | None = None,
        from_time: int | None = None,
        to_time: int | None = None,
    ) -> list[dict]:
        """Get time-series snapshots. Optionally filter by variable names and time range."""
        result = self.snapshots

        if from_time is not None:
            result = [s for s in result if s["time"] >= from_time]
        if to_time is not None:
            result = [s for s in result if s["time"] <= to_time]

        if variables:
            filtered = []
            for snap in result:
                row: dict = {"time": snap["time"]}
                for var in variables:
                    if var in snap["resources"]:
                        row[var] = snap["resources"][var]
                    elif var in snap["metrics"]:
                        row[var] = snap["metrics"][var]
                    elif var in snap["flags"]:
                        row[var] = snap["flags"][var]
                filtered.append(row)
            return filtered

        return result

    def get_history(self, limit: int | None = None) -> list[HistoryEvent]:
        """Get simulation history."""
        if limit:
            return self.history[-limit:]
        return self.history.copy()

    def get_event(self, event_id: UUID) -> HistoryEvent | None:
        """Get specific event by ID."""
        for event in self.history:
            if event.event_id == event_id:
                return event
        return None

    def reset(self, seed: int | None = None, keep_rules: bool = False) -> None:
        """Reset simulation to initial state."""
        old_sim_id = self.state.simulation_id
        # Save rules before reset if requested
        saved_rules = self.world_rule_engine.rules.copy() if keep_rules else []

        self.state = SimulationState(seed=seed)
        if seed is not None:
            self.state.seed = seed
            self.rng = random.Random(seed)
        else:
            self.rng = random.Random()

        self.history.clear()
        self.snapshots.clear()

        # Restore rules if requested
        if keep_rules:
            self.world_rule_engine.rules = saved_rules

        self._add_event(
            EventType.SIMULATION_RESET,
            reason=f"Simulation reset with seed {seed}",
        )

        logger.info(
            "simulation_reset",
            old_simulation_id=str(old_sim_id),
            new_simulation_id=str(self.state.simulation_id),
            seed=seed,
        )

    def fork(self, name: str | None = None) -> "SimulationEngine":
        """Create a fork of the current simulation."""
        # Deep copy state
        forked_state = self.state.model_copy()
        forked_state.simulation_id = UUID(int=random.getrandbits(128))
        forked_state.metadata["forked_from"] = str(self.state.simulation_id)
        forked_state.metadata["forked_at_time"] = self.state.time
        if name:
            forked_state.metadata["fork_name"] = name

        # Create new engine with forked state
        forked_engine = SimulationEngine.__new__(SimulationEngine)
        forked_engine.state = forked_state
        forked_engine.constraint_engine = ConstraintEngine()
        forked_engine.world_rule_engine = WorldRuleEngine()
        # Copy constraints and rules
        forked_engine.constraint_engine.constraints = self.constraint_engine.constraints.copy()
        forked_engine.world_rule_engine.rules = self.world_rule_engine.rules.copy()
        forked_engine.history = self.history.copy()
        forked_engine.snapshots = self.snapshots.copy()
        forked_engine.rng = random.Random(self.state.seed)

        # Add fork event
        forked_engine._add_event(
            EventType.TIMELINE_FORKED,
            reason=f"Forked from simulation {self.state.simulation_id} at time {self.state.time}",
        )

        logger.info(
            "simulation_forked",
            parent_id=str(self.state.simulation_id),
            child_id=str(forked_state.simulation_id),
            time=self.state.time,
        )

        return forked_engine

    def apply_action(self, action_name: str, params: dict[str, Any]) -> ActionResult:
        """Apply an action to the simulation."""
        # Get action
        action_class = ACTION_REGISTRY.get(action_name)
        if not action_class:
            raise ValueError(f"Unknown action: {action_name}")

        action = action_class()

        # Store state before
        state_before = self.state.model_copy()

        try:
            # Execute action
            new_state, reason = action.execute(self.state, params, self.rng)

            # Update timestamp
            new_state.updated_at = datetime.now(UTC)

            # Validate constraints
            violations = self.constraint_engine.validate(new_state)

            if violations:
                # Rollback - don't apply state
                event = self._add_event(
                    EventType.CONSTRAINT_VIOLATED,
                    action_name=action_name,
                    params=params,
                    reason=f"Constraint violations: {[v.constraint_id for v in violations]}",
                )

                logger.warning(
                    "constraint_violated",
                    simulation_id=str(self.state.simulation_id),
                    action=action_name,
                    violations=[v.constraint_id for v in violations],
                )

                return ActionResult(
                    success=False,
                    event_id=event.event_id,
                    state_before=state_before,
                    state_after=state_before,  # No change
                    delta={},
                    constraints_violated=violations,
                    message=f"Action rejected due to constraint violations",
                    reason=reason,
                )

            # Apply world rules and record snapshots (per step for multi-step)
            applied_rules: list[str] = []
            steps_taken = int(params.get("steps", 1)) if action_name == "step" else 1

            if action_name == "step" and steps_taken > 1:
                # Re-simulate step-by-step from state_before for proper world rule accumulation
                intermediate = state_before.model_copy()
                for _ in range(steps_taken):
                    intermediate.time += 1
                    intermediate.updated_at = datetime.now(UTC)
                    if self.world_rule_engine.rules:
                        intermediate, step_rules = self.world_rule_engine.apply_rules(intermediate)
                        applied_rules.extend(step_rules)
                    self.snapshots.append({
                        "time": intermediate.time,
                        "resources": dict(intermediate.resources),
                        "metrics": dict(intermediate.metrics),
                        "flags": dict(intermediate.flags),
                    })
                new_state = intermediate
                if applied_rules:
                    unique_rules = list(dict.fromkeys(applied_rules))
                    reason += f" | World rules applied: {', '.join(unique_rules)}"
            elif action_name == "step":
                if self.world_rule_engine.rules:
                    new_state, applied_rules = self.world_rule_engine.apply_rules(new_state)
                    if applied_rules:
                        reason += f" | World rules applied: {', '.join(applied_rules)}"
                self.snapshots.append({
                    "time": new_state.time,
                    "resources": dict(new_state.resources),
                    "metrics": dict(new_state.metrics),
                    "flags": dict(new_state.flags),
                })

            # Apply state change
            self.state = new_state

            # For non-step actions: record snapshot if resources/metrics/flags changed
            if action_name != "step":
                state_changed = (
                    state_before.resources != new_state.resources
                    or state_before.metrics != new_state.metrics
                    or state_before.flags != new_state.flags
                )
                if state_changed:
                    self.snapshots.append({
                        "time": new_state.time,
                        "action": action_name,
                        "resources": dict(new_state.resources),
                        "metrics": dict(new_state.metrics),
                        "flags": dict(new_state.flags),
                    })

            # Compute delta
            delta = compute_delta(
                state_before.model_dump(exclude={"updated_at"}),
                new_state.model_dump(exclude={"updated_at"}),
            )

            # Record event
            event = self._add_event(
                EventType.ACTION_APPLIED,
                action_name=action_name,
                params=params,
                state_delta=delta,
                constraints_checked=self.constraint_engine.get_constraint_ids(),
                reason=reason,
            )

            logger.info(
                "action_applied",
                simulation_id=str(self.state.simulation_id),
                action=action_name,
                event_id=str(event.event_id),
            )

            return ActionResult(
                success=True,
                event_id=event.event_id,
                state_before=state_before,
                state_after=new_state,
                delta=delta,
                message="Action applied successfully",
                reason=reason,
            )

        except Exception as e:
            logger.error(
                "action_failed",
                simulation_id=str(self.state.simulation_id),
                action=action_name,
                error=str(e),
            )
            raise

    def _add_event(
        self,
        event_type: EventType,
        action_name: str | None = None,
        params: dict[str, Any] | None = None,
        state_delta: dict[str, Any] | None = None,
        constraints_checked: list[str] | None = None,
        constraints_violated: list[str] | None = None,
        reason: str | None = None,
    ) -> HistoryEvent:
        """Add an event to history."""
        event = HistoryEvent(
            event_type=event_type,
            action_name=action_name,
            params=params or {},
            state_delta=state_delta or {},
            constraints_checked=constraints_checked or [],
            constraints_violated=constraints_violated or [],
            reason=reason,
        )
        self.history.append(event)
        return event
