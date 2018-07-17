#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Документ прикладной системы.
В общем виде документ это объект состояния,
в котором определяются операции изменения состояния.
С помощью методов документа могут выполняться внутренние
операции. Результат выполнения операции может быть смена
состояния документа.

ВНИМАНИЕ! Смена состояний документа производиться
только в обработчиках выполнения операции!
Это правильное использование
метода изменения состояния документа.
(change_state и changeState)

Основные используемы методы документа:
    do_operation - выполнить операцию по имени.
    undo_operation - отмена операции по имени.
    do_operations - выполнение всех операций документа.
    undo_operations - выполнение отмены всех операций документа.

@type SPC_IC_DOCUMENT: C{dictionary}
@var SPC_IC_DOCUMENT: Спецификация на ресурсное описание документа.
Описание ключей SPC_IC_DOCUMENT:

    - B{name = 'default'}: Имя.
    - B{type = 'Document'}: Тип объекта.
    - B{description = ''}: Описание.
    - B{table = None}: Таблица, в которой хранятся документы заданного типа.
    - B{init_form = None}: Форма/Визард для создания/инициализации документа.
    - B{edit_form = None}: Форма для редактирования документа.
    - B{view_form = None}: Форма для просмотра документа.
    - B{report = None}: Отчет для распечатки документа.
    - B{prototype = None}: Документ, у которого наследуются реквизиты.
    
"""

# --- Подключение библиотек ---
from ic.log import log
from work_flow.work_sys import icstateobj
from . import docfunc
from work_flow.work_sys import persistent


# Версия
__version__ = (0, 0, 2, 1)

# --- Спецификация ---
SPC_IC_DOCUMENT = {'type': 'Document',
                   'name': 'default',
                   'description': '',    # Описание
                        
                   '__parent__': icstateobj.SPC_IC_STATEOBJ,
                   }

SPC_IC_NODE_DOCUMENT = {'type': 'NodeDocument',
                        'name': 'default',
                        'description': '',  # Описание

                        '__parent__': SPC_IC_DOCUMENT,
                        }


class icDocumentProto(icstateobj.icStateObjProto):
    """
    Документ.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icstateobj.icStateObjProto.__init__(self, *args, **kwargs)

    def getChildrenRequisites(self):
        """
        Дочерние реквизиты и спецификации.
        """
        return list()

    def getChildrenOperations(self):
        """
        Дочерние операции.
        """
        return list()

    def getDocUUID(self, doc_number=None):
        """
        Определить UUID документа по его номеру.
        @param doc_number: Номер документа.
        @return: UUID долкумента или None,
            если документ с таким номером отсутствует.
        """
        if doc_number is None:
            doc_number = self.getRequisiteValue('n_obj')

        tab = self.getTable()
        result = tab.get_where(tab.c.n_obj == doc_number)
        if result and result.rowcount:
            record = result.first()
            return record.uuid
        return None

    def find_operation(self, operation_name):
        """
        Поиск объекта операции по имени.
        @param operation_name: Имя операции.
        @return: Объект операции или None если операция
            не найдена.
        """
        find_operation_list = [requisite for requisite in self.getChildrenOperations() if requisite.getName() == operation_name]
        if find_operation_list:
            return find_operation_list[0]
        else:
            log.warning(u'Не найдена операция <%s> в документе <%s>' % (operation_name, self.getName()))
        return None

    def do_operation(self, operation_name):
        """
        Выполнить операцию по имени.
        ВНИМАНИЕ! Параметры функции не передаются т.к.
        операции работают только с документом и его реквизитами.
        Перед выполнением операции необходимо заполнить соответствующие
        реквизиты (необходимые для выполнения операции) значениями.
        @param operation_name: Имя операции.
        @return: True/False.
        """
        operation = self.find_operation(operation_name)
        if operation:
            return self._do_operation(operation)
        return False

    def _do_operation(self, operation):
        """
        Выполнить операцию.
        @param operation: Объект операции.
        @return: True/False.
        """
        return operation.do()

    def undo_operation(self, operation_name):
        """
        Отмена операции по имени.
        ВНИМАНИЕ! Параметры функции не передаются т.к.
        операции работают только с документом и его реквизитами.
        Перед выполнением операции необходимо заполнить соответствующие
        реквизиты (необходимые для выполнения операции) значениями.
        @param operation_name: Имя операции.
        @return: True/False.
        """
        operation = self.find_operation(operation_name)
        if operation:
            return self._undo_operation(operation)
        return False

    def _undo_operation(self, operation):
        """
        Отмена операции.
        @param operation: Объект операции.
        @return: True/False.
        """
        return operation.undo()

    def do_operations(self):
        """
        Выполнение всех операций документа.
        @return: True/False.
        """
        result = True
        for operation in self.getChildrenOperations():
            result = result and self._do_operation(operation)
        return result

    def undo_operations(self):
        """
        Выполнение отмены всех операций документа.
        @return: True/False.
        """
        result = True
        for operation in self.getChildrenOperations():
            result = result and self._undo_operation(operation)
        return result

    def remove_to(self, dst_doc, doc_uuid=None, doc_num=None,
                  requisite_replace=None, ask_del=False):
        """
        Переместить документ из одной структуры документа в другую.
        Функция является примером архивирования документа.
        @param dst_doc: Объект документа-приемника.
        @param doc_uuid: UIID переносимого документа.
            Переносимый документ может задаваться как номером так и UUID.
        @param doc_num: Номер переносимого документа.
            Если номер не определен, то перенос производиться по UUID документа.
        @param requisite_replace: Словарь замены имен реквизитов.
            Формат:
            {'Имя реквизита в документе-приемнике': 'Имя реквизита в документе-источнике'}
        @param ask_del: Спрашивать об удалении документа из источника?
        @return: True/False.
        """
        if doc_num:
            doc_uuid = self.getDocUUID(doc_num)

        if doc_uuid is None:
            log.warning(u'Не определен UUID документа для перемещения')
            return False

        return docfunc.document_remove_to(doc_uuid, self, dst_doc,
                                          requisite_replace, ask_del)


class icNodeDocumentProto(persistent.icNodePersistent, icDocumentProto):
    """
    Узловой документ.
    Узловые документы позволяют организовывать древовидные структуры из документов а также
    организовывать связи между документами типа графов в виде ссылок.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        persistent.icNodePersistent.__init__(self, *args, **kwargs)
        icDocumentProto.__init__(self, *args, **kwargs)
