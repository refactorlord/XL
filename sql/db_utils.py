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