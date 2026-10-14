# Cookie Cats: Player Retention A/B Test Analysis (SQL + ECharts)

**Question:** Does moving the first progression gate in a mobile puzzle game from level 30 to level 40 change how many players come back?

**Live dashboard:** _add your GitHub Pages link here_

## Data
Public Cookie Cats A/B test dataset (Tactile Entertainment, via Kaggle/DataCamp): **90,189 players**, randomly assigned to:
- `gate_30`: first gate at level 30 (control)
- `gate_40`: first gate moved to level 40

| Column | Meaning |
|---|---|
| `userid` | Player ID |
| `version` | A/B group (`gate_30` / `gate_40`) |
| `sum_gamerounds` | Game rounds played in the first 14 days |
| `retention_1` / `retention_7` | Player returned 1 / 7 days after install |

## Data-quality checks (`sql/01_data_quality.sql`)
- No duplicate or missing player IDs; A/B groups are balanced (44,700 vs 45,489).
- **3,994 players (4.4%)** installed but played 0 rounds.
- **One impossible outlier:** a player logged 49,854 rounds in 14 days (next highest: 2,961). It inflated the gate_30 average from 51.3 to 52.5 rounds, so it was excluded from the analysis.

## Findings (`sql/02_retention.sql`)
| Group | Day-1 retention | Day-7 retention |
|---|---|---|
| gate_30 | 44.82% | 19.02% |
| gate_40 | 44.23% | 18.20% |

1. **Moving the gate to level 40 lowered 7-day retention by 0.8 points** (19.02% → 18.20%). The difference is statistically significant (two-proportion z-test, p ≈ 0.002).
2. **Day-1 retention dropped slightly (0.6 points), but that is not statistically significant** (p ≈ 0.07), so the data does not support a day-1 effect.
3. **The gap is concentrated among players with 40–99 rounds** (32.9% vs 29.4% day-7 retention), around where gate_40 players hit the gate. One likely explanation: an earlier gate forces a break that brings players back refreshed.

**Recommendation:** keep the gate at level 30.

**Limitations:** rounds played is not the same as levels reached, and engagement tiers are based on behavior after assignment, so the tier breakdown shows *where* the effect appears rather than proving the cause.

## Project structure
```
load_data.py        # loads the CSV into SQLite (cookie_cats.db)
run_sql.py          # runs a .sql file and prints each result
sql/                # data-quality and retention queries (CTEs, CASE tiers, aggregations)
export_data.py      # runs the analysis queries and writes dashboard/data.js
dashboard/          # JavaScript + Apache ECharts dashboard
```

## How to run
```
python load_data.py
python run_sql.py sql/01_data_quality.sql
python run_sql.py sql/02_retention.sql
python export_data.py
```
Then open `dashboard/index.html` in a browser.

**Tools:** SQL (SQLite), Python (Pandas), JavaScript, Apache ECharts
