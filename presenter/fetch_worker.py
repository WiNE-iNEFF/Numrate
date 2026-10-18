# -*- coding: utf-8 -*-

from PySide2.QtCore import QThread, Signal


class CurrencyFetchWorker(QThread):
    success_signal = Signal(str, list)
    error_signal = Signal(str)

    def __init__(self, api_instance, period="1D"):
        super().__init__()
        self.api = api_instance
        self.period = period

    def run(self):
        try:
            nbrb_data = self.api.get_nbrb(self.period)
            self.success_signal.emit("National Bank of the Republic of Belarus", nbrb_data)
        except Exception as e:
            self.error_signal.emit(f"Error with loading information from:\n\"National Bank of the Republic of Belarus\"\n{str(e)}")

        try:
            cbr_data = self.api.get_cbr(self.period)
            self.success_signal.emit("The Central Bank of the Russian Federation", cbr_data)
        except Exception as e:
            self.error_signal.emit(f"Error with loading information from:\n\"The Central Bank of the Russian Federation\"\n{str(e)}")

        try:
            cfets_data = self.api.get_cfets(self.period)
            self.success_signal.emit("China Foreign Exchange Trade System (National Interbank Funding Center)", cfets_data)
        except Exception as e:
            self.error_signal.emit(f"Error with loading information from:\n\"China Foreign Exchange Trade System\"\n{str(e)}")

        try:
            cfets2_data = self.api.get_cfets2(self.period)
            self.success_signal.emit("China Foreign Exchange Trade System (National Interbank Funding Center) Reference Rate", cfets2_data)
        except Exception as e:
            self.error_signal.emit(f"Error with loading information from:\n\"China Foreign Exchange Trade System\"\n{str(e)}")
