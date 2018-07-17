#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Браузер реестров.

Описание ключей спецификации:
    - B{reestrbox=None}: Указатель на портфель реестров, который кодируется строкой
        '<имя подсистемы>:<имя ресурса>'. Внешний редактор атрибута дает список
        ресурсов текущей подсистемы.
    - B{current=None}: Имя текущего реестра.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import ic.kernel.icobject as icobject
import ic.kernel.ickernel as ickernel
import ic.engine.ic_user as ic_user
import ic.PropertyEditor.icDefInf as icDefInf
import STD.interfaces.reestr.browsInterface as ifs

def get_reestr_name_lst():
    """
    Возвращает список имен реестров.
    """
    pth = ic_user.icGet('SYS_RES')
    subsys = ''
    
    if pth:
        lst = pth.replace('\\', '/').split('/')
        if lst[-1] == '':
            subsys = lst[-2]
        else:
            subsys = lst[-1]

    lst = ic_user.get_names_in_res(('mtd',), 'StdReestrBox')
    return ['%s:%s' % (subsys, x) for x in lst]
    
    
### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CTreeReestrBrowser')

ic_class_spc = {'name':'defaultPanel',
                'type':'TreeReestrBrowser',
                'nest':'Unit:ReestrNest',
                'reestrbox':None,
#                'selected':None,
#                'activated':None,
                'current':None,
                '__lists__':{'nest':['Unit:ReestrNest'],
                             'reestrbox':get_reestr_name_lst()},
                '__attr_types__':{icDefInf.EDT_CHOICE:['reestrbox']},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['StdReestrBox']
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'550939069f94910cb95536fc503d0195', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': wx.Point(91, 54), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'cc3882afab2ece7716cb3eba9ea28219', 'proportion': 0, 'name': u'Bszr', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'refresh': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'layout': u'vertical', 'alias': None, 'component_module': None, 'win1': {'activate': 1, 'show': 1, 'recount': None, 'titles': [u'\u0420\u0435\u0435\u0441\u0442\u0440\u044b'], 'refresh': None, 'images': [], 'border': 0, 'size': (-1, -1), 'style': 2186, 'foregroundColor': None, 'span': (1, 1), 'source': None, 'component_module': None, 'proportion': 0, 'colorTo': (240, 240, 236), 'backgroundColor': None, 'type': u'FlatNotebook', 'description': None, '_uuid': u'5cf94741d3b2ba91553ede9301354299', 'moveAfterInTabOrder': u'', 'flag': 0, 'child': [{'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': wx.Size(231, 440), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (255, 255, 255), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'05d0cea928ee96ddcbe15bd8d0147fe7', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': wx.Point(94, 109), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'f11eab7f2a498c9819760431541953bb', 'proportion': 1, 'name': u'TreeBSZR', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'proportion': 1, 'nest': u'None', '_uuid': u'f0b0b5a0df0de71b5e1322b6fde77f91', 'activated': None, 'name': u'TReestrCtrl', 'alias': None, 'flag': 8192, 'init_expr': None, 'type': u'TreeReestrCtrl', 'child': [], 'selected': u'', 'position': (-1, -1), 'titleRoot': u'\u0417\u0430\u0442\u0440\u0430\u0442\u044b', 'border': 0, 'size': (-1, -1)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': wx.Size(100, 440)}], 'name': u'TopLeftPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(123, 103), 'onInit': u''}, {'activate': u'0', 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'e10ffd205f6a0c4e9dc75ad915b5b697', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_1172', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'name': u'BrowserNotebook', 'keyDown': None, 'colorFrom': (240, 240, 236), 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'SplitterWindow', 'description': None, '_uuid': u'8ea3ac26bc45d08464e75625bef77b96', 'style': 768, 'docstr': u'ic.components.icsplitter-module.html', 'flag': 8192, 'recount': None, 'span': (1, 1), 'name': u'browsSplitter', 'min_panelsize': 20, 'keyDown': None, 'win2': {'activate': 1, 'show': 1, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'component_module': None, 'border': 0, 'span': (1, 1), '_uuid': u'205171242df4bafae6f96841cd2fcce8', 'proportion': 1, 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'RegPanel', 'nest': u'BoxSizer:clientRgSizer', '_uuid': u'8f1b563660a0e67bada33e224dcceb5a', 'proportion': 1, 'name': u'RegPanel', 'alias': None, 'flag': 8192, 'foregroundColor': (174, 174, 174), 'init_expr': None, 'backgroundColor': (243, 243, 233), 'child': [], 'position': wx.Point(8, 20), 'border': 0, 'size': (100, 100)}, {'activate': 1, 'show': u'0', 'child': [], 'keyDown': None, 'border': 0, 'size': (0, 0), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'24d9e834537868fdd9c053a104db7690', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'unvisiblePanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'position': (0, 0), 'size': (-1, -1), 'type': u'BoxSizer', 'vgap': 0, 'name': u'DefaultName_1568'}, {'style': 0, 'activate': u'1', 'name': u'ReestrNest', 'component_module': None, '_uuid': u'ad81b87086cf866a814feadaf67f7a91', 'value': None, 'alias': None, 'init_expr': None, 'child': [], 'type': u'Unit', 'description': None}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'1ddcc67a76ce0190484052f928164837', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'defaultWindow_1740', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, 'init_expr': None, 'position': wx.Point(25, 0), 'sash_pos': 200, 'onInit': None}, {'activate': u'0', 'show': 1, 'image_size': (16, 16), 'titles': u"['\u0420\u0435\u0435\u0441\u0442\u0440 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432']", 'keyDown': None, 'images': [], 'border': 0, 'select': None, 'size': (-1, -1), 'onRightMouseClick': None, 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'pageChanged': None, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Notebook', 'description': None, '_uuid': u'beceaa03ec3290140815e09613baea8c', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'child': [{'activate': 1, 'show': 1, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'component_module': None, 'border': 0, 'span': (1, 1), '_uuid': u'f11eab7f2a498c9819760431541953bb', 'proportion': 1, 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'size': (-1, -1), 'border': 0, 'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'activated': None, 'nest': u'None', '_uuid': u'f0b0b5a0df0de71b5e1322b6fde77f91', 'proportion': 1, 'alias': None, 'flag': 8192, 'titleRoot': u'\u0417\u0430\u0442\u0440\u0430\u0442\u044b', 'init_expr': None, 'child': [], 'position': (-1, -1), 'selected': u'', 'type': u'TreeReestrCtrl', 'name': u'TReestrCtrl'}], 'position': wx.Point(94, 109), 'size': wx.Size(100, 440), 'type': u'BoxSizer', 'vgap': 0, 'name': u'TreeBSZR'}], 'keyDown': None, 'border': 0, 'size': wx.Size(231, 440), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (255, 255, 255), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'05d0cea928ee96ddcbe15bd8d0147fe7', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'TopLeftPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(123, 103), 'onInit': u''}], 'name': u'BrowserNotebook_1382', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'mainPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': u''}

#   Версия объекта
__version__ = (1, 1, 5, 1)
###END SPECIAL BLOCK

class CTreeReestrBrowser(ictemplate.icTemplateInterface, ifs.icBrowsReestrInterface):
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        self.reestrbox = component['reestrbox']
        self._reestrbox_obj = None
        self.current = component['current']

        #   Указатель на текущий объект реестра
        self._obj = None
        
        if not self.current:
            self.current = 'fReestrZatrat'
            
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        ifs.icBrowsReestrInterface.__init__(self)
#        res = self.GetObjectResource('TReestrCtrl', 'TreeReestrCtrl')
#        #   Изменение вычисляемых атрибутов должно соправождаться изменением
#        # uuid, т.к. в буфере может остаться компилированное выражение от
#        # другого объекта собранного по данному шаблону
#        res['selected'] = component['selected']
#        res['activated'] = component['activated']
#        res['_uuid'] = uuid.get_uuid()
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource

    def init_component(self, context=None):
        """
        Инициализация компонента. Вызывается парсером после создания компонента.
        """
        if self.reestrbox:
            kernel = self.get_kernel()
            subsys, name = self.reestrbox.split(':')
            pspf = icobject.getResPSP(name+'.mtd', subsys, self.GetInterfaceName())
            self._reestrbox_obj = kernel.Create(pspf)
            print('### CREATE REESTRBOX:', self._reestrbox_obj)
            
            if self.current:
                reestr = self._reestrbox_obj[self.current]
                ifs = self.GetContext().GetInterface('TReestrCtrl')
                print('---> TReestrCtrl=', ifs, reestr)
                ifs.SetReestr(reestr)
            
    def get_kernel(self):
        """
        """
        kernel = ic_user.icGetRunner()
        
        if not kernel:
            kernel = ickernel.icKernel()

        return kernel
        
    def SetRightPanel(self, obj, buff_key=None):
        """
        Устанавливает оконный объект в правую панель браузера.
        
        @type obj: C{wx.Window}
        @param obj: Оокнный компонент, который устанавливается в браузер.
        @param buff_key: Ключ, по которому будет буферизироваться объект.
        """
        ifs = self.GetContext().GetInterface('RegPanel')
        ifs.SetPanel(obj)
        
    def EditObject(self, obj=None):
        """
        Функция выбора объекта реестра.
        
        @param formName: Имя формы.
        @param obj: Указатель на объект реестра (документ ... StdDoc).
        """
        print('TreeBrowser <selectObject>')
        if obj:
            self._obj = obj
        
        #formName = self._obj.GetEditForm()
        if self._obj:
            ifs = self.GetContext().GetInterface('RegPanel')
            ifs.SetEditPanel(self._obj)
            return True
        else:
            return False
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CTreeReestrBrowser.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()