import sqlite3

def connect_db(file):
    return sqlite3.connect(file)

def list_tables(file):
    try:
        connection = connect_db(file)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        cursor.close()
        connection.close()
        return [table[0] for table in tables]
    except sqlite3.Error as ex:
            print(f"Ошибка при работе с базой данных: {ex}")
            return []
    
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
        select_clause = ", ".join([f"CAST({col[1]} AS TEXT) AS {col[1]}_text" for col in columns])

        # Execute the query and fetch the result
        cursor.execute(f"SELECT {select_clause} FROM {table_name};")
        table = cursor.fetchall()

        # Add the column names as the first row of the table
        num_rows = len(table)
        num_columns = len(columns)
        table.insert(0, [col[1] + "_text" for col in columns])
        connection.close()
        return table, (num_rows, num_columns)
    except sqlite3.Error as ex:
        print(f"Error while working with the database: {ex}")
        return None, (0, 0)
    
def get_cell_value(file, name, i, j):
    table, (rows, columns) = get_table(file, name)
    if 0 <= i < rows and 0 <= j < columns:
        return table[i][j]
    else:
        raise IndexError("Индексы выходят за пределы таблицы")
    
def get_merged_table(file):
    """
    Returns a merged table of Experts and Reg_Obl_City tables and grntirub table filtered by the first two characters of the grnti field.

    Args:
        file (str): path to the SQLite database file

    Returns:
        tuple: merged table and its shape
    """
    try:
        connection = connect_db(file)
        cursor = connection.cursor()
        # Select all columns from Experts, Reg_Obl_City and grntirub tables
        # by joining tables on the region and city fields
        # and filtering grntirub table by the first two characters of the grnti field
        query = """
            SELECT 
                kod, name, region, city, grnti, rubrika, obl_name
            FROM 
                Experts
            JOIN 
                Reg_Obl_City ON Experts.region = Reg_Obl_City.region AND Experts.city = Reg_Obl_City.city
            LEFT JOIN 
                grntirub ON SUBSTR(Experts.grnti, 1, 2) = SUBSTR(grntirub.grnti, 1, 2)
        """
        cursor.execute(query)

        # Get the column names from the cursor description
        merged_table = [description[0] for description in cursor.description]

        # Fetch all rows and add them to the merged table
        merged_table.extend(cursor.fetchall())

        cursor.close()
        connection.close()

        return merged_table, (len(merged_table) - 1, len(merged_table[0]))
    except sqlite3.Error as ex:
        print(f"Error while working with the database: {ex}")
        return None, (0, 0)
