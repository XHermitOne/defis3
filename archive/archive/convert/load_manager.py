#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер загрузки документов из DBF файла.
"""

import datetime
import uuid

from . import import_manager

from ic.log import log
from ic.db import dbf
from ic.utils import ic_extend
from ic.engine import ic_user
from ic.dlg import ic_dlg

import ic

# Version
__version__ = (0, 0, 1, 2)

# Functions

class icDBFDocLoadManager(import_manager.icBalansImportManager):
    """
    Класс общий для всех менеджеров импорта документов из DBF.
    """

    def __init__(self, pack_scan_panel=None):
        """
        Конструктор.
        @param pack_scan_panel: Панель отображения списка документов в пакетной обработке.
        """
        import_manager.icBalansImportManager.__init__(self, pack_scan_panel)

    def _create_doc(self, dbf_record, transaction, doc, sType):
        """
        Создание нового документа.
        @param dbf_record: Словарь записи DBF файла.
        @return: Словарь новой записи документа.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        # tab = doc.getTable()

        nn = dbf_record['NPP']
        str_n_doc = dbf_record['NDOC'].strip()
        n_doc = u'%s.%s.%s' % (self.get_sector_subcode(sType),
                               self.get_doc_type_subcode(dbf_record['TYP_DOC'], dbf_record['IN_OUT']),
                               str_n_doc)
        alt_n_doc = dbf_record['ALTNDOC']
        dt_doc = dbf_record['DTDOC']
        dt_obj = dbf_record['DATE1']
        dt_oper = dbf_record['DTOPER']
        doc_name = dbf_record['TYP_DOC']
        doc_typ =  self.find_doc_type_code(dbf_record['TYP_DOC'],
                                           dbf_record['IN_OUT'])
        cagent_cod = self.find_contragent_code(self.contragent_sprav,
                                               dbf_record['NAMD'],
                                               dbf_record['INN'],
                                               dbf_record['KPP'],
                                               dbf_record['CODK'])

        prim = dbf_record['PRIM']
        prim2 = dbf_record['PRIM2']
        prim3 = dbf_record['PRIM3']
        prim4 = dbf_record['PRIM4']
        prim5 = dbf_record['PRIM5']
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()

        tags = [doc_name.title(),
                self.get_sector_name(sType),
                u'Код операции %02d' % dbf_record['CODOPER'],
                u'',
                dbf_record['NAMD'],
                dbf_record['CODF'],
                u'',
                u'',
                dbf_record['YESNDS'],
                alt_n_doc]
        tags = ';'.join(tags)

        is_duplex = True if dbf_record['DUPLEX'] else False
        n_pages = dbf_record['NLIST'] if dbf_record['NLIST'] > 0 else 1

        new_rec = dict(uuid=str(uuid.uuid4()),
                       nn=nn,
                       state='00',
                       dt_create=datetime.date.today(),
                       dt_state=datetime.date.today(),
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_obj,
                       username=ic_user.getCurUserName(),
                       computer=ic_extend.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=doc_name,
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=tags,
                       is_duplex=is_duplex,
                       n_scan_pages=n_pages)
        return new_rec

    def _load_doc(self, doc_dbf_filename, sFileType):
        """
        Загрузить документы из DBF файла.
        @param doc_dbf_filename: Полное имя загружаемого файла.
        @param sFileType: Тип загружаемого файла.
        """
        doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.pack_scan_document.create()
        tab = doc.getTable()
        # Перед загрузкой полностью очищаем таблицу
        tab.clear()

        # Запускаем загрузку
        transaction = tab.getDB().getTransaction(autoflush=False, autocommit=False)
        # transaction = None
        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFileReadOnly()
            dbf_tab.Open(doc_dbf_filename)

            ic_dlg.icOpenProgressDlg(ic.getMainWin(),
                                     u'Пакетная обработка', u'Загрузка данных',
                                     Max_=dbf_tab.getRecCount())
            i = 0
            record = dbf_tab.getRecDict()
            while not dbf_tab.EOF():
                n_doc = None
                new_rec = self._create_doc(record, transaction, doc, sFileType)
                if new_rec:
                    n_doc = new_rec['n_doc']
                    # log.debug(u'+ %s' % str(new_rec))
                    tab.add_rec_transact(rec=new_rec, transaction=transaction)

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
            log.fatal(u'Ошибка загрузки данных документов материалов БАЛАНС+')

    def load_doc(self, doc_dbf_filename, sFileType):
        """
        Загрузить документы из DBF файла.
        @param doc_dbf_filename: Полное имя загружаемого файла.
        @param sFileType: Тип загружаемого файла.
        """
        self._load_doc(doc_dbf_filename, sFileType)

        # log.debug(u'Обновление списка документов...%s' % u'ДА' if self.pack_scan_panel else u'НЕТ')
        if self.pack_scan_panel:
            self.pack_scan_panel.refreshDocList(True)
