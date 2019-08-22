#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс менеджера импорта документов БАЛАНС+ участка <Основные средства>.
"""

import os
import os.path
import datetime

import ic
from ic.log import log
from ic.dlg import ic_dlg
from ic.dlg import std_dlg
from ic.utils import filefunc
from ic.utils import filefunc
from ic.utils import smbfunc
from ic.db import dbf
from ic.utils import extfunc
from ic.engine import glob_functions

from . import import_manager

# Version
__version__ = (0, 0, 1, 1)

DT_TODAY = datetime.date.today()

# Игнорируемые документы по признаку в поле CODF
IGNORED_CODF = (u'CA', u'CH')

DBF_DEFAULT_ENCODE = 'cp866'


FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/',
                 )

ACT_BASE_FILENAME = 'OSN01.DCO'
SF_BASE_FILENAME = 'ROSN000.DCM'
BUH_BASE_FILENAME = 'XS01.DBS'
PL_BASE_FILENAME = 'PLO153.PLD'

ACT_DBF_FILENAME = 'OSN01.DBF'
SF_DBF_FILENAME = 'ROSN000.DBF'
BUH_DBF_FILENAME = 'XS01.DBF'
PL_DBF_FILENAME = 'PLO153.DBF'

OC1_COD = u'+О'
OC4_COD = u'-О'
OC3_COD = u'ИС'


class icOsnovnImportManager(import_manager.icBalansImportManager):
    """
    Класс менеджера импорта документов БАЛАНС+ участка <Основные средства>.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        import_manager.icBalansImportManager.__init__(self, *args, **kwargs)

        if not self.dbf_find_smb_urls:
            self.dbf_find_smb_urls = FIND_SMB_URLS

    def _import_docs(self):
        """
        Запуск импорта документов <Основные средства>.
        """
        log.debug(u'Запуск импорта документов <Основные средства>')
        dt_range = std_dlg.getDateRangeDlg(parent=self.pack_scan_panel, is_concrete_date=False)
        result = False
        if dt_range is not None:
            dt_begin, dt_end = dt_range
            if self.pack_scan_panel:
                self.pack_scan_panel.dt_begin = dt_begin
                self.pack_scan_panel.dt_end = dt_end
                
            log.debug(u'Диапазон дат <%s> : <%s>' % (dt_begin, dt_end))

            idx = std_dlg.getRadioChoiceMaxiDlg(parent=self.pack_scan_panel, title=u'Документ',
                                                label=u'Выберите тип документа:',
                                                choices=(u'Расходные СФ',
                                                         u'Расходные СФ согласно книге продаж',
                                                         u'Приходные СФ',
                                                         u'Приходные СФ согласно книге покупок',
                                                         u'Акты приема-передачи ОС',
                                                         u'Путевые листы'))
            if idx is None:
                # Нажата ОТМЕНА
                return False
            is_nds = idx in (1, 3)

            if self.pack_scan_panel:
                self.pack_scan_panel.clearDocList()
                
            for cur_year in range(dt_begin.year, dt_end.year+1):
                if idx == 4:
                    # Загрузка актов приема-передачи ОС
                    result = self._import_osn_docs(cur_year, ACT_BASE_FILENAME)
                elif idx == 5:
                    # Загрузка путевых листов
                    result = self._import_osn_docs(cur_year, PL_BASE_FILENAME)
                elif idx in (0, 1):
                    # Загрузка расходных СФ
                    result = self._import_osn_docs(cur_year, SF_BASE_FILENAME, is_nds=is_nds)
                    result = result and self._import_osn_docs(cur_year, BUH_BASE_FILENAME, is_nds=is_nds)
                elif idx in (2, 3):
                    # Загрузка приходных СФ
                    result = self._import_osn_docs(cur_year, BUH_BASE_FILENAME, is_nds=is_nds)
                else:
                    log.warning(u'Не обрабатываемый вид документа')
                    return False
                
            if self.pack_scan_panel:
                self.pack_scan_panel.refreshDocList(dt_begin=dt_begin,
                                                    dt_end=dt_end)
        return result

    def _import_osn_docs(self, cur_year, base_filename, is_nds=False):
        """
        Импорт документов из БАЛАНСа <Основные средства>.
            Выборка документов производиться за год.
        @param cur_year: Год выборки документов.
        @param base_filename: Наименование файла данных для загрузки.
        @param is_nds: Признак обязательного наличия НДС в документе.
        @return: True/False.
        """
        log.info(u'--- ЗАПУСК ИМПОРТА ДОКУМЕНТОВ <Основные средства> ---')

        if self.pack_doc is None:
            self.pack_doc = ic.metadata.archive.mtd.scan_document_pack.create()
            self.pack_doc.GetManager().init()
        
        result = self._import_os_docs_file(cur_year, base_filename, is_nds, self.pack_doc)
        return result

    def _import_os_docs_file(self, cur_year, base_filename, is_nds=True, pack_doc=None):
        """
        Импорт документов учета основных средств из БАЛАНСа.
            Выборка документов производиться за год.
        @param cur_year: Обрабатываемый год.
        @param base_filename: Наименование файла данных для загрузки.
        @param is_nds: Признак обязательного наличия НДС в документе.
        @param pack_doc: Объект документа пакетной обработки.
        """
        if base_filename is None:
            log.warning(u'Не определено имя файла данных <Основные средства>')
            return False
    
        if pack_doc is None:
            log.warning(u'Не определен объект документа пакетной обработки')
            return False
    
        src_filename = os.path.join(str(cur_year), 'FDOC', base_filename)
        
        # Сначала загрузить DBF из бекапа
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db')
        dst_filename = os.path.join(dst_path, src_filename)
        result = smbfunc.smb_download_file(FIND_SMB_URLS, filename=src_filename, 
                                           out_path=dst_path)
        if result:
            # Успешно загрузили
            dbf_filename = dst_filename.replace(os.path.splitext(base_filename)[1], '.DBF')
            if not filefunc.is_same_file_length(dst_filename, dbf_filename):
                # Это другой файл
                # Скопировать DCM в DBF
                if os.path.exists(dbf_filename):
                    os.remove(dbf_filename)
                filefunc.CopyFile(dst_filename, dbf_filename)
            
                self._load_os_from_dbf(dbf_filename, cur_year, is_nds)

            else:
                log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
            return True
        else:
            log.warning(u'Ошибка связи с SMB ресурсом бекапа')
        return False

    def _load_os_from_dbf(self, dbf_filename=None, cur_year=None, is_nds=None):
        """
        Загрузить данные пакета документов основных средств
            из DBF файла БАЛАНСа.
        @param dbf_filename: Полное имя загружаемого DBF файла.
        @param cur_year: Загружаемый год. Если None, то грузим текущий год.
        @param is_nds: Признак обязательного наличия НДС в документе.
        """
        if dbf_filename is None or not os.path.exists(dbf_filename):
            log.warning(u'Отсутствует файл <%s> для импорта данных' % dbf_filename)
            return
        if cur_year is None:
            cur_year = datetime.date.today().year

        base_filename = os.path.basename(dbf_filename)

        doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()
        
        # Запускаем загрузку
        transaction = tab.getDB().getTransaction(autoflush=False, autocommit=False)         

        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFile()
            dbf_tab.Open(dbf_filename)
            
            ic_dlg.icOpenProgressDlg(ic.getMainWin(),
                                     u'Пакетная обработка', u'Импорт данных',
                                     max_value=dbf_tab.getRecCount())
            i = 0
            record = dbf_tab.getRecDict()
            while not dbf_tab.EOF():                
                
                n_doc = None
                # По документу генерируем <Акты приема-передачи ОС>
                if base_filename == ACT_DBF_FILENAME:
                    new_rec = self._create_act(record, transaction, doc)
                    if new_rec:
                        n_doc = new_rec['n_doc']
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                # По документу генерируем <Путевые листы>
                elif base_filename == PL_DBF_FILENAME:
                    new_rec = self._create_putevoi_list(record, transaction, doc)
                    if new_rec:
                        n_doc = new_rec['n_doc']
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                # По документу генерируем <Расходные СФ>
                elif base_filename == SF_DBF_FILENAME:
                    new_rec = self._create_out_schet_factura(record, is_nds, transaction, doc)
                    if new_rec:
                        n_doc = new_rec['n_doc']
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                # По документу генерируем <Приходные СФ>
                elif base_filename == BUH_DBF_FILENAME:
                    new_rec = self._create_in_schet_factura_buh(record, is_nds, transaction, doc)
                    if new_rec:
                        n_doc = new_rec['n_doc']
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                    # ... и <Расходные СФ>
                    new_rec = self._create_out_schet_factura_buh(record, is_nds, transaction, doc)
                    if new_rec:
                        n_doc = new_rec['n_doc']
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                else:
                    log.warning(u'Не коррекное имя файла данных <%s>' % base_filename)
                    
                dbf_tab.Next()
                record = dbf_tab.getRecDict()
                
                i += 1
                if n_doc:
                    ic_dlg.icUpdateProgressDlg(i, u'Загружены данные документа № <%s>' % n_doc)

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
            log.fatal(u'Ошибка импорта данных документов основных средств БАЛАНС+')

    def _create_act(self, record, transaction=None, doc=None):
        """
        Создать акт приема-передачи ОС
            по данным документа БАЛАНСа <Основные средства>.
            Все дополнительные признаки-атрибуты фиксируются 
            в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @return: Словарь новой записи документа.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'ОС.АКТ.%s' % str_n_doc        
        
        # Инвентарный номер
        n_inv = unicode(record['PRIM_2'], DBF_DEFAULT_ENCODE)
        
        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None

        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        

        # По документу генерируем <акт приема-передачи>
        doc_name = u''
        if codf == OC1_COD:
            doc_typ = '9009100000000'
            doc_name = u'Акт о приеме-передаче объекта основных средств (кроме зданий, сооружений)'
        elif codf == OC3_COD:
            doc_typ = '9009300000000'
            doc_name = u'Акт о приеме-сдаче отремонтированных, реконструированных, модернизированных объектов основных средств'
        elif codf == OC4_COD:
            doc_typ = '9009400000000'
            doc_name = u'Акт о списании объекта основных средств (кроме автотранспортных средств)'
        else:
            log.service(u'Не обрабатываемый тип документа по коду <%s>' % codf)
            return None
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=DT_TODAY,
                       dt_state=DT_TODAY,
                       dt_oper=dt_oper,
                       n_obj=u'',
                       obj_date=None,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=doc_name,
                       doc_type=doc_typ,
                       c_agent=None,
                       entity='00001',
                       comment=comment,
                       tags=u'%s;Основные средства;Инв. № %s;;;%s;;;;' % (doc_name, n_inv, codf))
        return new_rec

    def _create_putevoi_list(self, record, transaction=None, doc=None):
        """
        Создать путевой лист ОС
            по данным документа БАЛАНСа <Основные средства>.
            Все дополнительные признаки-атрибуты фиксируются 
            в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @return: Словарь новой записи документа.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'ОС.ПЛ.%s' % str_n_doc        
        
        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None

        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        

        poluchatel_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)

        # ВНИМАНИЕ! В случае если не указан контрагент, 
        # мы указываем его наименование в тегах и все
        poluchatel_tag = poluchatel_name

        # По документу генерируем <путевой лист>
        doc_typ = '9008000000000'
        doc_name = u'Путевой лист'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=DT_TODAY,
                       dt_state=DT_TODAY,
                       dt_oper=dt_oper,
                       n_obj=u'',
                       obj_date=None,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=doc_name,
                       doc_type=doc_typ,
                       c_agent=None,
                       entity='00001',
                       comment=comment,
                       tags=u'%s;Основные средства;;;;%s;;;;%s' % (doc_name, codf, poluchatel_tag))
        return new_rec

    def _is_nds_in_schet_factura(self, is_on, cod_oper):
        """
        Проверка на есть ли в СФ НДС.
        @param is_on: Признак наличия НДС.
        @param cod_oper: Код операции БАЛАНС+.
        """
        return bool(cod_oper) and is_on

    def _create_out_schet_factura(self, record, is_nds=None, transaction=None, doc=None):
        """
        Создать расходную счет-фактуру ОС
            по данным документа БАЛАНСа <Основные средства>.
            Все дополнительные признаки-атрибуты фиксируются 
            в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_nds: Признак обязательного наличия НДС в документе.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'ОС.СФ.%s' % str_n_doc        
        
        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None

        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        

        alt_n_doc = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE).strip()
        dt_obj = record['DATE1']

        # По документу генерируем <акт приема-передачи>
        doc_name = u'Счет-фактура'
        doc_typ = '2001000000000'
        
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)

        cagent_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        cagent_balans_code = int(record['CODK'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
        cagent_cod = self.find_contragent_code(self.contragent_sprav, cagent_name, inn, kpp, cagent_balans_code)
                
        # ВНИМАНИЕ! В случае если не указан контрагент, 
        # мы указываем его наименование в тегах и все
        cagent_tag = u''
        if cagent_cod is None:
            cagent_tag = cagent_name
            log.service(u'Документ <%s>. Не определен контрагент <%s>' % (n_doc, cagent_tag))

        # Контроль на наличие НДС в документе
        cod_oper = int(record['CODOPER'])
        is_on = bool(str(record['PARM_OPER']).strip())
        is_nds_doc = self._is_nds_in_schet_factura(is_on, cod_oper)
        if is_nds and not is_nds_doc:
            log.service(u'Документ <%s>. Нет НДС' % n_doc)
            return None
        is_nds_doc_str = u'с НДС' if is_nds_doc else u'без НДС'

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=DT_TODAY,
                       dt_state=DT_TODAY,
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_obj,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=doc_name,
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'%s;Основные средства;;;;%s;;;%s;%s' % (doc_name, codf, is_nds_doc_str, cagent_tag))
        return new_rec

    def _create_in_schet_factura_buh(self, record, is_nds=None, transaction=None, doc=None):
        """
        Создать приходную счет-фактуру ОС
            по данным документа БАЛАНСа <Основные средства>.
            Все дополнительные признаки-атрибуты фиксируются 
            в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_nds: Признак обязательного наличия НДС в документе.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        # Создаемо только по определенным бух.справкам
        ssd = int(record['SSD'])
        ssk = int(record['SSK'])
        if ssd != 6816 and ssk != 809:
            return None
        
        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'ОС.СФ.%s' % str_n_doc        
        
        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None

        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        

        alt_n_doc = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE).strip()
        dt_obj = record['DATE1']

        # По документу генерируем <акт приема-передачи>
        doc_name = u'Счет-фактура'
        doc_typ = '1001000000000'
        
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)

        cagent_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        cagent_balans_code = int(record['CODK'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
        cagent_cod = self.find_contragent_code(self.contragent_sprav, cagent_name, inn, kpp, cagent_balans_code)
                
        # ВНИМАНИЕ! В случае если не указан контрагент, 
        # мы указываем его наименование в тегах и все
        cagent_tag = u''
        if cagent_cod is None:
            cagent_tag = cagent_name
            log.service(u'Документ <%s>. Не определен контрагент <%s>' % (n_doc, cagent_tag))

        # Контроль на наличие НДС в документе
        cod_oper = int(record['CODOPER'])
        is_nds_doc = self._is_nds_in_schet_factura(True, cod_oper)
        if is_nds and not is_nds_doc:
            log.service(u'Документ <%s>. Нет НДС' % n_doc)
            return None
        is_nds_doc_str = u'с НДС' if is_nds_doc else u'без НДС'

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=DT_TODAY,
                       dt_state=DT_TODAY,
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_obj,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=doc_name,
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'%s;Основные средства;;;;%s;;;%s;%s' % (doc_name, codf, is_nds_doc_str, cagent_tag))
        return new_rec

    def _create_out_schet_factura_buh(self, record, is_nds=None, transaction=None, doc=None):
        """
        Создать расходную счет-фактуру ОС
            по данным документа БАЛАНСа <Основные средства>.
            Все дополнительные признаки-атрибуты фиксируются 
            в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_nds: Признак обязательного наличия НДС в документе.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        # Создаем только по определенным бух.справкам
        ssd = int(record['SSD'])
        ssk = int(record['SSK'])
        if ssd != 809 and ssk != 6816:
            return None
        
        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'ОС.СФ.%s' % str_n_doc        
        
        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None

        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        

        alt_n_doc = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE).strip()
        dt_obj = record['DATE1']

        # По документу генерируем
        doc_name = u'Счет-фактура'
        doc_typ = '2001000000000'
        
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)

        cagent_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        cagent_balans_code = int(record['CODK'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
        cagent_cod = self.find_contragent_code(self.contragent_sprav, cagent_name, inn, kpp, cagent_balans_code)
                
        # ВНИМАНИЕ! В случае если не указан контрагент, 
        # мы указываем его наименование в тегах и все
        cagent_tag = u''
        if cagent_cod is None:
            cagent_tag = cagent_name
            log.service(u'Документ <%s>. Не определен контрагент <%s>' % (n_doc, cagent_tag))

        # Контроль на наличие НДС в документе
        cod_oper = int(record['CODOPER'])
        is_nds_doc = self._is_nds_in_schet_factura(True, cod_oper)
        if is_nds and not is_nds_doc:
            log.service(u'Документ <%s>. Нет НДС' % n_doc)
            return None
        is_nds_doc_str = u'с НДС' if is_nds_doc else u'без НДС'

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=DT_TODAY,
                       dt_state=DT_TODAY,
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_obj,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=doc_name,
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'%s;Основные средства;;;;%s;;;%s;%s' % (doc_name, codf, is_nds_doc_str, cagent_tag))
        return new_rec
