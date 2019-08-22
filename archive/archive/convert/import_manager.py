#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс общий для всех менеджеров импорта документов из БАЛАНС+.
"""

# import os
# import os.path
# import smbclient
import datetime
import sqlalchemy

import ic
from ic.log import log
from ic.utils import smbfunc
from ic.dlg import ic_dlg
from ic.log import iclogbrowser
from ic.utils import ic_uuid


# Version
__version__ = (0, 0, 1, 1)

# Код КПП для ИП отсутствует, подменяем на КПП по умолчанию
DEFAULT_KPP_CODE = '---------'

# Формат автоматической генерации ИНН части кода если не указан
DEFAULT_INN_CODE_FMT = '%010d'

DEFAULT_DBF_DT_FMT = '%d.%m.%Y'
DEFAULT_DB_DT_FMT = '%Y-%m-%d'


class icImportManagerInterface(object):
    """
    Общий интерфейс для всех менеджеров импорта документов.
    """

    def init(self):
        """
        Инициализация внутреннего состояния менеджера.
        """
        log.warning(u'Метод инициализации не реализован в менеджере <%s>' % self.__class__.__name__)

    def import_docs(self):
        """
        Общий метод загрузки документов.
        """
        log.warning(u'Метод загрузки документов не реализован в менеджере <%s>' % self.__class__.__name__)


class icBalansImportManager(icImportManagerInterface):
    """
    Класс общий для всех менеджеров импорта документов из БАЛАНС+.
    """

    def __init__(self, pack_scan_panel=None, dbf_find_smb_urls=()):
        """
        Конструктор.
        @param pack_scan_panel: Панель отображения списка документов в пакетной обработке.
        @param dbf_find_smb_urls: Список путей SMB ресурсов для поиска DBF файлов загрузки.
        """
        self.dbf_find_smb_urls = dbf_find_smb_urls

        # Панель отображения списка документов в пакетной обработке
        self.pack_scan_panel = pack_scan_panel

        # Документ пакетной обработки
        self.pack_doc = None

        self.contragent_sprav = None

    def init(self):
        """
        Инициализация внутреннего состояния менеджера.
        """
        # Используемые справочники
        sprav_manager = ic.metadata.archive.mtd.nsi_archive.create()
        self.contragent_sprav = sprav_manager.getSpravByName('nsi_c_agent')

    def setPackScanPanel(self, pack_scan_panel):
        """
        Установить панель пакетного сканирования.
        """
        log.debug(u'Установить панель пакетного сканирования.')
        self.pack_scan_panel = pack_scan_panel

    def smb_download_dbf(self, download_urls=None, dbf_filename=None, dst_path=None):
        """
        Найти и загрузить DBF файл.
        @param download_urls: Список путей поиска DBF файла.
        @param dbf_filename: Имя DBF файла.
        @return: True - Произошла загрузка, False - ничего не загружено.
        """
        if download_urls is None:
            download_urls = self.dbf_find_smb_urls

        return smbfunc.smb_download_file(download_urls, filename=dbf_filename,
                                         out_path=dst_path)

    def find_contragent_code(self, contragent_sprav, name, inn, kpp, balance_cod):
        """
        Поиск кода контрагента по наименованию и ИНН.
        """
        if contragent_sprav is None:
            sprav_manager = ic.metadata.archive.mtd.nsi_archive.create()
            contragent_sprav = sprav_manager.getSpravByName('nsi_c_agent')

        name = name.strip()
        inn = inn.strip() if inn else inn
        kpp = kpp.strip() if kpp else kpp

        find_codes = list()
        if balance_cod and inn:
            # Ищем только по балансовскому коду и ИНН
            str_balans_cod = u'<%d>' % balance_cod
            tab = contragent_sprav.getStorage().getTable()
            find_codes = contragent_sprav.getStorage().find_code_where(sqlalchemy.and_(tab.c.s1.ilike(u'%'+str_balans_cod+u'%'),
                                                                                       tab.c.inn == inn))
        elif kpp and inn:
            # Ищем по ИНН с KPP и наименованию
            find_codes = contragent_sprav.getStorage().find_code(name=name, inn=inn, kpp=kpp)
        elif inn:
            # Ищем только по ИНН и наименованию
            find_codes = contragent_sprav.getStorage().find_code(name=name, inn=inn)
        else:
            # Нет полной информации ищем только по коду БАЛАНС
            str_balans_cod = u'<%d>' % balance_cod
            tab = contragent_sprav.getStorage().getTable()
            find_codes = contragent_sprav.getStorage().find_code_where(tab.c.s1.ilike(u'%'+str_balans_cod+u'%'))

        len_find_codes = len(find_codes)
        if len_find_codes == 1:
            log.debug(u'Найден контрагент <%s> для <%s>' % (find_codes[0], name))
            return find_codes[0]
        elif len_find_codes > 1:
            msg = u'Найдено несколько кодов для <%s> ИНН: <%s> КПП: <%s>' % (name, inn, kpp)
            log.warning(msg)
        else:
            log.warning(u'Не найден в справочнике контрагент <%s>. Код БАЛАНС+: %s.' %(name, balance_cod))
        return None

    def find_doc_type_code(self, typ_doc, in_out):
        """
        Поиск кода типа документа.
        """
        typ = None
        log.debug(u'Приход/Расход <%d>' % in_out)
        if typ_doc.upper() == u'СЧЕТ-ФАКТУРА':
            typ = '2001000000000' if in_out else '1001000000000'
        elif typ_doc.upper() == u'ТОРГ12':
            typ = '2002000000000' if in_out else '1002000000000'
        elif typ_doc.upper() == u'АКТ':
            typ = '2005000000000' if in_out else '1005000000000'
        # Акты участка ОСНОВНЫЕ СРЕДСТВА
        elif typ_doc.upper() == u'ОС1':
            # Акт приема-передачи
            typ = '9009100000000'
        elif typ_doc.upper() == u'ОС3':
            # Акт модернизации
            typ = '9009300000000'
        elif typ_doc.upper() == u'ОС4':
            # Акт списания
            typ = '9009400000000'
        elif typ_doc.upper() == u'ОС4А':
            # Акт списания автотранспорта
            typ = '9009500000000'
        elif typ_doc.upper() == u'ОС4Б':
            # Акт группового списания
            typ = '9009600000000'
        else:
            log.warning(u'Не определен тип документа <%s>' % typ_doc)
        return typ

    def get_doc_type_subcode(self, typ_doc, in_out):
        """
        Поиск кода типа документа.
        """
        if typ_doc.upper() == u'СЧЕТ-ФАКТУРА':
            return u'СФ'
        elif typ_doc.upper() == u'ТОРГ12':
            return u'ТОРГ12'
        elif typ_doc.upper() == u'АКТ':
            return u'АКТ'
        elif typ_doc.upper() in (u'ОС1', u'ОС3', u'ОС4', u'ОС4А', u'ОС4Б'):
            return u'АКТ'
        return u''

    def get_doc_name(self, typ_doc):
        """
        Поиск кода типа документа.
        """
        if typ_doc.upper() == u'ОС1':
            return u'Акт приема-передачи'
        elif typ_doc.upper() == u'ОС3':
            return u'Акт модернизации'
        elif typ_doc.upper() == u'ОС4':
            return u'Акт списания'
        elif typ_doc.upper() == u'ОС4А':
            return u'Акт списания автотранспорта'
        elif typ_doc.upper() == u'ОС4Б':
            return u'Акт группового списания'
        return typ_doc

    def get_sector_subcode(self, sType):
        """
        Поиск кода участка.
        """
        if sType.upper() == u'R':
            return u'РЛЗ'
        elif sType.upper() == u'M':
            return u'МТ'
        elif sType.upper() == u'Z':
            return u'ЗТР'
        elif sType.upper() == u'O':
            return u'ОС'
        elif sType.upper() == u'U':
            return u'УСЛ'
        return u''

    def get_sector_name(self, sType):
        """
        Поиск наименования участка.
        """
        if sType.upper() == u'R':
            return u'Реализация'
        elif sType.upper() == u'M':
            return u'Материалы'
        elif sType.upper() == u'Z':
            return u'Затраты на производство'
        elif sType.upper() == u'O':
            return u'Основные средства'
        elif sType.upper() == u'U':
            return u'Услуги/Аренда'
        return u''

    def gen_contragent_code(self, inn, kpp, i=0):
        """
        Генерация кода контрагента по инн + кпп.
        @param inn: ИНН контрагента.
        @param kpp: КПП контрагента.
        @param i: Порядковый индекс в обработке.
        """
        if inn == '0' or not inn.strip():
            # ВНИМАНИЕ! У иностранных фирм может быть не указан ИНН
            # но в справочнике они должны присутствовать
            inn = DEFAULT_INN_CODE_FMT % i
        # Учитываем что у ИП может отсутствовать КПП
        kpp = kpp.strip() if kpp and kpp.strip() else DEFAULT_KPP_CODE

        code = '-' * (12 - len(inn)) + inn + kpp
        return code

    def find_uuid_document(self, doc, n_doc, dt_doc, doc_type, tab=None, transaction=None):
        """
        Поиск UUID документа по значениям реквизитов.
        """
        find_uuid = doc.findRequisiteData(n_doc=n_doc,
                                          doc_date=dt_doc,
                                          doc_type=doc_type)
        if len(find_uuid) == 1:
            find_uuid = find_uuid[0]
        elif not find_uuid:
            find_uuid = ic_uuid.get_uuid()
        else:
            log.warning(u'Найдено несколько документов <%s> <%s> за %s %s' % (doc_type, n_doc, dt_doc, find_uuid))
            # Берем только первую счет фактуру
            tab.del_where_transact(sqlalchemy.or_(*[tab.c.uuid==cur_uuid for cur_uuid in find_uuid]),
                                   transaction=transaction)
            find_uuid = find_uuid[0]

        return find_uuid

    def is_correct_contragent_code(self, contragent_code):
        """
        Контроль на не корректный код контрагента.
        @param contragent_code: Проверяемый код контрагента.
        @return: True - код корректный/False - не корректный.
        """
        try:
            return (contragent_code is not None) and bool(contragent_code.strip()) and (len(contragent_code) == 21)
        except:
            return False

    def import_docs(self):
        """
        Общий метод загрузки документов.
        """
        try:
            start_dt = datetime.datetime.now()
            result = self._import_docs()
            if result and ic_dlg.openAskBox(u'Загрузка', u'Загрузка документов завершена. Показать журнал загрузки?'):
                iclogbrowser.show_log_browser_dlg(tLogTypes=('SERVICE',),
                                                  dtStartFilter=start_dt,
                                                  dtStopFilter=datetime.datetime.now())
        except:
            log.fatal(u'Ошибка импорта документов.')

    def _import_docs(self):
        """
        Общий метод загрузки документов.
        """
        log.warning(u'Метод загрузки документов не реализован в менеджере <%s>' % self.__class__.__name__)

