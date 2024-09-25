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
    try:
        connection = connect_db(file)
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        select_clause = ", ".join([f"CAST({col[1]} AS TEXT) AS {col[1]}_text" for col in columns])
        cursor.execute(f"SELECT {select_clause} FROM {table_name};")
        table = cursor.fetchall()
        num_rows = len(table)
        num_columns = len(columns)
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
    try:
        connection = connect_db(file)
        cursor = connection.cursor()
        query = """SELECT 
                    e.kod, e.name, e.region, e.city, e.grnti, g.rubrika, r.oblname
                FROM 
                    Experts e
                JOIN 
                    Reg_Obl_City r ON e.region = r.region AND e.city = r.city
                LEFT JOIN 
                    grntirub g 
                ?????????? """
        cursor.execute(query)
        table = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        table.insert(0, columns)
        cursor.close()
        connection.close()
        num_rows = len(table)
        num_columns = len(columns)
        return table, (num_rows, num_columns)
    except sqlite3.Error as ex:
        print(f"Ошибка при работе с базой данных: {ex}")
        return None, (0, 0)