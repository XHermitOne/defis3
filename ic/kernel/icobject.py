#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Описание базового компонента системы DEFIS. Все объекты системы, которые управляются
через диспечер объектов наследуются от этого компонента.
"""

import wx

from ic.utils import ic_uuid
from . import icContext
from . import icsignalsrc
from . import io_prnt
from . import icObjConnection
from . import ickernelmode
from .icaccesscontrol import ClassSecurityInfo
from ic.log import log
from ic.utils import wxfunc


__version__ = (0, 0, 2, 1)


def check_wx_dead_object(func):
    """
    .
    """
    def empty(self):
        return None

    def wrapper(self, *args, **kwargs):
        if not self:
            print('<%s> is dead' % self)
            return empty(self)
        return func(self, *args, **kwargs)
    return wrapper


class ic_list(list):
    pass


class icBasePassport(ic_list):
    """
    Базовый класс паспорта.
    """
    
    def __init__(self, *arg):
        """
        Конструктор.
        """
        ic_list.__init__(self, arg)
        
    def __eq__(self, obj):
        """
        Сравнение наборов идентификаторов. Если элемент паспорта задается
        картежем и длина картвежей разная, то элементы сверяются по самому короткому
        картежу.
        пример:
        >>> icObjectPassport((1,2,3,4,5), 7) == icObjectPassport((1,2,3,4), 8)
        >>> True
        ...
        >>> icObjectPassport((1,2,3,5), 7) == icObjectPassport((1,2,3,4), 8)
        >>> False
        """
        if not obj:
            return False
            
        for i, el in enumerate(self):
            if obj[i] == el:
                return True
            elif isinstance(el, tuple) and type(obj[i]) == type(el) and len(el) != len(obj[i]):
                bEq = True
                if len(el) > len(obj[i]):
                    for j, x in enumerate(obj[i]):
                        if x != el[j] and x is not None and el[j] is not None:
                            bEq = False
                            break
                else:
                    for j, x in enumerate(el):
                        if x != obj[i][j] and x is not None and obj[i][j] is not None:
                            bEq = False
                            break
                if bEq:
                    return True
            elif isinstance(el, tuple) and type(obj[i]) == type(el) and len(el) == len(obj[i]):
                bEq = True
                for j, x in enumerate(obj[i]):
                    if x != el[j] and x is not None and el[j] is not None:
                        bEq = False
                        break
                if bEq:
                    return True
        return False


class icObjectPassport(icBasePassport):
    """
    Класс описывающий множество идентификаторов объекта. Используется для идентификации
    объекта в системе. Первый элемент задает идентификатор описания объекта (тип объекта системы):
        - тип объекта,
        - имя объекта,
        - интерфейс компонента (для составных компонентов уникальным является имя интерфейса)
        - модуль,
        - подсистема,
        Пример 1 (Элемент ресурса): icObjectPassport(('Button','btn1',None,'buttonPanel.frm','STD'), uuid);
        Пример 2 (Элемент интерфейса): icObjectPassport(('Button','btn1',None,'buttonInterface.py','STD'), uuid);
        Пример 3 (Корневой элемент ресурса): icObjectPassport((None, None, None,'buttonInterface.py','STD'), uuid);
        Пример 4 (Элемент шаблона в составе ресурса): icObjectPassport(('Button','btn1', 'templateName','buttonPanel.frm','STD'), uuid);
            'templateName' - определяет имя объекта шаблона в ресурсе.
    Второй элемент зарезервирован под идентификатор объекта. Третий под uuid.
    """

    def __init__(self, *arg):
        """
        Конструктор.
        """
        icBasePassport.__init__(self, *arg)

    def getDescrId(self):
        """
        Возвращает идентификатор описания.
        @rtype: C{tuple}
        @return: Картеж заает идентификатор описания объекта - тип объекта,
            имя объекта, модуль, подсистема.
        """
        return self[0]
        
    def getDescrType(self):
        """
        Возвращает тип объекта из идентификатора описания.
        """
        return self.getDescrId()[0]

    def getDescrName(self):
        """
        Возвращает имя объекта из идентификатора описания.
        """
        return self.getDescrId()[1]

    def getDescrInterface(self):
        """
        Возвращает имя интерфейса из идентификатора описания.
        """
        return self.getDescrId()[2]
        
    def getDescrMod(self):
        """
        Возвращает имя модуля/ресурса объекта из идентификатора описания.
        """
        return self.getDescrId()[3]
        
    def getDescrSubsys(self):
        """
        Возвращает имя подсистемы объекта из идентификатора описания.
        """
        return self.getDescrId()[4]
    
    def get_id(self):
        """
        Возвращает идентификатор объекта.
        """
        if len(self) > 1:
            return self[1]

    def get_uuid(self):
        """
        Возвращает UUID идентификатор объекта.
        """
        if len(self) > 2:
            return self[2]
        
    type = property(getDescrType)
    name = property(getDescrName)
    interface = property(getDescrInterface)
    mod = property(getDescrMod)
    subsys = property(getDescrSubsys)
    id = property(get_id)
    uuid = property(get_uuid)


def getResPSP(resName, subsys=None, comp_interface=None):
    """
    Генрирует паспорт корневого объекта ресурса.
    """
    return icObjectPassport((None,None, comp_interface, resName, subsys))


def deco_func(func, pre=None, post=None):
    """
    Функция обкладки.
    @type func: C{types.FunctionType}
    @param func: Исходная функция.
    @type pre: C{types.FunctionType}
    @param pre: Функция обработки параметров функции. Возвращает картеж: 1-й элемент картеж параметров
        исходной функции, 2-й элемент словарь именованных параметров исходной функции.
    @type post: C{types.FunctionType}
    @param post: Функция обработки результатов функции. В качестве параметров использует выход исходной
        функции и ее входные параметры.
    """
    def new_func(*arg, **kwarg):
        if pre:
            arg, kwarg = pre(*arg, **kwarg)
        ret = func(*arg, **kwarg)
        
        if post:
            return post(ret, *arg, **kwarg)
        else:
            return ret
    
    return new_func


class icMetaObject(type):

    def __new__(cls, classname, bases, classdict):
        # Собираем список разрешений для объекта
        return super(icMetaObject, cls).__new__(cls, classname, bases, classdict)


class icObject(object):
    """
    Базовый класс объектов системы.
    """
    __metaclass__ = icMetaObject
    security = ClassSecurityInfo()
    
    def __init__(self, name=None, id=-1, context=None, bCreate=False,
                 cmpInterface=None, typ=None, *arg, **kwarg):
        """
        Конструктор.
        @type name: C{string}
        @param name: Имя объекта.
        @type id: C{int}
        @param id: Идентификатор объекта.
        @type context: C{icContext}
        @param context: Окружение (контекст) объекта.
        @type bCreate: C{bool}
        @param bCreate: Признак создания нового окружения объекта. Если = True, то
            создается новое окружение и из старого заимствуются объекты родительского
            контекста.
        @type cmpInterface: C{icObject}
        @param cmpInterface: Имя интерфеса, которому принадлежит объект (в случае
            комбинированных компонентов).
        """
        #
        self.permissions = list()
        #   Тип объекта
        if typ:
            self.type = typ
        else:
            self.type = self.__class__.__name__
        #   Имя объекта
        self.name = name
        # 
        self.__wrapper = None
        #   Идентификатор объекта системы в рабочем состоянии. При каждом создании
        #   он может быть разным.
        self._uniqId = id
        #   Уникальный идентификатор объекта описания (ресурса, если он есть)
        self._uuid = None
        #   Уникальный универсальный идентификатор объекта
        self._uuidObject = ic_uuid.get_uuid()
        #   Описание прав доступа к данному объект
        self._acl = None
        #   Атрибуты, за которыми ведется наблюдение
        self.__spy_attr = []
        #   Функции, за которыми ведется наблюдение
        self.__spy_function = []
        self.spy_function_dct = {}
        #   Паспорт объекта
        if context and not isinstance(context, dict):
            rfn = context.resFileName
            subsys = context.subsys
        else:
            rfn = None
            subsys = None
        
        #   Определяем паспорт объекта
        self.__interface = cmpInterface
        self.__passport = icObjectPassport((self.type, self.name, cmpInterface, rfn, subsys), id, self._uuidObject)
        #   Список соединений, в котором объект выступает в качестве источника
        self.srcCntLst = []
        #   Список соединений, в котором объект выступает в качестве приемника
        self.slotCntLst = []
        #   Список преобразователей событий в сигналы базовой сигнальной ситемы
        self.convLst = []
        #   Создаем контекст
        if context is None:
            self.context = icContext.Context()
        #   Заимствуем пространство имен (кроме служебных)
        elif bCreate:
            self.context = icContext.Context()
            self.context.update_context(context)
            self.context.SetParentContext(context)
        #   Полностью заимствуем контекст
        else:
            self.context = context

        self.init_object()

        # Регестрируем соединения с данным объектом
        self._reg_connection()
        
    def set_wrapper(self, wrp):
        """
        Устанавливает ссылку на объект обработчика.
        """
        self.__wrapper = wrp

    def get_wrapper(self):
        """
        Возвращает ссылку на объект обработчика.
        """
        return self.__wrapper

    def __getattribute__(self, name):
        """
        Доступ к атрибуту.
        """
        # Если ядро определяем инициализировано ядро или нет.
        # Для доступу к объектам, нобходимо сначала залогинится

        if name != 'spy_function_dct':
            try:
                dct = object.__getattribute__(self, 'spy_function_dct')
                if name in dct:
                    return dct[name]
            except AttributeError:
                object.__setattr__(self, 'spy_function_dct', {})
                
            # Проверяем права доступа
            if name not in ('_User', 'context', 'getPermissions', 'roles', 'permissions'):
                try:
                    context = object.__getattribute__(self, 'context')
                    security = object.__getattribute__(self, 'security')
                    user = context.get_kernel()._User
                    
                    # Сверяем список разрешений пользователя с разрешением на доступ к 
                    # данному атрибуту
                    if user and security:
                        security.can_access(name, user.getPermissions())
                except AttributeError:
                    pass

        val = super(icObject, self).__getattribute__(name)

        return val

    def __setattr__(self, name, value):
        """
        Переопределяем доступ к атрибуту.
        """
        class_obj = object.__getattribute__(self, '__class__')
        object.__setattr__(self, name, value)

        if wxfunc.isWxDeadObject(self):
            print('%s Is WX Dead Object' % class_obj)
            return

        try:
            if self.__spy_attr and name in self.__spy_attr:
                self._generate_changed_attr_signal(name, value)
        except AttributeError:
            self.__spy_attr = []

    def _reg_connection(self):
        """
        Определяется список соедиениий в которых объект выступает в качестве
        приемника или источника.
        """
        try:
            kernel = self.context.get_kernel()
        except:
            kernel = None
            io_prnt.outLog(u'WARNING! Ядро в контексте не определено')
            
        if kernel and hasattr(kernel, 'getConnectionByObject'):
            self.srcCntLst, self.slotCntLst = kernel.getConnectionByObject(self)
            if self.srcCntLst:
                io_prnt.outLog(u'Объект: %s. Зарегестрированы исходящие соединения:%s' % (self.name, self.srcCntLst))
            if self.slotCntLst:
                io_prnt.outLog(u'Объект: %s. Зарегестрированы входящие соединения:%s' % (self.name, self.slotCntLst))
            
            #   Создаем источники
            # Регестрируем атрибуты за которыми ведется наблюдение
            for con in self.srcCntLst:
                if issubclass(con.src.__class__, icsignalsrc.icChangedAttrSrc) and not con.src.attr.startswith('_'):
                    self.__spy_attr.append(con.src.attr)
                elif issubclass(con.src.__class__, icsignalsrc.icPostFuncSrc):
                    # Обкладываем функцию
                    fn = con.src.func_name
                    if fn in self.__class__.__dict__:
                        self.spy_function_dct[fn] = self._post_func(getattr(self, fn))
                        
            # Прописываем в слоте указатель на объект, к которому приписан слот
            for con in self.slotCntLst:
                for slot in con.slotLst:
                    if slot.GetPassportLinkObj() == self.GetPassport():
                        slot.setObject(self)
                
    # Функции генерации сигналов
    def _generate_changed_attr_signal(self, attr, value, *arg, **kwarg):
        """
        Генерирует сигналы об изменнении атрибутов объекта.
        """
        for con in self.srcCntLst:
            if issubclass(con.src.__class__, icsignalsrc.icChangedAttrSrc) and con.src.attr == attr:
                sign = con.src.generate(attr, value, self)
                self.send_signal(sign, con)
        
    def _generate_pre_func_signal(self):
        """
        Генерация сигнала при входе в функцию.
        """
        pass
        
    def _generate_post_func_signal(self, result, name):
        """
        Генерация сигнала при выходе из функции.
        @param result: Результат функции.
        @param name: Имя функции.
        """
        for con in self.srcCntLst:
            if issubclass(con.src.__class__, icsignalsrc.icPostFuncSrc) and con.src.func_name == name:
                sign = con.src.generate(obj=self)
                self.send_signal(sign, con)
        
    def _post_func(self, func):
        """
        Функция обкладки.
        @type func: C{types.FunctionType}
        @param func: Исходная функция.
        """
        def new_func(*arg, **kwarg):
            result = func(*arg, **kwarg)
            return self._generate_post_func_signal(result, func.__name__)
        
        return new_func

    def init_object(self):
        """
        Инициализация объекта (переопределяемая функция).
        """
        pass
        
    def GetACL(self):
        """
        Возвращает список описаний доступа пользоувателей к объекту.
        """
        pass
        
    def GenObjectUUID(self):
        """
        Генерируется уникальный универсальный идентификатор объекта.
        В отличии от uuid комопненета (и id объекта) он для всех объектов разный.
        """
        return self._uuidObject
            
    def GetContext(self):
        """
        Возвращает указатель на контекст.
        """
        return self.context

    def GetObject(self, name):
        """
        Возвращает указатель на объект
        """
        return self.context.GetObject(name)
    
    def GetKernel(self):
        """
        Возвращает указатель на ядро.
        """
        if self.context:
            return self.context.get_kernel()
        else:
            log.warning('Not define context in object <%s>' % self)
            
    def GetComponentInterface(self):
        """
        Возвращает указатель на интерфейс, работающий с данным компонентом.
        """
        if self.__interface and ('_interfaces' in self.GetContext() and
           self.__interface in self.GetContext()['_interfaces']):
            return self.GetContext()['_interfaces'][self.__interface]

    def GetInterfaceName(self):
        """
        Возвращает указатель на интерфейс, работающий с данным компонентом.
        """
        return self.__interface

    def GetObjectUUID(self):
        """
        Возвращает уникальный универсальный идентификатор объекта.
        """
        return self._uuidObject

    def GetPassport(self):
        """
        Возвращает паспорт объекта.
        """
        return self.__passport

    def isSamePassport(self, passport):
        """
        Проверка на тот же паспорт что и у объекта.
        @param passport: Проверяемый паспорт.
        @return: True - паспорт соответствует паспорту объекта / False - нет.
        """
        return self.__passport == passport

    def isPassport(self, passport):
        """
        Проверка является ли проверяемый паспорт паспортом в действительности.
        @param passport: Проверяемый паспорт.
        @return: True - это паспорт. False - нет.
        """
        from ic.utils import ic_util
        return ic_util.is_pasport(passport)

    def GetUniqId(self):
        """
        Возвращает уникальный идентификатор объекта в приложении.
        """
        return self._uniqId

    def GetUUID(self):
        """
        Возвращает UUID компонента, который определен в описании компонента.
        """
        return self._uuid

    def IsDebugMode(self):
        """
        Возвращает признак режима отладки.
        """
        return ickernelmode.DEBUG_MODE

    def get_replace_object(self):
        """
        Возвращает указатель на объект, который встраивается в создаваемый компонент
        парсером.
        """
        return self

    def send_signal(self, signal, con):
        """
        Посылаем сигнал.
        @type signal: C{icSignal}
        @param signal: Возбужденный сигнал.
        @type con: C{icConnection}
        @param con: Соединение, по которому передается сигнал.
        """
        # Проверяем сигнал на соответствие соединению
        if not con.isValidSignal(signal):
            io_prnt.outLog(u'WARRNING. Сигнал <%s> не соответствует соединению <%s>' % (signal, con))
            return False
        # Передаем сигнал на слоты
        kernel = self.context.get_kernel()
        if kernel:
            if issubclass(con.__class__, icObjConnection.icDirectConnection):
                return kernel.send_signal(signal, con.getSlotLst())
            else:
                # Правильно post_signal
                return kernel.post_signal(signal, con.getSlotLst())
        
        return False
        
    def SetContext(self, cont):
        """
        Устанавливает контекст объекта.
        """
        self.context = cont


def test():
    icObject()
    psp1 = icObjectPassport((1, 2, 3, 4, 5), 7)
    psp2 = icObjectPassport((1, 2, 3, 4), 8)
    psp3 = icObjectPassport((1, 2, 3, 5), 7)
    psp4 = icObjectPassport((1, 2, 3, 5), 8)
    psp5 = icObjectPassport((1, 2, 3, 4, None), 8)
    psp6 = icObjectPassport((1, 2, 3, 5), 9, 'aa1')
    psp7 = icObjectPassport((1, 2, 3, 4, None), 8, 'aa1')
    
    print(u'icObjectPassport((1,2,3,4,5), 7)==icObjectPassport((1,2,3,4), 8) <%s>' % (psp1 == psp2))
    print(u'icObjectPassport((1,2,3,5), 7) == icObjectPassport((1,2,3,4), 8) <%s>' % (psp3 == psp2))
    print(u'icObjectPassport((1,2,3,5), 8) == icObjectPassport((1,2,3,4), 8) <%s>' % (psp4 == psp2))
    print(u'icObjectPassport((1,2,3,4,5), 7)==icObjectPassport((1,2,3,4,None), 8) <%s>' % (psp1 == psp5))
    print(u'icObjectPassport((1,2,3,5), 9, \'aa1\')==icObjectPassport((1,2,3,4,None), 8, \'aa1\') <%s>' % (psp6 == psp7))


if __name__ == '__main__':
    test()
