#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
РОЛЬ.

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
import ic.PropertyEditor.icDefInf as icDefInf

# Расширенные редакторы
from ic.PropertyEditor.ExternalEditors.multichoiceeditor import icMultiChoiceUserEdt as multiChoiceEdt

from ic.utils import icprotector
from ic.kernel import icrole
from ic.kernel import icpermission

_ = wx.GetTranslation

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icRole'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'Role',
                'name': 'default',
                'description': None,
                '_uuid': None,

                'permissions': [],  # Разрешения

                '__styles__': ic_class_styles,
                '__events__': {},

                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description'],
                                   icDefInf.EDT_USER_PROPERTY: ['permissions'],
                                   },

                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_hlp__': {'permissions': u'Разрешения',
                                 },
                }
                    
# Имя иконки класса, которые располагаются в директории
# ic/components/user/images
ic_class_pic = '@common.imgRole'
ic_class_pic2 = '@common.imgRole'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_role_wrp.icRole-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 2)


# Функции редактирования
# Формат представления пермиссии в расширенном редакторе
_permissions_label_fmt = u'%s (%s; %s; %s)'


def getPermissionsChoiceList():
    """
    Список выбора возможных разрешений.
    """
    permission_dict = icpermission.getPermissionDct()
    if permission_dict:
        permission_list = [(permission.type,
                            permission.id,
                            permission.title,
                            permission.description) for permission in permission_dict.values()]
        # Отсортировать по типу
        permission_list.sort()
        permission_choice = [_permissions_label_fmt % (permission_rec[1],
                                                       permission_rec[0],
                                                       permission_rec[2],
                                                       permission_rec[3]) for permission_rec in permission_list]
        return permission_choice
    return []
    

def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств
    (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('permissions',):
        choice = getPermissionsChoiceList()
        val = str_to_val_user_property(attr, value, propEdt, *arg, **kwarg)
        ret = multiChoiceEdt.get_user_property_editor(val, pos, size, style, propEdt,
                                                      title=_('Permissions'),
                                                      edt_txt=_('Select permissions:'), choice=choice)

    if ret is None:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('permissions',):
        return multiChoiceEdt.property_editor_ctrl(value, propEdt)


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('permissions',):
        return multiChoiceEdt.str_to_val_user_property(text, propEdt)


class icRole(icwidget.icSimple,icrole.icRole):
    """
    Роль.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    # Разрешения роли
    permissions = None
    
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

        icrole.icRole.__init__(self, self.name, self.description)
        # Установить идентификатор роли как имя объекта
        self.id = self.name

        icRole.permissions = icprotector.readonly(self._createPermissions())

    def _getPermissionAttrList(self):
        """
        Список атрибутов разрешений роли.
        """
        permissions = self.getICAttr('permissions')
        permissions_attrs = []
        for permission in permissions:
            permission_list = permission.split('(')
            permission_id = permission_list[0].strip()
            permission_attr_list = [attr.strip() for attr in permission_list[1].replace(')', '').split(';')]
            attr_rec = [permission_id] + permission_attr_list
            permissions_attrs.append(tuple(attr_rec))
        return permissions_attrs

    def _createPermissions(self, PermissionAttrList_=None):
        """
        Создать список разрешений по списку атрибутов пермиссий.
        """
        if PermissionAttrList_ is None:
            PermissionAttrList_ = self._getPermissionAttrList()
            
        permission_list = []
        for permission_attrs in PermissionAttrList_:
            new_permission_obj = icpermission.icPermission(id=permission_attrs[0],
                                                           title=permission_attrs[2],
                                                           description=permission_attrs[3],
                                                           component_type=permission_attrs[1])
            permission_list.append(new_permission_obj)
        
        return tuple(permission_list)

    def getPermissionsIdList(self):
        """
        Список идентификаторов разрешений.
        """
        permissions = self.getICAttr('permissions')
        permissions_id = [permission.split('(')[0].strip() for permission in permissions]
        return permissions_id
