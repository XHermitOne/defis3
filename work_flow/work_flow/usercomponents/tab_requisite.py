#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс пользовательского компонента ТАБЛИЧНЫЙ РЕКВИЗИТ.

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
from ic.utils import coderror
from ic.dlg import ic_dlg
from ic.bitmap import ic_bmp
import ic.components.icResourceParser as prs
# from work_flow.work_sys import workflow_img
import ic.PropertyEditor.icDefInf as icDefInf

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

import work_flow.work_sys.ictabrequisite as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icTABRequisite'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = dict({'type': 'TABRequisite',
                     'name': 'default',
                     'child': [],
                     'activate': True,
                     'init_expr': None,
                     '_uuid': None,

                     # --- Свойства генерации контролов редактирования/просмотра ---
                     'grp_title': u'',  # Реквизиты могут группироваться по страницам
                                        # Страницы различаются только по русским заголовкам.
                                        # Если заголовок страницы не определен, то
                                        # считается что реквизит располагается на главной
                                        # странице 'Основные'
                        
                     'label': u'',  # Надпись реквизита
                                    # Если надпись пустая, то берется вместо надписи описание (description)
    
                     'is_init': True,   # Реквизит является инициализируемым пользователем
                     'is_view': True,   # Реквизит можно просматривать на форме просмотра
                     'is_edit': True,   # Реквизит можно редактировать на форме редактировать
                     'is_search': False,  # Реквизит можно задавать в качестве критерия поиска объекта

                     # --- Ссылка на объект справочника ---
                     'table': None,     # Паспорт таблицы хранения, если None то генерируется по имени реквизита

                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description', 'grp_title', 'label'],
                                        icDefInf.EDT_TEXTLIST: ['init_users', 'edit_users', 'view_users',
                                                                'print_users', 'del_users', 'send_users'],
                                        icDefInf.EDT_CHECK_BOX: ['activate', 'is_init', 'is_view', 'is_edit',
                                                                 'is_search'],
                                        icDefInf.EDT_USER_PROPERTY: ['table'],
                                        },
                     '__events__': {},
                     '__parent__': parentModule.SPC_IC_TAB_REQUISITE,
                     '__attr_hlp__': {'grp_title': u'Заголовок страницы',
                                      'label': u'Надпись реквизита',
                                      'is_init': u'Реквизит является инициализируемым пользователем',
                                      'is_view': u'Реквизит можно просматривать на форме просмотра',
                                      'is_edit': u'Реквизит можно редактировать на форме редактировать',
                                      'is_search': u'Реквизит можно задавать в качестве критерия поиска объекта',
                                      'table': u'Паспорт таблицы хранения, если None то генерируется по имени реквизита',
                                      },
                     })
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('tags-label.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('tags-label.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Requisite', 'NSIRequisite']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('table',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('table',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in ('Table',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является ТАБЛИЦЕЙ.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('table',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icTABRequisite(parentModule.icTABRequisitePrototype,
                     icwidget.icSimple):
    """
    Табличный реквизит.

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

        parentModule.icTABRequisitePrototype.__init__(self, parent)
        
        # --- Свойства компонента ---
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
            
        # Устаонвить значение по умолчанию
        # self.init_data()
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)
      
    def getChildrenRequisites(self):
        """
        Дочерние реквизиты и спецификации.
        """
        return self.component_lst
          
    def getTabPsp(self):
        """
        Паспорт таблицы.
        """
        return self.getICAttr('table')

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
        return False
    
    def isIDAttr(self):
        """
        Реквизит является идентифицирующим объект?
        """
        return False
    
    def isDescription(self):
        """
        Реквизит является описывающим объект?
        """
        return False
    
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
