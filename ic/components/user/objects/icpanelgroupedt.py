#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
import ic.utils.graphicUtils as grph

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': u'1', 'obj_module': None, 'show': u'1', 'recount': u'None', 'refresh': u'None', 'border': 0, 'size': wx.Size(378, 322), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'61967f3ea8f4cc8223b1574c176c0462', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'activate': u'1', 'obj_module': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': u'BoxSizer', 'res_module': None, 'hgap': u'0', 'description': None, '_uuid': u'f315fe306cdbfe61a47a3c4409b854e3', 'flag': 0, 'child': [{'activate': u'1', 'obj_module': None, 'show': u'1', 'init_expr': u"GetInterface().init_title(self, _('Project Tree'))", 'borderRightColor': (100, 100, 100), 'child': [{'activate': u'0', 'obj_module': None, 'show': u'1', 'hlp': u'None', 'refresh': u'[]', 'file': u"@import ic.imglib.common as common\n_resultEval = common.icImageLibName('Prj.png')\r\n", 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': u'None', 'backgroundColor': None, 'type': u'Image', 'res_module': None, 'description': None, '_uuid': '2b2067272e93f69180f66e2a4c4a16b0', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': u'[]', 'field_name': u'None', 'name': u'DefaultName_1629', 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (18, 4), 'onInit': None}], 'states': [0, 1, 2], 'mouseClick': u"obj = _dict_obj['projectPanel']\nbsz = _dict_obj['bsz']\r\n\nif self.GetState() == 0:\n    self.SetState(1)\n    bsz.Show(obj)\nelse:\n    self.SetState(0)\n    #obj.Show(False)\r\n    bsz.Hide(obj)\r\nbsz.Layout()", 'images': [u'Down.png', u'nextCorel.png'], 'borderTopColor': (100, 100, 100), 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (211, 24), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'alias': u'None', 'component_module': None, 'proportion': 0, 'label': u'\u0414\u0435\u0440\u0435\u0432\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0430', 'alignmentImg': "('left', 'middle')", 'source': u'None', 'backgroundColor': (243, 242, 233), 'isSort': False, 'type': u'IndicatorState', 'res_module': None, 'enable': True, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': '9ae24597ff2deacd04e35efe9a9e976a', 'style': 0, 'bgrImage': None, 'flag': 8192, 'recount': u'None', 'path': u'@import ic.imglib.common as common\r\n_resultEval = common.path\r\n#C:\\Python23\\Lib\\site-packages\\ic\\imglib\\common\\', 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'borderStyle': u'None', 'borderStep': 0, 'borderLeftColor': (100, 100, 100), 'roundConer': [0, 0, 0, 0], 'name': u'projectTitle', 'data_name': None, 'borderBottomColor': (100, 100, 100), 'keyDown': u'None', 'borderWidth': 1, 'position': wx.Point(0, 0), 'backgroundType': 1, 'onInit': None, 'refresh': u'None'}, {'activate': u'1', 'obj_module': None, 'show': u'1', 'recount': u'None', 'refresh': u'None', 'border': 0, 'size': (243, 150), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'alias': u'None', 'component_module': None, 'proportion': 1, 'source': u'None', 'onLeftMouseClick': None, 'backgroundColor': (255, 255, 255), 'type': u'Panel', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': u'320e9295629dce3627abbcb7ca086f1c', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'hgap': 0, 'style': 0, 'activate': u'1', 'layout': u'vertical', 'name': u'projectBSZ', 'position': (58, 36), 'type': u'BoxSizer', '_uuid': u'6e625124e08168272f6bed41367172c6', 'proportion': 0, 'alias': u'None', 'flag': 0, 'init_expr': u'None', 'child': [{'style': 0, 'activate': u'1', 'prim': u'', 'name': u'default_1114', '_uuid': u'b94f78541a31776b6bf917cf0f96884f', 'alias': u'None', 'init_expr': u'None', 'child': [], 'type': u'Group'}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'projectPanel', 'data_name': None, 'keyDown': None, 'init_expr': u'None', 'position': wx.Point(0, 24), 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': u'1', 'init_expr': u"return GetInterface().init_title(self, _('Resource Editor'))\r\n'''\r\nimport wx\r\nimport ic.utils.graphicUtils as grph\r\nself.SetState(1)\r\n\r\n#self.SetRoundCorners((1,1,1,1))\r\n\r\nclr1 = grph.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), -50)\r\nclr2 = grph.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), 50)\r\nbnd = grph.AdjustColour(clr1, -60)\r\n\r\n#clr = self.GetParent().GetBackgroundColour()\r\n#clrn = grph.GetMidColor(clr, wx.Colour(255,255,255), 0.5)\r\nself.SetBackgroundColour(clr1)\r\nself.bgr2 = clr2\r\n\r\nif self.imageState:\r\n    self.imageState.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))\r\n\r\nself.leftColor = bnd\r\nself.topColor = bnd\r\nself.rightColor = bnd\r\nself.bottomColor = bnd\r\n'''", 'borderRightColor': (100, 100, 100), 'child': [{'activate': u'0', 'obj_module': None, 'show': u'1', 'hlp': u'None', 'keyDown': u'None', 'file': u'@import ic.imglib.common as common\r\n_resultEval = common.imgEdtResource', 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': u'None', 'backgroundColor': None, 'type': u'Image', 'res_module': None, 'description': None, '_uuid': 'd05e9615daeee522b14ed6fe15879572', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': u'[]', 'field_name': u'None', 'name': u'DefaultName_1629_1430', 'refresh': u'[]', 'alias': u'None', 'init_expr': u'None', 'position': (18, 4), 'onInit': None}], 'states': [0, 1, 2], 'mouseClick': u"bsz = _dict_obj['bsz']\r\ntry: \r\n    obj = _dict_obj['resourcePanel']\r\nexcept:\r\n    obj = None\r\n\r\nif self.GetState() == 0:\r\n    self.SetState(1)\r\n    if obj:\r\n        bsz.Show(obj)\r\nelse:\r\n    self.SetState(0)\r\n    if obj:\r\n        bsz.Hide(obj)\r\n\r\nbsz.Layout()\r\n", 'images': [u'Down.png', u'nextCorel.png'], 'borderTopColor': (100, 100, 100), 'font': {'style': 'bold', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'alignment': u"('centred', 'middle')", 'size': (243, 24), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'alias': u'None', 'component_module': None, 'proportion': 0, 'label': u'\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0440\u0435\u0441\u0443\u0440\u0441\u043e\u0432', 'alignmentImg': u"('left', 'middle')", 'source': u'None', 'backgroundColor': (243, 242, 233), 'isSort': False, 'type': u'IndicatorState', 'res_module': None, 'enable': True, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': '0568f380d5305be563d80812377976c6', 'style': 0, 'bgrImage': None, 'flag': 8192, 'recount': u'None', 'path': u'@import ic.imglib.common as common\n_resultEval = common.path\n\n#C:\\Python23\\Lib\\site-packages\\ic\\imglib\\common\\', 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'borderStyle': u'None', 'borderStep': 0, 'borderLeftColor': (100, 100, 100), 'roundConer': [0, 0, 0, 0], 'name': u'resourceTitle', 'data_name': None, 'borderBottomColor': (100, 100, 100), 'keyDown': u'None', 'borderWidth': 1, 'position': wx.Point(0, 24), 'backgroundType': 1, 'onInit': None, 'refresh': u'None'}, {'activate': u'1', 'obj_module': None, 'show': u'1', 'recount': u'None', 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 2, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (255, 255, 255), 'type': u'Panel', 'res_module': None, 'description': None, 'onClose': None, '_uuid': u'6679e60fb6995f529d92bc662941dc51', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'hgap': 0, 'style': 0, 'activate': u'1', 'layout': u'vertical', 'name': u'resourceBSZ', 'position': (0, 0), 'type': u'BoxSizer', '_uuid': u'e36a34489958c40c554053c3887ab286', 'proportion': 0, 'alias': u'None', 'flag': 0, 'init_expr': u'None', 'child': [{'activate': u'0', 'show': u'1', 'keyDown': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'layout': u'horizontal', 'win2': {'activate': '1', 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'Panel', 'onClose': None, '_uuid': 'd2a44d85ae0cb89ff0c8ceb6db3f3e32', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': '1', 'layout': 'vertical', 'name': 'DefaultName_2090_1695', 'position': (66, 23), 'type': 'BoxSizer', '_uuid': 'f8d24f035d936ffd45480015c76526a1', 'proportion': 1, 'alias': 'None', 'flag': 8192, 'init_expr': 'None', 'child': [{'activate': '1', 'show': '1', 'selPageColor': (200, 200, 200), 'child': [], 'onSelectTitle': None, 'titles': ['page1', 'page2', 'page3', 'page4'], 'refresh': 'None', 'images': [], 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (241, 26), 'moveAfterInTabOrder': '', 'foregroundColor': (128, 128, 128), 'span': (1, 1), 'proportion': 0, 'source': 'None', 'backgroundColor': (243, 243, 243), 'type': 'TitlesNotebook', '_uuid': '104d44fab7781da61ba71c4ee1c4e87b', 'style': 0, 'flag': 8192, 'recount': 'None', 'path': '', 'name': 'NB', 'icDelButton': 1, 'keyDown': None, 'alias': 'None', 'init_expr': 'None', 'position': (0, 0)}, {'line_color': (200, 200, 200), 'activate': '1', 'show': '1', 'cols': [{'activate': 1, 'ctrl': None, 'pic': 'S', 'getvalue': '', 'style': 0, 'label': 'col', 'width': 50, 'init': None, 'valid': None, 'type': 'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'shortHelpString': '', '_uuid': None, 'recount': None, 'hlp': None, 'name': 'default_3172', 'setvalue': '', 'attr': 'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'keyDown': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'delRec': None, 'row_height': 20, 'selected': None, 'proportion': 1, 'init': None, 'label': 'Grid', 'source': None, 'getattr': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': 'GridDataset', 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'fixColSize': 0, 'post_del': None, 'post_init': None, '_uuid': 'be4767bbde62d487342d97068767ceb4', 'style': 0, 'docstr': 'ic.components.icgrid.html', 'flag': 8192, 'recount': 'None', 'label_attr': {'foregroundColor': (255, 255, 255), 'name': '', '_uuid': None, 'backgroundColor': (100, 100, 100), 'font': {'style': None, 'name': 'defaultFont', 'family': None, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'label_attr', 'alignment': ('left', 'middle')}, 'name': 'default_3039', 'label_height': 20, 'changed': None, 'refresh': 'None', 'alias': 'None', 'init_expr': 'None', 'position': (74, 17)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': 'defaultWindow_1549', 'refresh': None, 'alias': 'None', 'init_expr': 'None', 'position': (-1, -1)}, 'win1': {'activate': '1', 'show': '1', 'recount': 'None', 'refresh': 'None', 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'title': 'default', 'scrollRate': [5, 5], 'proportion': 1, 'source': 'None', 'backgroundColor': None, 'type': 'ScrolledWindow', '_uuid': 'cb5a5e26b0ffbf7c379cb552f1ca0cd2', 'moveAfterInTabOrder': '', 'flag': 8192, 'child': [{'activate': '1', 'show': '1', 'borderRightColor': (100, 100, 100), 'recount': 'None', 'keyDown': None, 'borderTopColor': (250, 250, 250), 'font': {}, 'border': 0, 'alignment': ('centred', 'middle'), 'size': (139, 139), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': '', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': 'HeadCell', 'init_expr': 'None', 'shortHelpString': '', '_uuid': 'c6ae9b16e31ee9d123490e17b50c03c0', 'style': 0, 'flag': 0, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (250, 250, 250), 'name': 'HeadCell_1780', 'borderBottomColor': (100, 100, 100), 'refresh': 'None', 'alias': 'None', 'borderWidth': 1, 'position': (75, 7), 'borderStyle': None}], 'name': 'groupPanel_2130', 'keyDown': 'None', 'alias': 'None', 'init_expr': 'None', 'position': (0, 248)}, 'proportion': 1, 'source': u'None', 'backgroundColor': None, 'type': u'SplitterWindow', 'min_panelsize': 0, '_uuid': u'c192ddd12e9ab8a8b194ced1f7b0e571', 'style': 768, 'docstr': u'ic.components.icsplitter-module.html', 'flag': 8192, 'recount': u'None', 'span': (1, 1), 'name': u'resourceTree_1518', 'refresh': u'None', 'alias': u'None', 'init_expr': u'None', 'position': (-1, -1), 'sash_pos': 100}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'resourcePanel', 'refresh': u'None', 'alias': u'None', 'init_expr': u'None', 'position': wx.Point(0, 139), 'onInit': None}], 'layout': u'vertical', 'name': u'bsz', 'alias': u'None', 'init_expr': u'None', 'position': (62, 32), 'vgap': u'0'}], 'name': u'EditorPanel', 'keyDown': None, 'alias': u'None', 'init_expr': u'None', 'position': (-1, -1), 'onInit': None}

#   Version
__version__ = (1, 1, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icPanelGroupEdt'


class icPanelGroupEdt(icobjectinterface.icObjectInterface):

    def __init__(self, parent):
        """
        Конструктор.
        @param parent: Указатель на родительское окно.
        """
        #   Указатель на редактор проектов
        self._projectEditor = None
        #   Указатель на редактор ресурсов
        self._resourceEditor = None

        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
        self.object.Bind(wx.EVT_SIZE, self.OnSize)

    def init_title(self, obj, label=None):
        """
        Инициализация заголовков.
        @type obj: C{IndicatorState}
        @param obj: Заголовок группы. 
        """
        obj.SetState(1)
        clr1 = grph.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), -50)
        clr2 = grph.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), 50)
        bnd = grph.AdjustColour(clr1, -60)
        obj.SetBackgroundColour(clr1)
        obj.bgr2 = clr2

        if obj.imageState:
            obj.imageState.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))

        obj.leftColor = bnd
        obj.topColor = bnd
        obj.rightColor = bnd
        obj.bottomColor = bnd
        
        if label:
            obj.SetLabel(label)
    
    def OnSize(self, evt):
        """
        Обрабатывает wx.EVT_SIZE.
        """
        self.getObject().Refresh()
        evt.Skip()
        
    def SetProjectEditor(self, edt):
        """
        Устанавливает редактор проектов.
        """
        self._projectEditor = edt
        #   Вставляем в нужный сайзер
        if edt:
            self.GetProjectBSZ().Add(edt, 1, wx.EXPAND)
            self.GetProjectBSZ().SetItemMinSize(edt, (-1, 170))
            
    def GetProjectEditor(self):
        """
        Возвращает редактор проектов.
        """
        return self._projectEditor

    def GetProjectBSZ(self):
        """
        Возвращает сайзер, куда вставляется редактор проекта.
        """
        if 'projectBSZ' in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj']['projectBSZ']

    def GetProjectPanel(self):
        """
        Возвращает панель проекта.
        """
        if 'projectPanel' in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj']['projectPanel']
        
    def SetResourceEditor(self, edt):
        """
        Устанавливает редактор ресурсов.
        """
        self._resourceEditor = edt
        #   Вставляем в нужный сайзер
        if edt:
            self.GetResourceBSZ().Add(edt, 1, wx.EXPAND)

    def GetResourceEditor(self):
        """
        Возвращает редактор ресурсов.
        """
        return self._resourceEditor

    def GetResourceBSZ(self):
        """
        Возвращает сайзер, куда вставляется редактор ресурсов.
        """
        if 'resourceBSZ' in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj']['resourceBSZ']

    def GetResourcePanel(self):
        """
        Возвращает панель проекта.
        """
        if 'resourcePanel' in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj']['resourcePanel']


def test(par=0):
    """
    Тестируем класс icPanelGroupEdt.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')

    ################
    # Тестовый код #
    ################
    win = icPanelGroupEdt(frame)
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
