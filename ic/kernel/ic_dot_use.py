#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поддержка доступа к метаописаниям ресурсов системы через точку.
Доступ: metadata.THIS.frm.resource_name.ObjectType.object_name.create()
"""

# Подключение библиотек
from ic.utils import ic_mode

from ic.prj.prj_prototype import nodeReg
from ic.engine import ic_user
from ic.components import icwidget
from ic.log import log

__version__ = (0, 0, 2, 1)


class icMetaDotUsePrototype(object):
    """
    Класс поддержки доступа к метаописаниям.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Консруктор.
        """
        if DefaultPassportList_:
            self._cur_passport_list = DefaultPassportList_[:]
        else:
            self._cur_passport_list = [None, None, None, None, None]

    def create(self, parent=None, *arg, **kwarg):
        """
        Создание выбранного объекта.
        """
        if ic_mode.isDebugMode():
            log.debug('CREATE Object <%s>' % self.passport())
        kernel = ic_user.getKernel()
        if kernel:
            if 'context' in kwarg:
                if isinstance(kwarg['context'], dict):
                    # В случае если передается контекст в виде словаря
                    # необходимо создать объект контекста
                    context = icwidget.icResObjContext(kernel)
                    context.update(kwarg['context'])
                else:
                    # Контекст создаваемому объекту передается явно
                    context = kwarg['context']
                del kwarg['context']
            else:
                # Надо определить контекст
                context = icwidget.icResObjContext(kernel)
            return kernel.Create(self.passport(), parent, context=context, *arg, **kwarg)

    def get(self, parent=None, *arg, **kwarg):
        """
        Получить объект. Если не зарегистрирован в ядре, то создать его.
        """
        if ic_mode.isDebugMode():
            log.debug('GET Object <%s>' % self.passport())
        kernel = ic_user.getKernel()
        if kernel:
            # Проверить зарегистрирован ли уже объект в ядре
            name = self.passport()[0][1]
            obj = kernel.getObject(name)
            if obj:
                # Если уже зарегистрирован, то просто вернуть его
                return obj

            if 'context' in kwarg:
                if isinstance(kwarg['context'], dict):
                    # В случае если передается контекст в виде словаря
                    # необходимо создать объект контекста
                    context = icwidget.icResObjContext(kernel)
                    context.update(kwarg['context'])
                else:
                    # Контекст создаваемому объекту передается явно
                    context = kwarg['context']
                del kwarg['context']
            else:
                # Надо определить контекст
                context = icwidget.icResObjContext(kernel)
            return kernel.Create(self.passport(), parent, context=context, *arg, **kwarg)

    def passport(self):
        """
        Получение паспорта выбранного объекта.
        """
        return (tuple(self._cur_passport_list), )


class icMetaDataDotUse(icMetaDotUsePrototype):
    """
    Класс описания метаданных. Для доступа к метаописаниям через точку.
    """
    THIS_PRJ = 'THIS'

    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icMetaDotUsePrototype.__init__(self, DefaultPassportList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к метаописанию через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            

        prj = icPrjDotUse(object.__getattribute__(self, '_cur_passport_list'))

        if AttrName_ == object.__getattribute__(self, 'THIS_PRJ'):
            ic_user.icPrintStore()
            prj._cur_passport_list[-1] = ic_user.icGet('PrjName')
        else:
            prj._cur_passport_list[-1] = AttrName_
            
        return prj


class icPrjDotUse(icMetaDotUsePrototype):
    """
    Класс проекта. Для доступа к метаописаниям через точку.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icMetaDotUsePrototype.__init__(self, DefaultPassportList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к метаописанию через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            
            
        res_type = icResTypeDotUse(object.__getattribute__(self, '_cur_passport_list'))
        
        if AttrName_ in nodeReg.keys():
            res_type._cur_passport_list[-2] = '*.'+AttrName_
            
        return res_type


class icResTypeDotUse(icMetaDotUsePrototype):
    """
    Класс типа ресурса. Для доступа к метаописаниям через точку.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icMetaDotUsePrototype.__init__(self, DefaultPassportList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к метаописанию через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            
            
        res_name = icResNameDotUse(object.__getattribute__(self, '_cur_passport_list'))
        
        if res_name._cur_passport_list[-2]:
            res_name._cur_passport_list[-2] = res_name._cur_passport_list[-2].replace('*.', AttrName_+'.')
            
        return res_name


class icResNameDotUse(icMetaDotUsePrototype):
    """
    Класс имени ресурса. Для доступа к метаописаниям через точку.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icMetaDotUsePrototype.__init__(self, DefaultPassportList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к метаописанию через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            
            
        obj_type = icObjTypeDotUse(object.__getattribute__(self, '_cur_passport_list'))
        
        obj_type._cur_passport_list[0] = AttrName_
            
        return obj_type


class icObjTypeDotUse(icMetaDotUsePrototype):
    """
    Класс типа объекта. Для доступа к метаописаниям через точку.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icMetaDotUsePrototype.__init__(self, DefaultPassportList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к метаописанию через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            
            
        obj_name = icObjNameDotUse(object.__getattribute__(self, '_cur_passport_list'))
        obj_name._cur_passport_list[1] = AttrName_
        return obj_name


class icObjNameDotUse(icMetaDotUsePrototype):
    """
    Класс имени объекта. Для доступа к метаописаниям через точку.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icMetaDotUsePrototype.__init__(self, DefaultPassportList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к метаописанию через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            
            
        interface_name = icInterfaceNameDotUse(object.__getattribute__(self, '_cur_passport_list'))
        
        interface_name._cur_passport_list[2] = AttrName_
            
        return interface_name


class icInterfaceNameDotUse(icMetaDotUsePrototype):
    """
    Класс имени интерфейса объекта. Для доступа к метаописаниям через точку.
    """
    def __init__(self, DefaultPassportList_=None):
        """
        Конструктор.
        """
        icMetaDotUsePrototype.__init__(self, DefaultPassportList_)
