#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
from ic.PropertyEditor.images import grptoolimg

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': u'1', 'obj_module': None, 'keyDown': u'None', 'show': u'1', 'init_expr': u'WrapperObj.init_view(self)', 'borderRightColor': (100, 100, 100), 'child': [], 'states': [0, 1, 2], 'mouseClick': u'WrapperObj.OnIndicatorMouseClick(evt)', 'images': [], 'borderTopColor': (100, 100, 100), 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': u'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'alignment': u"('left', 'middle')", 'size': (243, 24), 'style': 0, 'foregroundColor': (59, 59, 59), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'alignmentImg': u"('left', 'middle')", 'source': u'None', 'backgroundColor': None, 'isSort': False, 'type': u'IndicatorState', 'res_module': None, 'enable': True, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': 'e5bcd7cdd52872382613d6f53914b2e1', 'moveAfterInTabOrder': u'', 'bgrImage': None, 'flag': 8192, 'alias': u'None', 'recount': u'None', 'path': u'', 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'borderStyle': u'None', 'borderStep': 0, 'borderLeftColor': (100, 100, 100), 'roundConer': [0, 0, 0, 0], 'name': u'groupTitle', 'data_name': None, 'borderBottomColor': (100, 100, 100), 'refresh': u'None', 'borderWidth': 1, 'position': (0, 0), 'backgroundType': 1, 'onInit': None}

#   Version
__version__ = (1, 1, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'ToolGroupPanel'


class ToolGroupPanel(icobjectinterface.icObjectInterface):
    """
    Панель группы.
    """
    def __init__(self, parent, sizer=None, label='', panel=None):
        #   Указатель на панель группы
        self._panel = panel
        #   Указатель на сайзер, где располагается панель групп
        self._sizer = sizer
        #   Указатель на главную панель, где располагаются группы
        self._mainPanel = None
        # Картинки по умолчанию
        if not resource['images']:
            resource['images'] = [grptoolimg.open_group.GetBitmap(), grptoolimg.close_group.GetBitmap(),
                                  grptoolimg.close_group2.GetBitmap()]

        icobjectinterface.icObjectInterface.__init__(self, parent, resource)        
        if 'left' in resource['alignment']:
            label = u'       %s' % label
        self.SetLabel(label)
        
        if sizer:
            sizer.Add(self.object, 0, wx.EXPAND)
        if panel and sizer:
            sizer.Add(panel, 1, wx.EXPAND)

    def init_view(self, obj):
        """
        """
        import ic.utils.graphicUtils as grph
        obj.SetState(1)

        clr1 = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)
        clr2 = grph.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), 50)
        bnd = grph.AdjustColour(clr1, -60)
        bnd2 = grph.AdjustColour(clr2, 50)

        obj.SetBackgroundColour(clr1)
        obj.bgr2 = clr2

        if obj.imageState and wx.Platform == '__WXMSW__':
            obj.imageState.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))
            
        obj.leftColor = bnd
        obj.topColor = wx.WHITE
        obj.rightColor = bnd
        obj.bottomColor = bnd    

    def GetMainPanel(self):
        """
        Возвращает указатель на главную панель,
        где располагаются группы.
        """
        return self._mainPanel

    def GetPanel(self):
        """
        Возвращает указатель на панель группы.
        """
        return self._panel

    def GetSizer(self):
        """
        Возвращает указатель на сайзек панели групп.
        """
        return self._sizer

    def Expand(self):
        """
        Открывает группу.
        """
        panel = self.GetPanel()
        bsz = self.GetSizer()
        ob = self.getObject()
        if panel and bsz:
            if self.GetMainPanel():
                self.GetMainPanel().PanelGroupsRefresh()
            ob.SetState(1)
            bsz.Show(panel)
            bsz.Layout()

    def Hide(self):
        """
        Закрывает группу.
        """
        panel = self.GetPanel()
        bsz = self.GetSizer()
        ob = self.getObject()
        if panel and bsz:
            if self.GetMainPanel():
                self.GetMainPanel().PanelGroupsRefresh()
            ob.SetState(0)
            bsz.Hide(panel)
            bsz.Layout()

    def OnIndicatorMouseClick(self, evt):
        """
        Обработка нажатия левой кнопки мыши на индикаторе.
        """
        panel = self.GetPanel()
        bsz = self.GetSizer()
        ob = self.getObject()
        if panel and bsz:
            if self.GetMainPanel():
                self.GetMainPanel().PanelGroupsRefresh()
            if ob.GetState() == 0:
                ob.SetState(1)
                bsz.Show(panel)
                panel.Refresh()
            else:
                ob.SetState(0)
                bsz.Hide(panel)
            bsz.Layout()

    def Refresh(self):
        self.getObject().Refresh()
        if self.GetPanel():
            self.GetPanel().Refresh()

    def SetMainPanel(self, panel):
        """
        Устанавливает указатель на главную панель, где располагаются группы.
        """
        self._mainPanel = panel

    def SetPanel(self, panel):
        """
        Устанавливает панель группы.
        """
        self._panel = panel

    def SetLabel(self, text):
        """
        Устанавливает подпись группы.
        """
        self.getObject().SetLabel(text)
        self.getObject().Refresh()


def test(par=0):
    """
    Тестируем класс ToolGroupPanel.
    """
    from ic.components import ictestapp
    import ic.components.sizers.icboxsizer as icboxsizer
    import ic.components.icwxpanel as icwxpanel
    import ic.components.user.icscrolledpanel as icscrolledpanel
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = icwxpanel.icWXPanel(frame, -1, {'backgroundColor': (245, 245, 245)})

    ################
    # Тестовый код #
    ################
    pn1 = icwxpanel.icWXPanel(win, -1, {'backgroundColor': (200, 0, 0)})
    pn2 = icwxpanel.icWXPanel(win, -1, {'backgroundColor': (0, 200, 0)})
    pn3 = icscrolledpanel.icScrolledPanel(win, -1, {'backgroundColor': (0, 0, 200)})
    b1 = wx.Button(pn3, -1, 'b1', size=(100, 200))
    bsz = icboxsizer.icBoxSizer(win, -1, {})
    g1 = ToolGroupPanel(win, bsz, 'Group 1', pn1)
    g2 = ToolGroupPanel(win, bsz, 'Group 2', pn2)
    g3 = ToolGroupPanel(win, bsz, 'Group 3', pn3)
    g3.Hide()
    win.SetSizer(bsz)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
