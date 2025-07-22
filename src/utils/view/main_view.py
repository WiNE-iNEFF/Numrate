from PySide2.QtWidgets import QMainWindow, QSpacerItem, QSizePolicy
from src.utils.ui.ui_main import Ui_MainWindow

class MainView(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

	def add_item(self, widget):
		self.ui.verticalLayout_2.addWidget(widget)

	def add_spacer(self):
		spacer = QSpacerItem(20, 178, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.ui.verticalLayout_2.addItem(spacer)

	def set_filter_handler(self, handler):
		self.ui.Search.textChanged.connect(handler)