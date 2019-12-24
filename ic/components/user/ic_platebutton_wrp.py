#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.PlateButton.
"""

import wx
import wx.lib.platebtn

from ic.dlg import dlgfunc
from ic.log.iclog import *
from ic.components.icfont import *
from ic.utils import util
from ic.bitmap import bmpfunc
from ic.components import icwidget
import ic.utils.coderror as coderror
from ic.PropertyEditor import icDefInf

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

PLATE_BUTTON_STYLE = {'PB_STYLE_DEFAULT': wx.lib.platebtn.PB_STYLE_DEFAULT,
                      'PB_STYLE_DROPARROW': wx.lib.platebtn.PB_STYLE_DROPARROW,
                      'PB_STYLE_GRADIENT': wx.lib.platebtn.PB_STYLE_GRADIENT,
                      'PB_STYLE_NOBG': wx.lib.platebtn.PB_STYLE_NOBG,
                      'PB_STYLE_SQUARE': wx.lib.platebtn.PB_STYLE_SQUARE,
                      'PB_STYLE_TOGGLE': wx.lib.platebtn.PB_STYLE_TOGGLE,
                      }

SPC_IC_PLATEBUTTON = {'type': 'PlateButton',
                      'name': 'default',

                      'label': 'button',
                      'style': 0,
                      'position': (-1, -1),
                      'size': (-1, -1),
                      'font': {},
                      'foregroundColor': None,
                      'backgroundColor': None,
                      'image': None,  # Образ кнопки

                      'mouseClick': None,

                      '__styles__': PLATE_BUTTON_STYLE,
                      '__events__': {'mouseClick': ('wx.EVT_BUTTON', 'onMouseClick', False),
                                     },
                      '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                                  'description', 'label'],
                                         icDefInf.EDT_CHECK_BOX: ['attach_focus'],
                                         icDefInf.EDT_USER_PROPERTY: ['image'],
                                         },
                      '__parent__': icwidget.SPC_IC_WIDGET,
                      '__attr_hlp__': {'label': u'Надпись',
                                       'image': u'Образ кнопки',
                                       'mouseClick': u'Обработчик нажатия кнопки',
                                       },
                      }

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icPlateButton'

#   Описание стилей компонента
ic_class_styles = PLATE_BUTTON_STYLE

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_PLATEBUTTON

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('wxbitmaptogglebutton.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('wxbitmaptogglebutton.png')

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ic_platebutton_wrp.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).

    :type attr: C{string}
    :param attr: Имя текущего атрибута.
    :type value: C{string}
    :param value: Текущее значение цвета в виде 'wx.Colour(r,g,b)'.
    :type pos: C{wx.Point}
    :param pos: Позиция окна.
    :type size: C{wx.Size}
    :param size: Размер диалогового окна.
    :type style: C{int}
    :param style: Стиль диалога.
    :type propEdt: C{ic.components.user.objects.PropNotebookEdt}
    :param propEdt: Указатель на редактор свойств.
    """
    ret = None
    if attr in ('image', ):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.

    :type attr: C{string}
    :param attr: Имя текущего атрибута.
    :type value: C{string}
    :param value: Текущее значение цвета в виде 'wx.Colour(r,g,b)'.
    :type propEdt: C{ic.components.user.objects.PropNotebookEdt}
    :param propEdt: Указатель на редактор свойств.
    """
    if attr in ('image', ):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Bitmap',):
                dlgfunc.openMsgBox(u'ВНИМАНИЕ!',
                                   u'Выбранный объект не является картинкой.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.

    :type attr: C{string}
    :param attr: Имя текущего атрибута.
    :type propEdt: C{ic.components.user.objects.PropNotebookEdt}
    :param propEdt: Указатель на редактор свойств.
    """
    if attr in ('image', ):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icPlateButton(icwidget.icWidget, wx.lib.platebtn.PlateButton):
    """
    Класс icButton реализует обкладку над компонентом wx.Button.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icPlateButton.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно
        :type id: C{int}
        :param id: Идентификатор окна
        :type component: C{dictionary}
        :param component: Словарь описания компонента
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        :type evalSpace: C{dictionary}
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        component['font'] = util.icSpcDefStruct(SPC_IC_FONT, component['font'])

        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        wx.lib.platebtn.PlateButton.__init__(self, parent, id,
                                             label=self.getLabel(),
                                             bmp=self.getImage(),
                                             pos=component['position'],
                                             size=component['size'],
                                             style=component['style'],
                                             name=self.getName())

        fgr = component['foregroundColor']
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        bgr = component['backgroundColor']
        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        font = component['font']
        obj = icFont(font)
        self.SetFont(obj)

        #   Обработчики сообщений
        self.Bind(wx.EVT_BUTTON, self.onMouseClick, id=id)
        self.BindICEvt()

    def onMouseClick(self, event):
        """
        Обрабатываем нажатие кнопки (сообщение EVT_BUTTON).
        """
        self.eval_event('mouseClick', event, True)

    def getLabel(self):
        """
        Надпись.
        """
        return self.getICAttr('label')

    def _createPicBmp(self, bmp_psp):
        """
        Создать картинку по паспорту.
        """
        # Паспорт не определен
        if not bmp_psp:
            return None

        bitmap_obj = self.GetKernel().Create(bmp_psp)
        bmp = bitmap_obj.getBitmap()
        if not bmp:
            log.debug(u'Не определена картинка для кнопки <%s>' % self.getName())
        return bmp

    def getImage(self):
        """
        Картинка кнопки.
        """
        bmp_psp = self.getICAttr('image')
        bmp = self._createPicBmp(bmp_psp)
        if bmp is None:
            return wx.NullBitmap
        return bmp
