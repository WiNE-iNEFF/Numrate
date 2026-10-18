from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from urllib.parse import quote
import pandas as pd
import requests

class CurrencyData:
	def __init__(self, source, cur_id, ab, scale, rate, old_rate):
		self._source = source
		self._id = cur_id
		self._abbreviation = ab
		self._scale = scale
		self._rate = rate
		self._old_rate = old_rate

	@property
	def abbreviation(self):
		return self._abbreviation

	@property
	def scale(self):
		return self._scale

	@property
	def rate(self):
		return self._rate

	@property
	def percent(self):
		if not self._old_rate: return f"0.00"
		return f"{(((self._rate - self._old_rate)/self._old_rate) * 100):.2f}"

	@property
	def int_percent(self):
		if not self._old_rate: return 0.00
		return ((self._rate - self._old_rate)/self._old_rate) * 100

	@property
	def source(self):
		return self._source



class CurrencyAPIs:
	def get_nbrb(self, period="1D"):
		currencys = []
		source = "National Bank of the Republic of Belarus"

		today_data = requests.get("https://api.nbrb.by/exrates/rates?periodicity=0").json()

		if period == "1W":
			data = requests.get(f"https://api.nbrb.by/exrates/rates?ondate={date.today() - timedelta(weeks=1)}&periodicity=0").json()
		elif period == "1M":
			data = requests.get(f"https://api.nbrb.by/exrates/rates?ondate={date.today() - relativedelta(months=1)}&periodicity=0").json()
		elif period == "1Y":
			data = requests.get(f"https://api.nbrb.by/exrates/rates?ondate={date.today() - relativedelta(years=1)}&periodicity=0").json()
		else:
			data = requests.get(f"https://api.nbrb.by/exrates/rates?ondate={date.today() - timedelta(days=1)}&periodicity=0").json()

		for num, currency in enumerate(today_data):
			cur_id = currency["Cur_ID"]
			ab = currency["Cur_Abbreviation"]
			scale = currency["Cur_Scale"]
			rate = currency["Cur_OfficialRate"]

			for old_num, old_currency in enumerate(data):
				if ab == old_currency["Cur_Abbreviation"]:
					old_rate = old_currency["Cur_OfficialRate"]
					break

			currencys.append(CurrencyData(source, cur_id, f"{ab}/BYN", scale, rate, old_rate))

		return currencys
		

	def get_cbr(self, period="1D"):
		currencys = []
		source = "The Central Bank of the Russian Federation"

		today_data = pd.read_xml(requests.get("https://www.cbr.ru/scripts/XML_daily.asp").text, encoding="windows-1251")

		if period == "1W":
			data = pd.read_xml(requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={(date.today() - timedelta(weeks=1)).strftime('%d/%m/%Y')}").text, encoding="windows-1251")
		elif period == "1M":
			data = pd.read_xml(requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={(date.today() - relativedelta(months=1)).strftime('%d/%m/%Y')}").text, encoding="windows-1251")
		elif period == "1Y":
			data = pd.read_xml(requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={(date.today() - relativedelta(years=1)).strftime('%d/%m/%Y')}").text, encoding="windows-1251")
		else:
			data = pd.read_xml(requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={(date.today() - timedelta(days=1)).strftime('%d/%m/%Y')}").text, encoding="windows-1251")

		for num, currency in today_data.iterrows():
			cur_id = currency['ID']
			ab = currency['CharCode']
			scale = currency['Nominal']
			rate = currency['Value'].replace(",", ".")

			for old_num, old_currency in data.iterrows():
				if ab == old_currency['CharCode']:
					old_rate = old_currency['Value'].replace(",", ".")
					break

			currencys.append(CurrencyData(source, cur_id, f"{ab}/RUB", scale, float(rate), float(old_rate)))

		return currencys


	def get_cfets(self, period="1D"):
		currencys = []
		source = "China Foreign Exchange Trade System"

		today_data = requests.get("https://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/crr.json").json()['records']

		if period == "1Y":
			data = requests.get(f"https://www.chinamoney.com.cn/ags/ms/cm-u-bk-fx/CrrHis?a=1&startDate={quote((date.today() - relativedelta(years=1) + timedelta(days=1)).strftime('%d %b %Y'))}&endDate={quote(date.today().strftime('%d %b %Y'))}&currency=ALL").json()['records']
		else:
			#Сайт не предоставляет актуальную информацию по каждому дню месяца
			data = requests.get(f"https://www.chinamoney.com.cn/ags/ms/cm-u-bk-fx/CrrHis?a=1&startDate={quote((date.today() - relativedelta(months=1)).strftime('%d %b %Y'))}&endDate={quote(date.today().strftime('%d %b %Y'))}&currency=ALL").json()['records']

		for num, currency in enumerate(today_data):
			cur_id = None
			ab = currency["code"]
			scale = 1
			rate = currency["rate"]

			for old_num, old_currency in enumerate(data):
				if ab == old_currency["pair"][4:]:
					if period == "1Y":
						old_rate = old_currency['ratelist'][11]
					else:
						old_rate = old_currency['ratelist'][0]
					break

			currencys.append(CurrencyData(source, cur_id, f"{ab}/CNY", scale, float(rate), float(old_rate)))

		return currencys


	def get_cfets2(self, period="1D"):
		currencys = []
		source = "China Foreign Exchange Trade System"

		today_data = requests.get("https://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/ccpr.json").json()['records']
	
		if period == "1W":
			data = requests.get(f"https://www.chinamoney.com.cn/ags/ms/cm-u-bk-ccpr/CcprHisNew?startDate={quote((date.today() - timedelta(weeks=1)).strftime('%d %b %Y'))}&endDate={quote((date.today() - timedelta(weeks=1)).strftime('%d %b %Y'))}").json()['records']
		#elif period == "1M":
		#	data = requests.get(f"https://api.nbrb.by/exrates/rates?ondate={date.today() - relativedelta(months=1)}&periodicity=0").json()
		#elif period == "1Y":
		#	data = requests.get(f"https://api.nbrb.by/exrates/rates?ondate={date.today() - relativedelta(years=1)}&periodicity=0").json()
		else:
			data = requests.get(f"https://www.chinamoney.com.cn/ags/ms/cm-u-bk-ccpr/CcprHisNew?startDate={quote((date.today() - timedelta(days=1)).strftime('%d %b %Y'))}&endDate={quote(date.today().strftime('%d %b %Y'))}").json()['records']
		
		for num, currency in enumerate(today_data):
			cur_id = currency['vrtCode']
			ab = "JPY/CNY" if currency["vrtEName"] == "100JPY/CNY" else currency["vrtEName"]
			scale = 100 if ab.startswith("100") else 1
			rate = currency["price"]

			if len(data) != 0:
				old_rate = data[0]['values'][num]
			else:
				old_rate = 0.00

			currencys.append(CurrencyData(source, cur_id, ab, scale, float(rate), float(old_rate)))

		return currencys

			
