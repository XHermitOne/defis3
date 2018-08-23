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

# Формат автоматической генерации ИНН части кода если не указан
DEFAULT_INN_CODE_FMT = '%010d'

# Полное имя файла SPRAV.DBF (Справочник БАЛАНС+)
SPRAV_DBF_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'SPRVENT.DBF') if os.path.dirname(__file__) else  '/mnt/defis/defis3/archive/db/SPRVENT.DBF'


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
        if not os.path.exists(SPRAV_DBF_FILENAME):
            log.warning(u'Отсутствует файл <%s> для импорта данных справочника контрагентов' % SPRAV_DBF_FILENAME)
            return

        tab = self.get_object()        
        # Очистить таблицу
        tab.clear()
        
        transaction = tab.getDB().getTransaction(autoflush=False, autocommit=False)         

        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFile()
            dbf_tab.Open(SPRAV_DBF_FILENAME)
            
            ic_dlg.icOpenProgressDlg(ic.getMainWin(),
                                     u'Справочник контрагентов', u'Импорт данных',
                                     Max_=dbf_tab.getRecCount())
            i = 0
            i_code = 0
            record = dbf_tab.getRecDict()
            balans_code_cache = dict()
            while not dbf_tab.EOF():
                inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
                if inn == '0' or not inn.strip():
                    # ВНИМАНИЕ! У иностранных фирм может быть не указан ИНН
                    # но в справочнике они должны присутствовать
                    i_code += 1
                    inn = DEFAULT_INN_CODE_FMT % i_code
                kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
                # Учитываем что у ИП может отсутствовать КПП
                kpp = kpp.strip() if kpp and kpp.strip() and len(kpp) == 9 else DEFAULT_KPP_CODE
                
                cod = '-' * (12 - len(inn)) + inn + kpp
                
                name = unicode(record['NM_PLT'], DBF_DEFAULT_ENCODE).replace(u'\r', u'').replace(u'\n', u'')
                
                # Контроль на не корректный код
                if len(cod) != 21:
                    log.warning(u'Код <%s> контрагента <%s> [ИНН %s] [КПП %s] считается не корректным' % (cod, name, inn, kpp))
                    dbf_tab.Next()
                    record = dbf_tab.getRecDict()
                    i += 1
                    continue
                
                # name = unicode(record['NM_PLT'], DBF_DEFAULT_ENCODE).replace(u'\r', u'').replace(u'\n', u'')
                full_name = unicode(record['NM_PLTFULL'], DBF_DEFAULT_ENCODE).replace(u'\r', u'').replace(u'\n', u'')
                address = unicode(record['ADRP'], DBF_DEFAULT_ENCODE).replace(u'\r', u'').replace(u'\n', u'')
                phone = (unicode(record['TELEFON'], DBF_DEFAULT_ENCODE) if record['TELEFON'].strip() else u'') + u', ' + (unicode(record['A5'], DBF_DEFAULT_ENCODE) if record['A5'].strip() else u'')
                balans_code = int(record['CPLT'])
                
                try:
                    log.debug('NSI [%s : %s]' % (cod, name))
                except UnicodeDecodeError:
                    log.debug('NSI [%s]' % cod)
                    
                find_rec = tab.get_where_transact(tab.c.cod==cod, transaction=transaction)
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

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icNSIContrAgentTabManager