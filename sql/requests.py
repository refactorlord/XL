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
        select_clause = ", ".join([f"CAST({col[1]} AS TEXT) AS {col[1]}" for col in columns])

        # Execute the query and fetch the result
        cursor.execute(f"SELECT {select_clause} FROM {table_name};")
        table = cursor.fetchall()

        # Add the column names as the first row of the table
        num_rows = len(table)
        num_columns = len(columns)
        table.insert(0, [col[1] for col in columns])
        connection.close()
        return table, (num_rows, num_columns)
    except sqlite3.Error as ex:
        print(f"Error while working with the database: {ex}")
        return None, (0, 0)

def add_row_to_table(file: str, table_name: str, data: list) -> None:
    """
    Adds a row to the specified table in the SQLite database file.

    Args:
        file (str): path to the SQLite database file
        table_name (str): name of the table
        data (list): data to be inserted, length must match the number of columns in the table
    """
    connection = connect_db(file)
    cursor = connection.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    column_names = [column[1] for column in cursor.fetchall()]

    query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['?'] * len(column_names))})"

    cursor.execute(query, data)

    connection.commit()
    connection.close()

def get_cell_value(file, name, i, j):
    table, (rows, columns) = get_table(file, name)
    if 0 <= i < rows and 0 <= j < columns:
        return table[i][j]
    else:
        raise IndexError("Индексы выходят за пределы таблицы")
    
def get_merged_table(file):
    """
    Returns a merged table of Experts and Reg_obl_city tables and grntirub table filtered by the first two characters of the grnti field.

    Args:
        file (str): path to the SQLite database file

    Returns:
        tuple: merged table and its shape
    """
    try:
        connection = connect_db(file)
        cursor = connection.cursor()
        # Get the column names and types of the table
        cursor.execute("PRAGMA table_info(Experts);")
        columns_experts = cursor.fetchall()
        cursor.execute("PRAGMA table_info(Reg_obl_city);")
        columns_regions = cursor.fetchall()
        cursor.execute("PRAGMA table_info(grntirub);")
        columns_grntirub = cursor.fetchall()

        # Check if the list of columns is not empty
        if not columns_experts or not columns_regions or not columns_grntirub:
            raise IndexError("The table does not exist")

        # Construct the SELECT clause to convert all columns to text
        select_clause = ", ".join([f"CAST(Experts.{col[1]} AS TEXT) AS {col[1]}" for col in columns_experts] +
                                  [f"CAST(Reg_obl_city.oblname AS TEXT) AS oblname"] +
                                  [f"CAST(grntirub.{col[1]} AS TEXT) AS grntirub_{col[1]}" for col in columns_grntirub])

        # Select all columns from Experts, Reg_obl_city and grntirub tables
        # by joining tables on the region and city fields
        # and filtering grntirub table by the first two characters of the grnti field
        query = f"""
                SELECT {select_clause}
            FROM 
                Experts
            INNER JOIN 
                Reg_obl_city 
                ON Experts.region = Reg_obl_city.region
                AND Experts.city = Reg_obl_city.city
            LEFT JOIN 
                grntirub 
                ON COALESCE(
                    SUBSTR(Experts.grnti, 1, INSTR(Experts.grnti, '.') - 1),
                    SUBSTR(Experts.grnti, 1, INSTR(Experts.grnti, ';') - 1)
                ) = grntirub.codrub
            WHERE
                Experts.grnti IS NOT NULL
        """

        # Execute the query and fetch all rows
        cursor.execute(query)
        merged_table = cursor.fetchall()

        # Add the column names as the first row of the merged table
        if merged_table:
            merged_table.insert(0, [col[1] for col in columns_experts] + ["oblname"] + [f"grntirub_{col[1]}" for col in columns_grntirub])

        cursor.close()
        connection.close()

        return merged_table, (len(merged_table) - 1, len(merged_table[0])) if merged_table else (None, (0, 0))
    except sqlite3.Error as ex:
        print(f"Error while working with the database: {ex}")
        return None, (0, 0)
    except IndexError as ex:
        print(f"Error while working with the database: {ex}")
        return None, (0, 0)
    
def get_combined_table(file, table_name, merge):
    if merge:
        return get_merged_table(file)
    else:
        return get_table(file, table_name)