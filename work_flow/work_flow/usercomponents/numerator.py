#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Нумератор.
Класс пользовательского компонента НУМЕРАТОР.

Порядок работы с нумератором:
1. Создаем объект нумератора.
2. Вызываем метод генерации/отмены нового номер-кода (do_gen|undo_gen)

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
from ic.dlg import ic_dlg
from ic.utils import ic_time
import ic.PropertyEditor.icDefInf as icDefInf

import work_flow.work_sys.numerator as parentModule
# from work_flow.work_sys import icworkbase
# from work_flow.work_sys import persistent
#
# from work_flow.work_sys import icrequisite

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
# from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt

import ic

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icNumerator'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = dict({'type': 'Numerator',
                     'name': 'default',
                     'child': [],
                     '__events__': {},
                     'activate': True,
                     'init_expr': None,

                     # БД хранения данных
                     'db': None,

                     # Имя таблицы нумератора
                     'numerator_table': 'numerator_tab',

                     # Формат номер-кода
                     'num_code_fmt': parentModule.DEFAULT_NUM_CODE_FMT,

                     # Проверить уникальность номер-кода?
                     'check_unique': False,

                     # Системное время используем?
                     'use_sys_dt': True,

                     '_uuid': None,
                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description',
                                                                 'numerator_table',
                                                                 'num_code_fmt'],
                                        icDefInf.EDT_CHECK_BOX: ['check_unique', 'use_sys_dt'],
                                        icDefInf.EDT_USER_PROPERTY: ['db'],
                                        },
                     '__parent__': icwidget.SPC_IC_SIMPLE,
                     '__attr_hlp__': {'db': u'БД хранения данных',
                                      'numerator_table': u'Имя таблицы нумератора',
                                      'num_code_fmt': u'Формат номер-кода',
                                      'check_unique': u'Проверить уникальность номер-кода?',
                                      'use_sys_dt': u'Системное время используем?',
                                      },
                     })
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('ui-paginator.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('ui-paginator.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 1)

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


class icNumerator(icwidget.icSimple,
                  parentModule.icNumerator):
    """
    Нумератор.

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
        parentModule.icNumerator.__init__(self, db_url=db_url,
                                          numerator_table_name=self.getNumeratorTabName(),
                                          num_code_format=self.getNumCodeFormat(),
                                          check_unique=self.getCheckUnique())

        # --- Свойства компонента ---
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [name for name in component.keys() if not name.startswith('__')]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

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

    def getChildren(self):
        """
        Все внутренние объекты: реквизиты объекта и вложенные объекты в виде списка.
        """
        return self.get_children_lst()

    def getNumeratorTabName(self):
        """
        Имя таблицы нумератора.
        """
        return self.getICAttr('numerator_table')

    def getNumCodeFormat(self):
        """
        Формат номер-кода.
        Формат кода нумератора может содержать все временные форматы,
        а также
            <%N> - номер идентификатора строки таблицы нумератора.
            <%E> - дополнительные параметры, передаваемые функции
                   генерации кода в качестве дополнительных аргументов.
        """
        return self.getICAttr('num_code_fmt')

    def getCheckUnique(self):
        """
        Производить проверку уникальности
            генерируемого номер-кода?
        """
        return self.getICAttr('check_unique')

    def getUseSysDT(self):
        """
        Используем системные дату-время?
        """
        return self.getICAttr('use_sys_dt')

    def get_actual_year(self):
        """
        Актуальнй год для определения максимального счетчика.
        Но метод можно переопределить.
        В качестве актуального года берется программный/операционный год.
        А если он не определен, то берем системный.
        @return: Значение года системы.
        """
        if self.getUseSysDT():
            return ic_time.getNowYear()

        operate_year = ic.getOperateYear()
        # print 'Operate year', operate_year, type(operate_year)
        return operate_year if operate_year else ic_time.getNowYear()
