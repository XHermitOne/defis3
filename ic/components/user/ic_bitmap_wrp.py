#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Картинка как ресурс.
Класс пользовательского компонента КАРТИНКА.

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
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

from ic.utils import coderror
from ic.utils import ic_file
from ic.dlg import ic_dlg

from ic.bitmap import icimg2py
from ic.bitmap import icimagelibrary as parentModule

#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icBitmap'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'Bitmap',
                'name': 'default',

                '_body': None,
                'file_name': None,
                '__default_page__': 2,
                '__styles__': ic_class_styles,
                '__lists__': {},
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_RO_TEXTFIELD: ['_body'],
                                   icDefInf.EDT_USER_PROPERTY: ['file_name'],
                                   },
                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_hlp__': {'file_name': u'Имя файла картинки',
                                 },
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtImage'
ic_class_pic2 = '@common.imgEdtImage'

#   Путь до файла документации
ic_class_doc = None
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 4)

### EDITOR_FUNCS_BLOCK

# --- Функции редактирования


def _draw_picture_by_filename(dc, rect, img_body):
    """
    Отрисовать картинку в гриде редактора свойств с указанием имени файла образа.
    """
    bmp = icimg2py.bitmapFromData(img_body)
    if bmp.Ok():
        memDC = wx.MemoryDC()
        memDC.SelectObject(bmp)

        x, y = rect.GetPosition()
        rect_width, rect_height = rect.GetSize()
        bmp_width, bmp_height = bmp.GetSize()
        width = min(rect_width, bmp_width)
        height = min(rect_height, bmp_height)

        dc.SetBrush(wx.Brush(wx.LIGHT_GREY, wx.SOLID))
        dc.Clear()
        dc.Blit(x, y, width, height, memDC, 0, 0, wx.COPY, True)
        return True
    return False


def property_editor_draw(dc, attr, rect, row, col, isSelected, propEdt):
    """
    Стандартная функция отрисовки свойства в редакторе ресурсов.
    @param dc: Контекст устройства.
    @param attr: Имя текущего атрибута.
    @param rect: Область отрисовки.
    @param row: Номер строки грида. 
    @param col: Номер колонки грида.
    @param isSelected: Признак выбранной ячейки грида.
    @type propEdt: C{ic.components.user.objects.PropNotebookEdt}
    @param propEdt: Указатель на редактор свойств.
    @return: False - вызывается стандартная функция отрисовки свойства.
    """
    if attr == 'file_name':
        body = propEdt.GetProperty('_body')
        if body:
            return _draw_picture_by_filename(dc, rect, body)
        else:
            return False
    return False


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    
    @type attr: C{string}
    @param attr: Имя текущего атрибута.
    @type value: C{string}
    @param value: Текущее значение цвета в виде 'wx.Colour(r,g,b)'.
    @type pos: C{wx.Point}
    @param pos: Позиция окна.
    @type size: C{wx.Size}
    @param size: Размер диалогового окна.
    @type style: C{int}
    @param style: Стиль диалога.
    @type propEdt: C{ic.components.user.objects.PropNotebookEdt}
    @param propEdt: Указатель на редактор свойств.
    """
    if attr == 'file_name':
        parent = propEdt
        img_file_name = ic_dlg.icImageDlg(parent)
        return img_file_name


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr == 'file_name':
        if value and ic_file.Exists(value):
            # Серилизованная строка
            srlz_string = icimg2py.getImgFileData(value)
            # Т.к. функция создания серилизованной строки
            # создает строку для вставки ее в код
            # надо сделать над ней eval
            body = eval(srlz_string)
            propEdt.setPropertyValue('_body', body, False)
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr == 'file_name':
        return text
    
### END_EDITOR_FUNCS_BLOCK


class icBitmap(icwidget.icSimple, parentModule.icSerializedImagePrototype):
    """
    Образ/Картинка.
    """
    
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
        self._body = component['_body']
        self.file_name = component['file_name']
        parentModule.icSerializedImagePrototype.__init__(self, self.name, self._body)
