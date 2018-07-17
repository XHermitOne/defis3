#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<< Типовой шаблон пользовательского компонента >>

"""
Объект, регистрируемый в реестре.

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
import ic.engine.ic_user as ic_user

import ic.components.user.ic_metaitem_wrp as parentModule
from STD import reestr_img

#--- Спецификация ---
SPC_IC_REESTROBJ={
    'init_obj':None, #Скрипт, выполняемый при инициализации объекта реестра
    '__parent__':parentModule.SPC_IC_METAITEM,
    }
#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icReestrObject'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {},
                'child': [],
                'type': 'ReestrObject',
                'name': 'default',
                'activate':1,
                'doc_type':None,
                'init_expr':None,
                '_uuid':None,
                '__lists__':{'storage_type':[parentModule.FILE_NODE_STORAGE_TYPE,parentModule.FILE_STORAGE_TYPE,parentModule.DIR_STORAGE_TYPE],
                             'doc_type':ic_user.getPrjRoot().getObjNamesInResources(('mtd',), 'StdDoc')},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description','_uuid','doc'],
                                    icDefInf.EDT_PY_SCRIPT:['view_form','edit_form','print_report', 'init_obj'],
                                    #icDefInf.EDT_TEXTLIST:['can_contain','can_not_contain'],
                                    icDefInf.EDT_CHECK_BOX:['container'],
                                    icDefInf.EDT_CHOICE:['storage_type','doc_type'],
                                    icDefInf.EDT_TEXTDICT:['spc','const_spc'],
                                   },
                '__parent__':SPC_IC_REESTROBJ,
                }
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = reestr_img.imgReestrObj
ic_class_pic2 = reestr_img.imgReestrObj

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0,0,0,1)

class icReestrObject(icwidget.icSimple, parentModule.icMetaItemEngine):
    """
    Объект, регистрируемый в реестре.

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
        parentModule.icMetaItemEngine.__init__(self,parent,component)
        #parentModule.icMetaItemEngine.__init__(self, *args, **kwargs)
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
      
    def Add(self,Name_=None,Type_=None):
        """
        Добавить дочерний объект реестра.
        @param Name_: Имя добавляемого объекта,
            если None, то имя генерируется.
        @param Type_: Имя компонента, объект которого
            будет добавлен в дерево.
            Если None, то будет сделан запрос имени.
        @return: Созданный объект реестра.
        """
        new_reestr_obj=parentModule.icMetaItemEngine.Add(self,Name_,Type_)

        #Сразу проинициализировать, если это необходимо
        self.evalSpace['self']=self
        self.evalSpace['new_reestr_obj']=new_reestr_obj
        result,object=new_reestr_obj.eval_attr('init_obj')
        print('!!!NEW ReestrObject!!!',result,object,new_reestr_obj)
        if result and object and type(object)==type(''):
            #Объект задается именем
            obj=prs.icCreateObject(object,'frm')
            new_reestr_obj.setUserData(obj)
            #Сохранить сразу
            new_reestr_obj.Save()
        elif object and type(object)<>type(''):
            #Объект задается явно
            new_reestr_obj.setUserData(object)
            #Сохранить сразу
            new_reestr_obj.Save()
        else:
            #Объект по какой-то причине НЕ СОЗДАН!
            self.DelChild(new_reestr_obj.name)

        return new_reestr_obj
        
    def Edit(self,*args,**kwargs):
        """
        Открыть форму редактирования объекта реестра.
        """
        #Сразу проинициализировать, если это необходимо
        self.evalSpace['self']=self
        edit_form=self.getICAttr('edit_form')
        print('!!!EDIT ReestrObject!!!',edit_form)
        
        if edit_form and type(edit_form)==type(''):
            #Форма редактирования задается именем
            self._edit_form=edit_form
            return parentModule.icMetaItemEngine.Edit(self,*args,**kwargs)
        else:
            #Форма редактирования задается явно
            return edit_form
            
    #   Обработчики событий
