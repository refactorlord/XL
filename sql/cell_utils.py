from sql.get_utils import *

def get_cell_value(file, name, i, j):
    table = get_table(file, name)
    rows = get_rows_in_table(file, name)
    cols = get_columns_in_table(file, name)
    if 0 <= i < rows and 0 <= j < cols:
        return table[i][j]
    else:
        raise IndexError("Индексы выходят за пределы таблицы")
    
