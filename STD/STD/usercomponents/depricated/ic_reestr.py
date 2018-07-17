#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<< Типовой шаблон пользовательского компонента >>

"""
Реестр объектов.

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

#import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

import ic.components.user.ic_metatree_wrp as parentModule
from ic.components.user import ic_metaitem_wrp
from STD import reestr_img

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icReestr'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {
    '__events__': {}, 
    'child': [], 
    'type': 'Reestr', 
    'name': 'default', 
    'activate':1,
    'init_expr':None,
    '_uuid':None,
    '__lists__':{'storage_type':[ic_metaitem_wrp.FILE_NODE_STORAGE_TYPE,ic_metaitem_wrp.FILE_STORAGE_TYPE, ic_metaitem_wrp.DIR_STORAGE_TYPE]},
    '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', 
                        'view_form','edit_form','print_report', '_uuid'],
                        #icDefInf.EDT_TEXTLIST:['can_contain','can_not_contain'],
                        icDefInf.EDT_CHECK_BOX:['container'],
                        icDefInf.EDT_TEXTDICT:['spc','const_spc'],
                        icDefInf.EDT_CHOICE:['storage_type'],
                       }, 
    '__parent__':parentModule.SPC_IC_METATREE, 
    }
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = reestr_img.imgReestr
ic_class_pic2 = reestr_img.imgReestr

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['ReestrObject']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0,0,0,1)

class icReestr(icwidget.icSimple, parentModule.icMetaTreeEngine):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

    """

    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType = 0, evalSpace = None,
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

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') <> 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.icMetaTreeEngine.__init__(self,component)
        #img = common.imgEdtImage
        #parentModule.GenBitmapTextButton.__init__(self, parent, id, img, self.label, self.position, self.size, style = self.style, name = self.name)
        
        #   Регистрация обработчиков событий
        

        #self.BindICEvt()
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace = self.evalSpace, 
                                bCounter = bCounter, progressDlg = progressDlg)
      
    #   Обработчики событий
