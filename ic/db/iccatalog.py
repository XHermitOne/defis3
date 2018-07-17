#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Основные моменты:
- Каталог является аналогом списка и хранит специальные объеты ссылок на
    регистрируемые объекты
- Атирбуты объекта ссылки:
    1) path: идентификатор объекта
    2) pobj: указатель на объект
    3) otype: тип объекта
    4) title: название объекта
    5) description: описание объекта
    6) reg_time (datetime): время регистрации
    7) act_time (datetime): время актуальности в каталоге
    8) pic: путь до картинки
    9) security: Описание разрешений на действие с элементом.
    ... дополнительные атрибуты
"""

from ic.interfaces.icabstract import abstract
import time
import datetime
import wx
# Исключения
import exceptions

_ = wx.GetTranslation


class PathExistException(exceptions.Exception):
    """
    Заданный путь существует.
    """
    def __init__(self, args=None, user=None):
        self.args = args


class InvalidCatalogItemTypeException(exceptions.Exception):
    """
    Не верный тип элемента каталога.
    """
    def __init__(self, args=None, user=None):
        self.args = args

FLD_DIV = '/'


class icAbsItemCatalog(object):
    """
    Абстрактный класс элемента каталога.
    """
    def save(self):
        abstract()
        
    def can_contain_item(self, item):
        """
        Признак возможности добавления элемента в качестве дочернего.
        """
        abstract()

DEFAULT_OTYPE = 'object'


class icItemCatalog(icAbsItemCatalog):    
    """
    Элемент каталога.
    """
    _icon = None
    catalog_type = DEFAULT_OTYPE
    
    @staticmethod
    def get_pic(bInit=False):
        """
        Инициализация картинку.
        """
        if not icItemCatalog._icon or bInit:
            try:
                from ic.imglib import newstyle_img
                icItemCatalog._icon = newstyle_img.getfile_ubBitmap()
            except wx.PyNoAppError:
                icItemCatalog._icon = None
        return icItemCatalog._icon
            
    def __init__(self, path, pobj, title='', description='', 
                 reg_time=None, act_time=None, pic=None, *arg, **kwarg):
        """
        Конструктор.
        @param path: Идентификатор объекта.
        @param pobj: Указатель на объект.
        @param otype: Тип объекта.
        @param title: Заголовок.
        @param description: Описание объекта.
        @type reg_time: C{string}
        @param reg_time: Время регистрации в формате yyyy-mm-dd hh:MM:ss.
        @type act_time: C{string}
        @param act_time: Время актуальности в формате yyyy-mm-dd hh:MM:ss.
        @param pic: путь до соответствующей картинки.
        @param id: Идентификатор в хранилище.
        @param catalog: Ссылка на каталог, в котором зарегистрирован элемент.
        """
        self.get_pic(bInit=True)
        self.id = kwarg.get('id', None)
        self.path = path
        self.pobj = pobj
        self.title = title
        self.description = description
        self.pic = pic
        self.catalog = kwarg.get('catalog', None)
        
        if reg_time is None:
            lt = time.localtime()
            self.reg_time = str(datetime.datetime(*(time.localtime()[:7])))[:19]
        else:
            self.reg_time = reg_time
            
        self.act_time = act_time
        # Устанавливает дополнительные атрибуты
        for key, val in kwarg.items():
            setattr(self, key, val)

    def __getitem__(self, val):
        try:
            return getattr(self, val)
        except AttributeError:
            raise KeyError, val
            
    def save(self):
        pass
    
    def pointer(self):
        return str(self.pobj)
        
    def get_parent_item(self):
        """
        Возвращает родительский элемент.
        """
        return self.catalog.get_parent_item(self)
        
    def get_name(self):
        """
        Возвращает имя объекта
        """
        if self.path:
            return norm(self.path).split(FLD_DIV)[-1]
            
        return ''
        
    def get_sp(self):
        if self.catalog.get_child_path_lst(self.path):
            return ''
        else:
            return ' '
    
    def can_contain_item(self, item):
        return True


class icFolderItem(icItemCatalog):
    """
    Элемент папки.
    """
    _icon = None
    catalog_type = 'Folder'
    
    @staticmethod
    def get_pic(bInit=False):
        """
        Инициализация картинку.
        """
        if not icFolderItem._icon or bInit:
            try:
                from ic.imglib import newstyle_img
                icFolderItem._icon = newstyle_img.getfolder_ubBitmap()
            except wx.PyNoAppError:
                icFolderItem._icon = None
        return icFolderItem._icon
    
    def pointer(self):
        return u''


class icRootItem(icItemCatalog):
    """
    Служебный элемент.
    """
    catalog_type = 'root'
    
# Структура, где регистрируются все элементы каталога
catalog_type_dct = {}


def reg_catalog_type(item_cls):
    """
    Регистрация типов элементов.
    @type item_cls: C{icItemCatalog}
    @param item_cls: Класс элемента каталога.
    """
    global catalog_type_dct
    catalog_type_dct[item_cls.catalog_type] = item_cls

reg_catalog_type(icItemCatalog)
reg_catalog_type(icFolderItem)


class icAbsCatalog(object):
    """
    Абстрактный класс каталога.
    """
    def __init__(self, *arg, **kwarg):
        pass

    def add_item(self, parent_item, name, item):
        """
        Добавление элемента в родительскую папку.
        """
        abstract()
        
    def add(self, path, pobj, *arg, **kwarg):
        """
        Зарегистрировать объект в каталоге.
        """
        abstract()
        
    def remove(self, path):
        """
        Удалить объект из каталога.
        """
        abstract()

    def refresh(self):
        """
        Обновление буфера каталога из хранилища.
        """
        abstract()
        
    def get_pobj(self, path):
        """
        Возвращает указатель на объект.
        """
        abstract()
        
    def get_object(self, path):
        """
        Возвращает объект.
        """
        abstract()

    def get_item(self, path):
        """
        Возвращает элемент каталога.
        """
        abstract()
        
    def __getitem__(self, path):
        return self.get_item(path)
        
    def __iter__(self): 
        abstract()
        
    def keys(self, *arg, **kwarg):
        abstract()

    def items(self, *arg, **kwarg):
        abstract()
        
    def get_items(self):
        abstract()


class icAbsResultSearch(object):
    """
    Абстрактный класс результата поиска.
    """
    pass


class icListResultSearch(icAbsResultSearch, list):
    """
    Результат поиска в виде списка.
    """


def norm(p):
    """
    Функция нормализации путей.
    """
    p = p.replace('\\', '/').replace('//', '/')
    if p.startswith(FLD_DIV):
        p = p[1:]
    if p.endswith(FLD_DIV):
        p = p[:-1]
    return p


def norm_path(func):
    """
    Декоратор для нормализации имен путей.
    """
    def wrap(*arg, **kwarg):
        if len(arg) > 1:
            p = arg[1]
            p = norm(p)
            arg = list(arg)
            arg[1] = p
            arg = tuple(arg)
        return func(*arg, **kwarg)
    return wrap


class icCatalog(icAbsCatalog):
    """
    Каталог объектов. Ключ задает путь объекта в папочной структуре.
    """
    def __init__(self, *arg, **kwarg):
        self._catalog = []
        self.root = icRootItem('', None)
        
    def init_catalog(self):
        """
        """
        pass

    def add_item(self, parent_item, name, item):
        """
        Добавление элемента в родительскую папку.
        @param parent_item: Родительский элемент. Если None, то элемент добавляется
            в корень каталога.
        """
        if parent_item:
            path = norm(parent_item.path+FLD_DIV+name)
        else:
            path = name
            
        keys = self.keys()
        if path in keys:
            raise PathExistException(('Path always exist :%s' % path,))
        elif parent_item.can_contain_item(item):
            item.path = path
            item.catalog = self
            self._catalog.append(item)
            return item
        else:
            CatalogItemTypeException(('Invalid item type',))
                            
    @norm_path    
    def add(self, path, pobj, otype=None, title='', description='', *arg, **kwarg):
        """
        Зарегистрировать объект в каталоге. У каждого объекта должен быть
        родитель.
        @param path: Ключ.
        @param pobj: Указатель на объект, который регистрируется в каталоге.
        @param otype: Тип регистрируемого объекта.
        """
        pp = self.get_parent_path(path)
        if not pp or (pp in self.keys()):
            cls = catalog_type_dct.get(otype or DEFAULT_OTYPE, None)
            if cls:
                item = cls(path, pobj, title, description, **kwarg)
                self.add_item(self.get_item(pp) or self.root, path.split(FLD_DIV)[-1], item)
                return item
            else:
                raise InvalidCatalogItemTypeException(('Unknown catalog type:%s' % otype,))
        else:
            raise NotImplementedError('Must be parent object')
            
    @norm_path
    def get_path_lst(self, path):
        """
        Возвращает список указательей на объекты по заданному пути.
        @param path: Путь в каталоге.
        """
        t = path.split(FLD_DIV)
        lst = []
        for el in self.keys():
            t1 = el.split(FLD_DIV)[:-1]
            b = True
            for i, x in enumerate(t):
                if x and (len(t1) <= i or x <> t1[i]):
                    b = False
                    break
            if b:
                lst.append(el)
                
        return lst
    
    @norm_path        
    def get_child_path_lst(self, path):
        """
        Возвращает список дочерних элементов папки.
        """
        t = path.split(FLD_DIV)
        lst = []
        for el in self.keys():
            t1 = el.split(FLD_DIV)[:-1]
            if t1 == t or (not t1 and not t[0]):
                lst.append(el)
                
        return lst

    def get_child_items(self, item=None, path=None):
        """
        Возвращает список дочерних элементов папки. Если элемент не определен, то
        возвращает дочерние элементы корневого элемента.
        """
        if item:
            path = item.path
        else:
            path = path or ''
            
        t = path.split(FLD_DIV)
        lst = []
        for obj in self._catalog:
            p = obj.path
            t1 = p.split(FLD_DIV)[:-1]
            if t1 == t or (not t1 and not t[0]):
                lst.append(obj)
                
        return lst

    def has_child_items(self, item=None, path=None):
        """
        Возвращает признак наличия дочерних элементов.
        """
        if item:
            path = item.path
        else:
            path = path or ''
            
        t = path.split(FLD_DIV)
        for obj in self._catalog:
            p = obj.path
            t1 = p.split(FLD_DIV)[:-1]
            if t1 == t or (not t1 and not t[0]):
                return True
                
        return False
        
    @norm_path        
    def get_parent_path(self, path=''):
        """
        Возвращает путь до родительского объекта.
        """
        return FLD_DIV.join(path.split(FLD_DIV)[:-1])

    def get_parent_item(self, item):
        """
        Возвращает родительский эдемент.
        @param item: Элемент каталога.
        """
        pp = self.get_parent_path(item.path)
        if pp:
            return self.get_item(pp)
        else:
            return self.root

    @norm_path
    def get_obj_lst(self, path):
        """
        Возвращает список объектов по заданному пути.
        @param path: Путь в каталоге.
        """
        
    @norm_path
    def remove(self, path):
        """
        Удалить объект из каталога.
        """
        item = self.get_item(path)
        if item:
            self._catalog.remove(item)

    def remove_item(self, item):
        """
        Удалить объект из каталога.
        """
        self._catalog.remove(item)

    @norm_path    
    def get_item(self, path):
        """
        Возвращает объект по заданному ключу.
        """
        for el in self._catalog:
            if path == el['path']:
                return el

    def get_items(self):
        """
        Возвращает список элементов каталога.
        """
        return self._catalog

    def __iter__(self): 
        """
        Итератор каталога.
        """
        for el in self._catalog:
            yield el

    @norm_path
    def get_pobj(self, path):
        """
        Возвращает указатель на объекта.
        """
        return self.get_item(path).pobj
        
    @norm_path    
    def get_object(self, path):
        """
        Возвращает объект по заданному ключу.
        """
        pass

    @norm_path    
    def get_object_type(self, path):
        """
        Возвращает тип объекта по заданному ключу.
        """
        return self.get_item(path).otype

    @norm_path    
    def get_tuple(self, path, attr1='otype', attr2='pobj'):
        """
        Возвращает картеж из типа и ссылки объекта.
        """
        item = self.get_item(path)
        return item.catalog_type, item[attr2]
        
    def keys(self, *arg, **kwarg):
        return [el['path'] for el in self._catalog]
    
    def items(self, *arg, **kwarg):
        return [(el['path'], el) for el in self._catalog]
        
    def filter_type(self, otype=None):
        """
        Поиск объектов заданного типа.
        @param otype: Тип объекта.
        """
        otype = otype or DEFAULT_OTYPE
        lst = icListResultSearch()
        for key in self.keys():
            t, p = self.get_tuple(key)
            if t == otype:
                lst.append(p)
        return lst
        
    def get_type_dct(self, tps=None):
        """
        Возвращает словарь: ключи типы объектов, значения списка объектов заданного типа.
        @param tps: Список типов попадающих в словарь. Если None, то отбираются 
            все типы.
        """
        dct = {}
        for key in self.keys():
            t, p = self.get_tuple(key)
            if tps is None or t in tps:
                if t in dct.keys():
                    dct[t].append(p)
                else:
                    dct[t] = icListResultSearch([p])
                
        return dct
        
    def search(self, **kwarg):
        """
        Поиск объектов по набору атрибутов.
        """
        tps = []
        for key, val in self.items():
            tp = val[-1]
            if tp not in tps:
                pass
