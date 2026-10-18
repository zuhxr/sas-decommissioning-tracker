import pandas as pd
from faker import Faker
import random

fake = Faker('de_DE')
random.seed(42)

DEPARTMENTS = ['Actuarial', 'Finance', 'Claims', 'Underwriting',
               'Risk & Compliance', 'Marketing Analytics']
ASSET_TYPES = ['Regulatory Report', 'Actuarial Model', 'ETL Job',
               'Ad-hoc Analysis', 'Dashboard Feed', 'Pricing Model']
TARGETS = ['Python / Databricks', 'SQL / Snowflake', 'Power BI',
           'Decommission - no replacement']
STATUS = ['Not started', 'Discovery', 'In migration', 'Testing',
          'Migrated', 'Decommissioned']

rows = []
for i in range(60):
    asset_type = random.choice(ASSET_TYPES)
    is_model = 'Model' in asset_type
    rows.append({
        'asset_id': f'SAS-{1000 + i}',
        'asset_name': f'{fake.word().capitalize()}_{asset_type.replace(" ", "_")}',
        'asset_type': asset_type,
        'owning_department': random.choice(DEPARTMENTS),
        'business_criticality': random.choices(
            ['Critical', 'High', 'Medium', 'Low'], weights=[1, 3, 4, 2])[0],
        'last_run_date': fake.date_between(start_date='-3y', end_date='today'),
        'est_migration_days': random.randint(2, 45),
        'day_rate_eur': random.choice([750, 900, 1100]),
        'target_platform': random.choice(TARGETS),
        'migration_status': random.choice(STATUS),
        'contains_personal_data': random.choice([True, False]),
        'ai_act_relevant': is_model,
        'assigned_owner': random.choice([fake.name(), fake.name(), None]),
    })

df = pd.DataFrame(rows)
df['est_cost_eur'] = df['est_migration_days'] * df['day_rate_eur']
df.to_csv('data/sas_asset_inventory.csv', index=False)

print(df.head())
print(f"{len(df)} assets, total est. cost EUR {df['est_cost_eur'].sum():,}")