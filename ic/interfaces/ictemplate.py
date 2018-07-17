#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс шаблона.
"""

import wx
import ic.utils.util as util
import ic.PropertyEditor.icDefInf as icDefInf
from ic.PropertyEditor.images import editorimg
import ic.components.icwidget as icwidget
import copy

#   Спецификация на объект группы
SPC_IC_TEMPLATE = {'name': 'default',
                   'type': 'TEMPLATE',
                   'child': [],
                   'nest': None,    # Задает гнездо строкой вида <тип:имя> из списка возможных гнезд

                   '__styles__': {'DEFAULT': 0},
                   '__lists__': {'nest': []},
                   '__attr_types__': {icDefInf.EDT_CHOICE: ['nest']},
                   '__parent__': icwidget.SPC_IC_BASE,
                   '__attr_hlp__': {'nest': u'Задает гнездо строкой вида <тип:имя> из списка возможных гнезд',
                                    },
                   }

__version__ = (0, 0, 1, 2)


def init_component_interface(modSpace, **replDct):
    """
    Инициализация пространства имен модуля дочернего класса.
    """
    if modSpace:
        modSpace['ic_class_type'] = icDefInf._icUserType

        #   Имя пользовательского класса
        modSpace['ic_class_name'] = 'CStdGridPanel'

        #   Описание стилей компонента
        modSpace['ic_class_styles'] = {'DEFAULT': 0}

        #   Спецификация на ресурсное описание пользовательского класса
        modSpace['ic_class_spc'] = SPC_IC_TEMPLATE
        modSpace['ic_class_spc']['__styles__'] = modSpace['ic_class_styles']

        #   Имя иконки класса, которые располагаются в директории
        #   ic/components/user/images
        modSpace['ic_class_pic'] = editorimg.interface.GetBitmap()      # '@common.imgEdtInterface'
        modSpace['ic_class_pic2'] = editorimg.interface.GetBitmap()     # '@common.imgEdtInterface'

        #   Путь до файла документации
        modSpace['ic_class_doc'] = None
                            
        #   Список компонентов, которые могут содержаться в компоненте
        modSpace['ic_can_contain'] = -1

        #   Список компонентов, которые не могут содержаться в компоненте, если не определен
        #   список ic_can_contain
        modSpace['ic_can_not_contain'] = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

        for key, val in replDct.items():
            modSpace[key] = val


def inherit_component_interface(modSpace, parentModule, **replDct):
    """
    Инициализация пространства имен модуля дочернего класса.
    """
    if modSpace:
        modSpace['ic_class_type'] = parentModule.ic_class_type

        #   Имя пользовательского класса
        modSpace['ic_class_name'] = None

        #   Описание стилей компонента
        modSpace['ic_class_styles'] = parentModule.ic_class_styles or {'DEFAULT': 0}

        #   Спецификация на ресурсное описание пользовательского класса
        modSpace['ic_class_spc'] = parentModule.ic_class_spc
        modSpace['ic_class_spc']['__styles__'] = modSpace['ic_class_styles']

        #   Имя иконки класса, которые располагаются в директории
        #   ic/components/user/images
        modSpace['ic_class_pic'] = parentModule.ic_class_pic
        modSpace['ic_class_pic2'] = parentModule.ic_class_pic2

        #   Путь до файла документации
        modSpace['ic_class_doc'] = None
                            
        #   Список компонентов, которые могут содержаться в компоненте
        modSpace['ic_can_contain'] = parentModule.ic_can_contain

        #   Список компонентов, которые не могут содержаться в компоненте, если не определен
        #   список ic_can_contain
        modSpace['ic_can_not_contain'] = parentModule.ic_can_not_contain

        # Функции пользовательских редакторов
        modSpace['get_user_property_editor'] = getattr(parentModule, 'get_user_property_editor', None)
        modSpace['property_editor_ctrl'] = getattr(parentModule, 'property_editor_ctrl', None)
        modSpace['str_to_val_user_property'] = getattr(parentModule, 'str_to_val_user_property', None)
        modSpace['property_editor_draw'] = getattr(parentModule, 'property_editor_draw', None)
        
        for key, val in replDct.items():
            modSpace[key] = val


class res_dict(dict):
    """
    Создаем пустой класс для того, чтобы получить доступ к конструктору словаря.
    """
    pass


CHLS = set(icDefInf.icContainerAttr)


class templateResDict(res_dict):
    """
    Ресурсное описание шаблона.
    """

    def __init__(self, *arg):
        res_dict.__init__(self, *arg)

    def __setitem__(self, key, item):
        pass


class icTemplateInterface(icwidget.icBase):
    """
    Интерфейс шаблона.
    """
    replace_spc_keys = []
    std_replace_spc_keys = ['size', 'position', 'span', 'proportion', 'flag', 'border']
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания шаблона.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        component = util.icSpcDefStruct(SPC_IC_TEMPLATE, component)
        icwidget.icBase.__init__(self, parent, id, component, logType, evalSpace)
        #   Определение гнезда компонента
        self._init_nest()
        
        # Словарь объектов интерфейса
        self._reg_objects = {}
        
        # Инициализация ресурса шаблона
        self._templRes = None
        self._init_template_resource()
        
        # Достраиваем ресурс компонента с учетом шаблона
        self.resource = self._build_resource()
        
        #   Наследуем uuid, для того чтобы избежать проблем
        # с буферизируемыми компилированными выражениями -
        # там uuid используется как часть уникального идентификатора выражения
        self.resource['_uuid'] = component['_uuid']
        
        #   Атрибуты гарфического редактора
        if '__item_id' in component:
            self.resource['__item_id'] = component['__item_id']
        
        # Наследование свойств описания
        self._inherit_property(component)
        
        # Регистрируемся в контексте
        self.context.register_wrapper(self, self.name)
        
    def _inherit_property(self, component):
        """
        Inherit component property.
        """
        rsk = self.resource.keys()
        for key in icTemplateInterface.std_replace_spc_keys + (getattr(self, 'replace_spc_keys', None) or []):
            if key in rsk:
                self.resource[key] = component[key]
        
    def _init_nest(self, nest=None):
        """
        Определяет гнездо компонента.
        """
        if nest:
            self._nest = nest
        elif 'nest' in self.resource and self.resource['nest']:
            self._nest = self.resource['nest'].split(':')
        elif 'nest_name' in self.resource:
            self._nest = self.resource['nest_type'], self.resource['nest_name']
        else:
            self._nest = None
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        pass

    def get_template(self):
        """
        Возвращет шаблон компонента.
        """
        return self._templRes or resource
        
    def is_contain_object(self, obj, tmp=None):
        """
        Определяет содержит ли шаблон объект.
        """
        tmp = tmp or self.get_template()
        if tmp.get('_uuid', None) == obj.GetUUID():
            return True
        
        optLst = list(set(tmp.keys()) & CHLS)
        if optLst:
            for el in tmp[optLst[0]]:
                if self.is_contain_object(obj, el):
                    return True
        
    def _build_resource(self):
        """
        Собирает ресурс из ресурса компонента и ресурса шаблона.
        """
        if self._templRes and 'child' in self._templRes:
            chld = self.resource['child']
            # Вставляемым в гнездо компонентам необходимо прописать имя интерфейса
            # класса обработчика если он есть - это будет родительский интерфейс.
            self.resource = copy.deepcopy(self._templRes)
            # Ищем гнездо для вставления дочерних элементов (считаем, что у
            # нас односвязные компоненты)
            if chld and self._nest not in (None, '', 'None') and self._nest[1]:
                res = self._findres(self.GetResource(), self._nest[1], self._nest[0])
                if res:
                    optLst = list(set(res.keys()) & set(icDefInf.icContainerAttr))
                    if optLst:
                        res[optLst[0]] = chld
        elif self._templRes:
            self.resource = copy.deepcopy(self._templRes)    
        return self.resource

    def _findres(self, res, nameObj, typeObj):
        """
        Ищет ресурс нужного объекта по дереву ресурса.
        @type res: C{dictionary}
        @param res: Ресурсное описание.
        @type nameObj: C{string}
        @param nameObj: Имя объекта.
        @type typeObj: C{string}
        @param typeObj: Тип объекта.
        @rtype: C{dictionary}
        @return: Ресурсное описание найденного объекта.
        """
        if ((typeObj is None and res['name'] == nameObj) or
           (res['type'] == typeObj and res['name'] == nameObj)):
            return res
        
        optLst = list(set(res.keys()) & set(icDefInf.icContainerAttr))
        for key in optLst:
            if isinstance(res[key], list):
                for rs in res[key]:
                    r = self._findres(rs, nameObj, typeObj)
                    if r:
                        return r
            elif isinstance(res[key], dict):
                r = self._findres(res[key], nameObj, typeObj)
                if r:
                    return r
            
    def GetObjectResource(self, nameObj, typeObj=None, resource=None):
        """
        Возвращает ресурс нужного объекта.
        @type nameObj: C{string}
        @param nameObj: Имя объекта.
        @type typeObj: C{string}
        @param typeObj: Тип объекта.
        @rtype: C{dictionary}
        @return: Ресурсное описание найденного объекта.
        """
        if resource is None:
            return self._findres(self.GetResource(), nameObj, typeObj)
        else:
            return self._findres(resource, nameObj, typeObj)
          
    def init_component(self, context=None, *arg, **kwarg):
        """
        Инициализация компонента. Вызывается парсером после создания компонента.
        """
        pass

    def reg_object(self, object, name=None):
        """
        Регистрация объекта.
        """
        if name:
            self._reg_objects[name] = object
        else:
            self._reg_objects[object.name] = object
            
    def getRegObjDict(self):
        """
        Возвращает словарь зарегестрированных объектов.
        """
        return self._reg_objects
        
    def getRegObj(self, name):
        """
        По имени возвращает зарегестрированный объект интерфейса.
        """
        if name in self._reg_objects:
            return self._reg_objects[name]
    
    def GetPosition(self):
        """
        Для графического редактора.
        """
        return self.GetContext().GetObject(self.resource['name']).GetPosition()
    
    def SetPosition(self, pos):
        self.GetContext().GetObject(self.resource['name']).SetPosition(pos)

    def GetSize(self, size):
        return self.GetContext().GetObject(self.resource['name']).GetSize()

    def SetSize(self, size):
        self.GetContext().GetObject(self.resource['name']).SetSize(size)


def test():
    lst = {'name': 1,
           'child': [{'name': 2},
                     {'name': 3,
                      'child': [{'name': 4, 'child': []},
                                {'name': 5, 'child': []},
                                ]},
                     {'name': 4}
                     ]}
    rs = find_nest(lst)


if __name__ == '__main__':
    test()
