#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
БИЗНЕС-ОБЪЕКТ ИМЕЮЩИЙ СОСТОЯНИЕ.

ВНИМАНИЕ! Все комопненты которые могут сохранять свою историю
через компонент ObjHistory должны содержать следующие реквизиты:
'state', 'n_obj', 'dt_create', 'dt_state'.
Они создаются автоматически при добавлении нового объекта.
Имена реквизитов изменять нельзя!


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
from ic.components import icwidget
from ic.utils import util
from ic.dlg import dlgfunc
import ic.components.icResourceParser as prs
from ic.PropertyEditor import icDefInf
from ic.utils import coderror
from ic.log import log
from ic.bitmap import bmpfunc
from ic.engine import glob_functions

import work_flow.work_sys.icstateobj as parentModule
from work_flow.work_sys import icworkstorage

# Для организации реквизита-справочника состояния объекта
from . import requisite
from . import nsi_requisite

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icStateObj'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---

# ВНИМАНИЕ! Все комопненты которые могут сохранять свою историю
# через компонент ObjHistory должны содержать следующие реквизиты
# Имена реквизитов изменять нельзя!

# Спецификация реквизита-справочника состояния объекта
ic_state_requisite_spc = copy.deepcopy(nsi_requisite.ic_class_spc)
ic_state_requisite_spc['name'] = 'state'
ic_state_requisite_spc['description'] = u'Состояние объекта'
ic_state_requisite_spc['label'] = u'Состояние объекта'

# Спецификация реквизита номера объекта документа
ic_num_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_num_requisite_spc['name'] = 'n_obj'
ic_num_requisite_spc['description'] = u'Номер документа'
ic_num_requisite_spc['label'] = u'Номер документа'

# Спецификация реквизита даты создания
ic_dt_create_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_dt_create_requisite_spc['name'] = 'dt_create'
ic_dt_create_requisite_spc['type_val'] = 'DateTime'
ic_dt_create_requisite_spc['description'] = u'Дата-время создания'
ic_dt_create_requisite_spc['label'] = u'Дата-время создания'
ic_dt_create_requisite_spc['default'] = u'@datetime.datetime.now()'

# Спецификация реквизита даты-времени последней смены состояния
ic_dt_state_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_dt_state_requisite_spc['name'] = 'dt_state'
ic_dt_state_requisite_spc['type_val'] = 'DateTime'
ic_dt_state_requisite_spc['description'] = u'Дата-время последней смены состояния'
ic_dt_state_requisite_spc['label'] = u'Дата-время последней смены состояния'
ic_dt_state_requisite_spc['default'] = u'@datetime.datetime.now()'

# Спецификация реквизита имени компьютера
ic_comp_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_comp_requisite_spc['name'] = 'computer'
ic_comp_requisite_spc['description'] = u'Компьютер'
ic_comp_requisite_spc['label'] = u'Компьютер'
ic_comp_requisite_spc['default'] = u'@ic.engine.glob_functions.getComputerName()'

# Спецификация реквизита имени пользователя
ic_user_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_user_requisite_spc['name'] = 'username'
ic_user_requisite_spc['description'] = u'Пользователь'
ic_user_requisite_spc['label'] = u'Пользователь'
ic_user_requisite_spc['default'] = u'@ic.engine.glob_functions.getCurUserName()'

# Спецификация объекта
ic_class_spc = {'type': 'StateObj',
                'name': 'default',
                'child': [ic_state_requisite_spc,
                          ic_num_requisite_spc,
                          ic_dt_create_requisite_spc,
                          ic_dt_state_requisite_spc,
                          ic_comp_requisite_spc,
                          ic_user_requisite_spc],
                'activate': True,
                'init_expr': None,

                'db': None,        # БД хранения данных

                # Автоматически создавать компоненты группировки в формах
                'auto_group': False,

                # Формы управления/взаимодействия с объектом(ами)
                # Если форма не определена, то она генерируется при первом запуске,
                # добавляется в проект и затем используется.
                'init_form': None,     # Форма/Визард для создания/инициализации
                'edit_form': None,     # Форма для редактирования
                'view_form': None,     # Форма для просмотра
                'search_form': None,   # Форма поиска бизнес объекта по значениям его атрибутов
                'choice_form': None,   # Форма выбора бизнес объекта

                'report': None,        # Отчет для распечатки

                'prototype': None,     # Прототип, у которого наследуются реквизиты/атрибуты

                # Дополнительные свойства управления генерацией
                'is_page_grp_init': False,  # Производить группировку реквизитов по страницам/
                                            # или выводить все реквизиты одним списком на форме инициализации?
                'is_page_grp_edit': True,   # Производить группировку реквизитов по страницам/
                                            # или выводить все реквизиты одним списком на форме редактирования?
                'is_page_grp_view': True,   # Производить группировку реквизитов по страницам/
                                            # или выводить все реквизиты одним списком на форме просмотра?
                'is_page_grp_search': True,  # Производить группировку реквизитов по страницам/
                                             # или выводить все реквизиты одним списком на форме поиска?
    
                'do_init': None,    # Функция инициализации
                'do_edit': None,    # Функция редактирования
                'do_view': None,    # Функция просмотра
                'do_search': None,  # Функция поиска
                'do_choice': None,  # Функция выбора

                'valid_init': None,    # Функция валидации при инициализации
                'valid_edit': None,    # Функция валидации при редактировании
                'valid_del': None,     # Функция валидации при удалении

                'history': None,   # История хранения изменений состояния объекта
    
                # Обработчик события смены состояния объекта
                'on_change_state': None,

                '_uuid': None,

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_PY_SCRIPT: ['report', 'do_init', 'do_edit',
                                                            'do_view', 'do_search', 'do_choice',
                                                            'valid_init', 'valid_edit', 'valid_del',
                                                            'on_change_state'],
                                   icDefInf.EDT_TEXTLIST: ['init_users', 'edit_users', 'view_users', 'print_users',
                                                           'del_users', 'send_users'],
                                   icDefInf.EDT_USER_PROPERTY: ['db', 'init_form', 'edit_form',
                                                                'view_form', 'search_form', 'choice_form',
                                                                'prototype', 'history'],
                                   icDefInf.EDT_CHECK_BOX: ['is_page_grp_init', 'is_page_grp_edit',
                                                            'is_page_grp_view', 'is_page_grp_search',
                                                            'auto_group'],
                                   },
                '__events__': {'init': (None, None, False),
                               'ctrl': (None, None, False),
                               'del': (None, None, False),
                               'post_init': (None, None, False),
                               'post_ctrl': (None, None, False),
                               'post_del': (None, None, False),

                               'do_init': (None, 'doInit', False),
                               'do_edit': (None, 'doEdit', False),
                               'do_view': (None, 'doView', False),
                               'do_search': (None, 'doSearch', False),
                               'do_choice': (None, 'doChoice', False),
                               'valid_init': (None, 'validInit', False),
                               'valid_edit': (None, 'validEdit', False),
                               'valid_del': (None, 'validDel', False),
                               'on_change_state': (None, 'doOnChangeState', False),
                               },
                '__parent__': parentModule.SPC_IC_STATEOBJ,
                '__attr_hlp__': {'db': u'БД хранения данных',
                                 'auto_group': u'Автоматически создавать компоненты группировки в формах',
                                 'init_form': u'Форма/Визард для создания/инициализации',
                                 'edit_form': u'Форма для редактирования',
                                 'view_form': u'Форма для просмотра',
                                 'search_form': u'Форма поиска бизнес объекта по значениям его атрибутов',
                                 'choice_form': u'Форма выбора бизнес объекта',
                                 'report': u'Отчет для распечатки',
                                 'prototype': u'Прототип, у которого наследуются реквизиты/атрибуты',
                                 'is_page_grp_init': u'Производить группировку реквизитов по страницам/или выводить все реквизиты одним списком на форме инициализации?',
                                 'is_page_grp_edit': u'Производить группировку реквизитов по страницам/или выводить все реквизиты одним списком на форме редактирования?',
                                 'is_page_grp_view': u'Производить группировку реквизитов по страницам/или выводить все реквизиты одним списком на форме просмотра?',
                                 'is_page_grp_search': u'Производить группировку реквизитов по страницам/или выводить все реквизиты одним списком на форме поиска?',
                                 'do_init': u'Функция инициализации',
                                 'do_edit': u'Функция редактирования',
                                 'do_view': u'Функция просмотра',
                                 'do_search': u'Функция поиска',
                                 'do_choice': u'Функция выбора',
                                 'valid_init': u'Функция валидации при инициализации',
                                 'valid_edit': u'Функция валидации при редактировании',
                                 'valid_del': u'Функция валидации при удалении',
                                 'history': u'История хранения изменений состояния объекта',
                                 'on_change_state': u'Обработчик события смены состояния объекта',
                                 },
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('box--exclamation.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('box--exclamation.png')

#   Путь до файла документации
ic_class_doc = 'work_flow/doc/_build/html/work_flow.usercomponents.stateobj.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Requisite', 'NSIRequisite', 'TABRequisite', 'OBJRequisite']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 2, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('db', 'init_form', 'edit_form', 'view_form', 'search_form',
                'choice_form', 'prototype', 'history'):
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
            # parent = propEdt.GetPropertyGrid().GetView()
            parent = propEdt
            if not ret[0][0] in ('PostgreSQLDB', 'SQLiteDB'):
                dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                                       u'Выбранный объект не является БД.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        else:
            # Не определена БД
            parent = propEdt
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                                   u'Свойство <%s> обязательно должно быть определено для этого объекта.' % attr, parent)
            
    elif attr in ('init_form', 'edit_form', 'view_form', 'search_form', 'choice_form'):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Dialog', 'Frame', 'Panel', 'ScrolledWindow'):
                dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                                       u'Выбранный объект не является формой.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    elif attr in ('prototype',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('BusinessObj',):
                dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                                       u'Выбранный объект не является БИЗНЕС-ОБЪЕКТОМ.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    elif attr in ('history',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('ObjHistory',):
                dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                                       u'Выбранный объект не является ИСТОРИЕЙ БИЗНЕС-ОБЪЕКТА.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('db', 'init_form', 'edit_form', 'view_form', 'search_form',
                'choice_form', 'prototype', 'history'):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icStateObj(parentModule.icStateObjProto, icwidget.icSimple):
    """
    Бизнес-объект имеющий состояние.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        """
        Функция тестирования компонента таблицы в режиме редактора ресурса.

        :param res:
        :param context:
        :param parent:
        :param arg:
        :param kwarg:
        :return:
        """
        import ic.components.user.objects.ictablebrows as brws

        state_obj = glob_functions.getKernel().createObjBySpc(parent=None, res=res, context=context)

        table_name = state_obj.getTable().getName()
        log.info(u'Тестирование БИЗНЕС ОБЪЕКТА <%s>. Таблица <%s>' % (res['name'], table_name))

        cl = brws.TableBrows(None, table_name, ext='tab')
        win = cl.getObject()
        if win:
            win.Show(True)
            win.SetFocus()
        return

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
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

        parentModule.icStateObjProto.__init__(self, parent)
        
        # Свойства компонента
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        #   Создаем дочерние компоненты
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

        self.requisites = dict([(requisite.name, requisite) for requisite in self.getAllRequisites()])
    
        # Создать таблицу хранения документа
        self._createTableResource()
        
        self.getWorkStorage().container.setTable(self.getTableName())
        
    #   Свойства
    def getInitFormPsp(self):
        """
        Форма/Визард для создания/инициализации.
        """
        return self.getICAttr('init_form')

    def getSearchFormPsp(self):
        """
        Форма/Визард для поиска.
        """
        return self.getICAttr('search_form')
        
    def getChoiceFormPsp(self):
        """
        Форма для выбора объекта.
        """
        return self.getICAttr('choice_form')
    
    def getEditFormPsp(self):
        """
        Форма для редактирования.
        """
        return self.getICAttr('edit_form')
        
    def getViewFormPsp(self):
        """
        Форма для просмотра.
        """
        return self.getICAttr('view_form')
        
    def getReport(self):
        """
        Отчет для распечатки.
        """
        return self.getICAttr('report')

    def getInitUsers(self):
        """
        Список пользователей, которые могут инициализировать объект, 
            если None, то может инициализировать любой пользователь.
        """
        return self.getICAttr('init_users')
        
    def getEditUsers(self):
        """
        Список пользователей, которые могут редактировать объект, 
            если None, то может редактировать любой пользователь.
        """
        return self.getICAttr('edit_users')
        
    def getViewUsers(self):
        """
        Список пользователей, которые могут смотреть объект, 
            если None, то может смотреть любой пользователь.
        """
        return self.getICAttr('view_users')

    def getPrintUsers(self):
        """
        Список пользователей, которые могут распечатать объект, 
            если None, то может распечатать любой пользователь.
        """
        return self.getICAttr('print_users')
        
    def getDelUsers(self):
        """
        Список пользователей, которые могут удалить объект, 
            если None, то может удалить любой пользователь.
        """
        return self.getICAttr('del_users')
        
    def getDBPsp(self):
        """
        БД.
        """
        return self.getICAttr('db')
        
    def getChildrenRequisites(self):
        """
        Дочерние реквизиты и спецификации.
        """
        return self.component_lst
    
    def getStorage(self):
        """
        Хранилище.
        """
        return icworkstorage.getWorkSQLStorageByPsp(self.getDBPsp())
    
    def isPageGroupInit(self):
        """
        Производить группировку реквизитов по страницам
        или выводить все реквизиты одним списком на форме инициализации?
        """
        return self.getICAttr('is_page_grp_init')

    def isPageGroupEdit(self):
        """
        Производить группировку реквизитов по страницам
        или выводить все реквизиты одним списком на форме редактирования?
        """
        return self.getICAttr('is_page_grp_edit')

    def isPageGroupView(self):
        """
        Производить группировку реквизитов по страницам
        или выводить все реквизиты одним списком на форме инициализации?
        """
        return self.getICAttr('is_page_grp_view')

    def isPageGroupSearch(self):
        """
        Производить группировку реквизитов по страницам
        или выводить все реквизиты одним списком на форме поиска?
        """
        return self.getICAttr('is_page_grp_search')

    def getHistoryPsp(self):
        """
        Паспорт истории изменения состояния объекта.
        """
        return self.getICAttr('history')
        
    def getHistory(self):
        """
        История измений состояния объекта.
        """
        history_psp = self.getHistoryPsp()
        if history_psp and (self._history_obj is None):
            self._history_obj = self.GetKernel().Create(history_psp)
        return self._history_obj
    
    def GetPassport(self):
        """
        Переопределенная функция получения паспорта для корректной работы
        сохранения/востановления объектов из БД.
        """
        psp = icwidget.icSimple.GetPassport(self)
        new_psp = list(psp[0])
        if new_psp[-2] is None:
            new_psp[-2] = new_psp[1]+'.mtd'
        return (tuple(new_psp), )

    def doInit(self, *args, **kwargs):
        """
        Функция инициализации.

        :return: Объект функции инициализации,
            или None если не определена.
        """
        context = self.GetContext()
        context['ARGS'] = args
        context['RECORD'] = kwargs.get('requisite_values', None)
        context.update(kwargs)
        result = self.eval_attr('do_init')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка инициализации БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def doEdit(self, *args, **kwargs):
        """
        Функция редактирования.

        :return: Объект функции редактирования,
            или None если не определена.
        """
        context = self.GetContext()
        context['ARGS'] = args
        context['RECORD'] = kwargs.get('requisite_values', None)
        context.update(kwargs)
        result = self.eval_attr('do_edit')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка редактирования БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def doView(self, *args, **kwargs):
        """
        Функция просмотра.

        :return: Объект функции просмотра,
            или None если не определена.
        """
        context = self.GetContext()
        context['ARGS'] = args
        context['RECORD'] = kwargs.get('requisite_values', None)
        context.update(kwargs)
        result = self.eval_attr('do_view')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка просмотра БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def doSearch(self, *args, **kwargs):
        """
        Функция поиска.

        :return: Объект функции поиска,
            или None если не определена.
        """
        context = self.GetContext()
        context['ARGS'] = args
        context['RECORD'] = kwargs.get('requisite_values', None)
        context.update(kwargs)
        result = self.eval_attr('do_search')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка поиска БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def doChoice(self, *args, **kwargs):
        """
        Функция выбора.

        :return: Объект функции выбора,
            или None если не определена.
        """
        context = self.GetContext()
        context['ARGS'] = args
        context['RECORD'] = kwargs.get('requisite_values', None)
        context.update(kwargs)
        result = self.eval_attr('do_choice')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка выбора БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def isDoInit(self):
        """
        Определена функция инициализации?

        :return: True/False.
        """
        return self.isICAttrValue('do_init')

    def isDoEdit(self):
        """
        Определена функция редактирования?

        :return: True/False.
        """
        return self.isICAttrValue('do_edit')

    def isDoView(self):
        """
        Определена функция просмотра?

        :return: True/False.
        """
        return self.isICAttrValue('do_view')

    def isDoSearch(self):
        """
        Определена функция поиска?

        :return: True/False.
        """
        return self.isICAttrValue('do_search')

    def isDoChoice(self):
        """
        Определена функция выбора?

        :return: True/False.
        """
        return self.isICAttrValue('do_choice')

    def validInit(self, *args, **kwargs):
        """
        Функция валидации при инициализации.

        :return: True/False.
        """
        # Если функция валидации не определена,
        # то и валидацию производить не надо
        if not self.isValidInit():
            return True

        context = self.GetContext()
        context['ARGS'] = args
        context['RECORD'] = kwargs.get('requisite_values', None)
        context.update(kwargs)
        result = self.eval_attr('valid_init')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка валидации при инициализации БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return False

    def isValidInit(self):
        """
        Определена функция валидации при инициализации?

        :return: True/False.
        """
        return self.isICAttrValue('valid_init')

    def validEdit(self, *args, **kwargs):
        """
        Функция валидации при редактировании.

        :return: True/False.
        """
        # Если функция валидации не определена,
        # то и валидацию производить не надо
        if not self.isValidEdit():
            return True

        context = self.GetContext()
        context['ARGS'] = args
        context['OBJ_UUID'] = kwargs.get('obj_uuid', None)
        context['RECORD'] = kwargs.get('requisite_values', None)
        context.update(kwargs)
        result = self.eval_attr('valid_edit')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка валидации при редактировании БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return False

    def isValidEdit(self):
        """
        Определена функция валидации при редактировании?

        :return: True/False.
        """
        return self.isICAttrValue('valid_edit')

    def validDel(self, *args, **kwargs):
        """
        Функция валидации при удалении.

        :return: True/False.
        """
        # Если функция валидации не определена,
        # то и валидацию производить не надо
        if not self.isValidDel():
            return True
        else:
            print('>>>', self.isValidDel(), self.isICAttrValue('valid_del'))

        context = self.GetContext()
        context['ARGS'] = args
        context['OBJ_UUID'] = kwargs.get('obj_uuid', None)
        context['RECORD'] = kwargs.get('requisite_values', None)
        context.update(kwargs)
        result = self.eval_attr('valid_del')
        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'Ошибка валидации при удалении БИЗНЕС ОБЪЕКТА <%s>.' % self.name)
        return False

    def isValidDel(self):
        """
        Определена функция валидации при удалении?

        :return: True/False.
        """
        return self.isICAttrValue('valid_del')

    def isAutoGroup(self):
        """
        Автоматически создавать компоненты группировки в формах?
        """
        return self.getICAttr('auto_group')

    def doOnChangeState(self):
        """
        Функция обработчика смены состояния.

        :return: True/False.
        """
        context = self.GetContext()
        context['RECORD'] = self.requisites
        result = self.eval_attr('on_change_state')
        if result[0] == coderror.IC_EVAL_OK:
            return True
        else:
            log.warning(u'Ошибка обработки смены состояни ОБЪЕКТА <%s>' % self.name)
        return False
