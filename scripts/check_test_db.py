# check_test_db.py

import django
import os
import psycopg2
from django.db import connection
from django.core.management import call_command
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


# Ensure correct settings are loaded
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "syafiqkaydotcom.settings_test")
django.setup()

def check_db_connection():
    print("🔌 Checking database connectivity...")
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "mydatabase"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "mysecretpassword"),
            host="localhost",
            port=5432
        )
        conn.close()
        print("✅ PostgreSQL connection succeeded.")
    except Exception as e:
        print("❌ Connection failed:", str(e))

def list_unapplied_migrations():
    print("\n📦 Checking unapplied migrations...")
    from django.db.migrations.executor import MigrationExecutor

    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    plan = executor.migration_plan(targets)
    
    if not plan:
        print("🟢 All migrations are applied.")
    else:
        for app, migration in plan:
            print(f"🚧 Unapplied: {app.label} - {migration.name}")

def main():
    check_db_connection()
    list_unapplied_migrations()

if __name__ == "__main__":
    main()
