import os
import sys
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

from sql.cell_utils import *
from sql.edit_utils import *
from sql.get_utils import *
from sql.get_merged_utils import *

class MyApp(QMainWindow): 
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Управление организацией экспертизы научно-технических проектов") 
        self.setGeometry(0, 0, 1000, 1000) 
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

    def get_table_ui(self, name, flag=False):
        file = os.path.join("data", "DATABASE.db")
        if flag:
            tb = get_merged_table(file)
            cols = get_merged_columns(file)
            rows = get_merged_rows(file)
            self.table = QTableWidget(rows, len(cols))
            self.setCentralWidget(self.table)
            self.insert_data(tb, rows, len(cols))
        else:
            tb = get_table(file, name)
            cols = get_columns_in_table(file, name)
            rows = get_rows_in_table(file, name)
            self.table = QTableWidget(rows, cols)
            self.setCentralWidget(self.table)
            self.insert_data(tb, rows, cols)