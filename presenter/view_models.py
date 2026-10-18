# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class CurrencyRow:
    pair: str
    rate: str
    change: str
    is_negative: bool
    scale: str
    source: str
