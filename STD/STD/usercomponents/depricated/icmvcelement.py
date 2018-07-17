#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<< Типовой шаблон пользовательского компонента >>

"""
Элемент паттерна.
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
#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMVCElement'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {},
                'child': [],
                'type': 'MVCElement',
                'name': 'default',
                'model_in':None,        # функция обработки входных сигналов (в роли модели)
                'model_out':None,       # функция генерации выходных сигналов (в роли модели)
                'view_in':None,
                'view_out':None,
                'controller_in':None,
                'controller_out':None,
                'current_pattern':None,   # текущий рабочий паттерн
                'socket_in':None,       # вход
                'socket_out':None,      # выход
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
ic_class_pic = reestr_img.mvcElement
ic_class_pic2 = reestr_img.mvcElement

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['MVCElement','MVCPattern', 'Group', 'Unit']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0,0,0,1)

###
def findObjLst(res, typObj, lst=None):
    """
    Возвращает список объектов заданного типа.
    """
    if lst == None:
        lst = []
        
    if 'child' in res:
        for el in res['child']:
            if el['type'] == typObj:
                lst.append(el['name'])
            elif el['type'] == 'Group':
                lst = findObjLst(el, typObj, lst)

    return lst

def findClassLst(res, classObj, infoLst, lst=None):
    """
    Возвращает список объектов наследованных от заданного класса.
    
    @param res: Ресурс, в котором ведется поиск.
    @param classObj: Класс родительского объекта.
    @param infoLst: Список, описывающий импортированные компоненты системы.
    """
    
    if lst == None:
        lst = []
        
    if 'child' in res:
        for el in res['child']:
            info = infoLst[el['type']]
            mod = info[-1]
            if mod and hasattr(mod, 'ic_class_name') and issubclass(getattr(mod, mod.ic_class_name), classObj):
                lst.append(el['name'])
            elif el['type'] == 'Group':
                lst = findClassLst(el, classObj, infoLst, lst)

    return lst

def findClassResLst(res, classObj, infoLst, lst=None):
    """
    Возвращает список объектов наследованных от заданного класса.
    
    @param res: Ресурс, в котором ведется поиск.
    @param classObj: Класс родительского объекта.
    @param infoLst: Список, описывающий импортированные компоненты системы.
    """
    
    if lst == None:
        lst = []
        
    if 'child' in res:
        for el in res['child']:
            info = infoLst[el['type']]
            mod = info[-1]
            if mod and hasattr(mod, 'ic_class_name') and issubclass(getattr(mod, mod.ic_class_name), classObj):
                lst.append(el)
            elif el['type'] == 'Group':
                lst = findClassResLst(el, classObj, infoLst, lst)

    return lst

### Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    if attr in ('object', 'socket_in', 'socket_out'):
        return pspEdt.get_user_property_editor(value, pos, size, style, propEdt)
    elif attr == 'current_pattern':
        parent = propEdt.GetPropertyGrid().GetView()
        lst = findObjLst(propEdt.GetResource(), 'MVCPattern')
        
        if lst:
            dlg = baseeditor.ChoiceMenu(parent, lst)
            parent.PopupMenu(dlg, pos)
        
            #   Возвращаем выбранный элемент списка
            if lst and dlg.IsSelString():
                value = dlg.GetSelString()
            
            dlg.Destroy()
            return value
        else:
            msgbox.MsgBox(parent, u'Паттерны элемента не определены')

def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('object', 'socket_in', 'socket_out'):
        return pspEdt.property_editor_ctrl(value, propEdt)
    elif attr == 'current_pattern':
        lst = findObjLst(propEdt.GetResource(), 'MVCPattern', 'MVCHPattern')

        if value in lst:
            return coderror.IC_CTRL_OK

def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('object', 'socket_in', 'socket_out'):
        return pspEdt.str_to_val_user_property(text, propEdt)
    elif attr == 'current_pattern':
        return text
        
def get_can_contain_lst(propEdt=None):
    """
    Функция возвращает список компонентов, которые могут вставлятся в компонент.
    """
    dct = propEdt.tree.GetObjectsInfo()
    #lst = ['MVCElement','MVCPattern', 'Group', 'Unit']
    lst = ['Group', 'Unit']
    
    for key, el in dct.items():
        mod = el[-1]
        try:
            if (mod and hasattr(mod, 'ic_class_name') and
                (issubclass(getattr(mod, mod.ic_class_name), parentModule.ic_mvc_element) or
                issubclass(getattr(mod, mod.ic_class_name), parentModule.ic_mvc_pattern))):
                    lst.append(key)
        except:
            io_prnt.outErr('error in key=%s' % key)
            
    return lst

###

class icMVCElement(icwidget.icSimple, parentModule.ic_mvc_element):
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
        - B{object=None}: паспорт агрегируемого объекта.
        - B{socket_in=None}: входной интерфейс - паспорт компонента WX_Binder;
        - B{socket_out=None}: выходной интерфейс - паспорт компонента WX_Binder;
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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') <> 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.ic_mvc_element.__init__(self, self.name)
        
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        #   Указатель на агрегированный объект
        self._agr_object = None
        self.agr_psp = None
#        if self.object:
#            self.agr_psp = icobject.icObjectPassport(*self.object)

        #   Регестрируем патерны
        #self.pattern_lst = [el for el in self.components.values() if el.type in ('MVCPattern','MVCHPattern')]
        self.pattern_lst = [el for el in self.components.values() if issubclass(el.__class__, parentModule.ic_mvc_pattern)]
    
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace = self.evalSpace,
                                bCounter = bCounter, progressDlg = progressDlg)
                          
    def create_object(self, psp, parent=None):
        """
        Создает объект.
        
        @param psp: Паспорт объекта, которые нобходимо создать.
        @param parent: Указатель на родительский объект.
        """
        if not psp:
            return
            
        if type(psp) in (type(tuple()), type(list())):
            psp = icobject.icObjectPassport(*psp)
            
        return ic_user.getKernel().Create(psp, parent)

    def create_agr_object(self, parent=None):
        """
        Создает агрегированный объект.
        
        @param parent: Указатель на родительский объект.
        """
        self._agr_object = self.create_object(self.object, parent)
        return self._agr_object

    def get_agr_object(self, bCreate=False):
        """
        Возвращает указатель на агрегированный объект.
        """
        if not self._agr_object and bCreate:
            self.create_agr_object()
        else:
            return self._agr_object

    def get_model_lst(self):
        """
        Возвращает список елементов в роли модели.
        """
        lst = []
        for ptrn in self.pattern_lst:
            el = ptrn.get_model()
            if el and not el in lst:
                lst.append(el)
        
        return lst

    def get_view_lst(self):
        """
        Возвращает список елементов в роли представления.
        """
        lst = []
        for ptrn in self.pattern_lst:
            el = ptrn.get_view()
            if el and not el in lst:
                lst.append(el)
        
        return lst
        
    def get_controller_lst(self):
        """
        Возвращает список елементов в роли контроллера.
        """
        lst = []
        for ptrn in self.pattern_lst:
            el = ptrn.get_controller()
            if el and not el in lst:
                lst.append(el)
        
        return lst
        
    #--- Функции модели ---
    def post_model(self, evt, *arg, **kwarg):
        """
        Вход.
        """
        self.GetContext()['self'] = self
        self.GetContext()['evt'] = evt
        self.eval_attr('model_in')
    
    def out_model(self, *arg, **kwarg):
        """
        Выход.
        """
        self.GetContext()['self'] = self
        self.eval_attr('model_out')

    #--- Функции представления ---
    def post_view(self, evt, *arg, **kwarg):
        """
        Вход.
        """
        self.GetContext()['self'] = self
        self.GetContext()['evt'] = evt
        self.eval_attr('view_in')
    
    def out_view(self, *arg, **kwarg):
        """
        Выход.
        """
        self.GetContext()['self'] = self
        self.eval_attr('view_out')

    #--- Функции контроллера ---
    def post_controller(self, evt, *arg, **kwarg):
        """
        Вход.
        """
        self.GetContext()['self'] = self
        self.GetContext()['evt'] = evt
        self.eval_attr('controller_in')

    def out_controller(self, *arg, **kwarg):
        """
        Выход.
        """
        self.GetContext()['self'] = self
        self.eval_attr('controller_out')
    
    #--- Функции доступа к остальным элементам паттрерна
    def GetView(self):
        """
        """
        ap = self.parent.get_active_pattern()
        if ap and self in ap.getMVC():
            return ap.get_view()
            
    def GetModel(self):
        """
        """
        ap = self.parent.get_active_pattern()
        if ap and self in ap.getMVC():
            return ap.get_model()
            
    def GetController(self):
        """
        """
        ap = self.parent.get_active_pattern()
        if ap and self in ap.getMVC():
            return ap.get_controller()
            
    def update(self, msg=None):
        """
        Обновление представления - для элемента в роли представления.
        """
        if self.GetView() == self:
            if not msg:
                msg = parentModule.UpdateViewSignal(self.parent.get_active_pattern())
            self.post_view(msg)
        
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
