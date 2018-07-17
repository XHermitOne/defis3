#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import ic.components.icwxpanel as icwxpanel

_ = wx.GetTranslation

class icStyleToolPanel(icwxpanel.icWXPanel):

    BGR_PANEL_CLR = (140, 150, 160)
    FGR_PANEL_CLR = (100, 110, 120)
    PANEL_H = 27

    def __init__(self, parent, *arg, **kwarg):
        """
        Конструктор.
        """
        self.parent = parent
        bgr_clr = icStyleToolPanel.BGR_PANEL_CLR
        icwxpanel.icWXPanel.__init__(self, parent, -1, 
                                     {'backgroundColor': bgr_clr,
                                      'size': (-1, icStyleToolPanel.PANEL_H)})
        self.SetBorderMode(icStyleToolPanel.FGR_PANEL_CLR, 0)
        self._toolList = []
        self.CreateToolPanel()
        self.designer_panel = kwarg.get('designer_panel', None)
                
    def CreateToolPanel(self):
        """
        Создаем панель инструментов.
        """
        from ic.imglib import newstyle_img
        import ic.components.custom.ictoggleimagebutton as ictoggleimagebutton

        szr = wx.BoxSizer()
        self.flagCompDict = {}
        btn_sz = (23, 23)
        bgr_clr = self.BGR_PANEL_CLR
        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.align_left,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('Align Left')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 2)
        img_btn.SetBackgroundColour(bgr_clr)
        self.flagCompDict[wx.ALIGN_LEFT] = img_btn
        self.AddTool(img_btn)

        #   Так как wx.ALIGN_LEFT == wx.ALIGN_TOP == 0
        self.flagCompDict['left'] = img_btn

        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.align_right,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('Align Right')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.flagCompDict[wx.ALIGN_RIGHT] = img_btn
        self.AddTool(img_btn)
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.align_top,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('Align Top')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.flagCompDict[wx.ALIGN_TOP] = img_btn
        self.AddTool(img_btn)
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.align_bottom,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('Align Bottom')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.flagCompDict[wx.ALIGN_BOTTOM] = img_btn
        self.AddTool(img_btn)
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.align_vcenter,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('Centred Vertical')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.flagCompDict[wx.ALIGN_CENTER_VERTICAL] = img_btn
        self.AddTool(img_btn)

        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.align_hcenter,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('Centred Horizontal')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.flagCompDict[wx.ALIGN_CENTER_HORIZONTAL] = img_btn
        self.AddTool(img_btn)
        
        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.grow,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('EXPAND style')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.flagCompDict[wx.EXPAND] = img_btn
        self.AddTool(img_btn)

        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.proportional,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('PROPORTIONAL Style')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.flagCompDict['proportion'] = img_btn
        self.AddTool(img_btn)

        # Обновление дизайнера
        img_btn = ictoggleimagebutton.icToggleImageButton(self, -1,
                                                          {'image': newstyle_img.refresh3,
                                                           'backgroundColor': bgr_clr,
                                                           'size': btn_sz,
                                                           'shortHelpString': _('Refresh')})
        szr.Add(img_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        img_btn.Bind(wx.EVT_BUTTON, self.OnRefresh, id=img_btn.GetId())
        self.refresh_tool = img_btn
        
        szr.Add((5,27), 0, wx.ALIGN_CENTER_VERTICAL)
        self.AddTool(img_btn)
        
        self.SetSizer(szr)

    def AddTool(self, tool):
        """
        Добавлят инструмент в с надор инструментов.
        @type tool: C{ictoggleimagebutton.icToggleImageButton}
        @param tool: Инструмент палитры.
        """
        self._toolList.append(tool)
        tool.Bind(wx.EVT_BUTTON, self.OnMouseClick, id=tool.GetId())

    def GetGraphEditor(self):
        """
        Возвращает указатель на графический редактор.
        """
        return self.designer_panel

    def OnRefresh(self, evt):
        """
        Обновление дизайнера.
        """
        self.GetGraphEditor().GetPointer().open_formeditor_doc()
        # В момент обновления панель может быть разрушена
        try:
            self.refresh_tool.SetToggle(False)
            evt.Skip()
        except:
            pass
        
    def OnMouseClick(self, evt):
        """
        Обрабатывет сообщение.
        """
        obj = evt.GetEventObject()
        flag = self.GetFlag()
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
    
    def GetToolList(self):
        """
        Возвращает список инструментов.
        """
        return self._toolList
    
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
        сайзере.
        """
        return self.flagCompDict['proportion'].GetToggle()
        
    def GetToggleType(self):
        """
        Возвращает выбранный тип компонента.
        """
        for tool in self.GetToolList():
            if tool.GetToggle() and tool not in self.flagCompDict.values():
                return tool.shortHelpString
        return None


def test(par=0):
    """
    Тестируем класс.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)

    frame = wx.Frame(None, -1, 'icWXPanel Test')
    win = icStyleToolPanel(frame)
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
