from qt.main import *

def main():
    print(f"{get_table("data\\DATABASE.db", "grntirub")}\n{get_rows_in_table("data\\DATABASE.db", "grntirub")}")
    #delete_row_by_number("data\\DATABASE.db", "grntirub", 82)
    #print(f"{get_table("data\\DATABASE.db", "grntirub")}\n{get_rows_in_table("data\\DATABASE.db", "grntirub")}")
    app = QApplication(sys.argv) 
    window = MyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()