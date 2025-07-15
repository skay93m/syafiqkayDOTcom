#!/usr/bin/env python
import os
import shutil
from datetime import datetime
from django.core.management import call_command
import subprocess
from pathlib import Path

def create_backup_directory():
    """Create backup directory with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(__file__).parent / 'backups' / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir

def backup_mssql(backup_dir):
    """Export Azure SQL Database to BACPAC using sqlpackage"""
    print("Backing up Azure SQL Database...")
    try:
        backup_file = backup_dir / 'azure_sql_backup.bacpac'
        # Using environment variables from Django settings
        server = os.environ.get('AZURE_SQL_DB_HOST', '').split('.')[0]  # Extract server name without domain
        db = os.environ.get('AZURE_SQL_DB_NAME')
        user = os.environ.get('AZURE_SQL_DB_USER')
        password = os.environ.get('AZURE_SQL_DB_PASSWORD')
        
        # Create connection string
        connection_string = f"Data Source={server}.database.windows.net;Initial Catalog={db};User Id={user};Password={password}"
        
        # Create export command using sqlpackage
        cmd = [
            'sqlpackage',
            '/a:Export',
            f'/ssn:{server}.database.windows.net',
            f'/sdn:{db}',
            f'/su:{user}',
            f'/sp:{password}',
            f'/tf:{backup_file}'
        ]
        
        subprocess.run(cmd, check=True)
        print(f"Azure SQL backup completed: {backup_file}")
    except Exception as e:
        print(f"Error backing up Azure SQL database: {e}")
        print("Make sure sqlpackage is installed. You can download it from: https://learn.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-download")

def backup_postgresql(backup_dir):
    """Backup PostgreSQL database using pg_dump"""
    print("Backing up PostgreSQL database...")
    try:
        backup_file = backup_dir / 'postgresql_backup.sql'
        # Using environment variables from Django settings
        db = os.environ.get('DB_NAME', 'mydatabase')
        user = os.environ.get('DB_USER', 'postgres')
        password = os.environ.get('DB_PASSWORD', 'mysecretpassword')
        host = os.environ.get('DB_HOST', 'localhost')
        port = os.environ.get('DB_PORT', '5432')
        
        # Set PGPASSWORD environment variable
        os.environ['PGPASSWORD'] = password
        
        cmd = [
            'pg_dump',
            '-h', host,
            '-p', port,
            '-U', user,
            '-F', 'c',  # Custom format
            '-b',  # Include large objects
            '-v',  # Verbose
            '-f', str(backup_file),
            db
        ]
        
        subprocess.run(cmd, check=True)
        print(f"PostgreSQL backup completed: {backup_file}")
    except Exception as e:
        print(f"Error backing up PostgreSQL database: {e}")
    finally:
        # Clear PGPASSWORD
        os.environ.pop('PGPASSWORD', None)

def backup_sqlite(backup_dir):
    """Backup SQLite database by copying the file"""
    print("Backing up SQLite database...")
    try:
        sqlite_path = Path(__file__).parent.parent / 'db.sqlite3'
        if sqlite_path.exists():
            backup_file = backup_dir / 'sqlite_backup.sqlite3'
            shutil.copy2(sqlite_path, backup_file)
            print(f"SQLite backup completed: {backup_file}")
        else:
            print("SQLite database file not found")
    except Exception as e:
        print(f"Error backing up SQLite database: {e}")

def backup_django_data(backup_dir):
    """Backup Django data using dumpdata"""
    print("Creating Django data dump...")
    try:
        backup_file = backup_dir / 'django_data.json'
        with open(backup_file, 'w') as f:
            call_command('dumpdata', '--indent', '2', '--exclude', 'contenttypes', '--exclude', 'auth.permission', stdout=f)
        print(f"Django data dump completed: {backup_file}")
    except Exception as e:
        print(f"Error creating Django data dump: {e}")

def main():
    """Main backup routine"""
    print("Starting database backup process...")
    backup_dir = create_backup_directory()
    
    # Backup all databases
    backup_mssql(backup_dir)
    backup_postgresql(backup_dir)
    backup_sqlite(backup_dir)
    backup_django_data(backup_dir)
    
    print(f"\nBackup process completed. Backup files are in: {backup_dir}")

if __name__ == "__main__":
    main()
