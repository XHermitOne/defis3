#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<< Типовой шаблон пользовательского компонента >>

"""
Объект, агента Microsoft.

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
    
@type ICSpeedometerStyle: C{dictionary}
@var ICSpeedometerStyle: Словарь специальных стилей компонента.
Описание ключей ICSpeedometerStyle:

    - C{SM_ROTATE_TEXT): Отрисовка текста шкалы перпендикулярно радиусу.
    - C{SM_DRAW_SECTORS): Отрисовка полного круга поля.
    - C{SM_DRAW_PARTIAL_SECTORS): Отрисовка полосы по кругу поля.
    - C{SM_DRAW_HAND): Отрисовка стрелки.
    - C{SM_DRAW_SHADOW): Отрисовка тени стрелки.
    - C{SM_DRAW_PARTIAL_FILLER): Отрисовка следа за стрелкой.
    - C{SM_DRAW_SECONDARY_TICKS): Отрисовка минорной шкалы.
    - C{SM_DRAW_MIDDLE_TEXT): -.
    - C{SM_DRAW_MIDDLE_ICON): -.
    - C{SM_DRAW_GRADIENT): Градиентная заливка поля.
    - C{SM_DRAW_FANCY_TICKS): Отрисовка мажорной шкалы.
"""

#import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import ic.engine.ic_user as ic_user

from ic.log import ic_log
#from ic.utils import ic_file
#from ic.components import icfont

import STD.visualcomponents.icMSAgent as parentModule
from STD.visualcomponents import visualcomponents_img

#--- Спецификация ---

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMSAgent'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {},
                'child': [],
                'type': 'MSAgent',
                'name': 'default',
                'activate':1,
                '_uuid':None,

                'character':'default',
                
                '__lists__':{'character':parentModule.CHARACTERS,},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description','_uuid',],
                                    icDefInf.EDT_CHOICE:['character'],
                                   },
                '__parent__':parentModule.SPC_IC_MSAGENT,
                }
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = visualcomponents_img.Agent
ic_class_pic2 = visualcomponents_img.Agent

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

class icMSAgent(icwidget.icSimple,parentModule.icMSAgentControl):
    """
    Объект, агента Microsoft.

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
        parentModule.icMSAgentControl.__init__(self,component)
        
        #   Регистрация обработчиков событий
        
        #self.BindICEvt()
            
    #   Обработчики событий
