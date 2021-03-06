#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Перечисления, хранящиеся в БД.

Класс пользовательского компонента ПЕРЕЧИСЛЕНИЯ.

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

import copy
import wx

from ic.dlg import dlgfunc
from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.bitmap import bmpfunc
from ic.PropertyEditor import icDefInf
from ic.utils import coderror

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

import NSI.nsi_sys.icdbenum as parentModule
from . import spravlevel

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icDBEnum'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'__events__': {}, 
                'type': 'DBEnum',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                '__styles__': ic_class_styles,

                'description': '',  # Описание справочника
                'table': None,      # Имя таблицы храниения данных
                'db': None,         # Имя БД хранения данных
                'cache': True,      # Автоматически кэшировать?
                'cache_frm': True,  # Автоматически кешировать формы?
                'choice_form': None,    # Форма для просмотра и выбора кода справочника
                'edit_form': None,  # Форма для редактирования справочника
    
                # '__lists__': {'level_count':range(1,6)},
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description', 'choice_form', 'edit_form'],
                                   # icDefInf.EDT_CHOICE:['level_count'],
                                   icDefInf.EDT_CHECK_BOX: ['cache', 'cache_frm'],
                                   icDefInf.EDT_USER_PROPERTY: ['db', 'table'],
                                   },
                '__parent__': parentModule.SPC_IC_DBENUM,
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('sort_price.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('sort_price.png')

#   Путь до файла документации
ic_class_doc = 'NSI/doc/_build/html/NSI.usercomponents.dbenum.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 3)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret=None
    if attr in ('db', 'table'):
        ret=pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('db',):
        # return pspEdt.property_editor_ctrl(value, propEdt)
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in ('PostgreSQLDB', 'SQLiteDB'):
                dlgfunc.openWarningBox(u'ОШИБКА', u'Выбранный объект не является БД.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    elif attr in ('table',):
        # return pspEdt.property_editor_ctrl(value, propEdt)
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in ('Table',):
                dlgfunc.openWarningBox(u'ОШИБКА', u'Выбранный объект не является таблицей.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('db', 'table'):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icDBEnum(icwidget.icSimple, parentModule.icDBEnumProto):
    """
    Описание пользовательского компонента ПЕРЕЧИСЛЕНИЕ.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

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

        parentModule.icDBEnumProto.__init__(self, parent, component['name'])
        
        # --- Свойства компонента ---
        # Описание перечисления
        self.description = ''
        if 'description' in component:
            self.description = component['description']

        #   Создаем дочерние компоненты
        component = self.addEnumLevelsSPC(component)
        
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

    def addEnumLevelsSPC(self, component_spc):
        """
        Сразу задается структура из 1 уровня.
        """
        level_spc = copy.deepcopy(spravlevel.ic_class_spc)
        level_spc['name'] = 'Enum'
        level_spc['len'] = 10
        level_spc['description'] = u'Перечисление:'
        level_spc['notice'] = {'cod': u'Имя перечисления',
                               'name': u'Описание',
                               's1': u'Тип значения'}
        
        component_spc['child'] = [level_spc]
        return component_spc
        
    def getLevelCount(self):
        """
        Количество уровней.
        """
        if not self.components:
            return 0
        return len(self.components)
        
    def getLevels(self):
        """
        Уровни справочника.
        """
        return self.GetComponentsList()
        
    def getDBName(self):
        """
        Имя БД.
        """
        db_psp = self.getICAttr('db')
        if db_psp:
            return db_psp[0][1]
        return None
        
    def getTableName(self):
        """
        Имя объекта хранения/Таблицы.
        """
        tab_psp = self.getICAttr('table')
        if tab_psp:
            return tab_psp[0][1]
        return None
    
    def getDBPsp(self):
        """
        Паспорт БД.
        """
        return self.getICAttr('db')
        
    def getTablePsp(self):
        """
        Паспорт объекта хранения/Таблицы.
        """
        return self.getICAttr('table')
    
    def getAutoCache(self):
        """
        Признак автоматического кэширования.
        """
        return self.getICAttr('cache')
        
    def getAutoCacheFrm(self):
        """
        Признак автоматического кэширования форм.
        """
        return self.getICAttr('cache_frm')
        
    def getChoiceFormName(self):
        """
        Форма для выбора данных справочника.
        """
        choice_form = self.getICAttr('choice_form')
        if choice_form is None:
            dlgfunc.openMsgBox(u'ВНИМАНИЕ!',
                               u'В справочнике %s не определена форма выбора' % self.name)
        return choice_form

    def getEditFormName(self):
        """
        Форма для редактирования данных справочника.
        """
        edit_form = self.getICAttr('edit_form')
        if edit_form is None:
            dlgfunc.openMsgBox(u'ВНИМАНИЕ!',
                               u'В справочнике %s не определена форма редактирования.' % self.name)
        return edit_form
        
    def getChoiceFormPsp(self):
        """
        Форма для выбора данных справочника.
        """
        return None

    def getEditFormPsp(self):
        """
        Форма для редактирования данных справочника.
        """
        return None
        
    #   Обработчики событий
