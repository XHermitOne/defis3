#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс менеджера импорта документов БАЛАНС+ участка <Затраты>.
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
from ic.db import dbf
from ic.utils import extfunc
from ic.engine import glob_functions

from . import import_manager

# Version
__version__ = (0, 0, 1, 2)

DT_TODAY = datetime.date.today()

# Игнорируемые документы по признаку в поле CODF
# ВП - внутреннее перемещение
IGNORED_CODF = (u'ВП', u'АТ', u'ПП', u'АВ')

DBF_DEFAULT_ENCODE = 'cp866'


FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/',
                 )

COD_OPER_NDS = 1


class icZatratyImportManager(import_manager.icBalansImportManager):
    """
    Класс менеджера импорта документов БАЛАНС+ участка <Затраты>.
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
        Запуск импорта документов <Затраты>.
        """
        log.debug(u'Запуск импорта документов <Затраты на производство>')
        dt_range = std_dlg.getDateRangeDlg(parent=self.pack_scan_panel, is_concrete_date=False)
        result = False
        if dt_range is not None:
            dt_begin, dt_end = dt_range
            if self.pack_scan_panel:
                self.pack_scan_panel.dt_begin = dt_begin
                self.pack_scan_panel.dt_end = dt_end
            
                # self.pack_scan_panel.is_input = is_input
                self.pack_scan_panel.documents = list()

            # Определяем загружаем книгу покупок или просто документы
            idx = std_dlg.getRadioChoiceMaxiDlg(parent=self.pack_scan_panel, title=u'Документ',
                                                label=u'Выберите тип документов:',
                                                choices=(u'Счет-фактуры согласно книге продаж',
                                                         u'Счет-фактуры согласно книге покупок',
                                                         u'Прочие документы'))
            if idx is None:
                # Нажата ОТМЕНА
                return False
            is_kniga_pokupok = idx == 1
            is_kniga_prodaj = idx == 0
            
            for cur_year in range(dt_begin.year, dt_end.year+1):
                result = result or self._import_zatraty_docs(cur_year, None, 
                                                             is_nds=is_kniga_pokupok or is_kniga_prodaj)
                
            if self.pack_scan_panel:
                self.pack_scan_panel.refreshDocList(dt_begin=dt_begin,
                                                    dt_end=dt_end)
        return result

    def _import_zatraty_docs(self, cur_year, is_input=False, is_nds=False):
        """
        Импорт документов затрат на производство из БАЛАНСа.
            Выборка документов производиться за год.
        @param cur_year: Год выборки документов.
        @param is_input: Признак приходного документа.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        @return: True/False.
        """
        log.info(u'--- ЗАПУСК ИМПОРТА ДОКУМЕНТОВ ЗАТРАТ НА ПРОИЗВОДСТВО ---')

        if self.pack_doc is None:
            self.pack_doc = ic.metadata.archive.mtd.scan_document_pack.create()
            # self.pack_doc.GetManager().init()
        
        result1 = self._import_ztr7601_docs_file(cur_year, is_input, self.pack_doc,
                                                 is_nds=is_nds)
        result2 = self._import_ztr7606_docs_file(cur_year, is_input, self.pack_doc,
                                                 is_nds=is_nds)
        return result1 and result2

    def _import_ztr_docs_file(self, cur_year, is_input=None, pack_doc=None, 
                              base_filename='BS0Z76.DBS', is_nds=False,
                              n_schet=None):
        """
        Импорт документов затрат на производство из БАЛАНСа.
            Выборка документов производиться за год.
        @param cur_year: Обрабатываемый год.
        @param is_input: Признак приходного документа.
        @param pack_doc: Объект документа пакетной обработки.
        @param base_filename: Базовое имя файла источника данных.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        @param n_schet: Номер счета 76-01/76-06.
        @return: True/False.
        """
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
            dbf_filename = dst_filename.replace('.DBS', '.DBF')
            if not filefunc.is_same_file_length(dst_filename, dbf_filename):
                # Это другой файл
                # Скопировать DBS в DBF
                if os.path.exists(dbf_filename):
                    os.remove(dbf_filename)
                filefunc.CopyFile(dst_filename, dbf_filename)
            
                self._load_ztr_from_dbf(dbf_filename, cur_year, is_input, 
                                        is_nds=is_nds, n_schet=n_schet)

            else:
                log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
            return True
        else:
            log.warning(u'Ошибка связи с SMB ресурсом бекапа')
        return False

    def _import_ztr7601_docs_file(self, cur_year, is_input=False, pack_doc=None, 
                                  is_nds=False):
        """
        Импорт документов затрат на производство по 7601 счету из БАЛАНСа.
            Выборка документов производиться за год.
        @param cur_year: Обрабатываемый год.
        @param is_input: Признак приходного документа.
        @param pack_doc: Объект документа пакетной обработки.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        """
        return self._import_ztr_docs_file(cur_year, is_input, pack_doc, 
                                          base_filename='BS0Z76.DBS', is_nds=is_nds,
                                          n_schet='76-01')


    def _import_ztr7606_docs_file(self, cur_year, is_input=False, pack_doc=None, 
                                  is_nds=False):
        """
        Импорт документов затрат на производство по 7606 счету из БАЛАНСа.
            Выборка документов производиться за год.
        @param cur_year: Обрабатываемый год.
        @param is_input: Признак приходного документа.
        @param pack_doc: Объект документа пакетной обработки.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        """
        return self._import_ztr_docs_file(cur_year, is_input, pack_doc, 
                                          base_filename='BS7606.DBS', is_nds=is_nds,
                                          n_schet='76-06')

    def _load_ztr_from_dbf(self, dbf_filename=None, cur_year=None, is_input=None, 
                           is_nds=False, n_schet=None):
        """
        Загрузить данные пакета документов реализации (счет-фактур и ТОРГ12) 
            из DBF файла БАЛАНСа.
        @param is_input: Признак приходного документа.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        @param n_schet: Номер счета 76-01/76-06.
        """
        if dbf_filename is None or not os.path.exists(dbf_filename):
            log.warning(u'Отсутствует файл <%s> для импорта данных' % dbf_filename)
            return
        if cur_year is None:
            cur_year = DT_TODAY.year
        
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
                if is_input is None:
                    # По документу генерируем <счет-фактуры>
                    new_rec = self._create_schet_factura(record, transaction, True, doc, is_nds=is_nds, n_schet=n_schet)
                    if new_rec:
                        n_doc = new_rec['n_doc'] 
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                    new_rec = self._create_schet_factura(record, transaction, False, doc, is_nds=is_nds, n_schet=n_schet)
                    if new_rec:
                        n_doc = new_rec['n_doc'] 
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)

                    # По документу генерируем <Акт выполненных работ>
                    new_rec = self._create_act(record, transaction, True, doc, n_schet=n_schet)
                    if new_rec:
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                    new_rec = self._create_act(record, transaction, False, doc, n_schet=n_schet)
                    if new_rec:
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)

                    # По документу генерируем <Приложения>
                    new_rec = self._create_priloj(record, transaction, True, doc, n_schet=n_schet)
                    if new_rec:
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                    new_rec = self._create_priloj(record, transaction, False, doc, n_schet=n_schet)
                    if new_rec:
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                else:
                    # По документу генерируем <счет-фактуры>
                    new_rec = self._create_schet_factura(record, transaction, is_input, doc, is_nds=is_nds, n_schet=n_schet)
                    if new_rec:
                        n_doc = new_rec['n_doc'] 
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)

                    # По документу генерируем <Акт выполненных работ>
                    new_rec = self._create_act(record, transaction, is_input, doc, n_schet=n_schet)
                    if new_rec:
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)

                    # По документу генерируем <Приложения>
                    new_rec = self._create_priloj(record, transaction, is_input, doc, n_schet=n_schet)
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
            log.fatal(u'Ошибка импорта данных документов затрат на производство БАЛАНС+')

    def _get_ztr_schet_tag(self, doc_cod, n_schet=None):
        if n_schet is not None:
            schet_tag = u'Счет %s' % n_schet
            return schet_tag
        
        schet_tag = u''
        if doc_cod in (u'АС', u'СФ', u'КП'):
            schet_tag = u'Счет 76-01'
        elif doc_cod in (u'А6', u'С6', u'К6'):
            schet_tag = u'Счет 76-06'
        else:
            log.warning(u'Не определен счет по коду документа <%s>' % doc_cod)
        return schet_tag

    def _is_nds_in_schet_factura(self, is_on, cod_oper):
        """
        Проверка на есть ли в СФ НДС.
        @param is_on: Признак наличия НДС.
        @param cod_oper: Код операции БАЛАНС+.
        """
        return cod_oper == COD_OPER_NDS or is_on
    
    def _create_schet_factura(self, record, transaction=None, 
                              is_input=False, doc=None, is_nds=False, 
                              n_schet=None):
        """
        Создать счет-фактуру по данным документа БАЛАНСа <Затраты на производство>.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @param is_nds: Учет наличия НДС в документе для загрузки.
        @param n_schet: Номер счета 76-01/76-06.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'ЗТР.СФ.%s' % str_n_doc        
        
        alt_n_doc = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE).strip()
        if is_input and not alt_n_doc:
            # Если не определен номер СФ, то не генерировать документ
            log.service(u'Документ <%s>. Не определен номер счет-фактуры в документе' % n_doc)
            return None

        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        elif is_input and codf in (u'СФ', u'С6'):
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        elif not is_input and codf in (u'АС', u'А6'):
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        if codf in (u'КП', u'К6'):
            n_doc = u'ЗТР.СФ.КП.%s' % str_n_doc
        
        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        dt_obj = record['DATE1']
        
        platelchik_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        platelchik_balans_code = int(record['CODK'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
        # Код операции
        cod_oper = int(record['CODOPER'])
        # Признак явного наличия НДС
        is_on = bool(str(record['PARM_OPER']).strip())
        
        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        
                
        cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, inn, kpp, platelchik_balans_code)
                
        # Контроль на не корректный код
        if not self.is_correct_contragent_code(cagent_cod):
            log.service(u'Документ <%s>. Не корректный код <%s> контрагента <%s>' % (n_doc, cagent_cod, platelchik_name))
            # return None                

        # Контроль на наличие НДС в документе для КНИГИ ПОКУПОК
        is_nds_doc = self._is_nds_in_schet_factura(is_on, cod_oper)
        if is_nds and is_input and not is_nds_doc:
            log.service(u'Документ <%s>. Нет НДС' % n_doc)
            return None

        # По документу генерируем <счет-фактуры>
        doc_typ = '2001000000000' if not is_input else '1001000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)
                    
        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        # Указываем счет в тегах по типу документа
        schet_tag = self._get_ztr_schet_tag(codf, n_schet=n_schet)

        is_nds_doc_str = u'с НДС' if is_nds_doc else u'без НДС'
        
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
                       doc_name=u'Счет-фактура',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'Счет-фактура;Затраты на производство;Код операции %02d;%s;;%s;;;%s;%s' % (cod_oper, schet_tag, codf, is_nds_doc_str, alt_n_doc))
        return new_rec

    def _create_act(self, record, transaction=None, 
                    is_input=False, doc=None, n_schet=None):
        """
        Создать акт выполненных работ 
            по данным документа БАЛАНСа <Затраты на производство>.
            Все дополнительные признаки-атрибуты фиксируются 
            в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @param n_schet: Номер счета 76-01/76-06.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        alt_n_doc = unicode(record['N_DOGOV'], DBF_DEFAULT_ENCODE).strip()

        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        elif is_input and codf in (u'СФ', u'С6'):
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        elif not is_input and codf in (u'АС', u'А6'):
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        elif codf in (u'КП', u'К6'):
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None

        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'ЗТР.АКТ.%s' % str_n_doc        
        if not alt_n_doc:
            # Если не определен номер, то cгенерировать
            alt_n_doc = u'%s от %s' % (n_doc, record['DTDOC'])
        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        dt_obj = record['D_DOGOV']
        if not dt_obj:
            # Если не указывается дата документа явно, то подставляем
            # в качестве даты дату счет фактуры
            dt_obj = record['DATE1'] if record['DATE1'] else dt_doc

        platelchik_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        platelchik_balans_code = int(record['CODK'])
        inn = unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp = unicode(record['KPP'], DBF_DEFAULT_ENCODE)

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()        

        cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, inn, kpp, platelchik_balans_code)

        # Контроль на не корректный код
        if not self.is_correct_contragent_code(cagent_cod):
            log.service(u'Документ <%s>. Не корректный код <%s> контрагента <%s>' % (n_doc, cagent_cod, platelchik_name))
            # return None                

        # По документу генерируем <акт ваполненных работ>
        doc_typ = '2005000000000' if not is_input else '1005000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        # Указываем счет в тегах по типу документа
        schet_tag = self._get_ztr_schet_tag(codf, n_schet=n_schet)

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
                       doc_name=u'Акт выполненных работ',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'Акт выполненных работ;Затраты на производство;%s;;;%s;;;;%s' % (schet_tag, codf, alt_n_doc))
        return new_rec

    def _create_priloj(self, record, transaction=None, 
                       is_input=False, doc=None, n_schet=None):
        """
        Создать приложение по данным документа БАЛАНСа <Затраты на производство>.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @param n_schet: Номер счета 76-01/76-06.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        alt_n_doc = unicode(record['N_DOGOV'], DBF_DEFAULT_ENCODE).strip()

        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        elif is_input and codf in (u'СФ', u'С6'):
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        elif not is_input and codf in (u'АС', u'А6'):
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None
        elif codf in (u'КП', u'К6'):
            log.service(u'Не обрабатываемый код документа <%s>' % codf)
            return None

        str_n_doc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        n_doc = u'ЗТР.ПРИЛ.%s' % str_n_doc        

        if not alt_n_doc:
            # Если не определен номер, то cгенерировать
            alt_n_doc = u'%s от %s' % (n_doc, record['DTDOC'])
        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        dt_obj = record['D_DOGOV']
        if not dt_obj:
            # Если не указывается дата документа явно, то подставляем
            # в качестве даты дату счет фактуры
            dt_obj = record['DATE1'] if record['DATE1'] else dt_doc

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

        # Контроль на не корректный код
        if not self.is_correct_contragent_code(cagent_cod):
            log.service(u'Документ <%s>. Не корректный код <%s> контрагента <%s>' % (n_doc, cagent_cod, platelchik_name))
            # return None                

        # По документу генерируем
        doc_typ = '9001000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)        

        # Указываем счет в тегах по типу документа
        schet_tag = self._get_ztr_schet_tag(codf, n_schet=n_schet)
        
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
                       doc_name=u'Приложение',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'Приложение;Затраты на производство;%s;;;%s;;;;%s' % (schet_tag, codf, alt_n_doc))
        return new_rec
