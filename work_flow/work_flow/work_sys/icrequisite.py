#!/usr/bin/env python"""
#  -*- coding: utf-8 -*-

"""
Реквизит. 
Реквизит определяет атрибут объекта, указывает его тип, 
описывает поля редактирования/просмотра этого атрибута, 
поле хранения атрибута и т.п.

@type SPC_IC_REQUISITE: C{dictionary}
@var SPC_IC_REQUISITE: Спецификация на ресурсное описание реквизита.
Описание ключей SPC_IC_REQUISITE:

    - B{name = 'default'}: Имя.
    - B{type = 'Requisite'}: Тип объекта.
    - B{description = ''}: Описание.
    - B{field = None}: Поле таблицы родительского компонента, в котором храниться значение реквизита.
    - B{len = None}: Длина поля таблицы.
    - B{type_val = 'T'}: Тип поля таблицы. R - связь со справочником.
    - B{default = None}: Значение по умолчанию.
    - B{set_value = None}: Функционал, исполняемый при установке значения реквизита.
    - B{get_value = None}: Функционал, исполняемый при получениии значения реквизита.

@type SPC_IC_NSI_REQUISITE: C{dictionary}
@var SPC_IC_NSI_REQUISITE: Спецификация на ресурсное описание реквизита-связи со справочником.
Описание ключей SPC_IC_NSI_REQUISITE:

    - B{name = 'default'}: Имя.
    - B{type = 'NSIRequisite'}: Тип объекта.
    - B{description = ''}: Описание.
    - B{fields = None}: Соответствие полей таблицы и справочника, в котором храниться значения реквизита (словарь).
    - B{defaults = None}: Значения по умолчанию (словарь).
    - B{set_value = None}: Функционал, исполняемый при установке значения реквизита.
    - B{get_value = None}: Функционал, исполняемый при получениии значения реквизита.
    - B{nsi_res = None}: Ресурс справочника. Если None, то 'nsi_sprav'.
    - B{nsi_type = None}: Справочник.
    - B{auto_set = True}: Признак автоматического заполнения полей при редактировании.

@type SPC_IC_DOC_REQUISITE: C{dictionary}
@var SPC_IC_DOC_REQUISITE: Спецификация на ресурсное описание реквизита-связи с документом.
Описание ключей SPC_IC_DOC_REQUISITE:

    - B{name = 'default'}: Имя.
    - B{type = 'DOCRequisite'}: Тип объекта.
    - B{description = ''}: Описание.
    - B{fields = None}: Соответствие полей таблицы и документа, в котором храниться значения реквизита (словарь).
    - B{defaults = None}: Значения по умолчанию (словарь).
    - B{set_value = None}: Функционал, исполняемый при установке значения реквизита.
    - B{get_value = None}: Функционал, исполняемый при получениии значения реквизита.
    - B{document = None}: Паспорт документа.
    - B{auto_set = True}: Признак автоматического заполнения полей при редактировании.
"""

# --- Подключение библиотек ---
import ic

from ic.utils import util
from ic.utils import resource
from ic.utils import ic_file
from ic.utils import ic_util
from ic.log import log

import work_flow.work_sys.icworkbase as icworkbase
from work_flow.work_sys import persistent
from work_flow.work_sys import form_generator
from STD.queries import filter_builder_env

from ic.components.user import ic_field_wrp

# Версия
__version__ = (0, 0, 1, 3)

# --- Specifications ---
SPC_IC_REQUISITE = dict({'type': 'Requisite',
                         'name': 'default',
                         'description': '',    # Описание
    
                         # --- Свойства генерации поля хранения ---
                         'type_val': 'T',  # Тип значения реквизита
                         'len': None,      # Длина значения реквизита
                         'field': None,    # Поле таблицы родительского компонента,
                                           # в котором храниться значение реквизита
                         'default': None,  # Значение по умолчанию
    
                         'set_value': None,  # Функционал, исполняемый при установке значения реквизита
                         'get_value': None,  # Функционал, исполняемый при получениии значения реквизита

                         # --- Свойства генерации контролов редактирования/просмотра ---
                         'grp_title': u'',  # Реквизиты могут группироваться по страницам
                                            # Страницы различаются только по русским заголовкам.
                                            # Если заголовок страницы не определен, то
                                            # считается что реквизит располагается на главной
                                            # странице 'Основные'
                        
                         'label': u'',  # Надпись реквизита
                                        # Если надпись пустая, то берется вместо надписи описание (description)
    
                         'is_init': True,    # Реквизит является инициализируемым пользователем
                         'is_view': True,    # Реквизит можно просматривать на форме просмотра
                         'is_edit': True,    # Реквизит можно редактировать на форме редактировать
                         'is_search': True,  # Реквизит можно задавать в качестве критерия поиска объекта
    
                         'id_attr': False,   # Реквизит является идентифицирующим объект каким-то либо образом
                                             # Реквизит, у которого True будет добавляться в
                                             # гриды объектов  в виде колонки
                         'is_description': False,  # Реквизит является описательным
    
                         '__parent__': icworkbase.SPC_IC_WORKBASE,
                         })
    
# Группы регистра
SPC_IC_REG_GROUP = dict({'type': 'RegGroup',
                         'name': 'default',
                         'description': '',    # Описание

                         'type_val': 'T',  # Тип значения группы регистра
                         'len': None,      # Длина значения группы регистра
                         'field': None,    # Поле таблицы родительского компонента,
                                           # в котором храниться значение группы регистра
                         'default': None,  # Значение по умолчанию
    
                         'set_value': None,  # Функционал, исполняемый при установке значения группы регистра
                         'get_value': None,  # Функционал, исполняемый при получениии значения группы регистра
    
                         '__parent__': icworkbase.SPC_IC_WORKBASE,
                         })
    
# Агрегатные функции, используемы при расчете итогов
AGGREGATE_FUNCTIONS = ['INCR', 'SUM', 'COUNT', 'MIN', 'MAX']

# Итоги регистра
SPC_IC_REG_SUM = dict({'type': 'RegSum',
                       'name': 'default',
                       'description': '',    # Описание
    
                       'type_val': 'F',  # Тип значения итогов регистра
                       'len': None,      # Длина значения итогов регистра
                       'field': None,    # Поле таблицы родительского компонента,
                                         # в котором храниться значение итогов регистра
                       'default': None,  # Значение по умолчанию
    
                       'set_value': None,  # Функционал, исполняемый при установке значения итогов регистра
                       'get_value': None,  # Функционал, исполняемый при получениии значения итогов регистра
    
                       'aggregate_func': 'INCR',  # Указание агрегатной функции при расчете итога
    
                       '__parent__': icworkbase.SPC_IC_WORKBASE,
                       })
    
SPC_IC_NSI_REQUISITE = dict({'type': 'NSIRequisite',
                             'name': 'default',
                             'description': '',    # Описание
    
                             # --- Свойства генерации контролов редактирования/просмотра ---
                             'grp_title': u'',  # Реквизиты могут группироваться по страницам
                                                # Страницы различаются только по русским заголовкам.
                                                # Если заголовок страницы не определен, то
                                                # считается что реквизит располагается на главной
                                                # странице 'Основные'
                        
                             'label': u'',  # Надпись реквизита
                                            # Если надпись пустая, то берется вместо надписи описание (description)
    
                             'is_init': True,    # Реквизит является инициализируемым пользователем
                             'is_view': True,    # Реквизит можно просматривать на форме просмотра
                             'is_edit': True,    # Реквизит можно редактировать на форме редактировать
                             'is_search': True,  # Реквизит можно задавать в качестве критерия поиска объекта
    
                             'id_attr': False,  # Реквизит является идентифицирующим объект каким-то либо образом
                                                # Реквизит, у которого True будет добавляться в
                                                # гриды объектов  в виде колонки
                             'is_description': False,   # Реквизит является описательным

                             # --- Свойства генерации полей хранения ---
                             'fields': None,    # Соответствие полей таблицы и справочника,
                                                # в котором храниться значения реквизита (словарь)
                             'defaults': None,  # Значения по умолчанию (словарь)
                             'field': None,     # Поле кода справочника
    
                             'set_value': None,  # Функционал, исполняемый при установке значения реквизита
                             'get_value': None,  # Функционал, исполняемый при получениии значения реквизита
    
                             # --- Ссылка на объект справочника ---
                             'nsi_psp': None,   # Справочник NSI
                             'auto_set': True,  # Признак автоматического заполнения полей при редактировании
    
                             '__parent__': icworkbase.SPC_IC_WORKBASE,
                             })

DEFAULT_CTRL_WIDTH = 100
DEFAULT_DATE_WIDTH = 90
DEFAULT_TEXT_WIDTH = 200
DEFAULT_INT_WIDTH = 50
DEFAULT_FLOAT_WIDTH = 50


class icRequisitePrototype(icworkbase.icRequisiteBase):
    """
    Реквизит.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        icworkbase.icRequisiteBase.__init__(self, Parent_)
        
        # Имя реквизита
        self.name = None

        # Имя поля
        self.field = None
        # Описание
        self.description = ''
        # Тип поля
        self.type_val = 'T'
        # Длина поля
        self.len = None

    def getTypeValue(self):
        """
        Тип поля хранения реквизита.
        """
        return self.type_val

    def setMyData(self, Rec_):
        """
        Установить мои данные из строки.
        @param Rec_: Строка в виде словаря.
        """
        if self.field in Rec_:
            self.setData(Rec_[self.field])

    def getFieldNames(self):
        """
        Имена полей реквизита.
        """
        return [self.getFieldName()]

    def isInit(self):
        """
        Реквизит является инициализируемым пользователем?
        """
        return True

    def isEdit(self):
        """
        Реквизит является редактируемым пользователем?
        """
        return True

    def isView(self):
        """
        Реквизит является просматриваемым пользователем?
        """
        return True
    
    def isSearch(self):
        """
        Реквизит можно задавать в качестве критерия поиска объекта?
        """
        return True

    def isDescription(self):
        """
        Реквизит является описывающим объект?
        """
        return False

    def getLabel(self):
        """
        Надпись реквизита.
        """
        return u''

    def isIDAttr(self):
        """
        Реквизит является идентифицирующим объект?
        """
        return False
    
    def getGroupTitle(self):
        """
        Надпись группы, в которую входит реквизит.
        """
        return u''

    def _getEditType(self):
        """
        Определить тип редактора реквизита.
        Тип редактора в случае реквизита определяется по типу хранимого 
        значения.
        """
        if self.type_val == 'T':
            # Текст
            return form_generator.TEXT_EDIT_TYPE
        elif self.type_val == 'D':
            # Дата
            return form_generator.DATE_EDIT_TYPE
        elif self.type_val == 'I':
            # Целое
            return form_generator.INT_EDIT_TYPE
        elif self.type_val == 'F':
            # Число с плавающей запятой
            return form_generator.FLOAT_EDIT_TYPE
        else:
            ic.io_prnt.outLog(u'Не определен тип хранения \'%s\' реквизита <%s>' % (self.type_val, self.name))
            
        return form_generator.DEFAULT_EDIT_TYPE        
    
    def _getDefaultWidth(self):
        """
        Ширина контрола для редктирования этого реквизита по умолчанию.
        Это значение нужно в основном для вычисления ширины редакторов и
        ширин колонок грида.
        """
        if self.type_val == 'T':
            if self.len and isinstance(len, int):
                return self.len*10
            return DEFAULT_TEXT_WIDTH
        elif self.type_val == 'D':
            return DEFAULT_DATE_WIDTH
        elif self.type_val == 'I':
            return DEFAULT_INT_WIDTH
        elif self.type_val == 'F':
            return DEFAULT_FLOAT_WIDTH
        else:
            ic.io_prnt.outLog(u'Не определен тип хранения \'%s\' реквизита <%s>' % (self.type_val, self.name))
        return DEFAULT_CTRL_WIDTH
    
    def createLabelCtrl(self, Parent_=None):
        """
        Создание объекта контрола надписи реквизита.
        """
        spc=self._genStdLabelRes()
        return self.GetKernel().createObjBySpc(Parent_, spc)
        
    def createEditorCtrl(self, Parent_=None):
        """
        Создание объекта контрола редактора реквизита.
        @param Parent_: Родительское окно.
        """
        if self.type_val == 'T':
            spc = self._genTxtEditorRes(self.name+'_edit')
            return self.GetKernel().createObjBySpc(Parent_, spc)
        elif self.type_val == 'D':
            spc = self._genDateEditorRes(self.name+'_edit')
            return self.GetKernel().createObjBySpc(Parent_, spc)
        elif self.type_val == 'I':
            spc = self._genIntEditorRes(self.name+'_edit')
            return self.GetKernel().createObjBySpc(Parent_, spc)
        elif self.type_val == 'F':
            spc = self._genFloatEditorRes(self.name+'_edit')
            return self.GetKernel().createObjBySpc(Parent_, spc)
        else:
            ic.io_prnt.outLog(u'Не определен тип хранения \'%s\' реквизита <%s>' % (self.type_val, self.name))
        return None


class icRegGroupPrototype(icworkbase.icRequisiteBase):
    """
    Группа регистра.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        icworkbase.icRequisiteBase.__init__(self, Parent_)
        
        # Имя
        self.name = None

        # Имя поля
        self.field = None
        # Описание
        self.description = ''
        # Тип поля
        self.type_val = 'T'
        # Длина поля
        self.len = None

    def getFieldNames(self):
        """
        Имена полей списком.
        """
        return [self.getFieldName()]


class icRegSumPrototype(icworkbase.icRequisiteBase):
    """
    Итоги регистра.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        icworkbase.icRequisiteBase.__init__(self, Parent_)
        
        # Имя
        self.name = None

        # Имя поля
        self.field = None
        # Описание
        self.description = ''
        # Тип поля
        self.type_val = 'T'
        # Длина поля
        self.len = None
        
        # Агрегатная функция, испоьлзуемая при расчете итогов
        self._aggregate_func = None

    def getFieldNames(self):
        """
        Имена полей списком.
        """
        return [self.getFieldName()]

    def getAggregateFunc(self):
        """
        Агрегатная функция используемая при расчете итогов.
        """
        return self._aggregate_func


class icNSIRequisitePrototype(icworkbase.icRequisiteBase):
    """
    Реквизит связи со справочником системы NSI.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        icworkbase.icRequisiteBase.__init__(self, Parent_)
        
        # Текущее значение реквизита - код справочника
        self.value = None
        
        # Объект справочника
        self.sprav = None

    def getSprav(self):
        """
        Объект справочника.
        """
        return self.sprav
    
    def getFilterFuncs(self):
        """
        Список функций фильтрации.
        """
        funcs = filter_builder_env.DEFAULT_FUNCS.get(filter_builder_env.REQUISITE_TYPE_NSI)
        
        # Поменять привязку к справочнику в расширенном редакторе
        for func_body in filter_builder_env.DEFAULT_ENV_NSI_FUNCS.values():
            func_body['args'][0]['ext_kwargs']['component'] = {'sprav': self.getNSIPsp()}
            
        return funcs
    
    def isDataRequisite(self):
        """
        Это реквизит хранения данных?
        У реквизитов хранения ссылки, например справочников 
        эта функция возвращает False.
        """
        return False

    def getTypeValue(self):
        """
        Тип поля хранения реквизита.
        """
        return form_generator.NSI_EDIT_TYPE

    def getNSIRes(self):
        """
        Имя ресурсного файла справочника.
        """
        nsi_psp = self.getNSIPsp()
        if nsi_psp:
            return nsi_psp[0][3]
        return None
        
    def getNSIType(self):
        """
        Имя справочника.
        """
        nsi_psp = self.getNSIPsp()
        if nsi_psp:
            return nsi_psp[0][1]
        return None

    def getFields(self):
        """
        Имена полей реквизита таблицы.
        """
        return None
        
    def getField(self):
        """
        Имя поля реквизита таблицы.
        """
        return None
    
    def getDefaults(self):
        """
        Значения по умолчанию.
        """
        return None
        
    def getDefault(self):
        """
        Значения по умолчанию.
        """
        return self.getDefaults()
        
    def _getNSIFieldsSpc(self, NSIRes_, NSIType_, FieldNames_):
        """
        Взять спецификацию поля справочника.
        @param NSIRes_: Имя ресурсного файла справочника.
        @param NSIType_: Тип справочника.
        @param FieldNames_: Список имен полей справочника.
        """
        if NSIRes_ is None:
            nsi_res_name = 'nsi_sprav'
            nsi_res_ext = 'mtd'
        else:
            nsi_res = ic_file.SplitExt(ic_file.BaseName(NSIRes_))
            nsi_res_name = nsi_res[0]
            nsi_res_ext = nsi_res[1][1:]  # И стереть первую точку
            
        # Получить ресурсное описание справочника
        nsi_sprav_manager_res = resource.icGetRes(nsi_res_name,
                                                  nsi_res_ext, nameRes=nsi_res_name)
        if nsi_sprav_manager_res['name'] == NSIType_:
            # Справочник определен просто в ресурсе
            nsi_sprav_res = [nsi_sprav_manager_res]
        else:
            # Справочник определен в менеджере справочников
            nsi_sprav_res = [sprav for sprav in nsi_sprav_manager_res['child'] if sprav['name'] == NSIType_]
        if not nsi_sprav_res:
            ic.io_prnt.outWarning(u'Не найден справочник <%s> в ресурсе [%s]' % (NSIType_, NSIRes_))
            return None
        nsi_sprav_res = nsi_sprav_res[0]
        # Получить ресурсное описание полей
        nsi_tab_psp = nsi_sprav_res['table']
        if nsi_tab_psp:
            nsi_tab_name = nsi_tab_psp[0][1]
        else:
            nsi_tab_name = 'nsi_data'
        nsi_tab_spc = resource.icGetRes(nsi_tab_name, 'tab', nameRes=nsi_tab_name)
        nsi_fields_spc = [util.DeepCopy(field_spc) for field_spc in [fld for fld in nsi_tab_spc['child'] if fld['name'] in FieldNames_]]
        return nsi_fields_spc
        
    def _createFieldsSpc(self):
        """
        Создать спецификацию полей реквизита связи со справочником.
        """
        field_names = self.getFields().values()
        fields_spc = self._getNSIFieldsSpc(self.getNSIRes(),
                                           self.getNSIType(), field_names)
        if fields_spc is None:
            # Произошла какаято ошибка при определении спецификации поля
            log.warning(u'Ошибка генерации спецификации поля таблицы реквизита справочника <%s>' % self.name)
            log.warning(u'ВНИМАНИЕ! Проверьте заполнение атрибута <nsi_psp> реквизита справочника <%s>' % self.name)
            return None
        elif not fields_spc:
            log.warning(u'Не определены спецификации поля таблицы реквизита справочника <%s>' % self.name)

        # Поменять имена полей в спецификациях
        field_names_convert = dict([(fld[1], fld[0]) for fld in self.getFields().items()])
        for i, field_spc in enumerate(fields_spc):
            field_spc['name'] = field_names_convert[field_spc['name']]
            fields_spc[i] = field_spc
        
        return fields_spc

    def init_data(self):
        """
        Инициализация объекта.
        """
        # Устаонвить значение по умолчанию
        self.value = util.DeepCopy(self.getDefaults())

    def getData(self):
        """
        Текущее значение объекта.
        """
        code = self.getCode()
        if self.value is None and code:
            # Если значение не определено а код определен
            # то инициализировать значение справочника
            sprav = self.getSprav()
            if sprav:
                self.value = sprav.getRec(code)
        return self.value

    def getCode(self):
        """
        Текущий код.
        """
        return self._value

    getValue = getCode

    def getStrData(self):
        """
        Строковое представление текущего значения объекта.
        ВНИМАНИЕ! у реквизита справочника строковое представление -
        это поле name.
        """
        sprav = self.getSprav()
        if sprav:
            name = sprav.Find(self._value)
            if name is None:
                name = ''
            elif type(name) not in (str, unicode):
                name = str(name)
            return name
        return str(self._value) if self._value is not None else ''

    def setData(self, Data_):
        """
        Установить текущее значение объекта.
        @param Data_: Данные справочника в виде словаря в формате 'defaults'.
        """
        if self.value is None:
            self.value = dict()
        self.value.update(Data_)

    def _getRequisiteData(self, ParentID_=None):
        """
        Текущее значение объекта.
        """
        return self.value

    def _getEditType(self):
        """
        Определить тип редактора реквизита.
        Тип редактора в случае реквизита определяется по типу хранимого 
        значения.
        """
        return form_generator.NSI_EDIT_TYPE        

    def setMyData(self, Rec_):
        """
        Установить мои данные из строки.
        @param Rec_: Строка в виде словаря.
        """
        for field_name in self.getFields().keys():
            if Rec_ is not None:
                if field_name in Rec_:
                    self.setData({field_name: Rec_[field_name]})
            else:
                log.warning(u'Не определен словарь записи в функции setMyData класса <%s>' % self.__class__.__name__)

    def getFieldNames(self):
        """
        Имена полей реквизита.
        """
        return self.getFields().keys()

    def _getDefaultWidth(self):
        """
        Ширина контрола для редктирования этого реквизита по умолчанию.
        Это значение нужно в основном для вычисления ширины редакторов и
        ширин колонок грида.
        """
        return 300
    
    def createLabelCtrl(self, Parent_=None):
        """
        Создание объекта контрола надписи реквизита.
        """
        spc = self._genStdLabelRes()
        return self.GetKernel().createObjBySpc(Parent_, spc)
        
    def createEditorCtrl(self, Parent_=None):
        """
        Создание объекта контрола редактора реквизита.
        @param Parent_: Родительское окно.
        """
        spc = self._genNSIEditorRes(self.name+'_edit')
        return self.GetKernel().createObjBySpc(Parent_, spc)

    def setSprav(self, sprav):
        """
        Установить справочник.
        @param sprav: Объект справочника.
            Можно также задавать паспортом.
        @return:
        """
        if ic_util.is_pasport(sprav):
            self.setSpravByPsp(sprav)
        else:
            self.sprav = sprav

    def setSpravByPsp(self, nsi_psp):
        """
        Установить справочник по его паспорту.
        @param nsi_psp: Паспорт справочника.
        @return: Объект созданного справочника.
        """
        sprav = self.GetKernel().Create(nsi_psp)
        self.setSprav(sprav)
        return self.sprav
