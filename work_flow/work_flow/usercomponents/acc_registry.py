#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Регистр накопления
Класс пользовательского компонента РЕГИСТР НАКОПЛЕНИЯ.

Порядок работы с регистром накопления:
1. Создаем объект регистра накопления
2. Создаем связь с БД (Вызываем метод connect())
3. Вызываем методы прихода/расхода/групповых операций (receipt/expense/do_operations)
4. Закрываем связь с БД (Вызываем метод disconnect())

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
import ic.components.icResourceParser as prs
from ic.bitmap import ic_bmp
from ic.log import log
from ic.utils import coderror
from ic.dlg import ic_dlg
import ic.PropertyEditor.icDefInf as icDefInf

import work_flow.work_sys.icregistry as parentModule
from work_flow.work_sys import icworkbase
from work_flow.work_sys import persistent

from work_flow.work_sys import icrequisite

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icAccumulateRegistry'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = dict({'type': 'AccumulatingRegistry',
                     'name': 'default',
                     'child': [],
                     '__events__': {},
                     'activate': True,
                     'init_expr': None,

                     # БД хранения данных
                     'db': None,

                     # Список имен реквизитов измерений
                     'dimension_requisites': [],
                     # Список имен реквизитов ресурсов
                     'resource_requisites': [],

                     # Имя таблицы операций движения
                     'operation_table': 'operation_tab',

                     # Имя таблицы итогов
                     'result_table': 'result_tab',

                     '_uuid': None,
                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description',
                                                                 'operation_table', 'result_table'],
                                        icDefInf.EDT_USER_PROPERTY: ['db'],
                                        icDefInf.EDT_TEXTLIST: ['dimension_requisites',
                                                                'resource_requisites'],
                                        },
                     '__parent__': parentModule.SPC_IC_ACCUMULATE_REGISTRY,
                     '__attr_hlp__': {'db': u'БД хранения данных',
                                      'dimension_requisites': u'Список имен реквизитов измерений',
                                      'resource_requisites': u'Список имен реквизитов ресурсов',
                                      'operation_table': u'Имя таблицы операций движения',
                                      'result_table': u'Имя таблицы итогов',
                                      },
                     })
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('table-sum.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('table-sum.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Requisite', 'NSIRequisite', 'REFRequisite']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 5)

# Словарь конвертации типов значений реквизитов ресурса
# к типу полей таблиц регистра накопления
REQUISITE_VAL_TYPE_TRANSLATE = dict(T='text', I='int', F='float',
                                    DateTime='datetime')


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('db', ):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('db',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('PostgreSQLDB', 'SQLiteDB'):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является БД.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('db', ):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icAccumulateRegistry(icwidget.icSimple,
                           parentModule.icAccumulateRegistryProto,
                           persistent.icAccRegPersistent):
    """
    Регистр накопления.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

    """

    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0,
                 evalSpace=None, bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
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

        db = self.getDB()
        db_url = db.getDBUrl() if db else None
        if not db_url:
            log.warning(u'Не определен URL БД регистра накопления <%s>' % self.getName())
        parentModule.icAccumulateRegistryProto.__init__(self, db_url=db_url,
                                                        operation_table_name=self.getOperationTabName(),
                                                        result_table_name=self.getResultTabName())
        persistent.icAccRegPersistent.__init__(self)
        
        # --- Свойства компонента ---
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [name for name in component.keys() if not name.startswith('__')]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        # Определить измерения и ресурсы регистра накопления
        dimension_requisite_names = self.getDimensionRequisiteNames()
        dimension_requisites = [requisite for requisite in self.getChildrenRequisites() if requisite.name in dimension_requisite_names]
        for requisite in dimension_requisites:
            requisite_name = requisite.name
            requisite_type = REQUISITE_VAL_TYPE_TRANSLATE.get(requisite.getTypeValue(), 'text')
            self.append_dimension_requisite(requisite_name, requisite_type)

        resource_requisite_names = self.getResourceRequisiteNames()
        resource_requisites = [requisite for requisite in self.getChildrenRequisites() if requisite.name in resource_requisite_names]
        for requisite in resource_requisites:
            requisite_name = requisite.name
            requisite_type = REQUISITE_VAL_TYPE_TRANSLATE.get(requisite.getTypeValue(), 'text')
            self.append_resource_requisite(requisite_name, requisite_type)

        # Дополнительные реквизиты
        extended_requisite_names = self.getExtendedRequisiteNames()
        extended_requisites = [requisite for requisite in self.getChildrenRequisites() if requisite.name in extended_requisite_names]
        for requisite in extended_requisites:
            requisite_name = requisite.name
            requisite_type = REQUISITE_VAL_TYPE_TRANSLATE.get(requisite.getTypeValue(), 'text')
            self.append_extended_requisite(requisite_name, requisite_type)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        for child_res in self.resource['child']:
            prs.icBuildObject(self, child_res, evalSpace=self.evalSpace,
                              bIndicator=progressDlg)
                
    #   Обработчики событий
    
    #   Свойства
    def getDBPsp(self):
        """
        Паспорт БД.
        """
        return self.getICAttr('db')

    def getDB(self):
        """
        Объект БД.
        """
        db_psp = self.getDBPsp()
        db = None
        if db_psp:
            db = self.GetKernel().Create(db_psp)
        return db

    def getChildrenRequisites(self):
        """
        Дочерние реквизиты.
        """
        return [child for child in self.get_children_lst() if issubclass(child.__class__, icworkbase.icRequisiteBase)]

    def getChildren(self):
        """
        Все внутренние объекты: реквизиты объекта и вложенные объекты в виде списка.
        """
        return self.get_children_lst()

    def getOperationTabName(self):
        """
        Имя таблицы операций движений.
        """
        return self.getICAttr('operation_table')

    def getResultTabName(self):
        """
        Имя таблицы итогов.
        """
        return self.getICAttr('result_table')

    def getDimensionRequisiteNames(self):
        """
        Имена реквизитов измерений.
        """
        return self.getICAttr('dimension_requisites')

    def getResourceRequisiteNames(self):
        """
        Имена реквизитов ресурсов.
        """
        return self.getICAttr('resource_requisites')

    def getExtendedRequisiteNames(self):
        """
        Имена реквизитов ресурсов.
        """
        used_requisite_names = self.getDimensionRequisiteNames() + self.getResourceRequisiteNames()
        return [requisite.name for requisite in self.getChildrenRequisites() if requisite.name not in used_requisite_names]
