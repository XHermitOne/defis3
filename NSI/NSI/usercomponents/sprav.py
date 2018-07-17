#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Справочник.
Класс пользовательского компонента СПРАВОЧНИК.

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
from ic.dlg import ic_dlg
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
from ic.bitmap import ic_bmp
import ic.PropertyEditor.icDefInf as icDefInf

from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

import NSI.nsi_sys.icsprav as parentModule

# Регистрация прав использования
from ic.kernel import icpermission
from ic.kernel.icaccesscontrol import ClassSecurityInfo

prm = icpermission.icPermission(id='sprav_edit', title='SpravEdit',
                                description=u'Редактирование справочников',
                                component_type='NSI')
icpermission.registerPermission(prm)


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSprav'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# Спецификация на ресурсное описание класса
ic_class_spc = dict({'__events__': {},
                     'type': 'Sprav',
                     'name': 'default',
                     'child': [],
                     'activate': 1,
                     'init_expr': None,
                     '_uuid': None,
                     '__brief_attrs__': ['name', 'description'],
                     'description': '',    # Описание справочника
    
                     'table': None,         # Имя таблицы храниения данных
                     'db': None,            # Имя БД хранения данных
                     'cache': True,         # Автоматически кэшировать?
                     'is_tab_time': False,  # Есть ли у справочника таблица временных значений?
                     'cache_frm': True,     # Автоматически кешировать формы?
                     # 'choice_form': 'spravChoiceDlgStd',    # Форма для просмотра и выбора кода справочника
                     # 'edit_form': 'spravEditDlgStd',        # Форма для редактирования справочника
                     'choice_form': '',     # Форма для просмотра и выбора кода справочника
                     'edit_form': '',       # Форма для редактирования справочника

                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description', 'choice_form', 'edit_form'],
                                        icDefInf.EDT_CHECK_BOX: ['is_tab_time', 'cache', 'cache_frm'],
                                        icDefInf.EDT_USER_PROPERTY: ['db', 'table'],
                                        },
                     '__parent__': parentModule.SPC_IC_SPRAV,
                     '__attr_hlp__': {'table': u'Паспорт таблицы храниения данных',
                                      'db': u'Имя БД хранения данных',
                                      'cache': u'Автоматически кэшировать?',
                                      'is_tab_time': u'Есть ли у справочника таблица временных значений?',
                                      'cache_frm': u'Автоматически кешировать формы?',
                                      'choice_form': u'Форма для просмотра и выбора кода справочника',
                                      'edit_form': u'Форма для редактирования справочника',
                                      },
                     })

ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('book-question.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('book-question.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['SpravLevel']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 1)

# Функции редактирования


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('db', 'table'):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('db',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('PostgreSQLDB', 'SQLiteDB'):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является БД.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK

    elif attr in ('table',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Table',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является таблицей.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('db', 'table'):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icSprav(icwidget.icSimple, parentModule.icSpravPrototype):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    security = ClassSecurityInfo()

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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icSpravPrototype.__init__(self, parent, component['name'])

        # Свойства компонента
        # Описание перечисления
        self.description = ''
        if 'description' in component:
            self.description = component['description']

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    # Установка ограничения редактирования справочника
    security.declareProtected('sprav_edit', 'Edit')

    def Edit(self, *args, **kwargs):
        return parentModule.icSpravPrototype.Edit(self, *args, **kwargs)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def getLevelCount(self):
        """
        Количество уровней.
        """
        if not self.components:
            return 0
        return len(self.components.keys())

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

    def getDBResSubSysName(self):
        """
        Имя подсистемы ресурса БД.
        """
        tab_psp = self.getICAttr('db')
        if tab_psp:
            return tab_psp[0][-1]
        return None

    def getTableName(self):
        """
        Имя объекта хранения/Таблицы.
        """
        tab_psp = self.getICAttr('table')
        if tab_psp:
            return tab_psp[0][1]
        return None

    def getTabResSubSysName(self):
        """
        Имя подсистемы ресурса таблицы.
        """
        tab_psp = self.getICAttr('table')
        if tab_psp:
            return tab_psp[0][-1]
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

    def isTabTime(self):
        """
        Есть у справочника таблица временных параметров?.
        """
        return self.getICAttr('is_tab_time')

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
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'В справочнике [%s] не определена форма выбора.' % self.name)
        return choice_form

    def getEditFormName(self):
        """
        Форма для редактирования данных справочника.
        """
        edit_form = self.getICAttr('edit_form')
        if edit_form is None:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'В справочнике [%s] не определена форма редактирования.' % self.name)
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

    def canEdit(self):
        """
        Проверка возможности редактирования справочника.
        @return: True - Зарегистрированный в программе пользователь может редактировать справочник,
            False - не может
        """
        return self.security.is_permission('sprav_edit',
                                           self.GetKernel().GetAuthUser().getPermissions())
