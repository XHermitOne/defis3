#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Содержит классы редакторов свойств.

Идентификаторы типов редакторов.
    
    - B{EDT_TEXTFIELD}: Редактор текста.
    - B{EDT_NUMBER}: Редактор числовых значений (int | float).
    - B{EDT_TEXTLIST}: Редактор списка в синтаксисе Python. Пример: ['1', 2, 'abc'].
    - B{EDT_TEXTDICT}: Редактор словаря в синтаксисе Python. Пример: {'1':2, 'abc':3}.
    - B{EDT_DICT}: Редактор словаря.
    - B{EDT_IMPORT_NAMES}: Редактор словаря импортируемых имен. Пример: {'ic':['db','iccomponents'], 'wxPython':['wx']}.
    - B{EDT_CHOICE} Редактор свойств через wxChoice.
    - B{EDT_CHECK_BOX} Редактор свойств через wxCheckBox.
    - B{EDT_EXTERNAL}: Редактор текста с возможностью выбора внешнего редактор (по нажатию на кнопку).
    - B{EDT_COMBINE}: Редактор комбинированных свойств (например, стили wxWindow: wxSIMPLE_BORDER | wxNO_3D).
    - B{EDT_COLOR}: Редактор цветов wxColour.
    - B{EDT_FONT}: Редактор шрифтов wxFont.
    - B{EDT_POINT}: Редактор координат точки wxPoint.
    - B{EDT_SIZE}: Редактор параметров размеров wxSize.
    - B{EDT_PY_SCRIPT}: Редактор Python скриптов.
    - B{EDT_ADD_PROPERTY}: Редактор дополнительных свойств.
    - B{EDT_NEW_PROPERTY}: Редактор для добавления дополнительного свойства.
"""

import wx
# import ic
from ic.components.icfont import *
# from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
import os
import sys
import ic.PropertyEditor.ic_pyed as ic_pyed
import types
# from ic.icEditor.CfgMthDialog import MthDialog
from ic.components.icwidget import icEvent
from ic.utils.util import icSpcDefStruct
import ic.components.icwidget as icwidget
from . import icDefInf
from ic.log import log

# Признак, что атрибут описывает дополнительное свойство.
icAddPropertyPrzn = ''

# Ключи для описания шрифта
icEdtFontKeys = ('size', 'family', 'faceName', 'style', 'underline')

# Идентификаторы типов представлений названий свойств.
icNameTypeNormal = 0
icNameTypeCheckBox = 1
icNameTypeReadonly = 2
icNameTypeAddPropery = 3

class icEditPropCtrl(icEvent):
    """
    Интерфейс для компонентов, которые редактируют свойства в редакторе свойств.
    """

    def __init__(self, nameValue):
        """
        Конструктор.
        """
        icEvent.__init__(self)
        self.nameValue = nameValue
        self.propEditor = nameValue.dict
        self.editorCtrl = None
        self.wID = icwidget.icNewId()
        self.value = nameValue.value

    def SetFocus(self):
        if self.editorCtrl: self.editorCtrl.SetFocus()

    def Destroy(self):
        """
        Close an open editor control
        """
        if self.editorCtrl:
            self.editorCtrl.Destroy()
            self.editorCtrl = None

    def GetValue(self):
        """
        Read value from editor control
        """
        val = self.value
        
        if self.editorCtrl:
            try:
                val = self.editorCtrl.GetValue()
            except:
                pass
            
        return val

    def SetValue(self, value):
        """
        Write value to editor control
        """
        self.value = value
        
        if self.editorCtrl:
            try:
                self.editorCtrl.SetValue(value)
            except:
                pass

    def SetSize(self, (width, height)):
        if self.editorCtrl:
            self.editorCtrl.SetSize(wx.Size(width-1, height))

    def Refresh(self, par):
        if self.editorCtrl:
            self.editorCtrl.Refresh(par)
            
    def OnSelect(self, event):
        pass


class icEditPropText(icEditPropCtrl):
    """
    Класс редактирования текстовых свойств.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        
        self.nameValue = nameValue
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)


class icEditPropNumber(icEditPropCtrl):
    """
    Класс редактора числовых значений (int | float).
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        
        self.nameValue = nameValue
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)

    def GetValue(self):
        """
        Read value from editor control
        """
        try:
            val = eval(self.editorCtrl.GetValue())
                
            if isinstance(val, int) and not isinstance(val, float):
                val = self.value
                MsgBox(None, u'Несоответствие типа <%s>' % self.editorCtrl.GetValue())
        except:
            val = self.value
            MsgBox(None, u'Ошибка ввода <%s>' % self.editorCtrl.GetValue())
            
        return val


class icEditPropTextList(icEditPropCtrl):
    """
    Класс редактирования списка.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        self.nameValue = nameValue
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)

    def GetValue(self):
        """
        Read value from editor control
        """
        try:
            val = eval(self.editorCtrl.GetValue())
                
            if isinstance(val, list) and not isinstance(val, tuple):
                val = self.value
                MsgBox(None, u'Несоответствие типа <%s>'  % self.editorCtrl.GetValue())
        except:
            val = self.value
            MsgBox(None, u'Ошибка ввода <%s>' % self.editorCtrl.GetValue())
        return val


class icEditPropTextDict(icEditPropCtrl):
    """
    Класс редактирования списка.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        self.nameValue = nameValue
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)

    def GetValue(self):
        """
        Read value from editor control
        """
        try:
            val = eval(self.editorCtrl.GetValue())
                
            if not isinstance(val, dict):
                val = self.value
                MsgBox(None, u'Несоответствие типа <%s>' % self.editorCtrl.GetValue())
        except:
            val = self.value
            MsgBox(None, u'Ошибка ввода <%s>' % self.editorCtrl.GetValue())
        return val


class icEditPropPoint(icEditPropCtrl):
    """
    Класс редактирования текстовых свойств.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        self.nameValue = nameValue
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)

    def GetValue(self):
        try:
            ret = eval(str(self.editorCtrl.GetValue()))
            
            if (type(ret) != type(wx.Point(0, 0)) and not isinstance(ret, tuple)) or \
                    (isinstance(ret, tuple) and len(ret) != 2):
                ret = self.value
                MsgBox(None, u'Несоответствие типа <%s>' % self.editorCtrl.GetValue())
            else:
                ret = (ret[0], ret[1])
        except:
            ret = self.value
            MsgBox(None, u'Ошибка ввода <%s>' % self.editorCtrl.GetValue())
        return ret


class icEditPropSize(icEditPropCtrl):
    """
    Класс редактирования размеров объекта.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция расположения редактора.
        @type size: C{wx.Size}
        @param size: Размеры редактора.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        self.nameValue = nameValue
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)
    
    def GetValue(self):
        try:
            ret = eval(str(self.editorCtrl.GetValue()))
            
            if (type(ret) != type(wx.Size(0, 0)) and not isinstance(ret, tuple)) or \
                    (isinstance(ret, tuple) and len(ret) != 2 ):
                ret = self.value
                MsgBox(None, u'Несоответствие типа <%s>' + self.editorCtrl.GetValue())
            else:
                ret = (ret[0], ret[1])
        except:
            ret = self.value
            MsgBox(None, u'Ошибка ввода <%s>' % self.editorCtrl.GetValue())
        return ret


class icEditPropCombine(icEditPropCtrl):
    """
    Класс редактирования комбинированных свойств.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        self.nameValue = nameValue
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)
            
    def GetValue(self):
        """
        """
        ret = self.nameValue.oldValue
        keys = self.editorCtrl.GetValue().replace(' ', '').split('|')
        
        for key in self.nameValue.oldValue.keys():
            if key in keys:
                ret[key] = 1
            else:
                ret[key] = 0
        return ret
    
    def Expand(self):
        """
        Функция сворачивает список комбинированных свойств.
        """
        if not self.nameValue.name_ctrl.IsChecked():
            self.editorCtrl.Enable(False)
            self.nameValue.SetEnableEditor(False)
            indx = self.nameValue.GetIndx() + 1

            if isinstance(self.nameValue.oldValue, dict):
                for key in self.nameValue.oldValue.keys():
                    self.nameValue.main.InsNameValues(indx, '  '+key, self.nameValue.oldValue[key],
                                                      icDefInf.EDT_CHECK_BOX, bRefresh=False)
                    indx += 1
        else:
            indx = self.nameValue.GetIndx() + 1
            
            if isinstance(self.nameValue.oldValue, dict):
                self.editorCtrl.Enable(True)
                self.nameValue.SetEnableEditor(True)
                
                # Определяем новое значение основного поля и удаляем объекты редактора.
                for key in self.nameValue.oldValue.keys():
                    if isinstance(self.nameValue.oldValue[key], int):
                        self.nameValue.oldValue[key] = int(self.nameValue.main.NameValues[indx].value)
                    else:
                        self.nameValue.oldValue[key] = self.nameValue.main.NameValues[indx].value

                    self.nameValue.main.RemoveIndx(indx)
                    
            self.nameValue.value = self.nameValue.oldValue
            self.nameValue.value_ctrl.SetLabel(self.nameValue.GetStr())
            self.SetValue(self.nameValue.GetStr())
            
        self.nameValue.main.RefreshPos()
        self.nameValue.main.refreshSplitter()
        
    def OnExpand(self, evt):
        """
        Функция запускается при выборе CheckBox в строке свойств.
        """
        self.Expand()
        evt.Skip()


class icEditPropDict(icEditPropCtrl):
    """
    Класс редактирования значений словаря.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        self.nameValue = nameValue
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)
                        
    def GetValue(self):
        """
        """
        try:
            ret = eval(self.editorCtrl.GetValue())
            
            if isinstance(ret, dict):
                ret = self.value
                MsgBox(None, u'Несоответствие типа <%s>' % self.editorCtrl.GetValue())
        except:
            ret = self.value
            MsgBox(None, u'Ошибка ввода <%s>' % self.editorCtrl.GetValue())
        return ret
    
    def Expand(self):
        """
        Функция сворачивает список комбинированных свойств.
        """
        if not self.nameValue.name_ctrl.IsChecked():
            self.editorCtrl.Enable(False)
            self.nameValue.SetEnableEditor(False)
            indx = self.nameValue.GetIndx() + 1

            if isinstance(self.nameValue.value, dict):
                for key in self.nameValue.value.keys():
                    val = self.nameValue.value[key]

                    if isinstance(val, int) or isinstance(val, float):
                        self.nameValue.main.InsNameValues(indx, '  '+key, val, icDefInf.EDT_NUMBER, bRefresh=False)
                    elif isinstance(val, dict):
                        self.nameValue.main.InsNameValues(indx, '  '+key, val, icDefInf.EDT_TEXTDICT, bRefresh=False)
                    elif isinstance(val, list) or isinstance(val, tuple):
                        self.nameValue.main.InsNameValues(indx, '  '+key, val, icDefInf.EDT_TEXTLIST, bRefresh=False)
                    else:
                        self.nameValue.main.InsNameValues(indx, '  '+key, val, bRefresh=False)
                        
                    indx += 1
        else:
            indx = self.nameValue.GetIndx() + 1
            
            if isinstance(self.nameValue.value, dict):
                self.editorCtrl.Enable(True)
                self.nameValue.SetEnableEditor(True)
                
                # Определяем новое значение основного поля и удаляем объекты редактора.
                for key in self.nameValue.value.keys():
                        
                    self.nameValue.value[key] = self.nameValue.main.NameValues[indx].value
                    self.nameValue.main.RemoveIndx(indx)
                    
            self.nameValue.value_ctrl.SetLabel(self.nameValue.GetStr())
            self.SetValue(self.nameValue.GetStr())
            
        self.nameValue.main.RefreshPos()
        self.nameValue.main.refreshSplitter()
        
    def OnExpand(self, evt):
        """
        Функция запускается при выборе CheckBox в строке свойств.
        """
        self.Expand()
        evt.Skip()

    def AddProp(self):
        """
        """
        pass
    
    def DelProp(self, indx):
        """
        """
        pass


class icEditImportNames(icEditPropDict):
    """
    Класс редактирования словаря импортируемых имен.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        icEditPropDict.__init__(self, nameValue, pos, size, style)
        
    def OnExpand(self, evt):
        """
        Функция запускается при выборе CheckBox в строке свойств.
        """
        self.Expand()
        
        if not self.nameValue.name_ctrl.IsChecked():
            indx = self.nameValue.GetIndx() + 1
            last_indx = indx + len(self.nameValue.value.keys())
                
            for i in range(indx, last_indx):
                nm = self.nameValue.main.NameValues[i]
                nm.name_ctrl.Bind(wx.EVT_LEFT_DCLICK, self.OnDblClick)
                
                if indx > last_indx:
                    break
        
        evt.Skip()
        
    def OnDblClick(self, evt):
        """
        Обрабатывает двойной щелчок мыши на редакторе импортируемых имен.
        """
        ctrl = evt.GetEventObject()
        
        dirs = [os.getcwd()] + sys.path
        fname = os.sep + ctrl.GetLabel().replace(' ', '').replace('.', os.sep)+'.py'
        txt = None
        fn = None
        
        for _path in dirs:
            fn = _path + fname

            if os.path.exists(fn):
                f = open(fn)
                txt = f.read()
                f.close()
                break
            
        if txt is None:
            if MsgBox(None, u'Модуль <%s> не найден. Хотите создать новый модуль?' % fname,
                      style=wx.YES_NO | wx.NO_DEFAULT) == wx.ID_YES:
                txt = ''
        
        if txt is not None:
            frame = icPyEditorFrame(None, {'name': 'editor', 'type': 'PyEditor',
                                           'position': (50, 50), 'size': (500, 500)}, txt)
            frame.editor.SetModuleName(fn)
            frame.Show()
            frame.SetTitle(u'Редактор (%s)' % fn)


class icEditPropChoice(icEditPropCtrl):
    """
    Класс редактирования свойств через wx.Choice.
    """
    
    def __init__(self, nameValue, pos, size, style=0):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        icEditPropCtrl.__init__(self, nameValue)
        indx = -1
        
        try:
            mchoice = nameValue.dict['choices']
            
            for el in mchoice:
                indx += 1
                
                if el == str(nameValue.value):
                    break
        except:
            mchoice = []
                    
        self.editorCtrl = wx.Choice(nameValue.main.panel2, self.wID,
                                    pos=pos, size=size, choices = mchoice, style=style)
        
        if indx >= 0:
            self.editorCtrl.SetSelection(indx)
        else:
            self.editorCtrl.SetSelection(0)

    def GetValue(self):
        """
        """
        indx = self.editorCtrl.GetSelection()
        return self.nameValue.dict['choices'][indx]


class icEditPropCheckBox(icEditPropCtrl):
    """
    Класс редактирования свойств через wx.CheckBox.
    """
    
    def __init__(self, nameValue, pos, size, style=0):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента.
        """
        if int(nameValue.value) <= 0:
            label = 'False'
            value = 0
        else:
            label = 'True'
            value = 1
                
        icEditPropCtrl.__init__(self, nameValue)
        self.editorCtrl = wx.Window(nameValue.main.panel2, icwidget.icNewId(),
                                    pos=pos, size=size, style=wx.WANTS_CHARS)
        self.checkBox = wx.CheckBox(self.editorCtrl, self.wID, label, pos=(2, 1))

        self.checkBox.SetValue(value)
        self.editorCtrl.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, id=self.wID)
        self.editorCtrl.SetFocus()
        
    def OnCheckBox(self, evt):
        
        if self.GetValue():
            self.value = 0
            self.checkBox.SetValue(0)
            self.checkBox.SetLabel('False')
        else:
            self.value = 1
            self.checkBox.SetValue(1)
            self.checkBox.SetLabel('True')
            
        evt.Skip()


EPBSize = 26


class icEditPropTButton(icEditPropCtrl):
    """
    Класс редактирования текстовых свойств.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER, label='...'):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента.
        """
        icEditPropCtrl.__init__(self, nameValue)
        x, y = pos
        w, h = size
        self.editorCtrl = wx.TextCtrl(nameValue.main.panel2, self.wID, nameValue.GetStr(),
                                      pos=pos, size=size, style=style)
        idButton = icwidget.icNewId()
        self.button = wx.Button(self.editorCtrl, idButton, label,
                                pos=(w-EPBSize-1, 0), size = (EPBSize, h))
        self.button.editor = self
        self.button.Show()

        if 'OnButton' in self.propEditor:
            self.editorCtrl.Bind(wx.EVT_BUTTON, self.propEditor['OnButton'], id=idButton)

        self.nameValue.main.panel2.Bind(wx.EVT_TEXT, self.OnText, id=self.wID)
        
    def OnButton(self, evt):
        """
        """
                
        self.nameValue.value = self.propEditor['OnButton']()
        self.nameValue.oldValue = self.value
        self.nameValue.edit_ctrl.SetValue(self.nameValue.GetStr())
        evt.Skip()
        
    def OnText(self, evt):
        evt.Skip()
        self.button.Refresh(True)
        
    def SetSize(self, (width, height)):
        if self.editorCtrl:
            self.editorCtrl.SetSize(wx.Size(width-1, height))
            self.button.SetPosition((width - EPBSize - 1, 0))

    def Destroy(self):
        """
        Close an open editor control
        """
        if self.editorCtrl:
            self.editorCtrl.Destroy()
            self.editorCtrl = None
            
        if self.button:
            self.button.Destroy()
            self.button = None


class icEditColor(icEditPropTButton):
    """
    Редактор для редактирования цветов.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента.
        """
        nameValue.dict['OnButton'] = self.OnSelectColor
        icEditPropTButton.__init__(self, nameValue, pos, size, style)

    def GetValue(self):
                
        try:
            ret = eval(self.editorCtrl.GetValue())

            if ret is not None and type(ret) != type(wx.Colour(0, 0, 0)) and \
               not isinstance(ret, tuple) or (isinstance(ret, tuple) and len(ret) != 3):
                ret = self.value
                MsgBox(None, u'Несоответствие типа <%s>' % self.editorCtrl.GetValue())
        except:
            ret = self.value
            MsgBox(None, u'Ошибка ввода <%s>' % self.editorCtrl.GetValue())
        
        if type(ret) == type(wx.Colour(0, 0, 0)):
            ret = (ret.Red(), ret.Green(), ret.Blue())
        return ret
    
    def OnSelectColor(self, evt):
        """
        Запускает стандартное диалоговое окно для выбора цвета.
        """
        dlg = wx.ColourDialog(self.nameValue.main)
        dlg.GetColourData().SetChooseFull(True)
        clr = self.GetValue()
        
        if clr is not None:
            dlg.GetColourData().SetColour(wx.Colour(clr[0], clr[1], clr[2]) )
        else:
            dlg.GetColourData().SetColour(wx.Colour(0, 0, 0))
            
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            clr = data.GetColour()
            self.nameValue.value = (clr.Red(), clr.Green(), clr.Blue())
            self.nameValue.oldValue = self.value
            self.nameValue.edit_ctrl.SetValue(self.nameValue.GetStr())
            self.nameValue.edit_ctrl.SetFocus()
        
        dlg.Destroy()
        evt.Skip()


class icEditFont(icEditPropTButton):
    """
    Редактор для редактирования шрифтов.
    """
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента.
        """
        self.nameValue = nameValue
        nameValue.dict['OnButton'] = self.OnSelectFont
        icEditPropTButton.__init__(self, nameValue, pos, size, style)
                
    def GetValue(self):
        
        try:
            ret = eval(self.editorCtrl.GetValue())
            
            if not isinstance(ret, dict):
                ret = self.value
                MsgBox(None, u'Несоответствие типа <%s>' % self.editorCtrl.GetValue())
        except:
            ret = self.value
            MsgBox(None, u'Ошибка ввода <%s>' % self.editorCtrl.GetValue())
        return ret
            
    def OnSelectFont(self, evt):
        """
        Запускает стандартное диалоговое окно для выбора шрифта.
        """
        data = wx.FontData()
        data.EnableEffects(True)
        curFont = icFont(self.GetValue())
        data.SetInitialFont(curFont)

        dlg = wx.FontDialog(self.nameValue.main, data)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            
            self.nameValue.value['size'] = font.GetPointSize()
            self.nameValue.value['family'] = getICFamily(font)
            self.nameValue.value['style'] = getICFontStyle(font)
            self.nameValue.value['faceName'] = font.GetFaceName()
            self.nameValue.value['underline'] = font.GetUnderlined()
            self.nameValue.oldValue = self.nameValue.value
            self.nameValue.value_ctrl.SetLabel(self.nameValue.GetStr())
            self.nameValue.edit_ctrl.SetValue(self.nameValue.GetStr())
            
            self.nameValue.edit_ctrl.SetFocus()

        dlg.Destroy()
            
    def OnExpand(self, evt):
        """
        Функция запускается при выборе CheckBox.
        """
        keys = icEdtFontKeys
        
        if not self.nameValue.name_ctrl.IsChecked():
            indx = self.nameValue.GetIndx() + 1
            self.editorCtrl.Enable(False)
            self.nameValue.SetEnableEditor(False)

            if not self.nameValue.value:
                self.nameValue.value = icSpcDefStruct(SPC_IC_FONT, self.nameValue.value)
            
            self.nameValue.main.InsNameValues(indx, '  size', self.nameValue.value['size'],
                                              icDefInf.EDT_TEXTFIELD, bRefresh=False)
            self.nameValue.main.InsNameValues(indx+1, '  family', self.nameValue.value['family'],
                                              icDefInf.EDT_CHOICE, {'choices': ICFontFamily},
                                              bRefresh=False)
            self.nameValue.main.InsNameValues(indx+2, '  faceName', self.nameValue.value['faceName'],
                                              icDefInf.EDT_TEXTFIELD, bRefresh=False)
            self.nameValue.main.InsNameValues(indx+3, '  style', self.nameValue.value['style'],
                                              icDefInf.EDT_CHOICE, {'choices': ICFontStyle}, bRefresh=False)
            self.nameValue.main.InsNameValues(indx+4, '  underline', self.nameValue.value['underline'],
                                              icDefInf.EDT_CHECK_BOX)
                
        else:
            indx = self.nameValue.GetIndx() + 1
            self.nameValue.SetEnableEditor(True)
            self.editorCtrl.Enable(True)
            
            # Определяем новое значение основного поля
            for key in keys:
                    if key == 'size':
                        try:
                            self.nameValue.oldValue[key] = int(self.nameValue.main.NameValues[indx].value)
                        except:
                            self.nameValue.oldValue[key] = 8
                    else:
                        self.nameValue.oldValue[key] = self.nameValue.main.NameValues[indx].value
                        
                    self.nameValue.main.RemoveIndx(indx)
                                        
            self.nameValue.value = self.nameValue.oldValue
            self.nameValue.value_ctrl.SetLabel(self.nameValue.GetStr())
            self.editorCtrl.SetValue(self.nameValue.GetStr())
            self.value = self.nameValue.value
            
        self.nameValue.main.RefreshPos()
        self.nameValue.main.refreshSplitter()
            
        evt.Skip()


class icEditPropPyScript(icEditPropTButton):
    """
    Класс редактирования питоновских скриптов.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента. По умолчанию wx.SIMPLE_BORDER.
        """
        self.nameValue = nameValue
        nameValue.dict['OnButton'] = self.OnEditScript
        self.dlg = None
        
        icEditPropTButton.__init__(self, nameValue, pos, size, style, label='Py')
        self.editorCtrl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        
    def OnKeyDown(self, evt):
        """
        Отлавливаем нажатие <Ctrl-M> для выбора метода из библиотеки методов.
        """
        cod = evt.GetKeyCode()
        
        if (cod in [ord('m'), ord('M')] and evt.ControlDown()) or cod == wx.WXK_F1:
            dlg = MthDialog(self.nameValue.main, icwidget.icNewId(), u'Выбери метод', size=(400, 350))
            ret = dlg.ShowModal()
        
            # Копия
            if ret in [10,20]:
                wx.TheClipboard.Open()
                txt_obj = wx.TextDataObject()
                txt = '@'+dlg.ret_tpl
                txt_obj.SetText(txt)
                wx.TheClipboard.SetData(txt_obj)
                wx.TheClipboard.Close()
                
                self.nameValue.value = txt
                self.nameValue.oldValue = txt
                
                self.nameValue.value_ctrl.SetLabel(self.nameValue.GetStr())
                self.nameValue.edit_ctrl.SetValue(txt)
                self.editorCtrl.SetValue(self.nameValue.GetStr())
                self.nameValue.edit_ctrl.SetFocus()
                                                
            dlg.Destroy()
         
        evt.Skip()
        
    def isScript(self):
        """
        Возвращает признак скрипта.
        """
        value = self.nameValue.value
        return type(value) in (str, unicode) and ('\r\n' in value or '\n' in value)
        
    def OnEditScript(self, evt):
        """
        """
        #   Определяем смещение видимой части окна
        wOffset, hOffset = self.nameValue.main.GetViewStart()
        puw, puh = self.nameValue.main.GetScrollPixelsPerUnit()
        
        pos_cl = self.nameValue.main.panel2.ClientToScreenXY(70, 0)
        pos = (pos_cl[0]+2, pos_cl[1]+(hOffset*puh)-2)
        
        sz = [-1, -1]
        sz[0] = self.nameValue.main.panel2.GetSize()[0] - 70 + 20
        sz[1] = self.nameValue.main.GetSize()[1]+3

        try:
            split = self.nameValue.main.GetGrandParent().GetParent()
            if split.type == 'ResEditor':
                sz[1] += split.tree.GetSize()[1] + 5
        except:
            LogLastError('OnEditScript')
            
        self.dlg = ic_pyed.icPyEditorDlg(self.nameValue.main, self.nameValue.value, pos, sz)

        if not self.nameValue.IsEnableEditor():
            self.dlg.editor.SetReadOnlyMode()
        
        #
        ret = self.dlg.ShowModal()
        
        if ret == wx.ID_OK:
            #   Генерируем новый UUID
            if self.nameValue.IsEnableEditor():
                self.SaveText()
                old_uuid = _uuid
                _uuid = self.nameValue.main.GenNewUUIDObj()
            else:
                old_uuid = _uuid = self.nameValue.main.GetUUIDObj()
                            
            # запомнить точки останова
            self.dlg.editor.GetBreakpoints()
            SysProc.SetPointList(old_uuid, _uuid, attr, self.dlg.editor._Breakpoints,
                                 self.dlg.editor.GetText(),
                                 (self.dlg.editor.GetLineCount(), self.dlg.editor.GetIndent(),
                                  self.dlg.editor.GetEOLMode()))
        if self.dlg:
            self.dlg.Destroy()
        
    def SaveText(self):
        """
        Сохраняет текст в ресурсном описании.
        """
        if self.dlg:
            self.nameValue.value = self.dlg.editor.GetText()
            self.nameValue.oldValue = self.nameValue.value
            self.nameValue.value_ctrl.SetLabel(self.nameValue.GetStr())
            self.nameValue.edit_ctrl.SetValue(self.nameValue.value)
            self.editorCtrl.SetValue(self.nameValue.GetStr())
            self.nameValue.edit_ctrl.SetFocus()
        
    def Destroy(self):
        """
        """
        if self.editorCtrl:

            if self.dlg:
                self.dlg.EndModal(wx.ID_OK)

            self.dlg = None
            self.editorCtrl.Destroy()
            self.editorCtrl = None
            
    def GetValue(self):
        """
        Read value from editor control
        """
        val = self.value
        
        if self.editorCtrl and not self.isScript():
            try:
                val = self.editorCtrl.GetValue()
 
                # Генерируем новый UUID ресурса
                import ic.icEditor.CfgSysProc as SysProc
                old_uuid = self.nameValue.main.GenUUIDObj()
                _uuid = self.nameValue.main.GenNewUUIDObj()
                
                # Меняем uuid в буфере точек остонова
                SysProc.SetPointList(old_uuid, _uuid, attr)
            except:
                pass
            
        return val

    def SetValue(self, value):
        """
        Write value to editor control
        """
        self.value = value
        
        if self.editorCtrl and not self.isScript():
            try:
                self.editorCtrl.SetValue(value)
            except:
                pass


class icEditNewProperty(icEditPropTButton):
    """
    Редактор для добавления нового свойства.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента.
        """
        nameValue.dict['OnButton'] = self.OnAddProperty
        icEditPropTButton.__init__(self, nameValue, pos, size, style, '+')

    def OnAddProperty(self, evt):
        """
        Добавляет дополнительное свойство в редактор.
        """
        indx = self.nameValue.GetIndx()

        val = self.GetValue().strip()
        
        if not val in ['<...>', None, '']:
            
            if val.find(icAddPropertyPrzn) == 0:
                propName = val
            else:
                propName = icAddPropertyPrzn + val
            
            # Проверяем имя свойства на уникальность
            # 1. Определяем список дополнительных свойств
            lst = [x.name for x in [x for x in self.nameValue.main.NameValues if x.type == icDefInf.EDT_ADD_PROPERTY]]
            
            if propName not in lst:
                # Вставляем свойство
                self.nameValue.main.InsNameValues(indx, propName, '', icDefInf.EDT_ADD_PROPERTY,
                                                  nameType=icNameTypeAddPropery, bRefresh=True)
                self.nameValue.main.PostSelectProperty(indx)
            else:
                MsgBox(self.nameValue.main, u'Свойств с именем <%s> уже есть.' % propName)
            
        evt.Skip()


class icEditAddProperty(icEditPropPyScript):
    """
    Редактор для добавления нового свойства.
    """
    
    def __init__(self, nameValue, pos, size, style=wx.SIMPLE_BORDER):
        """
        @type nameValue: C{NameValue}
        @param nameValue: Указатель на объект свойства NameValue.
        @type pos: C{wx.Point}
        @param pos: Позиция компонента.
        @type size: C{wx.Size}
        @param size: Размеры компонента.
        @type style: C{long}
        @param style: Стиль компонента.
        """
        icEditPropPyScript.__init__(self, nameValue, pos, size, style)
        
        x, y = pos
        w, h = size
        ss = 3

        idButtonDel = icwidget.icNewId()

        self.buttonDel = wx.Button(self.editorCtrl, idButtonDel, 'X',
                                   pos=(w-2*EPBSize-1+ss, 0), size = (EPBSize-ss, h-ss))
        self.buttonDel.editor = self
        self.buttonDel.Show()
        
        self.editorCtrl.Bind(wx.EVT_BUTTON, self.OnDelProperty, id=idButtonDel)
        
    def OnText(self, evt):
        evt.Skip()
        self.button.Refresh(True)
        self.buttonDel.Refresh(True)

    def OnDelProperty(self, evt):
        """
        Удаляет дополнительное свойство из редактора.
        """
        evt.Skip()
        indx = self.nameValue.GetIndx()
        msg = u'Вы действительно хотите удалить свойство <%s>?' % self.nameValue.name
                
        if MsgBox(self.nameValue.main, msg, style=wx.YES_NO | wx.NO_DEFAULT) == wx.ID_YES:
            if len(self.nameValue.main.NameValues)-1 > indx:
                self.nameValue.main.NameValues[indx+1].list_del_property = [indx]
                self.nameValue.main.PostSelectProperty(indx+1)
            else:
                self.nameValue.main.NameValues[indx-1].list_del_property = [indx]
                self.nameValue.main.PostSelectProperty(indx-1)
