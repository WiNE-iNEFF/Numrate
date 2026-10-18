# -*- coding: utf-8 -*-

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QIcon,
    QColor
)
from PySide2.QtWidgets import (
    QPushButton,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTableView,
    QComboBox,
    QAbstractItemView,
    QHeaderView,
    QMenu
)
from qframelesswindow import FramelessWindow, StandardTitleBar

from resources import resource_path
from view.notifications import NotificationManager
from view.currency_proxy import CurrencyProxy



class MainWindow(FramelessWindow):
    period_changed = Signal(str)
    context_action_requested = Signal(str, list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.notification = NotificationManager(self)

        self.setTitleBar(StandardTitleBar(self))
        self.setWindowTitle("Numrate")
        self.setWindowIcon(QIcon(resource_path("icon_1.ico")))
        self.setMinimumSize(700, 600)

        self.titleBar.titleLabel.setStyleSheet("color: white; font-weight: bold;")
        self.titleBar.minBtn.setNormalColor(Qt.white)
        self.titleBar.minBtn.setHoverColor(QColor(150, 150, 150))
        self.titleBar.maxBtn.setNormalColor(Qt.white)
        self.titleBar.maxBtn.setHoverColor(QColor(150, 150, 150))
        self.titleBar.closeBtn.setNormalColor(Qt.white)

        self.setStyleSheet("""
        QWidget {
            background-color: rgb(0,0,0);
        }

        QLineEdit {
            background-color: rgb(29,29,29);
            border: none;
            border-radius: 10px;
            color: white;
            padding-left: 10px;
        }

        QLineEdit:focus {
            border: 1px solid rgb(70,70,70);
        }

        QMenu {
            background-color: rgb(29,29,29);
            border: none;
            border-radius: 4px;
            color: white;  
        }

        QMenu::item {
            padding: 8px 30px 8px 30px;
            border-radius: 4px;
        }

        QMenu::item:selected {
            background-color: rgb(50,50,50);
        }

        QComboBox {
            background-color: rgb(29,29,29);
            border: none;
            border-radius: 10px;
            color: white;
            padding-left: 10px;
        }

        QComboBox QAbstractItemView {
            background-color: rgb(29,29,29);
            color: white;
            selection-background-color: rgb(50,50,50);
            border: none;
        }

        QTableView {
            background-color: rgb(29,29,29);
            color: white;
            border: none;
            border-radius: 10px;
            alternate-background-color: rgb(24,24,24);
            selection-background-color: rgb(50,50,50);
            gridline-color: transparent;
        }

        QTableView::item {
            padding: 6px;
        }

        QHeaderView::section {
            background-color: rgb(20,20,20);
            color: rgb(142,142,142);
            border: none;
            padding: 8px;
            font-weight: bold;
        }
        QScrollBar:horizontal {
            border: none; background: transparent; height: 5px; margin: 0;
        }
        QScrollBar::handle:horizontal {
            background:  rgb(29, 29, 29); border-radius: 2px; min-width: 10px;
        }
        QScrollBar::add-line:horizontal {
            border: none; background: transparent; width: 0px;
        }
        QScrollBar::sub-line:horizontal {
            border: none; background: transparent; width: 0px;
        }
        QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
            border: none; width: 0px; height: 0px; background: transparent;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        QScrollBar:vertical {
            border: none; background: transparent; width: 5px; margin: 0;
        }
        QScrollBar::handle:vertical {
            background:  rgb(29, 29, 29); border-radius: 2px; min-height: 40px;
        }
        QScrollBar::add-line:vertical {
            border: none; background: transparent; width: 0px;
        }
        QScrollBar::sub-line:vertical {
            border: none; background: transparent; width: 0px; 
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            border: none; width: 0px; height: 0px; background: transparent;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """)

        #--LAYOUT--
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-1, 32, -1, -1)
        top_layout = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.setClearButtonEnabled(True)
        self.search.setFixedHeight(30)

        self.range_combo = QComboBox()
        self.range_combo.setFixedSize(80, 30)
        self.range_combo.addItems([
            "1D",
            "1W",
            "1M",
            "1Y"
        ])

        top_layout.addWidget(self.search)
        top_layout.addWidget(self.range_combo)
        layout.addLayout(top_layout)

        #--TABLE--
        self.table = QTableView()
        self.table.verticalHeader().hide()
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        #--MODEL--
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "Current Pair",
            "Rate",
            "Change (1D)",
            "Scale",
            "Source"
        ]) 

        #--PROXY--
        self.proxy = CurrencyProxy()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)
        self.table.setModel(self.proxy)

        #--SIGNALS--
        self.search.textChanged.connect(self.proxy.setFilterFixedString)
        self.range_combo.currentTextChanged.connect(self.period_changed)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def set_table_headers(self, period):
        self.model.setHorizontalHeaderLabels([
            "Current Pair",
            "Rate",
            f"Change ({period})",
            "Scale",
            "Source"
        ])

    def show_rows(self, rows):
        self.table.setSortingEnabled(False)
        self.model.removeRows(0, self.model.rowCount())

        for row in rows:
            q_item = QStandardItem(row.change)
            q_item.setForeground(Qt.red if row.is_negative else Qt.green)

            items = [
                QStandardItem(row.pair),
                QStandardItem(row.rate),
                q_item,
                QStandardItem(row.scale),
                QStandardItem(row.source)
            ]

            for item in items:
                item.setTextAlignment(Qt.AlignCenter)
            self.model.appendRow(items)

        self.table.setSortingEnabled(True)

    def set_period_enabled(self, enabled):
        self.range_combo.setEnabled(enabled)

    def show_notification(self, text, notif_type="info"):
        self.notification.show_notification(text, notif_type)

    def copy_to_clipboard(self, text):
        QApplication.clipboard().setText(text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.notification.reposition()

    def show_context_menu(self, pos):
        index = self.table.indexAt(pos)

        if not index.isValid():
            return

        menu = QMenu(self)
        menu.setAttribute(Qt.WA_TranslucentBackground)
        menu.setWindowFlags(menu.windowFlags() | Qt.FramelessWindowHint)
        menu.setStyleSheet("""
        QMenu {
            background-color: rgb(29,29,29);
            border: none;
            border-radius: 4px;
            color: white;  
        }
        QMenu::item {
            padding: 8px 30px 8px 30px;
            border-radius: 4px;
        }
        QMenu::item:selected {
            background-color: rgb(50,50,50);
        }
        """)

        copy_pair = menu.addAction("Copy Pair")
        copy_rate = menu.addAction("Copy Rate")
        copy_change = menu.addAction("Copy Change")
        copy_scale = menu.addAction("Copy Scale")
        copy_source = menu.addAction("Copy Source")
        copy_row = menu.addAction("Copy Entire Row")
        menu.addSeparator()
        update_data = menu.addAction("Refresh")
        menu.addSeparator()
        statistic = menu.addAction("Statistics")

        action = menu.exec_(self.table.viewport().mapToGlobal(pos))

        action_keys = {
            copy_pair: "copy_pair",
            copy_rate: "copy_rate",
            copy_change: "copy_change",
            copy_scale: "copy_scale",
            copy_source: "copy_source",
            copy_row: "copy_row",
            update_data: "update_data",
            statistic: "statistic",
        }

        key = action_keys.get(action)
        if key is None:
            return

        row = index.row()
        row_values = [self.proxy.index(row, column).data() for column in range(5)]

        self.context_action_requested.emit(key, row_values)
