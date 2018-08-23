#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
!!! МОДУЛЬ НЕ ИСПОЛЬЗУЕТСЯ !!!
Функции импорта расходных документов в таблицу пакетной обработки.
"""

import os
import os.path
import datetime
import smbclient
import urlparse

from ic.log import log
import ic
from ic.utils import ic_file
from ic.utils import filefunc
from ic.utils import smbfunc

# Version
__version__ = (0, 0, 2, 1)

# Список путей поиска DBF файла
FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#RLZ/',
                 )

ZTR_FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/',
                     )

MT_FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/',
                    )

OSN_FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/#MTS/OSN/',
                     )

#PRJ_DIRNAME = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) if os.path.dirname(__file__) else os.path.dirname(os.path.dirname(os.getcwd()))
#LOCAL_SPRVENT_FILENAME = os.path.join(PRJ_DIRNAME, 'db', 'SPRVENT.VNT')

# Склады тары
TARE_WAREHOUSES = (10, 2, 6, 5)
# Склад пивной дробины
WASTE_WAREHOUSES = (3, )
# Склад безтарки
KEG_WAREHOUSES = (8, )


def smb_download_dbf(download_urls=None, dbf_filename=None, dst_path=None):
    """
    Найти и загрузить DBF файл.
    @param download_urls: Список путей поиска DBF файла.
    @param dbf_filename: Имя DBF файла.
    @return: True - Произошла загрузка, False - ничего не загружено.
    """
    if download_urls is None:
        download_urls = FIND_SMB_URLS

    return smbfunc.smb_download_file(download_urls, filename=dbf_filename, 
                                     out_path=dst_path)


def get_src_dbf_filename(src_year, src_month, n_warehouse, is_input=False):
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

    
def import_docs(dt_begin, dt_end, n_warehouse, is_input=False):
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
        
        pack_doc = ic.metadata.archive.mtd.scan_document_pack.create()
        pack_doc.GetManager().init()
        
        result1 = import_rlz_docs(cur_year, cur_dt.month, n_warehouse, 
                                  min_dt, max_dt, is_input, pack_doc)
        result2 = import_ttn_docs(cur_year, cur_dt.month, n_warehouse, 
                                  min_dt, max_dt, is_input, pack_doc)
        # result2= True
        return result1 and result2
    return False


def import_ttn_docs(cur_year, cur_month, n_warehouse, min_dt, max_dt, 
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
    dst_path = os.path.join(ic_file.getRootProjectDir(), 'db')
    dst_filename = os.path.join(dst_path, src_filename)
    dst_filename_spc = os.path.join(dst_path, src_filename_spc)
    result = smb_download_dbf(dbf_filename=src_filename, dst_path=dst_path)
    result_spc = smb_download_dbf(dbf_filename=src_filename_spc, dst_path=dst_path)
    if result and result_spc:
        # Успешно загрузили
        dbf_filename = dst_filename.replace('.DCB', '.DBF')
        dbf_filename_spc = dst_filename_spc.replace('.DSB', 'S.DBF')
        if not filefunc.is_same_file_length(dst_filename, dbf_filename):
            # Это другой файл
            # Скопировать DCB в DBF
            if os.path.exists(dbf_filename):
                os.remove(dbf_filename)
            ic_file.CopyFile(dst_filename, dbf_filename)
            if os.path.exists(dbf_filename_spc):
                os.remove(dbf_filename_spc)
            ic_file.CopyFile(dst_filename_spc, dbf_filename_spc)
            
            pack_doc.GetManager().load_ttn_from_dbf(dbf_filename, min_dt, max_dt, is_input)

        else:
            log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
        return True
    else:
        log.warning(u'Ошибка связи с SMB ресурсом бекапа')
    return False
    

def import_rlz_docs(cur_year, cur_month, n_warehouse, min_dt, max_dt, 
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
    
    src_filename = get_src_dbf_filename(cur_year, cur_month, n_warehouse, is_input)
        
    # Сначала загрузить DBF из бекапа
    dst_path = os.path.join(ic_file.getRootProjectDir(), 'db')
    dst_filename = os.path.join(dst_path, src_filename)
    result = smb_download_dbf(dbf_filename=src_filename, dst_path=dst_path)
    if result:
        # Успешно загрузили
        dbf_filename = dst_filename.replace('.DCM', '.DBF')
        if not filefunc.is_same_file_length(dst_filename, dbf_filename):
            # Это другой файл
            # Скопировать DCM в DBF
            if os.path.exists(dbf_filename):
                os.remove(dbf_filename)
            ic_file.CopyFile(dst_filename, dbf_filename)
            
            pack_doc.GetManager().load_rlz_from_dbf(dbf_filename, min_dt, max_dt, is_input)

        else:
            log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
        return True
    else:
        log.warning(u'Ошибка связи с SMB ресурсом бекапа')
    return False


def import_doc_book(dt_begin, dt_end, n_warehouses=(), is_input=False):
    """
    Импорт документов из БАЛАНСа в виде книги покупок / продаж.
        Выборка документов производиться по диапазону дат документов 
        по определенным складам.
    @param dt_begin: Дата начала выборки документов.
    @param dt_end: Дата конца выборки документов.
    @param n_warehouses: Список номеров складов.
    @param is_input: Признак приходного документа.
    @return: True/False.
    """
    if not n_warehouses:
        log.warning(u'Не определены склады книги покупок / продаж.')
        return False
    
    result = True
    for n_warehouse in n_warehouses:
        result = result and import_docs(dt_begin, dt_end, n_warehouse, is_input)
    return result


def import_zatraty_docs(cur_year, is_input=False):
    """
    Импорт документов затрат на производство из БАЛАНСа.
        Выборка документов производиться за год.
    @param cur_year: Год выборки документов.
    @param is_input: Признак приходного документа.
    @return: True/False.
    """
    log.info(u'--- ЗАПУСК ИМПОРТА ДОКУМЕНТОВ ЗАТРАТ НА ПРОИЗВОДСТВО ---')

    pack_doc = ic.metadata.archive.mtd.scan_document_pack.create()
    pack_doc.GetManager().init()
        
    result1 = import_ztr7601_docs(cur_year, is_input, pack_doc)
    result2 = import_ztr7606_docs(cur_year, is_input, pack_doc)
    return result1 and result2


def import_ztr_docs(cur_year, is_input=None, pack_doc=None, 
                    base_filename='BS0Z76.DBS'):
    """
    Импорт документов затрат на производство из БАЛАНСа.
        Выборка документов производиться за год.
    @param cur_year: Обрабатываемый год.
    @param is_input: Признак приходного документа.
    @param pack_doc: Объект документа пакетной обработки.
    @param base_filename: Базовое имя файла источника данных.
    """
    if pack_doc is None:
        log.warning(u'Не определен объект документа пакетной обработки')
        return False
    
    src_filename = os.path.join(str(cur_year), 'FDOC', base_filename)
        
    # Сначала загрузить DBF из бекапа
    dst_path = os.path.join(ic_file.getRootProjectDir(), 'db')
    dst_filename = os.path.join(dst_path, src_filename)
    result = smbfunc.smb_download_file(ZTR_FIND_SMB_URLS, filename=src_filename, 
                                       out_path=dst_path)
    if result:
        # Успешно загрузили
        dbf_filename = dst_filename.replace('.DBS', '.DBF')
        if not filefunc.is_same_file_length(dst_filename, dbf_filename):
            # Это другой файл
            # Скопировать DBS в DBF
            if os.path.exists(dbf_filename):
                os.remove(dbf_filename)
            ic_file.CopyFile(dst_filename, dbf_filename)
            
            pack_doc.GetManager().load_ztr_from_dbf(dbf_filename, cur_year, is_input)

        else:
            log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
        return True
    else:
        log.warning(u'Ошибка связи с SMB ресурсом бекапа')
    return False


def import_ztr7601_docs(cur_year, is_input=False, pack_doc=None):
    """
    Импорт документов затрат на производство по 7601 счету из БАЛАНСа.
        Выборка документов производиться за год.
    @param cur_year: Обрабатываемый год.
    @param is_input: Признак приходного документа.
    @param pack_doc: Объект документа пакетной обработки.
    """
    return import_ztr_docs(cur_year, is_input, pack_doc, 
                           base_filename='BS0Z76.DBS')


def import_ztr7606_docs(cur_year, is_input=False, pack_doc=None):
    """
    Импорт документов затрат на производство по 7606 счету из БАЛАНСа.
        Выборка документов производиться за год.
    @param cur_year: Обрабатываемый год.
    @param is_input: Признак приходного документа.
    @param pack_doc: Объект документа пакетной обработки.
    """
    return import_ztr_docs(cur_year, is_input, pack_doc, 
                           base_filename='BS7606.DBS')
   

def import_mt_docs(cur_year, n_warehouse, is_input=True, pack_doc=None):
    """
    Импорт документов учета материалов из БАЛАНСа.
        Выборка документов производиться за год.
    @param cur_year: Обрабатываемый год.
    @param n_warehouse: Номер склада.
    @param is_input: Признак приходного документа.
    @param pack_doc: Объект документа пакетной обработки.
    """
    if n_warehouse is None:
        log.warning(u'Не определен номер склада при импорте документов <Материалы>')
        return False
    
    if pack_doc is None:
        log.warning(u'Не определен объект документа пакетной обработки')
        return False
    
    base_filename = 'MI%03d.DCM' % n_warehouse if is_input else 'MO%03d.DCM' % n_warehouse
    src_filename = os.path.join(str(cur_year), 'FDOC', base_filename)
        
    # Сначала загрузить DBF из бекапа
    dst_path = os.path.join(ic_file.getRootProjectDir(), 'db')
    dst_filename = os.path.join(dst_path, src_filename)
    result = smbfunc.smb_download_file(MT_FIND_SMB_URLS, filename=src_filename, 
                                       out_path=dst_path)
    if result:
        # Успешно загрузили
        dbf_filename = dst_filename.replace('.DCM', '.DBF')
        if not filefunc.is_same_file_length(dst_filename, dbf_filename):
            # Это другой файл
            # Скопировать DCM в DBF
            if os.path.exists(dbf_filename):
                os.remove(dbf_filename)
            ic_file.CopyFile(dst_filename, dbf_filename)
            
            pack_doc.GetManager().load_mt_from_dbf(dbf_filename, cur_year, is_input)

        else:
            log.debug(u'Уже загружен актуальный файл <%s>' % dst_filename)
        return True
    else:
        log.warning(u'Ошибка связи с SMB ресурсом бекапа')
    return False


def import_material_docs(cur_year, n_warehouse, is_input=False):
    """
    Импорт документов из БАЛАНСа <Материалы>.
        Выборка документов производиться за год.
    @param cur_year: Год выборки документов.
    @param is_input: Признак приходного документа.
    @param n_warehouse: Номер склада.
    @return: True/False.
    """
    log.info(u'--- ЗАПУСК ИМПОРТА ДОКУМЕНТОВ <МАТЕРИАЛЫ> ---')

    pack_doc = ic.metadata.archive.mtd.scan_document_pack.create()
    pack_doc.GetManager().init()
        
    result = import_mt_docs(cur_year, n_warehouse, is_input, pack_doc)
    return result


def test():
    """
    Тестирование.
    """
    from ic import config
    log.init(config)
    
    smb_download_sprvent()
    
    is_same_file(LOCAL_SPRVENT_FILENAME, 
                 LOCAL_SPRVENT_FILENAME.replace('.VNT', '.DBF'))
    
    
if __name__ == '__main__':
    test()