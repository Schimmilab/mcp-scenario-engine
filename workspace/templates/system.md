# Template: System / Load Simulation

> 1 step = 1 hour or 1 day

## Initial Values

### Entities
```
server:
  type: "web"
  cores: 8
  ram_gb: 32
database:
  type: "postgres"
  max_connections: 200
```

### Resources
```
cpu_pct: 30
ram_pct: 45
db_connections: 50
queue_length: 0
```

### Metrics
```
requests_per_min: 1000
latency_ms: 120
error_rate_pct: 0.1
uptime_pct: 100
```

### Flags
```
peak_traffic: false
maintenance_mode: false
auto_scaling_active: true
```

## World Rules

### CPU → Latency Correlation
- **Condition:** `cpu_pct > 80`
- **Action:** `latency_ms += 50`, `error_rate_pct += 0.5`
- **Rationale:** Overloaded server increases response time and error rate

### Queue Build-Up Under Overload
- **Condition:** `requests_per_min > 2000`
- **Action:** `queue_length += 100`
- **Rationale:** More requests than capacity → queue grows

### Auto-Scaling
- **Condition:** `auto_scaling_active == true` AND `cpu_pct > 70`
- **Action:** `cpu_pct -= 20`
- **Rationale:** New instance absorbs load

## Scenarios
| Scenario | Deviation | Question |
|---|---|---|
| Normal operation | – | Stability in daily use? |
| Traffic spike | `requests_per_min = 5000` from step 3 | System under high load? |
| Auto-scaling failure | `auto_scaling_active = false` | How quickly does it break? |
