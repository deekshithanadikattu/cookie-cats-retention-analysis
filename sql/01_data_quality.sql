-- Q1. Row count, duplicate players, missing IDs
SELECT COUNT(*)               AS total_rows,
       COUNT(DISTINCT userid) AS unique_players,
       SUM(userid IS NULL)    AS missing_ids
FROM players;

-- Q2. Are the A/B groups roughly the same size?
SELECT version, COUNT(*) AS players
FROM players
GROUP BY version;

-- Q3. Range of game rounds played (look at the max!)
SELECT MIN(sum_gamerounds) AS min_rounds,
       MAX(sum_gamerounds) AS max_rounds,
       ROUND(AVG(sum_gamerounds), 1) AS avg_rounds
FROM players;

-- Q4. Top 5 players by rounds played: is anyone suspicious?
SELECT userid, version, sum_gamerounds
FROM players
ORDER BY sum_gamerounds DESC
LIMIT 5;

-- Q5. How many players installed the game but played 0 rounds?

SELECT SUM(sum_gamerounds = 0) AS zero_round_players,
       ROUND(100.0 * SUM(sum_gamerounds = 0) / COUNT(*), 1) AS pct_of_players
FROM players;