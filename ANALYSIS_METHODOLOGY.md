# Seasonal Decomposition Analysis - Methodology & Insights Guide

## What is Seasonal Decomposition?

Seasonal decomposition separates a time series into four independent components:

```
Observed = Trend + Seasonal + Residual
(Additive Model)
```

### Component Definitions

**1. Observed (Original Data)**
- The raw time series you measure
- Daily flight count, cancellation rate, delay, etc.
- Contains all information but is difficult to interpret directly

**2. Trend**
- Long-term direction (increasing, decreasing, or stable)
- Smoothed pattern that removes short-term noise
- Shows whether the metric is improving or deteriorating
- Time scale: weeks to months

**3. Seasonal**
- Repeating pattern at regular intervals
- In this analysis: weekly patterns (Monday through Sunday)
- Shows which days are systematically higher or lower
- Predictable, repeats in every cycle

**4. Residual**
- What remains after removing trend and seasonal
- Represents anomalies and irregular events
- Should be mostly noise with few large spikes
- Large residuals indicate unusual days worth investigating

---

## Why Period = 7 (Weekly)?

We use a 7-day period because:

1. **Business Cycle**: Monday-Friday differ from Saturday-Sunday
2. **Passenger Behavior**: Weekday (business) vs weekend (leisure) patterns
3. **Operations**: Staffing and scheduling follow weekly cycles
4. **Data Signal**: Flight data shows clear 7-day repetition

---

## Interpreting Each Chart

### Flight Count Decomposition

**Why it matters:**
- Flight volume = fundamental operational metric
- Trend = strategic capacity decisions
- Seasonal pattern = scheduling optimization opportunities

**What to look for:**
- **Strong trend** (steep slope) = significant growth/decline
- **Strong seasonal** (large peaks/valleys) = highly predictable demand
- **Large residuals** on specific dates = unusual events (holidays, weather, disruptions)

**Actionable Insights:**
- Increasing trend → Plan fleet expansion, hire staff
- Decreasing trend → Consider consolidation, optimize routes
- High Friday peak → Extra crew, maintenance slots for Monday
- Large spike → Investigate cause (holiday, event, system outage)

---

### Cancellation Rate Decomposition

**Why it matters:**
- Cancellation = customer dissatisfaction and operational failure
- Trend = whether operations are getting more or less reliable
- Seasonal = predictable patterns for planning/recovery

**What to look for:**
- **Increasing trend** = ALERT - operational reliability worsening
- **High on weekends** = weather likely culprit
- **High on Mondays** = possible backlog from weekend disruptions
- **Large residual on one date** = specific event (weather, mechanical)

**Actionable Insights:**
- Investigate days with high residual spikes
- Compare high vs low cancellation days for best practices
- Correlate with weather data and maintenance logs
- Seasonal pattern suggests preventative action timing

---

### Air Time Decomposition

**Why it matters:**
- Air time = operational efficiency (alongside distance)
- Trend = fleet efficiency changes or route modifications
- Seasonal = aircraft mix or congestion patterns by day

**What to look for:**
- **Increasing trend** = flights taking longer (worse efficiency)
  - Could indicate: longer routes, older aircraft, more congestion, stronger headwinds
- **Decreasing trend** = flights getting faster (improving efficiency)
  - Could indicate: new aircraft, optimized routes, favorable winds
- **Large standard deviation** = inconsistent operations
- **Day-of-week variation** = different equipment or routes used on different days

**Actionable Insights:**
- Compare highest vs lowest air time days for operational differences
- Investigate if seasonal pattern correlates with fleet maintenance schedule
- Long-term increasing trend = efficiency initiative opportunity
- High variability = potential for standardization/optimization

---

### Delay Intensity Decomposition

**Why it matters:**
- Delay = customer experience and operational reliability
- Intensity = average delay per flight (normalized by volume)
- Most directly impacts customer satisfaction

**What to look for:**
- **Increasing trend** = getting worse (concerning trend)
- **Decreasing trend** = improvements working (positive trend)
- **High on specific days** = predictable patterns (e.g., Friday congestion)
- **Large residuals** = unexpected events (storms, system failures, incidents)
- **High variance** = inconsistent operations

**Actionable Insights:**
- Large residuals = correlate with weather reports, ATC delays, mechanical issues
- If trend is increasing: emergency intervention needed
- Seasonal pattern = proactive scheduling/planning opportunity
- Best vs worst days = analyze operational differences for replication

---

## Seasonal Strength Metric (0 to 1)

**Formula**: 
```
Seasonal Strength = 1 - (Var(Residual) / Var(Seasonal + Residual))
```

**Interpretation:**
- **0.0 - 0.2**: Very weak weekly pattern (similar across all days)
- **0.2 - 0.5**: Moderate weekly pattern (some day-to-day variation)
- **0.5 - 0.8**: Strong weekly pattern (clear daily preferences)
- **0.8 - 1.0**: Very strong weekly pattern (highly predictable)

**What it means for operations:**
- **Strong (>0.5)**: Weekly patterns are reliable for planning
  - Schedule critical maintenance on quiet days
  - Staff up on consistently busy days
  - Plan cushion for high-delay days

- **Weak (<0.3)**: Day-to-day variation is unpredictable
  - Can't rely on day-of-week patterns
  - May indicate other factors at play (weather, demand volatility)
  - Need investigation into root causes

---

## How to Read the 4-Panel Decomposition Plots

### Top Panel (Observed)
- Raw data with all variability
- Note the overall range and volatility
- Trend can be visually identified

### Second Panel (Trend)
- Smooth curve showing long-term direction
- Ignore short-term up/down movements
- Focus on slope direction and magnitude
- Critical for strategic decisions

### Third Panel (Seasonal)
- Repeating pattern, typically smaller in magnitude
- Height = strength of daily effect
- Pattern repeats exactly every 7 days
- Shows which days are systematically higher/lower

### Bottom Panel (Residual)
- What's left over after removing trend and seasonal
- Should look like random noise centered at zero
- Large spikes = anomalies worth investigating
- Baseline level of unexplained variation

---

## Real-World Example: Cancellation Rate

**Hypothetical Pattern:**

```
Trend: Slight upward slope (from 2.1% to 2.3%)
→ Interpretation: Cancellations slowly getting worse

Seasonal: High peak on Sundays, low on Tuesdays
→ Interpretation: Weekend weather delays, weekday operational consistency

Residual: Large spike on Jan 17, Feb 28
→ Interpretation: Investigate those specific dates (likely major weather events)
```

**Actions Based on This:**
1. **Trend**: Launch reliability improvement initiative
2. **Seasonal**: 
   - Sunday: Extra maintenance crews ready for Monday recovery
   - Tuesday: This is our best day operationally - study why
3. **Residual**:
   - Jan 17: Check historical weather - was there a blizzard?
   - Feb 28: Correlate with ATC data - was there a system outage?

---

## When Decomposition Might Mislead

⚠️ **Cautions:**
- If data has missing values, decomposition quality decreases
- Seasonal component assumes perfect 7-day cycle (holidays/events break this)
- Trend assumes smooth change (sudden operational changes cause artifacts)
- Residuals still contain information not captured (external factors)

**Best Practices:**
1. Always inspect the raw data first
2. Cross-check residual spikes with external events
3. Combine with domain knowledge (operations, maintenance)
4. Don't rely solely on statistical decomposition
5. Investigate anomalies with actual data investigation

---

## Connecting Components Back to Operations

### For Operations Manager
"Which days should I staff up and why?"
- Look at **seasonal component** of flight count
- Staff peaks happen on systematically high-demand days
- **Residuals** show unexpected surges requiring flexibility

### For Reliability Officer
"Why are cancellations increasing?"
- Check **trend** direction and slope
- Compare cancellation rate **seasonal** vs flight count seasonal
- Investigate **large residual spikes** (specific events)

### For Finance/Planning
"What's the growth trajectory?"
- **Trend** shows operational scale changes
- **Seasonal** shows predictable within-week variation
- **Residuals** represent disruption risk

### For Quality/Continuous Improvement
"Which days/weeks need focus?"
- High **residual** values = specific dates worth auditing
- **Seasonal peaks** = where improvements have biggest impact
- **Trend** = whether historical improvements are sustained

---

## Next Steps After Analysis

1. **Investigate Residuals**
   - Large spikes = correlate with external factors
   - Create incident log cross-reference

2. **Test Seasonal Insights**
   - Design A/B tests on high vs low seasonal days
   - What operational differences exist?

3. **Trend Analysis**
   - Extract trend slope for forecasting
   - Project capacity needs 6-12 months out

4. **Predictive Modeling**
   - Use seasonal pattern for demand forecasting
   - Reduce uncertainty for capacity planning

5. **Monitoring Dashboard**
   - Track if trends reverse (improvement/deterioration)
   - Alert if seasonal pattern breaks down
   - Monitor for new residual spikes

---

## Statistical Background (Optional)

**Additive Model Used**:
$$Y_t = T_t + S_t + R_t$$

Where:
- $Y_t$ = Observed value at time t
- $T_t$ = Trend component
- $S_t$ = Seasonal component
- $R_t$ = Residual/error component

**Why Additive?**
- Seasonal effect is roughly constant in magnitude
- Temperature of decomposition doesn't change amplitude

**Alternative (Multiplicative)**:
$$Y_t = T_t \times S_t \times R_t$$
Used when seasonal effect grows with trend (e.g., sales growing + seasonal %growth)

**Method: STL (Seasonal-Trend decomposition using Loess)**
- More robust than classical decomposition
- Handles irregular patterns better
- Sets period=7 for weekly frequency
- extrapolate_trend='freq' fills edges with frequency domain extrapolation

