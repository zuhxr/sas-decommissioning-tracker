import sqlite3
import pandas as pd
import os

conn = sqlite3.connect('data/tracker.db')
os.makedirs('results', exist_ok=True)


# For assets not yet migrated, how many are left per department, how many days of work, and how much money?
q1 = """
SELECT owning_department,
       COUNT(*) AS assets_remaining,
       SUM(est_migration_days) AS days_required,
       SUM(est_cost_eur) AS cost_to_complete
FROM assets
WHERE migration_status NOT IN ('Migrated', 'Decommissioned')
GROUP BY owning_department
ORDER BY cost_to_complete DESC;
"""

# Which unfinished assets have not been run in over 24 months?
q2 = """
SELECT asset_id, asset_name, owning_department, est_cost_eur, last_run_date
FROM assets
WHERE last_run_date < date('now', '-24 months') AND migration_status NOT IN ('Migrated', 'Decommissioned')
ORDER BY est_cost_eur DESC;
"""

# Which unfinished assets contain personal data?
q3 = """
SELECT asset_id, asset_name, owning_department, business_criticality
FROM assets
WHERE migration_status NOT IN ('Migrated', 'Decommissioned') AND contains_personal_data = 1;
"""

# Which Critical or High criticality assets have no assigned owner?
q4 = """
SELECT asset_id, asset_name, owning_department, business_criticality
FROM assets
WHERE business_criticality IN ('Critical', 'High') AND assigned_owner IS NULL;
"""

# How many assets in each migration status, and what percentage of the total?
q5 = """
SELECT migration_status, COUNT(*) AS count,
ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM assets), 2) AS percentage
FROM assets
GROUP BY migration_status;
"""

# Which AI Act relevant assets aren't migrated yet?
q6 = """
SELECT asset_id, asset_name, owning_department, business_criticality, asset_type
FROM assets
WHERE ai_act_relevant = 1 AND migration_status NOT IN ('Migrated', 'Decommissioned');
"""

queries = [
    ('Q1', 'Cost to complete by department', q1),
    ('Q2', 'Assets unused 24+ months', q2),
    ('Q3', 'Unmigrated assets with personal data', q3),
    ('Q4', 'Critical/High assets with no owner', q4),
    ('Q5', 'Migration progress by status', q5),
    ('Q6', 'AI Act relevant assets not migrated', q6),
]

for name, description, query in queries:
    df = pd.read_sql_query(query, conn)
    df.to_csv(f'results/{name.lower()}.csv', index=False)
    print(f"\n=== {name}: {description}  ({len(df)} rows) ===")
    print(df.to_string(index=False))

conn.close()