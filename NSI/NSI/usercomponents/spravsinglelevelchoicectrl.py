#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол выбора кода элемента справочника одного уровня.
"""

import wx

from ic.log import log
from ic.PropertyEditor import icDefInf
from ic.utils import coderror
from ic.dlg import dlgfunc
from ic.utils import util
from ic.bitmap import bmpfunc
from ic.components import icwidget
import ic.components.icResourceParser as prs

# from NSI.nsi_sys import nsi_images
import NSI.nsi_sys.icspravsinglelevelchoicectrl as parentModule

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSpravSingleLevelChoiceCtrl'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SpravSingleLevelChoiceCtrl',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'sprav': None,  # Паспорт справочника-источника данных
                'label': None,  # Заголовок области выбора справочника
                                # если не определена, то берется как descrption из справочника
                'n_level': 0,   # Номер уровня справочника для выбора

                'on_select_code': None,  # Код, который выполняется
                                         # при заполнении кода

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description', 'label'],
                                   icDefInf.EDT_USER_PROPERTY: ['sprav'],
                                   icDefInf.EDT_NUMBER: ['n_level'],
                                   },
                '__events__': {'on_select_code': (None, 'onSelectCode', False),
                               },
                '__parent__': parentModule.SPC_IC_SPRAVSINGLELEVELCHOICECTRL,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('ic_nsi_combo_ctrl.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('ic_nsi_combo_ctrl.png')

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
    if attr in ('sprav',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('sprav',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Sprav', 'RefObject'):
                dlgfunc.openMsgBox(u'ВНИМАНИЕ!',
                                   u'Выбранный объект не является Справочником.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('sprav',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icSpravSingleLevelChoiceCtrl(parentModule.icSpravSingleLevelChoiceCtrlProto, icwidget.icWidget):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

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
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icSpravSingleLevelChoiceCtrlProto.__init__(self, parent, id,
                                                                size=self.size, pos=self.position, style=self.style)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        # Установить справочник
        sprav_psp = self.getSpravPsp()
        sprav = self.GetKernel().Create(sprav_psp) if sprav_psp else None
        self.setSprav(sprav)

    def getSpravPsp(self):
        """
        Паспорт справочника.
        """
        return self.getICAttr('sprav')

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def getNLevel(self):
        """
        Индекс выбираемого уровня справочника.
        """
        return self.getICAttr('n_level')

    def onSelectCode(self):
        """
        Код, который выполняется когда заполняется код справочника.
        """
        context = self.GetContext()
        context['SELECTED_CODE'] = self._selected_code
        result = self.eval_attr('on_select_code')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка выполнения блока кода при заполнении кода справочника')
        return None
