#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль дополнительных функций обработки документов.
"""

from ic.log import log
from work_flow.work_sys import ictabrequisite


def document_remove_to(doc_uuid, src_doc, dst_doc,
                       requisite_replace=None, ask_del=False):
    """
    Переместить документ из одной структуры документа
    в другую.
    Функция является примером архивирования документа.
    @param doc_uuid: UIID переносимого документа.
    @param src_doc: Объект документа-источника.
    @param dst_doc: Объект документа-приемника.
    @param requisite_replace: Словарь замены имен реквизитов.
        Формат:
        {'Имя реквизита в документе-приемнике': 'Имя реквизита в документе-источнике'}
    @param ask_del: Спрашивать об удалении документа из источника?
    @return: True/False.
    """
    # Заменить имена реквизитов на имена таблиц
    new_requisite_replace = dict()
    for requisite_dst_name, requisite_src_name in requisite_replace.items():
        src_tabname = None
        if src_doc.isRequisite(requisite_src_name):
            src_requisite = src_doc.getRequisite(requisite_src_name)
            if isinstance(src_requisite, ictabrequisite.icTABRequisitePrototype):
                src_tabname = src_requisite.getTableName()
        dst_tabname = None
        if dst_doc.isRequisite(requisite_dst_name):
            dst_requisite = dst_doc.getRequisite(requisite_dst_name)
            if isinstance(dst_requisite, ictabrequisite.icTABRequisitePrototype):
                dst_tabname = dst_requisite.getTableName()

        if src_tabname is None and dst_tabname is None:
            # Если табличные реквизиты не заменяются, то оставляем по старому
            new_requisite_replace[requisite_dst_name] = requisite_src_name
        elif src_tabname is None and dst_tabname:
            new_requisite_replace[dst_tabname] = requisite_src_name
        elif src_tabname and dst_tabname is None:
            new_requisite_replace[requisite_dst_name] = src_tabname
        else:
            new_requisite_replace[dst_tabname] = src_tabname

    try:
        src_doc.load_obj(doc_uuid)
        data = src_doc.getRequisiteData()

        if requisite_replace:
            for dst_requisite, src_requisite in new_requisite_replace.items():
                data[dst_requisite] = data[src_requisite]
                del data[src_requisite]
        dst_doc.addRequisiteData(data)
        src_doc.Del(doc_uuid, ask=ask_del)
        return True
    except:
        log.fatal(u'Ошибка переноса документа <%s> из <%s> в <%s>' % (doc_uuid,
                                                                      src_doc.getName(),
                                                                      dst_doc.getName()))
    return False
