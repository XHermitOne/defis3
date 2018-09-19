#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль прототипа компонента менеджера навигации документов.

Под навигацией понимаем весь спектр функций/методов, которые можно
выполнять над документом или списком документов.

Функции движения:
first - Переход на первый документ в списке
last - Переход на последний документ в списке
prev - Переход на предыдущий документ в списке
next - Переход на следующий документ в списке
move_to - Перемещение документа по индексу в списке
move_up - Перемещение документа вверх по списку
move_down - Перемещение документа вниз по списку
find - Поиск документа в списке документов, начиная с текущего
filter - Применить фильтр к списку документов
sort - Сортировка списка документов в заданной последовательности
reverse - Обратная сортировка списка документов в заданной последовательности
copy - Получить копию текущего документа в Clipboard
paste - Вставить копию документа в список из Clipboard'а
clone - Клонировать документ через Clipboard, но с другим UUID

Функции оперирования документом:
view - Режим просмотра текущего документа
edit - Режим редактирвания текущего документа
update - Обновление текущего документа
create - Режим создания нового документа
delete - Удаление уже созданного документа
insert - Вставить внешний документ в список по индексу
print - Режим печати текущего документа
print_all - Режим печати всех документов списка
validate - Режим проверки корректности заполнения документа
errors - Просмотр списка ошибок заполнения документа
import - Режим импорта документа из внешнего источника/файла
export - Режим экспорта документа во внешний источник/файл
send - Отправить документ по почте
save - Сохранение текущего документа в БД
save_all - Сохранение всех документов списка в БД
load - Загрузка текущего документа из БД
load_all - Загрузка всех дкументов из БД
show - Отображение текущего документа в альтернативном виде
scheme - Отобразить схему представления для текущего документа
run - Запуск текущего документа на выполнение
stop - Останов выполнения документа
do - Запуск вспомогательных операций документа (аналог проведения)
undo - Отомена вспомогательных операций документа (аналог распроведения)
open - Отрытие текущего документа для действий/операций
close - Загрытие текущего документа для действий/операций
link - Связать с текущим документом другой документ
unlink - Разорвать связь документа с текущим документом
check - Поставить дополнительную метку на текущий документ
uncheck - Снять дополнительную метку c текущего документа
attach - Вложить дополнение в текущий документ
detach - Убрать вложенное дополнение из текущего документа
calc - Произвести дополнительные расчеты связанные с текущим документом
extend - Выполнить дополнительные действия над документом
sum - Выполнить суммирование по реквизиту всех документов списка
count - Подсчет количества документов в списке
upload - Выгрузка документа на сервер
download - Загрузка документа с сервера

Дополнительные функции:
view_requisites - Изменение списка просматриваемых реквизитов в списке докумнтов
etc - Все дополнительные действия над документом или списком документов
settings - Вызов редактора дополнительных настроек документа или списка документов
help - Вызов помощи по документу или списку документов
"""

import types
import uuid
import wx

from ic.log import log
from ic.engine import listctrl_manager
from ic.engine import ic_user
from ic.dlg import ic_dlg
from ic.components import icwidget

# Версия
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_DOCUMENT_NAVIGATOR_MANAGER = {'document': None,
                                     'list_ctrl': None,
                                     'columns': None,

                                     '__parent__': icwidget.SPC_IC_SIMPLE,
                                     }

# Наименования внутренних атрибутов менеджера
DOC_NAVIGATOR_SLAVE_LIST_CTRL_NAME = '__document_navigator_slave_list_ctrl'
DOC_NAVIGATOR_SLAVE_LIST_COLUMNS_NAME = '__document_navigator_slave_list_columns'
DOC_NAVIGATOR_SLAVE_DOCUMENT_NAME = '__document_navigator_slave_document'
DOC_NAVIGATOR_DATASET_NAME = '__document_navigator_dataset'


class icDocumentNavigatorManagerProto(listctrl_manager.icListCtrlManager):
    """
    Прототип компонента менеджера навигации документов.
    """
    def setSlaveListCtrl(self, list_ctrl=None):
        """
        Установить ведомый контрол списка для отображения списка документов.
        @param list_ctrl: Контрол списка для отображения списка документов.
        """
        setattr(self, DOC_NAVIGATOR_SLAVE_LIST_CTRL_NAME, list_ctrl)

    def getSlaveListCtrl(self):
        """
        Установить ведомый контрол списка для отображения списка документов.
        @return: Контрол списка для отображения списка документов.
        """
        try:
            return getattr(self, DOC_NAVIGATOR_SLAVE_LIST_CTRL_NAME)
        except AttributeError:
            # Не определен контрол списка
            pass
        except:
            log.fatal(u'Ошибка получения ведомый контрол списка для отображения списка документов')
        return None

    def setSlaveListCtrlByPsp(self, list_ctrl_psp=None):
        """
        Установить ведомый контрол списка для отображения списка документов по его паспорту.
        @param list_ctrl_psp: Паспорт контрола списка для отображения списка документов.
        """
        if not list_ctrl_psp:
            log.warning(u'Не определен паспорт контрола списка для отображения списка документов')
            return

        try:
            kernel = ic_user.getKernel()
            if kernel:
                list_ctrl = kernel.Create(list_ctrl_psp)
                self.setSlaveListCtrl(list_ctrl)
            else:
                log.error(u'Не определен объект ядра для создания объекта %s' % list_ctrl_psp)
        except:
            log.fatal(u'Ошибка установки контрола списка %s для управления им' % list_ctrl_psp)

    def setSlaveDocumentByPsp(self, document_psp):
        """
        Установить ведомый объект документа для управления им по его паспорту.
        @param document_psp: Паспорт объекта документа.
        """
        if not document_psp:
            log.warning(u'Не определен паспорт ведомого документа для менеджера навигации')
            return

        try:
            kernel = ic_user.getKernel()
            if kernel:
                document = kernel.Create(document_psp)
                setattr(self, DOC_NAVIGATOR_SLAVE_DOCUMENT_NAME, document)
            else:
                log.error(u'Не определен объект ядра для создания объекта %s' % document_psp)
        except:
            log.fatal(u'Ошибка установки документа %s для управления им' % document_psp)

    def setSlaveDocument(self, document):
        """
        Установить ведомый объект документа для управления им.
        @param document: Объект документа.
        """
        setattr(self, DOC_NAVIGATOR_SLAVE_DOCUMENT_NAME, document)

    def _getDocIndex(self, UUID=None, index=None):
        """
        Определить индекс в датасете документа по UUID или по индексу в dataset.
        @param UUID: UUID документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @return: ИНдекс объект документа.
        """
        # Определение индекса документа
        idx = -1
        if UUID:
            dataset = self.getDocDataset()
            uuids = [doc.get('uuid', None) for doc in dataset]
            try:
                idx = uuids.index(UUID)
            except:
                log.error(u'UUID документа <%s> не найден' % UUID)
        elif index:
            idx = index
        else:
            # Текущий выбранный элемент
            list_ctrl = self.getSlaveListCtrl()
            idx = self.getItemSelectedIdx(list_ctrl)
        return idx

    def getSlaveDocument(self, UUID=None, index=None, bLoad=False):
        """
        Получить ведомый объект документа для управления им.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @param bLoad: Загрузить реквизиты документа из БД?
        @return: Объект документа.
        """
        document = None
        try:
            document = getattr(self, DOC_NAVIGATOR_SLAVE_DOCUMENT_NAME)
        except:
            log.fatal(u'Ошибка получения ведомый объект документа для управления им')

        dataset = self.getDocDataset()

        # Определение индекса документа
        idx = self._getDocIndex(UUID=UUID, index=index)

        if idx != -1:
            doc_requisites = dataset[idx]
            if document:
                doc_uuid = doc_requisites.get('uuid', None)
                if doc_uuid:
                    if bLoad:
                        # Загружаем из БД
                        document.load_obj(doc_uuid)
                    else:
                        # Просто берем из буфера
                        document.setRequisiteData(doc_requisites)

        return document

    def updateDocDataset(self):
        """
        Обновление списка документов.
        @return: Полученный список документов.
        """
        # Очистить список датасета
        self.__document_navigator_dataset = list()
        try:
            document = self.getSlaveDocument()
            self.__document_navigator_dataset = document.getDataset()
        except:
            log.fatal(u'Ошибка обновления списка документов')
        return self.__document_navigator_dataset

    def getDocDataset(self):
        """
        Текущий заполненный список документов.
        @return: Текущий заполненный список документов.
        """
        try:
            return getattr(self, DOC_NAVIGATOR_DATASET_NAME)
        except AttributeError:
            # не определен датасет
            pass
        except:
            log.fatal(u'Ошибка получения текущего заполненного списка документов')
        return list()

    def setDocDataset(self, dataset):
        """
        Установить текущий заполненный список документов.
        @return: Текущий заполненный список документов.
        """
        try:
            setattr(self, DOC_NAVIGATOR_DATASET_NAME, dataset)
            return getattr(self, DOC_NAVIGATOR_DATASET_NAME)
        except:
            log.fatal(u'Ошибка установки текущего заполненного списка документов')
        return list()

    def getDocDatasetFilter(self):
        """
        Текущий фильтр списка документов.
        @return: Текущий заполненный список документов.
        """
        try:
            document = self.getSlaveDocument()
            return document.getFilter()
        except:
            log.fatal(u'Ошибка получения текущего фильтра списка документов')
        return None

    def setDocDatasetFilter(self, doc_filter=None):
        """
        Текущий фильтр списка документов.
        @param doc_filter: Фильтр документов.
            Для создания фильтров надо пользоваться
                функциями из STD.queries.filter_generate.
                Функции генерации фильтров для вызова
                из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        @return: Текущий заполненный список документов.
        """
        try:
            document = self.getSlaveDocument()
            return document.setFilter(doc_filter)
        except:
            log.fatal(u'Ошибка получения текущего фильтра списка документов')
        return None

    def setDocDatasetRecord(self, index, doc_requisites):
        """
        Установить запись в датасете по индексу.
        @param index: Индекс записи в датасете.
        @param doc_requisites: Сохраняемый словарь значений реквизитов документа.
        @return: Обновленный список dataset.
        """
        dataset = self.getDocDataset()
        if index >= len(dataset):
            dataset.append(doc_requisites)
        else:
            dataset[index] = doc_requisites
        return dataset

    def insertDocDatasetRecord(self, index, doc_requisites):
        """
        Вставить запись в датасете по индексу.
        @param index: Индекс записи в датасете.
        @param doc_requisites: Сохраняемый словарь значений реквизитов документа.
        @return: Обновленный список dataset.
        """
        dataset = self.getDocDataset()
        if index >= len(dataset) or index < 0:
            dataset.append(doc_requisites)
        else:
            dataset.insert(index, doc_requisites)
        return dataset

    def setDocListCtrlColumns(self, *columns):
        """
        Определение колонок спискового контрола.
        @param columns: Список функций получения значений колонок.
            Если в качестве колонки передается строка, то считется что это просто
            имя реквизита.
            Если в качестве колонки передается lambda выражение/функция,
            то оно выполняется. В качестве аргумента lambda/функция должна принимать
            словарь текущей записи.
        """
        setattr(self, DOC_NAVIGATOR_SLAVE_LIST_COLUMNS_NAME, columns)

        # Если определены колонки и определен контрол списка,
        # то установить колонки в контрол
        list_ctrl = self.getSlaveListCtrl()
        doc = self.getSlaveDocument()
        if list_ctrl and columns and doc:
            cols = [dict(label=doc.findRequisite(column).getLabel(),
                         width=wx.LIST_AUTOSIZE) if isinstance(column, str) else dict(label=u'Колонка %d' % (i+1),
                                                                                      width=wx.LIST_AUTOSIZE) for i, column in enumerate(columns)]
            self.setColumns_list_ctrl(list_ctrl, cols=cols)

    def getDocListCtrlColumns(self):
        """
        Определение колонок спискового контрола.
        @return: Список функций получения значений колонок.
            Если в качестве колонки передается строка, то считется что это просто
            имя реквизита.
            Если в качестве колонки передается lambda выражение/функция,
            то оно выполняется. В качестве аргумента lambda/функция должна принимать
            словарь текущей записи.
        """
        try:
            return getattr(self, DOC_NAVIGATOR_SLAVE_LIST_COLUMNS_NAME)
        except AttributeError:
            # Не определен список колонок
            pass
        except:
            log.fatal(u'Ошибка получения колонок спискового контрола')
        return list()

    def getDocListCtrlRows(self, dataset=None, *columns):
        """
        Получение списка строк спискового контрола для заполнения.
        @param dataset: Список документов.
            Если не определен, то берется текущий заполненный.
        @param columns: Список функций получения значений колонок.
            Если в качестве колонки передается строка, то считется что это просто
            имя реквизита.
            Если в качестве колонки передается lambda выражение/функция,
            то оно выполняется. В качестве аргумента lambda/функция должна принимать
            словарь текущей записи.
        @return: Список строк спискового контрола.
        """
        if dataset is None:
            dataset = self.getDocDataset()

        if not columns:
            columns = self.getDocListCtrlColumns()

        rows = list()
        for record in dataset:
            row = list()
            for column in columns:
                value = None
                if isinstance(column, str):
                    # Это просто имя реквизита
                    value = record.get(column, None)
                elif isinstance(column, types.FunctionType):
                    try:
                        value = column(record)
                    except:
                        log.fatal(u'Ошибка выполнения функции <%s>' % str(column))
                elif isinstance(column, types.LambdaType):
                    try:
                        value = column(record)
                    except:
                        log.fatal(u'Ошибка выполнения lambda <%s>' % str(column))
                else:
                    log.warning(u'Не поддерживаемый тип колонки <%s>' % column.__class__.__name__)
                row.append(value)
            rows.append(tuple(row))
        return rows

    def refreshtDocListCtrlRows(self, rows=None):
        """
        Обновление списка строк контрола отображения списка документов.
        @param rows: Список строк.
            Если не определен, то заполняется автоматически по датасету.
        @return: True/False.
        """
        if rows is None:
            dataset = self.getDocDataset()
            rows = self.getDocListCtrlRows(dataset)

        list_ctrl = self.getSlaveListCtrl()
        self.setRows_list_ctrl(list_ctrl, rows=rows,
                               evenBackgroundColour=wx.WHITE,
                               oddBackgroundColour=wx.LIGHT_GREY)

    def refreshtDocListCtrlRow(self, index=None, row=None):
        """
        Обновление списка строк контрола отображения списка документов.
        @param index: Индекс обновляемой строки.
            Если не определен, то берется индекс текущего выбранного элемента.
        @param row: Строка в виде списка.
            Если не определен, то заполняется автоматически по датасету.
        @return: True/False.
        """
        list_ctrl = self.getSlaveListCtrl()
        if index is None:
            index = self.getItemSelectedIdx(list_ctrl)

        if index > -1:
            if row is None:
                dataset = self.getDocDataset()
                row = self.getDocListCtrlRows(dataset)[index]

            self.setRow_list_ctrl(list_ctrl, row_idx=index, row=row,
                                  evenBackgroundColour=wx.WHITE,
                                  oddBackgroundColour=wx.LIGHT_GREY)

    # --- Функции движения ---
    def selectItem(self, UUID=None, index=None):
        """
        Передвинуть фокус к ...
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID редактируемого документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @return: Новый индекс.
        """
        idx = self._getDocIndex(UUID=UUID, index=index)
        if idx > -1:
            list_ctrl = self.getSlaveListCtrl()
            if list_ctrl:
                self.selectItem_list_ctrl(ctrl=list_ctrl, item_idx=idx)
            else:
                log.warning(u'Не определен контрол списка манеджера навигации документов')
        return idx

    def selectFirst(self):
        """
        Передвинуть фокус на первый элемент списка.
        """
        return self.selectItem(index=0)

    def selectLast(self):
        """
        Передвинуть фокус на последний элемент списка.
        """
        last_idx = self.getItemCount(self.getSlaveListCtrl()) - 1
        return self.selectItem(index=last_idx)

    def selectPrev(self, UUID=None, index=None):
        """
        Передвинуть фокус на предыдущий элемент списка.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID редактируемого документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @return: Новый индекс.
        """
        idx = self._getDocIndex(UUID=UUID, index=index)
        idx -= 1
        idx = 0 if idx < 0 else idx
        self.selectItem(index=idx)

    def selectNext(self, UUID=None, index=None):
        """
        Передвинуть фокус на следующий элемент списка.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID редактируемого документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @return: Новый индекс.
        """
        idx = self._getDocIndex(UUID=UUID, index=index)
        idx += 1
        last_idx = self.getItemCount(self.getSlaveListCtrl()) - 1
        idx = last_idx if idx > last_idx else idx
        self.selectItem(index=idx)

    def moveTo(self, fromUUID=None, fromIndex=None, toIndex=None, bRefresh=True):
        """
        Перемещение документа с индекса fromindex на индекс toIndex в списке документов.
        @param fromUUID: UUID перемещаемого документа если необходимо.
        @param fromIndex: Индекс перемещаемого документа в списке документов.
        @param toIndex: Новый индекс документа.
        @param bRefresh: Сделать автоматическое обновление.
        @return: Новый индекс документа.
        """
        dataset = self.getDocDataset()
        from_idx = self._getDocIndex(UUID=fromUUID, index=fromIndex)
        last_idx = self.getItemCount(self.getSlaveListCtrl()) - 1

        if isinstance(toIndex, int) and 0 <= toIndex <= last_idx:
            dataset[toIndex] = dataset[from_idx]
            del dataset[fromIndex]
            if bRefresh:
                self.refreshtDocListCtrlRows()

    def moveDown(self, fromUUID=None, fromIndex=None, stepIndex=1, bRefresh=True):
        """
        Перемещение документа с индекса fromindex на stepIndex ниже в списке документов.
        @param fromUUID: UUID перемещаемого документа если необходимо.
        @param fromIndex: Индекс перемещаемого документа в списке документов.
        @param stepIndex: Шаг индекса. На сколько сделать перемещение.
        @param bRefresh: Сделать автоматическое обновление.
        @return: Новый индекс документа.
        """
        dataset = self.getDocDataset()
        from_idx = self._getDocIndex(UUID=fromUUID, index=fromIndex)
        last_idx = self.getItemCount(self.getSlaveListCtrl()) - 1
        to_idx = max(min(from_idx - stepIndex, last_idx), 0)

        dataset[to_idx] = dataset[from_idx]
        del dataset[fromIndex]

        if bRefresh:
            self.refreshtDocListCtrlRows()

    def moveUp(self, fromUUID=None, fromIndex=None, stepIndex=1, bRefresh=True):
        """
        Перемещение документа с индекса fromindex на stepIndex выше в списке документов.
        @param fromUUID: UUID перемещаемого документа если необходимо.
        @param fromIndex: Индекс перемещаемого документа в списке документов.
        @param stepIndex: Шаг индекса. На сколько сделать перемещение.
        @param bRefresh: Сделать автоматическое обновление?
        @return: Новый индекс документа.
        """
        dataset = self.getDocDataset()
        from_idx = self._getDocIndex(UUID=fromUUID, index=fromIndex)
        last_idx = self.getItemCount(self.getSlaveListCtrl()) - 1
        to_idx = max(min(from_idx + stepIndex, last_idx), 0)

        dataset[to_idx] = dataset[from_idx]
        del dataset[fromIndex]

        if bRefresh:
            self.refreshtDocListCtrlRows()

    def findDoc(self, requisite=None, value=None, fromUUID=None, fromIndex=None, bSelect=True):
        """
        Поиск документа по значению реквизита начиная с текущего.
        @param requisite: Имя реквизита по которому надо производить поиск.
        @param value: Искомое значение.
        @param fromUUID: UUID текущего документа если необходимо.
        @param fromIndex: Индекс текущего документа в списке документов.
        @param bSelect: Автоматически выделить искомый документ в списке?
        @return: Индекс искомого документа или -1, если не найден документ.
        """
        from_idx = self._getDocIndex(UUID=fromUUID, index=fromIndex)
        last_idx = self.getItemCount(self.getSlaveListCtrl()) - 1
        for idx in range(from_idx, last_idx):
            document = self.getSlaveDocument(index=idx)
            requisite_value = document.getRequisiteValue(requisite)
            if isinstance(requisite_value, str):
                # Проверка на вхождение подстроки в строку
                if str(value) in requisite_value:
                    if bSelect:
                        self.selectItem_list_ctrl(self.getSlaveListCtrl(), item_idx=idx)
                    return idx
            else:
                # Проверка на точное совпадение
                if value == requisite_value:
                    if bSelect:
                        self.selectItem_list_ctrl(self.getSlaveListCtrl(), item_idx=idx)
                    return idx
        # Ничего не найдено
        if ic_dlg.icAskBox(u'ПОИСК', u'Документ не найден в списке. Начать поиск с начала?'):
            return self.findDoc(requisite, value, fromIndex=0, bSelect=bSelect)
        return -1

    def filterDocs(self, doc_filter=None, bRefresh=True):
        """
        Отфильтровать список документов.
        @param doc_filter: Словарь значений реквизитов фильтров.
            Если None, то берется текущий фильтр бизнес объектов.
            Для создания фильтров надо пользоваться
            функциями из STD.queries.filter_generate.
            Функции генерации фильтров для вызова
            из функций прикладного уровня.
            Использование:
                create_filter_group_AND(create_filter_compare_requisite('field1', '==', 'FFF'))
        @return: Возвращает список-dataset объектов, соответствующих заданному фильтру.
        """
        self.setDocDatasetFilter(doc_filter)
        dataset = self.updateDocDataset()
        if bRefresh:
            self.refreshtDocListCtrlRows()
        return dataset

    def sortDocs(self, *sort_fields):
        """
        Сортировка списка документов.
        @param sort_fields: Список порядка сортировки списка документов.
            В качестве поля сортировки может выступать имя реквизита или
            функция или lambda выражение.
            В случае функции или lambda-выражения они должны принимать
            в качестве аргумента словарь записи документа и возвращать
            значение по которому будет производиться сортитровка.
        @return: Отсортированный список документов.
        """
        dataset = self.getDocDataset()

        do_refresh = False
        try:
            dataset = sorted(dataset,
                             key=lambda rec: [rec[field] if isinstance(field, str) else field(rec) for field in sort_fields],
                             reverse=False)
            do_refresh = True
        except:
            log.fatal(u'Ошибка сортировки списка документов')

        if do_refresh:
            self.setDocDataset(dataset)
            self.refreshtDocListCtrlRows()

    def sortReverseDocs(self, *sort_fields):
        """
        Обратная сортировка списка документов.
        @param sort_fields: Список порядка сортировки списка документов.
            В качестве поля сортировки может выступать имя реквизита или
            функция или lambda выражение.
            В случае функции или lambda-выражения они должны принимать
            в качестве аргумента словарь записи документа и возвращать
            значение по которому будет производиться сортитровка.
        @return: Отсортированный список документов.
        """
        dataset = self.getDocDataset()

        do_refresh = False
        try:
            dataset = sorted(dataset,
                             key=lambda rec: [rec[field] if isinstance(field, str) else field(rec) for field in sort_fields],
                             reverse=True)
            do_refresh = True
        except:
            log.fatal(u'Ошибка обратной сортировки списка документов')

        if do_refresh:
            self.setDocDataset(dataset)
            self.refreshtDocListCtrlRows()

    def copyDoc(self, UUID=None, index=None):
        """
        Копировать документ в клипбоард.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID редактируемого документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @return: Скопированный словарь значений реквизитов документа.
        """
        idx = self._getDocIndex(UUID=UUID, index=index)
        doc_requisites = None
        if idx > -1:
            dataset = self.getDocDataset()
            doc_requisites = dataset[idx]
            txt_data_obj = wx.TextDataObject()
            txt_data_obj.SetText(str(doc_requisites))
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(txt_data_obj)
                wx.TheClipboard.Close()
            else:
                msg = u'Ошибка открытия клипбоарда'
                log.warning(msg)
                ic_dlg.icWarningBox(u'ОШИБКА', msg)
        return doc_requisites

    def pasteDoc(self, index=None):
        """
        Вставить документ из клипбоарда в датасет.
        @param index: Индекс документа в dataset.
            Если index не указываются,
            то берется текущий выделенный документ.
        @return: Скопированный словарь значений реквизитов документа.
        """
        doc_requisites = None
        if not wx.TheClipboard.IsOpened():
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                doc_requisites = eval(do.GetText())
                # ВНИМАНИЕ! Необходимо поменять UUID документа при вставке
                # чтобы документы различались
                doc_requisites['uuid'] = str(uuid.uuid4())
            else:
                log.warning(u'Клипбоард пуст')

        if doc_requisites:
            idx = self._getDocIndex(index=index)
            self.insertDocDatasetRecord(idx, doc_requisites)

    def cloneDoc(self, UUID=None, index=None):
        """
        Клонироваь документа в списке документов.
        @param UUID:
        @param index:
        @return:
        """
        self.copyDoc(UUID=UUID, index=index)
        self.pasteDoc(index=index + 1)

    # --- Функции оперирования документом ---
    def viewDoc(self, UUID=None, index=None, view_form_method=None):
        """
        Просмотр документа.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID редактируемого документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @param view_form_method: Метод вызова формы просмотра документа.
            Может задаваться фукнцией.
            Если не определен, то вызывается document.View().
        @return: True/False
        """
        document = self.getSlaveDocument(UUID=UUID, index=index)
        if document:
            log.debug(u'Просмотр документа UUID <%s>' % document.getUUID())

            if view_form_method:
                result = view_form_method(document)
            else:
                result = document.View()
            return result
        else:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ для просмотра')
        return False

    def editDoc(self, UUID=None, index=None, edit_form_method=None):
        """
        Редактирование документа.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID редактируемого документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @param edit_form_method: Метод вызова формы редактирования документа.
            Может задаваться фукнцией.
            Если не определен, то вызывается document.Edit().
        @return: True/False
        """
        document = self.getSlaveDocument(UUID=UUID, index=index)
        if document:
            log.debug(u'Редактирование документа UUID <%s>' % document.getUUID())

            if edit_form_method:
                result = edit_form_method(document)
            else:
                result = document.Edit()

            if result:
                document.save_obj()
                # Определение индекса документа
                idx = self._getDocIndex(UUID=UUID, index=index)
                # Обновить выделенный документ после радактирования
                self.setDocDatasetRecord(index=idx, doc_requisites=document.getRequisiteData())
                # Обновить список документов если нормально отредактировали документ
                self.refreshtDocListCtrlRows()
            return result
        else:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ для редактирования')
        return False

    def updateDoc(self, UUID=None, index=None, update_form_method=None):
        """
        Обновить документ. По умолчанию обновляется из БД.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID редактируемого документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @param update_form_method: Метод вызова формы обновления документа.
            Может задаваться фукнцией.
            Если не определен, то вызывается document.load_obj().
        @return: True/False
        """
        document = self.getSlaveDocument(UUID=UUID, index=index)
        if document:
            log.debug(u'Обновление документа UUID <%s>' % document.getUUID())

            if update_form_method:
                result = update_form_method(document)
            else:
                doc_requisites = document.load_obj()
                idx = self._getDocIndex(UUID=UUID, index=index)
                self.setDocDatasetRecord(idx, doc_requisites)
                result = True

            if result:
                # Обновить список документов если нормально отредактировали документ
                self.refreshtDocListCtrlRows()
            return result
        else:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ для обновления')
        return False

    def createDoc(self, create_form_method=None):
        """
        Создать документ.
        Документ может задаваться по UUID или по индексу в dataset.
        @param create_form_method: Метод вызова формы создания документа.
            Может задаваться фукнцией.
            Если не определен, то вызывается document.Add().
        @return: True/False.
        """
        document = self.getSlaveDocument()
        log.debug(u'Создание документа')

        if create_form_method:
            result = create_form_method(document)
        else:
            result = document.Add()

        if result:
            # Обновить список документов если нормально выполнили действие над документ
            self.refreshtDocListCtrlRows()
        return result

    def deleteDoc(self, UUID=None, index=None, delete_form_method=None):
        """
        Удалить документ.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID редактируемого документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @param delete_form_method: Метод вызова формы удаления документа.
            Может задаваться фукнцией.
            Если не определен, то вызывается document.Del().
        @return: True/False
        """
        document = self.getSlaveDocument(UUID=UUID, index=index)
        if document:
            log.debug(u'Удаление документа UUID <%s>' % document.getUUID())

            if delete_form_method:
                result = delete_form_method(document)
            else:
                result = document.Del()

            if result:
                # Обновить список документов если нормально отредактировали документ
                self.refreshtDocListCtrlRows()
            return result
        else:
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Выберите документ для удаления')
        return False

    def insertDoc(self, UUID=None, index=None, insert_form_method=None):
        """
        """
        log.warning(u'Метод <insertDoc> не реализован')

    def printDoc(self, UUID=None, index=None, print_form_method=None):
        """
        """
        log.warning(u'Метод <printDoc> не реализован')

    def printAllDoc(self, print_form_method=None):
        """
        """
        log.warning(u'Метод <printAllDoc> не реализован')

    def validateDoc(self, UUID=None, index=None, validate_form_method=None):
        """
        """
        log.warning(u'Метод <validateDoc> не реализован')

    def errorsDoc(self, UUID=None, index=None, errors_form_method=None):
        """
        """
        log.warning(u'Метод <errorsDoc> не реализован')

    def importDoc(self, UUID=None, index=None, import_form_method=None):
        """
        """
        log.warning(u'Метод <importDoc> не реализован')

    def exportDoc(self, UUID=None, index=None, import_form_method=None):
        """
        """
        log.warning(u'Метод <exportDoc> не реализован')

    def sendDoc(self, UUID=None, index=None, send_form_method=None):
        """
        """
        log.warning(u'Метод <sendDoc> не реализован')

    def saveDoc(self, UUID=None, index=None, save_form_method=None):
        """
        """
        log.warning(u'Метод <saveDoc> не реализован')

    def saveAllDoc(self, save_form_method=None):
        """
        """
        log.warning(u'Метод <saveAllDoc> не реализован')

    def loadDoc(self, UUID=None, index=None, load_form_method=None):
        """
        """
        log.warning(u'Метод <loadDoc> не реализован')

    def loadAllDoc(self, load_form_method=None):
        """
        """
        log.warning(u'Метод <loadAllDoc> не реализован')

    def showDoc(self, UUID=None, index=None, show_form_method=None):
        """
        """
        log.warning(u'Метод <showDoc> не реализован')

    def schemeDoc(self, UUID=None, index=None, scheme_form_method=None):
        """
        """
        log.warning(u'Метод <schemeDoc> не реализован')

    def runDoc(self, UUID=None, index=None, run_form_method=None):
        """
        """
        log.warning(u'Метод <runDoc> не реализован')

    def stopDoc(self, UUID=None, index=None, stop_form_method=None):
        """
        """
        log.warning(u'Метод <stopDoc> не реализован')

    def doDoc(self, UUID=None, index=None, do_form_method=None):
        """
        """
        log.warning(u'Метод <doDoc> не реализован')

    def undoDoc(self, UUID=None, index=None, undo_form_method=None):
        """
        """
        log.warning(u'Метод <undoDoc> не реализован')

    def openDoc(self, UUID=None, index=None, open_form_method=None):
        """
        """
        log.warning(u'Метод <openDoc> не реализован')

    def closeDoc(self, UUID=None, index=None, close_form_method=None):
        """
        """
        log.warning(u'Метод <closeDoc> не реализован')

    def linkDoc(self, UUID=None, index=None, link_form_method=None):
        """
        """
        log.warning(u'Метод <linkDoc> не реализован')

    def unlinkDoc(self, UUID=None, index=None, unlink_form_method=None):
        """
        """
        log.warning(u'Метод <unlinkDoc> не реализован')

    def checkDoc(self, UUID=None, index=None, check_form_method=None):
        """
        """
        log.warning(u'Метод <checkDoc> не реализован')

    def uncheckDoc(self, UUID=None, index=None, uncheck_form_method=None):
        """
        """
        log.warning(u'Метод <uncheckDoc> не реализован')

    def attachDoc(self, UUID=None, index=None, attach_form_method=None):
        """
        """
        log.warning(u'Метод <attachDoc> не реализован')

    def detachDoc(self, UUID=None, index=None, detach_form_method=None):
        """
        """
        log.warning(u'Метод <detachDoc> не реализован')

    def calcDoc(self, doc_requisite):
        """
        """
        log.warning(u'Метод <calcDoc> не реализован')

    def sumDoc(self, doc_requisite):
        """
        Выполнить суммирование по реквизиту всех документов списка.
        @param doc_requisite: Имя реквизита, по которому производится суммирование.
        @return: Расчетная сумма.
        """
        dataset = self.getDocDataset()
        result_sum = 0.0
        try:
            requisite_values = [doc_requisites.get(doc_requisite, 0.0) for doc_requisites in dataset]
            requisite_values = [value if isinstance(value, int) or isinstance(value, float) else float(value) for value in requisite_values]
            result_sum = sum(requisite_values)
        except:
            log.fatal(u'Ошибка суммирования по реквизиту <%s> всех документов списка' % doc_requisite)
        return result_sum

    def countDoc(self):
        """
        Выполнить подсчет количества всех документов списка.
        @return: Расчетное количество.
        """
        dataset = self.getDocDataset()
        return len(dataset)

    def extendDoc(self, UUID=None, index=None, extend_form_method=None):
        """
        """
        log.warning(u'Метод <extendDoc> не реализован')

    def uploadDoc(self, UUID=None, index=None, upload_form_method=None):
        """
        """
        log.warning(u'Метод <uploadDoc> не реализован')

    def downloadDoc(self, UUID=None, index=None, download_form_method=None):
        """
        """
        log.warning(u'Метод <downloadDoc> не реализован')

    # --- Дополнительные функции ---
    def viewRequisites(self):
        """
        """
        log.warning(u'Метод <viewRequisites> не реализован')

    def etc(self):
        """
        """
        log.warning(u'Метод <etc> не реализован')

    def editSettings(self):
        """
        """
        log.warning(u'Метод <editSettings> не реализован')

    def showHelp(self):
        """
        """
        log.warning(u'Метод <showHelp> не реализован')
