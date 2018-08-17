# -*- coding:utf-8 -*-

"""
Defis RAD system plugin for Editra IDE.
"""

import sys
import os
import wx
import plugin
import ed_i18n
import ed_glob
import gettext

import iface
from profiler import Profile_Get, Profile_Set
from ic.PropertyEditor import icResTree
from ic.interfaces import editraIdeInterface

__author__ = 'Kolchanov Alexander'
__version__ = (0, 0, 1, 2)

_ = wx.GetTranslation

ID_DEFIS_TOOL = wx.NewId()

PANE_NAME = u'Defis'


def init_locale():
    """
    Initialize the Language Settings.
    """
    the_locale = wx.Locale(ed_i18n.GetLangId(Profile_Get('LANG')))
    if the_locale.GetCanonicalName() in ed_i18n.GetAvailLocales():
        lc = ed_glob.CONFIG['LANG_DIR']+'defis\\'
        wx.GetApp().GetLog()('----- init_locale ----- %s' % lc)
        gettext.bindtextdomain('defis', lc)
        gettext.textdomain('defis')


class DefisProjectPlugin(plugin.Plugin):
    """
    Defis RAD sistem plugin.
    """

    plugin.Implements(iface.MainWindowI)

    def PlugIt(self, parent):
        """
        Implements MainWindowI's PlugIt Method
        """
        init_locale()
        self.main_win = parent
        self._log = wx.GetApp().GetLog()
        if self.main_win is not None:
            self._log('[Defis][info] Installing Defis RAD system plugin')

            view_menu = self.main_win.GetMenuBar().GetMenuByName('view')

            self.menu = view_menu.InsertAlpha(ID_DEFIS_TOOL,
                                              _('Defis'),
                                              _('Defis Sidepanel'),
                                              wx.ITEM_CHECK,
                                              after=ed_glob.ID_PRE_MARK)

            # Интерфейс к IDE
            ifs = editraIdeInterface.EditraIDEInterface(self.main_win)
            self._defis = icResTree.GetProjectEditor(self.main_win, self.main_win, ifs)

            mgr = self.main_win.GetFrameManager()
            mgr.AddPane(self._defis,
                        wx.aui.AuiPaneInfo().Name(PANE_NAME).
                        Caption(_('Defis')).
                        Top().Left().Layer(1).
                        CloseButton(True).MaximizeButton(True).
                        BestSize(wx.Size(300, 150)))
            mgr.Update()

        ed_msg.Subscribe(self.OnUpdate, ed_msg.EDMSG_UI_NB_CHANGED)

    def GetMenuHandlers(self):
        """
        Pass even handler for menu item to main window for management
        """
        return [(ID_DEFIS_TOOL, self.OnShow)]

    def GetUIHandlers(self):
        """
        Pass Ui handlers to main window for management
        """
        return [(ID_DEFIS_TOOL, self.OnUpdateMenu)]

    def OnShow(self, evt):
        """
        Show the pane
        @param evt: wx.MenuEvent
        """
        if evt.GetId() == ID_DEFIS_TOOL:
            mgr = self.main_win.GetFrameManager()
            pane = mgr.GetPane(PANE_NAME)
            pane.Show(not pane.IsShown())
            mgr.Update()
            self.OnShowAUIPane()
        else:
            evt.Skip()

    def OnUpdateMenu(self, evt):
        """
        UpdateUI handler for the panels menu item, to update the check
        mark.
        @param evt: wx.UpdateUIEvent
        """
        pane = self.main_win.GetFrameManager().GetPane(PANE_NAME)
        evt.Check(pane.IsShown())

    def OnShowAUIPane(self):
        """
        Interface method that the main Editra window will call
        When its auimanager does a Show when this window is contained
        within an aui pane. Forces the tree to update.
        """
        self.OnUpdate(force=True)

    def OnUpdate(self, msg=None, force=False):
        """
        Update the ctrl when an action message is sent
        @param msg: Message Object.
        @param force: Force update.
        """
        if not force:
            context = None
            if msg is not None:
                context = msg.GetContext()

            if context is not None and context != self.main_win.GetId():
                return

        # Don't update if panel is not visible
        if not self._ShouldUpdate():
            return

        page = self._GetCurrentCtrl()
        cfname = page.GetFileName()

    def _ShouldUpdate(self):
        """
        Check whether the tree should do an update or not
        @return: bool
        """
        pane = self.main_win.GetFrameManager().GetPane(PANE_NAME)
        if self.main_win.IsExiting() or not pane.IsShown():
            return False
        else:
            return True

    def _GetCurrentCtrl(self):
        """
        Get the current buffer
        """
        return self.main_win.GetNotebook().GetCurrentCtrl()
