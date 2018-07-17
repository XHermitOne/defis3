#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    components  - пакет для работы с визуальными компонентами. Является
    продлджением пакета iccomponents для wxPython ver 2.4.1.2 под  Python 2.3b2.
    Создание нового пакета связвно с перекомпоновкой пакета wxPython (появился пакет wx).
"""

from . import ictestapp

from . import icfont

from . import icdatasetnavigator
from . import icdialog
from . import icframe
from . import icgrid
from . import icgriddataset
from . import iclistdataset
from . import icmulticolumnlist

from . import icscrolledwindow
from . import icscrolledpanel

from . import ictextfield

from . import icwxpanel
from . import icimport
from . import icobjectlink


__version__ = (1, 0, 3, 7)


#   Словарь модулей системных компонентов
icSysModulDict = {icdatasetnavigator.ic_class_spc['type']: icdatasetnavigator,
                  icdialog.ic_class_spc['type']: icdialog,
                  icframe.ic_class_spc['type']: icframe,
                  icgriddataset.ic_class_spc['type']: icgriddataset,
                  iclistdataset.ic_class_spc['type']: iclistdataset,
                  icmulticolumnlist.ic_class_spc['type']: icmulticolumnlist,
                    
                  icscrolledwindow.ic_class_spc['type']: icscrolledwindow,
                  icscrolledpanel.ic_class_spc['type']: icscrolledpanel,
                    
                  ictextfield.ic_class_spc['type']: ictextfield,
                  icwxpanel.ic_class_spc['type']: icwxpanel,
                  # 'Panel': icwxpanel,
                  'Window': icwxpanel,  # Для совместимости
                  icimport.ic_class_spc['type']: icimport,
                  icobjectlink.ic_class_spc['type']: icobjectlink,
                  }


def icGetSysModulDict():
    """
    Возвращает словарь модулей системных компонентов.
    """
    #   Словарь модулей системных компонентов
    global icSysModulDict
    from . import custom
    from . import sizers
    icSysModulDict = custom.icGetModulDict(icSysModulDict)
    icSysModulDict = sizers.icGetModulDict(icSysModulDict)
    
    return icSysModulDict
