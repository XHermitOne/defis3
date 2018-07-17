#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Група пользователей системы.

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
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

from ic.dlg import msgbox
from ic.utils import coderror
from ic.utils import ic_file
from ic.engine import ic_user

import ic.engine.icUser as icuser

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icUserGroup'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
icuser.SPC_IC_USERGROUP['__parent__'] = icwidget.SPC_IC_SIMPLE

ic_class_spc = {'type': 'UserGroup',
                'name': 'default', 
                '_uuid': None,

                'group': None,  # имя группы-родителя, у которой наследуются права доступа,
                'lock_time': [[], [], [], [], [], [], []],  # временной график  доступа к системе  за неделю
                'menubars': [],     # Список меню.
                'on_login': None,   # скрипт, выполняемый после успешного логина
                'on_logout': None,  # скрипт, выполняемый после успешного логаута

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description'],
                                   icDefInf.EDT_TEXTLIST: ['lock_time', 'menubars'],
                                   },
                '__parent__': icuser.SPC_IC_USERGROUP,
                '__attr_hlp__': {'group': u'Имя группы-родителя, у которой наследуются права доступа',
                                 'lock_time': u'Временной график  доступа к системе  за неделю',
                                 'menubars': u'Список меню',
                                 'on_login': u'Скрипт, выполняемый после успешного логина',
                                 'on_logout': u'Скрипт, выполняемый после успешного логаута',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtUsers'
ic_class_pic2 = '@common.imgEdtUsers'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_usergrp_wrp.icUserGroup-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icUserGroup(icwidget.icSimple, icuser.icUserGroup):
    """
    Группа пользователей системы.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родителя
        @type id: C{int}
        @param id: Идентификатор
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
        icuser.icUserGroup.__init__(self, ic_file.PathFile(ic_user.icGet('SYS_RES'),
                                    icuser.DEFAULT_USERS_RES_FILE))

    def _exec_on_login(self, Code_):
        """
        Выполнить при успешном логине.
        """
        return self.eval_expr(Code_, 'on_login')
        
    def _exec_on_logout(self, Code_):
        """
        Выполнить при успешном логауте.
        """
        return self.eval_expr(Code_, 'on_logout')
