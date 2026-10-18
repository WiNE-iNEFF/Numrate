# -*- coding: utf-8 -*-

import sys

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

from resources import resource_path
from model.currency import CurrencyAPIs
from view.main_window import MainWindow
from presenter.main_presenter import MainPresenter

APP_ID = "WiNEiNEFF.Numrate.0.0.2"


def set_windows_app_id():
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


if __name__ == "__main__":
    set_windows_app_id()

    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path("icon_1.ico")))

    currency = CurrencyAPIs()
    window = MainWindow()
    presenter = MainPresenter(window, currency)

    #window.show()
    window.showMaximized()
    presenter.start()
    sys.exit(app.exec_())
