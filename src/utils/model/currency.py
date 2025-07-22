from datetime import date, timedelta
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
		return f"{(((self._rate - self._old_rate)/self._old_rate) * 100):.2}"

	@property
	def source(self):
		return self._source



class CurrencyAPIs:
	def get_nbrb(self):
		currencys = []
		source = "National Bank of the Republic of Belarus"

		today_data = requests.get("https://api.nbrb.by/exrates/rates?periodicity=0").json()
		yesterday_data = requests.get(f"https://api.nbrb.by/exrates/rates?ondate={date.today() - timedelta(days=1)}&periodicity=0").json()

		for num, currency in enumerate(today_data):
			cur_id = currency["Cur_ID"]
			ab = currency["Cur_Abbreviation"]
			scale = currency["Cur_Scale"]
			rate = currency["Cur_OfficialRate"]

			old_rate = yesterday_data[num]["Cur_OfficialRate"]

			currencys.append(CurrencyData(source, cur_id, f"{ab}/BYN", scale, rate, old_rate))

		return currencys
	
	
	
	

