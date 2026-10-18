# -*- coding: utf-8 -*-

from PySide2.QtCore import QObject, QTimer, Slot

from presenter.fetch_worker import CurrencyFetchWorker
from presenter.view_models import CurrencyRow


class MainPresenter(QObject):
    DEFAULT_PERIOD = "1D"

    COPY_COLUMNS = {
        "copy_pair": 0,
        "copy_rate": 1,
        "copy_change": 2,
        "copy_scale": 3,
        "copy_source": 4,
    }

    def __init__(self, view, currency, parent=None):
        super().__init__(parent)

        self.view = view
        self.currency = currency

        self.period = self.DEFAULT_PERIOD
        self.loaded_bank_data = {}
        self.worker = None

        self.view.period_changed.connect(self.on_period_changed)
        self.view.context_action_requested.connect(self.on_context_action)

    def start(self):
        QTimer.singleShot(500, lambda: self.start_background_fetch(self.DEFAULT_PERIOD))

    def start_background_fetch(self, period):
        self.view.set_period_enabled(False)
        self.worker = CurrencyFetchWorker(self.currency, period)
        self.worker.success_signal.connect(self.on_data_loaded)
        self.worker.error_signal.connect(self.on_load_error)
        self.worker.finished.connect(lambda: self.view.set_period_enabled(True))
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def reload(self):
        self.loaded_bank_data.clear()
        self.start_background_fetch(self.period)

    @Slot(str, list)
    def on_data_loaded(self, name, results):
        self.loaded_bank_data[name] = results

        rows = []
        for r in self.loaded_bank_data.values():
            for result in r:
                is_negative = result.int_percent < 0
                if is_negative:
                    change = str(result.percent) + "%"
                else:
                    change = "+" + str(result.percent) + "%"

                rows.append(CurrencyRow(
                    pair=str(result.abbreviation),
                    rate=str(result.rate),
                    change=change,
                    is_negative=is_negative,
                    scale=f"{result.scale} / {result.rate}",
                    source=str(result.source)
                ))

        self.view.show_rows(rows)

    @Slot(str)
    def on_load_error(self, error_message):
        self.view.show_notification(error_message, "error")

    @Slot(str)
    def on_period_changed(self, period):
        self.period = period
        self.view.set_table_headers(period)
        self.reload()

    @Slot(str, list)
    def on_context_action(self, action, row_values):
        if action in self.COPY_COLUMNS:
            self.view.copy_to_clipboard(row_values[self.COPY_COLUMNS[action]])

        elif action == "copy_row":
            pair, rate, change, scale, source = row_values
            self.view.copy_to_clipboard(f"{pair}\t{rate}\t{change}\t{scale}\t{source}")

        elif action == "update_data":
            self.reload()

        elif action == "statistic":
            row_count = sum(len(r) for r in self.loaded_bank_data.values())
            self.view.show_notification(
                f"Row count: {row_count}\nAvailable source number: {len(self.loaded_bank_data)}",
                "info"
            )
