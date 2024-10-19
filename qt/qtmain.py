import os
import sys
from PySide6.QtCore import QRect, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidget, 
    QTableWidgetItem, QWidget, QHeaderView, QMenu, 
    QMenuBar, QSizePolicy, QStatusBar, QAbstractItemView, 
    QPushButton, QDialog, QComboBox, QLineEdit, 
    QGroupBox, QLabel, QHBoxLayout, QVBoxLayout
)
from PySide6.QtGui import QPalette, QColor, QAction
from filter_by_keyword import *
from sql.cell_utils import *
from sql.edit_utils import *
from sql.get_utils import *
from sql.get_merged_utils import *

class MyApp(QMainWindow): 
    def __init__(self): 
        super().__init__()
        self.current_table_name = None
        self.setWindowTitle("Управление организацией экспертизы научно-технических проектов")
        self.sel_rows = 0 
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
            self.table = QTableWidget(rows - 1, cols)  # Adjusted for header row
            self.table.setColumnCount(cols)
            self.table.setRowCount(rows - 1)  # Adjusted for header row
            self.insert_data(tb[1:], rows - 1, cols)  # Skip header row
        else:
            tb = get_table(file, name)
            cols = get_columns_count_in_table(file, name)
            rows = get_rows_count_in_table(file, name)
            self.table = QTableWidget(rows - 1, cols)  # Adjusted for header row
            self.table.setColumnCount(cols)
            self.table.setRowCount(rows - 1)  # Adjusted for header row
            self.insert_data(tb[1:], rows - 1, cols)  # Skip header row
        for col in range(cols):
            self.table.setHorizontalHeaderItem(col, QTableWidgetItem(tb[0][col]))  # Set header names
        self.current_table_name = name

        titles = {
            "all": "[ Объединенные таблицы ]",
            "Experts": "[ Эксперты ]",
            "grntirub": "[ ГРНТИ ]",
            "Reg_obl_city": "[ Регионы ]"
        }

        self.setWindowTitle("Управление организацией экспертизы научно-технических проектов: " + titles.get(name, ""))
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: rgb(53, 53, 53); color: white; }")
        self.table.verticalHeader().setStyleSheet("QHeaderView::section { background-color: rgb(53, 53, 53); color: white; }")
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.update_context_menu()
        for i in range(cols):
            self.adjust_column_width(i)
        self.setCentralWidget(self.table)

    def get_current_table_name(self):
        return self.current_table_name

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
 
        
    def del_data_triggered(self):
        table_name = self.get_current_table_name()
        select_rows = self.get_select_rows()
        item = []
        for i in select_rows:
            item.append(self.table.item(i,0).text())
        self.del_data_window = del_data_window(self, table_name, item)
        self.del_data_window.show()
        
    def ch_data_triggered(self):
        selected_row = self.table.currentRow()  # Получаем номер выбранной строки
        if selected_row >= 0:  # Проверяем, что строка выбрана
            # Получаем имя текущей таблицы
            current_table_name = self.get_current_table_name()
            item = int(self.table.item(selected_row,0).text())
            # Создаем окно редактирования
            self.ch_data_window = EditDataWindow(self, current_table_name, item)  # Передаем номер строки (SQLite использует 1-based indexing)
            self.ch_data_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите строку для редактирования.")

    def filter_data_triggered(self):
        self.filter_data_window = filter_data_window(MyApp)
        self.filter_data_window.show()
    def get_select_rows(self):
        selected_rows = self.table.selectionModel().selectedRows()
        return [row.row() for row in selected_rows]
    def update_context_menu(self):
        self.sel_rows = self.get_select_rows()
        self.context_menu.actions()[2].setEnabled(len(self.sel_rows) == 0)  # Изменить данные
        #print(self.sel_rows)
    
    def refresh_table(self):
        file = os.path.join("data", "DATABASE.db")
        tb = get_table(file, self.get_current_table_name())
        cols = get_columns_count_in_table(file, self.get_current_table_name())
        rows = len(tb)
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        self.insert_data(tb, rows, cols)
        for i in range(cols):
            self.adjust_column_width(i)
    
    def add_data_triggered(self):
        # Get the current table name, you may need to adjust this line
        current_table_name = self.get_current_table_name()  # Implement this method as needed

        # Create the add_data_window and pass the current table name
        self.add_data_dialog = add_data_window(self, current_table_name)
        self.add_data_dialog.show()  # Show the dialog

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
    def __init__(self, parent, table_name):
        super().__init__()
        self.parent = parent  # Ссылка на экземпляр MyApp
        self.table_name = table_name
        self.setWindowTitle("Добавление новых данных")
        self.setGeometry(100, 100, 600, 500)
        self.setFixedSize(600,500)
        # Применение темной темы
        self.dark_theme = DarkTheme()
        self.dark_theme.apply(self)

        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(10, 10, 380, 360)

        self.fields = {}  # Словарь для хранения полей ввода

        self.create_input_fields()  # Создаем поля ввода

        # Кнопка для добавления данных
        self.pushButton = QPushButton("Добавить", self.groupBox)
        self.pushButton.setGeometry(130, 310, 81, 21)
        self.pushButton.clicked.connect(self.add_data)

        # Кнопка для закрытия окна
        self.pushButton_2 = QPushButton("Закрыть", self.groupBox)
        self.pushButton_2.setGeometry(10, 310, 81, 21)
        self.pushButton_2.clicked.connect(self.close)
        self.close()
    def create_input_fields(self):
        # Получаем имена столбцов для текущей таблицы
        column_names = get_columns_in_table(os.path.join("data", "DATABASE.db"), self.table_name)

        for index, column_name in enumerate(column_names):
            label = QLabel(column_name, self.groupBox)
            label.setGeometry(10, 30 + index * 30, 100, 20)

            line_edit = QLineEdit(self.groupBox)
            line_edit.setGeometry(120, 30 + index * 30, 200, 20)
            line_edit.setStyleSheet("QLineEdit { background-color: rgb(35, 35, 35); color: rgb(255, 255, 255); }")  # Темный фон и белый текст
            self.fields[column_name] = line_edit  # Сохраняем поле ввода в словарь

    def add_data(self):
        # Сбор данных из динамически созданных полей ввода
        data = []
        for column_name in get_columns_in_table(os.path.join("data", "DATABASE.db"), self.table_name):
            value = self.fields[column_name].text()
            data.append(value)

        # Вызов функции для добавления строки в базу данных
        file = os.path.join("data", "DATABASE.db")
        add_row_to_table(file, self.table_name, data)

        # Очищаем поля ввода после добавления
        self.clear_fields()

        # Обновляем основную таблицу, чтобы отобразить новые данные
        self.parent.refresh_table()
        QMessageBox.information(self, "Успех", "Данные успешно добавлены.")
        self.close()
        #перекидывает на последнюю добавленную строку
        row_count = self.parent.table.rowCount()
        self.parent.table.scrollToBottom()
        self.parent.table.selectRow(row_count - 1)

    def clear_fields(self):
        for line_edit in self.fields.values():
            line_edit.clear()
            
            
class filter_data_window(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        
        self.setWindowTitle("Фильтрация данных")
        self.setGeometry(100, 100, 600, 500)
        self.setFixedSize(600,500)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 380, 280))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setText("Выберите регион:")
        self.label.setGeometry(QRect(10, 30, 150, 21))
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(130, 210, 81, 21))
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(10, 210, 81, 21))
        self.combobox = QComboBox(self.groupBox)
        #self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.combobox.setGeometry(QRect(7, 54, 200, 19))
        file = os.path.join("data", "DATABASE.db")

        a = get_table(file,"Reg_obl_city")
        unique_values = set(row[0] for row in a)
        for value in unique_values:
            if value != "region":
                self.combobox.addItem(value)

        
        
        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.pushButton_2.setText("Закрыть")
        self.pushButton.setText("Фильтровать")
        self.pushButton_2.clicked.connect(self.close_window)
        self.pushButton.clicked.connect(self.filtr_data)

    def close_window(self):
        self.close()  
    def filtr_data(self):
        print(filter_merged_table_by_keyword(self.combobox.currentText()))
        print(self.combobox.currentText())
        '''self.table.clear()
        data = filter_merged_table_by_keyword(self.combobox.currentText())
        for i in range(len(data)):
            self.table.addItem(data[i])
        QMessageBox.information(self, "Успех", "Данные успешно добавлены!")
        self.parent.refresh_table()'''


class EditDataWindow(QMainWindow):
    def __init__(self, parent, table_name, row_number):
        super().__init__()
        self.parent = parent
        self.table_name = table_name

        self.row_number = row_number  # Используем 1-based индекс
        self.setWindowTitle("Редактирование данных")
        self.setGeometry(100, 100, 600, 500)
        self.setFixedSize(600,500)
        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(10, 10, 380, 350)  # Уменьшили высоту группы

        self.fields = {}

        self.create_input_fields()

        # Кнопка для сохранения изменений
        self.pushButton = QPushButton("Сохранить", self.groupBox)
        self.pushButton.setGeometry(130, 310, 81, 21)  # Отступ сверху
        self.pushButton.clicked.connect(self.save_data)

        # Кнопка для закрытия окна
        self.pushButton_2 = QPushButton("Закрыть", self.groupBox)
        self.pushButton_2.setGeometry(10, 310, 81, 21)  # Отступ сверху
        self.pushButton_2.clicked.connect(self.close)

        self.dark_theme = DarkTheme()
        self.dark_theme.apply(self)

    def create_input_fields(self):
        column_names = get_columns_in_table(os.path.join("data", "DATABASE.db"), self.table_name)

        for index, column_name in enumerate(column_names):
            label = QLabel(column_name, self.groupBox)
            label.setGeometry(10, 30 + index * 30, 100, 20)

            line_edit = QLineEdit(self.groupBox)
            line_edit.setGeometry(120, 30 + index * 30, 200, 20)
            line_edit.setStyleSheet("QLineEdit { background-color: rgb(35, 35, 35); color: rgb(255, 255, 255); }")  # Темный фон и белый текст

            # Получаем текущее значение
            current_value = get_cell_value(os.path.join("data", "DATABASE.db"), self.table_name, self.row_number, column_name)

            # Убедитесь, что current_value является строкой
            line_edit.setText(str(current_value) if current_value is not None else '')

            self.fields[column_name] = line_edit  # Сохраняем поле ввода в словарь

    def save_data(self):
        # Сбор данных из полей ввода
        data = [self.fields[column_name].text() for column_name in self.fields]

        # Обновление строки в таблице
        update_row_in_table(os.path.join("data", "DATABASE.db"), self.table_name, self.row_number, data)

        # Обновление таблицы в основном окне
        self.parent.refresh_table()

        # Закрытие окна
        self.close()



class del_data_window(QMainWindow):
    def __init__(self,parent,table_name,select_rows):   
        super().__init__()
        self.parent = parent  # Ссылка на экземпляр MyApp
        self.table_name = table_name
        self.select_rows = select_rows
        self.setWindowTitle("Удаление данных")
        self.setGeometry(100, 100, 500, 400)
        self.setFixedSize(500, 400)
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(50, 100, 400, 150)
        
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setText("Вы действительно хотите удалить?")
        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
        self.pushButton = QPushButton("Удалить", self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton("Отмена", self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.dark_theme = DarkTheme() 
        self.dark_theme.apply(self)
        self.pushButton_2.clicked.connect(self.close_window)
        self.pushButton.clicked.connect(self.delete_selected_row)

    def close_window(self):
        
        self.close()  # Close the window
    
    def delete_selected_row(self):
        file = os.path.join("data", "DATABASE.db")
        del_rows = self.select_rows
        
        for i in del_rows:
            if i is not None:
                #сделать удаление по коду, а не по номеру строки
                delete_row_by_code(file, self.table_name, str(i))
                self.parent.refresh_table()      
        QMessageBox.information(self, "Успех", "Данные успешно удалены!")
        
        
    

class ch_data_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактирование данных")
        self.setGeometry(100, 100, 600, 500)
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
