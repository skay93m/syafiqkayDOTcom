#!/usr/bin/env python
import os
import shutil
import subprocess
from pathlib import Path
from django.core.management import call_command
import argparse
from datetime import datetime

def get_latest_backup_dir():
    """Get the most recent backup directory"""
    backup_base = Path(__file__).parent / 'backups'
    if not backup_base.exists():
        raise FileNotFoundError("No backups directory found")
    
    backup_dirs = [d for d in backup_base.iterdir() if d.is_dir()]
    if not backup_dirs:
        raise FileNotFoundError("No backup directories found")
    
    return max(backup_dirs, key=lambda x: datetime.strptime(x.name, '%Y%m%d_%H%M%S'))

def restore_mssql(backup_dir):
    """Restore Azure SQL Database from BACPAC using sqlpackage"""
    print("Restoring Azure SQL Database...")
    try:
        backup_file = backup_dir / 'azure_sql_backup.bacpac'
        if not backup_file.exists():
            print("Azure SQL backup file (BACPAC) not found")
            return

        # Using environment variables from Django settings
        server = os.environ.get('AZURE_SQL_DB_HOST', '').split('.')[0]  # Extract server name without domain
        db = os.environ.get('AZURE_SQL_DB_NAME')
        user = os.environ.get('AZURE_SQL_DB_USER')
        password = os.environ.get('AZURE_SQL_DB_PASSWORD')

        # Create import command using sqlpackage
        cmd = [
            'sqlpackage',
            '/a:Import',
            f'/tsn:{server}.database.windows.net',
            f'/tdn:{db}',
            f'/tu:{user}',
            f'/tp:{password}',
            f'/sf:{backup_file}'
        ]

        subprocess.run(cmd, check=True)
        print(f"Azure SQL restore completed from: {backup_file}")
    except Exception as e:
        print(f"Error restoring Azure SQL database: {e}")
        print("Make sure sqlpackage is installed. You can download it from: https://learn.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-download")

def restore_postgresql(backup_dir):
    """Restore PostgreSQL database"""
    print("Restoring PostgreSQL database...")
    try:
        backup_file = backup_dir / 'postgresql_backup.sql'
        if not backup_file.exists():
            print("PostgreSQL backup file not found")
            return

        # Using environment variables from Django settings
        db = os.environ.get('DB_NAME', 'mydatabase')
        user = os.environ.get('DB_USER', 'postgres')
        password = os.environ.get('DB_PASSWORD', 'mysecretpassword')
        host = os.environ.get('DB_HOST', 'localhost')
        port = os.environ.get('DB_PORT', '5432')

        # Set PGPASSWORD environment variable
        os.environ['PGPASSWORD'] = password

        # Drop existing connections
        disconnect_cmd = [
            'psql',
            '-h', host,
            '-p', port,
            '-U', user,
            '-d', 'postgres',
            '-c', f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{db}' AND pid <> pg_backend_pid();"
        ]
        
        # Drop and recreate database
        drop_cmd = [
            'psql',
            '-h', host,
            '-p', port,
            '-U', user,
            '-d', 'postgres',
            '-c', f"DROP DATABASE IF EXISTS {db}; CREATE DATABASE {db};"
        ]

        # Restore command
        restore_cmd = [
            'pg_restore',
            '-h', host,
            '-p', port,
            '-U', user,
            '-d', db,
            '-v',
            str(backup_file)
        ]

        subprocess.run(disconnect_cmd, check=True)
        subprocess.run(drop_cmd, check=True)
        subprocess.run(restore_cmd, check=True)
        print(f"PostgreSQL restore completed from: {backup_file}")
    except Exception as e:
        print(f"Error restoring PostgreSQL database: {e}")
    finally:
        # Clear PGPASSWORD
        os.environ.pop('PGPASSWORD', None)

def restore_sqlite(backup_dir):
    """Restore SQLite database"""
    print("Restoring SQLite database...")
    try:
        backup_file = backup_dir / 'sqlite_backup.sqlite3'
        if not backup_file.exists():
            print("SQLite backup file not found")
            return

        target_path = Path(__file__).parent.parent / 'db.sqlite3'
        shutil.copy2(backup_file, target_path)
        print(f"SQLite restore completed from: {backup_file}")
    except Exception as e:
        print(f"Error restoring SQLite database: {e}")

def restore_django_data(backup_dir):
    """Restore Django data"""
    print("Restoring Django data...")
    try:
        backup_file = backup_dir / 'django_data.json'
        if not backup_file.exists():
            print("Django data backup file not found")
            return

        call_command('loaddata', str(backup_file))
        print(f"Django data restore completed from: {backup_file}")
    except Exception as e:
        print(f"Error restoring Django data: {e}")

def main():
    """Main restore routine"""
    parser = argparse.ArgumentParser(description='Restore databases from backup')
    parser.add_argument('--backup-dir', type=str, help='Specific backup directory to restore from (format: YYYYMMDD_HHMMSS)')
    args = parser.parse_args()

    try:
        if args.backup_dir:
            backup_dir = Path(__file__).parent / 'backups' / args.backup_dir
            if not backup_dir.exists():
                raise FileNotFoundError(f"Backup directory not found: {args.backup_dir}")
        else:
            backup_dir = get_latest_backup_dir()
            print(f"Using most recent backup from: {backup_dir.name}")

        # Restore all databases
        restore_mssql(backup_dir)
        restore_postgresql(backup_dir)
        restore_sqlite(backup_dir)
        restore_django_data(backup_dir)

        print("\nRestore process completed successfully!")
    except Exception as e:
        print(f"Error during restore process: {e}")

if __name__ == "__main__":
    main()
