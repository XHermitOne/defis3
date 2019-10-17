#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Реквизит - ссылка на объект/документ.
Реквизит определяет ссылку на другой бизнес объект.

@type SPC_IC_REF_REQUISITE: C{dictionary}
@var SPC_IC_REF_REQUISITE: Спецификация на ресурсное описание реквизита-ссылки на объект.
Описание ключей SPC_IC_REF_REQUISITE:

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
"""

# --- Подключение библиотек ---
import os
import os.path
from ic.log import log
from ic.utils import util
from ic.utils import strfunc
from ic.utils import resource
from ic.utils import toolfunc
from . import icworkbase
from . import form_generator
from ic.components.user import ic_field_wrp

# Версия
__version__ = (0, 1, 1, 2)

# --- Specifications ---
SPC_IC_OBJ_REQUISITE = {'type': 'OBJRequisite',
                        'name': 'default',
                        'description': '',  # Описание

                        # --- Свойства генерации контролов редактирования/просмотра ---
                        'grp_title': u'',  # Реквизиты могут группироваться по страницам
                                           # Страницы различаются только по русским заголовкам.
                                           # Если заголовок страницы не определен, то
                                           # считается что реквизит располагается на главной
                                           # странице 'Основные'

                        'label': u'',  # Надпись реквизита
                                       # Если надпись пустая, то берется вместо надписи описание (description)

                        'is_init': True,  # Реквизит является инициализируемым пользователем
                        'is_view': True,  # Реквизит можно просматривать на форме просмотра
                        'is_edit': True,  # Реквизит можно редактировать на форме редактировать
                        'is_search': True,  # Реквизит можно задавать в качестве критерия поиска объекта

                        'id_attr': False,  # Реквизит является идентифицирующим объект каким-то либо образом
                                           # Реквизит, у которого True будет добавляться в
                                           # гриды объектов  в виде колонки
                        'is_description': False,  # Реквизит является описательным

                        # --- Свойства генерации полей хранения ---
                        'fields': None,  # Соответствие полей таблицы и объекта,
                                         # в котором храниться значения реквизита (словарь)
                        'defaults': None,  # Значения по умолчанию (словарь)
                        'field': None,  # Поле UUID

                        'set_value': None,  # Функционал, исполняемый при установке значения реквизита
                        'get_value': None,  # Функционал, исполняемый при получениии значения реквизита

                        # --- Ссылка на объект справочника ---
                        'obj_psp': None,   # Бизнес объект/документ
                        'auto_set': True,  # Признак автоматического заполнения полей при редактировании

                        '__parent__': icworkbase.SPC_IC_WORKBASE,
                        '__attr_hlp__': {'grp_title': u'Реквизиты могут группироваться по страницам',
                                         'label': u'Надпись реквизита',

                                         'is_init': u'Реквизит является инициализируемым пользователем',
                                         'is_view': u'Реквизит можно просматривать на форме просмотра',
                                         'is_edit': u'Реквизит можно редактировать на форме редактировать',
                                         'is_search': u'Реквизит можно задавать в качестве критерия поиска объекта',

                                         'id_attr': u'Реквизит является идентифицирующим объект каким-то либо образом',
                                         'is_description': u'Реквизит является описательным',

                                         'fields': u'Соответствие полей таблицы и объекта, в котором храниться значения реквизита (словарь)',
                                         'defaults': u'Значения по умолчанию (словарь)',
                                         'field': u'Поле UUID',

                                         'set_value': u'Функционал, исполняемый при установке значения реквизита',
                                         'get_value': u'Функционал, исполняемый при получениии значения реквизита',

                                         'obj_psp': u'Бизнес объект/документ',
                                         'auto_set': u'Признак автоматического заполнения полей при редактировании',
                                         },
                        }


class icOBJRequisiteProto(icworkbase.icRequisiteBase):
    """
    Реквизит-ссылка на бизнес объект/документ.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        """
        icworkbase.icRequisiteBase.__init__(self, parent)
        
        # Текущее значение реквизита ссылка uuid
        self.value = None

        # Объект, на который ссылается реквизит
        self.ref_obj = None

    def getRefObj(self):
        """
        Объект, на который ссылается реквизит.
        """
        return self.ref_obj
    
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
        return form_generator.REF_EDIT_TYPE

    def getRefObjRes(self):
        """
        Имя ресурсного файла объекта.
        """
        obj_psp = self.getRefObjPsp()
        if obj_psp:
            return obj_psp[0][3]
        return None

    def getRefObjName(self):
        """
        Имя объекта.
        """
        obj_psp = self.getRefObjPsp()
        if obj_psp:
            return obj_psp[0][1]
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

    def _getOBJFieldsSpc(self, ref_obj_resource, ref_obj_name, field_names):
        """
        Взять спецификацию поля связи с бизнес объектом/документом.
        @param ref_obj_resource: Имя ресурсного файла связи с бизнес объектом/документом.
        @param ref_obj_name: Имя бизнес объекта/документа.
        @param field_names: Список имен полей.
        """
        if ref_obj_resource is None:
            log.warning(u'Не определено имя ресурсного файла связи с бизнес объектом/документом.')
            return None

        obj_res = os.path.splitext(os.path.basename(ref_obj_resource))
        obj_res_name = obj_res[0]
        obj_res_ext = obj_res[1][1:]  # И стереть первую точку

        # Получить ресурсное описание
        obj_res = resource.icGetRes(obj_res_name, obj_res_ext, nameRes=obj_res_name)

        if not obj_res:
            log.warning(u'Не найден ресурс <%s>' % ref_obj_name)
            return None

        # Получить ресурсное описание полей
        obj_tab_name = str(obj_res['name']).lower() + '_tab'
        obj_tab_spc = resource.icGetRes(obj_tab_name, 'tab', nameRes=obj_tab_name)

        obj_fields_spc = [util.DeepCopy(field_spc) for field_spc in [fld for fld in obj_tab_spc['child'] if fld['name'] in field_names]]
        return obj_fields_spc

    def _createFieldsSpc(self):
        """
        Создать спецификацию полей реквизита связи с бизнес объектом/документом.
        """
        field_names = self.getFields().values()
        fields_spc = self._getOBJFieldsSpc(self.getRefObjRes(),
                                           self.getRefObjName(), field_names)
        if fields_spc is None:
            # Произошла какаято ошибка при определении спецификации поля
            log.warning(u'Ошибка генерации спецификации поля таблицы реквизита связи с бизнес объектом/документом <%s>' % self.name)
            return None
        elif not fields_spc:
            log.warning(u'Не определены спецификации поля таблицы реквизита связи с бизнес объектом/документом <%s>' % self.name)

        # Поменять имена полей в спецификациях
        field_names_convert = dict([(fld[1], fld[0]) for fld in self.getFields().items()])
        for i, field_spc in enumerate(fields_spc):
            field_spc['name'] = field_names_convert[field_spc['name']]
            # Для UUID поля по умолчанию явно указывается что это поле <uuid>
            # поэтому отключаем это
            field_spc['field'] = None
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
        ref_uuid = self.getRefUUID()
        if self.value is None and ref_uuid:
            # Если значение не определено а UUID определен
            # то инициализировать значение
            self.value = ref_uuid
        return self.value

    def getRefUUID(self):
        """
        Текущий UUID.
        """
        return self._value

    getValue = getRefUUID

    def getStrData(self):
        """
        Строковое представление текущего значения объекта.
        ВНИМАНИЕ! у реквизита связи с бизнес объектом/документом
        строковое представление - это поле n_obj.
        """
        ref_obj = self.getRefObj()
        if ref_obj:
            n_obj = ref_obj.getRequisiteValue('n_obj')
            if n_obj is None:
                n_obj = ''
            elif not isinstance(n_obj, str):
                n_obj = str(n_obj)
            return n_obj
        return str(self._value) if self._value is not None else ''

    def setData(self, data):
        """
        Установить текущее значение объекта.
        @param data: Данные в виде словаря в формате 'defaults'.
        """
        if self.value is None:
            self.value = dict()
        self.value.update(data)

    def _getEditType(self):
        """
        Определить тип редактора реквизита.
        Тип редактора в случае реквизита определяется по типу хранимого
        значения.
        """
        return form_generator.REF_EDIT_TYPE

    def setMyData(self, record):
        """
        Установить мои данные из записи.
        @param record: Запись в виде словаря.
        """
        for field_name in self.getFields().keys():
            if record is not None:
                if field_name in record:
                    self.setData({field_name: record[field_name]})
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

    def createLabelCtrl(self, parent=None):
        """
        Создание объекта контрола надписи реквизита.
        """
        spc = self._genStdLabelRes()
        return self.GetKernel().createObjBySpc(parent, spc)

    def createEditorCtrl(self, parent=None):
        """
        Создание объекта контрола редактора реквизита.
        @param parent: Родительское окно.
        """
        spc = self._genREFEditorRes(self.name+'_edit')
        return self.GetKernel().createObjBySpc(parent, spc)

    def setRefObj(self, ref_obj):
        """
        Установить бизнес объект/документ.
        @param ref_obj: Объект бизнес объекта/документа.
            Можно также задавать паспортом.
        @return:
        """
        if toolfunc.is_pasport(ref_obj):
            self.setRefObjByPsp(ref_obj)
        else:
            self.ref_obj = ref_obj

    def setRefObjByPsp(self, obj_psp):
        """
        Установить бизнес объект/документ по его паспорту.
        @param obj_psp: Паспорт бизнес объекта/документа.
        @return: Объект созданного бизнес объекта/документа.
        """
        ref_obj = self.GetKernel().Create(obj_psp)
        self.setRefObj(ref_obj)
        return self.ref_obj
