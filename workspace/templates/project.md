# Template: Project & Resource Planning

> 1 step = 1 sprint (1–2 weeks)

## Initial Values

### Entities
```
team:
  size: 5
  velocity: 40           # story points per sprint
  technology: "..."
product:
  name: "Product name"
  phase: "development"
```

### Resources
```
budget_eur: 100000
story_points_total: 400
story_points_done: 0
technical_debt: 0        # accumulated debt (arbitrary units)
```

### Metrics
```
velocity_current: 40
burn_rate_eur_week: 5000
quality_score: 80        # 0–100
risk_score: 20           # 0–100
```

### Flags
```
on_track: true
scope_creep: false
key_person_risk: false
```

## World Rules

### Sprint Progress
- **Condition:** `always`
- **Action:** `story_points_done += 40`, `budget_eur -= 5000`
- **Rationale:** Base velocity and burn rate per sprint

### Budget Warning
- **Condition:** `budget_eur < 20000`
- **Action:** `risk_score = 60`, `on_track = false`
- **Rationale:** Below 20% budget → critical

### Scope Creep
- **Condition:** `scope_creep == true`
- **Action:** `story_points_total += 20`, `quality_score -= 2`
- **Rationale:** Each sprint with scope creep increases total scope

## Scenarios
| Scenario | Deviation | Question |
|---|---|---|
| Base | – | Delivery within budget? |
| Key person leaves | `velocity_current = 25` from sprint 3 | When does deadline risk arise? |
| Scope Creep | `scope_creep = true` | How many extra sprints? |
