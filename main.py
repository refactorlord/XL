from PyQt6.QtWidgets import QMainWindow, QMenu, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QAbstractItemView, QPushButton
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
import os, sys
from sql.requests import *

class MyApp(QMainWindow): 
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Управление организацией экспертизы научно-технических проектов") 
        self.setGeometry(100, 100, 800, 600) 
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)    
        self.create_menu()
        self.create_context_menu()
        self.setMouseTracking(True)
        self.dialogs = list()

    def create_context_menu(self):
        # Создание контекстного меню
        self.context_menu = QMenu(self)
        add_data = self.context_menu.addAction("Добавить данные")
        del_data = self.context_menu.addAction("Удалить данные")
        ch_data = self.context_menu.addAction("Изменить данные")
 
        # Добавляем к нему функции 
        add_data.triggered.connect(self.add_data_triggered)
        del_data.triggered.connect(self.del_data_triggered)
        ch_data.triggered.connect(self.ch_data_triggered)

    def create_menu(self): 
        menubar = self.menuBar() 
        menubar.setStyleSheet("QMenuBar { background-color: rgb(53, 53, 53); color: white; }"
                               "QMenu { background-color: rgb(53, 53, 53); color: white; }"
                               "QMenu::item:selected { background-color: rgb(42, 130, 218); }")
        data_menu = menubar.addMenu("Данные")
        groups_menu = menubar.addMenu("Группы")
        report_menu = menubar.addMenu("Отчет")
        help_menu = menubar.addMenu("Помощь")
        
        action1 = QAction("Все таблицы", self) 
        action1.triggered.connect(lambda: self.get_table_ui("all", True)) 
        data_menu.addAction(action1) 
        
        action2 = QAction("Эксперты", self)
        action2.triggered.connect(lambda: self.get_table_ui("Experts")) 
        data_menu.addAction(action2) 
 
        action3 = QAction("ГРНТИ", self)
        action3.triggered.connect(lambda: self.get_table_ui("grntirub")) 
        data_menu.addAction(action3) 
 
        action4 = QAction("Регионы", self)
        action4.triggered.connect(lambda: self.get_table_ui("Reg_obl_city")) 
        data_menu.addAction(action4) 

    def insert_data(self, data, rows, cols):
        for row in range(rows):
            for column in range(cols):
                self.table.setItem(row, column, QTableWidgetItem(data[row][column]))

    def get_table_ui(self, name, flag=False):
        file = os.path.join("data", "DATABASE.db")
        tb, (rows, cols) = get_combined_table(file, name, flag)
        self.table = QTableWidget(rows, cols)

        self.table.setColumnCount(cols)
        self.table.setRowCount(rows)
        self.insert_data(tb, rows, cols)
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: rgb(53, 53, 53); color: white; }")
        self.table.verticalHeader().setStyleSheet("QHeaderView::section { background-color: rgb(53, 53, 53); color: white; }")
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        #self.setCentralWidget(self.table)
        self.setCentralWidget(self.table)

    def contextMenuEvent(self, event):
        # Show the context menu
        self.context_menu.exec(event.globalPos())
 
    def add_data_triggered(self):
        
        self.add_data_dialog = add_data_window()  # Создаем экземпляр окна
        
        self.add_data_dialog.show()  # Показываем окно
        
    def del_data_triggered(self):
        self.del_data_window = del_data_window()
        self.del_data_window.show()
        
    def ch_data_triggered(self):
        self.ch_data_window = ch_data_window()
        self.ch_data_window.show()
        
class DarkTheme:
    def __init__(self):
        self.palette = QPalette()
        self.set_colors()

    def set_colors(self):
        self.palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        self.palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        self.palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        self.palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        self.palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        self.palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        self.palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        self.palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    def apply(self, widget):
        widget.setPalette(self.palette)
        
class add_data_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление новых данных")
        self.setGeometry(100, 100, 400, 300)
        self.button = QPushButton("Закрыть", self)
        self.button.setGeometry(QRect(150, 120, 100, 30))
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.button.clicked.connect(self.close_window)

    def close_window(self):
        self.close()  # Закрытие окна

class del_data_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Удаление данных")
        self.setGeometry(100, 100, 400, 300)
        self.button = QPushButton("Закрыть", self)
        self.button.setGeometry(QRect(150, 120, 100, 30))
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.button.clicked.connect(self.close_window)

    def close_window(self):
        self.close()  # Закрытие окна
class ch_data_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактирование данных")
        self.setGeometry(100, 100, 400, 300)
        self.button = QPushButton("Закрыть", self)
        self.button.setGeometry(QRect(150, 120, 100, 30))
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.button.clicked.connect(self.close_window)

    def close_window(self):
        self.close()  # Закрытие окна
    

if __name__ == "__main__":
    file = os.path.join("data", "DATABASE.db")
    print(get_table(file, "grntirub"))
    add_row_to_table(file, "grntirub", [1003, "check this"])
    print(get_table(file, "grntirub"))
    #print(list_tables("data/DATABASE.db"))
    app = QApplication(sys.argv) 
    window = MyApp()
    window.show()
    sys.exit(app.exec())