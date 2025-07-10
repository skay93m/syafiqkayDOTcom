# Database Manual: Working with MySQL (Azure) & Other SQL Providers

## Table of Contents
1. [Introduction](#introduction)
2. [Choosing a SQL Database Provider](#choosing-a-sql-database-provider)
3. [Provisioning MySQL on Azure](#provisioning-mysql-on-azure)
4. [Connecting to MySQL (Azure)](#connecting-to-mysql-azure)
5. [Common MySQL CLI Commands](#common-mysql-cli-commands)
6. [Database Management Best Practices](#database-management-best-practices)
7. [Working with Other SQL Providers](#working-with-other-sql-providers)
8. [Troubleshooting](#troubleshooting)
9. [Security & Maintenance](#security--maintenance)
10. [Useful Tools & Resources](#useful-tools--resources)

---

## 1. Introduction
This manual provides practical steps and best practices for working with MySQL databases hosted on Azure, as well as tips for other SQL database providers (PostgreSQL, SQL Server, etc.).

---

## 2. Choosing a SQL Database Provider
- **Azure Database for MySQL**: Managed, scalable, integrates with Azure ecosystem.
- **Azure Database for PostgreSQL**: Similar to MySQL, but for PostgreSQL.
- **Azure SQL Database**: Managed Microsoft SQL Server.
- **Amazon RDS / Google Cloud SQL**: Alternatives for AWS/GCP users.
- **Self-hosted**: For local development or on-premise needs.

---

## 3. Provisioning MySQL on Azure
### Using Azure Portal
1. Go to [Azure Portal](https://portal.azure.com/)
2. Search for "Azure Database for MySQL"
3. Click **Create** and fill in:
   - Resource Group
   - Server Name
   - Admin Username/Password
   - Location
   - Version (choose latest stable)
   - Pricing tier
4. Configure networking (allow access from your IP or Azure services)
5. Review and create

### Using Azure CLI
```bash
# Login to Azure
az login

# Create resource group
az group create --name myResourceGroup --location eastus

# Create MySQL server
az mysql server create \
  --resource-group myResourceGroup \
  --name mymysqlserver \
  --admin-user myadmin \
  --admin-password MyPassword123! \
  --sku-name B_Gen5_1 \
  --location eastus

# Configure firewall rule for your IP
az mysql server firewall-rule create \
  --resource-group myResourceGroup \
  --server mymysqlserver \
  --name AllowMyIP \
  --start-ip-address <your-ip> \
  --end-ip-address <your-ip>
```

---

## 4. Connecting to MySQL (Azure)
### Prerequisites
- Install MySQL client: `brew install mysql` (macOS), `apt install mysql-client` (Linux), or download from [MySQL Downloads](https://dev.mysql.com/downloads/).
- Get connection details from Azure Portal (host, username, password, database name, port).

### Connect via CLI
```bash
mysql -h <server-name>.mysql.database.azure.com \
  -u <admin-user>@<server-name> \
  -p
```

### Connect via Python (Django Example)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db',
        'USER': 'myadmin@mymysqlserver',
        'PASSWORD': 'MyPassword123!',
        'HOST': 'mymysqlserver.mysql.database.azure.com',
        'PORT': '3306',
        'OPTIONS': {
            'ssl': {'ca': '/path/to/BaltimoreCyberTrustRoot.crt.pem'}
        }
    }
}
```
- Download SSL CA cert from Azure Portal if required.

### Connect via DBeaver or MySQL Workbench
- Use the same host, user, password, and port as above.
- For SSL, import the CA certificate if prompted.

---

## 5. Common MySQL CLI Commands
```bash
# List databases
SHOW DATABASES;

# Create database
CREATE DATABASE mydb;

# Use database
USE mydb;

# List tables
SHOW TABLES;

# Describe table
DESCRIBE mytable;

# Run SQL script
mysql -h ... -u ... -p < script.sql

# Export database
mysqldump -h ... -u ... -p mydb > mydb_backup.sql

# Import database
mysql -h ... -u ... -p mydb < mydb_backup.sql
```

---

## 6. Database Management Best Practices
- Use strong, unique passwords for DB users
- Restrict network access (firewall, VNet, private endpoints)
- Enable SSL for all connections
- Regularly back up your database
- Use least-privilege principle for DB accounts
- Monitor performance and set up alerts
- Use parameter groups for tuning
- Automate schema migrations (e.g., Django migrations, Alembic for SQLAlchemy)

---

## 7. Working with Other SQL Providers
### PostgreSQL (Azure)
- Use `az postgres server create` and similar commands
- Connection string: `psql -h <server>.postgres.database.azure.com -U <user>@<server> -d <db>`
- Django ENGINE: `'django.db.backends.postgresql'`

### Azure SQL Database
- Use `az sql server create` and `az sql db create`
- Connect with `sqlcmd` or SQL Server Management Studio
- Django ENGINE: `'mssql'` (with `django-mssql-backend`)

### Amazon RDS / Google Cloud SQL
- Use provider-specific CLI or console
- Connection details and best practices are similar

---

## 8. Troubleshooting
### Common Issues
- **Cannot connect:** Check firewall, username format, SSL, and IP whitelisting
- **Timeouts:** Check network latency, DB performance, and connection pool settings
- **Authentication errors:** Double-check username (`user@server`), password, and permissions
- **SSL errors:** Ensure CA cert is correct and required by server
- **Migration issues:** Check Django settings, run `python manage.py migrate`, and review migration files

### Diagnostic Commands
```bash
# Test port connectivity
nc -vz <host> 3306

# Check MySQL server status
systemctl status mysql  # (self-hosted)

# View Azure server metrics
az monitor metrics list --resource <server-resource-id>
```

---

## 9. Security & Maintenance
- Enable automatic backups and geo-redundancy
- Rotate passwords and credentials regularly
- Use managed identities or Azure Key Vault for secrets
- Apply security updates and patches
- Monitor audit logs for suspicious activity
- Set up alerts for failed logins and high resource usage

---

## 10. Useful Tools & Resources
- [Azure CLI Documentation](https://docs.microsoft.com/en-us/cli/azure/mysql)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [DBeaver](https://dbeaver.io/) (cross-platform DB client)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)
- [Azure Database for MySQL](https://docs.microsoft.com/en-us/azure/mysql/)
- [Django Database Settings](https://docs.djangoproject.com/en/stable/ref/settings/#databases)
- [SSL for Azure MySQL](https://docs.microsoft.com/en-us/azure/mysql/howto-configure-ssl)

---

*This manual is a living document. Update as your database architecture evolves or as you try new providers.*
