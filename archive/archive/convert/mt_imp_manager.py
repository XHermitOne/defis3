#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс менеджера импорта документов БАЛАНС+ участка <Материалы>.
"""

import os
import os.path
import datetime

import ic
from ic.log import log
from ic.dlg import dlgfunc
from ic.dlg import std_dlg
from ic.utils import filefunc
from ic.utils import filefunc
from ic.utils import smbfunc
from ic.utils import strfunc
from ic.db import dbf
from ic.utils import extfunc
from ic.engine import glob_functions

from . import import_manager

# Version
__version__ = (0, 0, 1, 1)

# Игнорируемые документы по признаку в поле CODF
# ВП - внутреннее перемещение
IGNORED_CODF = (u'ВП', u'АС')

DBF_DEFAULT_ENCODE = 'cp866'


FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/',
                 )

COD_OPER_NDS = (1, 19, 20, 26, 18, 34)


class icMaterialImportManager(import_manager.icBalansImportManager):
    """
    Класс менеджера импорта документов БАЛАНС+ участка <Материалы>.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        import_manager.icBalansImportManager.__init__(self, *args, **kwargs)

        if not self.dbf_find_smb_urls:
            self.dbf_find_smb_urls = FIND_SMB_URLS
            
        self._9184_ndocs = list()

    def _get_input_doc_warehouses(self, dt):
        """
        Список номеров складов импортируемых для книги покупок.
        """
        month = dt.month
        start = 41 + dt.year - 2017
        if month >= 11:
            start += 1
        return (start, 55, 77, 136, 179, 180)

    def _get_output_doc_warehouses(self, dt):
        """
        Список номеров складов импортируемых для книги продаж.
        """
        month = dt.month
        start = 41 + dt.year - 2017
        if month >= 11:
            start += 1
        return (start, 110, 137, 143, 175, 177, 159)
        
    def _import_docs(self):
        """
        Запуск импорта документов <Материалы>.
        """
        log.debug(u'Запуск импорта документов <Материалы>')
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
                                                choices=(u'Расходный документ',
                                                         u'Счет-фактуры согласно книге продаж',
                                                         u'Приходный документ',
                                                         u'Счет-фактуры согласно книге покупок',
                                                         ))
            if idx is None:
                # Нажата ОТМЕНА
                return False
            is_input = idx in (2, 3)
            is_kniga_pokupok = idx == 3
            is_kniga_prodaj = idx == 1

            if not is_kniga_pokupok and not is_kniga_prodaj:
                n_warehouse = std_dlg.getIntegerDlg(parent=self.pack_scan_panel, title=u'Склад',
                                                    label=u'Введите номер склада:',
                                                    min_value=1, max_value=999)
                if n_warehouse is None:
                    # Нажата ОТМЕНА
                    return False
                n_warehouses = [n_warehouse]
                is_nds = False
            elif is_kniga_pokupok:
                input_doc_warehouses = self._get_input_doc_warehouses(dt_begin)
                choices = [u'%d Склад' % n_warehouse for n_warehouse in input_doc_warehouses]
                n_warehouses = std_dlg.getCheckBoxDlg(parent=self.pack_scan_panel, 
                                                      title=u'Склад',
                                                      label=u'Выберите номера складов:',
                                                      choices=choices)
                if n_warehouses is None:
                    # Нажата ОТМЕНА
                    return False
                n_warehouses = [input_doc_warehouses[i] for i, n in enumerate(n_warehouses) if n]
                is_nds = True
            elif is_kniga_prodaj:
                output_doc_warehouses = self._get_output_doc_warehouses(dt_begin)
                choices = [u'%d Склад' % n_warehouse for n_warehouse in output_doc_warehouses]
                n_warehouses = std_dlg.getCheckBoxDlg(parent=self.pack_scan_panel, 
                                                      title=u'Склад',
                                                      label=u'Выберите номера складов:',
                                                      choices=choices)
                if n_warehouses is None:
                    # Нажата ОТМЕНА
                    return False
                n_warehouses = [output_doc_warehouses[i] for i, n in enumerate(n_warehouses) if n]
                is_nds = True
            else:
                log.warning(u'Не обрабатываемый тип документов')
                return False

            if self.pack_scan_panel:
                self.pack_scan_panel.clearDocList()

            for cur_year in range(dt_begin.year, dt_end.year+1):
                for n_warehouse in n_warehouses:
                    result = self._import_material_docs(cur_year, n_warehouse=n_warehouse, 
                                                        is_input=is_input, 
                                                        is_nds=is_nds)
            if self.pack_scan_panel:
                self.pack_scan_panel.refreshDocList(dt_begin=dt_begin,
                                                    dt_end=dt_end)
        return result

    def _import_material_docs(self, cur_year, n_warehouse, is_input=False, 
                              is_nds=False):
        """
        Импорт документов из БАЛАНСа <Материалы>.
            Выборка документов производиться за год.
        @param cur_year: Год выборки документов.
        @param is_input: Признак приходного документа.
        @param n_warehouse: Номер склада.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        @return: True/False.
        """
        log.info(u'--- ЗАПУСК ИМПОРТА ДОКУМЕНТОВ <МАТЕРИАЛЫ> ---')

        if self.pack_doc is None:
            self.pack_doc = ic.metadata.archive.mtd.scan_document_pack.create()
            # self.pack_doc.GetManager().init()
        
        result1 = self._import_mt_docs_file(cur_year, n_warehouse, is_input, 
                                           self.pack_doc, is_nds=is_nds)
        result2 = self._import_mt_ext_file(cur_year, n_warehouse, is_input, 
                                           self.pack_doc, is_nds=is_nds)
        return result1 and result2

    def _import_mt_docs_file(self, cur_year, n_warehouse, is_input=True, 
                             pack_doc=None, is_nds=False):
        """
        Импорт документов учета материалов из БАЛАНСа.
            Выборка документов производиться за год.
        @param cur_year: Обрабатываемый год.
        @param n_warehouse: Номер склада.
        @param is_input: Признак приходного документа.
        @param pack_doc: Объект документа пакетной обработки.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        """
        if n_warehouse is None:
            log.warning(u'Не определен номер склада при импорте документов <Материалы>')
            return False
    
        if pack_doc is None:
            log.warning(u'Не определен объект документа пакетной обработки')
            return False
    
        # Загружаем спецификацию для определения номеров документов 
        # с проводками по 91-84 счету
        base_filename = 'MI%03d.DCS' % n_warehouse if is_input else 'MO%03d.DCS' % n_warehouse
        src_filename = os.path.join(str(cur_year), 'FDOC', base_filename)
        
        # Сначала загрузить DBF из бекапа
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db')
        dst_filename = os.path.join(dst_path, src_filename)
        result = smbfunc.smb_download_file(FIND_SMB_URLS, filename=src_filename, 
                                           out_path=dst_path)
        if result:
            # Успешно загрузили
            dbf_filename = dst_filename.replace('.DCS', 'S.DBF')
            if not filefunc.is_same_file_length(dst_filename, dbf_filename):
                # Это другой файл
                # Скопировать DCS в DBF
                if os.path.exists(dbf_filename):
                    os.remove(dbf_filename)
                filefunc.CopyFile(dst_filename, dbf_filename)
            else:
                log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
            self._load_ndocs_spec_from_dbf(dbf_filename)
        else:
            log.warning(u'Ошибка связи с SMB ресурсом бекапа')
            
        base_filename = 'MI%03d.DCM' % n_warehouse if is_input else 'MO%03d.DCM' % n_warehouse
        src_filename = os.path.join(str(cur_year), 'FDOC', base_filename)
        
        # Сначала загрузить DBF из бекапа
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db')
        dst_filename = os.path.join(dst_path, src_filename)
        result = smbfunc.smb_download_file(FIND_SMB_URLS, filename=src_filename, 
                                           out_path=dst_path)
        if result:
            # Успешно загрузили
            dbf_filename = dst_filename.replace('.DCM', '.DBF')
            if not filefunc.is_same_file_length(dst_filename, dbf_filename):
                # Это другой файл
                # Скопировать DCM в DBF
                if os.path.exists(dbf_filename):
                    os.remove(dbf_filename)
                filefunc.CopyFile(dst_filename, dbf_filename)
            
                self._load_mt_from_dbf(dbf_filename, cur_year, is_input, 
                                       is_nds=is_nds)
            else:
                log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
            return True
        else:
            log.warning(u'Ошибка связи с SMB ресурсом бекапа')
        return False

    def _import_mt_ext_file(self, cur_year, n_warehouse, is_input=True, 
                            pack_doc=None, is_nds=False):
        """
        Импорт документов востановления НДС из БАЛАНСа.
            Выборка документов производиться за год.
        @param cur_year: Обрабатываемый год.
        @param n_warehouse: Номер склада.
        @param is_input: Признак приходного документа.
        @param pack_doc: Объект документа пакетной обработки.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        """
        if pack_doc is None:
            log.warning(u'Не определен объект документа пакетной обработки')
            return False
    
        base_filename = 'BS6068.DBS'
        src_filename = os.path.join(str(cur_year), 'FDOC', base_filename)
        
        # Сначала загрузить DBF из бекапа
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db')
        dst_filename = os.path.join(dst_path, src_filename)
        result = smbfunc.smb_download_file(FIND_SMB_URLS, filename=src_filename, 
                                           out_path=dst_path)
        if result:
            # Успешно загрузили
            dbf_filename = dst_filename.replace('.DBS', '.DBF')
            if not filefunc.is_same_file_length(dst_filename, dbf_filename):
                # Это другой файл
                # Скопировать DBS в DBF
                if os.path.exists(dbf_filename):
                    os.remove(dbf_filename)
                filefunc.CopyFile(dst_filename, dbf_filename)
            
                self._load_mt_from_dbf(dbf_filename, cur_year, is_input, 
                                       is_nds=is_nds, is_vostanovl_nds=True)
            else:
                log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
            return True
        else:
            log.warning(u'Ошибка связи с SMB ресурсом бекапа')
        return False

    def _load_mt_from_dbf(self, dbf_filename=None, cur_year=None, is_input=None, 
                          is_nds=False, is_vostanovl_nds=False):
        """
        Загрузить данные пакета документов материалов (счет-фактур и ТОРГ12) 
            из DBF файла БАЛАНСа.
        @param dbf_filename: Полное имя загружаемого DBF файла.
        @param cur_year: Загружаемый год. Если None, то грузим текущий год.
        @param is_input: Признак приходного документа.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        @param is_vostanovl_nds: Признак загрузки СФ востановления НДС.
        """
        if dbf_filename is None or not os.path.exists(dbf_filename):
            log.warning(u'Отсутствует файл <%s> для импорта данных' % dbf_filename)
            return
        if cur_year is None:
            cur_year = datetime.date.today().year
        
        doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()
        
        # Запускаем загрузку
        transaction = tab.getDB().getTransaction(autoflush=False, autocommit=False)         

        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFile()
            dbf_tab.Open(dbf_filename)
            
            dlgfunc.openProgressDlg(ic.getMainWin(),
                                     u'Пакетная обработка', u'Импорт данных',
                                    max_value=dbf_tab.getRecCount())
            i = 0
            record = dbf_tab.getRecDict()
            while not dbf_tab.EOF():                
                n_doc = None
                # По документу генерируем <счет-фактуры>
                new_rec = self._create_schet_factura(record, transaction, 
                                                     is_input, doc, is_nds=is_nds)
                if new_rec:
                    n_doc = new_rec['n_doc']
                    tab.add_rec_transact(rec=new_rec, transaction=transaction)

                if not is_vostanovl_nds:
                    # По документу генерируем <ТОРГ12>
                    new_rec = self._create_torg12(record, transaction, is_input, doc)
                    if new_rec:
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)

                    # По документу генерируем <Приложения>
                    new_rec = self._create_priloj(record, transaction, is_input, doc)
                    if new_rec:
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
               
                dbf_tab.Next()
                record = dbf_tab.getRecDict()
                
                i += 1
                if n_doc:
                    dlgfunc.updateProgressDlg(i, u'Загружены данные документа № <%s>' % n_doc)

            dbf_tab.Close()
            dbf_tab = None
            
            dlgfunc.updateProgressDlg(i, u'')
            dlgfunc.closeProgressDlg()

            # Подтвердить транзакцию
            transaction.commit()
        except:
            # Отменить транзакцию
            transaction.rollback()
            
            dlgfunc.closeProgressDlg()
            if dbf_tab:
                dbf_tab.Close()
                dbf_tab = None
            log.fatal(u'Ошибка импорта данных документов материалов БАЛАНС+')

    def _is_nds_in_schet_factura(self, is_on, cod_oper):
        """
        Проверка на есть ли в СФ НДС.
        @param is_on: Признак наличия НДС.
        @param cod_oper: Код операции БАЛАНС+.
        """
        # return (cod_oper == 1 and is_on) or cod_oper in COD_OPER_NDS[1:]
        return bool(cod_oper)

    def _is_9184(self, record):
        """
        Определить является ли указанный документ документом с проводками по счету 91-84.
        @param record: Словарь записи DBF файла.
        @return: True-да есть проводка по счету 91-84 / False - нет.
        """
        # log.debug(u'91-84: %s' % str(self._9184_ndocs))
        n_doc = strfunc.toUnicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        return n_doc in self._9184_ndocs
        
    def _create_schet_factura(self, record, transaction=None, 
                                 is_input=False, doc=None, is_nds=False):
        """
        Создать счет-фактуру по данным документа БАЛАНСа <Материалы>.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        alt_n_doc = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE).strip()
        n_warehouse = int(record['PODR'])
        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()        
        n_doc = u'МТ.СФ.%s/%s' % (str_n_doc, n_warehouse)
        cod_oper = int(record['CODOPER'])
        is_on = bool(str(record['PARM_OPER']).strip())
        
        if not alt_n_doc and is_input:
            # Для приходных документов
            # Если не определен номер СФ, то не генерировать документ
            log.service(u'Документ <%s>. Не определен номер счет-фактуры в документе' % n_doc)
            return None
        elif not alt_n_doc and not is_input:
            # Для расходных документов
            alt_n_doc = u'%s/%s' % (str_n_doc, n_warehouse)

        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None
        elif is_input == True and codf in (u'СФ', u'СТ'):
            return None
        elif is_input == False and codf in (u'ПФ', u'КП'):
            return None

        # Проверка на наличие проводок по счету 91-84
        if is_input and is_nds and self._is_9184(record):
            log.service(u'Документ <%s>. Документ с проводками по счету 91-84.' % n_doc)
            return None            
        
        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        dt_obj = record['DATE1']
        
        platelchik_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        platelchik_balans_code = int(record['CODK'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
        
        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        
                
        cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, inn, kpp, platelchik_balans_code)
                
        # ВНИМАНИЕ! В случае если не указан контрагент, 
        # мы указываем его наименование в тегах и все
        cagent_tag = u''
        if cagent_cod is None:
            cagent_tag = platelchik_name
            log.service(u'Документ <%s>. Не определен контрагент <%s>' % (n_doc, cagent_tag))

        # Контроль на наличие НДС в документе для КНИГИ ПОКУПОК
        is_nds_doc = self._is_nds_in_schet_factura(is_on, cod_oper)
        if is_nds and is_input and not is_nds_doc:
            log.service(u'Документ <%s>. Нет НДС' % n_doc)
            return None
                    
        # По документу генерируем <счет-фактуры>
        doc_typ = '2001000000000' if not is_input else '1001000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                             tab, transaction)
                    
        warehouse_tag = u'Склад %d' % n_warehouse
        
        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        is_nds_doc_str = u'с НДС' if is_nds_doc else u'без НДС'

        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=datetime.date.today(),
                       dt_state=datetime.date.today(),
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_obj,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=u'Счет-фактура',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'Счет-фактура;Материалы;Код операции %02d;%s;%s;%s;;;%s;%s' % (cod_oper, warehouse_tag, cagent_tag, codf, is_nds_doc_str, alt_n_doc))
        return new_rec

    def _create_torg12(self, record, transaction=None, 
                       is_input=False, doc=None):
        """
        Создать ТОРГ12 по данным документа БАЛАНСа <Материалы>.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        alt_n_doc = unicode(record['NTORG12'], DBF_DEFAULT_ENCODE).strip()

        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None
        elif is_input == True and codf in (u'СФ', ):
            return None
        elif is_input == False and codf in (u'ПФ', ):
            return None
        
        n_warehouse = int(record['PODR'])        
        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'МТ.ТОРГ12.%s/%s' % (str_n_doc, n_warehouse)
        if not alt_n_doc:
            # Если не определен номер, то cгенерировать
            alt_n_doc = u'%s от %s' % (n_doc, record['DTDOC'])
        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        dt_obj = record['DATE1']
        if not dt_obj:
            # Если не указывается дата документа явно, то подставляем
            # в качестве даты дату счет фактуры
            dt_obj = dt_doc
            
        platelchik_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        platelchik_balans_code = int(record['CODK'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
        
        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        
                
        cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, inn, kpp, platelchik_balans_code)
                
        # ВНИМАНИЕ! В случае если не указан контрагент, 
        # мы указываем его наименование в тегах и все
        cagent_tag = u''
        if cagent_cod is None:
            cagent_tag = platelchik_name
            log.service(u'Документ <%s>. Не определен контрагент <%s>' % (n_doc, cagent_tag))
                    
        # По документу генерируем <акт ваполненных работ>
        doc_typ = '2002000000000' if not is_input else '1002000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)
                    
        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        
                    
        warehouse_tag = u'Склад %d' % n_warehouse
        
        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=datetime.date.today(),
                       dt_state=datetime.date.today(),
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_obj,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=u'Торг12',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'ТОРГ12;Материалы;%s;%s;;%s;;;;%s' % (warehouse_tag, cagent_tag, codf, alt_n_doc))
        return new_rec

    def _create_priloj(self, record, transaction=None, 
                          is_input=False, doc=None):
        """
        Создать приложение по данным документа БАЛАНСа <Материалы>.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        if not is_input:
            # Для расходных документов не надо создавать приложение
            log.warning(u'Для расходных документов приложение не создается')
            return None
        
        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None
        elif is_input == True and codf in (u'СФ', ):
            return None
        elif is_input == False and codf in (u'ПФ', ):
            return None
        
        n_warehouse = int(record['PODR'])        
        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'МТ.ПРИЛ.%s/%s' % (str_n_doc, n_warehouse)

        alt_n_doc = u'%s от %s' % (n_doc, record['DTDOC'])        
        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        dt_obj = record['DATE1']
        dt_reg = record['DATE2']
        
        # Если совпадают даты СФ и даты регистрации, то приложение создавать не надо
        if dt_obj == dt_reg:
            log.service(u'Документ <%s>. Приложение не создано. Совпадение даты СФ (%s) и даты поступления(%s)' % (n_doc, dt_obj, dt_reg))
            return None
        
        if not dt_obj:
            # Если не указывается дата документа явно, то подставляем
            # в качестве даты дату счет фактуры
            dt_obj = dt_doc
        
        platelchik_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        platelchik_balans_code = int(record['CODK'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
        
        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        
                
        cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, inn, kpp, platelchik_balans_code)
                
        # ВНИМАНИЕ! В случае если не указан контрагент, 
        # мы указываем его наименование в тегах и все
        cagent_tag = u''
        if cagent_cod is None:
            cagent_tag = platelchik_name
            log.service(u'Документ <%s>. Не определен контрагент <%s>' % (n_doc, cagent_tag))
                    
        # По документу генерируем
        doc_typ = '9001000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                             tab, transaction)
                    
        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        
                    
        warehouse_tag = u'Склад %d' % n_warehouse
        
        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=datetime.date.today(),
                       dt_state=datetime.date.today(),
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_obj,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=u'Приложение/Транспортные документы',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'Приложение;Материалы;%s;%s;;%s;;;;%s' % (warehouse_tag, cagent_tag, codf, alt_n_doc))
        return new_rec

    def _load_ndocs_spec_from_dbf(self, dbf_filename=None):
        """
        Загрузить номера документов из DBF файла спецификации БАЛАНСа.
        @param dbf_filename: Полное имя загружаемого DBF файла.
        """
        if dbf_filename is None or not os.path.exists(dbf_filename):
            log.warning(u'Отсутствует файл <%s> для импорта данных' % dbf_filename)
            return
        
        self._9184_ndocs = list()
        # Запускаем загрузку
        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFileReadOnly() 
            dbf_tab.Open(dbf_filename)
            
            dlgfunc.openProgressDlg(ic.getMainWin(),
                                     u'Пакетная обработка', u'Импорт спуцификаций документов',
                                    max_value=dbf_tab.getRecCount())
            i = 0
            record = dbf_tab.getRecDict()
            while not dbf_tab.EOF():                
                n_doc = '---'

                # Главная проверка наличия проводок по счету 91-84
                if record and (int(record['SSD']) == 9184 or int(record['SSK']) == 9184):
                    n_doc = strfunc.toUnicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
                    if n_doc not in self._9184_ndocs:
                        self._9184_ndocs.append(n_doc)
                    
                dbf_tab.Next()
                record = dbf_tab.getRecDict()
                
                i += 1
                if n_doc:
                    dlgfunc.updateProgressDlg(i, u'Загружены данные спецификации документа № <%s>' % n_doc)

            dbf_tab.Close()
            dbf_tab = None
            
            dlgfunc.updateProgressDlg(i, u'')
            dlgfunc.closeProgressDlg()

        except:
            
            dlgfunc.closeProgressDlg()
            if dbf_tab:
                dbf_tab.Close()
                dbf_tab = None
            log.fatal(u'Ошибка импорта данных спецификаций документов материалов БАЛАНС+')
