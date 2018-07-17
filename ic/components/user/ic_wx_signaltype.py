#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Расширение обработчиков событий.
Класс пользовательского компонента, описывающего дополнительный тип wx сообщения.

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
import ic.engine.ic_user as ic_user
import ic.kernel.io_prnt as io_prnt
from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors import baseeditor
import wx.lib as wxlib
import ic.kernel.icobject as icobject

# --- Спецификация ---
SPC_IC_WX_BINDER = {'type': 'WX_SignalType',
                    'name': 'default',
                    'src': None,
                    'receiver': None,
                    'lib': 'wx',
                    'function': 'post_controller',
                    'wx_signal_type': None,
                    '__attr_types__': {0: ['name', 'type', 'function'],
                                       icDefInf.EDT_USER_PROPERTY: ['wx_signal_type', 'src', 'receiver', 'lib'],
                                       },
                    '__parent__': icwidget.SPC_IC_SIMPLE,
                    }
    
# --- Описание компонента для редактора ресурса ---
#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icWX_SignalType'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = SPC_IC_WX_BINDER
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtSignal'
ic_class_pic2 = '@common.imgEdtSignal'

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


# Функции редактора
def _get_lib_evt_lst(lib='wx', bPref=False):
    """
    Возвращает список идентификаторов заданной библиотеки.
    """
    if lib and lib != 'wx':
        exec('import %s as wx_lib' % lib)
        if bPref:
            lst = [el for el in dir(wx_lib) if type(el) in (str, unicode) and el.startswith('EVT_')]
        else:
            lst = [el[4:] for el in dir(wx_lib) if type(el) in (str, unicode) and el.startswith('EVT_')]
    elif bPref:
        lst = [el for el in dir(wx) if type(el) in (str, unicode) and el.startswith('EVT_')]
    else:
        lst = [el[4:] for el in dir(wx) if type(el) in (str, unicode) and el.startswith('EVT_')]
    
    return lst


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    parent = propEdt.GetPropertyGrid().GetView()
    
    if attr in ('src', 'receiver'):
        return pspEdt.get_user_property_editor(value, pos, size, style, propEdt)
    elif attr == 'lib':
        lst = ['wx', 'wx.aui', 'wx.grid']
        lst += ['wx.lib.%s' % el for el in dir(wxlib) if not el.startswith('_')]

        if lst:
            dlg = baseeditor.ChoiceMenu(parent, lst)
            parent.PopupMenu(dlg, pos)
        
            #   Возвращаем выбранный элемент списка
            if lst and dlg.IsSelString():
                value = dlg.GetSelString()
            
            dlg.Destroy()
            return value

    elif attr == 'wx_signal_type':
        lib = propEdt.GetResource()['lib']
        lst = _get_lib_evt_lst(lib)
        if lst:
            dlg = baseeditor.ChoiceMenu(parent, lst)
            parent.PopupMenu(dlg, pos)
        
            #   Возвращаем выбранный элемент списка
            if lst and dlg.IsSelString():
                value = 'EVT_' + dlg.GetSelString()
            
            dlg.Destroy()
            return value
        else:
            ic_dlg.icWarningBox(u'ОШИБКА', u'Типы сообщений в библиотеке <%s> не определены' % lib)


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('src', 'receiver'):
        return pspEdt.property_editor_ctrl(value, propEdt)
    elif attr == 'wx_signal_type':
        lib = propEdt.GetResource()['lib']
        lst = _get_lib_evt_lst(lib, True)
        if value in lst:
            return coderror.IC_CTRL_OK
    elif attr == 'lib':
        return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('src', 'receiver'):
        return pspEdt.str_to_val_user_property(text, propEdt)
    elif attr == 'wx_signal_type':
        return text
    elif attr == 'lib':
        return text


class icWX_SignalType(icwidget.icSimple):
    """
    Описание интерфейса сигнала (кто, куда и что посылает, и кто это обрабатывает).

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
        - B{src=None}: Паспорт источника сообщения. Если паспорт не определен,
            то источником является объект, использующий данный интерфейс;
        - B{receiver=None}: Паспорт приемника сообщения.Если паспорт не определен,
            то приемником является объект, использующий данный интерфейс;
        - B{lib='wx'}: Библиотека, определяющая тип сообщений.
        - B{wx_signal_type=None}: Идентификатор типа сообщения.
        - B{function='post_controller'}: Имя функции, обработчика сообщений у объекта приемника.
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
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
        
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        # Превращаем картежи в паспорта
        if self.src:
            self.src = icobject.icObjectPassport(*self.src)
        if self.receiver:
            self.receiver = icobject.icObjectPassport(*self.receiver)
            
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
      
    def getEvtId(self):
        """
        Возвращет идентификатор сообщения.
        """
        exec('from %s import %s as evt_id' % (self.lib, self.wx_signal_type))
        return evt_id
        
    #   Обработчики событий
