import pyodbc

server = 'syafiq-kay-dotcom-dev1.database.windows.net'
database = 'syafiq-kay-doctcom-dev1'
username = 'django@syafiqsyafiqkay.onmicrosoft.com'
password = 'jompo0-wAxhiw-xyrkoq'
driver = 'ODBC Driver 18 for SQL Server'

conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Authentication=ActiveDirectoryPassword;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print('Connection successful!')
except Exception as e:
    print('Connection failed:', e)