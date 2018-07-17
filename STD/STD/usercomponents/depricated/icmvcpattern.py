#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<< Типовой шаблон пользовательского компонента >>

"""
MVC паттерн.
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
from ic.utils import coderror

from STD import reestr_img

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMVCPattern'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {},
                'type': 'MVCPattern',
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
ic_class_pic = reestr_img.mvcPattern
ic_class_pic2 = reestr_img.mvcPattern

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
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    if attr in ('model','view','controller'):
        parent = propEdt.GetPropertyGrid().GetView()
        #lst = icmvcelement.findObjLst(propEdt.GetPrntResource(), 'MVCElement')
        lst = icmvcelement.findClassLst(propEdt.GetPrntResource(), parentModule.ic_mvc_element, propEdt.GetResTree().GetObjectsInfo())
        if lst:
            dlg = baseeditor.ChoiceMenu(parent, lst)
            parent.PopupMenu(dlg, pos)
        
            #   Возвращаем выбранный элемент списка
            if lst and dlg.IsSelString():
                value = dlg.GetSelString()
            
            dlg.Destroy()
            return value
        else:
            msgbox.MsgBox(parent, u'Базисные элементы паттернов не определены')

def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('model','view','controller'):
        res = propEdt.GetResource()
        parent = propEdt.GetPropertyGrid().GetView()
        prnt_res = propEdt.GetPrntResource()
        lst = icmvcelement.findClassLst(propEdt.GetPrntResource(), parentModule.ic_mvc_element, propEdt.GetResTree().GetObjectsInfo())
        rlst = icmvcelement.findClassResLst(prnt_res, parentModule.ic_mvc_element, propEdt.GetResTree().GetObjectsInfo())
            
        if attr == 'view' and value in lst:
            #lst = icmvcelement.findClassResLst(prnt_res, parentModule.ic_mvc_element, propEdt.GetResTree().GetObjectsInfo())
            v_res = None
            # находим ресурс представления
            for r in rlst:
                if value == r['name']:
                    v_res = r
                    break
            # находим ресурс контроллера и проверяем
            for r in rlst:
                if r['name'] == res['controller']:
                    if r['socket_in'] == v_res['socket_out']:
                        return coderror.IC_CTRL_OK
                    else:
                        msgbox.MsgBox(parent, """Выходной интерфейс <%s>
представления <%s>
не совпадает с входным интерфесом <%s>
контроллера <%s>""" % (v_res['socket_out'], v_res['name'], r['socket_in'], r['name']))
                        return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif attr == 'controller' and value in lst:
            #lst = icmvcelement.findClassResLst(prnt_res, parentModule.ic_mvc_element, propEdt.GetResTree().GetObjectsInfo())
            #print '... controller'
            ctrl_res = None
            # находим ресурс контроллера
            for r in rlst:
                if value == r['name']:
                    ctrl_res = r
                    break
                    
            for r in rlst:
                if r['name'] == res['view']:
                    if r['socket_out'] == ctrl_res['socket_in']:
                        return coderror.IC_CTRL_OK
                    else:
                        msgbox.MsgBox(parent, """Входной интерфейс <%s>
контроллера <%s>
не совпадает с выходным интерфесом <%s>
представления <%s>""" % (ctrl_res['socket_in'], ctrl_res['name'], r['socket_out'], r['name']))
                        return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif value in lst:
            return coderror.IC_CTRL_OK

def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('model','view','controller'):
        return text
        
class icMVCPattern(icwidget.icSimple, parentModule.ic_mvc_pattern):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='MVCPattern'}:
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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') <> 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.ic_mvc_pattern.__init__(self, self.name)
        
        #   Регистрация обработчиков событий

        #self.BindICEvt()
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
        if self.model and self.view and self.controller:
            self.setp(self.parent.components[self.model],
                    self.parent.components[self.view],
                    self.parent.components[self.controller])
                
    def bind_wx_messages(self, wx_view=None):
        """
        Функция регистрации сообщений от представлений для контроллеров.
        
        @type wx_view: C{wx.Window}
        @param wx_view: Представление, которое генерит wx сообщения.
        """
        m, v, c = self.getMVC()
        if not wx_view:
            wx_view = v.get_agr_object()
        
        # Получаем паспорт входного интерфейса контроллера
        psp = c.socket_in
        
        if psp and wx_view:
            # Создаем интерфейс - компонент WX_Binder
            ifs = c.GetContext().get_kernel().Create(psp)
            # Отбирем все сообщения, относящиеся к ресурсу представления.
            vpsp = wx_view.GetPassport()
            evt_lst = []
            rn = vpsp.getDescrMod()
            subsys = vpsp.getDescrSubsys()
            
            for obj in ifs.GetContext().GetObject(psp[0][1]).components.values():
                if obj.type == 'WX_SignalType' and obj.src:
                    obj_rn = obj.src[0][3]
                    obj_subsys = obj.src[0][4]
                    
                    if (subsys and obj_subsys and (rn == obj_rn) and subsys==obj_subsys) or (rn == obj_rn):
                        evt_id = obj.getEvtId()
                        
                        if obj.src:
                            bindCtrl = wx_view.GetContext().FindObjByPsp(obj.src)
                            if bindCtrl and obj.function:
                                bindCtrl.Bind(evt_id, getattr(c, obj.function))
                                print('... >> Bind evt=', bindCtrl.name, c.name, obj.lib, evt_id, obj.function)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace = self.evalSpace,
                                bCounter = bCounter, progressDlg = progressDlg)
      
    #   Обработчики событий
    def do_activate(self, par=None):
        """
        """
        #print '... pattern_activate!!!!!'
        self.evalSpace['self'] = self
        self.eval_attr('pattern_activate')
        
        #   Контроллеру посылается сообщение о том, что паттерн
        #   активирован
        msg = parentModule.PatternActivateSignal(self)
        self.get_controller().post_controller(msg)
        self.get_model().post_model(msg)
        self.get_view().post_view(msg)
        
    def do_deactivate(self, *arg, **kwarg):
        """
        """
        self.evalSpace['self'] = self
        #self.evalSpace['evt'] = evt
        self.eval_attr('pattern_deactivate')
        
    def get_model(self):
        """
        """
        if self.model in self.parent.components:
            return self.parent.components[self.model]
        
    def get_view(self):
        """
        """
        if self.view in self.parent.components:
            return self.parent.components[self.view]
    
    def get_controller(self):
        """
        """
        if self.controller in self.parent.components:
            return self.parent.components[self.controller]
    
    def get_parent_pattern(self):
        """
        Возвращет родительский паттерн.
        """
        if self.parent and self.parent.parent:
            self.parent.parent.get_active_pattern()
        
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
