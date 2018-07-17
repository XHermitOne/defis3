#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс пользовательского компонента РЕКВИЗИТ-ССЫЛКА НА БИЗНЕС ОБЪЕКТ/ДОКУМЕНТ.

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
from ic.utils import util
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
from ic.utils import coderror
import ic.PropertyEditor.icDefInf as icDefInf

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
#from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt

import work_flow.work_sys.icrefrequisite as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icREFRequisite'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = dict({'type': 'REFRequisite',
                     'name': 'default',
                     'child': [],
                     'activate': 1,
                     'init_expr': None,
                     '_uuid': None,

                     # Свойства генерации контролов редактирования/просмотра
                     'grp_title': u'',      # Реквизиты могут группироваться по страницам
                                            # Страницы различаются только по русским заголовкам.
                                            # Если заголовок страницы не определен, то
                                            # считается что реквизит располагается на главной
                                            # странице 'Основные'

                     'label': u'',      # Надпись реквизита
                                        # Если надпись пустая, то берется вместо надписи описание (description)

                     'is_init': True,   # Реквизит является инициализируемым пользователем
                     'is_view': True,   # Реквизит можно просматривать на форме просмотра
                     'is_edit': True,   # Реквизит можно редактировать на форме редактировать
                     'is_search': True,  # Реквизит можно задавать в качестве критерия поиска объекта

                     'id_attr': True,   # Реквизит является идентифицирующим объект каким-то либо образом
                                        # Реквизит, у которого True будет добавляться в
                                        # гриды объектов  в виде колонки
                     'is_description': False,   # Реквизит является описательным

                     # Свойства генерации полей хранения

                     'fields': None,  # Соответствие полей таблицы и справочника,
                                      # в котором храниться значения реквизита (словарь)
                     'defaults': None,  # Значения по умолчанию (словарь)
                     'field': None,     # Поле кода справочника

                     'set_value': None,  # Функционал, исполняемый при установке значения реквизита
                     'get_value': None,  # Функционал, исполняемый при получениии значения реквизита

                     # Ссылка на объект справочника
                     'obj_psp': None,  # Бизнес объект/документ
                     'auto_set': True,  # Признак автоматического заполнения полей при редактировании

                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description', 'grp_title', 'label', 'field'],
                                        icDefInf.EDT_TEXTLIST: ['init_users', 'edit_users', 'view_users', 'print_users',
                                                                'del_users', 'send_users'],
                                        icDefInf.EDT_TEXTDICT: ['fields', 'defaults'],
                                        icDefInf.EDT_CHECK_BOX: ['auto_set', 'is_init', 'is_view', 'is_edit',
                                                                 'is_search', 'id_attr', 'is_description'],
                                         icDefInf.EDT_USER_PROPERTY: ['obj_psp'],
                                        },
                     '__events__': {},
                     '__parent__': parentModule.SPC_IC_REF_REQUISITE,
                     '__attr_hlp__': {'grp_title': u'Заголовок страницы',
                                      'label': u'Надпись реквизита',
                                      'is_init': u'Реквизит является инициализируемым пользователем',
                                      'is_view': u'Реквизит можно просматривать на форме просмотра',
                                      'is_edit': u'Реквизит можно редактировать на форме редактировать',
                                      'is_search': u'Реквизит можно задавать в качестве критерия поиска объекта',
                                      'id_attr': u'Реквизит является идентифицирующим объект каким-то либо образом',
                                      'is_description': u'Реквизит является описательным',
                                      'fields': u'Соответствие полей таблицы и справочника, в котором храниться значения реквизита (словарь)',
                                      'defaults': u'Значения по умолчанию (словарь)',
                                      'field': u'Поле кода справочника',
                                      'set_value': u'Функционал, исполняемый при установке значения реквизита',
                                      'get_value': u'Функционал, исполняемый при получениии значения реквизита',
                                      'obj_psp': u'Бизнес объект/документ',
                                      'auto_set': u'Признак автоматического заполнения полей при редактировании',
                                      },
                     })
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('tag--arrow.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('tag--arrow.png')

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

# Функции редактирования


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('obj_psp',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('obj_psp',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if ret[0][0] not in ('BusinessObj', 'StateObj', 'Document'):
                ic_dlg.icWarningBox(u'ОШИБКА', u'Выбранный объект не является Бизнес-объектом/Документом.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('obj_psp',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icREFRequisite(parentModule.icREFRequisitePrototype,icwidget.icSimple):
    """
    Реквизит-ссылка на бизнес объект/документ.

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
        if component['fields'] is None:
            component['fields'] = {component['name']: 'uuid'}
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icREFRequisitePrototype.__init__(self, parent)
        
        # --- Свойства компонента ---
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])

    def getFields(self):
        """
        Имена полей реквизита таблицы.
        """
        fields_dict = self.getICAttr('fields')
        field_value = self.getField()
        if fields_dict and isinstance(fields_dict, dict):
            if field_value:
                fields_dict[field_value] = 'uuid'
            return fields_dict
        else:
            return {field_value: 'uuid'}

    def getField(self):
        """
        Имя поля реквизита таблицы.
        """
        return self.getICAttr('field')

    def getDefaults(self):
        """
        Значения полей реквизита таблицы по умолчанию.
        """
        return self.getICAttr('defaults')

    def getRefObjPsp(self):
        """
        Паспорт бизнес объекта/документа, на который ссылается реквизит.
        """
        return self.getICAttr('obj_psp')

    def getRefObj(self):
        """
        Объект бизнес объекта/документа, на который ссылается реквизит.
        """
        if self.ref_obj is None:
            psp = self.getRefObjPsp()
            if psp is None:
                assert None, 'Not define <obj_psp> in REFRequisite <%s>' % self.name
                return None
            self.ref_obj = self.GetKernel().Create(psp)
        return self.ref_obj

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
