import sqlite3
from sql.db_utils import connect_db

def get_merged_table(file):
    """
    Returns a merged table of Experts and Reg_obl_city tables and grntirub table filtered by the first two characters of the grnti field.

    Args:
        file (str): path to the SQLite database file

    Returns:
        merged table
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

        return merged_table
    except sqlite3.Error as ex:
        print(f"Error while working with the database: {ex}")
        return None
    except IndexError as ex:
        print(f"Error while working with the database: {ex}")
        return None

def get_merged_columns(file):
    try:
        connection = connect_db(file)
        # Get the column names from the merged table
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(Experts);")
        columns_experts = cursor.fetchall()
        cursor.execute("PRAGMA table_info(Reg_obl_city);")
        columns_regions = cursor.fetchall()
        cursor.execute("PRAGMA table_info(grntirub);")
        columns_grntirub = cursor.fetchall()

        # Construct the list of column names
        columns = [col[1] for col in columns_experts] + ["oblname"] + [f"grntirub_{col[1]}" for col in columns_grntirub]

        return columns
    except Exception as ex:
        print(f"Error while working with the database: {ex}")
        return None


def get_merged_rows(file):
    try:
        connection = connect_db(file)
        # Get the number of rows from the merged table
        cursor = connection.cursor()
        query = """
                SELECT COUNT(*)
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
        cursor.execute(query)
        rows = cursor.fetchone()[0]

        return rows
    except Exception as ex:
        print(f"Error while working with the database: {ex}")
        return None