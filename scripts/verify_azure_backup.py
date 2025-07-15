#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path
import platform

def check_sqlpackage():
    """Check if sqlpackage is installed and accessible"""
    print("\nChecking sqlpackage installation...")
    try:
        result = subprocess.run(['sqlpackage', '--version'], 
                              capture_output=True, 
                              text=True)
        print(f"✅ sqlpackage is installed (version: {result.stdout.strip()})")
        return True
    except FileNotFoundError:
        print("❌ sqlpackage is not installed or not in PATH")
        print("\nInstallation instructions:")
        os_type = platform.system().lower()
        if os_type == 'darwin':  # macOS
            print("""
    Install using Homebrew:
    brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
    brew install msodbcsql18 mssql-tools18 sqlpackage
            """)
        elif os_type == 'linux':
            print("""
    Install using curl:
    curl -o sqlpackage.zip https://aka.ms/sqlpackage-linux
    mkdir -p /opt/sqlpackage
    unzip sqlpackage.zip -d /opt/sqlpackage
    chmod +x /opt/sqlpackage/sqlpackage
    export PATH=$PATH:/opt/sqlpackage
            """)
        else:  # Windows
            print("""
    Download from Microsoft's website:
    https://learn.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-download
            """)
        return False

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("\nChecking environment variables...")
    required_vars = {
        'AZURE_SQL_DB_HOST': 'Azure SQL Server hostname',
        'AZURE_SQL_DB_NAME': 'Database name',
        'AZURE_SQL_DB_USER': 'Username',
        'AZURE_SQL_DB_PASSWORD': 'Password'
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            masked_value = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '****'
            print(f"✅ {var} is set ({masked_value})")
        else:
            print(f"❌ {var} is not set ({description} required)")
            all_set = False
    
    return all_set

def test_database_connection():
    """Test connection to Azure SQL Database"""
    print("\nTesting database connection...")
    
    host = os.environ.get('AZURE_SQL_DB_HOST')
    db = os.environ.get('AZURE_SQL_DB_NAME')
    user = os.environ.get('AZURE_SQL_DB_USER')
    password = os.environ.get('AZURE_SQL_DB_PASSWORD')
    
    if not all([host, db, user, password]):
        print("❌ Cannot test connection: environment variables not set")
        return False
    
    try:
        server = host.split('.')[0]  # Extract server name without domain
        connection_string = f"Data Source={server}.database.windows.net;Initial Catalog={db};User Id={user};Password={password}"
        
        # Use sqlcmd to test connection
        cmd = [
            'sqlcmd',
            '-S', f"{server}.database.windows.net",
            '-d', db,
            '-U', user,
            '-P', password,
            '-Q', "SELECT @@VERSION"
        ]
        
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Successfully connected to Azure SQL Database")
            print(f"\nSQL Server version:\n{result.stdout.strip()}")
            return True
        else:
            print("❌ Failed to connect to Azure SQL Database")
            print(f"\nError:\n{result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {str(e)}")
        return False

def check_backup_permissions():
    """Check if we have necessary permissions for backup"""
    print("\nChecking database permissions...")
    
    host = os.environ.get('AZURE_SQL_DB_HOST')
    db = os.environ.get('AZURE_SQL_DB_NAME')
    user = os.environ.get('AZURE_SQL_DB_USER')
    password = os.environ.get('AZURE_SQL_DB_PASSWORD')
    
    if not all([host, db, user, password]):
        print("❌ Cannot check permissions: environment variables not set")
        return False
    
    try:
        server = host.split('.')[0]
        # Check if user has necessary permissions
        cmd = [
            'sqlcmd',
            '-S', f"{server}.database.windows.net",
            '-d', db,
            '-U', user,
            '-P', password,
            '-Q', """
                SELECT r.name AS role_name
                FROM sys.database_role_members rm
                JOIN sys.database_principals r ON rm.role_principal_id = r.principal_id
                JOIN sys.database_principals m ON rm.member_principal_id = m.principal_id
                WHERE m.name = CURRENT_USER;
            """
        ]
        
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Successfully checked database permissions")
            print("\nYour roles:")
            print(result.stdout.strip())
            return True
        else:
            print("❌ Failed to check database permissions")
            print(f"\nError:\n{result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking permissions: {str(e)}")
        return False

def check_disk_space():
    """Check if there's enough disk space for backups"""
    print("\nChecking available disk space...")
    
    backup_dir = Path(__file__).parent / 'backups'
    try:
        total, used, free = shutil.disk_usage(backup_dir)
        free_gb = free // (2**30)  # Convert to GB
        
        if free_gb > 5:  # Assuming we need at least 5GB
            print(f"✅ Sufficient disk space available ({free_gb}GB free)")
            return True
        else:
            print(f"⚠️ Low disk space warning (only {free_gb}GB free)")
            return False
    except Exception as e:
        print(f"❌ Error checking disk space: {str(e)}")
        return False

def main():
    """Main verification routine"""
    print("=== Azure SQL Database Backup Verification ===")
    
    results = []
    results.append(("SQLPackage Installation", check_sqlpackage()))
    results.append(("Environment Variables", check_environment_variables()))
    results.append(("Database Connection", test_database_connection()))
    results.append(("Database Permissions", check_backup_permissions()))
    
    print("\n=== Summary ===")
    all_passed = True
    for check, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check}")
        all_passed = all_passed and passed
    
    if all_passed:
        print("\n✅ All checks passed! You can now run the backup scripts.")
    else:
        print("\n❌ Some checks failed. Please fix the issues above before running backups.")
        sys.exit(1)

if __name__ == "__main__":
    main()
