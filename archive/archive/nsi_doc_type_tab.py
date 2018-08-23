#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis/archive/archive/nsi_doc_type.tab>
File            </mnt/defis/defis/archive/archive/nsi_doc_type_tab.py>
Description     <Resource module>
"""

import os.path
from ic import log
import ic
from ic.db import dbf
from ic.utils import ic_str
from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: /mnt/defis/defis/archive/archive/nsi_doc_type.tab

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 0, 1)

DBF_DEFAULT_ENCODE = 'cp866'

# Полное имя файла SPRAV.DBF (Справочник БАЛАНС+)
SPRAV_DBF_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'SPRAV.DBF') if os.path.dirname(__file__) else  '/mnt/defis/defis/archive/db/SPRAV.DBF'

SPRAV_TYPE_CODES = (161, 162, 163, 164, 165, 166, 167, 168, 169,
                    171, 172, 173, 174, 175, 176, 177, 178, 179,
                    282)

DOC_TYPE_DEFAULT_DATA = [('100', u'Приходные документы'),
                         ('1001000000000', u'Приход. Счет-фактура'),
                         ('1002000000000', u'Приход. ТОРГ12'),
                         ('1003000000000', u'Приход. Алкосправка'),
                         ('1004000000000', u'Приход. Товарно-транспортная накладная. ТТН'),
                         ('1005000000000', u'Приход. Акт выполненных работ/услуг'),
                         ('1006000000000', u'Приход. Приказ-распоряжение'),
                         ('1007000000000', u'Приход. Требование-накладная'),
                         ('1009000000000', u'Приход. Универсальный передаточный документ'),
                         ('200', u'Расходные документы'),
                         ('2001000000000', u'Расход. Счет-фактура'),
                         ('2002000000000', u'Расход. ТОРГ12'),
                         ('2003000000000', u'Расход. Алкосправка'),
                         ('2004000000000', u'Расход. Товарно-транспортная накладная. ТТН'),
                         ('2005000000000', u'Расход. Акт выполненных работ/услуг'),
                         ('2006000000000', u'Расход. Приказ-распоряжение'),
                         ('2007000000000', u'Расход. Требование-накладная'),
                         ('2008000000000', u'Расход. Акт списания'),
                         ('2009000000000', u'Расход. Универсальный передаточный документ'),
                         ('500', u'Юридические документы'),
                         ('5001000000000', u'Договор'),
                         ('5001100000000', u'Контракт'),
                         ('5001200000000', u'Уведомление о расторжении договора'),
                         ('5001300000000', u'Соглашение о расторжении договора'),
                         ('5002000000000', u'Дополнительное соглашение'),
                         ('5003000000000', u'Протокол разногласий'),
                         ('5003100000000', u'Протокол согласования'),
                         ('5004000000000', u'Доверенность'),
                         ('900', u'Прочие документы'),                         
                         ('9001000000000', u'Приложение'),
                         ('9002000000000', u'Спецификация'),
                         ('9003000000000', u'Заявка'),
                         ('9004000000000', u'Уведомление'),
                         ('9005000000000', u'Образец'),
                         ('9006000000000', u'Акт приема-передачи'),
                         ('9007000000000', u'Акт о приеме выполненных работ/услуг'),
                         ('9008000000000', u'Путевой лист'),
                         ('9009100000000', u'ОС1. Акт о приеме-передаче объекта основных средств (кроме зданий, сооружений)'),
                         ('9009300000000', u'ОС3. Акт о приеме-сдаче отремонтированных, реконструированных, модернизированных объектов основных средств'),
                         ('9009400000000', u'ОС4. Акт о списании объекта основных средств (кроме автотранспортных средств)'),
                         ]


class icNSIDocTypeTabManager(icmanagerinterface.icWidgetManager):
    """
    Менеджер таблицы справочника типов документов.
    """

    def onInit(self, evt):
        pass

    def set_default_data(self):
        """
        Установка значений справочника по умолчанию.
        Данные беруться по умолчанию.
        """
        tab = self.get_object()        
        # Очистить таблицу
        tab.clear()
        
        for record in DOC_TYPE_DEFAULT_DATA:
            new_cod = record[0]
            name = record[1]
            new_rec = dict(type='nsi_doc_type',
                           cod=new_cod, 
                           name=name)
            tab.add(**new_rec)
            
        
    def set_default_data_balans(self):
        """
        Установка значений справочника по умолчанию.
        Данные беруться из таблицы справочника БАЛАНС+.
        """
        if not os.path.exists(SPRAV_DBF_FILENAME):
            log.warning(u'Отсутствует файл <%s> для импорта данных справочника типов документов')
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
                    typ = ic_str.limit_len_text(record['TYP'], 3, '_')
                    if record['COD'].strip():
                        cod = unicode(record['COD'].strip(), DBF_DEFAULT_ENCODE)
                        cod = ic_str.limit_len_text(ic_str.rus2lat(cod), 10, '_')
                    else:
                        cod = u''
                    name = unicode(record['NAM'], DBF_DEFAULT_ENCODE)
                    try:
                        log.debug('NSI [%s : %s : %s]' % (typ, cod, name))
                    except UnicodeDecodeError:
                        log.debug('NSI [%s : %s]' % (typ, cod))
                    
                    new_cod = typ+cod
                    # Удаление на случай двойного описания 
                    # одного и того же в DBF файле
                    tab.del_where(tab.c.cod==new_cod)
                    new_rec = dict(type='nsi_doc_type',
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

manager_class = icNSIDocTypeTabManager
