#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Реквизит.
Класс пользовательского компонента РЕКВИЗИТ.

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
from ic.bitmap import ic_bmp
import ic.components.icResourceParser as prs
# from work_flow.work_sys import workflow_img
import ic.PropertyEditor.icDefInf as icDefInf

import work_flow.work_sys.icrequisite as parentModule
from ic.db import icsqlalchemy

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icRequisite'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# Спецификация на ресурсное описание класса
ic_class_spc = dict({'type': 'Requisite',
                     'name': 'default',
                     'child': [],
                     'activate': 1,
                     'init_expr': None,
                     '_uuid': None,
     
                     # Свойства генерации поля хранения
                     'type_val': 'T',   # Тип значения реквизита
                     'len': None,       # Длина значения реквизита
                     'field': None,     # Поле таблицы родительского компонента, в котором храниться значение реквизита
                     'default': None,   # Значение по умолчанию

                     # Свойства генерации контролов редактирования/просмотра
                     'grp_title': u'',   # Реквизиты могут группироваться по страницам
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

                     'id_attr': True,   # Реквизит является идентифицирующим объект каким-то либо образом
                                        # Реквизит, у которого True будет добавляться в
                                        # гриды объектов  в виде колонки
                     'is_description': False,   # Реквизит является описательным

                     '__lists__': {'type_val': list(icsqlalchemy.FIELD_VALUES_ALL_TYPES)},
                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description', 'field', 'task',
                                                                 'grp_title', 'label'],
                                        icDefInf.EDT_TEXTLIST: ['init_users', 'edit_users', 'view_users',
                                                                'print_users', 'del_users', 'send_users'],
                                        icDefInf.EDT_CHOICE: ['type_val'],
                                        icDefInf.EDT_NUMBER: ['len'],
                                        icDefInf.EDT_CHECK_BOX: ['is_init', 'is_view', 'is_edit', 'is_search',
                                                                 'id_attr', 'is_description'],
                                        },
                     '__events__': {},
                     '__parent__': parentModule.SPC_IC_REQUISITE,
                     '__attr_hlp__': {'type_val': u'Тип значения реквизита',
                                      'len': u'Длина значения реквизита',
                                      'field': u'Поле таблицы родительского компонента, в котором храниться значение реквизита',
                                      'default': u'Значение по умолчанию',
                                      'grp_title': u'Заголовок страницы',
                                      'label': u'Надпись реквизита',
                                      'is_init': u'Реквизит является инициализируемым пользователем',
                                      'is_view': u'Реквизит можно просматривать на форме просмотра',
                                      'is_edit': u'Реквизит можно редактировать на форме редактировать',
                                      'is_search': u'Реквизит можно задавать в качестве критерия поиска объекта',
                                      'id_attr': u'Реквизит является идентифицирующим объект каким-то либо образом',
                                      'is_description': u'Реквизит является описательным',
                                      },
                     })
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('tag.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('tag.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 2)


class icRequisite(parentModule.icRequisitePrototype, icwidget.icSimple):
    """
    Реквизит.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

    """

    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
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

        parentModule.icRequisitePrototype.__init__(self, parent)
        
        # Свойства компонента
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        # Устаонвить значение по умолчанию
        self.init_data()
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)
      
    def getField(self):
        """
        Имя поля реквизита таблицы, в которой храниться документ.
        """
        return self.getICAttr('field')
        
    def getTypeValue(self):
        """
        Тип поля хранения реквизита.
        """
        return self.getICAttr('type_val')
        
    def getDefault(self):
        """
        Значение поля реквизита таблицы по умолчанию.
        """
        return self.eval_attr('default')[1]
    
    def isInit(self):
        """
        Реквизит является инициализируемым пользователем?
        """
        return self.getICAttr('is_init')

    def isEdit(self):
        """
        Реквизит является редактируемым пользователем?
        """
        return self.getICAttr('is_edit')

    def isView(self):
        """
        Реквизит является просматриваемым пользователем?
        """
        return self.getICAttr('is_view')
    
    def isSearch(self):
        """
        Реквизит можно задавать в качестве критерия поиска объекта?
        """
        return self.getICAttr('is_search')
    
    def isIDAttr(self):
        """
        Реквизит является идентифицирующим объект?
        """
        return self.getICAttr('id_attr')
    
    def isDescription(self):
        """
        Реквизит является описывающим объект?
        """
        return self.getICAttr('is_description')
    
    def getLabel(self):
        """
        Надпись реквизита.
        """
        return self.getICAttr('label')
        
    def getGroupTitle(self):
        """
        Надпись страницы/группы при группировке реквизитов на форме.
        """
        page_title = self.getICAttr('grp_title')
        if not page_title:
            # Страница <<Основные>> должна присутствовать в любой форме объекта
            page_title = u'Основные'
        return page_title
        
    #   Обработчики событий
