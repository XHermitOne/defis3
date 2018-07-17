#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ПРОСТОЙ ГРИД ОБЪЕКТОВ С ГРУППИРОВКОЙ.
Класс пользовательского компонента ПРОСТОЙ ГРИД ОБЪЕКТОВ С ГРУППИРОВКОЙ.

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
import ic.components.icwidget as icwidget
from ic.utils import util
from ic.utils import coderror
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

import ic.contrib.ObjectListView as parentModule

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt

#   Тип компонента
ic_class_type = icDefInf._icComboType

#   Имя класса
ic_class_name = 'icSimpleObjectGrid'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'SimpleObjectGrid',
                'name': 'default',
                'description':None,
                'child': [],
                'activate': True,
                'init_expr':None,
                '_uuid':None,
    
                'selected': None,   # Выбор элемента
                'activated': None,  # Активация элемента

                '__styles__': ic_class_styles,
                '__events__': {'selected': ('wx.EVT_LIST_ITEM_SELECTED', 'OnItemSelected', False),
                               'activated': ('wx.EVT_LIST_ITEM_ACTIVATED', 'OnItemActivated', False),
                               },
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                '__attr_hlp__': {'selected': u'Выбор элемента',
                                 'activated': u'Активация элемента',
                                 },
                }


#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = common.imgEdtObjGrid
ic_class_pic2 = common.imgEdtObjGrid

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['GridCell']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 3)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    return pspEdt.str_to_val_user_property(text, propEdt)


class icSimpleObjectGrid(icwidget.icWidget, parentModule.GroupListView):
    """
    Простой грид объектов с группировкой.

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

        parentModule.GroupListView.__init__(self, parent, id)

        # --- Свойства компонента ---
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]

        for key in lst_keys:
            setattr(self, key, component[key])

        # Установить колонки
        self.setColumnsSpc(*self.resource['child'])

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, id=self.GetId())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, id=self.GetId())
        self.BindICEvt()

        self.SetFocus()
        
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
        if type(Value_) not in (str, unicode):
            Value_ = str(Value_)
        if isinstance(Value_, str):
            return unicode(Value_, 'utf-8')
        elif isinstance(Value_, unicode):
            return Value_
        return u''

    def setColumnsSpc(self, *Columns_):
        """
        Создание колонок грида по описанию.
        @param Columns_: Описание колонок.
        """
        columns = []
        for column in Columns_:
            name = column['name']
            label = self._str2unicode(column['label'])
            width = column['width']
            new_col = parentModule.ColumnDefn(title=label,
                                              align='left',
                                              width=width,
                                              valueGetter=name,
                                              minimumWidth=40,
                                              maximumWidth=400)
            columns.append(new_col)
        if columns:
            self.SetColumns(columns)

    def setDataset(self, DatasetList_):
        """
        Установка набора данных объектов.
        """
        return self.SetObjects(DatasetList_)

    def OnItemSelected(self, evt):
        """ 
        Обрабатываем сообщение о выборе строки списка.
        """
        self.SetFocus()
        evt.Skip()
        result = True
        currentItem = self.GetFocusedRow()
        #   Формируем пространство имен
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['row'] = currentItem

        self.evalSpace['values'] = self.GetObjectAt(currentItem)
        self.evalSpace['_lfp'] = {'func': 'OnItemSelected', 'evt': evt,
                                  'currentItem': currentItem, 'row': currentItem,
                                  'self': self}
        
        if not self.selected in [None, '', 'None']:
            ret, val = self.eval_attr('selected')
            if ret:
                result = bool(val)

    def OnItemActivated(self, evt):
        """ 
        Активация (Enter/DobleClick) строки.
        """
        currentItem = self.GetFocusedRow()
        rowData = []
        #   Формируем пространство имен
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['row'] = currentItem
        
        rowDict = self.GetObjectAt(currentItem)
        self.evalSpace['values'] = rowDict
        self.evalSpace['_lfp'] = {'func': 'OnItemActivated', 'evt': evt,
                                  'currentItem': currentItem, 'result': rowDict,
                                  'self': self}
        self.eval_attr('activated')
        evt.Skip()
        

def test():
    """
    Функция тестирования.
    """
    columns = [parentModule.ColumnDefn(u"Заголовок", "left", 160, valueGetter="title", minimumWidth=40,
                                       maximumWidth=200),
               parentModule.ColumnDefn(u"Исполнитель", "left", 150, valueGetter="artist", minimumWidth=40,
                                       maximumWidth=200, autoCompleteCellEditor=True, headerImage="star"),
               parentModule.ColumnDefn(u"Альбом", "left", 150, valueGetter="album", maximumWidth=250,
                                       isSpaceFilling=True, autoCompleteCellEditor=True, headerImage=2),
               parentModule.ColumnDefn(u"Стиль", "left", 60, valueGetter="genre", autoCompleteComboBoxCellEditor=True),
               parentModule.ColumnDefn(u"Размер", "right", 60, valueGetter="size"),
               parentModule.ColumnDefn(u"Рейтинг", "center", 60, valueGetter="rating"),
               parentModule.ColumnDefn(u"Duration", "center", 150, valueGetter="duration",
                                       stringConverter="%S seconds and %M minutes"),
               parentModule.ColumnDefn(u"Date Played", "left", 150, valueGetter="dateLastPlayed", stringConverter="%x",
                                       valueSetter="SetDateLastPlayed"),
               parentModule.ColumnDefn(u"Last Played", "left", 150, valueGetter="lastPlayed", stringConverter="%x %X",
                                       maximumWidth=100),
               parentModule.ColumnDefn(u"Colour", "left", 60, valueGetter="trackColour", minimumWidth=40),
               ]

    dataset = [{'title': "Zoo Station", 'artist': "U2", 'size': 5.5, 'album': "Achtung Baby", 'genre': "Rock",
                'rating': 60, 'duration': "4:37", 'lastPlayed': "21/10/2007 5:42"},
               {'title': "Who's Gonna Ride Your Wild Horses", 'artist': "U2", 'size': 6.3, 'album': "Achtung Baby",
                'genre': "Rock", 'rating': 80, 'duration': "5:17", 'lastPlayed': "9/10/2007 11:32"},
               {'title': "So Cruel", 'artist': "U3", 'size': 6.9, 'album': u"Внимание", 'genre': "Rock", 'rating': 60,
                'duration': "5:49", 'lastPlayed': "9/10/2007 11:38"},
               {'title': "The Fly", 'artist': "U2", 'size': 5.4, 'album': "Achtung Baby", 'genre': "Rock", 'rating': 60,
                'duration': "4:29", 'lastPlayed': "9/10/2007 11:42"},
               ]

    app = wx.PySimpleApp()
    form = wx.Frame(None)
    grid = icSimpleObjectGrid(form)
    grid.SetColumns(columns)
    grid.SetObjects(dataset)
    form.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
