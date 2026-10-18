
-- =============================================================
-- SAS Decommissioning Migration Tracker
-- Analysis queries against data/tracker.db (table: assets)
-- =============================================================


-- Q1: What is the remaining cost and effort per department?
-- For assets not yet migrated, how many are left per department, how many days of work, and how much money?

SELECT owning_department,
       COUNT(*) AS assets_remaining,
       SUM(est_migration_days) AS days_required,
       SUM(est_cost_eur) AS cost_to_complete
FROM assets
WHERE migration_status NOT IN ('Migrated', 'Decommissioned')
GROUP BY owning_department
ORDER BY cost_to_complete DESC;


-- Q2: Which unfinished assets have not been run in over 24 months?
-- For assets unused 24+ months

SELECT asset_id, asset_name, owning_department, est_cost_eur, last_run_date
FROM assets
WHERE last_run_date < date('now', '-24 months') AND migration_status NOT IN ('Migrated', 'Decommissioned')
ORDER BY est_cost_eur DESC;


-- Q3: Which unfinished assets contain personal data?
-- For unmigrated assets with personal data

SELECT asset_id, asset_name, owning_department, business_criticality
FROM assets
WHERE migration_status NOT IN ('Migrated', 'Decommissioned') AND contains_personal_data = 1;


-- Q4: Which Critical or High criticality assets have no assigned owner?
-- For assets with high business criticality and no assigned owner

SELECT asset_id, asset_name, owning_department, business_criticality
FROM assets
WHERE business_criticality IN ('Critical', 'High') AND assigned_owner IS NULL;


-- Q5: How many assets in each migration status, and what percentage of the total?
-- For each migration status, count the number of assets and calculate the percentage

SELECT migration_status, COUNT(*) AS count,
ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM assets), 2) AS percentage
FROM assets
GROUP BY migration_status;


-- Q6: Which AI Act relevant assets aren't migrated yet?
-- For assets that are relevant to the AI Act and not yet migrated

SELECT asset_id, asset_name, owning_department, business_criticality, asset_type
FROM assets
WHERE ai_act_relevant = 1 AND migration_status NOT IN ('Migrated', 'Decommissioned');
