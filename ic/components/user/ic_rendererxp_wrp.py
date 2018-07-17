#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Отрисовщик XP стиля.
ОТРИСОВЩИК КОНТРОЛОВ. XP СТИЛЬ.

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

from ic.engine import icrenderer

#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icRendererXP'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
SPC_IC_RENDERERXP_WRP = icrenderer.SPC_IC_RENDERERXP
SPC_IC_RENDERERXP_WRP['__parent__'] = icwidget.SPC_IC_SIMPLE

ic_class_spc = {'type': 'RendererXP',
                'name': 'default', 
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                
                'menubar_background_start_colour': (167, 202, 240),
                'menubar_background_end_colour': (167, 202, 240),
    
                'toolbar_background_start_colour': (224, 238, 252),
                'toolbar_background_end_colour': (159, 193, 232),
                'toolbar_background_start_colour_tail': (117, 166, 241),
                'toolbar_background_end_colour_tail': (6, 59, 150),
                'toolbar_background_colour': (159, 193, 232),
                'toolbar_background_colour_tail': (79, 129, 210),
                'toolbar_bottom_colour': (59, 97, 156),
                'toolbar_bottom_colour_tail': (0, 53, 145),
        
                'separator_col_start_colour': (241, 249, 255),
                'separator_col_end_colour': (106, 140, 203),
        
                'enable_text_colour': (0, 0, 0),    # wx.BLACK
                'toolbar_width': 350,   # Ширина

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__':   {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                              'description'],
                                     icDefInf.EDT_NUMBER: ['toolbar_width'],
                                     icDefInf.EDT_COLOR: ['menubar_background_start_colour',
                                                          'menubar_background_end_colour',
                                                          'toolbar_background_start_colour',
                                                          'toolbar_background_end_colour',
                                                          'toolbar_background_start_colour_tail',
                                                          'toolbar_background_end_colour_tail',
                                                          'toolbar_background_colour',
                                                          'toolbar_background_colour_tail',
                                                          'toolbar_bottom_colour',
                                                          'toolbar_bottom_colour_tail',
                                                          'separator_col_start_colour',
                                                          'separator_col_end_colour',
                                                          'enable_text_colour',
                                                          ],
                                     },
                '__parent__': icrenderer.SPC_IC_RENDERERXP,
                '__attr_hlp__': {'toolbar_width': u' Ширина',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = common.imgEdtRenderer
ic_class_pic2 = common.imgEdtRenderer

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_rendererxp_wrp.icRendererXP-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 4)


class icRendererXP(icwidget.icSimple, icrenderer.icRendererXPPrototype):
    """
    Отрисовщик контролов. Стиль XP.
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
        icrenderer.icRendererXPPrototype.__init__(self)

        if component['menubar_background_start_colour']:
            self.menubar_background_start_colour = wx.Colour(*component['menubar_background_start_colour'])
        if component['menubar_background_end_colour']:
            self.menubar_background_end_colour = wx.Colour(*component['menubar_background_end_colour'])
    
        if component['toolbar_background_start_colour']:
            self.toolbar_background_start_colour = wx.Colour(*component['toolbar_background_start_colour'])
        if component['toolbar_background_end_colour']:
            self.toolbar_background_end_colour = wx.Colour(*component['toolbar_background_end_colour'])
        if component['toolbar_background_start_colour_tail']:
            self.toolbar_background_start_colour_tail = wx.Colour(*component['toolbar_background_start_colour_tail'])
        if component['toolbar_background_end_colour_tail']:
            self.toolbar_background_end_colour_tail = wx.Colour(*component['toolbar_background_end_colour_tail'])
        if component['toolbar_background_colour']:
            self.toolbar_background_colour = wx.Colour(*component['toolbar_background_colour'])
        if component['toolbar_background_colour_tail']:
            self.toolbar_background_colour_tail = wx.Colour(*component['toolbar_background_colour_tail'])
        if component['toolbar_bottom_colour']:
            self.toolbar_bottom_colour = wx.Colour(*component['toolbar_bottom_colour'])
        if component['toolbar_bottom_colour_tail']:
            self.toolbar_bottom_colour_tail = wx.Colour(*component['toolbar_bottom_colour_tail'])
        
        if component['separator_col_start_colour']:
            self.separator_col_start_colour = wx.Colour(*component['separator_col_start_colour'])
        if component['separator_col_end_colour']:
            self.separator_col_end_colour = wx.Colour(*component['separator_col_end_colour'])
        
        if component['enable_text_colour']:
            self.enable_text_colour = wx.Colour(*component['enable_text_colour'])
            
        self.toolBarWidth = component['toolbar_width']
