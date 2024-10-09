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

from PyQt6.QtWidgets import QMainWindow, QMenu, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QAbstractItemView, QPushButton, QDialog, QComboBox, QLineEdit, QGroupBox, QLabel, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from PyQt6.QtCore import Qt
import os, sys
from filter_by_keyword import *

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
        self.context_menu = QMenu(self)
        add_data = self.context_menu.addAction("Добавить данные")
        del_data = self.context_menu.addAction("Удалить данные")
        ch_data = self.context_menu.addAction("Изменить данные")
        sort_menu = self.context_menu.addMenu("Сортировка")
        sort_asc = sort_menu.addAction("Сортировка по возрастанию")
        sort_desc = sort_menu.addAction("Сортировка по убыванию")
        filtr =  self.context_menu.addAction("Фильтрация")
        filtr.triggered.connect(self.filter_data_triggered)
        add_data.triggered.connect(self.add_data_triggered)
        del_data.triggered.connect(self.del_data_triggered)
        ch_data.triggered.connect(self.ch_data_triggered)
        sort_asc.triggered.connect(lambda: self.sort_column(True))
        sort_desc.triggered.connect(lambda: self.sort_column(False))

    def filter_data(self, keyword):
        filtered_data = filter_merged_table_by_keyword(keyword)
    
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
        if flag:
            tb = get_merged_table(file)
            cols = get_merged_columns(file)
            rows = get_merged_rows(file)
            self.table = QTableWidget(rows, cols)
            self.table.setColumnCount(cols)
            self.table.setRowCount(rows)
            self.insert_data(tb, rows, cols)
        else:
            tb = get_table(file, name)
            cols = get_columns_in_table(file, name)
            rows = get_rows_in_table(file, name)
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
        for i in range(cols):
            self.adjust_column_width(i)
        self.setCentralWidget(self.table)

    def sort_column(self, ascending):
        index = self.table.currentColumn()
        self.table.sortItems(index, Qt.SortOrder.AscendingOrder if ascending else Qt.SortOrder.DescendingOrder)

    def adjust_column_width(self, column):
        max_length = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row, column)
            if item is not None:
                max_length = max(max_length, len(item.text()))
        self.table.setColumnWidth(column, max_length*8)  # Adjust multiplier as needed


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
    def filter_data_triggered(self):
        self.filter_data_window = filter_data_window()
        self.filter_data_window.show()
    
    def refresh_table(self):
        file = os.path.join("data", "DATABASE.db")
        tb = get_table(file, "Experts")
        cols = get_columns_in_table(file, "Experts")
        rows = len(tb)
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        self.insert_data(tb, rows, cols)
        for i in range(cols):
            self.adjust_column_width(i)
    
    def add_data_triggered(self):
        self.add_data_dialog = add_data_window(self)  # Передаем экземпляр MyApp
        self.add_data_dialog.show()

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
    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance  # Сохраняем ссылку на экземпляр MyApp
        self.setWindowTitle("Добавление новых данных")
        self.setGeometry(100, 100, 400, 300)

        # Создание элементов интерфейса
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 380, 280))

        # Поля ввода
        self.label = QLabel("ФИО", self.groupBox)
        self.label.setGeometry(QRect(10, 30, 100, 20))  # Задайте размер и положение
        self.lineEdit_fio = QLineEdit(self.groupBox)
        self.lineEdit_fio.setGeometry(QRect(120, 30, 250, 20))

        self.label_2 = QLabel("Город", self.groupBox)
        self.label_2.setGeometry(QRect(10, 70, 100, 20))
        self.lineEdit_city = QLineEdit(self.groupBox)
        self.lineEdit_city.setGeometry(QRect(120, 70, 250, 20))

        self.label_3 = QLabel("Регион", self.groupBox)
        self.label_3.setGeometry(QRect(10, 110, 100, 20))
        self.lineEdit_region = QLineEdit(self.groupBox)
        self.lineEdit_region.setGeometry(QRect(120, 110, 250, 20))

        self.label_4 = QLabel("ГРНТИ", self.groupBox)
        self.label_4.setGeometry(QRect(10, 150, 100, 20))
        self.lineEdit_grnti = QLineEdit(self.groupBox)
        self.lineEdit_grnti.setGeometry(QRect(120, 150, 250, 20))

        # Кнопки
        self.pushButton = QPushButton("Добавить", self.groupBox)
        self.pushButton.setGeometry(QRect(120, 210, 100, 30))
        self.pushButton.clicked.connect(self.add_data)  # Подключаем функцию добавления

        self.pushButton_2 = QPushButton("Закрыть", self.groupBox)
        self.pushButton_2.setGeometry(QRect(230, 210, 100, 30))
        self.pushButton_2.clicked.connect(self.close_window)

        # Применяем темную тему
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)

    def add_data(self):
        # Соберите данные из полей ввода
        data = [
            self.lineEdit_fio.text(),
            self.lineEdit_city.text(),
            self.lineEdit_region.text(),
            self.lineEdit_grnti.text(),
            " ",  # Для других столбцов
            " ",
            " ",
            " "
        ]

        # Добавьте строку в базу данных
        file = os.path.join("data", "DATABASE.db")
        table_name = "Experts"  # Замените на актуальное имя таблицы
        add_row_to_table(file, table_name, data)
        
        # Обновите основную таблицу в MyApp
        self.app_instance.refresh_table()
        
        self.close()

    def close_window(self):
        self.close()



class filter_data_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фильтрация данных")
        self.setGeometry(100, 100, 400, 300)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 380, 280))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 30, 31, 21))
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(130, 210, 81, 21))
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(10, 210, 81, 21))
        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(7, 54, 97, 19))
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.pushButton_2.clicked.connect(self.close_window)
    def close_window(self):
        self.close()  


class del_data_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Удаление данных")
        self.setGeometry(100, 100, 400, 300)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(10, 10, 380, 100)
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
        self.pushButton = QPushButton("Delete", self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton("Cancel", self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.pushButton_2.clicked.connect(self.close_window)

    def close_window(self):
        self.close()  # Close the window
class ch_data_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактирование данных")
        self.setGeometry(100, 100, 400, 300)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 380, 280))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 40, 31, 16))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(7, 77, 51, 16))
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(7, 114, 51, 16))
        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(7, 54, 191, 19))
        self.lineEdit_3 = QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(7, 91, 191, 19))
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(7, 151, 71, 16))
        self.lineEdit_4 = QLineEdit(self.groupBox)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(7, 128, 191, 19))
        self.lineEdit_8 = QLineEdit(self.groupBox)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setGeometry(QRect(7, 165, 191, 21))
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(130, 210, 71, 21))
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(10, 210, 111, 21))
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.pushButton_2.clicked.connect(self.close_window)

    def close_window(self):
        self.close()  # Close the window
