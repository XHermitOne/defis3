#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс панели инструментов редактора форм.
"""

import wx
from ic.imglib import common
import ic.components.sizers.icstaticboxsizer as icstaticboxsizer
import ic.components.sizers.icboxsizer as icboxsizer
import ic.components.custom.ictoggleimagebutton as ictoggleimagebutton
import ic.PropertyEditor.icDefInf as icDefInf
from ic.log import log

_ = wx.GetTranslation

if wx.VERSION > (2, 8, 11, 10):
    wx.Colour = wx.Colour

class icPanelTool(wx.Panel):
    """
    Класс панели инструментов.
    """
    PANEL_BGR_TUPL = (245, 245, 245)
    PANEL_BGR_COLOR = wx.Colour(*PANEL_BGR_TUPL)

    def addStyleGroup(self):
        """
        Добавляет на панель инструменты стилей.
        """
        # Словарь указателей на инструменты стилей
        self.flagCompDict = {}
        # Инструменты стилей
        sbsz = icstaticboxsizer.icStaticBoxSizer(self.panel, -1, {'label': u'Стили'})
        # Ряд 1
        szr = icboxsizer.icBoxSizer(self.panel, -1, {'layout': 'horizontal'})

        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtAlignLeft,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('Align Left')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict[wx.ALIGN_LEFT] = img_btn
        self.AddTool(img_btn)

        # Так как wx.ALIGN_LEFT == wx.ALIGN_TOP == 0
        self.flagCompDict['left'] = img_btn

        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtAlignRight,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('Align Right')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict[wx.ALIGN_RIGHT] = img_btn
        self.AddTool(img_btn)
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtAlignTop,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('Align Top')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict[wx.ALIGN_TOP] = img_btn
        self.AddTool(img_btn)
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtAlignBottom,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('Align Bottom')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict[wx.ALIGN_BOTTOM] = img_btn
        self.AddTool(img_btn)
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtVCenter,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('Centred Vertical')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict[wx.ALIGN_CENTER_VERTICAL] = img_btn
        self.AddTool(img_btn)
        
        sbsz.Add(szr, 0, wx.EXPAND)

        # Ряд 2
        szr = icboxsizer.icBoxSizer(self.panel, -1, {'layout': 'horizontal'})
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtHCenter,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('Centred Horizontal')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict[wx.ALIGN_CENTER_HORIZONTAL] = img_btn
        self.AddTool(img_btn)

        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtGrow,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('GROW style')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict[wx.GROW] = img_btn
        self.AddTool(img_btn)

        # Так как wx.GROW == wx.EXPAND
        self.flagCompDict['grow'] = img_btn
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtExpand,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('EXPAND style')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict[wx.EXPAND] = img_btn
        self.AddTool(img_btn)
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                          {'image': common.imgEdtProportion,
                                                           'size': (25, 25),
                                                           'shortHelpString': _('Proportional Style')})
        szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
        self.flagCompDict['proportion'] = img_btn
        self.AddTool(img_btn)
        
        sbsz.Add(szr, 0, wx.EXPAND)
        self.sz.Add(sbsz, 0, wx.EXPAND)
        
    def BindTools(self):
        lst = self.GetToolList()
        for tool in lst:
            tool.Bind(wx.EVT_BUTTON, self.OnMouseClick, id=tool.GetId())

    def init_groups_horz(self):
        """
        Заполняет горизонтальную панель инструментами по группам.
        """
        grp_keys = self.groups.keys()
        grp_keys.sort()

        for grp in grp_keys:
            val = self.groups[grp]

            # Находим описания компонентов данной группы
            tool_list = [x for x in self.objects.values() if x[0] == grp]

            # Определяем количество рядов инструментов в группе
            nline = 2
            wLine = len(tool_list)/nline + 1
         
            #
            if len(tool_list) > 0:
                self.sz.Add((5, 5))
                sbsz = icstaticboxsizer.icStaticBoxSizer(self.panel, -1,
                                                         {'label': val,
                                                          'layout': 'vertical'})

                for line in range(nline):
                    szr = icboxsizer.icBoxSizer(self.panel, -1, {'layout': 'horizontal'})
                    for indx in range(wLine):
                        try:
                            obj = tool_list[line * wLine + indx]
                            img = obj[1]
                            spc = obj[3]
                            if isinstance(img, int):
                                img = common.imgPage

                            img_btn = ictoggleimagebutton.icToggleImageButton(self.panel, -1,
                                                                              {'image': img,
                                                                               'size': (25, 25),
                                                                               'shortHelpString': str(spc['type'])})
                            
                            szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
                            self.AddTool(img_btn)
                        except:
                            pass
                        
                    sbsz.Add(szr, 0, wx.EXPAND)

                # Добавляем в главный сайзер
                self.sz.Add(sbsz, 0, wx.EXPAND)
        self.BindTools()

    def init_groups_vert2(self):
        """
        Заполняет вертикальную панель инструментами по группам.
        """
        from ic.components.user import icscrolledpanel
        from ic.components.user.objects import ictoolgrouppanel
        
        # Добавляем инструменты группы

        # Создаем панели групп
        grp_keys = self.groups.keys()
        grp_keys.sort()

        for grp in grp_keys:
            val = self.groups[grp]
            pnl = icscrolledpanel.icScrolledPanel(self.panel, -1, {'size': (-1, 50),
                                                                   'backgroundColor': self.PANEL_BGR_TUPL})
            g1 = ictoolgrouppanel.ToolGroupPanel(self.panel, self.sz, val, pnl)
            self._groupPanelList.append(g1)
            g1.SetMainPanel(self)
            g1.Hide()
            
            sbsz = wx.BoxSizer(wx.VERTICAL)
            pnl.SetSizer(sbsz)
            
            # Находим описания компонентов данной группы
            tool_list = [x for x in self.objects.values() if x[0] == grp]

            # Определяем количество рядов инструментов в группе
            wLine = 1
            nline = len(tool_list)/wLine + 1
         
            if len(tool_list) > 0:
                for line in range(nline):
                    szr = wx.BoxSizer()
        
                    for indx in range(wLine):
                        try:
                            obj = tool_list[line*wLine + indx]
                            img = obj[1]
                            spc = obj[3]

                            if isinstance(img, int):
                                img = common.imgPage

                            label = ' %s' % spc['type']
                            w = 25
                            img_btn = ictoggleimagebutton.icToggleImageButton(pnl, -1,
                                                                              {'image': img,
                                                                               'size': (w, 25),
                                                                               'backgroundColor': self.PANEL_BGR_TUPL,
                                                                               })
                            img_btn.vtype = spc['type']
                            lab_ctrl = wx.StaticText(pnl, label=label)
                            szr.Add(img_btn, 0, wx.ALIGN_BOTTOM)
                            self.AddTool(img_btn)
                            szr.Add(lab_ctrl, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                            
                        except:
                            pass
                        
                    sbsz.Add(szr, 0, wx.EXPAND | wx.LEFT, 20)
                    
            # Добавляем в главный сайзер
        self.BindTools()
        
    def __init__(self, parent, title, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, GroupsInfo=None, ObjectsInfo=None, layout='horiz'):
        """
        Конструктор создания панели инструментов.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type pos: C{wx.Point}
        @param pos: Расположение панели.
        @type size: C{wx.Size}
        @param size: Размер панели.
        @type style: C{int}
        @param style: Стиль окна панели.
        @type GroupsInfo: C{dictionary}
        @param GroupsInfo: Описание групп.
        @type ObjectsInfo: C{dictionary}
        @param ObjectssInfo: Описание объектов.
        """
        wx.Panel.__init__(self, parent, -1)
        self.SetBackgroundColour(self.PANEL_BGR_COLOR)
        self.panel = self
        # Указатель на графический редактор.
        self._grapEditor = None
        # Словарь указателей на инструменты стилей
        self.flagCompDict = {}
        # Список инструментов
        self._toolList = []
        # Список панелей групп
        self._groupPanelList = []
        from ic.PropertyEditor import icResTree
        
        if not GroupsInfo:
            GroupsInfo = icDefInf.GroupsInfo
        if not ObjectsInfo:
            ObjectsInfo = icResTree.GetObjectsInfo()
            
        self.groups = GroupsInfo
        self.objects = ObjectsInfo
        self.layout = layout
        self.flagCompDict = {}
        self.layout = layout
        self.sz = None
        self.CreateGrpTools()
        
        # Определяем обработчики событий
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def CreateGrpTools(self):
        # Заполняем панель стандартными группами инструментов
        if self.layout == 'vertical':
            self.sz = sz = wx.BoxSizer(wx.VERTICAL)
            self.init_groups_vert2()
        else:
            self.sz = sz = wx.BoxSizer(wx.HORIZONTAL)
            self.init_groups_horz()
        
        self.SetSizer(sz)
        sz.Layout()

    def GetToolPanel(self):
        """
        Возвращает указатель на панель инструментов.
        """
        return self

    def AddTool(self, tool):
        """
        Добавлят инструмент в с надор инструментов.
        @type tool: C{ictoggleimagebutton.icToggleImageButton}
        @param tool: Инструмент палитры.
        """
        self._toolList.append(tool)
        
    def GetToolList(self):
        """
        Возвращает список инструментов.
        """
        return self._toolList

    def GetFlag(self):
        """
        Возвращает стиль расположения компонета в сайзере.
        """
        flag = 0
        for key, obj in self.flagCompDict.items():
            if key not in ['proportion', 'left'] and obj.GetToggle():
                if key == 'grow':
                    flag = flag | wx.GROW
                else:
                    flag = flag | key
        return flag

    def OnSize(self, evt):
        evt.Skip()
        
    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnMouseClick(self, evt):
        """
        Обрабатывет сообщение.
        """
        obj = evt.GetEventObject()
        if obj in self.flagCompDict.values():
            flag = self.GetFlag()
            prop = self.GetProportionStyle()
            edt = self.GetGraphEditor()
            if edt and edt.selectedObj:
                edt.ChangeResProperty(edt.selectedObj, 'flag', flag, bRefresh=True)
                edt.ChangeSelItemProperty('flag', flag)
                edt.ChangeResProperty(edt.selectedObj, 'proportion', int(prop), bRefresh=True)
                edt.ChangeSelItemProperty('proportion', int(prop))
                
            evt.Skip()
            return

        for tool in self.GetToolList():
            if tool != obj and tool not in self.flagCompDict.values():
                tool.SetToggle(False)
        evt.Skip()

    def PanelGroupsRefresh(self):
        """
        Обнавляются все панели групп.
        """
        for pnl in self._groupPanelList:
            pnl.Refresh()

    def SetFlag(self, flag):
        """
        Устанавливает для отображенмя в панели инструментов стиль расположения компонента
        в сайзере.
        @type flag: C{int}
        @param flag: Стиль расположения компонента в сайзере.
        """
        for key, obj in self.flagCompDict.items():
            if key not in ['proportion', 'left', 'grow']:
                if (key == 0 and flag == 0) or (key & flag and key != 0):
                    obj.SetToggle(True)
                else:
                    obj.SetToggle(False)
            elif key == 'left':
                if flag == 0:
                    obj.SetToggle(True)
                else:
                    obj.SetToggle(False)
                    
    def SetProportionStyle(self, prop):
        """
        Устанавливает признак пропорциональности при размещении компонента в сайзере.
        @type prop: C{bool}
        @param prop: Признак пропорциональность при размещении компонента в сайзере.
        """
        self.flagCompDict['proportion'].SetToggle(prop)
    
    def GetProportionStyle(self):
        """
        Возвращает признак пропорциональность при размещении компонента в
        сайзере."""
        return self.flagCompDict['proportion'].GetToggle()
        
    def GetToggleType(self):
        """
        Возвращает выбранный тип компонента.
        """
        for tool in self.GetToolList():
            if tool.GetToggle() and tool not in self.flagCompDict.values():
                return getattr(tool, 'vtype', None) or tool.shortHelpString
        return None
        
    def ReleaseToggleType(self):
        """
        Чистит панель компонентов.
        """
        for tool in self.GetToolList():
            if tool not in self.flagCompDict.values():
                tool.SetToggle(False)

    def SetGraphEditor(self, edt):
        """
        Устанавливает указатель на графический редактор.
        @type edt: C{icBackground}
        @param edt: Указатель на графический редактор.
        """
        self._grapEditor = edt

    def ReleaseGraphEditor(self):
        """
        Освобождает указатель на графический редактор.
        """
        self._grapEditor = None
        
    def GetGraphEditor(self):
        """
        Возвращает указатель на графический редактор.
        """
        return self._grapEditor
        
    def EnableType(self, typeObj, bEnable=True):
        """
        Активируем кнопки определенного типа.
        """
        for tool in self.GetToolList():
            if tool not in self.flagCompDict.values() and \
                    (tool.shortHelpString == typeObj or getattr(tool, 'vtype', None) == typeObj):
                tool.Enable(bEnable)
                return True
        return False

    def EnableAllType(self, bEnable=True):
        """
        Активируем все кнопки.
        """
        for tool in self.GetToolList():
            if tool not in self.flagCompDict.values():
                tool.Enable(bEnable)
        return True
                
    def EnableCanAddObj(self, typeObj, bEnable=True):
        """
        Активируем кнопки разрешенных компонентов.
        """
        if not self.objects:
            return

        canAdd = self.objects[typeObj][4]
        if len(self.objects[typeObj]) > 5:
            notCanAdd = self.objects[typeObj][5]
        else:
            notCanAdd = []
        
        for key, val in self.objects.items():
            if isinstance(canAdd, list) and key in canAdd:
                self.EnableType(key, True)
            elif isinstance(canAdd, list) and key not in canAdd:
                self.EnableType(key, False)
            elif (canAdd == -1 or canAdd is None) and key in notCanAdd:
                self.EnableType(key, False)
            elif (canAdd == -1 or canAdd is None):
                self.EnableType(key, True)


class icPanelToolFrame(wx.MiniFrame):
    """
    Фрейм панели инструментов.
    """

    def __init__(self, parent, title, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, GroupsInfo=None, ObjectsInfo=None, layout='horiz'):
        """
        Конструктор создания панели инструментов.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type pos: C{wx.Point}
        @param pos: Расположение панели.
        @type size: C{wx.Size}
        @param size: Размер панели.
        @type style: C{int}
        @param style: Стиль окна панели.
        @type GroupsInfo: C{dictionary}
        @param GroupsInfo: Описание групп.
        @type ObjectsInfo: C{dictionary}
        @param ObjectssInfo: Описание объектов.
        """
        wx.MiniFrame.__init__(self, parent, -1, title, pos, size, style | wx.STAY_ON_TOP)
        self._toolpanel = icPanelTool(self, title, pos, size, style, GroupsInfo, ObjectsInfo, layout)
        
        if layout == 'vertical':
            self.SetSize((150, 565))
        else:
            self.SetSize((800, 95))
            
    def GetToolPanel(self):
        """
        Возвращает указатель на панель инструментов.
        """
        return self._toolpanel


def test(par=0):
    """
    Тестируем класс icPanelToolFrame.
    """
    from ic.components import ictestapp
    from ic.PropertyEditor import icResTree
    app = ictestapp.TestApp(par)
    common.img_init()
    icResTree.InitObjectsInfo()
    frame = icPanelToolFrame(None, 'icPanelTool Test', layout='vertical')
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    """
    Тестируем класс icPanelToolFrame.
    """
    test()
