"""Run every query in a .sql file and print the results.
Usage:  python run_sql.py sql/01_data_quality.sql
Queries are separated by semicolons; lines starting with -- are comments."""
import sqlite3, sys
import pandas as pd

con = sqlite3.connect("cookie_cats.db")
text = open(sys.argv[1]).read()
for block in text.split(";"):
    lines = [l for l in block.strip().splitlines()]
    sql = "\n".join(l for l in lines if not l.strip().startswith("--")).strip()
    if not sql:
        continue
    title = next((l.strip("- ").strip() for l in lines if l.strip().startswith("--")), "")
    print(f"\n=== {title} ===")
    print(pd.read_sql(sql, con).to_string(index=False))
