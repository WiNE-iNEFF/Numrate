from src.utils.presenter.main_presenter import MainPresenter
from src.utils.model.currency import CurrencyAPIs
from src.utils.view.main_view import MainView
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
import sys
import os


os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.abspath("platforms")


if __name__ == "__main__":
	resource = lambda path: os.path.join(getattr(sys, '_MEIPASS', os.getcwd()), path)
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon(resource('app_code/src/assets/logo/logo.ico')))
	view = MainView()
	model = CurrencyAPIs()
	presenter = MainPresenter(view, model)
	view.show()
	sys.exit(app.exec_())