#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/defis/NSI/NSI/nsi_data.tab>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/nsi_data.tab
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/nsi_data_tab.py
# Purpose:     Resource module.
#
# Author:      <...>
#
# Created:
# RCS-ID:      $Id: $
# Copyright:   (c)
# Licence:     <your licence>
# -----------------------------------------------------------------------------
### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

import os.path
import ic
from ic import log
from ic.interfaces import icmanagerinterface
from ic.db import dbf
from ic.utils import ic_str

#   Version
__version__ = (0,0,0,1)

DBF_DEFAULT_ENCODE = 'cp866'

SPRAV_DBF_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'SPRAV.DBF') if os.path.dirname(__file__) else  '/mnt/samba/defis/NSI/data/SPRAV.DBF'

SPRAV_TYPE_CODES = (161, 162, 163, 164, 165, 166, 167, 168, 169,
                    171, 172, 173, 174, 175, 176, 177, 178, 179,
                    282)


class icNSIDataTabManager(icmanagerinterface.icWidgetManager):
    
    def Init(self):
        pass

    def set_default_data(self):
        """
        Установить данные справочника по умолчанию.
        Данные беруться из таблицы справочника БАЛАНС+.
        """
        log.info(u'Start set_default_data')
        if not os.path.exists(SPRAV_DBF_FILENAME):
            log.warning(u'Отсутствует файл <%s> для импорта данных справочника типов документов' % SPRAV_DBF_FILENAME)
            return

        tab = self.get_object()        
        # Очистить таблицу
        tab.clear()

        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFile()
            dbf_tab.Open(SPRAV_DBF_FILENAME)
            record = dbf_tab.getRecDict()
            while not dbf_tab.EOF():
                if int(record['TYP']) in SPRAV_TYPE_CODES:
                    typ = ic_str.limit_len_text(record['TYP'], 3, '0')
                    if record['COD'].strip():
                        cod = unicode(record['COD'].strip(), DBF_DEFAULT_ENCODE)
                        cod = ic_str.limit_len_text(ic_str.rus2lat(cod), 10, '0')
                    else:
                        cod = u''
                    name = unicode(record['NAM'], DBF_DEFAULT_ENCODE)
                    try:
                        log.debug('NSI [%s : %s : %s]' % (typ, cod, name))
                    except UnicodeDecodeError:
                        log.debug('NSI [%s : %s]' % (typ, cod))
                    
                    new_cod = typ + cod
                    # Удаление на случай двойного описания 
                    # одного и того же в DBF файле
                    tab.del_where(tab.c.cod==new_cod)
                    new_rec = dict(type='NSITst',
                                   cod=new_cod, name=name)
                    tab.add(**new_rec)
                
                dbf_tab.Next()
                record = dbf_tab.getRecDict()
            dbf_tab.Close()
            dbf_tab = None
        except:
            if dbf_tab:
                dbf_tab.Close()
                dbf_tab = None
            log.fatal(u'Ошибка импорта данных справочника типов документов БАЛАНС+')
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icNSIDataTabManager