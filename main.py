from qt.main import *

def main():
    #set_cell_value("data\\DATABASE.db", "grntirub", 80, "codrub", 121212)
    #add_row_to_table("data\\DATABASE.db", "grntirub", [8148, "asdasdasd"])
    #print(f"{get_table("data\\DATABASE.db", "grntirub")}\n{get_rows_in_table("data\\DATABASE.db", "grntirub")}")
    #delete_row_by_number("data\\DATABASE.db", "grntirub", 81)
    #print(f"{get_table("data\\DATABASE.db", "grntirub")}\n{get_rows_in_table("data\\DATABASE.db", "grntirub")}")
    app = QApplication(sys.argv) 
    window = MyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()