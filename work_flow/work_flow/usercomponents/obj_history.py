#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ИСТОРИЯ БИЗНЕС-ОБЪЕКТА (Регистр/реестр бизнес объектов).
Класс пользовательского компонента ИСТОРИЯ БИЗНЕС-ОБЪЕКТ.

Порядок работы с регистром:
1. Создаем объект регистра
2. Создаем связь с БД (Вызываем метод connect())
3. Вызываем методы изменения состояния объекта (do_state/undo_state)
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
from ic.utils import coderror
from ic.log import log
from ic.dlg import ic_dlg
import ic.PropertyEditor.icDefInf as icDefInf

import work_flow.work_sys.icregistry as parentModule
from work_flow.work_sys import icworkbase

from work_flow.work_sys import icrequisite

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icObjHistory'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = dict({'type': 'ObjHistory',
                     'name': 'default',
                     'child': [],
                     '__events__': {},
                     'activate': True,
                     'init_expr': None,

                     # БД хранения данных
                     'db': None,

                     # Имя таблицы операций движения
                     'operation_table': 'operation_object',

                     # Имя таблицы объектов
                     'obj_table': 'object_tab',

                     '_uuid': None,
                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description',
                                                                 'operation_table', 'obj_table'],
                                        icDefInf.EDT_USER_PROPERTY: ['db'],
                                        },
                     '__parent__': parentModule.SPC_IC_OBJECT_REGISTRY,
                     '__attr_hlp__': {'db': u'БД хранения данных',
                                      'operation_table': u'Имя таблицы операций движения',
                                      'obj_table': u'Имя таблицы объектов',
                                      },
                     })
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('clock-history-frame.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('clock-history-frame.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Requisite', 'NSIRequisite', 'REFRequisite']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 1)

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


class icObjHistory(icwidget.icSimple, parentModule.icObjectRegistryProto):
    """
    Регистр бизнес объекта.

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
            log.warning(u'Не определен URL БД истории бизнес объекта <%s>' % self.getName())
        parentModule.icObjectRegistryProto.__init__(self, db_url=db_url,
                                                    operation_table_name=self.getOperationTabName(),
                                                    obj_table_name=self.getObjectTabName())
        
        # --- Свойства компонента ---
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [name for name in component.keys() if not name.startswith('__')]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        # Дополнительные реквизиты
        obj_requisites = self.getChildrenRequisites()
        for requisite in obj_requisites:
            requisite_name = requisite.name
            requisite_type = REQUISITE_VAL_TYPE_TRANSLATE.get(requisite.getTypeValue(), 'text')
            self.append_obj_requisite(requisite_name, requisite_type)

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
            if not db:
                log.warning(u'Не определена БД для истории бизнес объекта <%s>' % self.getName())
        else:
            log.warning(u'Не определен паспорт БД')
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

    def getObjectTabName(self):
        """
        Имя таблицы объектов.
        """
        return self.getICAttr('obj_table')

    def getObjRequisiteNames(self):
        """
        Имена реквизитов ресурсов.
        """
        return [requisite.name for requisite in self.getChildrenRequisites()]
