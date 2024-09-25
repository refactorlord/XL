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
    QTableWidgetItem, QWidget)
from sql.requests import *

class MyApp(QMainWindow): 
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Управление организацией экспертизы научно-технических проектов") 
        self.setGeometry(100, 100, 600, 400) 
        self.create_menu()

    def create_menu(self): 
        menubar = self.menuBar() 
        data_menu = menubar.addMenu("Данные")
        groups_menu = menubar.addMenu("Группы")
        report_menu = menubar.addMenu("Отчет")
        help_menu = menubar.addMenu("Помощь")
        action1 = QAction("Все таблицы", self) 
        action1.triggered.connect(lambda: self.get_table_ui("all", True)) 
        data_menu.addAction(action1) 
        
        action2 = QAction("Ученые", self)
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

    def def2(self):
        return [
            ["Row1-Col1", "Row1-Col2", "Row1-Col3"],
            ["Row2-Col1", "Row2-Col2", "Row2-Col3"],
            ["Row3-Col1", "Row3-Col2", "Row3-Col3"],
            ["Row4-Col1", "Row4-Col2", "Row4-Col3"],
            ["Row5-Col1", "Row5-Col2", "Row5-Col3"],
        ]

    def get_table_ui(self, name, flag=False):
        file = os.path.join("data", "DATABASE.db")
        tb, (rows, cols) = get_combined_table(file, name, flag)
        #print(rows, cols)
        self.table = QTableWidget(rows, cols)
        self.setCentralWidget(self.table)
        self.insert_data(tb, rows, cols)

if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    window = MyApp()
    window.show()
    sys.exit(app.exec())