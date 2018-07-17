#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс контекста объкта системы. Контекст задает окружение объекта системы, в
котором он работает.
"""

import time
from . import io_prnt

#   Код доступа недопускающий переопределения
CODE_NOBODY = 1234567
CODE_NODEL = 1

__version__ = (0, 0, 1, 3)


class context_dict(dict):
    """
    Создаем пустой класс для того, чтобы получить доступ к конструктору словаря.
    """


class BaseContext(context_dict):
    """
    Базовый контекст.
    """

    def __init__(self, kernel=None, *arg):
        """
        Конструктор контекста.
        """
        #   Указатель на ядро системы
        self.kernel = kernel

        #   Указатель на родительский контекст
        self.parentContext = None
        #   Имя файла ресурса (с расширением), для которого создается контекст
        self.resFileName = None
        #   Имя подсистемы
        self.subsys = None
        
        context_dict.__init__(self, *arg)
    
        #   Функции прописанные в контексте
        self.func_names = []
        self['_access_keys'] = {}
        
        # Инициализация контекста
        self.init_serv_context()
        self.init_context()

        # ВНИМАНИЕ! В контексте обязательно д.б. определено ядро
        if self.kernel is None:
            from . import ickernel
            self.kernel = ickernel.getKernel()

    def add_context_func(self, func, fn=None):
        """
        Добавляет функцию в контекст. Её желательно предварительно откомпилировать.
        @param func: Откомпилированное тело функции.
        @param fn: Имя функции.
        """
        if fn:
            self['_access_keys'][fn] = CODE_NOBODY
            
        self.func_names.append(func)
        exec(func, self)    # Зачем выполнять?
            
    def init_serv_context(self):
        """
        Инициализируем сервесные ключи.
        """
        pass
        
    def init_context(self, *arg, **kwarg):
        """
        Инициализирует контекст.
        """
        pass

    def get_kernel(self):
        """
        Возвращает указатель на ядро системы.
        """
        if self.kernel:
            return self.kernel
        elif self.get_parent():
            return self.get_parent().get_kernel()

    def get_parent(self):
        """
        Возвращает указатель на родительский контекст.
        """
        return self.parentContext
        
    def reg_object(self, obj, name=None):
        """
        Регестрирует объект.
        """
        try:
            if '_dict_obj' in self:
                if name:
                    self['_dict_obj'][name] = obj
                else:
                    self['_dict_obj'][obj.name] = obj
        except AttributeError:
            io_prnt.outErr(u'Ошибка регистрации')

    def get_object(self, obj, name=None):
        """
        Получить объект.
        """
        try:
            if '_dict_obj' in self:
                if name and name in self['_dict_obj']:
                    return self['_dict_obj'][name]
        except:
            io_prnt.outErr(u'Ошибка получения объекта')
        return None


# Реализация контекста объекта системы
# Функции пространства имен формы
GET_OBJECT_SCRIPT = compile('''def GetObject(name=None):
    if name:
        return globals()['_dict_obj'][name]
    elif globals().has_key('self'):
        return globals()['self']''', '<string>', 'exec')

#   Доступ к внешнему () интерфейсу объекта.
#   - если задано имя интерфейса, доступ к определенному интерфейсу сложного
#      компонента, которые регестрируются в словаре '_interfaces'
#   - если имя не задано, доступ к интерфейсу текущего компонента (имя определяется функцией GetInterfaceName())
#   - если имя не задано и нет возможности определить инетрфейс через GetInterfaceName()
#      смотрим переменную WrapperObj (старый способ доступа к интерфейсу)
GET_INTERFACE_SCRIPT = compile('''def GetInterface(name=None):
    if name and name in globals()['_interfaces']:
        return globals()['_interfaces'][name]
    elif 'self' in globals() and globals()['self'] and globals()['self'].GetInterfaceName() in globals()['_interfaces']:
        return globals()['_interfaces'][globals()['self'].GetInterfaceName()]
    elif 'WrapperObj' in globals():
        return globals()['WrapperObj']''',  '<string>', 'exec')

GET_WRAPPER_OBJ = compile('''def GetWrapper(obj=None):
    if 'self' in globals():
        obj = obj or globals()['self']
    elif 'WrapperObj' in globals():
        obj = obj or globals()['WrapperObj']
    wrp = obj.context.GetWrapper(obj)
    return wrp''',  '<string>', 'exec')

GET_CONTEXT_FUNC = compile('''
def GetContext():
    return globals()
''', '<string>', 'exec')

# Возвращает модуль ресурса данного объекта
GET_RES_MODUL = compile('''
def GetResModule(obj=None):
    if obj:
        mod = obj.get_res_module()
    else:
        mod = globals()['self'].get_res_module()
    return mod
''', '<string>', 'exec')

# Возвращает менеджер объекта
GET_MANAGER = compile('''
def GetManager(obj=None):
    if obj:
        mngr = obj.get_manager()
    else:
        mngr = globals()['self'].get_manager()
    return mngr
''', '<string>', 'exec')

GET_OBJ_MODUL = compile('''
def GetObjModule(obj=None):
    if obj:
        mod = obj.get_obj_module()
    else:
        mod = globals()['self'].get_obj_module()
    return mod
''', '<string>', 'exec')

FIND_INTERFACE_LST = compile('''
def FindInterfaces(type=None, name=None):
    lst=[]
    if type and not name:
        for el in globals()['_interfaces_lst']:
            if el.type == type:
                lst.append(el)
    elif type and name:
        for el in globals()['_interfaces_lst']:
            if el.type == type and el.name == name:
                lst.append(el)
    else:
        for el in globals()['_interfaces_lst']:
            if el.name == name:
                lst.append(el)
    return lst
''', '<string>', 'exec')
  
FIND_OBJECT_LST = compile('''
def FindObjects(type=None, name=None):
    lst=[]
    if type and not name:
        for el in globals()['_list_obj']:
            if el.type == type:
                lst.append(el)
    elif type and name:
        for el in globals()['_list_obj']:
            if el.type == type and el.name == name:
                lst.append(el)
    else:
        for el in globals()['_list_obj']:
            if el.name == name:
                lst.append(el)
    return lst
''', '<string>', 'exec')

CREATE_OBJ = compile('''
def Create(*arg, **kwarg):
    if globals().get_kernel():
        return globals().get_kernel().Create(*arg, **kwarg)
''', '<string>', 'exec')

bInit_var = False


def init():
    global bInit_var
    
    if not bInit_var:
        import ic.components.icResourceParser as icprs
        import ic.utils.resource as icres
        import ic.imglib.common as common


class Context(BaseContext):
    """
    Контекст объектов системы.
    """

    def init_serv_context(self):
        """
        Инициализация сервесных ключей.
        """
        # Словарь специальных ключей не начинающихся с '_'
        #   Используется в ResultForm для определения ключей которые обновляются
        #   в буфферезированной форме
        # self['_access_keys'] = {}
        
        # Основные ключи, используемые в прошлых версиях системы
        self['_dict_obj'] = {}
        # Список всех созданных в этом контексте компонентов
        self['_list_obj'] = []
        #   Словарь зарегестрированных интерфейсов
        self['_interfaces'] = {}
        self['_interfaces_lst'] = []
        #   Признак блокировки сообщений от клавиатуры
        self['__block_key_down'] = False
        #   Признак запрещающий блокировки записей
        self['__block_lock_rec'] = False
        #   Режим работы компонента False - резим запуска, True - режим отладки
        self['__runtime_mode'] = 0
        #   Содержит словарь всех объектов, которые обращаются к источникам данных. Признаком таких объектов
        #   является ключ 'source' в их ресурсном описании.
        self['_has_source'] = {}
        #   Содержит словарь всех источников данных
        self['_sources'] = {}
        #   Ссылка на пространство имен <Осталось для совместимости>
        self['_esp'] = self
        #   Содержит переменную которую возвращает ic_eval, в случае если выражение
        #   является скриптом и обрабатывается функцией exec(...)
        self['_resultEval'] = None

        # Функции для доступа к объектам контекста
        # Доступ к объектам контекста (_dict_obj) - GetObject(<name>)
        self.add_context_func(GET_OBJECT_SCRIPT, 'GetObject')
        # Доступ к интерфейсу объекта (WrapperObj) - GetInterface()
        self.add_context_func(GET_INTERFACE_SCRIPT, 'GetInterface')
        # Надежный способ нахождения объекта интерфейса
        self.add_context_func(GET_WRAPPER_OBJ, 'GetWrapper')
        #
        self.add_context_func(GET_CONTEXT_FUNC, 'GetContext')
        # Поиск списка интерфейсов по типу и имени
        self.add_context_func(FIND_INTERFACE_LST, 'FindInterfaces')
        # Поиск списка объектов по типу и имени
        self.add_context_func(FIND_OBJECT_LST, 'FindObjects')
        # Возвращает модуль ресурса
        self.add_context_func(GET_RES_MODUL, 'GetResModule')
        # Возвращает модуль объекта
        self.add_context_func(GET_OBJ_MODUL, 'GetObjModule')
        # Возвращает указатель на менеджер
        self.add_context_func(GET_MANAGER, 'GetManager')
        # Создает объект через ядро
        self.add_context_func(CREATE_OBJ, 'Create')

        # Копируем ссылку на объкт методанных
        if self.kernel and self.kernel.GetContext():
            cntxt = self.kernel.GetContext()
            if 'metadata' in cntxt:
                self['metadata'] = cntxt['metadata']
            if 'schemas' in cntxt:
                self['schemas'] = cntxt['schemas']
            if 'settings' in cntxt:
                self['settings'] = cntxt['settings']
            
    def init_context(self):
        """
        Инициализация словаря.
        """
        pass
    
    def isSpecKey(self, key):
        """
        Возвращает признак специального ключа.
        """
        if type(key) not in (str, unicode):
            return True
        if key and (key.startswith('_') or key in self['_access_keys']):
            return True
        
        return False
        
    def clear_spc_structs(self):
        """
        Чистит служебные структуры.
        """
        self['_dict_obj'] = {}
        self['_list_obj'] = []
        self['_interfaces'] = {}
        self['_interfaces_lst'] = []
        self['_has_source'] = {}
        self['_sources'] = {}
        
    def register_wrapper(self, wrp, name):
        """
        Регистраци объекта обкладки для ресурса в контексте.
        """
        if '_interfaces' in self:
            self['_interfaces'][name] = wrp
        else:
            self['_interfaces'] = {name: wrp}
        
        self['_interfaces_lst'].append(wrp)
        self['_list_obj'].append(wrp)
        
    def GetWrapper(self, obj):
        """
        Функция находит wrapper для данного объекта.
        """
        if hasattr(obj, 'get_wrapper'):
            if not obj.get_wrapper():
                for wrp in self['_interfaces_lst']:
                    if wrp.is_contain_object(obj):
                        obj.set_wrapper(wrp)
                        return wrp
            else:
                return obj.get_wrapper()
        
        wrp = self.get('WrapperObj', None)
        return wrp
        
    def FindObjects(self, type=None, name=None):
        """
        Ищет список заданных объектов в контектсте.
        """
        lst = []
        if type and not name:
            for el in self['_list_obj']:
                if el and el.type == type:
                    lst.append(el)
        elif type and name:
            for el in self['_list_obj']:
                if el and el.type == type and el.name == name:
                    lst.append(el)
        else:
            for el in self['_list_obj']:
                if el and el.name == name:
                    lst.append(el)
        return lst

    def FindObject(self, type=None, name=None):
        """
        Ищет заданный объект.
        """
        if type and not name:
            for el in self['_list_obj']:
                if el and el.type == type:
                    return el
        elif type and name:
            for el in self['_list_obj']:
                if el and el.type == type and el.name == name:
                    return el
        else:
            for el in self['_list_obj']:
                if el and el.name == name:
                    return el
        # ОБъект не найден
        obj_names = [obj.name for obj in self['_list_obj']]
        io_prnt.outLog(u'Объект <%s> не найден среди объектов <%s>' % (name, obj_names))
        return None

    def FindObjByPsp(self, psp):
        """
        Ищет объект по пасспорту.
        """
        for obj in self['_list_obj']:
            if psp == obj.GetPassport():
                return obj
            
    def GetInterface(self, name):
        """
        Возвращает указатель на внешний интерфейс.
        """
        if name in self['_interfaces']:
            return self['_interfaces'][name]

    def GetObject(self, name):
        """
        Возврвщает указатель на объект.
        """
        try:
            return self['_dict_obj'][name]
        except KeyError:
            io_prnt.outLog(u'Объект <%s> не найден среди <%s>' % (name, str(self['_dict_obj'].keys())))
        return None
        
    def GetObjectLst(self):
        """
        Возвращает список всех компонентов созданных в данном контексте.
        """
        return self['_list_obj']

    def GetParentContext(self):
        """
        Возвращает указатель на родительский контекст.
        """
        return self.parentContext
        
    def SetParentContext(self, context):
        """
        Запоминает родительский контекст.
        """
        self.parentContext = context

    def setKey(self, key, obj, cod_access=CODE_NOBODY):
        """
        Функция добавляет объект в пространство имен.
        
        @param key: Ключ в пространстве имен.
        @type key: C{string}
        @param obj: Объект, который надо добавить.
        @param cod_access: Код доступа на изменение значения ключа.
        @rtype: C{bool}
        @return: Возвращает признак успешного добавления.
        """
        akey = self['_access_keys']
        try:
            if key not in akey.keys() or (key in akey.keys() and cod_access == akey[key]):
                
                if cod_access != CODE_NOBODY or (cod_access == CODE_NOBODY and key not in self):
                    self[key] = obj
                    
                if cod_access is not None:
                    self['_access_keys'][key] = cod_access
                    
                return True
        except:
            io_prnt.outErr('ERROR setKey')
                
        return False

    def getMode(self):
        """
        Возвращает режим контекста.
        """
        return self['__runtime_mode']

    def setMode(self, mode):
        """
        Устанавливает режим контекста.
        """
        self['__runtime_mode'] = mode
        
    def update_context(self, context):
        """
        Служебные ключи игнорируются.
        """
        for key, val in context.items():
            if type(key) in (str, unicode) and (key[0] == '_' or key in self.func_names):
                pass
            else:
                self[key] = val


def test(n):
    """
    Тест
    """
    init()
    t1 = time.clock()
    for x in xrange(n):
        Context()
    t2 = time.clock()
    print(u'test1 time = <%s>' % (t2 - t1))


def test2(n):
    lst = ['_resultEval', '_resultEval1', '_resultEval2', '_resultEval3', '_resultEval4',
           '_resultEval5', '_resultEval16', '_resultEval7', '_resultEval8', '_resultEval9',
           '_resultEval', '_resultEval1', '_resultEval2', '_resultEval3', '_resultEval4']
    t1 = time.clock()
    
    for x in xrange(n):
        d = {}
        for y in xrange(10):
            d[lst[y]] = y
            
    t2 = time.clock()
    print(u'test2 time = <%s>' % (t2 - t1))


def test3():
    from . import ickernel
    kernel = ickernel.icKernel()

    c1 = kernel.init_new_context()
    c2 = kernel.init_new_context()

    c2['fgh'] = 5
    c2['_resultEval'] = 'C2'
    t1 = time.clock()
    for x in xrange(10000):
        c1.update_context(c2)

    t2 = time.clock()
    
    print(u'test3 time = <%s>' % (t2 - t1))


if __name__ == '__main__':
    test(10000)
    test2(10000)
    test3()
    pass
