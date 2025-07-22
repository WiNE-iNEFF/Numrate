# -*- coding: utf-8 -*-
import os, sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 407)
        MainWindow.setMinimumSize(QSize(500, 300))
        MainWindow.setMaximumSize(QSize(600, 16777215))
        resource = lambda path: os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), path)
        #icon = QIcon()
        #icon.addFile(u"app_code/src/assets/logo/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(QIcon(resource("app_code/src/assets/logo/logo.ico")))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"QScrollBar:horizontal {border: none; background: transparent; height: 5px; margin: 0;}\n"
"QScrollBar::handle:horizontal {background:  rgb(29, 29, 29); border-radius: 2px; min-width: 10px;}\n"
"QScrollBar::add-line:horizontal {border: none; background: transparent; width: 0px;}\n"
"QScrollBar::sub-line:horizontal {border: none; background: transparent; width: 0px;}\n"
"QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {border: none; width: 0px; height: 0px; background: transparent;}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {background: none;}\n"
"QScrollBar:vertical {border: none; background: transparent; width: 5px; margin: 0;}\n"
"QScrollBar::handle:vertical {background:  rgb(29, 29, 29); border-radius: 2px; min-height: 40px;}\n"
"QScrollBar::add-line:vertical {border: none; background: transparent; width: 0px;}\n"
"QScrollBar::sub-line:vertical {border: none; background: transparent; width: 0px; }\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {border: none; width: 0px; height: 0px; background: transparent;}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}")
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.centralwidget.setStyleSheet(u"background-color: rgb(0,0,0);")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Search = QLineEdit(self.centralwidget)
        self.Search.setObjectName(u"Search")
        self.Search.setMinimumSize(QSize(0, 25))
        self.Search.setMaximumSize(QSize(16777215, 25))
        font = QFont()
        font.setPointSize(9)
        self.Search.setFont(font)
        self.Search.setMouseTracking(True)
        self.Search.setFocusPolicy(Qt.ClickFocus)
        self.Search.setToolTipDuration(-1)
        self.Search.setStyleSheet(u"background-color: rgb(29, 29, 29); border-color: transparent; border: 0px; border-radius: 10px; color: rgb(142, 142, 142); padding-left: 5px;")
        self.Search.setMaxLength(10)

        self.gridLayout.addWidget(self.Search, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"background-color: rgba(0,0,0,0); color: rgb(255, 255, 255); border-color: transparent; border: none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 582, 358))
        self.scrollAreaWidgetContents.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Numrate", None))
        self.Search.setPlaceholderText("Search...")

