#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Пакет системы управления запуском внешней
программы генераторов отчетов icReport.
"""

__version__ = (0, 0, 5, 3)

from . import report_manager

REPORT_MANAGER = report_manager.icReportManager()
