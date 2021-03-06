#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Выпадающее меню.
Класс пользовательского визуального компонента ВЫПАДАЮЩЕЕ МЕНЮ.

:type ic_user_name: C{string}
:var ic_user_name: Имя пользовательского класса.
:type ic_can_contain: C{list | int}
:var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других 
    компонентов в данный комопнент. 
:type ic_can_not_contain: C{list}
:var ic_can_not_contain: Запрещающее правило - список типов компонентов, 
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой 
    компонент (ic_can_contain = -1).
"""

import wx
from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf

from ic.engine import icflatmenu
from ic.engine import icflatmenubar

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icFlatMenu'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
SPC_IC_FLATMENU_WRP = icflatmenu.SPC_IC_FLATMENU
SPC_IC_FLATMENU_WRP['__parent__'] = icwidget.SPC_IC_WIDGET

ic_class_spc = {'type': 'FlatMenu',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],
                
                'label': 'new_menu',

                '__styles__': ic_class_styles,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'label'],
                                   icDefInf.EDT_CHECK_BOX: ['activate'],
                                   },
                '__events__': {},
                '__parent__': SPC_IC_FLATMENU_WRP,
                '__attr_hlp__': {'label': u'Надпись',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMenu'
ic_class_pic2 = '@common.imgEdtMenu'

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ic_flatmenu_wrp.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['FlatMenu', 'FlatMenuItem']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icFlatMenu(icwidget.icWidget, icflatmenu.icFlatMenuPrototype):
    """
    Выпадающее меню.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

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
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        icflatmenu.icFlatMenuPrototype.__init__(self, parent)

        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)
        
        if parent:
            # Добавить меню в родительское меню
            self.appendIntoParent(parent)

    def getLabel(self):
        """
        Надпись.
        """
        return self.getICAttr('label')
    
    def appendIntoParent(self, parent):
        """
        Добавить меню в родительское меню.
        """
        if parent:
            if issubclass(parent.__class__, icflatmenubar.icFlatMenuBarPrototype):
                # Добавляем в горизонтальное меню
                label = self.getLabel()
                parent.Append(self, label)
            elif issubclass(parent.__class__, icflatmenu.icFlatMenuPrototype):
                # Добавляем в выпадающее меню
                parent.appendMenu(self)
