"""Step 1: load the Cookie Cats CSV into a SQLite database (cookie_cats.db)."""
import sqlite3
import pandas as pd

df = pd.read_csv("data/cookie_cats.csv")
# retention columns come in as True/False; store them as 1/0 so SQL can SUM/AVG them
df["retention_1"] = df["retention_1"].astype(int)
df["retention_7"] = df["retention_7"].astype(int)

con = sqlite3.connect("cookie_cats.db")
df.to_sql("players", con, if_exists="replace", index=False)
print(f"Loaded {len(df):,} players into cookie_cats.db (table: players)")
