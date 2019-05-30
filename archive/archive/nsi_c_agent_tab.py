#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis3/archive/archive/nsi_c_agent.tab>
File            </mnt/defis/defis3/archive/archive/nsi_c_agent_tab.py>
Description     <Resource module>
"""

import os.path
from ic import log
import ic
from ic.db import dbf
from ic.utils import ic_str
from ic import ic_dlg
from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/nsi_c_agent.tab

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 1, 1)

DBF_DEFAULT_ENCODE = 'cp866'

# Код КПП для ИП отсутствует, подменяем на КПП по умолчанию
DEFAULT_KPP_CODE = '---------'
DEFAULT_PERSON_KPP_CODE = '+++++++++'

# Формат автоматической генерации ИНН части кода если не указан
DEFAULT_INN_CODE_FMT = '%010d'

# Полное имя файла SPRAV.DBF (Справочник БАЛАНС+)
COMPANY_SPRAV_DBF_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'SPRVENT.DBF') if os.path.dirname(__file__) else  '/mnt/defis/defis3/archive/db/SPRVENT.DBF'
PERSON_SPRAV_DBF_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'ZPL.DBF') if os.path.dirname(__file__) else  '/mnt/defis/defis3/archive/db/ZPL.DBF'




class icNSIContrAgentTabManager(icmanagerinterface.icWidgetManager):
    """
    Менеджер таблицы справочника контрагентов.
    """

    def onInit(self, evt):
        pass

    def set_default_data(self):
        """
        Установка значений справочника по умолчанию.
        Данные беруться из таблицы справочника БАЛАНС+.
        """
        self.set_company_default_data(True, COMPANY_SPRAV_DBF_FILENAME)
        self.set_person_default_data(False, PERSON_SPRAV_DBF_FILENAME)

    def set_company_default_data(self, bClear=False, dbf_filename=None):
        """
        Установка значений справочника по умолчанию.  Справочник предприятий.
        Данные беруться из таблицы справочника БАЛАНС+.
        """
        if not os.path.exists(dbf_filename):
            log.warning(u'Отсутствует файл <%s> для импорта данных справочника контрагентов' % dbf_filename)
            return

        tab = self.get_object()
        # Очистить таблицу
        if bClear:
            tab.clear()

        transaction = tab.getDB().getTransaction(autoflush=False, autocommit=False)

        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFileReadOnly()
            dbf_tab.Open(dbf_filename)

            ic_dlg.icOpenProgressDlg(ic.getMainWin(),
                                     u'Справочник контрагентов', u'Импорт данных',
                                     Max_=dbf_tab.getRecCount())
            i = 0
            i_code = 0
            record = dbf_tab.getRecDict()
            balans_code_cache = dict()
            while not dbf_tab.EOF():
                inn = str(record['INN'])
                if inn == '0' or not inn.strip():
                    # ВНИМАНИЕ! У иностранных фирм может быть не указан ИНН
                    # но в справочнике они должны присутствовать
                    i_code += 1
                    inn = DEFAULT_INN_CODE_FMT % i_code
                kpp = str(record['KPP'])
                # Учитываем что у ИП может отсутствовать КПП
                kpp = kpp.strip() if kpp and kpp.strip() and len(kpp) == 9 else DEFAULT_KPP_CODE

                cod = '-' * (12 - len(inn)) + inn + kpp

                name = str(record['NM_PLT']).replace(u'\r', u'').replace(u'\n', u'')

                # Контроль на не корректный код
                if len(cod) != 21:
                    log.warning(u'Код <%s> контрагента <%s> [ИНН %s] [КПП %s] считается не корректным' % (cod, name,
                                                                                                          inn, kpp))
                    dbf_tab.Next()
                    record = dbf_tab.getRecDict()
                    i += 1
                    continue

                # name = str(record['NM_PLT']).replace(u'\r', u'').replace(u'\n', u'')
                full_name = str(record['NM_PLTFULL']).replace(u'\r', u'').replace(u'\n', u'')
                address = str(record['ADRP']).replace(u'\r', u'').replace(u'\n', u'')
                phone = (str(record['TELEFON']) if record['TELEFON'].strip() else u'') + u', ' + (str(record['A5']) if record['A5'].strip() else u'')
                balans_code = int(record['CPLT'])

                try:
                    log.debug('NSI [%s : %s]' % (cod, name))
                except UnicodeDecodeError:
                    log.debug('NSI [%s]' % cod)

                find_rec = tab.get_where_transact(tab.c.cod == cod, transaction=transaction)
                not_new = find_rec and find_rec.rowcount

                if not not_new:
                    # Нет такого предприятия
                    new_rec = dict(type='nsi_c_agent',
                                   cod=cod, name=name,
                                   inn=inn, kpp=kpp,
                                   full_name=full_name,
                                   address=address, phone=phone,
                                   s1='<%d>' % balans_code)

                    tab.add_rec_transact(rec=new_rec, transaction=transaction)
                    balans_code_cache[cod] = [balans_code]
                else:
                    # Такое предприятие уже есть
                    if cod in balans_code_cache:
                        if balans_code not in balans_code_cache[cod]:
                            balans_code_cache[cod].append(balans_code)
                    else:
                        balans_code_cache[cod] = [balans_code]

                    prev_rec = dict(type='nsi_c_agent',
                                    cod=cod, name=name,
                                    inn=inn, kpp=kpp,
                                    full_name=full_name,
                                    address=address, phone=phone,
                                    s1=';'.join(['<%d>' % c for c in balans_code_cache[cod]]))
                    tab.update_rec_transact(find_rec.first().id, prev_rec, transaction=transaction)

                dbf_tab.Next()
                record = dbf_tab.getRecDict()

                i += 1
                ic_dlg.icUpdateProgressDlg(i, u'Загружены данные <%s>' % name)

            dbf_tab.Close()
            dbf_tab = None

            ic_dlg.icUpdateProgressDlg(i, u'')
            ic_dlg.icCloseProgressDlg()

            # Подтвердить транзакцию
            transaction.commit()
        except:
            # Отменить транзакцию
            transaction.rollback()

            ic_dlg.icCloseProgressDlg()
            if dbf_tab:
                dbf_tab.Close()
                dbf_tab = None
            log.fatal(u'Ошибка импорта данных справочника контрагентов БАЛАНС+')

    def set_person_default_data(self, bClear=False, dbf_filename=None):
        """
        Установка значений справочника по умолчанию. Справочник физлиц.
        Данные беруться из таблицы справочника БАЛАНС+.
        """
        if not os.path.exists(dbf_filename):
            log.warning(u'Отсутствует файл <%s> для импорта данных справочника физ.лиц' % dbf_filename)
            return

        tab = self.get_object()
        # Очистить таблицу
        if bClear:
            tab.clear()

        transaction = tab.getDB().getTransaction(autoflush=False, autocommit=False)

        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFileReadOnly()
            dbf_tab.Open(dbf_filename)

            ic_dlg.icOpenProgressDlg(ic.getMainWin(),
                                     u'Справочник физических лиц', u'Импорт данных',
                                     Max_=dbf_tab.getRecCount())
            i = 0
            i_code = 0
            record = dbf_tab.getRecDict()
            balans_code_cache = dict()
            while not dbf_tab.EOF():
                name = str(record['NAMD']).replace(u'\r', u'').replace(u'\n', u'')
                inn = str(record['INN'])
                if inn == '0' or not inn.strip():
                    # ВНИМАНИЕ! Если у физических лиц не указан ИНН
                    # то пропускаем их
                    log.warning(u'У физического лица <%s> не указан ИНН. В справочник не добавлен' % name)
                    dbf_tab.Next()
                    record = dbf_tab.getRecDict()
                    i += 1
                    continue

                # Учитываем что у Физического лица отсутствует КПП
                kpp = DEFAULT_PERSON_KPP_CODE

                cod = '-' * (12 - len(inn)) + inn + kpp

                # Контроль на не корректный код
                if len(cod) != 21:
                    log.warning(u'Код <%s> физического лица <%s> [ИНН %s] [КПП %s] считается не корректным' % (cod,
                                                                                                               name,
                                                                                                               inn,
                                                                                                               kpp))
                    dbf_tab.Next()
                    record = dbf_tab.getRecDict()
                    i += 1
                    continue

                full_name = ';'.join([name, str(record['DOLGN']), str(record['SEX'])])
                address = ';'.join([str(record['POST']),
                                    str(record['AREA']),
                                    str(record['VCITY'])+'. '+str(record['CITY']),
                                    str(record['VSTREET'])+'. '+str(record['STREET']),
                                    str(record['HOUSE']), str(record['ROOM'])])
                phone = u''
                balans_code = int(record['CODK'])

                try:
                    log.debug('NSI [%s : %s]' % (cod, name))
                except UnicodeDecodeError:
                    log.debug('NSI [%s]' % cod)

                find_rec = tab.get_where_transact(tab.c.cod == cod, transaction=transaction)
                not_new = find_rec and find_rec.rowcount

                if not not_new:
                    # Нет такого физ лица
                    new_rec = dict(type='nsi_c_agent',
                                   cod=cod, name=name,
                                   inn=inn, kpp=u'',
                                   full_name=full_name,
                                   address=address, phone=phone,
                                   s1='<%d>' % balans_code)

                    tab.add_rec_transact(rec=new_rec, transaction=transaction)
                    balans_code_cache[cod] = [balans_code]
                else:
                    # Такое физ лицо уже есть
                    if cod in balans_code_cache:
                        if balans_code not in balans_code_cache[cod]:
                            balans_code_cache[cod].append(balans_code)
                    else:
                        balans_code_cache[cod] = [balans_code]

                    prev_rec = dict(type='nsi_c_agent',
                                    cod=cod, name=name,
                                    inn=inn, kpp=u'',
                                    full_name=full_name,
                                    address=address, phone=phone,
                                    s1=';'.join(['<%d>' % c for c in balans_code_cache[cod]]))
                    tab.update_rec_transact(find_rec.first().id, prev_rec, transaction=transaction)

                dbf_tab.Next()
                record = dbf_tab.getRecDict()

                i += 1
                ic_dlg.icUpdateProgressDlg(i, u'Загружены данные <%s>' % name)

            dbf_tab.Close()
            dbf_tab = None

            ic_dlg.icUpdateProgressDlg(i, u'')
            ic_dlg.icCloseProgressDlg()

            # Подтвердить транзакцию
            transaction.commit()
        except:
            # Отменить транзакцию
            transaction.rollback()

            ic_dlg.icCloseProgressDlg()
            if dbf_tab:
                dbf_tab.Close()
                dbf_tab = None
            log.fatal(u'Ошибка импорта данных справочника контрагентов БАЛАНС+')

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK


manager_class = icNSIContrAgentTabManager
