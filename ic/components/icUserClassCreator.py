#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции генерации пользовательских классов.
"""

import os.path
import time
import wx

from ic.utils import resource
import ic.PropertyEditor.icDefInf as icDefInf
import wx.wizard as wiz
from ic.imglib import common
import ic.dlg.msgbox as msg
import ic.utils.ic_res as ic_res
from ic.kernel import io_prnt

_ = wx.GetTranslation

IC_USER_CLASS_DESCR = {'module_name': '',
                       'purpose': '',
                       'author': '',
                       'created': '',
                       'Id': '',
                       'copyright': 'Copyright (c):',
                       'import': None,
                       'parent_class': None,
                       'class_name': None,
                       'icon': 'default.ico',
                       'doc': None,
                       'contain': [],
                       'not_contain': [],
                       'spc_description': None,
                       'spc': None,
                       'styles': None,
                       'init_arg': None,
                       'bind_events': None,
                       'events_function': None,
                       }
    
openTag = '$'
closeTag = '$'


def ReplaceTag(templ, pos, tag, text):
    """
    Заменяет в шаблоне тэг на нужный текст.
    @type templ: C{string}
    @param templ: Шаблона.
    @type pos: C{int}
    @param pos: Позиция, откуда ищется тэг.
    @type tag: C{string}
    @param tag: Имя тэга.
    @type text: C{string}
    @param text: Текст, который вставляется.
    @rtype: C{int}
    @return: Возвращает позицию, в которой найден открывающий тэг
    """
    beg = templ.find(openTag+tag, pos)
    if beg < 0:
        return -1, templ
        
    end = templ.find(closeTag, beg+1)
    if end >= 0:
        templ = templ[:beg]+text+templ[end+1:]
    else:
        templ = templ[:beg]+text
    
    return beg, templ


def findOpenTag(templ, pos):
    """
    Возвращает имя первого отрывающего тэга с определнной позиции.
    """
    beg = templ.find(openTag, pos)
    if beg < 0:
        return -1, None
        
    n2 = templ.find(':', beg+1)
    if n2 < 0:
        return beg, None
        
    name = templ[beg+1: n2]
    return beg, name


def CreatUserClass(discr, file_templ=None):
    """
    По описанию генерируется модуль с пользовательским классом.
    @type discr: C{dictionary}
    @param discr: Структура описания класса пользователя.
    @type file_templ: C{string}
    @param file_templ: Имя файла шаблона.
    """
    if not file_templ:
        file_templ = resource.icGetICPath() + '/components/templates/icuserclass.tpl'

    #   Читаем текст шаблона
    f = open(file_templ, 'rb')
    templ = unicode(f.read().replace('\r\n', '\n'), 'utf-8')
    f.close()
    
    dct = IC_USER_CLASS_DESCR
    lst = discr.keys()
    cur = 0
    i = 0
    while cur >= 0:
        cur, name = findOpenTag(templ, cur)
        i += 1
        #   Регистрация событий
        if cur >= 0 and name and name == 'bind_events':
            text = ''
            ot = ' ' * 8
            if '__events__' in discr['spc'] and isinstance(discr['spc']['__events__'], dict):
                for attr, val in discr['spc']['__events__'].items():
                    tp, func, id = val
                    if not func:
                        func = 'On_' + attr
                    if id:
                        text += ot + 'self.Bind(%s, self.%s, id=id)' % (tp, func)+'\n'
                    else:
                        text += ot + 'self.Bind(%s, self.%s)' % (tp, func) + '\n'
                    
                text = '\n'+text
            cur, templ = ReplaceTag(templ, cur, name, text)
        
        #   Создаем обработчики событий
        elif cur >= 0 and name and name == 'events_function':
            text = ''
            ot = 4*' '
            if '__events__' in discr['spc'] and isinstance(discr['spc']['__events__'], dict):
                for attr, val in discr['spc']['__events__'].items():
                    tp, func, id = val
                    if not func:
                        func = 'On_' + attr
                    text += ot + 'def %s(self, evt):' % func + '\n'
                    text += ot + u'    """Event %s, attribute=%s"""' % (tp, attr) + '\n'
                    text += ot + '    self.evalSpace[\'evt\'] = evt\n'
                    text += ot + '    self.evalSpace[\'self\'] = self\n'
                    text += ot + '    ret, val = self.eval_attr(\'%s\')' % attr + '\n'
                    text += ot + '    if ret and val:\n'
                    text += ot + '        evt.Skip()\n'
                    text += ot + '    elif not ret:\n'
                    text += ot + '        evt.Skip()\n\n'
                    
                text = '\n'+text
            cur, templ = ReplaceTag(templ, cur, name, text)
                              
        elif cur >= 0 and name and name == 'created':
            cur, templ = ReplaceTag(templ, cur, name, str(discr[name])+time.ctime())
        elif cur >= 0 and name and name == 'spc_description':
            text = ''
            ot = ' '*8
            for attr, val in discr['spc'].items():
                if attr.find('__') != 0:
                    if isinstance(val, str):
                        text += ot + '- B{%s=\'%s\'}:\n' % (attr, str(val))
                    else:
                        text += ot + '- B{%s=%s}:\n' % (attr, str(val))
            text = '\n'+text
            cur, templ = ReplaceTag(templ, cur, name, text)
        elif cur >= 0 and name and name in lst and name == 'spc':
            spc_txt = str(discr[name]).replace('\'icwidget.SPC_IC_WIDGET\'', 'icwidget.SPC_IC_WIDGET')
            cur, templ = ReplaceTag(templ, cur, name, spc_txt)
        elif cur >= 0 and name and name in lst:
            cur, templ = ReplaceTag(templ, cur, name, discr[name] or '')
        elif cur >= 0:
            cur += 1
    return templ


# ----------------------------------------------------------------------
#   Wizard
def makePageTitle(wizPg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND | wx.ALL, 5)
    return sizer


def makePageTitle2(wizPg, title):
    sizer = wx.GridBagSizer(5, 5)
    sizer.SetEmptyCellSize((20, 20))
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, (0, 0), (1, 3), 1, wx.ALIGN_CENTER_HORIZONTAL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1, size=(300, 1)), (1, 0), (1, 3), 0, wx.EXPAND | wx.ALL, 5)
    return sizer


class TitledPage(wiz.WizardPageSimple):

    def __init__(self, parent, title):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle2(self, title)
        self._row = 3


def makeFirstPage(wizPg, title):
    """
    Первая страница.
    """
    import ic.components.user.objects.icfirstwizpage as pagemod
    obj = pagemod.icFirstPage(wizPg)
    sizer = obj.getObject()
    return sizer


def makeAttrPage(wizPg, title):
    """
    Страница со списком атрибутов спецификации.
    """
    import ic.components.user.objects.icinpclsattrwizpage as attrGrid
    obj = attrGrid.icInputAttrClass(wizPg)
    sizer = obj.getObject()
    grid = obj.GetNameObj('AttrGrid')
    grid.AddRows(2)
    grid.setNameValue('name', 'name', 0)
    grid.setNameValue('type', 'EDT_TEXTFIELD', 0)
    grid.setNameValue('defaultVal', 'default', 0)
    grid.Update(0)
    grid.setNameValue('name', 'type', 1)
    grid.setNameValue('type', 'EDT_TEXTFIELD', 1)
    grid.setNameValue('defaultVal', 'defaultType', 1)
    grid.Update(1)
   
    # Чистим буфер
    grid.GetDataset().clearChangeRowBuff(-1)
    grid.SetFocus()
    return sizer


def makeMsgPage(wizPg, title):
    """
    Страница описания обработчиков событий компонента.
    """
    import ic.components.user.objects.icmsgwizpage as pagemod
    obj = pagemod.icInputMsgAttrClass(wizPg)
    sizer = obj.getObject()
    return sizer


def makeEditModulPage(wizPg, title):
    """
    Страница редактирования текста компонента.
    """
    import ic.components.user.objects.iceditorwizpage as pagemod
    obj = pagemod.icEditModulClass(wizPg)
    sizer = obj.getObject()
    return sizer


class FirstPage(wiz.PyWizardPage):

    def __init__(self, parent, title):
        wiz.PyWizardPage.__init__(self, parent)
        self.sizer = makeFirstPage(self, title)
        self.next = self.prev = None

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev


class AttrPage(wiz.PyWizardPage):

    def __init__(self, parent, title):
        wiz.PyWizardPage.__init__(self, parent)
        self.sizer = makeAttrPage(self, title)
        self.next = self.prev = None

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev


class MsgPage(wiz.PyWizardPage):

    def __init__(self, parent, title):
        wiz.PyWizardPage.__init__(self, parent)
        self.sizer = makeMsgPage(self, title)
        self.next = self.prev = None

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        first = self.GetPrev().GetPrev()
        dct = first.sizer.evalSpace['_dict_obj']
        text = self.GenerateModText()
        self.next.editor.SetText(text)
        self.next.modulName.SetLabel(dct['TextModulName'].GetValue())
        return self.next

    def GetPrev(self):
        return self.prev

    def GenerateModText(self):
        """
        Генерирует текст модуля.
        """
        first = self.GetPrev().GetPrev()
        dct = first.sizer.evalSpace['_dict_obj']
        spc = {}
        spc['__events__'] = {}
        spc['__attr_types__'] = {}
        spc['__parent__'] = 'icwidget.SPC_IC_WIDGET'
        
        #   Читаем атрибуты пользовательского класса
        attrGrid = self.GetPrev().sizer.evalSpace['_dict_obj']['AttrGrid']
        lr = attrGrid.GetDataset().getRecordCount()
        
        for row in range(lr):
            key = attrGrid.getNameValue('name', row)
            typ = attrGrid.getNameValue('type', row)
            val = attrGrid.getNameValue('defaultVal', row)
            spc[key] = value = icDefInf.strToVal(typ, val)
            
            try:
                id_type = getattr(icDefInf, typ)
                if id_type in spc['__attr_types__']:
                    spc['__attr_types__'][id_type].append(key)
                else:
                    spc['__attr_types__'][id_type] = [key]
            except:
                io_prnt.outLastErr(u'Set Attribute Type')
                
        #   Читаем атрибуты обработчиков сообщений
        msgGrid = self.sizer.evalSpace['_dict_obj']['MsgGrid']
        lr = msgGrid.GetDataset().getRecordCount()
        
        for row in range(lr):
            key = msgGrid.getNameValue('name', row)
            typ = msgGrid.getNameValue('type', row)
            func = msgGrid.getNameValue('function', row)
            prz = msgGrid.getNameValue('przCommand', row)
            
            if not func:
                func = None
                
            spc['__events__'][key] = (typ, func, prz)
            if icDefInf.EDT_PY_SCRIPT in spc['__attr_types__']:
                spc['__attr_types__'][icDefInf.EDT_PY_SCRIPT].append(key)
            else:
                spc['__attr_types__'][icDefInf.EDT_PY_SCRIPT] = [key]
                
            spc[key] = None

        #   Если установлен признак контейнера
        if self.GetPrev().sizer.evalSpace['_dict_obj']['przContainer'].IsChecked():
            spc['child'] = []
            
        discr = {'module_name': dct['TextModulName'].GetValue(),
                 'class_name': dct['TextClassName'].GetValue(),
                 'purpose': dct['TextDiscr'].GetValue(),
                 'author': dct['TextAuthor'].GetValue(),
                 'created': 'class:',
                 'Id': '',
                 'copyright': dct['TextCopyright'].GetValue(),
                 'import': dct['TextParentModule'].GetValue(),
                 'parent_class': dct['TextParentClass'].GetValue(),
                 'icon': dct['TextIcon'].GetValue(),
                 'doc': '\'%s\'' % dct['TextDoc'].GetValue(),
                 'contain': '[]',
                 'not_contain': 'None',
                 'spc_description': None,
                 'spc': spc,
                 'styles': '{\'DEFAULT\':0}',
                 'init_arg': '*args, **kwargs',
                 'bind_events': None,
                 'events_function': None}
        
        text_mod = CreatUserClass(discr)
        return text_mod


class EditModulPage(wiz.PyWizardPage):

    def __init__(self, parent, title):
        wiz.PyWizardPage.__init__(self, parent)
        self.sizer = makeEditModulPage(self, title)
        self.editor = self.sizer.evalSpace['_dict_obj']['Editor']
        self.modulName = self.sizer.evalSpace['_dict_obj']['ModulName']
        self.next = self.prev = None

    def SetEditText(self, text):
        self.editor.SetText(text)

    def SetModulName(self):
        pass

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev


def createMainPropPage(page):
    """
    Создает страницу с основными параметрами, по котороым генерирутся
    пользовательский класс.
    """
    page.sizer.Add(wx.StaticText(page, -1, _('Component description property.')), (2, 0), (1, 3))
    addStrProperty2(page, _('Module name:'), 'user.py')
    addStrProperty2(page, _('Class name:'), 'urUserClass')
    addStrProperty2(page, _('Purpose:'), 'User component class')
    addStrProperty2(page, _('Author:'), 'User name')
    addStrProperty2(page, _('Copyrights:'), '(c) ')
    addStrProperty2(page, _('Parent module name:'), 'wx')
    addStrProperty2(page, _('Parent class name:'), 'Button')
    addStrProperty2(page, _('Icon path:'), 'images/classpic.png')
    addStrProperty2(page, _('Doc file path (*.html):'), 'doc/public/user/user.html')


def RunWizard(parent):
    """
    Create the wizard and the pages.
    """
    wizard = wiz.Wizard(parent, -1, _('Create Component Wizard'), common.imgUserCompWizard)
    page1 = FirstPage(wizard, _('Base parameters'))
    page2 = AttrPage(wizard, _('Class attributes'))
    page3 = MsgPage(wizard, _('Event attributes'))
    page4 = EditModulPage(wizard, _('Edit module'))
    parent.page1 = page1
    wizard.FitToPage(page1)
    
    page1.SetNext(page2)
    page2.SetPrev(page1)
    page2.SetNext(page3)
    page3.SetPrev(page2)
    page3.SetNext(page4)
    page4.SetPrev(page3)
    
    if wizard.RunWizard(page1):
        #   Сохраняем модуль в библиотеке пользовательских компонентов
        txt = page4.editor.GetText()
        
        if resource.icGetResPath():
            user_mod_dir = resource.icGetResPath()+'/usercomponents'
        else:
            user_mod_dir = None
        
        if not user_mod_dir:
            module_name = resource.icGetICPath() + '/components/user/' + page4.modulName.GetLabel()
        elif not os.path.isdir(user_mod_dir):
            # Создаем пакет
            ic_res.CreatePackage(user_mod_dir)
            module_name = user_mod_dir + '/' + page4.modulName.GetLabel()
        else:
            module_name = user_mod_dir + '/' + page4.modulName.GetLabel()
            
        bCr = wx.ID_YES
        
        if os.path.isfile(module_name):
            bCr = msg.MsgBox(None, _('Module %s already exist. Rewrite?') % module_name,
                             style=wx.YES_NO | wx.NO_DEFAULT)

        if bCr == wx.ID_YES:
            f = open(module_name, 'w')
            io_prnt.outLog(u'CREATE MODULE: <%s>' % module_name)
            f.write(txt.encode('utf-8'))
            f.close()
            wx.MessageBox(_('Module %s is created.') % module_name, '')
    else:
        wx.MessageBox(_('Wizard was cancelled'), u'')

# ----------------------------------------------------------------------


def test(par=0):
    """
    Тестируем пользовательский класс.
    @type par: C{int}
    @param par: Тип консоли.
    """
    import ic.components.ictestapp as ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    frame.Show(True)
    RunWizard(win)
    app.MainLoop()


def testGenUserClass():
    """
    Тестируем генерацию пользовательского класса.
    """
    spc = {'type': 'urButton',
           'name': 'Default',
           'style': 0,
           'label': 'Label',
           'size': (100, -1),
           'position': (-1, -1),
           'image': None,
           'backgroundColor': None,
           'foregroundColor': None,
           'onButton': None,
           'onLeftDown': 'True',
           'onLeftUp': None,
           '__version__': (0, 0, 0, 1),
           '__events__': {'onButton': ('wx.EVT_BUTTON', None, 1),
                          'onLeftDown': ('wx.EVT_LEFT_DOWN', 'OnLeft_DWN', None),
                          'onLeftUp': ('wx.EVT_LEFT_UP', 'OnLeft_Up', None)},
           '__attr_types__': {icDefInf.EDT_PY_SCRIPT: ['onButton', 'onLeftDown', 'onLeftUp'],
                              icDefInf.EDT_TEXTFIELD: ['label'],
                              icDefInf.EDT_COLOR: ['foregroundColor', 'backgroundColor']}}
                
    st = {'BU_LEFT': wx.BU_LEFT,
          'BU_TOP': wx.BU_TOP,
          'BU_RIGHT': wx.BU_RIGHT,
          'BU_BOTTOM': wx.BU_BOTTOM,
          'BU_EXACTFIT': wx.BU_EXACTFIT}
        
    discr = {'module_name': 'urstateindicator.py',
             'purpose': 'Indicator',
             'author': 'Author',
             'created': 'resource: 14.09.2004, class:',
             'Id': '',
             'copyright': '(c) 2004 Company',
             'import': 'wx.lib.buttons',
             'parent_class': 'GenBitmapTextButton',
             'class_name': 'StateIndicator',
             'icon': None,
             'doc': None,
             'contain': [],
             'not_contain': None,
             'spc_description': None,
             'spc': spc,
             'styles': st,
             'init_arg': '*args, **kwargs',
             'bind_events': None,
             'events_function': None}
    
    CreatUserClass(discr)


if __name__ == '__main__':
    test()
