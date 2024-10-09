# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerhlPjsX.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setMinimumSize(QSize(1920, 1080))
        MainWindow.setAutoFillBackground(True)
        self.scientists = QAction(MainWindow)
        self.scientists.setObjectName(u"scientists")
        self.grnti = QAction(MainWindow)
        self.grnti.setObjectName(u"grnti")
        self.regions = QAction(MainWindow)
        self.regions.setObjectName(u"regions")
        self.all_tables = QAction(MainWindow)
        self.all_tables.setObjectName(u"all_tables")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setBaseSize(QSize(1920, 0))
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(70, 20, 1800, 900))
#if QT_CONFIG(tooltip)
        self.tableWidget.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tableWidget.setShowGrid(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 22))
        self.data = QMenu(self.menubar)
        self.data.setObjectName(u"data")
        self.groups = QMenu(self.menubar)
        self.groups.setObjectName(u"groups")
        self.report = QMenu(self.menubar)
        self.report.setObjectName(u"report")
        self.help = QMenu(self.menubar)
        self.help.setObjectName(u"help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.data.menuAction())
        self.menubar.addAction(self.groups.menuAction())
        self.menubar.addAction(self.report.menuAction())
        self.menubar.addAction(self.help.menuAction())
        self.data.addSeparator()
        self.data.addAction(self.all_tables)
        self.data.addAction(self.scientists)
        self.data.addAction(self.grnti)
        self.data.addAction(self.regions)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.scientists.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0447\u0435\u043d\u044b\u0435", None))
        self.grnti.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0420\u041d\u0422\u0418", None))
        self.regions.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0433\u0438\u043e\u043d\u044b", None))
        self.all_tables.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435 \u0442\u0430\u0431\u043b\u0438\u0446\u044b", None))
        self.data.setTitle(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u043d\u043d\u044b\u0435", None))
        self.groups.setTitle(QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0443\u043f\u043f\u044b", None))
        self.report.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0435\u0442", None))
        self.help.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043c\u043e\u0449\u044c", None))
    # retranslateUi

