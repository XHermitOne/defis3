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
sort - Сортировка списка документов в заданной последовательности
reverse - Обратная сортировка списка документов в заданной последовательности
find - Поиск документа в списке документов, начиная с текущего
copy - Получить копию текущего документа в Clipboard
paste - Вставить копию документа в список из Clipboard'а
clone - Клонировать документ через Clipboard, но с другим UUID
filter - Применить фильтр к списку документов

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
send - Отправить документа по почте
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
import wx

from ic.log import log
from ic.engine import listctrl_manager
from ic.engine import ic_user
from ic.dlg import ic_dlg

# Версия
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_DOCUMENT_NAVIGATOR_MANAGER = {}

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
                setattr(self, DOC_NAVIGATOR_SLAVE_LIST_CTRL_NAME, document)
            else:
                log.error(u'Не определен объект ядра для создания объекта %s' % document_psp)
        except:
            log.fatal(u'Ошибка установки документа %s для управления им' % document_psp)

    def setSlaveDocument(self, document):
        """
        Установить ведомый объект документа для управления им.
        @param document: Объект документа.
        """
        setattr(self, DOC_NAVIGATOR_SLAVE_LIST_CTRL_NAME, document)

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

    def getSlaveDocument(self, UUID=None, index=None):
        """
        Получить ведомый объект документа для управления им.
        Документ может задаваться по UUID или по индексу в dataset.
        @param UUID: UUID документа.
        @param index: Индекс документа в dataset.
            Если ни UUID ни index не указываются,
            то берется текущий выделенный документ.
        @return: Объект документа.
        """
        document = None
        try:
            document = getattr(self, DOC_NAVIGATOR_SLAVE_LIST_CTRL_NAME)
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
                    document.load_obj(doc_uuid)

        return document

    def updateDocDataset(self, ext_filter=None):
        """
        Обновление списка документов.
        @param ext_filter: Дополнительный фильтр документов.
            Если фильтр не указан, то беруться все документы.
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
        except:
            log.fatal(u'Ошибка получения текущего заполненного списка документов')
        return list()

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

    # --- Функции оперирования документом ---
    def viewDocument(self, UUID=None, index=None, view_form_method=None):
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

    def editDocument(self, UUID=None, index=None, edit_form_method=None):
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

    def sumDocument(self, doc_requisite):
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

    def countDocument(self):
        """
        Выполнить подсчет количества всех документов списка.
        @return: Расчетное количество.
        """
        dataset = self.getDocDataset()
        return len(dataset)

    # --- Дополнительные функции ---
