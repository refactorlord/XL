import sqlite3
import os

def filter_merged_table_by_keyword(keyword):
    file = os.path.join("data", "DATABASE.db")
    try:
        connection = sqlite3.connect(file)
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('Experts', 'Reg_obl_city', 'grntirub');")
        tables = cursor.fetchall()

        if not any(table[0] in ('Experts', 'Reg_obl_city', 'grntirub') for table in tables):
            raise ValueError("One of the required tables does not exist")

        select_clause = """
            SELECT 
                CAST(e.kod AS TEXT) AS kod, 
                e.name, 
                e.grnti, 
                gr.rubrika,
                e.region,
                rc.oblname, 
                e.city, 
                e.input_date
        """

        from_clause = """
            FROM 
                Experts e
            INNER JOIN 
                Reg_obl_city rc 
                ON e.region = rc.region
                AND e.city = rc.city
        """

        left_join_clause = """
            LEFT JOIN 
                grntirub gr 
                ON COALESCE(
                    SUBSTR(e.grnti, 1, INSTR(e.grnti, '.') - 1),
                    SUBSTR(e.grnti, 1, INSTR(e.grnti, ';') - 1)
                ) = gr.codrub
        """

        where_clause = f"""
            WHERE
                e.grnti IS NOT NULL
                AND e.name LIKE '%{keyword}%'
        """

        query = f"{select_clause} {from_clause} {left_join_clause} {where_clause}"

        cursor.execute(query)
        filtered_table = cursor.fetchall()

        column_names = ['Код', 'ФИО', 'Код "GRNTI"', 'Рубрика', 'Регион', 'Область', 'Город', 'Дата ввода']

        if filtered_table:
            filtered_table.insert(0, column_names)

        cursor.close()
        connection.close()

        return filtered_table if filtered_table else [column_names]

    except sqlite3.Error as ex:
        print(f"Error while working with the database: {ex}")
        return None
    except ValueError as ex:
        print(f"Error: {ex}")
        return None