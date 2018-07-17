#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Главное окно системы.
Класс Главное окно системы.

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

import ic.engine.ic_win as ic_win
import ic.engine.ic_user as ic_user
from ic.utils import coderror
from ic.dlg import ic_dlg
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icMainWindow'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'MainWindow',
                'name': 'default',
                'activate': True,
                'init_expr': None,

                'max_button': True,
                'sys_menu': True,
                'min_button': True,

                'is_menubar': True,    # Присутствует в главном окне меню?
                'is_statusbar': True,  # Присутствует в главном окне статусная строка?
                'content': None,       # Заполнить фрейм главного окна объектом ...

                '_uuid': None,
                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'title_label',
                                                            'icon', 'splash'],
                                   icDefInf.EDT_CHECK_BOX: ['title_readonly', 'sys_menu',
                                                            'min_button', 'max_button', 'area_split',
                                                            'is_menubar', 'is_statusbar'],
                                   icDefInf.EDT_NUMBER: ['border'],
                                   icDefInf.EDT_POINT: ['pos'],
                                   icDefInf.EDT_SIZE: ['size'],
                                   icDefInf.EDT_RO_TEXTFIELD: ['res_module', '_uuid', 'obj_module'],
                                   icDefInf.EDT_COLOR: ['title_color', 'phone_color'],
                                   icDefInf.EDT_USER_PROPERTY: ['content'],
                                   },
                '__parent__': ic_win.SPC_IC_WIN,
                '__attr__hlp__': {'is_menubar': u'Присутствует в главном окне меню?',
                                  'is_statusbar': u'Присутствует в главном окне статусная строка?',
                                  'content': u'Заполнить фрейм главного окна объектом ...',
                                  },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMainWin'
ic_class_pic2 = '@common.imgEdtMainWin'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_mainwin_wrp.icMainWindow-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 5)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('content',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('content',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in ('Panel', 'ScrolledWindow', 'Notebook', 'SplitterWindow'):
                ic_dlg.icWarningBox(u'ОШИБКА', u'Выбранный объект не является главным окном.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('content',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icMainWindow(icwidget.icSimple, ic_win.icMainWindow):
    """
    Главное окно приложения.
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
        
        main_win_parent = None
        if parent:
            main_win_parent = parent
        
        ic_win.icMainWindow.__init__(self, component['name'], component,
                                     Parent_=main_win_parent, Runner_=ic_user.icGetRunner())

        # Дополнительный функционал инициализации
        if component.get('init_expr', None):
            self.eval_attr('init_expr')
