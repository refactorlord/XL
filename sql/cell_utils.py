from sql.get_utils import *

def get_cell_value(file, name, i, j):
    table = get_table(file, name)
    rows = get_rows_in_table(file, name)
    cols = get_columns_in_table(file, name)
    if 0 <= i < rows and 0 <= j < cols:
        return table[i][j]
    else:
        raise IndexError("Индексы выходят за пределы таблицы")
    
def set_cell_value(file, table_name, row_number, column, value):
    """
    Sets a cell value in the SQLite table by row number.

    :param file: Path to the database file.
    :param table_name: Table name.
    :param row_number: Row number (starts from 1).
    :param column: Column name.
    :param value: New cell value.
    """
    try:
        # Connect to the database
        connection = connect_db(file)
        cursor = connection.cursor()

        # Construct the SQL query using ROWID
        query = f"UPDATE \"{table_name}\" SET \"{column}\" = ? WHERE ROWID = ?"
        
        # Execute the query
        cursor.execute(query, (value, row_number))
        
        # Save changes
        connection.commit()
        print("Value updated successfully!")
        
    except sqlite3.Error as e:
        print(f"Error while working with SQLite: {e}")
        
    finally:
        if connection:
            connection.close()
