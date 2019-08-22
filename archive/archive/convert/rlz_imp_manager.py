#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс менеджера импорта документов БАЛАНС+ участка <Реализация>.
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
# from ic.utils import smbfunc
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

FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#RLZ/',
                 )

# Склады тары
TARE_WAREHOUSES = (10, 2, 6, 5)
# Склад пивной дробины
WASTE_WAREHOUSES = (3, )
# Склад безтарки
KEG_WAREHOUSES = (8, )

# Импортируемые склады приходных документов
INPUT_DOC_WAREHOUSES = (2, 5, 6, 8, 10)


class icRealizImportManager(import_manager.icBalansImportManager):
    """
    Класс менеджера импорта документов БАЛАНС+ участка <Реализация>.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        import_manager.icBalansImportManager.__init__(self, *args, **kwargs)

        if not self.dbf_find_smb_urls:
            self.dbf_find_smb_urls = FIND_SMB_URLS

    def _get_src_dbf_filename(self, src_year, src_month, n_warehouse, is_input=False):
        """
        Получить имя DBF файла исходных данных документа.
        @param src_year: Год.
        @param src_month: Месяц.
        @param n_warehouse: Номер склада.
        @param is_input: Признак приходного документа.
        @return: Имя DBF файла исходных данных документа БАЛАНС+.
        """
        str_month = '%X' % src_month
        if n_warehouse in TARE_WAREHOUSES:
            if is_input:
                base_filename = 'TI%s%03d.DCM' % (str_month, n_warehouse)
            else:
                base_filename = 'TO%s%03d.DCM' % (str_month, n_warehouse)
        elif n_warehouse in WASTE_WAREHOUSES:
            base_filename = 'R0%03d.DCM' % n_warehouse
        elif n_warehouse in KEG_WAREHOUSES and is_input:
            base_filename = 'TI%s%03d.DCM' % (str_month, n_warehouse)
        else:
            base_filename = 'R%s%03d.DCM' % (str_month, n_warehouse)
        return os.path.join(str(src_year), 'FDOC', base_filename)

    def _get_n_torg12(self, record):
        """
        Определение номера накладной ТОРГ12 поставщика.
        1. Номер накладной ТОРГ12 определяется по полю NTORG12.
        2. Если поле пустое, то поиск в полях примечания:
            следующее слово после <накл>.
        3. Если в примечаниях не найдено, то используем номер счет фактуры поставщика.
        @param record: Словарь записи DBF файла.
        """
        # Получить поля записи
        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()

        alt_n_torg12 = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE)        
        n_torg12 = unicode(record.get('NTORG12', ''), DBF_DEFAULT_ENCODE)

        if n_torg12:
            return n_torg12
        elif u'накл' in comment:
            comment = comment.strip().replace(u'  ', u' ')
            line = comment.split(u' ')
            try:
                i = line.index(u'накл') + 1
                return line[i] if i < len(line) else alt_n_torg12
            except ValueError:
                # Нет такого слова в примечании
                # Следующим шагом возвращает альтернативный номер
                pass
        return alt_n_torg12

    def _import_docs(self):
        """
        Запуск импорта документов <Реализация>.
        """
        log.debug(u'Запуск импорта документов <Реализация>')
        dt_range = std_dlg.getDateRangeDlg(parent=self.pack_scan_panel, is_concrete_date=True)
        result = False
        if dt_range is not None:
            dt_begin, dt_end = dt_range
            if self.pack_scan_panel:
                self.pack_scan_panel.dt_begin = dt_begin
                self.pack_scan_panel.dt_end = dt_end

            idx = std_dlg.getRadioChoiceDlg(parent=self.pack_scan_panel, title=u'Документ',
                                            label=u'Выберите тип документа:',
                                            choices=(u'Расходный документ (Продажа)',
                                                     u'Приходный документ (Покупка)'))
            if idx is None:
                return False
            is_input = idx == 1
            
            if not is_input:
                n_warehouse = std_dlg.getIntegerDlg(parent=self.pack_scan_panel, 
                                                    title=u'Склад',
                                                    label=u'Введите номер склада:', 
                                                    min_value=1, max_value=100)
                if n_warehouse is None:
                    # Нажата ОТМЕНА
                    return False
                n_warehouses = [n_warehouse]
            else:
                n_warehouses = std_dlg.getCheckBoxDlg(parent=self.pack_scan_panel, 
                                                      title=u'Склад',
                                                      label=u'Выберите номера складов:',
                                                      choices=(u'2 Склад', u'5 Склад', u'6 Склад', u'8 Склад', u'10 Склад'))
                if n_warehouses is None:
                    # Нажата ОТМЕНА
                    return False
                n_warehouses = [INPUT_DOC_WAREHOUSES[i] for i, n in enumerate(n_warehouses) if n]

            if self.pack_scan_panel:
                # self.pack_scan_panel.n_warehouse = n_warehouse
                self.pack_scan_panel.is_input = is_input
                self.pack_scan_panel.clearDocList()

            result = True
            for n_warehouse in n_warehouses:
                result = self._import_docs_rlz(dt_begin, dt_end,
                                               n_warehouse, is_input)

            if self.pack_scan_panel:
                self.pack_scan_panel.refreshDocList(dt_begin=dt_begin,
                                                    dt_end=dt_end)
        return result

    def _import_docs_rlz(self, dt_begin, dt_end, n_warehouse, is_input=False):
        """
        Импорт документов реализации из БАЛАНСа.
            Выборка документов производиться по диапазону дат документов 
            по определенному складу.
        @param dt_begin: Дата начала выборки документов.
        @param dt_end: Дата конца выборки документов.
        @param n_warehouse: Номер склада.
        @param is_input: Признак приходного документа.
        @return: True/False.
        """
        log.info(u'--- ЗАПУСК ИМПОРТА ДОКУМЕНТОВ РЕАЛИЗАЦИИ ---')

        min_dt = min(dt_begin, dt_end)
        max_dt = max(dt_begin, dt_end)
        day_count = (max_dt - min_dt).days if min_dt != max_dt else 1
        for i_day in range(day_count):
            cur_dt = min_dt + datetime.timedelta(days=i_day)        
            cur_year = cur_dt.year

            if self.pack_doc is None:
                self.pack_doc = ic.metadata.archive.mtd.scan_document_pack.create()
                self.pack_doc.GetManager().init()

            result1 = self._import_rlz_docs_file(cur_year, cur_dt.month, n_warehouse, 
                                            min_dt, max_dt, is_input, self.pack_doc)
            result2 = self._import_ttn_docs_file(cur_year, cur_dt.month, n_warehouse, 
                                                 min_dt, max_dt, is_input, self.pack_doc)
            # result2= True
            return result1 and result2
        return False

    def _import_rlz_docs_file(self, cur_year, cur_month, n_warehouse, min_dt, max_dt, 
                              is_input=False, pack_doc=None):
        """
        Импорт документов реализации из БАЛАНСа.
            Выборка документов производиться по диапазону дат документов 
            по определенному складу.
        @param cur_year: Обрабатываемый год.
        @param cur_month: Обрабатываемый месяц.
        @param n_warehouse: Номер склада.
        @param is_input: Признак приходного документа.
        @param pack_doc: Объект документа пакетной обработки.
        """
        if pack_doc is None:
            log.warning(u'Не определен объект документа пакетной обработки')
            return False
    
        src_filename = self._get_src_dbf_filename(cur_year, cur_month, n_warehouse, is_input)
        
        # Сначала загрузить DBF из бекапа
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db')
        dst_filename = os.path.join(dst_path, src_filename)
        result = self.smb_download_dbf(dbf_filename=src_filename, dst_path=dst_path)
        if result:
            # Успешно загрузили
            dbf_filename = dst_filename.replace('.DCM', '.DBF')
            if not filefunc.is_same_file_length(dst_filename, dbf_filename):
                # Это другой файл
                # Скопировать DCM в DBF
                if os.path.exists(dbf_filename):
                    os.remove(dbf_filename)
                filefunc.CopyFile(dst_filename, dbf_filename)
            
                self._load_rlz_from_dbf(dbf_filename, min_dt, max_dt, is_input)
            else:
                log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
            return True
        else:
            log.warning(u'Ошибка связи с SMB ресурсом бекапа')
        return False

    def _import_ttn_docs_file(self, cur_year, cur_month, n_warehouse, min_dt, max_dt, 
                              is_input=False, pack_doc=None):
        """
        Импорт документов ТТН из БАЛАНСа.
            Выборка документов производиться по диапазону дат документов 
            по определенному складу.
        @param cur_year: Обрабатываемый год.
        @param cur_month: Обрабатываемый месяц.
        @param n_warehouse: Номер склада.
        @param is_input: Признак приходного документа.
        @param pack_doc: Объект документа пакетной обработки.
        """
        if pack_doc is None:
            log.warning(u'Не определен объект документа пакетной обработки')
            return False

        str_month = '%X' % cur_month
        base_filename = 'SB%s111.DCB' % str_month
        src_filename = os.path.join(str(cur_year), 'FDSB', base_filename)
        base_filename = 'SB%s111.DSB' % str_month
        src_filename_spc = os.path.join(str(cur_year), 'FDSB', base_filename)

        # Сначала загрузить DBF из бекапа
        dst_path = os.path.join(filefunc.getRootProjectDir(), 'db')
        dst_filename = os.path.join(dst_path, src_filename)
        dst_filename_spc = os.path.join(dst_path, src_filename_spc)
        result = self.smb_download_dbf(dbf_filename=src_filename, dst_path=dst_path)
        result_spc = self.smb_download_dbf(dbf_filename=src_filename_spc, dst_path=dst_path)
        if result and result_spc:
            # Успешно загрузили
            dbf_filename = dst_filename.replace('.DCB', '.DBF')
            dbf_filename_spc = dst_filename_spc.replace('.DSB', 'S.DBF')
            if not filefunc.is_same_file_length(dst_filename, dbf_filename):
                # Это другой файл
                # Скопировать DCB в DBF
                if os.path.exists(dbf_filename):
                    os.remove(dbf_filename)
                filefunc.CopyFile(dst_filename, dbf_filename)
                if os.path.exists(dbf_filename_spc):
                    os.remove(dbf_filename_spc)
                filefunc.CopyFile(dst_filename_spc, dbf_filename_spc)
            
                self._load_ttn_from_dbf(dbf_filename, min_dt, max_dt, is_input)

            else:
                log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
            return True
        else:
            log.warning(u'Ошибка связи с SMB ресурсом бекапа')
        return False

    def _load_rlz_from_dbf(self, dbf_filename=None, begin_dt=None, end_dt=None, is_input=False):
        """
        Загрузить данные пакета документов реализации (счет-фактур и ТОРГ12) 
            из DBF файла БАЛАНСа.
        @param is_input: Признак приходного документа.
        """
        if dbf_filename is None or not os.path.exists(dbf_filename):
            log.warning(u'Отсутствует файл <%s> для импорта данных' % dbf_filename)
            return
        if begin_dt is None:
            begin_dt = DT_TODAY
        if end_dt is None:
            end_dt = DT_TODAY

        # Номер склада берем из имени файла
        n_warehouse = int(os.path.splitext(os.path.basename(dbf_filename))[0][-3:])

        doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        # Сначала удалить данные из таблицы за указанный период по определенному складу
        #tab.del_where(sqlalchemy.and_(tab.c.doc_date.between(begin_dt.strftime(DEFAULT_DB_DT_FMT), 
        #                              end_dt.strftime(DEFAULT_DB_DT_FMT)),
        #              tab.c.n_doc.endswith('/%d' % n_warehouse)))

        # Затем запускаем загрузку
        transaction = tab.getDB().getTransaction(autoflush=False, autocommit=False)         

        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFile()
            dbf_tab.Open(dbf_filename)

            ic_dlg.openProgressDlg(ic.getMainWin(),
                                     u'Пакетная обработка', u'Импорт данных',
                                   max_value=dbf_tab.getRecCount())
            i = 0
            # i_code = 0
            record = dbf_tab.getRecDict()
            while not dbf_tab.EOF():
                n_doc = None
                # По документу генерируем <счет-фактуры>
                new_rec = self._create_schet_factura(record, transaction, n_warehouse, is_input, doc)
                if new_rec:
                    n_doc = new_rec['n_doc']
                    tab.add_rec_transact(rec=new_rec, transaction=transaction)

                # По документу генерируем <ТОРГ12>
                new_rec = self._create_torg12(record, transaction, n_warehouse, is_input, doc)
                if new_rec:
                    tab.add_rec_transact(rec=new_rec, transaction=transaction)

                # По документу генерируем <Алкосправку>
                new_rec = self._create_alkospravka(record, transaction, n_warehouse, is_input, doc)
                if new_rec:
                    tab.add_rec_transact(rec=new_rec, transaction=transaction)

                dbf_tab.Next()
                record = dbf_tab.getRecDict()

                i += 1
                if n_doc:
                    ic_dlg.updateProgressDlg(i, u'Загружены данные документа № <%s>' % n_doc)

            dbf_tab.Close()
            dbf_tab = None

            ic_dlg.updateProgressDlg(i, u'')
            ic_dlg.closeProgressDlg()

            # Подтвердить транзакцию
            transaction.commit()
        except:
            # Отменить транзакцию
            transaction.rollback()
            
            ic_dlg.closeProgressDlg()
            if dbf_tab:
                dbf_tab.Close()
                dbf_tab = None
            log.fatal(u'Ошибка импорта данных документов реализации БАЛАНС+')

    def _load_ttn_from_dbf(self, dbf_filename=None, begin_dt=None, end_dt=None, is_input=False):
        """
        Загрузить данные пакета документов ТТН из DBF файла БАЛАНСа.
        @param is_input: Признак приходного документа.
        """
        if dbf_filename is None or not os.path.exists(dbf_filename):
            log.warning(u'Отсутствует файл <%s> для импорта данных' % dbf_filename)
            return
        if begin_dt is None:
            begin_dt = DT_TODAY
        if end_dt is None:
            end_dt = DT_TODAY

        # Имя файла спецификации
        spc_dbf_filename = dbf_filename.replace('.DBF', 'S.DBF')
        spc_dbf = dbf.icDBFFileReadOnly(spc_dbf_filename)
        spc_idx_records = spc_dbf.getIndexRecsByField('NDOC')

        doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        # Сначала удалить данные из таблицы за указанный период по определенному складу
        #tab.del_where(sqlalchemy.and_(tab.c.doc_date.between(begin_dt.strftime(DEFAULT_DB_DT_FMT), 
        #                              end_dt.strftime(DEFAULT_DB_DT_FMT)),
        #              tab.c.n_doc.endswith('/%d' % n_warehouse)))

        # Затем запускаем загрузку
        transaction = tab.getDB().getTransaction(autoflush=False, autocommit=False)         

        dbf_tab = None
        try:
            dbf_tab = dbf.icDBFFile()
            dbf_tab.Open(dbf_filename)

            ic_dlg.openProgressDlg(ic.getMainWin(),
                                     u'Пакетная обработка', u'Импорт данных',
                                   max_value=dbf_tab.getRecCount())
            i = 0
            # i_code = 0
            record = dbf_tab.getRecDict()
            while not dbf_tab.EOF():
                # По документу генерируем <ТТН>
                # Удаление на случай двойного описания 
                # одного и того же в DBF файле                              
                new_recs = self._create_ttn(record, transaction, is_input, doc, spc_idx_records)
                if new_recs:
                    for new_rec in new_recs:
                        tab.add_rec_transact(rec=new_rec, transaction=transaction)
                        ic_dlg.updateProgressDlg(i, u'Загружены данные документа № <%s>' % new_rec['n_doc'])

                dbf_tab.Next()
                record = dbf_tab.getRecDict()

                i += 1

            dbf_tab.Close()
            dbf_tab = None

            ic_dlg.updateProgressDlg(i, u'')
            ic_dlg.closeProgressDlg()

            # Подтвердить транзакцию
            transaction.commit()
        except:
            # Отменить транзакцию
            transaction.rollback()

            ic_dlg.closeProgressDlg()
            if dbf_tab:
                dbf_tab.Close()
                dbf_tab = None
            log.fatal(u'Ошибка импорта данных документов реализации БАЛАНС+')

    def _is_nds_in_schet_factura(self, is_on, cod_oper):
        """
        Проверка на есть ли в СФ НДС.
        @param is_on: Признак наличия НДС.
        @param cod_oper: Код операции БАЛАНС+.
        """
        return bool(cod_oper) and is_on

    def _create_schet_factura(self, record, transaction=None, n_warehouse=1, 
                              is_input=False, doc=None):
        """
        Создать счет-фактуру по данным документа БАЛАНСа.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        # ВНИМАНИЕ! Приходные документы по 8-му складу добавлять услуги
        # как расходные если они проходят с отрицательными суммами        
        doc_typ = None
        if n_warehouse == 8 and is_input:
            doc_sum = float(record['SUMMA'])
            if doc_sum > 0:
                # ВНИМАНИЕ! Если суммы положительные, то все равно загрузить документ
                # как приходный
                pass
            else:
                # Приходные документы по 8 складу с отрицательными суммами
                # считаем расходными
                doc_typ = '2001000000000'

        n_doc = u'%s/%d' % (unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip(), 
                            n_warehouse)

        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        platelchik_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        platelchik_balans_code = int(record['CODK'])
        gruzopol_name = unicode(record['NAMD2'], DBF_DEFAULT_ENCODE)
        gruzopol_balans_code = int(record['CODK2'])
        perevoz_name = unicode(record['NAMD3'], DBF_DEFAULT_ENCODE)
        perevoz_balans_code = int(record['CODK3'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)
        cod_oper = int(record['CODOPER'])
        is_nds_doc = self._is_nds_in_schet_factura(True, cod_oper)

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()

        alt_n_doc = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE)

        cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, inn, kpp, platelchik_balans_code)

        # Контроль на не корректный код
        if not self.is_correct_contragent_code(cagent_cod):
            log.service(u'Документ <%s>. Не корректный код <%s> контрагента <%s>' % (n_doc, cagent_cod, platelchik_name))
            return None                

        # По документу генерируем <счет-фактуры>
        if doc_typ is None:
            doc_typ = '2001000000000' if not is_input else '1001000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                             tab, transaction)

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)

        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None

        if is_input and n_warehouse == 8:
            # Для 8 склада приходные документы могут содержать расходные
            pass
        elif is_input and not alt_n_doc.strip():
            # ВНИМАНИЕ! Для приходных документов счет фактур если не определен 
            # номер документа поставщика, то считаем что от поставщика нет счет фактуры
            # поэтому документ не создаем
            log.service(u'Документ <%s>. Для приходных документов счет фактур если не определен номер документа поставщика, то считаем что от поставщика нет счет фактуры поэтому документ не создаем' % n_doc)
            return None
        elif is_input and not is_nds_doc:
            log.service(u'Документ <%s>. Нет НДС' % n_doc)
            return None

        is_nds_doc_str = u'с НДС' if is_nds_doc else u'без НДС'
        
        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=DT_TODAY,
                       dt_state=DT_TODAY,
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_doc,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=u'Счет-фактура',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'Счет-фактура;Реализация;Код операции %02d;Склад %d;;%s;;;%s;%s' % (cod_oper, n_warehouse, codf, is_nds_doc_str, alt_n_doc))
        return new_rec

    def _create_torg12(self, record, transaction=None, n_warehouse=1, 
                       is_input=False, doc=None):
        """
        Создать ТОРГ12 по данным документа БАЛАНСа.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @return: Словарь новой записи документа ТОРГ12.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        # ВНИМАНИЕ! Приходные документы по 8-му складу добавлять услуги
        # как расходные если они проходят с отрицательными суммами
        doc_typ = None
        if n_warehouse == 8 and is_input:
            doc_sum = float(record['SUMMA'])
            if doc_sum > 0:
                # ВНИМАНИЕ! Если суммы положительные, то все равно загрузить документ
                # как приходный
                pass
            else:
                # Приходные документы по 8 складу с отрицательными суммами
                # считаем расходными
                doc_typ = '2002000000000'

        n_doc = u'%s/%d' % (unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip(), 
                            n_warehouse)

        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        platelchik_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        platelchik_balans_code = int(record['CODK'])
        gruzopol_name = unicode(record['NAMD2'], DBF_DEFAULT_ENCODE)
        gruzopol_balans_code = int(record['CODK2'])
        perevoz_name = unicode(record['NAMD3'], DBF_DEFAULT_ENCODE)
        perevoz_balans_code = int(record['CODK3'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()

        alt_n_doc = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE)

        cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, inn, kpp, platelchik_balans_code)

        # Контроль на не корректный код
        if not self.is_correct_contragent_code(cagent_cod):
            log.service(u'Документ <%s>. Не корректный код <%s> контрагента <%s>' % (n_doc, cagent_cod, platelchik_name))
            return None

        # По документу генерируем <ТОРГ12>
        if doc_typ is None:
            doc_typ = '2002000000000' if not is_input else '1002000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ,
                                            tab, transaction)

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)

        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None

        # Определяем номер накладной из комментариев
        n_nakl = self._get_n_torg12(record)

        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=DT_TODAY,
                       dt_state=DT_TODAY,
                       dt_oper=dt_oper,
                       n_obj=n_nakl,
                       obj_date=dt_doc,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=u'ТОРГ12',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       tags=u'ТОРГ12;Реализация;Склад %d;;;%s;;;;' % (n_warehouse, codf))
        return new_rec

    def _create_alkospravka(self, record, transaction=None, n_warehouse=1, 
                            is_input=False, doc=None):
        """
        Создать алко-справку по данным документа БАЛАНСа.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @return: Словарь новой записи документа Счет-фактура.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        doc_typ = None

        n_doc = u'%s/%d' % (unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip(), 
                            n_warehouse)

        dt_doc = record['DTDOC']
        dt_oper = record['DTOPER']
        platelchik_name = unicode(record['NAMD'], DBF_DEFAULT_ENCODE)
        platelchik_balans_code = int(record['CODK'])
        gruzopol_name = unicode(record['NAMD2'], DBF_DEFAULT_ENCODE)
        gruzopol_balans_code = int(record['CODK2'])
        perevoz_name = unicode(record['NAMD3'], DBF_DEFAULT_ENCODE)
        perevoz_balans_code = int(record['CODK3'])
        inn =  unicode(str(record['INN']), DBF_DEFAULT_ENCODE)
        kpp =  unicode(record['KPP'], DBF_DEFAULT_ENCODE)

        prim = unicode(record['PRIM'], DBF_DEFAULT_ENCODE)
        prim2 = unicode(record['PRIM2'], DBF_DEFAULT_ENCODE)
        prim3 = unicode(record['PRIM3'], DBF_DEFAULT_ENCODE)
        prim4 = unicode(record['PRIM4'], DBF_DEFAULT_ENCODE)
        prim5 = unicode(record['PRIM5'], DBF_DEFAULT_ENCODE)
        comment = prim + u' ' + prim2 + u' ' + prim3 + u' ' + prim4 + u' ' + prim5
        comment = comment.strip()

        alt_n_doc = unicode(record['ALTNDOC'], DBF_DEFAULT_ENCODE)
        n_fix_egais = unicode(record['NEGAIS'], DBF_DEFAULT_ENCODE)
        n_ttn = unicode(record['NTTN'], DBF_DEFAULT_ENCODE)

        cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, inn, kpp, platelchik_balans_code)

        # Контроль на не корректный код
        if not self.is_correct_contragent_code(cagent_cod):
            log.service(u'Документ <%s>. Не корректный код <%s> контрагента <%s>' % (n_doc, cagent_cod, platelchik_name))
            return None                

        # По документу генерируем <алко-справки>
        if doc_typ is None:
            doc_typ = '2003000000000' if not is_input else '1003000000000'
        find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ, 
                                            tab, transaction)

        # Удаление на случай двойного описания 
        # одного и того же в DBF файле
        tab.del_where_transact(tab.c.uuid==find_uuid, 
                               transaction=transaction)

        # Проверка игнорирования обаботки документов по доп коду документа                    
        codf = unicode(record['CODF'], DBF_DEFAULT_ENCODE)
        if codf in IGNORED_CODF:
            return None

        if not n_fix_egais.strip():
            # ВНИМАНИЕ! Если не заполнен номер фиксации ЕГАИС
            # то документ не создаем
            return None

        # Количество листов уже присутствует в Балансе
        n_pages = int(record['PN3'])

        new_rec = dict(uuid=find_uuid,
                       state='00',
                       dt_create=DT_TODAY,
                       dt_state=DT_TODAY,
                       dt_oper=dt_oper,
                       n_obj=alt_n_doc,
                       obj_date=dt_doc,
                       username=glob_functions.getCurUserName(),
                       computer=extfunc.getComputerNameLAT(),
                       n_doc=n_doc,
                       doc_date=dt_doc,
                       doc_name=u'Алкосправка',
                       doc_type=doc_typ,
                       c_agent=cagent_cod,
                       entity='00001',
                       comment=comment,
                       n_scan_pages=n_pages,
                       tags=u'Алкосправка;Реализация;Склад %d;;;%s;;ТТН %s;ЕГАИС %s;%s' % (n_warehouse, codf, n_ttn, n_fix_egais, alt_n_doc))
        return new_rec

    def _create_ttn(self, record, transaction=None, is_input=False, doc=None, 
                    spc_idx_records=None, n_warehouse=None):
        """
        Создать ТТН по данным документа БАЛАНСа.
        Все дополнительные признаки-атрибуты фиксируются в тегах карточки документа.
        @param record: Словарь записи DBF файла.
        @param is_input: Признак приходного документа.
        @param spc_idx_records: Словарь индекса файла спецификации по номеру документа.
        @param n_warehouse: Номер склада.
        @return: Список словарей новых записей документов ТТН.
        """
        if doc is None:
            doc = self.pack_doc if self.pack_doc else ic.metadata.archive.mtd.scan_document_pack.create()
        tab = doc.getTable()

        balans_ndoc = unicode(record['NDOC'], DBF_DEFAULT_ENCODE).strip()
        spc_records = spc_idx_records.get(balans_ndoc, list())

        pos_count = len(spc_records)
        n_docs = [u'%s/%d' % (balans_ndoc, i+1) for i in range(pos_count)]        

        new_recs = list()
        for i, n_doc in enumerate(n_docs):
            if not n_doc.strip():
                log.warning(u'Не определен номер документа ТТН')
                continue

            try:
                spc_record = spc_records[i]
            except IndexError:
                log.service(u'Ошибка спецификации документа <%s>. NDOC <%s>' % (n_doc, balans_ndoc))
                continue

            # Проверка на соответствие обрабатываемого документа приходно/расходному признаку
            if not is_input and int(spc_record['TYPSTR']) == 10:
                # Нам необходимы расходные документы
                log.service(u'Документ ТТН <%s> ПРИХОДНЫЙ. Обработка пропущена.' % n_doc)
                continue
            elif is_input and int(spc_record['TYPSTR']) != 10:
                # Нам необходимы приходные документы
                log.service(u'Документ ТТН <%s> РАСХОДНЫЙ. Обработка пропущена.' % n_doc)
                continue

            dt_doc = record['DTDOC']
            dt_oper = record['DTOPER']
            platelchik_name = unicode(spc_record['NAMS'], DBF_DEFAULT_ENCODE) if not isinstance(spc_record['NAMS'], unicode) else spc_record['NAMS']
            platelchik_balans_code = int(spc_record['CODK'])
            inn =  unicode(str(spc_record['INN']), DBF_DEFAULT_ENCODE) if not isinstance(spc_record['INN'], unicode) else spc_record['INN']

            n_ttn = unicode(spc_record['NTTN'], DBF_DEFAULT_ENCODE) if not isinstance(spc_record['NTTN'], unicode) else spc_record['NTTN']
            n_egais = unicode(spc_record['NEGAIS'], DBF_DEFAULT_ENCODE) if not isinstance(spc_record['NEGAIS'], unicode) else spc_record['NEGAIS']
            n_egais_tag = u'ЕГАИС: %s' % n_egais if n_egais else u''
            d_egais = unicode(spc_record['DEGAIS'], DBF_DEFAULT_ENCODE) if not isinstance(spc_record['DEGAIS'], unicode) else spc_record['DEGAIS']
            #n_alko = unicode(spc_record['FORTAX'], DBF_DEFAULT_ENCODE).replace(u'РФ', u'Алкосправка') if not isinstance(spc_record['FORTAX'], unicode) else spc_record['FORTAX'].replace(u'РФ', u'Алкосправка')

            # ВНИМАНИЕ! Здесь выбираем дату, т.к. дата позиции может различаться с датой документа
            #dt_doc = ic_time.datetime2date(datetime.datetime.strptime(d_egais, DEFAULT_DBF_DT_FMT)) if d_egais else spc_record['DTDOC']

            n_alko = u''

            alko_count = spc_record.get('PN3', 0)
            alko_count_txt = u'Кол. алкосправок: %d' % alko_count if alko_count else u''

            cagent_cod = self.find_contragent_code(self.contragent_sprav, platelchik_name, None, None, platelchik_balans_code)

            # Контроль на не корректный код
            if not self.is_correct_contragent_code(cagent_cod):
                log.service(u'Документ <%s>. Не корректный код <%s> контрагента <%s>' % (n_doc, cagent_cod, platelchik_name))
                continue

            # По документу генерируем <ТТН>
            # Удаление на случай двойного описания 
            # одного и того же в DBF файле
            doc_typ = '2004000000000' if not is_input else '1004000000000'
            if not n_warehouse:
                try:
                    # n_from_ndoc = int(n_doc.strip().split(u'/')[-1])
                    # n_warehouse = spc_record.get('COD3', n_from_ndoc)
                    # n_warehouse = n_warehouse if n_warehouse != 0 else n_from_ndoc
                    doc_prim = unicode(spc_record['PRIM'], DBF_DEFAULT_ENCODE) if not isinstance(spc_record['PRIM'], unicode) else spc_record['PRIM']
                    n_warehouse = self._get_ttn_warehouse(n_doc, spc_record.get('COD3', 0), 
                                                          doc_prim)
                except:
                    log.fatal(u'Ошибка определения номера склада по номеру документа <%s>' % n_doc)
                    log.service(u'Ошибка определения номера склада по номеру документа <%s>' % n_doc)
                    continue
            find_uuid = self.find_uuid_document(doc, n_doc, dt_doc, doc_typ,
                                                tab, transaction)

            tab.del_where_transact(tab.c.uuid==find_uuid, 
                                   transaction=transaction)
            new_rec = dict(uuid=find_uuid,
                           state='00',
                           dt_create=DT_TODAY,
                           dt_state=DT_TODAY,
                           dt_oper=dt_oper,
                           n_obj=u'%s от %s' % (n_doc, dt_doc.strftime(import_manager.DEFAULT_DBF_DT_FMT)),
                           obj_date=dt_doc,
                           username=glob_functions.getCurUserName(),
                           computer=extfunc.getComputerNameLAT(),
                           n_doc=n_doc,
                           doc_date=dt_doc,
                           doc_name=u'Товарно-транспортная накладная',
                           doc_type=doc_typ,
                           c_agent=cagent_cod,
                           entity='00001',
                           comment=u'№ %s FIX: %s от %s' % (n_ttn, n_egais, d_egais),
                           tags=u'ТТН;Реализация;Склад %d;;;;;%s;%s;%s' % (n_warehouse, n_egais_tag, n_alko, alko_count_txt))
            new_recs.append(new_rec)
        return new_recs

    def _get_ttn_warehouse(self, n_doc, spc_cod3, doc_prim):
        """
        Вспомогательная фукнция определения номера склада по данным документа.
        """
        n_from_ndoc = int(n_doc.strip().split(u'/')[-1])
        n_warehouse = spc_cod3
        if n_warehouse == 0:
            n_warehouse = int(doc_prim.split(u',')[0].split(u'/')[0]) if doc_prim else n_from_ndoc
        return n_warehouse
