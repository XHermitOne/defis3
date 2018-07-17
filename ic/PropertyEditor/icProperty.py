#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Редакторы свойств.
"""

import wx
from wx.lib.stattext import GenStaticText
from .icPropEditors import *
import types
from ic.components.icfont import *
from ic.components.icframe import *
from ic.log.iclog import *
from ic.components.icwidget import icEvent
from . import icDefInf
from ic.utils import ic_uuid

scrollBarWidth = 0
IECWidthFudge = 3
oiLineHeight = 20

# Буфер объектов StaticText
staticTextBuff = {}


def getStaticTextBuff(parent, id, text, pos, size, bCreate=True):
    """
    Возвращает StaticText из буфера либо создает новый.
    """
    global staticTextBuff
    _uuid = parent._uuid
    bBuff = False
    
    if _uuid not in staticTextBuff or bCreate:
        statTextCtrl = GenStaticText(parent, -1, text, pos, size)
    else:
        try:
            statTextCtrl = staticTextBuff[_uuid].pop(0)
            statTextCtrl.SetPosition(pos)
            statTextCtrl.SetSize(size)
            statTextCtrl.SetLabel(text)
            
            font = icFont({})
            statTextCtrl.SetFont(font)
            statTextCtrl.Show(True)
            bBuff = True
        except:
            LogLastError('GIVE FROM BUFF ERROR')
            staticTextBuff = {}
            statTextCtrl = GenStaticText(parent, -1, text, pos, size)

    return bBuff, statTextCtrl


def AddStaticTextBuff(ctrl):
    """
    Добавляет объект в буфер.
    """
    global staticTextBuff
    _uuid = ctrl.GetParent()._uuid
        
    ctrl.Show(False)
    
    if _uuid in staticTextBuff:
        if len(staticTextBuff[_uuid]) < 50 and ctrl not in staticTextBuff[_uuid]:
            staticTextBuff[_uuid].append(ctrl)
    else:
        staticTextBuff[_uuid] = [ctrl]


def ClearStaticTextBuff(uuid):
    """
    Чистит буфер компонентов редактора с заданым идентификатором.
    """
    global staticTextBuff
    
    if uuid in staticTextBuff:
        for obj in staticTextBuff[uuid]:
            try:
                obj.Destroy()
            except:
                pass
                
        staticTextBuff.pop(uuid)


def OnButt(evt):
    evt.Skip()


class icTextValue(GenStaticText):
    """
    """

    def __init__(self, parent, ID, label, pos=wx.DefaultPosition, size = wx.DefaultSize, style=0):
        """
        """
        self._bRepaint = True
        GenStaticText.__init__(self, parent, ID, label, pos, size, style)

    def OnPaint2(self, event):
        """
        """
        dc = wx.BufferedPaintDC(self)
        width, height = self.GetClientSize()
        if not width or not height:
            return

        clr = self.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.SOLID)
        if wx.Platform == '__WXMAC__' and clr == self.defBackClr:
            # if colour is still the default then use the striped background on Mac
            backBrush.SetMacTheme(1)

        if self._bRepaint:
            label = self.GetLabel()
            dc.SetBackground(backBrush)
            dc.SetTextForeground(self.GetForegroundColour())
            dc.Clear()

            dc.SetFont(self.GetFont())
            style = self.GetWindowStyleFlag()
            x = y = 0
            
            for line in label.split('\n'):
                if line == '':
                    w, h = self.GetTextExtent('W')  # empty lines have height too
                else:
                    w, h = self.GetTextExtent(line)
                if style & wx.ALIGN_RIGHT:
                    x = width - w
                if style & wx.ALIGN_CENTER:
                    x = (width - w)/2
                dc.DrawText(line, (x, y))
                y += h
        else:
            pass
            
    def setRepaintMode(self, mode=True):
        """
        """
        self._bRepaint = mode

    def getRepaintMode(self):
        """
        """
        return self._bRepaint


class NameValue(icEvent):
    """
    Класс описывает строку панели свойств.
    """

    def __init__(self, main, indx, name='', value='', type=icDefInf.EDT_TEXTFIELD, dict={},
                 nameType=icNameTypeNormal, height=oiLineHeight):
        """
        @type main: C{wx.Window}
        @param main: Указатель на окно сплиттера.
        @type indx: C{int}
        @param indx: Индекс свойства.
        @type type: C{int}
        @param type: Тип редактора. 
            EDT_TEXTFIELD = 0 - текстовое поле, 
            EDT_CHOICE = 1 - Choice, 
            EDT_CHECK_BOX = 2 - CheckBox,
            EDT_2CHECK_BOX = 3 - Разворачиваемый набор CheckBox (используется для комбинированных свойств). 
            EDT_EXTERNAL = 4 - Внешний редактор.
        @type dict: C{Dictionary}
        @param dict: Словарь дополнительных свойств.            
        @type nameType: C{int}
        @param nameType: Тип представления названия свойства:
            icNameTypeNormal - StaticText.
            icNameTypeCheckBox - CheckBox.
            icNameTypeReadonly - Нередактируемое свойство - StaticText выделенный жирным шрифтом.
        @type height: C{int}
        @param height: Высота строки.
        """
        icEvent.__init__(self)
        
        self.main = main
        self.name = name
        self.value = value
        self.oldValue = value
        self.height = height-IECWidthFudge
        self.isSelected = False
        self.edit_ctrl = None
        self.topLine = None
        self.bottomLine = None
        self.colorBox = None
        
        # Список ключей комбинированного  свойства (EDT_COMBINE)
        self.comboKeys = None
        
        # Список индексов свойств помеченных для удаления
        self.list_del_property = []
        
        self.type = type
        self.nameType = nameType
        self.dict = dict
        self.__editorEnable = main.isToggleEnable()
        bBuffName = False
        bBuffVal = False
                
        if nameType != icNameTypeCheckBox and type != icDefInf.EDT_COMBINE:
            bBuffName, self.name_ctrl = getStaticTextBuff(main.panel1, icwidget.icNewId(), '     ' + name,
                                                          pos=(0, indx*height),  size=(1, height-2))
            self.name_ctrl.SetBackgroundColour(wx.Colour(240, 240, 240))
            
            if nameType == icNameTypeReadonly:
                font = icFont({'style': 'bold'})
                self.name_ctrl.SetFont(font)
                self.name_ctrl.SetLabel('   ' + name)
            elif nameType == icNameTypeAddPropery:
                font = icFont({'style': 'bold'})
                self.name_ctrl.SetFont(font)
                self.name_ctrl.SetLabel('   ' + name)
                self.name_ctrl.SetBackgroundColour(wx.Colour(230, 230, 210))
        else:
            id = icwidget.icNewId()
            self.name_ctrl = wx.CheckBox(main.panel1, id, name, pos=(0, indx*height), size=(1, height))
            self.name_ctrl.SetValue(1)
            self.name_ctrl.Bind(wx.EVT_CHECKBOX, self.OnExpand, id=id)
            
            if type == icDefInf.EDT_FONT:
                self.comboKeys = icEdtFontKeys
            else:
                try:
                    self.comboKeys = value.keys()
                except:
                    print(name, value)
                
            font = icFont({'style': 'bold'})
            self.name_ctrl.SetFont(font)

        if type == icDefInf.EDT_COLOR:
            self.colorBox = wx.Window(main.panel2, -1, (3, indx*height), (14, height - 6), style=wx.SIMPLE_BORDER)
            
            if value is not None:
                self.colorBox.SetBackgroundColour(wx.Colour(value[0], value[1], value[2]))
                
            self.value_ctrl = GenStaticText(main.panel2, icwidget.icNewId(),  self.GetStr(),
                                            pos=(20, indx*height), size=(1, height))
        elif type == icDefInf.EDT_CHOICE:
            self.value_ctrl = wx.StaticText(main.panel2, icwidget.icNewId(),  self.GetStr(),
                                            pos=(2, indx*height), size=(1, height), style=wx.ST_NO_AUTORESIZE)
        else:
            bBuffVal, self.value_ctrl = getStaticTextBuff(main.panel2, icwidget.icNewId(), self.GetStr(),
                                                          pos=(2, indx*height), size=(1, height))

        self.value_ctrl.SetForegroundColour(wx.Colour(20, 100, 180))
        
        self.line_name = wx.StaticLine(main.panel1, -1, style=wx.LI_HORIZONTAL,
                                       pos=(-2, (indx+1)*height-IECWidthFudge), size=(10, 1))
        self.line_value = wx.StaticLine(main.panel2, -1, style=wx.LI_HORIZONTAL,
                                        pos=(-2, (indx+1)*height-IECWidthFudge), size=(200, 1))

        if not bBuffName:
            self.name_ctrl.Bind(wx.EVT_LEFT_DOWN, main.OnSelect)
            
        if not bBuffVal:            
            self.value_ctrl.Bind(wx.EVT_LEFT_DOWN, main.OnSelect)
        
    def SetEnableEditor(self, bEnable):
        """
        Разрешает или запрещает редактирование свойства.
        
        @type bEnable: C{bool}
        @param bEnable: Признак разрешения редактирования. Если bEditor == True, редактирование разрешено 
            в противном случае запрещено.
        """
        self.__editorEnable = bEnable
        
    def IsEnableEditor(self):
        """
        Возвращает значение признака редактирования.
        
        @rtype: C{bool}
        @return: Возвращает значение признака редактирования. Если True, редактирование разрешено 
            в противном случае запрещено.
        """
        return self.__editorEnable
        
    def OnExpand(self, evt):
        """
        """
        if self.edit_ctrl is not None:
            self.edit_ctrl.OnExpand(evt)
            self.main.RefreshPos()
            self.main.refreshSplitter()

    def GetExpandValue(self):
        """
        Определяет значение словаря у раскрытого списка.
        """
        ret = self.value
           
        try: 
            if not self.name_ctrl.IsChecked():
                ret = {}
                indx = self.GetIndx() + 1
                    
                for key in self.comboKeys:
                    val = self.main.NameValues[indx].value
                    
                    if isinstance(self.oldValue[key], int):
                        ret[key] = int(self.main.NameValues[indx].value)
                    else:
                        ret[key] = self.main.NameValues[indx].value
                            
                    indx += 1
        except: 
            ret = self.value
        
        return ret

    def GetStr(self):
        """
        Возвращает строковое представление значение свойства.
        """
        if self.type == icDefInf.EDT_CHECK_BOX:
            if int(self.value):
                ret = 'True'
            else:
                ret = 'False'
        elif self.type == icDefInf.EDT_COMBINE:
            ret = ''
            for key in self.value.keys():
                if self.value[key]:
                    ret = ret + key + ' | ' 
            ret = ret[:-3]
        elif self.type == icDefInf.EDT_COLOR:
            if self.value is not None:
                ret = 'wx.Colour' + str(self.value)
            else:
                ret = 'None'
            
        elif self.type == icDefInf.EDT_POINT:
            ret = 'wx.Point' + str(self.value)
            
        elif self.type == icDefInf.EDT_SIZE:
            ret = 'wx.Size' + str(self.value)

        elif self.type in [icDefInf.EDT_PY_SCRIPT, icDefInf.EDT_ADD_PROPERTY] and \
             type(self.value) in (str, unicode) and ('\r\n' in self.value or '\n' in self.value):
            val = self.value.replace('\r\n', '\n')
            nf = val.find('\n')
            ret = '<Script> ' + val[:nf] + ' ...'         
        elif self.type == icDefInf.EDT_NEW_PROPERTY:
            ret = '<...>'  
        else:
            ret = str(self.value)
        
        return ret
    
    def CreateEditor(self, indx):
        """
        """
        height = self.height+IECWidthFudge
        prnt = self

        if self.type == icDefInf.EDT_TEXTFIELD:
            self.edit_ctrl = icEditPropText(prnt, pos=(-2, indx*height-1),
                                            size=(self.main.panel2.GetSize()[0]+4, self.height+2))

        elif self.type == icDefInf.EDT_PY_SCRIPT:
            self.edit_ctrl = icEditPropPyScript(prnt, pos=(-2, indx*height-1),
                                                size=(self.main.panel2.GetSize()[0]+4, self.height+2))
                    
            if type(self.value) in (str, unicode) and ('\r\n' in self.value or '\n' in self.value):
                self.edit_ctrl.OnEditScript(None)

        elif self.type == icDefInf.EDT_NUMBER:
            self.edit_ctrl = icEditPropNumber(prnt, pos=(-2, indx*height-1),
                                              size=(self.main.panel2.GetSize()[0]+4, self.height+2))
        
        elif self.type == icDefInf.EDT_TEXTLIST:
            self.edit_ctrl = icEditPropTextList(prnt, pos=(-2, indx*height-1),
                                                size=(self.main.panel2.GetSize()[0]+4, self.height+2))
        
        elif self.type == icDefInf.EDT_TEXTDICT:
            self.edit_ctrl = icEditPropTextDict(prnt, pos=(-2, indx*height-1),
                                                size=(self.main.panel2.GetSize()[0]+4, self.height+2))

        elif self.type == icDefInf.EDT_DICT:
            self.edit_ctrl = icEditPropDict(prnt, pos=(-2, indx*height-1),
                                            size=(self.main.panel2.GetSize()[0]+4, self.height+2))

        elif self.type == icDefInf.EDT_IMPORT_NAMES:
            self.edit_ctrl = icEditImportNames(prnt, pos=(-2, indx*height-1),
                                               size=(self.main.panel2.GetSize()[0]+4, self.height+2))
            
        elif self.type == icDefInf.EDT_COMBINE:
            self.edit_ctrl = icEditPropCombine(prnt, pos=(-2, indx*height-1),
                                               size=(self.main.panel2.GetSize()[0]+4, self.height+2))
                
        elif self.type == icDefInf.EDT_CHOICE:
            self.edit_ctrl = icEditPropChoice(prnt, (-2, indx*height-1),
                                              (self.main.panel2.GetSize()[0]+4, self.height+2))

        elif self.type == icDefInf.EDT_CHECK_BOX:
            self.edit_ctrl = icEditPropCheckBox(prnt, pos=(2, indx*height-1),
                                                size=(self.main.panel2.GetSize()[0]-2, self.height+2),
                                                style=wx.WANTS_CHARS | wx.TAB_TRAVERSAL)
       
        elif self.type == icDefInf.EDT_EXTERNAL:
            self.edit_ctrl = icEditPropTButton(prnt, pos=(-2, indx*height-1),
                                               size=(self.main.panel2.GetSize()[0]+4, self.height+2))
            
        elif self.type == icDefInf.EDT_COLOR:            
            self.edit_ctrl = icEditColor(prnt, pos=(-2, indx*height-1),
                                         size=(self.main.panel2.GetSize()[0]+4, self.height+2))
           
        elif self.type == icDefInf.EDT_FONT:
            self.edit_ctrl = icEditFont(prnt, pos=(-2, indx*height-1),
                                        size=(self.main.panel2.GetSize()[0]+4, self.height+2))
        
        elif self.type == icDefInf.EDT_POINT:
            self.edit_ctrl = icEditPropPoint(prnt, pos=(-2, indx*height-1),
                                             size=(self.main.panel2.GetSize()[0]+4, self.height+2))

        elif self.type == icDefInf.EDT_SIZE:
            self.edit_ctrl = icEditPropSize(prnt, pos=(-2, indx*height-1),
                                            size=(self.main.panel2.GetSize()[0]+4, self.height+2))

        elif self.type == icDefInf.EDT_NEW_PROPERTY:
            self.edit_ctrl = icEditNewProperty(prnt, pos=(-2, indx*height-1),
                                               size=(self.main.panel2.GetSize()[0]+4, self.height+2))

        elif self.type == icDefInf.EDT_ADD_PROPERTY:
            self.edit_ctrl = icEditAddProperty(prnt, pos=(-2, indx*height-1),
                                               size=(self.main.panel2.GetSize()[0]+4, self.height+2))

            if type(self.value) in (str, unicode) and ('\r\n' in self.value or '\n' in self.value):
                self.edit_ctrl.OnEditScript(None)

        # Устанавливаем для редактора его высоту
        if self.edit_ctrl and self.edit_ctrl.editorCtrl:
            self.edit_ctrl.height_edt = height
            
            y0 = indx * height - IECWidthFudge + 2
            
            if y0 < 0: 
                y0 = 0
            
            if not self.IsEnableEditor():
                self.edit_ctrl.editorCtrl.Enable(False)
                
            w = self.main.panel1.GetSize()[0]+4

            self.topLine = wx.Window(self.main.panel1, -1, style=wx.LI_HORIZONTAL | wx.SIMPLE_BORDER,
                                     pos=(-2, y0), size=(w, 1))
            self.bottomLine = wx.Window(self.main.panel1, -1, style=wx.LI_HORIZONTAL,
                                        pos=(-2, (indx+1)*height-IECWidthFudge), size=(w, 1))

            self.topLine.SetBackgroundColour(wx.Colour(0, 0, 0))
            self.bottomLine.SetBackgroundColour(wx.Colour(255, 255, 255))
            self.edit_ctrl.SetFocus()
            self.main.cursor = indx

            try:
                self.edit_ctrl.Bind(wx.EVT_KEY_DOWN, self.OnEditorKeyDown) 
            except:
                self.edit_ctrl.editorCtrl.Bind(wx.EVT_KEY_DOWN, self.OnEditorKeyDown) 

    def GetIndx(self):
        """
        Возвращает индекс строки
        """
        indx = 0
        
        for obj in self.main.NameValues:
            if obj == self:
                return indx
            indx += 1
            
        return -1
    
    def OnEditorKeyDown(self, evt):
        """
        """
        indx = self.GetIndx()
        wOffset, hOffset = self.main.GetViewStart()
            
        if evt.GetKeyCode() == wx.WXK_UP:
            if indx > 0:
                indx -= 1
                self.main.SelectEdt(indx)
                
            if self.line_name.GetPosition()[1] < (hOffset+1)*oiLineHeight:
                self.main.Scroll(0, hOffset - 1)
            
        elif evt.GetKeyCode() == wx.WXK_DOWN or evt.GetKeyCode() == wx.WXK_RETURN:
            
            if indx < len(self.main.NameValues)-1:
                indx += 1
                self.main.SelectEdt(indx)
            
            sy = self.main.GetClientSize().y/oiLineHeight
            sy += hOffset

            if self.line_name.GetPosition()[1] > sy*oiLineHeight:
                self.main.Scroll(0, self.line_name.GetPosition()[1]/oiLineHeight + 1)
                
        elif evt.GetKeyCode() == wx.WXK_HOME and evt.ControlDown(): 
            self.main.SelectEdt(0)
            self.main.Scroll(0, 0)
            
        elif evt.GetKeyCode() == wx.WXK_END and evt.ControlDown():
            indx = len(self.main.NameValues)-1
            self.main.SelectEdt(indx)
            self.main.Scroll(0, indx)
        else:
            evt.Skip()

        
class icPropWin(icEvent, wx.ScrolledWindow):
    """
    Класс описывает таблицу сойств определенного объекта.
    """
    
    def _init_ctrls(self, prnt):
        """
        Создаем необходимые компоненты
        """
        icEvent.__init__(self)
        # UUID ресурса
        self._uuidRes = None
        self._uuid = ic_uuid.get_uuid()
        
        # Список свойств
        self.NameValues = []
        
        # Список удаленных свойств
        self._delPropertyLst = []
        
        self.oldLen = 0
        self.parent = prnt
        id_sash = icwidget.icNewId()
        self.splitter = wx.SplitterWindow(self, id_sash, wx.Point(0, 0), prnt.GetSize(),
                                          style=wx.SP_LIVE_UPDATE | wx.NO_3D | wx.SP_3D | wx.SP_NOBORDER)
        self.splitter.SetSashSize(4)
        
        #   Создаем панели
        self.panel1 = wx.Panel(self.splitter, icwidget.icNewId(), style=wx.WANTS_CHARS)
        self.panel1.Bind(wx.EVT_SIZE, self.OnNameSize)
        self.panel1.box = None
        self.panel1._uuid = self._uuid+':p1'
        
        self.panel2 = wx.Panel(self.splitter, icwidget.icNewId(), style=wx.WANTS_CHARS)
        self.panel2.box = None
        self.panel2._uuid = self._uuid+':p2'
        self.splitter.SplitVertically(self.panel1, self.panel2)
        self.splitter.SetMinimumPaneSize(20)
        self.splitter.SetSashPosition(100)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def Destroy(self):
        """
        """
        # Чистим буфер комопнентов
        if self.GetUUID():
            ClearStaticTextBuff(self.GetUUID()+':p1')
            ClearStaticTextBuff(self.GetUUID()+':p2')
            
        wx.ScrolledWindow.Destroy(self)
        
    def GetUUID(self):
        """
        """
        return self._uuid
        
    def SetUUIDObj(self, uuidRes):
        """
        Запоминает uuid ресурсного описания.
        """
        self._uuidRes = uuidRes
        
    def GetUUIDObj(self):
        """
        Возвращает uuid ресурсного описания.
        """
        return self._uuidRes
        
    def GenNewUUIDObj(self):
        """
        Генерирует новый идентификатор ресурса.
        """
        self._uuidRes = ic_uuid.get_uuid()
        return self._uuidRes
        
    def getPopPropertyLst(self):
        """
        Возвращает список удаленных свойств.
        """
        return self._delPropertyLst
    
    def clearPopPropertyLst(self):
        """
        Возвращает список удаленных свойств.
        """
        self._delPropertyLst = []
    
    def SetNameProperty(self, prop, value):
        """
        Устанавливает новое значение свойства.
        
        @type prop: C{string}
        @param prop: Имя свойства.
        @type value: C{string}
        @param value: Новое значение свойства.
        """
        
        for prop_obj in self.NameValues:
            if prop_obj.name == prop:
                #   Закрываем редактор свойства
                if self.selectedEdt:
                    self.SelectEdt(None)
                
                prop_obj.value = value    
                prop_obj.value_ctrl.SetLabel(prop_obj.GetStr())
                return True
                
        return False
               
    def GetNameProperty(self, prop):
        """
        Возвращает значение свойства по имени свойства.
        """
        for prop_obj in self.NameValues:
            if prop_obj.name == prop:
                return prop_obj.value
        
        return None
        
    def PopPropery(self, indx, bRefresh = False):
        """
        Удаляет свойство из редактора.
        
        @type indx: C{int}
        @param indx: Индекс свойства
        """
        try:
            prop = self.NameValues[indx]
            
            #   Если удаляемая строка относится к дополнительному свойству, то 
            #   помечаем, что данное свойство было удалено. Это нужно для коректного
            #   изменения структуры ресурса. 
            if prop.type == icDefInf.EDT_ADD_PROPERTY:
                self._delPropertyLst.append(prop.name)
            
            self.RemoveIndx(indx, bRefresh)
        except:
            LogLastError('PopProperty Error')
            
    def FillNameValueDict(self, dict={}):
        """
        Заполняет словарь данными из редактора.
        
        @type dict: C{dictionary}
        @param dict: Словарь, который заполняется данными из редактора свойств.
        """
        
        for obj in self.NameValues:
            dict[obj.name] = obj.value
            
        return dict
        
    def RefreshPos(self):
        """
        Перерисовывает строки свойств.
        """
        indx = 0
        for obj in self.NameValues:
            name = obj.name
            height = obj.height+IECWidthFudge
            
            obj.name_ctrl.SetPosition((0, indx*height))
            obj.name_ctrl.SetSize((self.panel1.GetSize()[0], obj.height))
            
            obj.line_name.SetPosition((-2, (indx+1)*height - 2))
            obj.line_value.SetPosition((-2, (indx+1)*height - 2))
            obj.line_name.SetSize((self.panel1.GetSize()[0]+4, 1))
            obj.line_value.SetSize((self.panel2.GetSize()[0]+4, 1))
            
            if not obj.isSelected:
                
                if obj.colorBox is not None:
                    obj.colorBox.SetPosition((3, indx*height))
                    
                    try:
                        obj.colorBox.SetBackgroundColour(wx.Colour(obj.value[0], obj.value[1], obj.value[2]))
                    except:
                        pass
                    
                    obj.value_ctrl.SetPosition((20, indx*height))
                    obj.value_ctrl.SetSize((self.panel2.GetSize()[0]-20, obj.height))
                else:
                    obj.value_ctrl.SetPosition((2, indx*height))
                    obj.value_ctrl.SetSize((self.panel2.GetSize()[0], obj.height))
                
            else:
                if obj.edit_ctrl is None:
                    obj.CreateEditor(indx)
                    
                obj.edit_ctrl.Refresh(True)
                
            indx += 1
            
    def RefreshSize(self):
        indx = 0
        for obj in self.NameValues:
            obj.name_ctrl.SetSize((self.panel1.GetSize()[0], obj.height))
                        
            if obj.isSelected:
                obj.edit_ctrl.SetSize((self.panel2.GetSize()[0]+4, obj.height+2))
                obj.topLine.SetSize((self.panel1.GetSize()[0]+4, 1))
                obj.bottomLine.SetSize((self.panel1.GetSize()[0]+4, 1))

            else:
                if obj.colorBox is not None:
                    obj.value_ctrl.SetSize((self.panel2.GetSize()[0] - 20, obj.height))
                else:
                    obj.value_ctrl.SetSize((self.panel2.GetSize()[0], obj.height))

            obj.line_name.SetSize((self.panel1.GetSize()[0]+4, 1))
            obj.line_value.SetSize((self.panel2.GetSize()[0]+4, 1))
                        
            indx += 1
        
    def InsNameValues(self, indx, text, value, type=0, dict={}, 
                      nameType=0, bRefresh=True, height=oiLineHeight):
        """
        Вставляет строку в таблицу свойств.
        @type indx: C{int}
        @param indx: Позиция, куда вставляется свойство.
        @type text: C{string}
        @param text: Название свойства.
        @type value: C{...}
        @param value: Значение свойства. 
        @type type: C{int}
        @param type: Тип редактора. 
        @type dict: C{Dictionary}
        @param dict: Словарь дополнительных свойств.            
        @type bRefresh: C{bool}
        @param bRefresh: Признак перерисовки компонента.            
        """
        obj = NameValue(self, indx, text, value, type, dict, nameType, height)
        self.NameValues.insert(indx, obj)
        
        if bRefresh:
            self.RefreshPos()
            self.refreshSplitter()
        
    def AddNameValues(self, text, value, type=0, dict={}, nameType=0,
                      bRefresh=True, height=oiLineHeight):
        """
        Добавляет строку в таблицу свойств.
        @type text: C{string}
        @param text: Название свойства.
        @type value: C{...}
        @param value: Значение свойства. 
        @type type: C{int}
        @param type: Тип редактора. 
        @type dict: C{Dictionary}
        @param dict: Словарь дополнительных свойств.            
        @type bRefresh: C{bool}
        @param bRefresh: Признак перерисовки компонента.            
        """
        indx = len(self.NameValues)
        obj = NameValue(self, indx, text, value, type, dict, nameType, height)
        self.NameValues.append(obj)
        
        if bRefresh:
            self.RefreshPos()
            self.refreshSplitter()
    
    def RemoveIndx(self, indx, bRefresh=False):
        """
        Удаляет строку из редактора.
        @type indx: C{int}
        @param indx: Индекс совйства в редакторе.
        """
        
        if indx >= 0 and indx < len(self.NameValues):

            # Удаляем редактор
            if self.NameValues[indx].edit_ctrl is not None:
                self.NameValues[indx].edit_ctrl.Destroy()
                try:
                    self.NameValues[indx].topLine.Destroy()
                    self.NameValues[indx].bottomLine.Destroy()
                    self.NameValues[indx].topLine = None
                    self.NameValues[indx].bottomLine = None
                except:
                    pass
            
            self.NameValues[indx].name_ctrl.Destroy()
            self.NameValues[indx].value_ctrl.Destroy()
            self.NameValues[indx].line_name.Destroy()
            self.NameValues[indx].line_value.Destroy()

            if self.NameValues[indx].colorBox is not None:
                self.NameValues[indx].colorBox.Destroy()
            
            self.NameValues.pop(indx)
            
            if bRefresh:
                self.RefreshPos()
                self.refreshSplitter()
        else:
            return False
            
        return True
        
    def RemoveAll(self, bRefresh=True):
        """
        Удаляет все строки из редактора.
        
        @type bRefresh: C{bool}
        @param bRefresh: Признак перерисовки редактора.  Если True, то перерисовывается.
        """
        indx = 0
        size = len(self.NameValues)
        
        for indx in xrange(size):
            self.RemoveIndx(0)
            
        if bRefresh:
            self.RefreshPos()
            self.refreshSplitter()
    
        self.selectedEdt = None
        
    def OnNameSize(self, evt):
        """
        Отрабатывает сообщение об размеров окна.
        """
        sz = evt.GetSize()[0]

        for obj in self.NameValues:
            obj.name_ctrl.SetSize((sz+4, obj.height))
            
            obj.line_name.SetSize((sz+4, 1))
            obj.line_value.SetSize((self.splitter.GetSize()[0] - sz+4, 1))
            
            if obj.isSelected:
                obj.edit_ctrl.SetSize((self.splitter.GetSize()[0] - sz - 2, obj.height+2))
                obj.topLine.SetSize((sz+4, 1))
                obj.bottomLine.SetSize((sz+4, 1))
            else:
                obj.value_ctrl.Refresh(True)
            
        evt.Skip()
        
    def OnSashChanged(self, evt):
        """
        """
        sz = evt.GetSashPosition()

        for obj in self.NameValues:
            obj.name_ctrl.SetSize((sz+4, obj.height))
            
            obj.line_name.SetSize((sz+4, 1))
            obj.line_value.SetSize((self.splitter.GetSize()[0] - sz+4, 1))
            
            if obj.isSelected:
                obj.edit_ctrl.SetSize((self.splitter.GetSize()[0] - sz - 4, obj.height+2))
                obj.topLine.SetSize((sz+4, 1))
                obj.bottomLine.SetSize((sz+4, 1))
            else:
                obj.value_ctrl.Refresh(True)
            
        evt.Skip()
        
    def OnSize(self, evt):
        evt.Skip()
        self.refreshSplitter()
        self.RefreshSize()

    def getHeight(self):
        return len(self.NameValues) * oiLineHeight + 5
        
    def refreshSplitter(self):
        """
        Обновляем размеры сплиттера
        """
        s = wx.Size(self.GetClientSize().x, self.getHeight())
        wOffset, hOffset = self.GetViewStart()
        puw, puh = self.GetScrollPixelsPerUnit()
        self.splitter.SetDimensions(wOffset * puw, hOffset * puh * -1, s.x, s.y)
        self.updateScrollbars(wOffset, hOffset)

    def updateScrollbars(self, wOffset, hOffset):
        """
        Устанавливаем позиции прокруток.
        
        @type wOffset: C{int}
        @param wOffset:  Горизонатльное смещение.
        @type hOffset: C{int}
        @param hOffset: Вертикальное смещение.
        """
        height = len(self.NameValues)
        self.SetScrollbars(oiLineHeight, oiLineHeight, 0, height + 1, wOffset, hOffset)
    
    def ToggleEnable(self, bEnable=True):
        """
        Фунцкия разрешает/запрещает редактирование данных.
        
        @type bEnable: C{bool}.
        @param bEnable: Флаг разрешения редактирования.
        """
        self.__editorEnable = bEnable

    def isToggleEnable(self):
        """
        Возвращает признак редактирования. 
        """
        return self.__editorEnable
    
    def __init__(self, parent):
        """
        """
        wx.ScrolledWindow.__init__(self, parent, -1, size=parent.GetSize(), style=wx.HSCROLL | wx.VSCROLL)

        # Номер редактируемого свойства
        self.cursor = -1
        self.__editorEnable = True
        self._init_ctrls(parent)
        
        # Текущий редактор
        self.selectedEdt = None
                
    def SelectPropertyEdt(self, name):
        """
        Функция устанавливает редактор для редактирования заданного свойства.

        @type name: C{string}
        @param name: Имя заданного свойства.
        @rtype: C{bool}
        @return: Признак успешного выполнения.
        """
        for indx, obj in enumerate(self.NameValues):
            if obj.name == name:
                self.SelectEdt(indx)
                break
    
    def SelectEdt(self, indx):
        """
        Выбирает нужное свойство для редактирования.
        
        @type indx: C{int}
        @param indx: Индекс свойства, которое будет редактироваться. Если None, то 
            закроется редактор редактируемого свойства.
        """
        obj = self.selectedEdt

        try:
            sel = self.selectedEdt = self.NameValues[indx]        
        except: 
            sel = self.selectedEdt = None

        # Убираем признаки редактирования
        if (sel and obj and obj != sel and obj.isSelected and obj.edit_ctrl is not None) or not sel:
            obj.isSelected = False
            obj.value = obj.edit_ctrl.GetValue()

            try:
                obj.value_ctrl.setRepaintMode(True)
            except:
                pass
                
            obj.value_ctrl.Enable(True)
            obj.value_ctrl.SetLabel(obj.GetStr())
            obj.value_ctrl.SetSize((self.panel2.GetSize()[0]+4, obj.height+2))

            obj.edit_ctrl.Destroy()
            obj.edit_ctrl = None
                
            if obj.topLine:
                obj.topLine.Destroy()
                obj.topLine = None
                
            if obj.bottomLine:
                obj.bottomLine.Destroy()
                obj.bottomLine = None
                
        # Обновляем данные в дереве объектов
        try:
            self.parent.editor.tree.RefreshData()
        except:
            pass

        if sel:
            # Удаляем свойства помеченные для удаления
            try:
                if sel.list_del_property:
                    sel.list_del_property.sort()
                    sel.list_del_property.reverse()
                    
                    for indx in sel.list_del_property[:-1]:
                        self.PopPropery(indx)
                        
                    self.PopPropery(sel.list_del_property[-1], bRefresh=True)
            except:
                LogLastError('RemoveIndx in SelectEdt(...)')

            # Ставим признак редактирования
            sel.list_del_property = []
            sel.isSelected = True
            sel.value_ctrl.SetSize((0, 1))
            sel.value_ctrl.Enable(False)
            sel.value_ctrl.Refresh()
        
            self.RefreshPos()
            
    def PostSelectProperty(self, indx):
        """
        Иметирует сообщение <EVT_LEFT_DOWN> на нужном свойстве.
        
        @type indx: C{int}
        @param indx: Индекс свойства в редакторе.
        """
        try:
            obj = self.NameValues[indx]
            msg = wx.MouseEvent(wx.wxEVT_LEFT_DOWN)
            msg.SetEventObject(obj.name_ctrl)
            msg.SetId(obj.name_ctrl.GetId())
            msg.m_x, msg.m_y = (0, 0)
            obj.name_ctrl.GetEventHandler().AddPendingEvent(msg)
        except:
            LogLastError('ERROR in PostSelectProperty(indx=%d)' % indx)

    def OnSelect(self, evt):
        """
        """
        # Ищем объект, передавщий сообщение
        for i, obj in enumerate(self.NameValues):
            if evt.GetId() in [obj.value_ctrl.GetId(), obj.name_ctrl.GetId()]:
                self.SelectEdt(i)
                break
        
        evt.Skip()


if __name__ == '__main__':
    app = wx.PySimpleApp(1)
    frame = wx.Frame(None, -1, u'Текст', size=(500, 600),
                     style=wx.DEFAULT_FRAME_STYLE | wx.WANTS_CHARS)
    notebook1 = wx.Notebook(frame, -1, name='notebook1')
    win = icPropWin(notebook1)

    st = {}
    for key in ICFrameStyle.keys():
        if key == 'DEFAULT_FRAME_STYLE':
            st[key] = 1
        else:
            st[key] = 0
    
    fgr = SPC_IC_FRAME['foregroundColor']
    bgr = SPC_IC_FRAME['backgroundColor']
    
    if fgr is None:
        fgr = (0, 0, 0)
        
    win.AddNameValues('name', SPC_IC_FRAME['name'], bRefresh=False)
    win.AddNameValues('EXT', {'PropEditors': 0, 'list': [1, 2, 3, 4],
                              'dict': {}, 'string': 'asdf'},
                      icDefInf.EDT_IMPORT_NAMES, nameType=1, bRefresh=False)
    win.AddNameValues('title', SPC_IC_FRAME['title'], bRefresh=False)
    win.AddNameValues('title', SPC_IC_FRAME['title'], bRefresh=False)
    win.AddNameValues('choice', 'vertical', icDefInf.EDT_CHOICE,
                      {'choices': ['vertical', 'horizontal']}, bRefresh=False)
    win.AddNameValues('title', SPC_IC_FRAME['title'], bRefresh=False)
    win.AddNameValues('title', SPC_IC_FRAME['title'], bRefresh=False)
    win.AddNameValues('title', SPC_IC_FRAME['title'], bRefresh=False)
    win.AddNameValues('title', SPC_IC_FRAME['title'], bRefresh=False)
    win.AddNameValues('title', SPC_IC_FRAME['title'], bRefresh=False)

    win.AddNameValues('position', SPC_IC_FRAME['position'], icDefInf.EDT_POINT, bRefresh=False)
    win.AddNameValues('size', SPC_IC_FRAME['size'], icDefInf.EDT_SIZE, bRefresh=False)
    win.AddNameValues('foregroundColor', fgr, icDefInf.EDT_COLOR, bRefresh=False)
    win.AddNameValues('backgroundColor', bgr, icDefInf.EDT_COLOR, bRefresh=False)
    win.AddNameValues('style', st, icDefInf.EDT_COMBINE, bRefresh=False)
    win.AddNameValues('init', """Script
    kljdljlkfjdskldsf
    fklkdl;ksfl;ks;afkds""", icDefInf.EDT_PY_SCRIPT, bRefresh=False)
    win.AddNameValues('font', SPC_IC_FONT, icDefInf.EDT_FONT, nameType=1, bRefresh=False)
    win.AddNameValues('new property', '', icDefInf.EDT_NEW_PROPERTY, nameType=2)
    
    notebook1.AddPage(imageId=-1, page=win, select=True, text='\xca\xee\xed\xf1\xf2\xf0\xf3\xea\xf2\xee\xf0')
    frame.SetSize((500, 500))
    
    frame.Show(True)
    app.MainLoop()
