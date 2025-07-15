# bugfix/sql-driver

## Issue
SQL driver cannot be found, causing `runserver` to fail.

## Error message

```bash
Exception in thread django-main-thread:
Traceback (most recent call last):
  File "/home/codespace/.cache/pypoetry/virtualenvs/syafiqkaydotcom-1A_bNZBZ-py3.12/lib/python3.12/site-packages/django/db/backends/base/base.py", line 275, in ensure_connection
    self.connect()
  File "/home/codespace/.cache/pypoetry/virtualenvs/syafiqkaydotcom-1A_bNZBZ-py3.12/lib/python3.12/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/codespace/.cache/pypoetry/virtualenvs/syafiqkaydotcom-1A_bNZBZ-py3.12/lib/python3.12/site-packages/django/db/backends/base/base.py", line 256, in connect
    self.connection = self.get_new_connection(conn_params)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/codespace/.cache/pypoetry/virtualenvs/syafiqkaydotcom-1A_bNZBZ-py3.12/lib/python3.12/site-packages/mssql/base.py", line 368, in get_new_connection
    conn = Database.connect(connstr, **args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pyodbc.Error: ('01000', "[01000] [unixODBC][Driver Manager]Can't open lib 'ODBC Driver 18 for SQL Server' : file not found (0) (SQLDriverConnect)")
```

## Cause
The system does not have the `ODBC Driver 18 for SQL Server` installed or properly configured. This is a separate dependency from the `pyodbc` Python package.

## Actions Taken

1. Verified the Python package `pyodbc` is installed:
   ```bash
   $ pip install pyodbc
   Requirement already satisfied: pyodbc in /home/codespace/.cache/pypoetry/virtualenvs/syafiqkaydotcom-1A_bNZBZ-py3.12/lib/python3.12/site-packages (5.2.0)
   ```

2. Attempted to install the `ODBC Driver 18 for SQL Server` using the Microsoft repository:
   ```bash
   # Import the Microsoft GPG key
   curl https://packages.microsoft.com/keys/microsoft.asc -o microsoft.asc
   sudo mv microsoft.asc /usr/share/keyrings/microsoft-prod.gpg

   # Add the Microsoft repository
   sudo add-apt-repository "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/ubuntu/22.04/prod jammy main"

   # Update package lists
   sudo apt update

   # Install the ODBC Driver 18 for SQL Server
   sudo apt install -y msodbcsql18
   ```

3. Encountered the following error:
   ```bash
   W: GPG error: https://packages.microsoft.com/ubuntu/22.04/prod jammy InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY EB3E94ADBE1229CF
   E: The repository 'https://packages.microsoft.com/ubuntu/22.04/prod jammy InRelease' is not signed.
   N: Updating from such a repository can't be done securely, and is therefore disabled by default.
   ```

## Resolution Steps

1. **Manually Add the Repository**:
   Updated the repository configuration to reference the correct GPG key:
   ```bash
   curl https://packages.microsoft.com/keys/microsoft.asc -o microsoft.asc
   sudo mv microsoft.asc /usr/share/keyrings/microsoft-prod.gpg

   # Add the repository manually
   sudo nano /etc/apt/sources.list.d/microsoft-prod.list
   ```

   Added the following line:
   ```plaintext
   deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/ubuntu/22.04/prod jammy main
   ```

2. **Update Package Lists**:
   Ran the following command:
   ```bash
   sudo apt update
   ```

3. **Install the Driver**:
   Installed the driver:
   ```bash
   sudo apt install -y msodbcsql18
   ```

## Outcome
The driver was successfully installed, and the `runserver` command now works as expected.

```bash
$ python manage.py runserver
```

Run the following test for this bugfix:

```bash
python tests/test_odbc_driver.py
```
