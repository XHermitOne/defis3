#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Объект-ссылки/Справочник.
Класс пользовательского компонента ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК.
"""

import wx

from ic.dlg import dlgfunc
from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.bitmap import bmpfunc
from ic.PropertyEditor import icDefInf
from ic.log import log
from ic.engine import glob_functions

from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

import NSI.nsi_sys.ref_object as parentModule
from NSI.nsi_sys import ref_storage

# Регистрация прав использования
from ic.kernel import icpermission
from ic.kernel.icaccesscontrol import ClassSecurityInfo

prm = icpermission.icPermission(id='refobj_edit', title='RefObjectEdit',
                                description=u'Редактирование объектов-ссылок/справочников',
                                component_type='NSI')
icpermission.registerPermission(prm)

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icRefObject'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'RefObject',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                '__brief_attrs__': ['name', 'description'],
                'description': u'',  # Описание справочника

                'db': None,  # Имя БД хранения данных
                'cache': False,  # Автоматически кэшировать?

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_CHECK_BOX: ['cache'],
                                   icDefInf.EDT_USER_PROPERTY: ['db'],
                                   },
                '__parent__': parentModule.SPC_IC_REFOBJECT,
                '__attr_hlp__': {'db': u'Паспорт БД хранения данных',
                                 'cache': u'Автоматически кэшировать?',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('address-book.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('address-book.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['RefLevel']

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
    if attr in ('db', ):
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
                dlgfunc.openMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является БД.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('db', ):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icRefObject(icwidget.icSimple, parentModule.icRefObjectProto):
    """
    Класс пользовательского компонента ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    security = ClassSecurityInfo()

    component_spc = ic_class_spc

    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        """
        Функция тестирования компонента таблицы в режиме редактора ресурса.
        @param res:
        @param context:
        @param parent:
        @param arg:
        @param kwarg:
        @return:
        """
        obj = glob_functions.getKernel().createObjBySpc(parent=None, res=res, context=context)

        log.info(u'Тестирование ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК <%s>' % res['name'])
        obj.edit(parent=parent)
        return

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

        parentModule.icRefObjectProto.__init__(self, parent, component['name'])

        # Свойства компонента
        # Описание перечисления
        self.description = ''
        if 'description' in component:
            self.description = component['description']

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    # Установка ограничения редактирования справочника
    security.declareProtected('refobj_edit', 'edit')

    def Edit(self, *args, **kwargs):
        return parentModule.icRefObjectProto.Edit(self, *args, **kwargs)

    # Другое наименование метода
    edit = Edit

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
        else:
            log.warning(u'Не определена БД хранения справочника <%s>' % self.name)
        return None

    def getDBResSubSysName(self):
        """
        Имя подсистемы ресурса БД.
        """
        db_psp = self.getICAttr('db')
        if db_psp:
            return db_psp[0][-1]
        else:
            log.warning(u'Не определена БД хранения справочника <%s>' % self.name)
        return None

    def getTableName(self):
        """
        Имя объекта хранения/Таблицы.
        Это имя таблицы первого уровня.
        """
        levels = self.getLevels()
        # По умолчанию имя таблицы хранения справочника такое же как у справочника
        tab_name = levels[0].getTableName() if levels else self.getName()
        return tab_name

    def getTabResSubSysName(self):
        """
        Имя подсистемы ресурса таблицы.
        """
        # Считаем что текущий проект и есть нужная подсистема по умолчанию
        return glob_functions.getPrjName()

    def getDBPsp(self):
        """
        Паспорт БД.
        """
        return self.getICAttr('db')

    def getAutoCache(self):
        """
        Признак автоматического кэширования.
        """
        return self.getICAttr('cache')

    def canEdit(self):
        """
        Проверка возможности редактирования справочника.
        @return: True - Зарегистрированный в программе пользователь может редактировать справочник,
            False - не может
        """
        return self.security.is_permission('refobj_edit',
                                           self.GetKernel().GetAuthUser().getPermissions())

    def getStorage(self):
        """
        Хранилище.
        """
        if self._storage is None:
            self._storage = ref_storage.icRefSQLStorage(parent=self, db_psp=self.getDBPsp())
        return self._storage
