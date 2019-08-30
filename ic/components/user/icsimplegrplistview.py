#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ПРОСТОЙ СПИСОК ОБЪЕКТОВ с группировкой по полям.
Класс пользовательского компонента ПРОСТОЙ СПИСОК ОБЪЕКТОВ с группировкой по полям.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx

from ic.components import icwidget
from ic.utils import util
from ic.utils import toolfunc
from ic.dlg import dlgfunc
from ic.bitmap import bmpfunc
from ic.utils import coderror
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf
from ic.log import log
from ic.utils import wxfunc

import ic.contrib.ObjectListView as parentModule

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icComboType

#   Имя класса
ic_class_name = 'icSimpleGroupListView'

#   Описание стилей компонента
ic_class_styles = {# 'DEFAULT': 0,
                   # wx.ListCtrl styles
                   'LC_LIST': wx.LC_LIST,
                   'LC_REPORT': wx.LC_REPORT,
                   'LC_VIRTUAL': wx.LC_VIRTUAL,
                   'LC_ICON': wx.LC_ICON,
                   'LC_SMALL_ICON': wx.LC_SMALL_ICON,
                   'LC_ALIGN_TOP': wx.LC_ALIGN_TOP,
                   'LC_ALIGN_LEFT': wx.LC_ALIGN_LEFT,
                   'LC_AUTOARRANGE': wx.LC_AUTOARRANGE,
                   'LC_EDIT_LABELS': wx.LC_EDIT_LABELS,
                   'LC_NO_HEADER': wx.LC_NO_HEADER,
                   'LC_SINGLE_SEL': wx.LC_SINGLE_SEL,
                   'LC_SORT_ASCENDING': wx.LC_SORT_ASCENDING,
                   'LC_SORT_DESCENDING': wx.LC_SORT_DESCENDING,
                   'LC_HRULES': wx.LC_HRULES,
                   'LC_VRULES': wx.LC_VRULES,
                   #
                   'SUNKEN_BORDER': wx.SUNKEN_BORDER,
                   }

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SimpleGroupListView',
                'name': 'default',
                'description': None,
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                'evenRowsBackColour': None,
                'oddRowsBackColour': None,

                'foregroundColour': None,
                'backgroundColour': None,

                'data_src': None,  # Паспорт источника данных
                'get_dataset': None,   # Функция получения данных в виде списка словарей

                'sortable': True,      # Можно сортировать?
                'selected': None,      # Выбор элемента
                'activated': None,     # Активация элемента
                'conv_record': None,   # Преобразование записи
                'conv_dataset': None,  # Преобразование набора записи

                'row_text_colour': None,        # Получение цвета текста строки
                'row_background_colour': None,  # Получение цвета фона строки

                'show_item_counts': False,  # Признак отображения количесва элементов группы

                '__styles__': ic_class_styles,
                '__events__': {'selected': ('wx.EVT_LIST_ITEM_SELECTED', 'onItemSelected', False),
                               'activated': ('wx.EVT_LIST_ITEM_ACTIVATED', 'onItemActivated', False),
                               'conv_record': (None, None, False),  # Преобразование записи
                               'conv_dataset': (None, None, False),  # Преобразование набора записи

                               'row_text_colour': (None, None, False),  # Получение цвета текста строки
                               'row_background_colour': (None, None, False),  # Получение цвета фона строки
                               },
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_CHECK_BOX: ['activate', 'sortable', 'show_item_counts'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_COLOR: ['evenRowsBackColour', 'oddRowsBackColour',
                                                        'foregroundColour', 'backgroundColour'],
                                   icDefInf.EDT_USER_PROPERTY: ['data_src'],
                                   icDefInf.EDT_PY_SCRIPT: ['conv_record', 'conv_dataset', 
                                                            'row_text_colour', 'row_background_colour']
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                '__attr_hlp__': {'data_src': u'Паспорт источника данных',
                                 'get_dataset': u'Функция получения данных в виде списка словарей',

                                 'sortable': u'Можно сортировать?',
                                 'selected': u'Выбор элемента',
                                 'activated': u'Активация элемента',
                                 'conv_record': u'Преобразование записи',
                                 'conv_dataset': u'Преобразование набора записи',

                                 'row_text_colour': u'Получение цвета текста строки',
                                 'row_background_colour': u'Получение цвета фона строки',

                                 'show_item_counts': u'Признак отображения количесва элементов группы',
                                 },
                }


#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('table-heatmap.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('table-heatmap.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['GridCell']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None

    if attr in ('data_src',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('data_src',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Document',
                                 'StateObj',
                                 'BusinessObj',
                                 'Table',
                                 'GridDataset',
                                 'Recordset',
                                 'Query',
                                 'AccumulatingRegistry'):
                dlgfunc.openWarningBox(u'ОШИБКА', u'Выбранный объект не является ИСТОЧНИКОМ ДАННЫХ.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('data_src',):
        return pspEdt.str_to_val_user_property(text, propEdt)
    return pspEdt.str_to_val_user_property(text, propEdt)


class icSimpleGroupListView(icwidget.icWidget, parentModule.GroupListView):
    """
    Простой список объектов.

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
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        # Свойства компонента
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]

        for key in lst_keys:
            setattr(self, key, component[key])

        style = component['style']  # wx.LC_REPORT | wx.SUNKEN_BORDER
        parentModule.GroupListView.__init__(self, parent, id,
                                            style=style,
                                            sortable=self.sortable,
                                            useAlternateBackColors=True,
                                            showItemCounts=self.show_item_counts)

        # Цвет фона линий четных/не четных
        colour = self.getICAttr('evenRowsBackColour')
        if colour:
            self.evenRowsBackColor = colour
        else:
            self.evenRowsBackColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
        colour = self.getICAttr('oddRowsBackColour')
        if colour:
            self.oddRowsBackColor = colour
        else:
            self.oddRowsBackColor = wxfunc.getTintColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX))

        self._data_src_obj = None

        # Установить колонки
        self.setColumnsSpc(*self.resource['child'])
        self.rowFormatter = self.rowFormatterFunction

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, id=self.GetId())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated, id=self.GetId())
        self.BindICEvt()

        self.SetFocus()

        # По умолчанию после создания объекта обновить
        # его наполнение
        self.refreshDataset()

    def getDataSource(self):
        """
        Источник данных.
        """
        return self._data_src_obj

    def setDataSource(self, data_source):
        """
        Источник данных.
        """
        self._data_src_obj = data_source

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def _str2unicode(self, Value_):
        """
        Приведение всех надписей к юникоду.
        """
        if not isinstance(Value_, str):
            Value_ = str(Value_)
        if isinstance(Value_, str):
            return Value_
        return u''

    def setColumnsSpc(self, *Columns_):
        """
        Создание колонок грида по описанию.
        @param Columns_: Описание колонок.
        """
        columns = []
        auto_sort_col = None
        for column in Columns_:
            activate = column['activate']
            if not activate:
                # Пропустить отключенные колонки
                continue

            name = column['name']
            label = self._str2unicode(column['label'])
            width = column.get('width', 100)
            new_col = parentModule.ColumnDefn(title=label,
                                              align='left',
                                              width=width,
                                              valueGetter=name,
                                              minimumWidth=40,
                                              maximumWidth=400,
                                              groupKeyGetter=self.create_getColGroupKey_function(column),
                                              groupKeyConverter=self.create_convertColGroupKey_function(column)
                                              )
            if column['sort'] in ('True', True, 1, '1'):
                # Если установлена сортировка, то сделать
                # колонку автоматически сортируемой
                auto_sort_col = new_col

            columns.append(new_col)
        if columns:
            self.SetColumns(columns)

            if auto_sort_col:
                self.SetSortColumn(auto_sort_col)

    def create_getColGroupKey_function(self, column):
        """
        Создание функции получения ключа колонки.
        @param column: Структура описания колонки.
        """
        get_grp_key = column.get('get_grp_key', None)
        if get_grp_key:
            def getColGroupKey(RECORD):
                """
                Получить ключ группы колонки.
                @param RECORD: Словарь записи.
                """
                result = util.ic_eval(get_grp_key, evalSpace=locals())
                try:
                    log.info(u'Определение ключа группы колонки <%s>. Результат <%s>' % (column['name'],
                                                                                               result))
                except:
                    pass
                return result[1]

            return getColGroupKey
        return None

    def create_convertColGroupKey_function(self, column):
        """
        @param column: Структура описания колонки.
        """
        get_grp_title = column.get('get_grp_title', None)
        if get_grp_title:
            def convertColGroupKey(GROUP_KEY):
                """
                Преобразовать данный ключ группы в строку заголовка группы колонки.
                @param GROUP_KEY: Ключ группы.
                """
                result = util.ic_eval(get_grp_title, evalSpace=locals())
                try:
                    log.info(u'Определение заголовка группы колонки <%s>. Результат <%s>' % (column['name'],
                                                                                                   result))
                except:
                    pass
                return result[1]

            return convertColGroupKey
        return None

    def getDatasetFromDataSource(self, data_source=None, data_src_filter=None):
        """
        Получить набор данных из источника данных.
        @param data_source: Указание источника данных.
            Может указываться как паспорт или объект.
        @param data_src_filter: Дополнительный фильтр источника данных.
        @return: Список данных.
        """
        if not self._data_src_obj:
            self._data_src_obj = None
            if toolfunc.is_pasport(data_source):
                # Источник данных задается паспортом
                self._data_src_obj = self.GetKernel().Create(data_source)
            else:
                # Источник данных задается объектом
                self._data_src_obj = data_source
        if self._data_src_obj:
            if data_src_filter:
                self._data_src_obj.setFilter(data_src_filter)
            return self._data_src_obj.getDataDict()
        else:
            log.warning(u'Не определен источник данных в объекте <%s>' % self.name)
        return None

    def setDataset(self, DatasetList_=None, data_src_filter=None):
        """
        Установка набора данных объектов.
            ВНИМАНИЕ! В контекст объекта при обработке
            скриптов <conv_dataset> и <conv_record> передаются
            дополнительные объекты:
                DATASET - список записей.
                RECORD - словарь текущей обрабатываемой записи.
        @param data_src_filter: Дополнительный фильтр источника данных.
        """
        if DatasetList_ is None:
            if not self.data_src and not self._data_src_obj:
                # Набор данных задается явно
                ret, val = self.eval_attr('get_dataset')
                DatasetList_ = val
            elif self.data_src:
                # Если набор данных не определен, то получить
                # этот набор из источника данных
                DatasetList_ = self.getDatasetFromDataSource(self.data_src, data_src_filter)
            elif self._data_src_obj:
                # Если набор данных не определен, то получить
                # этот набор из источника данных
                DatasetList_ = self.getDatasetFromDataSource(self._data_src_obj, data_src_filter)

        if DatasetList_ is None:
            log.warning(u'Not define DATASET for object <%s>. DataSource: <%s>' % (self.name, self._data_src_obj))
        else:
            if self.isICAttrValue('conv_dataset'):
                # Определена функция преобразования датасета
                # Передаем ей управление
                self.context['DATASET'] = DatasetList_
                DatasetList_ = self.getICAttr('conv_dataset')

        if self.isICAttrValue('conv_record'):
            # Определена функция преобразования записи
            dataset = []
            for record in DatasetList_:
                self.context['RECORD'] = record
                new_record = self.getICAttr('conv_record')
                dataset.append(new_record)
        else:
            # Записи передаются контролу без изменения
            dataset = DatasetList_

        return self.SetObjects(dataset)

    def refreshDataset(self, data_src_filter=None):
        """
        Обновить набор данныхю
        @param data_src_filter: Дополнительный фильтр источника данных.
        """
        return self.setDataset(data_src_filter=data_src_filter)

    #   Обработчики событий
    def onItemSelected(self, event):
        """ 
        Обрабатываем сообщение о выборе строки списка.
        """
        self.SetFocus()
        event.Skip()
        result = True
        currentItem = self.GetFocusedRow()
        #   Формируем пространство имен
        self.evalSpace['event'] = event
        self.evalSpace['evt'] = event
        self.evalSpace['row'] = currentItem

        self.evalSpace['values']=self.GetObjectAt(currentItem)
        self.evalSpace['_lfp'] = {'function': 'onItemSelected', 'event': event,
                                  'currentItem': currentItem, 'row': currentItem, 'self': self}
        
        if not self.getSelectedRecord() in [None, '', 'None']:
            ret, val = self.eval_attr('selected')
            if ret:
                result = bool(val)

    def onItemActivated(self, event):
        """ 
        Активация (Enter/DobleClick) строки.
        """
        currentItem = self.GetFocusedRow()
        rowData = []
        #   Формируем пространство имен
        self.evalSpace['event'] = event
        self.evalSpace['evt'] = event
        self.evalSpace['row'] = currentItem
        
        rowDict = self.GetObjectAt(currentItem)
        self.evalSpace['values'] = rowDict
        self.evalSpace['_lfp'] = {'function': 'onItemActivated',
                                  'event': event, 'currentItem': currentItem,
                                  'result': rowDict, 'self': self}
        self.eval_attr('activated')
        event.Skip()
        
    #   Свойства
    def getSelectedRecord(self):
        """
        Выбранная запись.
        """
        return self.GetSelectedObject()
    
    def getSelectedObjUUID(self):
        """
        Определить UUID выбранного объекта.
        Мнемоническое правило расположения UUID объекта в наборе записей:
        Поле UUIDа находится всегда последней колонкой и не выводится на экран.
        @return: Возвращает uuid выбранного объекта или None если 
        объект не выбран.
        """
        selected_rec = self.getSelectedRecord()
        if selected_rec:
            if isinstance(selected_rec, dict):
                return selected_rec.get('uuid', None)
            else:
                return selected_rec[self.getColumnCount()]
        return None

    def getColumnCount(self):
        """
        Количество колонок.
        """
        return len(self.columns)

    def rowFormatterFunction(self, list_item, record):
        """
        Функция раскраски строк списка.
        @param list_item: Объект wx.ListItem строки списка.
        @param record: Словарь записи.
        """
        self.context['RECORD'] = record
        text_colour = self.getICAttr('row_text_colour')
        bg_colour = self.getICAttr('row_background_colour')

        if text_colour and isinstance(text_colour, wx.Colour):
            list_item.SetTextColour(text_colour)
        elif self.foregroundColour:
            text_colour = wx.Colour(*self.foregroundColour)
            list_item.SetTextColour(text_colour)

        if bg_colour and isinstance(bg_colour, wx.Colour):
            list_item.SetBackgroundColour(bg_colour)
        elif self.backgroundColour:
            bg_colour = wx.Colour(*self.backgroundColour)
            list_item.SetBackgroundColour(bg_colour)


def test():
    """
    Функция тестирования.
    """
    columns = [
            parentModule.ColumnDefn(u"Заголовок", "left", 160, valueGetter="title", minimumWidth=40, maximumWidth=200),
            parentModule.ColumnDefn(u"Исполнитель", "left", 150, valueGetter="artist", minimumWidth=40,
                                    maximumWidth=200, autoCompleteCellEditor=True, headerImage="star"),
            parentModule.ColumnDefn(u"Альбом", "left", 150, valueGetter="album", maximumWidth=250, isSpaceFilling=True,
                                    autoCompleteCellEditor=True, headerImage=2),
            parentModule.ColumnDefn(u"Стиль", "left", 60, valueGetter="genre", autoCompleteComboBoxCellEditor=True),
            parentModule.ColumnDefn(u"Размер", "right", 60, valueGetter="size"),
            parentModule.ColumnDefn(u"Рейтинг", "center", 60, valueGetter="rating"),
            parentModule.ColumnDefn(u"Duration", "center", 150, valueGetter="duration"),
            parentModule.ColumnDefn(u"Date Played", "left", 150, valueGetter="dateLastPlayed",
                                    valueSetter="SetDateLastPlayed"),
            parentModule.ColumnDefn(u"Last Played", "left", 150, valueGetter="lastPlayed", maximumWidth=100),
            parentModule.ColumnDefn(u"Colour", "left", 60, valueGetter="trackColour", minimumWidth=40),
            ]

    dataset = [
        {'title': "Zoo Station", 'artist': "U2", 'size': 5.5, 'album': "Achtung Baby", 'genre': "Rock", 'rating': 60,
         'duration': "4:37", 'lastPlayed': "21/10/2007 5:42"},
        {'title': "Who's Gonna Ride Your Wild Horses", 'artist': "U2", 'size': 6.3, 'album': "Achtung Baby",
         'genre': "Rock", 'rating': 80, 'duration': "5:17", 'lastPlayed': "9/10/2007 11:32"},
        {'title': "So Cruel", 'artist': "U3", 'size': 6.9, 'album': u"Внимание", 'genre': "Rock",
         'rating': 60, 'duration': "5:49", 'lastPlayed': "9/10/2007 11:38"},
        {'title': "The Fly", 'artist': "U2", 'size': 5.4, 'album': "Achtung Baby",
         'genre': "Rock", 'rating': 60, 'duration': "4:29", 'lastPlayed': "9/10/2007 11:42"},
        ]

    app = wx.PySimpleApp()
    form = wx.Frame(None)
    grid = icSimpleGroupListView(form, component={'oddRowsBackColour': (255, 255, 255)})
    grid.SetColumns(columns)
    grid.SetObjects(dataset)
    form.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
