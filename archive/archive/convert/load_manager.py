#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер загрузки документов из DBF файла.
"""

import datetime
import uuid
import os

from . import import_manager

from ic.log import log
from ic.db import dbf
from ic.utils import extfunc
from ic.engine import glob_functions
from ic.dlg import dlgfunc

import ic

# Version
__version__ = (0, 0, 2, 2)


class icDBFDocLoadManager(import_manager.icBalansImportManager):
    """
    Класс общий для всех менеджеров импорта документов из DBF.
    """
    def __init__(self, pack_scan_panel=None):
        """
        Конструктор.

        :param pack_scan_panel: Панель отображения списка документов в пакетной обработке.
        """
        import_manager.icBalansImportManager.__init__(self, pack_scan_panel)

    def _create_doc(self, dbf_record, transaction, doc, sType, in_out=None, from_1c=False):
        """
        Создание нового документа.

        :param dbf_record: Словарь записи DBF файла.
        :param transaction: Объект транзакции.
        :param doc: Объект документа для пакетной обработки.
        :param sType:
        :param in_out: Признак приходного/расходного документа.
            Если не определен, то берется из записи DBF файла.
        :return: Словарь новой записи документа.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        # tab = doc.getTable()

        # ВНИМАНИЕ! Чтобы не нарушить порядок сортировки документов сортировать
        # необходимо по NPP + NPPS
        nn = dbf_record['NPP']
        npps = dbf_record['NPPS']

        if from_1c:
            # !!! Для 1С
            str_n_doc = dbf_record['PRIM_2'].strip() if dbf_record['PRIM_2'].strip() else dbf_record['NDOC'].strip()
        else:
            # Для Баланс+
            str_n_doc = dbf_record['NDOC'].strip()
        
        alt_n_doc = dbf_record['NOMDOC']
        # ВНИМАНИЕ! Номер документа на бумажном носителе
        print_n_doc = dbf_record['NOMDOC']
        dt_doc = dbf_record['DTDOC']
        dt_obj = dbf_record['DATE1']
        dt_oper = dbf_record['DTOPER']
        doc_name = self.get_doc_name(dbf_record['TYP_DOC'])
        in_out = int(dbf_record['IN_OUT']) if in_out is None else in_out
        doc_typ = self.find_doc_type_code(dbf_record['TYP_DOC'], in_out)
        # log.debug(str(dbf_record))
        cagent_cod = self.find_contragent_code(self.contragent_sprav,
                                               dbf_record['NAMD'],
                                               dbf_record['INN'],
                                               dbf_record['KPP'],
                                               dbf_record['CODK'])

        if in_out:
            # Расходные документы/Продажа
            n_doc = u'%s.%s.%s' % (self.get_sector_subcode(sType),
                                   self.get_doc_type_subcode(dbf_record['TYP_DOC'], dbf_record['IN_OUT']),
                                   print_n_doc)
        else:
            # Приходные документы/Покупка
            n_doc = u'%s.%s.%s' % (self.get_sector_subcode(sType),
                                   self.get_doc_type_subcode(dbf_record['TYP_DOC'], dbf_record['IN_OUT']),
                                   str_n_doc)

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
                       nn=int(str(nn) + str(npps)),
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
                       doc_name=doc_name,
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=tags,
                       is_duplex=is_duplex,
                       n_scan_pages=n_pages)
        return new_rec

    def _load_doc(self, doc_dbf_filename, sFileType, from_1c=False):
        """
        Загрузить документы из DBF файла.

        :param doc_dbf_filename: Полное имя загружаемого файла.
        :param sFileType: Тип загружаемого файла.
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

            dlgfunc.openProgressDlg(ic.getMainWin(),
                                     u'Пакетная обработка', u'Загрузка данных',
                                    max_value=dbf_tab.getRecCount())
            i = 0
            record = dbf_tab.getRecDict()
            while not dbf_tab.EOF():
                n_doc = None
                if os.path.basename(doc_dbf_filename)[1].upper() in ('R', 'P'):
                    # ВНИМАНИЕ! В DBF файле не корректно указывается признак прихода/расхода
                    # поэтому определяем этот признак по имени файла
                    in_out = os.path.basename(doc_dbf_filename)[1].upper() == 'R'
                else:
                    in_out = None
                log.debug(u'Файл: %s. Приход/Расход: %s' % (os.path.basename(doc_dbf_filename), in_out))
                new_rec = self._create_doc(record, transaction, doc, sFileType, in_out=in_out, from_1c=from_1c)
                if new_rec:
                    n_doc = new_rec['n_doc']
                    # log.debug(u'+ %s' % str(new_rec))
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
            log.fatal(u'Ошибка загрузки данных документов материалов БАЛАНС+')

    def load_doc(self, doc_dbf_filename, sFileType, bAutoRemove=False, from_1c=False):
        """
        Загрузить документы из DBF файла.

        :param doc_dbf_filename: Полное имя загружаемого файла.
        :param sFileType: Тип загружаемого файла.
        :param bAutoRemove: Автоматически удалить файл после загрузки?
        """
        self._load_doc(doc_dbf_filename, sFileType, from_1c=from_1c)

        # Удалить файл после загрузки
        if bAutoRemove:
            try:
                os.remove(doc_dbf_filename)
            except:
                log.fatal(u'Ошибка удаления файла <%s>' % doc_dbf_filename)

        # log.debug(u'Обновление списка документов...%s' % u'ДА' if self.pack_scan_panel else u'НЕТ')
        if self.pack_scan_panel:
            self.pack_scan_panel.refreshDocList(True)
