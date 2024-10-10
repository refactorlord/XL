from sql.get_utils import connect_db, get_rows_count_in_table

def add_row_to_table(file: str, table_name: str, data: list) -> None:
    """
    Adds a row to the specified table in the SQLite database file.

    Args:
        file (str): path to the SQLite database file
        table_name (str): name of the table
        data (list): data to be inserted, length must match the number of columns in the table
    """
    try:
        connection = connect_db(file)
        cursor = connection.cursor()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        column_names = [column[1] for column in cursor.fetchall()]
        
        # Form and execute the query
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['?'] * len(column_names))})"
        cursor.execute(query, data)
        
        connection.commit()
        print("Data added successfully!")  # Debug message
    except Exception as ex:
        print(f"Error adding data: {ex}")
    finally:
        connection.close()

def delete_row_by_number(file: str, table_name: str, row_number: int) -> None:
    """
    Deletes a row by its number from the specified table in the SQLite database file.

    Args:
        file (str): path to the SQLite database file
        table_name (str): name of the table
        row_number (int): number of the row to be deleted

    Returns:
        None
    """
    try:
        # Connect to the SQLite database
        connection = connect_db(file)
        cursor = connection.cursor()

        # Get the total number of rows in the table
        total_rows = get_rows_count_in_table(file, table_name)

        # Check if the row number is valid
        if row_number < 1 or row_number > total_rows:
            raise ValueError("Invalid row number")

        # If the row number is the last row, delete it using a different approach
        if row_number == total_rows:
            cursor.execute(f"DELETE FROM {table_name} WHERE rowid = (SELECT MAX(rowid) FROM {table_name})")
        else:
            # Delete the row by its number (note: SQLite uses 1-based indexing)
            cursor.execute(f"DELETE FROM {table_name} WHERE rowid = ?", (row_number,))

        # Commit the changes
        connection.commit()

        # Close the connection
        connection.close()
    except Exception as ex:
        print(f"Error while deleting {row_number} row from database: {ex}")

def delete_row_by_code(file: str, table_name: str, kod: str) -> None:
    """
    Deletes a row by its code from the specified table in the SQLite database file.

    Args:
        file (str): path to the SQLite database file
        table_name (str): name of the table
        code (str): code of the row to be deleted

    Returns:
        None
    """
    try:
        # Connect to the SQLite database
        connection = connect_db(file)
        cursor = connection.cursor()

        # Check if the code exists in the table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE kod = ?", (kod,))
        exists = cursor.fetchone()[0]

        if exists == 0:
            raise ValueError("kod not found in the table")

        # Delete the row by its code
        cursor.execute(f"DELETE FROM {table_name} WHERE kod = ?", (kod,))

        # Commit the changes
        connection.commit()

        # Close the connection
        connection.close()
    except Exception as ex:
        print(f"Error while deleting row with code {kod} from database: {ex}")