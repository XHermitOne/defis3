#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль компонента доступа к историческим данным находящимся
в SQL БД в широком формате.
"""

from ic.PropertyEditor import icDefInf
from ic.components import icwidget

from ic.db import icsqlalchemy
from ic.utils import util
from ic.log import log
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg

from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

from . import history

# --- Спецификация ---
SPC_IC_SQLWIDEHISTORY = {'table': None,     # Таблица БД
                         'get_tab_name': None,  # Метод определения имени таблицы
                         'rec_filter': None,    # Дополнительная функция фильтрации исторических данных
                         '__parent__': icwidget.SPC_IC_SIMPLE,
                         '__attr_help__': {'table': u'Паспорт таблицы хранения исторических данных',
                                           'get_tab_name': u'Метод определения имени таблицы',
                                           'rec_filter': u'Дополнительная функция фильтрации исторических данных',
                                           },
                         }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSQLWideHistory'

#   Описание стилей компонента
ic_class_styles = 0

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SQLWideHistory',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__styles__': ic_class_styles,
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   icDefInf.EDT_USER_PROPERTY: ['table'],
                                   icDefInf.EDT_PY_SCRIPT: ['get_tab_name', 'rec_filter'],
                                   },
                '__parent__': SPC_IC_SQLWIDEHISTORY,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('clock-history-frame.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('clock-history-frame.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 2, 1)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('table',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('table',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Table',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является Таблицей.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('table',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icSQLWideHistory(icwidget.icSimple, history.icWideHistoryProto):
    """
    Компонент исторических данных в SQL БД широкого формата.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        history.icWideHistoryProto.__init__(self)

        # Объект таблицы исторических данных.
        self._table = None

        # Дополнительный фильтр записей
        self.rec_filter = component.get('rec_filter', None)

    def getTablePsp(self):
        """
        Паспорт таблицы исторических данных.
        @return: Паспорт или None в случае ошибки.
        """
        return self.getICAttr('table')

    def getTableName(self):
        """
        Определить имя таблицы исторических данных в БД.
        @return: Имя таблицы или None.
        """
        return self.getICAttr('get_tab_name')

    def getTable(self, table_name=None):
        """
        Объект таблицы исторических данных.
        @param table_name: Имя таблицы исторических данных, задаваемый явным образом.
            Если не определено, то задается функцией self.getTableName.
        @return: Объект таблицы исторических данных или
            None в случае ошибки.
        """
        if table_name is None:
            table_name = self.getTableName()

        if table_name is None and self._table is not None:
            # Если объект таблицы уже определен, то просто вернуть его
            return self._table
        elif table_name and self._table and self._table.getDBTableName() == table_name:
            # Необходимо проверить тали это таблица если определено имя явным образом
            return self._table

        psp = self.getTablePsp()
        if psp is not None:
            self._table = self.GetKernel().Create(psp)
            if table_name:
                self._table.setDBTableName(table_name)
        else:
            self._table = None
        return self._table

    def _do_record_filter(self, rec_filter, records):
        """
        Произвести фильтрацию записей по функции-фильтру.
        @param rec_filter: Функция дополнительного фильтра записей.
            Если фукция задается текстовым блоком кода:
            В качестве аргумента функция принимает текущую запись в виде словаря.
            В пространстве имен есть переменная RECORD, указывающая на текущую запись.
            Функция возвращает True для записи, которая попадает в результирующий список,
            False - если не попадает.
        @return: Отфильтрованный список записей.
        """
        if not rec_filter:
            # Если фильтр не указан, то возвращаем исходный список записей
            return records

        if type(rec_filter) in (str, unicode):
            # Если функция задается строкой, то необходимо правильно обработать
            # с помощью функии ic_eval
            self.evalSpace['self'] = self
            result = list()
            for record in records:
                self.evalSpace['RECORD'] = record
                err_code, expr_result = self.eval_expr(rec_filter)
                if err_code == coderror.IC_CTRL_OK and expr_result:
                    result.append(record)
            return result

        return [record for record in records if rec_filter(record)]

    def get(self, start_dt, stop_dt, rec_filter=None):
        """
        Получить исторические данные указанного диапазона.
        ВНИМАНИЕ! в таблице исторических данных должно ОБЯЗАТЕЛЬНО
        присутствовать поле <dt> в котором храниться дата-время.
        @type start_dt: datetime.datetime.
        @param start_dt: Начальное дата-время диапазона кеширования.
        @type stop_dt: datetime.datetime.
        @param stop_dt: Конечная дата-время диапазона кеширования.
        @param rec_filter: Функция дополнительного фильтра записей.
            Если функция не указана, то берется значение 'rec_filter' из спецификации.
            Если фукция задается текстовым блоком кода:
            В качестве аргумента функция принимает текущую запись в виде словаря.
            В пространстве имен есть переменная RECORD, указывающая на текущую запись.
            Функция возвращает True для записи, которая попадает в результирующий список,
            False - если не попадает.
        @return: Список записей широкого формата указанного диапазона.
            Или None в случае ошибки.
        """
        if rec_filter is None:
            rec_filter = self.rec_filter

        tab = self.getTable()
        log.debug(u'Чтение исторических данных из таблицы <%s>' % tab.getDBTableName())
        if tab:
            recordset = tab.select(tab.dataclass.c.dt.between(start_dt, stop_dt))
            records = [dict(record) for record in recordset]

            if rec_filter:
                return self._do_record_filter(rec_filter, records)
            else:
                return records
        else:
            log.warning(u'Не определена таблица хранения исторических данных в объекте <%s>' % self.name)
        return list()

    def get_tag_data(self, tag_name, start_dt, stop_dt, rec_filter=None):
        """
        Получить исторические данные указанного диапазона по определенному тегу.
        @param tag_name: Имя тега.
        @type start_dt: datetime.datetime.
        @param start_dt: Начальное дата-время диапазона кеширования.
        @type stop_dt: datetime.datetime.
        @param stop_dt: Конечная дата-время диапазона кеширования.
        @param rec_filter: Функция дополнительного фильтра записей.
            Если функция не указана, то берется значение 'rec_filter' из спецификации.
            Если фукция задается текстовым блоком кода:
            В качестве аргумента функция принимает текущую запись в виде словаря.
            В пространстве имен есть переменная RECORD, указывающая на текущую запись.
            Функция возвращает True для записи, которая попадает в результирующий список,
            False - если не попадает.
        @return: Список записей {'dt': дата-время из указанного диапазона,
                                 'data': значение тега}.
            Или None в случае ошибки.
        """
        records = self.get(start_dt, stop_dt, rec_filter=rec_filter)
        tag_data = [(rec.get('dt', None), rec.get(tag_name, 0)) for rec in records]
        # Обязательно отсортировать по времени
        tag_data.sort()
        return tag_data
