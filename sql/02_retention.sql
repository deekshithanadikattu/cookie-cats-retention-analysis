-- R1. Retention by A/B group (all players)
SELECT version,
       COUNT(*)                          AS players,
       ROUND(100.0 * AVG(retention_1), 2) AS day1_retention_pct,
       ROUND(100.0 * AVG(retention_7), 2) AS day7_retention_pct
FROM players
GROUP BY version;

-- R2. Same comparison, after removing the 49,854-round outlier (CTE = a named temporary result)
WITH clean_players AS (
    SELECT *
    FROM players
    WHERE sum_gamerounds < 10000          -- drop the impossible outlier found in Q4
)
SELECT version,
       COUNT(*)                          AS players,
       ROUND(AVG(sum_gamerounds), 1)      AS avg_rounds,
       ROUND(100.0 * AVG(retention_1), 2) AS day1_retention_pct,
       ROUND(100.0 * AVG(retention_7), 2) AS day7_retention_pct
FROM clean_players
GROUP BY version;

-- R3. Engagement tiers: how does retention change as players play more rounds? (two chained CTEs)
WITH clean_players AS (
    SELECT * FROM players WHERE sum_gamerounds < 10000
),
tiered AS (
    SELECT *,
           CASE
               WHEN sum_gamerounds = 0    THEN '0 rounds'
               WHEN sum_gamerounds < 30   THEN '1-29'
               WHEN sum_gamerounds < 40   THEN '30-39'
               WHEN sum_gamerounds < 100  THEN '40-99'
               ELSE '100+'
           END AS engagement_tier
    FROM clean_players
)
SELECT engagement_tier,
       version,
       COUNT(*)                          AS players,
       ROUND(100.0 * AVG(retention_7), 2) AS day7_retention_pct
FROM tiered
GROUP BY engagement_tier, version
ORDER BY MIN(sum_gamerounds), version;
