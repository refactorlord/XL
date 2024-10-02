import sqlite3
from sql.db_utils import connect_db

def get_table(file, table_name):
    """
    Returns the table with the given name from the SQLite database file.

    Args:
        file (str): path to the SQLite database file
        table_name (str): name of the table

    Returns:
        tuple: table and its shape (number of rows, number of columns)
    """
    try:
        connection = connect_db(file)
        cursor = connection.cursor()
        # Get the column names and types of the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Construct the SELECT clause to convert all columns to text
        select_clause = ", ".join([f"CAST({col[1]} AS TEXT) AS {col[1]}" for col in columns])

        # Execute the query and fetch the result
        cursor.execute(f"SELECT {select_clause} FROM {table_name};")
        table = cursor.fetchall()

        # Add the column names as the first row of the table
        table.insert(0, [col[1] for col in columns])
        connection.close()
        return table
    except sqlite3.Error as ex:
        print(f"Error while working with the database: {ex}")
        return None

def get_rows_in_table(file: str, table_name: str) -> int:
    """
    Returns the number of rows in the specified table in the SQLite database file.


    Args:
        file (str): path to the SQLite database file
        table_name (str): name of the table

    Returns:
        int: number of rows in the table
    """
    connection = connect_db(file)
    cursor = connection.cursor()

    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)

    rows = cursor.fetchone()[0]
    connection.close()

    return rows


def get_columns_in_table(file: str, table_name: str) -> int:
    """
    Returns the number of columns in the specified table in the SQLite database file.


    Args:
        file (str): path to the SQLite database file
        table_name (str): name of the table

    Returns:
        int: number of columns in the table
    """
    connection = connect_db(file)
    cursor = connection.cursor()

    query = f"PRAGMA table_info({table_name})"
    cursor.execute(query)

    columns = len(cursor.fetchall())
    connection.close()

    return columns