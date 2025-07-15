# SQLite Commands for Django dbshell

This guide provides common SQLite commands you can use through Django's `manage.py dbshell`.

## Basic Database Information

```sql
-- Show SQLite version
SELECT sqlite_version();

-- List all tables
SELECT 
    name,
    type 
FROM sqlite_master 
WHERE type='table';

-- Show table schema
.schema table_name

-- Show all tables with their schema
.schema

-- Show table info
PRAGMA table_info(table_name);

-- List all indexes
SELECT 
    name,
    tbl_name 
FROM sqlite_master 
WHERE type='index';
```

## Database Analysis

```sql
-- Get database size
SELECT page_count * page_size as size_bytes 
FROM pragma_page_count(), pragma_page_size();

-- Get table sizes
SELECT 
    name, 
    SUM(pgsize) AS bytes
FROM dbstat 
GROUP BY name 
ORDER BY bytes DESC;

-- Count rows in all tables
SELECT 
    sqlite_master.name,
    COUNT(*) as count 
FROM sqlite_master 
LEFT JOIN sqlite_master AS m ON 1=1
WHERE sqlite_master.type = 'table' 
GROUP BY sqlite_master.name;

-- Get index usage statistics
ANALYZE;
SELECT * FROM sqlite_stat1;
```

## Table Management

```sql
-- Create new table
CREATE TABLE example_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Add column (SQLite has limited ALTER TABLE support)
ALTER TABLE table_name
ADD COLUMN column_name data_type;

-- Rename table
ALTER TABLE old_name RENAME TO new_name;

-- Drop table
DROP TABLE IF EXISTS table_name;

-- Truncate table (SQLite has no TRUNCATE command)
DELETE FROM table_name;
-- or
DROP TABLE IF EXISTS table_name;
CREATE TABLE table_name (...);
```

## Data Management

```sql
-- Insert data
INSERT INTO table_name (column1, column2) 
VALUES ('value1', 'value2');

-- Update data
UPDATE table_name 
SET column1 = value1 
WHERE condition;

-- Delete data
DELETE FROM table_name 
WHERE condition;

-- Bulk insert
BEGIN TRANSACTION;
INSERT INTO table_name (column1, column2) VALUES ('value1', 'value2');
INSERT INTO table_name (column1, column2) VALUES ('value3', 'value4');
COMMIT;
```

## Querying Data

```sql
-- Basic select
SELECT * FROM table_name;

-- Select with conditions
SELECT * 
FROM table_name 
WHERE column1 = 'value'
AND column2 >= 100;

-- Join tables
SELECT t1.*, t2.column_name
FROM table1 t1
LEFT JOIN table2 t2 ON t1.id = t2.table1_id;

-- Group by with aggregates
SELECT 
    column1,
    COUNT(*) as count,
    AVG(number_column) as average
FROM table_name
GROUP BY column1;

-- Subqueries
SELECT *
FROM table1
WHERE id IN (SELECT table1_id FROM table2 WHERE condition);
```

## Maintenance

```sql
-- Vacuum database (reclaim space)
VACUUM;

-- Analyze tables for query optimization
ANALYZE;

-- Reindex
REINDEX table_name;

-- Check database integrity
PRAGMA integrity_check;

-- Optimize database
PRAGMA optimize;
```

## Backup and Export

```sql
-- Backup database (from command line)
.output backup.sql
.dump
.output stdout

-- Backup specific table
.output backup_table.sql
.dump table_name
.output stdout

-- Export query results to CSV
.mode csv
.output data.csv
SELECT * FROM table_name;
.output stdout

-- Import CSV data
.mode csv
.import data.csv table_name
```

## Transaction Management

```sql
-- Start transaction
BEGIN TRANSACTION;

-- Commit transaction
COMMIT;

-- Rollback transaction
ROLLBACK;

-- Set transaction behavior
PRAGMA journal_mode=WAL;  -- Write-Ahead Logging
PRAGMA synchronous=NORMAL;  -- Synchronous setting
```

## Special Commands (SQLite Shell)

```sql
-- Change output format
.mode column   -- Column aligned output
.mode csv      -- CSV output
.mode insert   -- SQL insert statements
.mode line     -- One value per line
.mode list     -- Default delimiter-separated
.mode tabs     -- Tab-separated values
.mode tcl      -- TCL list format

-- Show headers in result
.headers on

-- Format output
.width 10 20 10  -- Set column widths
.timer on        -- Show execution time

-- Save output to file
.output filename.txt
SELECT * FROM table_name;
.output stdout
```

## Usage in Django

1. Connect to database:
```bash
python manage.py dbshell
```

2. Basic operations:
```sql
-- List tables
.tables

-- Show schema
.schema

-- Run query
SELECT * FROM auth_user;
```

## Tips and Best Practices

1. Always use transactions for multiple operations
2. Use parameterized queries to prevent SQL injection
3. Regular VACUUM to reclaim space
4. Use indexes wisely for better performance
5. Backup regularly
6. Use WAL mode for better concurrency
7. Be careful with ALTER TABLE as it's limited in SQLite

## Common Issues and Solutions

1. Database is locked:
```sql
PRAGMA busy_timeout = 5000;  -- Set timeout to 5 seconds
```

2. Slow queries:
```sql
-- Add index
CREATE INDEX idx_name ON table_name(column_name);

-- Analyze tables
ANALYZE;
```

3. Corrupted database:
```sql
PRAGMA integrity_check;
PRAGMA foreign_key_check;
```
