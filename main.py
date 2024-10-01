# PyQt6 Application with Menu 

import sys
import os
from PySide6.QtCore import QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QWidget, QTableView)
from sql.requests import * 
class MyApp(QMainWindow): 
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Управление организацией экспертизы научно-технических проектов") 
        self.setGeometry(1080, 1080, 1920, 1920) 
        self.setStyleSheet(u"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(60, 52, 57, 255), stop:0.4375 rgba(66, 53, 65, 255), stop:0.994318 rgba(63, 51, 69, 255));\n color: white; \n font: 12pt 'Times New Roman'; \n"
"")     
        self.create_menu()
        self.create_context_menu()
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
        #print(rows, cols)
        self.table = QTableWidget(rows, cols)
      
        self.table.setStyleSheet(u"gridline-color:white; \n; color: white; \n""")
        stylesheet = "::section{Background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(60, 52, 57, 255), stop:0.4375 rgba(66, 53, 65, 255), stop:0.994318 rgba(63, 51, 69, 255));\n gridline-color:white; \n; color: white; \n}"
        self.table.verticalHeader().setStyleSheet(stylesheet)
        self.table.horizontalHeader().setStyleSheet(stylesheet)

        
        self.table.setColumnCount(cols)
        self.table.setRowCount(rows)
        self.setCentralWidget(self.table)
        self.insert_data(tb, rows, cols)
    
    def contextMenuEvent(self, event):
        # Show the context menu
        self.context_menu.exec(event.globalPos())
 
    def add_data_triggered(self):
        dialog = add_data_window()
        dialog.show()
        
 
    def del_data_triggered(self):
        dialog = del_data_window()
        dialog.show()
        
 
    def ch_data_triggered(self):
        dialog = ch_data_window()
        dialog.show()
        
class add_data_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление новых данных")

class del_data_window(QMainWindow):
    def __init__(self):
        super(del_data_window, self).__init__()
        self.setWindowTitle("Удаление данных")
class ch_data_window(QMainWindow):
    def __init__(self):
        super(ch_data_window, self).__init__()
        self.setWindowTitle("Редактирование данных")
    

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