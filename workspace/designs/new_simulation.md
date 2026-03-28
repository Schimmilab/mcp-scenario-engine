# Simulation Design: [Name]

## Goal
What should this simulation answer / demonstrate?

## Context
- Time period:
- 1 step corresponds to:
- Seed:

## Initial Values

### Entities
```
person / system / team:
  - attribute: value
```

### Resources (quantitative, variable)
```
resource_name: initial_value  # unit – what is being measured
```

### Metrics (KPIs, derived values)
```
metric_name: initial_value  # what does this express
```

### Flags (state switches)
```
flag_name: true/false  # when active, what does this mean
```

## Dynamics (World Rules)

### Rule 1: [Name]
- **Condition:** when the rule applies
- **Action:** what happens then
- **Rationale:** why this is realistic

### Rule 2: [Name]
- ...

## Scenarios / Forks
| Scenario | Deviation from base | Question |
|---|---|---|
| Base | – | What happens without intervention? |
| Optimistic | Flag X = true, Resource Y +20% | Best case? |
| Pessimistic | Resource Y -30% | What if things go wrong? |

## Evaluation
- Which metrics are decisive?
- After how many steps to evaluate?
- Which thresholds indicate success/failure?

## Notes
