#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Горизонтальное меню.
Класс пользовательского визуального компонента ГОРИЗОНТАЛЬНОЕ МЕНЮ.

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
from wx.lib.agw.artmanager import ArtManager

import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
from ic.dlg import ic_dlg
from ic.utils import coderror

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

from wx.lib.agw import fmresources
from ic.engine import icflatmenubar
from ic.engine import icflatmenu

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icFlatMenuBar'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': fmresources.FM_OPT_SHOW_CUSTOMIZE | fmresources.FM_OPT_IS_LCD,
                   'FM_OPT_IS_LCD': fmresources.FM_OPT_IS_LCD,
                   'FM_OPT_MINIBAR': fmresources.FM_OPT_MINIBAR,
                   'FM_OPT_SHOW_CUSTOMIZE': fmresources.FM_OPT_SHOW_CUSTOMIZE,
                   'FM_OPT_SHOW_TOOLBAR': fmresources.FM_OPT_SHOW_TOOLBAR,
    }

#   Спецификация на ресурсное описание класса
SPC_IC_FLATMENUBAR_WRP = icflatmenubar.SPC_IC_FLATMENUBAR
SPC_IC_FLATMENUBAR_WRP['__parent__'] = icwidget.SPC_IC_WIDGET

ic_class_spc = {'type': 'FlatMenuBar',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],
                
                'renderer': None,  # Стиль отрисовки
                'icon_size': 16,   # Размер иконок
                'spacer_size': 7,  # Размер расстояния между элементами

                '__styles__': ic_class_styles,
                '__lists__': {'icon_size': [16, 24, 32, 48],
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'description'],
                                   icDefInf.EDT_NUMBER: ['spacer_size', ],
                                   icDefInf.EDT_CHOICE: ['icon_size', ],
                                   icDefInf.EDT_CHECK_BOX: ['activate'],
                                   icDefInf.EDT_USER_PROPERTY: ['renderer'],
                                   },
                '__events__': {},
                '__parent__': SPC_IC_FLATMENUBAR_WRP,
                '__attr_hlp__': {'renderer': u'Стиль отрисовки',
                                 'icon_size': u'Размер иконок',
                                 'spacer_size': u'Размер расстояния между элементами',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMenuBar'
ic_class_pic2 = '@common.imgEdtMenuBar'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_flatmenubar_wrp.icFlatMenuBar-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['FlatMenu', 'FlatMenuTool']

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
    if attr in ('renderer',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('renderer',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('RendererXP',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является РЕНДЕРОМ.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('renderer',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icFlatMenuBar(icwidget.icWidget, icflatmenubar.icFlatMenuBarPrototype):
    """
    Горизонтальное меню.
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
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        id = wx.NewId()
        self.icon_size = self.getIconSize()
        self.spacer_size = self.getSpacerSize()
        icflatmenubar.icFlatMenuBarPrototype.__init__(self, parent, id=id,
                                                      iconSize=self.icon_size,
                                                      spacer=self.spacer_size,
                                                      options=self.style)
            
        # Рендер
        renderer = self.getRenderer()
        self.newMyTheme = None
        if renderer:
            self.newMyTheme = ArtManager.Get().AddMenuTheme(renderer)
            ArtManager.Get().SetMenuTheme(self.newMyTheme)

        if parent:
            w, h = parent.GetClientSize()
            self.SetSize(wx.Size(w, -1))
        else:
            menu_lst = [child for child in self.GetChildren() if issubclass(child.__class__,
                                                                            icflatmenu.icFlatMenuPrototype)]
            w = -1
            if menu_lst:
                w = 0
                for menu in menu_lst:
                    dw, dh = menu.GetSize()
                    w += dw
            self.SetSize(wx.Size(w, -1))

        self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter=False, progressDlg=None):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)
                            
    def appendMenuBar(self, MenuBar_, bCounter=False, progressDlg=None):
        """
        Добавить/Объединить два горизонтальных меню.
        """
        # Склеивание этих менюшек происходит не совсем так как хочется
        # надо разбираться
        pass
            
    def getIconSize(self):
        """
        Размер иконок.
        """
        return self.getICAttr('icon_size')
    
    def getSpacerSize(self):
        """
        Размер растояния между элементами.
        """
        return self.getICAttr('spacer_size')
    
    def getRendererPsp(self):
        """
        Рендер. Паспорт.
        """
        return self.getICAttr('renderer')
    
    def getRenderer(self):
        """
        Рендер. Объект.
        """
        renderer_psp = self.getRendererPsp()
        if renderer_psp:
            return self.GetKernel().Create(renderer_psp)
        return None
        

def simple_test():
    """
    Тестовая функция.
    """
    from ic.imglib import common
    from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR, SEPARATOR_WIDTH
    import copy
    from . import ic_menu_wrp
    
    app = wx.PySimpleApp()
    common.img_init()
    frame = wx.Frame(None)
    
    res = copy.deepcopy(ic_class_spc)
    res_menu = copy.deepcopy(ic_menu_wrp.ic_class_spc)
    res['child'] = [res_menu]
    
    bar = icFlatMenuBar(frame, -1, res)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    simple_test()
