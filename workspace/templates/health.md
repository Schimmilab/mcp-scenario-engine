# Template: Health & Body Composition

> 1 step = 1 week

## Initial Values

### Entities
```
person:
  name: "Name"
  age: 0
  height_cm: 175
```

### Resources
```
weight_kg: 85.0           # current body weight
body_fat_pct: 25.0        # body fat percentage
muscle_mass_kg: 60.0      # muscle mass
water_pct: 55.0           # body water percentage
calorie_balance_kcal: 0   # daily calorie deficit (negative) or surplus
```

### Metrics
```
bmi: 27.8
ffm_kg: 63.75             # fat-free mass
tdee_kcal: 2400           # Total Daily Energy Expenditure
training_days_week: 4
```

### Flags
```
active_lifestyle: true
calorie_tracking: true
strength_training: true
```

## World Rules

### Weekly Weight Loss
- **Condition:** `calorie_balance_kcal < 0`
- **Action:** `weight_kg -= 0.3` per step
- **Rationale:** ~500 kcal/day deficit ≈ 0.3 kg/week loss

### Muscle Gain Through Strength Training
- **Condition:** `strength_training == true`
- **Action:** `muscle_mass_kg += 0.05` per step
- **Rationale:** Natural gain ~0.05–0.1 kg/week for intermediate trainees

### Plateau Effect (optional)
- **Condition:** every 8 steps (`time_modulo: 8`)
- **Action:** `calorie_balance_kcal += 100`
- **Rationale:** Adaptive thermogenesis – body adjusts TDEE downward

## Scenarios
| Scenario | Deviation | Question |
|---|---|---|
| Base | – | Trajectory with constant deficit? |
| Stagnation | `calorie_balance_kcal = 0` from week 6 | What happens during a diet break? |
| Aggressive | `calorie_balance_kcal = -700` | Faster loss, muscle loss? |
