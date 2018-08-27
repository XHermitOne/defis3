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

from ic.log import log
from ic.engine import listctrl_manager
from ic.engine import ic_user

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

    def getSlaveDocument(self):
        """
        Получить ведомый объект документа для управления им.
        @return: Объект документа.
        """
        try:
            return getattr(self, DOC_NAVIGATOR_SLAVE_LIST_CTRL_NAME)
        except:
            log.fatal(u'Ошибка получения ведомый объект документа для управления им')
        return None

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
        self.setRows_list_ctrl(list_ctrl, rows=rows)

