import pyodbc

def test_odbc_driver():
    try:
        # Attempt to list available ODBC drivers
        drivers = pyodbc.drivers()
        assert "ODBC Driver 18 for SQL Server" in drivers, "ODBC Driver 18 for SQL Server is not installed."
        print("ODBC Driver 18 for SQL Server is installed and available.")
    except Exception as e:
        print(f"Test failed: {e}")
        assert False, "An error occurred while checking ODBC drivers."

if __name__ == "__main__":
    test_odbc_driver()