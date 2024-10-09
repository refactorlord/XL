import os
import pandas as pd
import sqlite3

# файл чтобы создать БД

def excel_to_db(excel_file, db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    xls = pd.ExcelFile(excel_file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        df.to_sql(sheet_name, connection, if_exists='replace', index=False)
    cursor.close()
    connection.close()

def convert_all(folder_path, db_file):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx'):
            excel_file = os.path.join(folder_path, file_name)
            print(f"Конвертация {excel_file}...")
            excel_to_db(excel_file, db_file)

def converter():
    folder_path = 'data'
    db_file = os.path.join(folder_path, 'DATABASE.db')
    convert_all(folder_path, db_file)