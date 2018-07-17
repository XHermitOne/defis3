#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль абстрактного базового класса компонентов организации бизнес процессов.

@type SPC_IC_WORKBASE: C{dictionary}
@var SPC_IC_WORKBASE: Спецификация на ресурсное описание базового компонента автоматизации бизнес-процессов.
Описание ключей SPC_IC_WORKBASE:

    - B{name = 'default'}: Имя.
    - B{type = 'WorkBase'}: Тип объекта.
    - B{description = ''}: Описание.
    - B{init_users = None}: Список пользователей, которые могут инициализировать объект, 
                            если None, то может инициализировать любой пользователь.
    - B{edit_users = None}: Список пользователей, которые могут редактировать объект, 
                            если None, то может редактировать любой пользователь.
    - B{view_users = None}: Список пользователей, которые могут просматривать объект, 
                            если None, то может просматривать любой пользователь.
    - B{print_users = None}: Список пользователей, которые могут печатать объект, 
                             если None, то может печатать любой пользователь.
    - B{del_users = None}: Список пользователей, которые могут удалять объект, 
                           если None, то может удалять любой пользователь.
    - B{send_users = None}: Список пользователей, которые могут перенаправить объект, 
                            если None, то может перенаправлять любой пользователь.
    - B{task = None}: Связанная с объектом задача.
    
"""

# --- Подключение библиотек ---
from ic.log import log
from ic.components import icwidget
from ic.engine import ic_user

from . import persistent
from . import form_generator

# --- Константы ---

# Версия
__version__ = (0, 0, 1, 1)

# --- Спецификация ---
SPC_IC_WORKBASE = dict({'type': 'WorkBase',
                        'name': 'default',
                        'description': '',    # Описание
                        'init_users': None,   # Список пользователей, которые могут инициализировать объект,
                                              # если None, то может инициализировать любой пользователь
                        'edit_users': None,   # Список пользователей, которые могут редактировать объект,
                                              # если None, то может редактировать любой пользователь
                        'view_users': None,   # Список пользователей, которые могут просматривать объект,
                                              # если None, то может просматривать любой пользователь
                        'print_users': None,  # Список пользователей, которые могут печатать объект,
                                              # если None, то может печатать любой пользователь
                        'del_users': None,    # Список пользователей, которые могут удалять объект,
                                              # если None, то может удалять любой пользователь
                        'send_users': None,   # Список пользователей, которые могут перенаправить объект,
                                              # если None, то может перенаправлять любой пользователь
                        'task': None,         # Связанная с объектом задача

                        'init': None,        # Блок кода контроля при инициализации объекта
                        'ctrl': None,        # Блок кода контроля при редактировании объекта
                        'del': None,         # Блок кода контроля при удалении объекта
                        'post_init': None,   # Блок кода контроля после инициализации объекта
                        'post_ctrl': None,   # Блок кода контроля после редавтирования объекта
                        'post_del': None,    # Блок кода контроля после удаления объекта
    
                        '__parent__': icwidget.SPC_IC_SIMPLE,
                        })


class icWorkBase(persistent.icObjPersistent, form_generator.icObjFormGenerator):
    """
    Базовый класс компонентов организации бизнесс-процессов.
        Реализует внутри себя механизм разграничения доступа.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        self._parent = Parent_
        
        persistent.icObjPersistent.__init__(self, Parent_)
        
        form_generator.icObjFormGenerator.__init__(self, Parent_)

    def getParent(self):
        return self._parent
        
    def getInitUsers(self):
        """
        Список пользователей, которые могут инициализировать объект, 
            если None, то может инициализировать любой пользователь.
        """
        return None
        
    def getEditUsers(self):
        """
        Список пользователей, которые могут редактировать объект, 
            если None, то может редактировать любой пользователь.
        """
        return None
        
    def getViewUsers(self):
        """
        Список пользователей, которые могут смотреть объект, 
            если None, то может смотреть любой пользователь.
        """
        return None

    def getPrintUsers(self):
        """
        Список пользователей, которые могут распечатать объект, 
            если None, то может распечатать любой пользователь.
        """
        return None
        
    def getDelUsers(self):
        """
        Список пользователей, которые могут удалить объект, 
            если None, то может удалить любой пользователь.
        """
        return None
        
    def getSendUsers(self):
        """
        Список пользователей, которые могут отослать объект, 
            если None, то может отослать любой пользователь.
        """
        return None
        
    def _canDo(self, User_=None, Permit_=None):
        """
        Можно ли производить что-либо?
        @param User_: Указание пользователя.
            Если None, то береться текущий зарегестрированный пользователь в системе.
        @param Permit_: Список разрешенных пользователей.
            Если None, можно любому пользователю.
        @return: True/False.
        """
        try:
            # Если None, можно любому пользователю.
            if Permit_ is None:
                return True
            if User_ is None:
                # Определение текущего пользователя
                User_ = ic_user.getCurUserName()
            
            return bool(User_ in list(Permit_))
        except:
            log.fatal(u'ОШИБКА определения прав пользователя <%s> системы бизнес-процессов' % User_)
            return False
        
    def canUserInit(self, User_=None):
        """
        Может ли пользователь проинициализировать объект?
        @param User_: Указание пользователя.
            Если None, то береться текущий зарегестрированный пользователь в системе.
        """
        return self._canDo(User_, self.getInitUsers())
        
    def canUserEdit(self, User_=None):
        """
        Может ли пользователь редактировать объект?
        @param User_: Указание пользователя.
            Если None, то береться текущий зарегестрированный пользователь в системе.
        """
        return self._canDo(User_, self.getEditUsers())
    
    def canUserView(self, User_=None):
        """
        Может ли пользователь редактировать объект?
        @param User_: Указание пользователя.
            Если None, то береться текущий зарегестрированный пользователь в системе.
        """
        return self._canDo(User_, self.getViewUsers())
    
    def canUserPrint(self, User_=None):
        """
        Может ли пользователь распечатать объект?
        @param User_: Указание пользователя.
            Если None, то береться текущий зарегестрированный пользователь в системе.
        """
        return self._canDo(User_, self.getPrintUsers())

    def canUserDel(self, User_=None):
        """
        Может ли пользователь удалить объект?
        @param User_: Указание пользователя.
            Если None, то береться текущий зарегестрированный пользователь в системе.
        """
        return self._canDo(User_, self.getDelUsers())

    def canUserSend(self, User_=None):
        """
        Может ли пользователь отослать объект?
        @param User_: Указание пользователя.
            Если None, то береться текущий зарегестрированный пользователь в системе.
        """
        return self._canDo(User_, self.getSendUsers())

    def doTask(self, Task_=None):
        """
        Выполнить задачу.
        @param Task_: Имя задачи для выполнение, если None, 
            то буруться имя из ресурса.
        """
        pass
        
    def get(self):
        """
        Получить значение объекта.
        """
        return None
        
    def set(self, Value_=None):
        """
        Установить значение объекта.
        @param Value_: Значение.
        """
        pass

    def control(self, CtrlObj_, CtrlCode_=None):
        """
        Контроль при добавлении/редактировании объекта.
        @param CtrlObj_: Контролируемый объект.
        @param CtrlCode_: Блок кода контроля.
        @return: Возвращает код ошибки контроля. Или 0, если все нормально.
        """
        return 0

    def GetInitForm(self):
        """
        Форма/Визард для создания/инициализации.
        """
        return None
        
    def GetEditForm(self):
        """
        Форма для редактирования.
        """
        return None
        
    def GetViewForm(self):
        """
        Форма для просмотра.
        """
        return None
        
    def GetChoiceForm(self):
        """
        Форма выбора.
        """
        return None
        
    def GetBrowseForm(self):
        """
        Форма браузера.
        """
        return None
        
    def GetReport(self):
        """
        Отчет для распечатки.
        """
        return None

    def SendTo(self, To_=None, evalSpace=None):
        """
        Отправка.
        @param To_: Указание адресата.
        @param evalSpace_: Пространство имен.
        """
        pass
        
    def Del(self, evalSpace=None):
        """
        Удаление.
        @param evalSpace_: Пространство имен.
        """
        pass


class icRequisiteBase(persistent.icAttrPersistent, form_generator.icAttrFormGenerator):
    """
    Базовый класс всех реквизитов.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        self._parent = Parent_
        
        persistent.icAttrPersistent.__init__(self, Parent_)
        
        form_generator.icAttrFormGenerator.__init__(self, Parent_)

        # Значение/Данные реквизита
        self._value = None
        
    def isDataRequisite(self):
        """
        Это реквизит хранения данных?
        У реквизитов хранения ссылки, например справочников 
        эта функция возвращает False.
        """
        return True
    
    def getFieldNames(self):
        """
        Имена полей реквизита.
        """
        log.warning(u'Не определен метод <getFieldNames>')
        
    def getData(self):
        """
        Текущее значение объекта.
        """
        return self._value

    def getStrData(self):
        """
        Строковое представление текущего значения объекта.
        """
        return str(self._value) if self._value is not None else ''

    def setData(self, Data_):
        """
        Установить текущее значение объекта.
        """
        self._value = Data_
    
    getValue = getData
    setValue = setData
    get = getData
    set = setData
        
    def init_data(self, Value_=None):
        """
        Инициализировать значение объекта.
        @param Value_: Значение.
        """
        if Value_ is None:
            Value_ = self.getDefault()
        self._value = Value_
        
    def getDefault(self):
        """
        Значение по умолчанию.
        """
        return None
        
    def setMyData(self, Rec_):
        """
        Установить мои данные из строки.
        @param Rec_: Строка в виде словаря.
        """
        log.warning(u'Не определен метод <setMyData>')

    def createLabelCtrl(self, Parent_=None):
        """
        Создание объекта контрола надписи реквизита.
        @param Parent_: Родительское окно.
        """
        return None
    
    def createEditorCtrl(self, Parent_=None):
        """
        Создание объекта контрола редактора реквизита.
        @param Parent_: Родительское окно.
        """
        return None


class icTabRequisiteBase(persistent.icObjPersistent,
                         form_generator.icGridFormGenerator):
    """
    Базовый класс всех табличных реквизитов.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        self._parent = Parent_
        
        persistent.icObjPersistent.__init__(self, Parent_)
        
        form_generator.icGridFormGenerator.__init__(self, Parent_)

        # Значение/Данные реквизита
        # ВНИМАНИЕ! Значение табличного реквизита д.б. всегда список
        # иначе будет возникать ошибка при записи БИЗНЕС ОБЪЕКТА
        self._value = list()

        # Дополнительные буферы обработки табличного реквизита
        # self._del_buffer = list()
        # self._add_buffer = list()
        # self._update_buffer = list()

    def getParent(self):
        return self._parent

    def isDataRequisite(self):
        """
        Это реквизит хранения данных?
        У реквизитов хранения ссылки, например справочников 
        эта функция возвращает False.
        """
        return True
    
    def getFieldNames(self):
        """
        Имена полей реквизита.
        """
        pass
        
    def getData(self):
        """
        Текущее значение объекта.
        """
        # ВНИМАНИЕ! Значение табличного реквизита д.б. всегда список
        # иначе будет возникать ошибка при записи БИЗНЕС ОБЪЕКТА
        if self._value is None:
            self._value = list()
        return self._value

    def setData(self, Data_):
        """
        Установить текущее значение объекта.
        """
        self._value = Data_
        # ВНИМАНИЕ! Значение табличного реквизита д.б. всегда список
        # иначе будет возникать ошибка при записи БИЗНЕС ОБЪЕКТА
        if self._value is None:
            self._value = list()

    getValue = getData
    setValue = setData
    get = getData
    set = setData

    def clearRows(self):
        """
        Удалить все строки из табличного реквизита.
        @return: True/False.
        """
        self._value = list()
        return True

    def addRow(self, **requisite_values):
        """
        Добавить строку в табличный реквизит.
        @param requisite_values: Данные реквизитов.
        @return: True/False.
        """
        row_requisites = dict()

        for requisite in self.getChildrenRequisites():
            row_requisites[requisite.name] = requisite_values.get(requisite.name, requisite.getDefault())

        # ВНИМАНИЕ! Значение табличного реквизита д.б. всегда список
        # иначе будет возникать ошибка при записи БИЗНЕС ОБЪЕКТА
        if self._value is None:
            self._value = list()
        self._value.append(row_requisites)
        return True

    def init_data(self, Value_=None):
        """
        Инициализировать значение объекта.
        @param Value_: Значение.
        """
        if Value_ is None:
            Value_ = self.getDefault()
        self._value = Value_
        # ВНИМАНИЕ! Значение табличного реквизита д.б. всегда список
        # иначе будет возникать ошибка при записи БИЗНЕС ОБЪЕКТА
        if self._value is None:
            self._value = list()

    def getDefault(self):
        """
        Значение по умолчанию.
        ВНИМАНИЕ! Значение табличного реквизита д.б. всегда список
        иначе будет возникать ошибка при записи БИЗНЕС ОБЪЕКТА
        """
        return list()
        
    def setMyData(self, Rec_):
        """
        Установить мои данные из строки.
        @param Rec_: Строка в виде словаря.
        """
        pass

    def createLabelCtrl(self, Parent_=None):
        """
        Создание объекта контрола надписи реквизита.
        @param Parent_: Родительское окно.
        """
        return None
    
    def createEditorCtrl(self, Parent_=None):
        """
        Создание объекта контрола редактора реквизита.
        @param Parent_: Родительское окно.
        """
        return None
