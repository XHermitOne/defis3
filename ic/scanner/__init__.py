#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Пакет системы управления запуском внешней
программы сканирования документов icScanner.
"""

__version__ = (0, 0, 1, 1)

from . import scanner_manager

SCANNER_MANAGER = scanner_manager.icScannerManager()
