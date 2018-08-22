#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функция получения списка документов за период.
"""

from ic.std.dlg import std_dlg
from ic.std.utils import ic_time

SQL_FMT = '''
SELECT DISTINCT
    scan_document_tab.n_doc AS n_doc,
    scan_document_tab.doc_name AS doc_name,
    to_char(scan_document_tab.doc_date, 'YYYY-MM-DD') AS doc_date,
    nsi_doc_type.name AS doc_typ,
    nsi_c_agent.name AS contragent,
    1 AS doc_count   
FROM
    scan_document_tab,
    nsi_doc_type,
    nsi_c_agent
WHERE scan_document_tab.doc_type = nsi_doc_type.cod AND
    scan_document_tab.c_agent = nsi_c_agent.cod %s;
'''

DB_DATE_FMT = '%Y-%m-%d'


def search_doc_data(docnum='', is_docnum_equal=False, docname='', 
                    docdate_start='', docdate_end='', 
                    doctype='', contragents=(), entity='',
                    description='', comment='',
                    tag0='', tag1='', tag2='', tag3='', tag4='', tag5='', 
                    tag6='', tag7='', tag8='', tag9='', 
                    order_by_field='doc_date'):
    """
    Получение списка документов записей удовлетворяющих критериям поиска.
    @param docnum: Номер документа.
    @param is_doc_equal: True - проверка на точное совпадение номера документа
        False - проверка на вхождение.
    @param docname: Наименование документа. Поиск производиться по вхождению.
    @param docdate_start: Начальная дата проверки даты документа.
    @param docdate_end: Конечная дата проверки даты документа.
    @param doc_type: Код типа документа.
    @param contragents: Список кодов контрагентов.
    @param entity: Код подразделения.
    @param description: Описание. Поиск производиться по вхождению.
    @param comment: Комментарии. Поиск производиться по вхождению.
    @param tag0: Тег/Метка 1. Поиск производиться по вхождению.
    @param tag1: Тег/Метка 2. Поиск производиться по вхождению.
    @param tag2: Тег/Метка 3. Поиск производиться по вхождению.
    @param tag3: Тег/Метка 4. Поиск производиться по вхождению.
    @param tag4: Тег/Метка 5. Поиск производиться по вхождению.
    @param tag5: Тег/Метка 6. Поиск производиться по вхождению.
    @param tag6: Тег/Метка 7. Поиск производиться по вхождению.
    @param tag7: Тег/Метка 8. Поиск производиться по вхождению.
    @param tag8: Тег/Метка 9. Поиск производиться по вхождению.
    @param tag9: Тег/Метка 10. Поиск производиться по вхождению.
    @param order_by_field: Указание поля сортировки.
    """
    if not docdate_start and  not docdate_end:
        dlg_params = std_dlg.getDateRangeDlg(None)
    
        if dlg_params is not None:
            date_start = dlg_params[0]
            date_end = dlg_params[1]
            docdate_start = date_start.strftime(DB_DATE_FMT)
            docdate_end = date_end.strftime(DB_DATE_FMT)
        else:
            # Нажата <отмена>
            return None
        
    where = list()
    if docnum:
        if is_docnum_equal and (isinstance(is_docnum_equal, str) or isinstance(is_docnum_equal, unicode)):
            is_docnum_equal = eval(is_docnum_equal)
        if is_docnum_equal:
            where.append('scan_document_tab.n_doc = \'%s\'' % docnum)
        else:
            where.append('scan_document_tab.n_doc  ILIKE \'%%%%%s%%%%\'' % docnum)

    if docname:
        where.append('scan_document_tab.doc_name  ILIKE \'%%%%%s%%%%\'' % docname)
        
    if docdate_start and docdate_end:
        if docdate_start == docdate_end:
            where.append('scan_document_tab.doc_date = \'%s\'' % docdate_start)
        else:
            where.append('scan_document_tab.doc_date BETWEEN \'%s\' AND \'%s\'' % (docdate_start, docdate_end) )

    if doctype:
        where.append('scan_document_tab.doc_type = \'%s\'' % doctype)

    if (isinstance(contragents, str) or isinstance(contragents, unicode)) and contragents:
        contragents = eval(contragents)
    if contragents:
        contragent_where = ['scan_document_tab.c_agent = \'%s\'' % contragent_cod for contragent_cod in contragents]
        where.append('( %s )' % ' OR '.join(contragent_where))

    if entity:
        where.append('scan_document_tab.entity = \'%s\'' % entity)

    if description:
        where.append('scan_document_tab.description  ILIKE \'%%%%%s%%%%\'' % description)
    if comment:
        where.append('scan_document_tab.comment  ILIKE \'%%%%%s%%%%\'' % comment)

    tags = [tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9]
    for i, tag in enumerate(tags):
        if tag:
            where.append('scan_document_tab.tag%d  ILIKE \'%%%%%s%%%%\'' % (i, tag))

    where_txt = ''
    if where:
        where_txt = ' AND \n' + ' AND '.join(where)

    # Сортировка
    if order_by_field:
        where_txt += 'ORDER BY %s' % order_by_field

    sql = SQL_FMT % where_txt
    
    return dict(__sql__=sql)
