# Boatrace Data Types

Explanation of each CSV data type available from BoatraceCSV.

## Data Types

### Programs (出走表) - `/data/programs/{YYYY}/{MM}/{DD}.csv`

Scheduled race information and entry list.

**When to use:** When users ask for entry information, scheduled race details, or starting lineup.

**Key information:** Competitor information, race schedule, entry positions.

### Previews (直前情報) - `/data/previews/{YYYY}/{MM}/{DD}.csv`

Preview information published just before races start.

**When to use:** When users ask for pre-race information, race forecasts, or last-minute updates.

**Key information:** Pre-race conditions, competitor status, weather.

### Results (レース結果) - `/data/results/{YYYY}/{MM}/{DD}.csv`

Final race results and finishing order.

**When to use:** When users ask for race results, winners, finishing times, or race outcomes.

**Key information:** Race results, finishing order, race times.

### Estimates (レース予想) - `/data/estimate/{YYYY}/{MM}/{DD}.csv`

Race predictions/estimates.

**When to use:** When users ask for race predictions or estimates.

**Key information:** Predicted outcomes, estimates.

### Confirms (レース予想結果) - `/data/confirm/{YYYY}/{MM}/{DD}.csv`

Confirmed prediction results.

**When to use:** When users ask for confirmed prediction results or prediction accuracy.

**Key information:** Confirmed predictions, accuracy data.

## URL Format

All URLs follow the pattern:

```
https://boatracecsv.github.io/data/{data_type}/{YYYY}/{MM}/{DD}.csv
```

Where:
- `data_type`: programs, previews, results, estimate, confirm
- `YYYY`: 4-digit year
- `MM`: 2-digit month (01-12)
- `DD`: 2-digit day (01-31)

Example: `https://boatracecsv.github.io/data/programs/2026/01/20.csv`
