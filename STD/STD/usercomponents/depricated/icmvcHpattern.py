#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент - 'Жесткий' MVC паттерн. Паттерн позволяет элемент
находится только в одном паттерне.

'Жесткий' MVC паттерн.
Класс пользовательского визуального компонента.

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
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
from ic.PropertyEditor.ExternalEditors import baseeditor
from ic.dlg import msgbox
import ic.patterns.mvc_pattern as parentModule
import icmvcelement
import icmvcpattern
from ic.utils import coderror

from STD import reestr_img

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMVCHPattern'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {},
                'type': 'MVCHPattern',
                'model':None,
                'view':None,
                'controller':None,
                'pattern_activate':None,
                'pattern_deactivate':None,
                #'bActiveState':True,         # Признак активного состояния
                'name': 'default',
                '__parent__': icwidget.SPC_IC_SIMPLE,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type'],
                                    icDefInf.EDT_USER_PROPERTY: ['model','view','controller']}}
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = reestr_img.mvcHPattern
ic_class_pic2 = reestr_img.mvcHPattern

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Unit']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0,0,0,1)

### Функции редактирования
get_user_property_editor = icmvcpattern.get_user_property_editor
str_to_val_user_property = icmvcpattern.str_to_val_user_property

def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('model','view','controller'):
        pres = propEdt.GetPrntResource()
        lst = icmvcelement.findClassLst(pres, parentModule.ic_mvc_element, propEdt.GetResTree().GetObjectsInfo())
        lstp = icmvcelement.findClassResLst(pres, parentModule.ic_mvc_pattern, propEdt.GetResTree().GetObjectsInfo())
        
        if value in lst:
            name = propEdt.GetResource()['name']
            for pt in lstp:
                if name <> pt['name'] and value in (pt['model'],
                                            pt['view'], pt['controller']):
                    parent = propEdt.GetPropertyGrid().GetView()
                    msgbox.MsgBox(parent, u'Элемент <%s> уже зарегистрирован в другом паттерне <%s>.'
                                %  (value, pt['name']))
                    return coderror.IC_CTRL_FAILED_IGNORE
                
            return icmvcpattern.property_editor_ctrl(attr, value, propEdt)
        
class icMVCHPattern(icmvcpattern.icMVCPattern):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='MVCHPattern'}:
        - B{name='default'}:
        - B{model=None}: указатель на модель;
        - B{view=None}: указатель на предсавление;
        - B{controller=None}: указатель на контроллек.
        - B{pattern_activate=None}: выражение активации паттерна.
        - B{pattern_deactivate=None}: выражение деактивации паттерна.
    """

    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType = 0, evalSpace = None,
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
        icmvcpattern.icMVCPattern.__init__(self, parent, id, component, logType,
                        evalSpace, bCounter, progressDlg)
        
def test(par=0):
    """
    Тестируем пользовательский класс.
    
    @type par: C{int}
    @param par: Тип консоли.
    """
    
    import ic.components.ictestapp as ictestapp
    
    app = ictestapp.TestApp(par)
    common.img_init()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    
    #   win = icButton(-1, win, {})
    #ctrl_1 = StateIndicator(win, -1, {'position':(100,35), 'size':(100,30)})
    
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    """
    Тестируем пользовательский класс.
    """
    test()
