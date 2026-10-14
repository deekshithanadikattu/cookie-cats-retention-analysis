"""Step 3a: run the analysis queries and save the results to dashboard/data.js
so the ECharts dashboard can read them (works by just double-clicking the HTML)."""
import json, sqlite3
import pandas as pd

con = sqlite3.connect("cookie_cats.db")

# Chart 1 data: retention by A/B group (outlier removed)
by_group = pd.read_sql("""
    WITH clean_players AS (SELECT * FROM players WHERE sum_gamerounds < 10000)
    SELECT version,
           ROUND(100.0 * AVG(retention_1), 2) AS day1,
           ROUND(100.0 * AVG(retention_7), 2) AS day7
    FROM clean_players GROUP BY version ORDER BY version
""", con)

# Chart 2 data: day-7 retention by engagement tier and group
by_tier = pd.read_sql("""
    WITH clean_players AS (SELECT * FROM players WHERE sum_gamerounds < 10000),
    tiered AS (
        SELECT *, CASE WHEN sum_gamerounds = 0 THEN '0 rounds'
                       WHEN sum_gamerounds < 30 THEN '1-29'
                       WHEN sum_gamerounds < 40 THEN '30-39'
                       WHEN sum_gamerounds < 100 THEN '40-99'
                       ELSE '100+' END AS tier
        FROM clean_players)
    SELECT tier, version, ROUND(100.0 * AVG(retention_7), 2) AS day7
    FROM tiered GROUP BY tier, version ORDER BY MIN(sum_gamerounds), version
""", con)

tiers = list(dict.fromkeys(by_tier["tier"]))  # keeps order, removes repeats
data = {
    "groups": by_group["version"].tolist(),
    "day1": by_group["day1"].tolist(),
    "day7": by_group["day7"].tolist(),
    "tiers": tiers,
    "tier_gate30": by_tier[by_tier.version == "gate_30"]["day7"].tolist(),
    "tier_gate40": by_tier[by_tier.version == "gate_40"]["day7"].tolist(),
}
with open("dashboard/data.js", "w") as f:
    f.write("const DATA = " + json.dumps(data, indent=2) + ";\n")
print("Wrote dashboard/data.js")
print(json.dumps(data, indent=2))
