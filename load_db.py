import pandas as pd
import sqlite3

df = pd.read_csv('data/sas_asset_inventory.csv')

conn = sqlite3.connect('data/tracker.db')
df.to_sql('assets', conn, if_exists='replace', index=False)
conn.close()

print(f"Loaded {len(df)} rows into data/tracker.db")