from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtGui import QFont

class MainPresenter:
	def __init__(self, view, model):
		self.view = view
		self.model = model 

		self.load_data()
		self.view.set_filter_handler(self.filter_items)

	def load_data(self):
		try:
			results = self.model.get_nbrb()
			self.widgets = []

			for result in results:
				widget = self.create_rows(result.source, result.abbreviation, result.scale, result.rate, result.percent)
				self.view.add_item(widget)
				self.widgets.append(widget)

			self.view.add_spacer()
		except Exception as e: self.error_view(str(e))

	def error_view(self, text):
		ErrorText = QLabel()
		ErrorText.setStyleSheet("color: red;")
		ErrorText.setText(text)

		self.view.add_spacer()
		self.view.add_item(ErrorText)
		self.view.add_spacer()

	def filter_items(self, text):
		text = text.lower()
		for widget in self.widgets:
			label = widget.findChild(QLabel)
			if label:
				widget.setVisible(text in label.text().lower())

	def create_rows(self, source, ab, scale, rate, percent):
		font1 = QFont()
		font1.setPointSize(9)
		font1.setBold(True)
		font1.setWeight(75)

		font2 = QFont()
		font2.setPointSize(8)
		font2.setKerning(True)

		font3 = QFont()
		font3.setPointSize(8)

		row = QWidget()
		row.setStyleSheet(u":hover{border-radius: 10px; background-color: rgb(57, 57, 57);}")

		horizontalLayout_2 = QHBoxLayout(row)
		horizontalLayout_2.setContentsMargins(9, 9, 9, -1)

		abWidget = QWidget(row)
		abWidget.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

		verticalLayout_1 = QVBoxLayout(abWidget)
		verticalLayout_1.setSpacing(0)
		verticalLayout_1.setContentsMargins(0, 0, 0, 0)

		Abbreviation = QLabel(abWidget)
		Abbreviation.setFont(font1)
		if scale != 1:
			Abbreviation.setText(f"{scale} {ab}")
		else:
			Abbreviation.setText(f"{ab}")

		Source = QLabel(abWidget)
		Source.setFont(font2)
		Source.setStyleSheet(u"color: rgb(142, 142, 142);")
		Source.setText(f"{source}")

		verticalLayout_1.addWidget(Abbreviation)
		verticalLayout_1.addWidget(Source)

		horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

		PriceWidget = QWidget(row)
		PriceWidget.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")

		horizontalLayout_1 = QHBoxLayout(PriceWidget)
		horizontalLayout_1.setSpacing(10)
		horizontalLayout_1.setContentsMargins(0, 0, 0, 0)

		Price = QLabel(PriceWidget)
		Price.setFont(font1)
		Price.setAlignment(Qt.AlignCenter)
		Price.setMargin(0)
		Price.setText(f"{rate}")

		Percent = QLabel(PriceWidget)
		Percent.setFont(font3)
		Percent.setAlignment(Qt.AlignCenter)
		if float(percent) < 0:
			Percent.setStyleSheet(u"background-color: rgb(219, 47, 99); min-width: 60px; min-height: 20px; border-radius: 5px;")
			Percent.setText(f"{percent}%")
		else:
			Percent.setStyleSheet(u"background-color: rgb(0, 170, 66); min-width: 60px; min-height: 20px; border-radius: 5px;")
			Percent.setText(f"+{percent}%")

		horizontalLayout_1.addWidget(Price)
		horizontalLayout_1.addWidget(Percent)

		horizontalLayout_2.addWidget(abWidget)
		horizontalLayout_2.addItem(horizontalSpacer)
		horizontalLayout_2.addWidget(PriceWidget)
		return row