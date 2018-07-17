#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Базовый интерфейс к объектам системы, которые строятся по ресурсному описанию.
"""

import os
import wx
import ic.components.icResourceParser as prs
import ic.PropertyEditor.icDefInf as icDefInf
import ic.components.icwidget as icwidget

__version__ = (0, 0, 0, 3)


class icObjectInterface:
    """
    Базовый класс интерфейсов к объектам построенным по ресурсному описанию.
    """

    def __init__(self, parent, resource, evalSpace=None, 
                 bIndicator=False, moduleRes=None, **par):
        """
        Конструктор интерфейса.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно, если оно есть. В противном случае None.
        @type resource: C{dictionary}
        @param resource: Ресурсное описание, по которому строится компонент.
        @type evalSpace: C{dictionary}
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type bIndicator: C{bool}
        @param bIndicator: Признак отображения процесса создания объекта в статусной строке
            главного окна.
        @param moduleRes: Полное имя модуля ресурса.
        @type par: C{dictionary}
        @param par: Список дополнительных параметров, которые будут добавлены в
            пространство имен объекта.
        """
        #   Инициализация пространства имен объекта
        if evalSpace:
            self.evalSpace = evalSpace
        else:
            self.evalSpace = icwidget.icResObjContext()
         
        #   Добавляем дополнительные параметры в пространство имен
        if par:
            self.evalSpace['_dict_obj'].update(par)
            
        if moduleRes:
            path, nm = os.path.split(moduleRes)
            resource['res_module'] = nm.replace('.pyc', '.py')
            self.evalSpace['__file_res'] = moduleRes
            
        #   Учтанавливаем ссылку на интерфейс
        self.evalSpace['WrapperObj'] = self
        self._resource = resource
        self.parent = parent
        #   Создаем объект по ресурсному описанию
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=bIndicator)
        self.object = self.evalSpace['_root_obj']
        self.Init()
        
    def GetContext(self):
        """
        Возвращает контекст объекта.
        """
        return self.getObject().GetContext()
        
    def getObject(self):
        """
        Возвращает объект.
        """
        return self.object

    def GetNameObj(self, name):
        """
        Возвращает указатель на объект с указанным именем.
        """
        if name in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj'][name]
        else:
            return None

    def GetResource(self):
        """
        Возвращает ресурсное описание.
        """
        return self._resource

    def GetRootObjName(self):
        """
        Возвращает имя корневого элемента ресурса.
        """
        return self.GetResource()['name']
        
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
        if 'name' not in res:
            return
            
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
                
    def Init(self):
        """
        Переопределяемая функция инициализации объекта.
        """
        pass
