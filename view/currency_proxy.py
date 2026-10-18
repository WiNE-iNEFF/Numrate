# -*- coding: utf-8 -*-

from PySide2.QtCore import QSortFilterProxyModel


class CurrencyProxy(QSortFilterProxyModel):
    def lessThan(self, left, right):
        if left.column() in [1, 2]:
            try:
                left_value = float(str(left.data()).replace("+", ""))
                right_value = float(str(right.data()).replace("+", ""))

                return left_value < right_value

            except Exception:
                pass

        return super().lessThan(left, right)
