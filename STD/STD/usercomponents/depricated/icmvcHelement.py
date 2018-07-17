#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компнент элемента MVC, который содержит только "жесткие" паттерны (icmvcHpattern.py)
- элемент может быть только в одном патерне.

Компонент реализует элемент MVC паттерна.

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
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors import baseeditor
import ic.patterns.mvc_pattern as parentModule
from ic.utils import coderror
from ic.dlg import msgbox
import ic.kernel.icobject as icobject
from ic.engine import ic_user
from STD import reestr_img
from ic.kernel import io_prnt
import icmvcelement
#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMVCHElement'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {},
                'child': [],
                'type': 'MVCHElement',
                'name': 'default',
                'model_in':None,        # функция обработки входных сигналов (в роли модели)
                'model_out':None,       # функция генерации выходных сигналов (в роли модели)
                'view_in':None,
                'view_out':None,
                'controller_in':None,
                'controller_out':None,
                'socket_in':None,       # вход
                'socket_out':None,      # выход
                'current_pattern':None,   # текущий рабочий паттерн
                'object':None,          # Ссылка на агрегируемый объект
                '__attr_types__': {0: ['name', 'type'],
                        icDefInf.EDT_USER_PROPERTY:['object',
                            'current_pattern',
                            'socket_in',
                            'socket_out']},
                '__parent__':icwidget.SPC_IC_SIMPLE}
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = reestr_img.mvcHElement
ic_class_pic2 = reestr_img.mvcHElement

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

### Функции редактирования
get_user_property_editor = icmvcelement.get_user_property_editor
property_editor_ctrl = icmvcelement.property_editor_ctrl
str_to_val_user_property = icmvcelement.str_to_val_user_property
        
def get_can_contain_lst(propEdt=None):
    """
    Функция возвращает список компонентов, которые могут вставлятся в компонент.
    """
    dct = propEdt.tree.GetObjectsInfo()
    lst = ['MVCElement','MVCHPattern', 'Group', 'Unit']
    
    for key, el in dct.items():
        mod = el[-1]
        try:
            if (mod and hasattr(mod, 'ic_class_name') and
                issubclass(getattr(mod, mod.ic_class_name), parentModule.ic_mvc_element)):
                    lst.append(key)
        except:
            io_prnt.outErr('error in key=%s' % key)

    return lst

###

class icMVCHElement(icmvcelement.icMVCElement):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{child=[]}:
        - B{type='MVCElement'}:
        - B{name='default'}:
        - B{model_in=None}: функция обработки входных сигналов (в роли модели);
        - B{model_out=None}:функция генерации выходных сигналов (в роли модели);
        - B{view_in=None}: функция обработки входных сигналов (в роли представления);
        - B{view_out=None}: функция генерации выходных сигналов (в роли представления);
        - B{controller_in=None}: функция обработки входных сигналов (в роли контроллера);
        - B{controller_out=None}: функция генерации выходных сигналов (в роли контроллера);
        - B{current_pattern=''}: текщий рабочий паттерн;
        - B{object:None}: паспорт агрегируемого объекта.
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
        icmvcelement.icMVCElement.__init__(self, parent, id, component, logType, evalSpace,
                                    bCounter, progressDlg)

    #--- Функции доступа к остальным элементам паттрерна
    def GetView(self):
        """
        """
        lst = self.get_in_pattern_lst()
        if lst:
            return lst[0].get_view()
            
    def GetModel(self):
        """
        """
        lst = self.get_in_pattern_lst()
        if lst:
            return lst[0].get_model()
        
    def GetController(self):
        """
        """
        lst = self.get_in_pattern_lst()
        if lst:
            return lst[0].get_controller()
        
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
