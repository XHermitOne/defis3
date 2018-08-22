#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Пакет системы управления запуском внешней
программы генераторов отчетов icReport.
"""

from . import report_manager

__version__ = (0, 1, 1, 1)

REPORT_MANAGER = report_manager.icReportManager()
