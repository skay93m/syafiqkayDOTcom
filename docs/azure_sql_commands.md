# Azure SQL Database Commands for Django dbshell

This guide provides common SQL commands you can use with Azure SQL Database through Django's `manage.py dbshell`.

## Basic Database Information

```sql
-- Show database version
SELECT @@VERSION;

-- Show current database
SELECT DB_NAME();

-- List all databases
SELECT name FROM sys.databases;

-- Show all tables in current database
SELECT TABLE_SCHEMA, TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE';

-- Show table details
SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'your_table_name';
```

## Database Size and Space

```sql
-- Check database size
SELECT 
    DB_NAME() AS DatabaseName,
    CAST(SUM(CAST(FILEPROPERTY(name, 'SpaceUsed') AS bigint) * 8. / 1024) AS DECIMAL(8,2)) AS SpaceUsedMB,
    CAST(SUM(size) * 8. / 1024 AS DECIMAL(8,2)) AS SpaceAllocatedMB
FROM sys.database_files
GROUP BY type_desc;

-- Table sizes
SELECT 
    t.NAME AS TableName,
    s.Name AS SchemaName,
    p.rows AS RowCounts,
    CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS TotalSpaceMB
FROM sys.tables t
INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
LEFT OUTER JOIN sys.schemas s ON t.schema_id = s.schema_id
GROUP BY t.Name, s.Name, p.Rows
ORDER BY TotalSpaceMB DESC;
```

## Performance Monitoring

```sql
-- Active connections
SELECT 
    DB_NAME(dbid) as DBName, 
    COUNT(dbid) as NumberOfConnections,
    loginame as LoginName
FROM sys.sysprocesses
WHERE dbid > 0
GROUP BY dbid, loginame;

-- Current executing queries
SELECT 
    r.session_id,
    r.status,
    r.wait_type,
    r.wait_time,
    SUBSTRING(t.text, (r.statement_start_offset/2)+1,
        ((CASE r.statement_end_offset
            WHEN -1 THEN DATALENGTH(t.text)
            ELSE r.statement_end_offset
        END - r.statement_start_offset)/2) + 1) AS executing_statement,
    r.cpu_time,
    r.total_elapsed_time
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t;

-- Index usage stats
SELECT 
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    ius.user_seeks,
    ius.user_scans,
    ius.user_lookups,
    ius.user_updates
FROM sys.dm_db_index_usage_stats ius
INNER JOIN sys.indexes i ON ius.object_id = i.object_id
    AND ius.index_id = i.index_id
WHERE database_id = DB_ID();
```

## Security and Users

```sql
-- List users
SELECT name, create_date, modify_date, type_desc 
FROM sys.database_principals 
WHERE type_desc != 'SYSTEM_USER';

-- List user permissions
SELECT 
    dp.NAME AS principal_name,
    dp.type_desc AS principal_type,
    o.NAME AS object_name,
    p.permission_name,
    p.state_desc AS permission_state
FROM sys.database_permissions p
JOIN sys.objects o ON p.major_id = o.object_id
JOIN sys.database_principals dp ON p.grantee_principal_id = dp.principal_id;

-- List role members
SELECT 
    r.name AS role_name,
    m.name AS member_name
FROM sys.database_role_members rm
JOIN sys.database_principals r ON rm.role_principal_id = r.principal_id
JOIN sys.database_principals m ON rm.member_principal_id = m.principal_id;
```

## Table Management

```sql
-- Create new table
CREATE TABLE example_table (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    created_at DATETIME DEFAULT GETDATE()
);

-- Add column
ALTER TABLE table_name
ADD column_name data_type;

-- Modify column
ALTER TABLE table_name
ALTER COLUMN column_name new_data_type;

-- Drop column
ALTER TABLE table_name
DROP COLUMN column_name;

-- Truncate table
TRUNCATE TABLE table_name;
```

## Data Management

```sql
-- Insert data
INSERT INTO table_name (column1, column2)
VALUES ('value1', 'value2');

-- Bulk update
UPDATE table_name
SET column1 = value1
WHERE condition;

-- Delete data
DELETE FROM table_name
WHERE condition;

-- Merge data (upsert)
MERGE target_table AS target
USING source_table AS source
ON target.id = source.id
WHEN MATCHED THEN
    UPDATE SET target.column1 = source.column1
WHEN NOT MATCHED THEN
    INSERT (column1) VALUES (source.column1);
```

## Maintenance

```sql
-- Rebuild indexes
ALTER INDEX ALL ON table_name REBUILD;

-- Update statistics
UPDATE STATISTICS table_name;

-- Kill specific session
KILL session_id;
```

## Backup and Restore
Note: In Azure SQL Database, traditional BACKUP/RESTORE commands are not supported. Here are the alternative methods:

### Using Azure CLI
```bash
# Export database to .bacpac file
az sql db export -s <server-name> -n <database-name> -g <resource-group-name> \
    -u <username> -p <password> \
    --storage-key <storage-access-key> \
    --storage-key-type StorageAccessKey \
    --storage-uri https://<storage-account>.blob.core.windows.net/<container>/<file>.bacpac

# Import database from .bacpac file
az sql db import -s <server-name> -n <database-name> -g <resource-group-name> \
    -u <username> -p <password> \
    --storage-key <storage-access-key> \
    --storage-key-type StorageAccessKey \
    --storage-uri https://<storage-account>.blob.core.windows.net/<container>/<file>.bacpac
```

### Using sqlpackage
```bash
# Export database to .bacpac
sqlpackage /action:Export \
    /sourcedatabasename:<database> \
    /sourceservername:<server>.database.windows.net \
    /sourceuser:<username> \
    /sourcepassword:<password> \
    /targetfile:<path_to_bacpac>

# Import database from .bacpac
sqlpackage /action:Import \
    /targetdatabasename:<database> \
    /targetservername:<server>.database.windows.net \
    /targetuser:<username> \
    /targetpassword:<password> \
    /sourcefile:<path_to_bacpac>
```

### Using PowerShell
```powershell
# Export database
$exportRequest = New-AzSqlDatabaseExport `
    -ResourceGroupName "<resource-group>" `
    -ServerName "<server>" `
    -DatabaseName "<database>" `
    -StorageKeyType "StorageAccessKey" `
    -StorageKey "<storage-access-key>" `
    -StorageUri "https://<storage-account>.blob.core.windows.net/<container>/<file>.bacpac" `
    -AdministratorLogin "<username>" `
    -AdministratorLoginPassword (ConvertTo-SecureString "<password>" -AsPlainText -Force)

# Import database
$importRequest = New-AzSqlDatabaseImport `
    -ResourceGroupName "<resource-group>" `
    -ServerName "<server>" `
    -DatabaseName "<database>" `
    -StorageKeyType "StorageAccessKey" `
    -StorageKey "<storage-access-key>" `
    -StorageUri "https://<storage-account>.blob.core.windows.net/<container>/<file>.bacpac" `
    -AdministratorLogin "<username>" `
    -AdministratorLoginPassword (ConvertTo-SecureString "<password>" -AsPlainText -Force)
```

### Check Backup Status
```sql
-- Check last backup time
SELECT TOP 1
    database_name,
    backup_start_date,
    backup_finish_date,
    backup_type
FROM msdb.dbo.backupset
ORDER BY backup_start_date DESC;

-- Check long-term backup retention policy
SELECT 
    name AS [Database Name],
    recovery_model_desc AS [Recovery Model],
    has_database_backups AS [Has Backups]
FROM sys.databases
WHERE name = DB_NAME();
```

Remember:
- Azure SQL Database is automatically backed up by Azure
- Full backups are created weekly
- Differential backups are created every 12 hours
- Transaction log backups are created every 5-10 minutes
- Retention period depends on your service tier
- Use Azure Portal to configure long-term retention policies
````
