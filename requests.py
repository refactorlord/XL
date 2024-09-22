import sqlite3
from const import *

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

def get_table(file, name):
    try:
        connection = connect_db(file)
        cursor = connection.cursor()
        query = f"SELECT * FROM {name}"
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
    
def get_cell_value(file, name, i, j):
    table, (rows, columns) = get_table(file, name)
    if 0 <= i < rows and 0 <= j < columns:
        return table[i][j]
    else:
        raise IndexError("Индексы выходят за пределы таблицы")