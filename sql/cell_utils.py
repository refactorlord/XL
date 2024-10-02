from sql.table_utils import get_table, get_rows_in_table, get_columns_in_table

def get_cell_value(file, name, i, j):
    table = get_table(file, name)
    rows = get_rows_in_table(file, name)
    cols = get_columns_in_table(file, name)
    if 0 <= i < rows and 0 <= j < cols:
        return table[i][j]
    else:
        raise IndexError("Индексы выходят за пределы таблицы")