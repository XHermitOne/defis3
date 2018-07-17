#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс пользовательского компонента УЗЛОВОЙ ДОКУМЕНТ.
Узловые документы позволяют организовывать древовидные структуры из документов а также
организовывать связи между документами типа графов в виде ссылок.

При разработке компонента было стремление приблизиться
к функционалу метаобъекта <Документ> 1C.

Документ прикладной системы.
В общем виде документ это объект состояния,
в котором определяются операции изменения состояния.
С помощью методов документа могут выполняться внутренние
операции. Результат выполнения операции может быть смена
состояния документа.
Основные используемы методы документа:
    do_operation - выполнить операцию по имени.
    undo_operation - отмена операции по имени.
    do_operations - выполнение всех операций документа.
    undo_operations - выполнение отмены всех операций документа.

ВНИМАНИЕ! Все комопненты которые могут сохранять свою историю
через компонент ObjHistory должны содержать следующие реквизиты:
'state', 'n_obj', 'dt_create', 'dt_state'.
Они создаются автоматически при добавлении нового объекта.
Имена реквизитов изменять нельзя!

Узловые документы:
    Связи осуществляются при помощи UUIDов объектов.
    Связь документов организована двух видов:
        1. Взаимодействие в виде древовидной структуры
            Для реализации связей используются поля parent_uuid и children_uuid.
            parent_uuid - список UUIDов родительских объектов текущего объекта
            children_uuid - список UUIDов дочерних объектов текущего объекта
        2. Взаимодействие в виде ссылок (Для организации графов)
            Для реализации связей используется поле link_uuid.
            link_uuid - список UUIDов объектов на которые ссылается текущий объект

    Также присутствует поле obj_type - код справочника типов объектов
    Справочник типов объектов - справочник, определяющий правила связей объектов по типам.
    В нем должны быть определены поля:
        can_contain - список типов объектов, которые могут включаться в объект в качестве дочерних
        can_not_contain - список типов объектов, которые НЕ могут включаться в объект в качестве дочерних
        can_link - список типов объектов, на которые может ссылаться объект
        can_not_link - список типов объектов, на которые НЕ может ссылаться объект
        default - словарь значений реквизитов, заполняемых по умолчанию при создании нового объекта указанного типа

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

import copy
import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.kernel import io_prnt
import ic.PropertyEditor.icDefInf as icDefInf

import work_flow.doc_sys.icdocument as parentModule
from work_flow.work_sys import icworkbase
from work_flow.doc_sys import icoperation
from work_flow.work_sys import icworkstorage

# Для организации реквизита-справочника состояния объекта
from . import requisite
from . import nsi_requisite
from . import tab_requisite

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icNodeDocument'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

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

# Спецификация реквизита имени компьютера
ic_comp_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_comp_requisite_spc['name'] = 'computer'
ic_comp_requisite_spc['description'] = u'Компьютер'
ic_comp_requisite_spc['label'] = u'Компьютер'

# Спецификация реквизита имени пользователя
ic_user_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_user_requisite_spc['name'] = 'username'
ic_user_requisite_spc['description'] = u'Пользователь'
ic_user_requisite_spc['label'] = u'Пользователь'

# Спецификация реквизита описания
ic_description_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_description_requisite_spc['name'] = 'description'
ic_description_requisite_spc['description'] = u'Описание'
ic_description_requisite_spc['label'] = u'Описание'

# Спецификация реквизита тегов
ic_tags_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_tags_requisite_spc['name'] = 'tags'
ic_tags_requisite_spc['description'] = u'Теги через ;'
ic_tags_requisite_spc['label'] = u'Теги'

# Спецификация реквизита UUIDов родительских объектов
ic_parentuuid_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_parentuuid_requisite_spc['name'] = 'parent_uuid'
ic_parentuuid_requisite_spc['description'] = u'UUIDы родительских объектов'
ic_parentuuid_requisite_spc['label'] = u'Родительские объекты'

# Спецификация реквизита UUIDов дочерних объектов
ic_childrenuuid_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_childrenuuid_requisite_spc['name'] = 'children_uuid'
ic_childrenuuid_requisite_spc['description'] = u'UUIDы дочерних объектов'
ic_childrenuuid_requisite_spc['label'] = u'Дочерние объекты'

# Спецификация реквизита UUIDов объектов-ссылок
ic_linkuuid_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_linkuuid_requisite_spc['name'] = 'link_uuid'
ic_linkuuid_requisite_spc['description'] = u'UUIDы объектов-ссылок'
ic_linkuuid_requisite_spc['label'] = u'Ссылки на объекты'

# Спецификация реквизита-справочника типа объекта
ic_objtype_requisite_spc = copy.deepcopy(nsi_requisite.ic_class_spc)
ic_objtype_requisite_spc['name'] = 'obj_type'
ic_objtype_requisite_spc['description'] = u'Тип объекта'
ic_objtype_requisite_spc['label'] = u'Тип объекта'

# Спецификация табличного реквизита для организации дополнительных реквизитов узла
ic_extrequisites_requisite_spc = copy.deepcopy(tab_requisite.ic_class_spc)
ic_extrequisites_requisite_spc['name'] = 'ext_requisites'
ic_extrequisites_requisite_spc['description'] = u'Дополнительные реквизиты объекта'
ic_extrequisites_requisite_spc['label'] = u'Дополнительные реквизиты объекта'
ic_extrequisites_requisite_spc['child'] = []
ic_extname_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_extname_requisite_spc['name'] = 'name'
ic_extname_requisite_spc['description'] = u'Наименование дополнительного реквизита'
ic_extname_requisite_spc['label'] = u'Наименование'
ic_extrequisites_requisite_spc['child'].append(ic_extname_requisite_spc)
ic_extdescription_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_extdescription_requisite_spc['name'] = 'description'
ic_extdescription_requisite_spc['description'] = u'Описание дополнительного реквизита'
ic_extdescription_requisite_spc['label'] = u'Описание'
ic_extrequisites_requisite_spc['child'].append(ic_extdescription_requisite_spc)
ic_exttype_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_exttype_requisite_spc['name'] = 'value_type'
ic_exttype_requisite_spc['description'] = u'Тип значения дополнительного реквизита'
ic_exttype_requisite_spc['label'] = u'Тип значения'
ic_extrequisites_requisite_spc['child'].append(ic_exttype_requisite_spc)
ic_extstrvalue_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_extstrvalue_requisite_spc['name'] = 'str_value'
ic_extstrvalue_requisite_spc['description'] = u'Строковое значение дополнительного реквизита'
ic_extstrvalue_requisite_spc['label'] = u'Строковое значение'
ic_extrequisites_requisite_spc['child'].append(ic_extstrvalue_requisite_spc)
ic_extdtvalue_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_extdtvalue_requisite_spc['name'] = 'dt_value'
ic_extdtvalue_requisite_spc['type_val'] = 'DateTime'
ic_extdtvalue_requisite_spc['description'] = u'Дата-время значение дополнительного реквизита'
ic_extdtvalue_requisite_spc['label'] = u'Дата-время'
ic_extdtvalue_requisite_spc['default'] = u'@datetime.datetime.now()'
ic_extrequisites_requisite_spc['child'].append(ic_extdtvalue_requisite_spc)
ic_extintvalue_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_extintvalue_requisite_spc['name'] = 'int_value'
ic_extintvalue_requisite_spc['type_val'] = 'I'
ic_extintvalue_requisite_spc['description'] = u'Целое значение дополнительного реквизита'
ic_extintvalue_requisite_spc['label'] = u'Числовое значение'
ic_extintvalue_requisite_spc['default'] = 0
ic_extrequisites_requisite_spc['child'].append(ic_extintvalue_requisite_spc)
ic_extfloatvalue_requisite_spc = copy.deepcopy(requisite.ic_class_spc)
ic_extfloatvalue_requisite_spc['name'] = 'float_value'
ic_extfloatvalue_requisite_spc['type_val'] = 'F'
ic_extfloatvalue_requisite_spc['description'] = u'Вещественное значение дополнительного реквизита'
ic_extfloatvalue_requisite_spc['label'] = u'Вещественное значение'
ic_extfloatvalue_requisite_spc['default'] = 0.0
ic_extrequisites_requisite_spc['child'].append(ic_extfloatvalue_requisite_spc)


#   Спецификация на ресурсное описание класса
ic_class_spc = dict({'type': 'NodeDocument',
                     'name': 'default',
                     'child': [ic_state_requisite_spc,
                               ic_num_requisite_spc,
                               ic_dt_create_requisite_spc,
                               ic_dt_state_requisite_spc,
                               ic_comp_requisite_spc,
                               ic_user_requisite_spc,
                               ic_description_requisite_spc,
                               ic_tags_requisite_spc,
                               ic_objtype_requisite_spc,
                               ic_parentuuid_requisite_spc,
                               ic_childrenuuid_requisite_spc,
                               ic_linkuuid_requisite_spc,
                               ic_extrequisites_requisite_spc],
                     'activate': True,
                     'init_expr': None,
                     '_uuid': None,

                     'db': None,  # БД хранения данных

                     # Автоматически создавать компоненты группировки в формах
                     'auto_group': False,

                     # Формы управления/взаимодействия с объектом(ами)
                     # Если форма не определена, то она генерируется при первом запуске,
                     # добавляется в проект и затем используется.
                     'init_form': None,  # Форма/Визард для создания/инициализации
                     'edit_form': None,  # Форма для редактирования
                     'view_form': None,  # Форма для просмотра
                     'search_form': None,  # Форма поиска бизнес объекта по значениям его атрибутов
                     'choice_form': None,  # Форма выбора бизнес объекта

                     'report': None,  # Отчет для распечатки

                     'prototype': None,  # Прототип, у которого наследуются реквизиты/атрибуты

                     # Дополнительные свойства управления генерацией
                     'is_page_grp_init': False,  # Производить группировку реквизитов по страницам/
                     # или выводить все реквизиты одним списком на форме инициализации?
                     'is_page_grp_edit': True,  # Производить группировку реквизитов по страницам/
                     # или выводить все реквизиты одним списком на форме редактирования?
                     'is_page_grp_view': True,  # Производить группировку реквизитов по страницам/
                     # или выводить все реквизиты одним списком на форме просмотра?
                     'is_page_grp_search': True,  # Производить группировку реквизитов по страницам/
                     # или выводить все реквизиты одним списком на форме поиска?

                     'do_init': None,  # Функция инициализации
                     'do_edit': None,  # Функция редактирования
                     'do_view': None,  # Функция просмотра
                     'do_search': None,  # Функция поиска
                     'do_choice': None,  # Функция выбора

                     'valid_init': None,  # Функция валидации при инициализации
                     'valid_edit': None,  # Функция валидации при редактировании
                     'valid_del': None,  # Функция валидации при удалении

                     'history': None,  # История хранения изменений состояния объекта

                     # Обработчик события смены состояния объекта
                     'on_change_state': None,

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
                     '__events__': {},
                     '__parent__': parentModule.SPC_IC_DOCUMENT,
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
                     })
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('ic_node_document.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('ic_node_document.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Requisite', 'NSIRequisite', 'TABRequisite', 'REFRequisite',
                  'FuncOperation']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 2)

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
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является БД.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        else:
            # Не определена БД
            parent = propEdt
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'Свойство <%s> обязательно должно быть определено для этого объекта.' % attr, parent)

    elif attr in ('init_form', 'edit_form', 'view_form', 'search_form', 'choice_form'):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Dialog', 'Frame', 'Panel', 'ScrolledWindow'):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является формой.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    elif attr in ('prototype',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('BusinessObj',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является БИЗНЕС-ОБЪЕКТОМ.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    elif attr in ('history',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('ObjHistory',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является ИСТОРИЕЙ БИЗНЕС-ОБЪЕКТА.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('db', 'init_form', 'edit_form', 'view_form', 'search_form',
                'choice_form', 'prototype', 'history'):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icNodeDocument(icwidget.icSimple, parentModule.icNodeDocumentProto):
    """
    Узловой документ прикладной системы.
    В общем виде документ это объект состояния,
    в котором определяются операции изменения состояния.
    С помощью методов документа могут выполняться внутренние
    операции. Результат выполнения операции может быть смена
    состояния документа.
    Основные используемы методы документа:
        do_operation - выполнить операцию по имени.
        undo_operation - отмена операции по имени.
        do_operations - выполнение всех операций документа.
        undo_operations - выполнение отмены всех операций документа.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
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

        parentModule.icNodeDocumentProto.__init__(self, parent)
        
        # Свойства компонента
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        self.requisites = dict([(requisite.name, requisite) for requisite in self.getAllRequisites()])

        # Создать таблицу хранения документа
        self._createTableResource()

        self.getWorkStorage().container.setTable(self.getTableName())

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)
      
    #   Обработчики событий
    
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
        # Нужно отфильтровать дочерние объекты операций
        return [child for child in self.component_lst if not isinstance(child, icoperation.icOperationPrototype)]

    def getChildrenOperations(self):
        """
        Дочерние операции.
        """
        # Нужно отфильтровать дочерние объекты операций
        return [child for child in self.component_lst if isinstance(child, icoperation.icOperationPrototype)]

    # Сделано для более короткой записи
    getOperations = getChildrenOperations

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
            new_psp[-2] = new_psp[1] + '.mtd'
        return (tuple(new_psp),)

    def doInit(self, *args, **kwargs):
        """
        Функция инициализации.
        @return: Объект функции инициализации,
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
            io_prnt.outWarning(u'Ошибка инициализации БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def doEdit(self, *args, **kwargs):
        """
        Функция редактирования.
        @return: Объект функции редактирования,
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
            io_prnt.outWarning(u'Ошибка редактирования БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def doView(self, *args, **kwargs):
        """
        Функция просмотра.
        @return: Объект функции просмотра,
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
            io_prnt.outWarning(u'Ошибка просмотра БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def doSearch(self, *args, **kwargs):
        """
        Функция поиска.
        @return: Объект функции поиска,
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
            io_prnt.outWarning(u'Ошибка поиска БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def doChoice(self, *args, **kwargs):
        """
        Функция выбора.
        @return: Объект функции выбора,
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
            io_prnt.outWarning(u'Ошибка выбора БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return None

    def isDoInit(self):
        """
        Определена функция инициализации?
        @return: True/False.
        """
        return self.isICAttrValue('do_init')

    def isDoEdit(self):
        """
        Определена функция редактирования?
        @return: True/False.
        """
        return self.isICAttrValue('do_edit')

    def isDoView(self):
        """
        Определена функция просмотра?
        @return: True/False.
        """
        return self.isICAttrValue('do_view')

    def isDoSearch(self):
        """
        Определена функция поиска?
        @return: True/False.
        """
        return self.isICAttrValue('do_search')

    def isDoChoice(self):
        """
        Определена функция выбора?
        @return: True/False.
        """
        return self.isICAttrValue('do_choice')

    def validInit(self, *args, **kwargs):
        """
        Функция валидации при инициализации.
        @return: True/False.
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
            io_prnt.outWarning(u'Ошибка валидации при инициализации БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return False

    def isValidInit(self):
        """
        Определена функция валидации при инициализации?
        @return: True/False.
        """
        return self.isICAttrValue('valid_init')

    def validEdit(self, *args, **kwargs):
        """
        Функция валидации при редактировании.
        @return: True/False.
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
            io_prnt.outWarning(u'Ошибка валидации при редактировании БИЗНЕС ОБЪЕКТА <%s>' % self.name)
        return False

    def isValidEdit(self):
        """
        Определена функция валидации при редактировании?
        @return: True/False.
        """
        return self.isICAttrValue('valid_edit')

    def validDel(self, *args, **kwargs):
        """
        Функция валидации при удалении.
        @return: True/False.
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
            io_prnt.outWarning(u'Ошибка валидации при удалении БИЗНЕС ОБЪЕКТА <%s>.' % self.name)
        return False

    def isValidDel(self):
        """
        Определена функция валидации при удалении?
        @return: True/False.
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
        @return: True/False.
        """
        context = self.GetContext()
        context['RECORD'] = self.requisites
        if self.isICAttrValue('on_change_state'):
            result = self.eval_attr('on_change_state')
            if result[0] == coderror.IC_EVAL_OK:
                return True
            else:
                io_prnt.outWarning(u'Ошибка обработки смены состояни ОБЪЕКТА <%s>. Результат: %s' % (self.name, result))
        else:
            # Обработчик не определен
            # Поэтому считаем что все OK
            return True
        return False
