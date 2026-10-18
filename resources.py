# -*- coding: utf-8 -*-

import os
import sys


BUNDLE_DIR_NAME = "app"


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base = os.path.join(sys._MEIPASS, BUNDLE_DIR_NAME)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, relative_path)
