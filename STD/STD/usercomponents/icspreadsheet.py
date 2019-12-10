#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Общий менеджер управления структурой SpreadSheet.
Оформлен в виде компонента.
"""

from ic.log import log
from ic.bitmap import bmpfunc
from ic.utils import util
from ic.utils import coderror
from ic.dlg import dlgfunc

from ic.components import icwidget
from ic.PropertyEditor import icDefInf

from ..spreadsheet import spreadsheet_proto

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSpreadSheet'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SpreadSheet',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'viewer': None,   # wx.Grid для отображения

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type'],
                                   icDefInf.EDT_USER_PROPERTY: ['viewer'],
                                   },
                '__parent__': spreadsheet_proto.SPC_IC_SPREADSHEET,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('table_excel.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('table_excel.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

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
    if attr in ('viewer',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('viewer',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Grid', ):
                dlgfunc.openMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является объектом Grid.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('viewer',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icSpreadSheet(icwidget.icSimple,
                    spreadsheet_proto.icSpreadSheetProto):
    """
    Общий менеджер управления структурой SpreadSheet.
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        spreadsheet_proto.icSpreadSheetProto.__init__(self)

    def getViewerPsp(self):
        """
        Паспорт грида-просмотрщика.
        """
        return self.getICAttr('viewer')

    def getViewer(self):
        """
        Объект грида-просмотрщика.
        """
        grid = self.getSpreadSheetGrid()
        if grid is None:
            grid_psp = self.getViewerPsp()
            kernel = self.GetKernel()
            grid = kernel.Create(grid_psp)
            self.setSpreadSheetGrid(grid)
        return grid
