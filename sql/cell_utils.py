from sql.get_utils import *

def get_cell_value(file: str, table_name: str, row_number: int, column_name: str):
    """
    Gets a cell value from the SQLite table by row number and column name.

    :param file: Path to the database file.
    :param table_name: Table name.
    :param row_number: Row number (starts from 1).
    :param column_name: Column name.
    :return: Value of the cell.
    """
    try:
        # Connect to the database
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        code_column = "kod" * (table_name == "Experts" or table_name == "Reg_obl_city") + "codrub" * (table_name == "grntirub")
        #print("asdasdasdasdasd: ", code_column)
        # Construct the SQL query to get the cell value
        query = f"SELECT \"{column_name}\" FROM \"{table_name}\" WHERE {code_column} = ?"
        
        # Execute the query
        cursor.execute(query, (row_number,))
        result = cursor.fetchone()
        
        if result is not None:
            return result[0]  # Возвращаем значение ячейки
        else:
            return None  # Если значение не найдено

    except sqlite3.Error as e:
        print(f"Error while working with SQLite: {e}")
        return None  # В случае ошибки возвращаем None

    finally:
        if connection:
            connection.close()

def update_row_in_table(file: str, table_name: str, row_number: int, data: list):
    try:
        connection = sqlite3.connect(file)
        cursor = connection.cursor()

        # Получаем имена столбцов
        column_names = get_columns_in_table(file, table_name)
        code_column = "kod" * (table_name == "Experts" or table_name == "Reg_obl_city") + "codrub" * (table_name == "grntirub")
        # Формируем SQL запрос для обновления строки
        set_clause = ', '.join([f'"{column_name}" = ?' for column_name in column_names])
        query = f"UPDATE \"{table_name}\" SET {set_clause} WHERE {code_column} = ?"

        # Выполняем запрос
        cursor.execute(query, (*data, row_number))
        connection.commit()

    except sqlite3.Error as e:
        print(f"Error while updating row: {e}")

    finally:
        if connection:
            connection.close()