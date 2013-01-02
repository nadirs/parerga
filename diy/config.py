# -*- set coding: utf-8 -*-

import os

# directories constants
PARERGA_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARERGA_ENTRY_DIR = os.path.join(PARERGA_ROOT_DIR, "p")
PARERGA_STATIC_DIR = os.path.join(PARERGA_ROOT_DIR, "static")
PARERGA_TEMPLATE_DIR = os.path.join(PARERGA_ROOT_DIR, "templates")

# database location
PARERGA_DB = os.path.join(PARERGA_ROOT_DIR, 'static', 'parerga.db')
