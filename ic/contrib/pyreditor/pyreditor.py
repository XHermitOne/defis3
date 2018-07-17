# PyReditor - Advanced Python Regular Expresion Editor
#
# Copyright (c) 2008, 2009
# Primoz Cermelj <primoz.cermelj@gmail.com>
#
# This program is based on RegexEditor.plug-in.py plugin originated from
# Boa Constructor and is licensed under GPL.
# 
# See LICENSE.TXT for license terms.
#----------------------------------------------------------------------------

import re
import sys
import os
import wx
from wx.lib.anchors import LayoutAnchors
import string
from .settings import Settings, ProjFile, Templates
from .commons import *
from .editor import Editor
from .menus import EditInsertMenu
from .commons import SETT_KEYS
from .commons import setpath, set_png
from .commons import STYLE_DEFAULT, LEXER_RE, YELLOW1, YELLOW2, GREEN1, GREEN2
from .commons import RE_FLAGS
from .commons import TEMP_FILE
from .commons import TITLE
from .tmpleditor import Frame1


__version__ = '1.1.4'
__author__ = 'Primoz Cermelj'
__release__ = '06.01.2010'
__authormail__ = 'primoz.cermelj@gmail.com'


def createPyreditor(parent):
    return PyReditorFrm(parent)

[wxID_REGEXEDITORFRM, wxID_REGEXEDITORFRMCLBFLAGS, 
 wxID_REGEXEDITORFRMLCGROUPS, wxID_REGEXEDITORFRMPANEL, 
 wxID_REGEXEDITORFRMPANEL1, wxID_REGEXEDITORFRMPANEL2, 
 wxID_REGEXEDITORFRMRBACTION, wxID_REGEXEDITORFRMSPLITTERWINDOW1, 
 wxID_REGEXEDITORFRMSPLITTERWINDOW2, wxID_REGEXEDITORFRMSTATICBOX1, 
 wxID_REGEXEDITORFRMSTATICBOX2, wxID_REGEXEDITORFRMSTATICBOX3, 
 wxID_REGEXEDITORFRMSTATICTEXT6, wxID_REGEXEDITORFRMSTATUSBAR, 
 wxID_REGEXEDITORFRMTOOLBAR1, wxID_REGEXEDITORFRMTXTREGEX, 
 wxID_REGEXEDITORFRMTXTSTRING, 
] = [wx.NewId() for _init_ctrls in range(17)]


class TextDialog(wx.Dialog):
    """Simple dialog with text control and one button (OK)."""
    def __init__(self, parent, fpath=None, w=500, h=600, title='', adv=False):
        """fpath is the full path to the file to be loaded and whose
        contents is to be displayed. If adv is True, an advanced
        highlighter-based editor will be used.
        """
        self._fpath = fpath
        wx.Dialog.__init__(self, parent=parent, title=title, id=wx.NewId(),
                           size=wx.Size(w, h),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.CLOSE_BOX | wx.RESIZE_BORDER |  wx.NO_FULL_REPAINT_ON_RESIZE)
        w, h = self.GetClientSize()
        if adv:
            try: style = wx.TE_MULTILINE | wx.BORDER_THEME
            except: style = wx.TE_MULTILINE
            self._txt = Editor(id=wx.NewId(), parent=self, enh_menu=False,
                               style=style)
            self._txt.set_lexer(style=STYLE_DEFAULT, lexer='container', lexer_style=LEXER_RE)
            self._txt.SetWrapMode(wx.stc.STC_WRAP_WORD)
            self._txt.SetEdgeColumn(0)
            self._txt.set_braces()
            self._txt.SetEdgeMode(wx.stc.STC_EDGE_NONE)
            self._txt.SetEndAtLastLine(True)
        else:
            self._txt = wx.TextCtrl(self, id=wx.NewId(), style=wx.TE_MULTILINE | wx.TE_READONLY)
            self._txt.SetFont(wx.Font(pointSize=10, family=wx.FONTFAMILY_DEFAULT,
                              weight=wx.FONTWEIGHT_NORMAL,
                              style=wx.FONTSTYLE_NORMAL, face=u'Courier new'))
        self._txt.SetSize((w, h))
        
        self.Bind(wx.EVT_KEY_UP, self.OnKey)
        self._txt.Bind(wx.EVT_KEY_UP, self.OnKey)
    
    def ShowModal(self):
        try:
            self._txt.LoadFile(self._fpath)
        except:
            pass
        wx.Dialog.ShowModal(self)
        
    def Show(self):
        try:
            self._txt.LoadFile(self._fpath)
        except:
            pass
        wx.Dialog.Show(self)
        
    def OnKey(self, event):
        if event.KeyCode in [wx.WXK_ESCAPE]:
            self.Close()
                
        
class PyReditorFrm(wx.Frame):
    def _init_coll_lcGroups_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'iter #', width=75)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=u'group #', width=75)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, heading='Name',
              width=75)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT, heading='Value',
              width=300)

    def _init_coll_statusBar_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(2)

        parent.SetStatusText(number=0, text='')
        parent.SetStatusText(number=1, text='')

        parent.SetStatusWidths([16, -1])

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_REGEXEDITORFRM, name='PyReditorFrm',
              parent=prnt, pos=wx.Point(424, 242), size=wx.Size(577, 742),
              style=wx.DEFAULT_FRAME_STYLE, title=u'PyReditor')
        self.SetClientSize(wx.Size(569, 708))
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSplitterChanged)

        self.statusBar = wx.StatusBar(id=wxID_REGEXEDITORFRMSTATUSBAR,
              name='statusBar', parent=self, style=wx.ST_SIZEGRIP)
        self.statusBar.SetPosition(wx.Point(0, 462))
        self.statusBar.SetSize(wx.Size(495, 20))
        self._init_coll_statusBar_Fields(self.statusBar)
        self.SetStatusBar(self.statusBar)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_REGEXEDITORFRMSPLITTERWINDOW1,
              name='splitterWindow1', parent=self, pos=wx.Point(0, 28),
              size=wx.Size(569, 660),
              style=wx.SP_LIVE_UPDATE | wx.CLIP_CHILDREN)
        self.splitterWindow1.SetMinimumPaneSize(150)

        self.panel1 = wx.Panel(id=wxID_REGEXEDITORFRMPANEL1, name='panel1',
              parent=self.splitterWindow1, pos=wx.Point(0, 432),
              size=wx.Size(569, 228), style=0)
        self.panel1.SetAutoLayout(True)

        self.lcGroups = wx.ListCtrl(id=wxID_REGEXEDITORFRMLCGROUPS,
              name='lcGroups', parent=self.panel1, pos=wx.Point(16, 24),
              size=wx.Size(536, 189), style=wx.LC_REPORT)
        self.lcGroups.SetConstraints(LayoutAnchors(self.lcGroups, True, True,
              True, True))
        self.lcGroups.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False,
              u'Courier New'))
        self.lcGroups.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.lcGroups.SetToolTipString(u'Regular expression groups')
        self._init_coll_lcGroups_Columns(self.lcGroups)

        self.staticBox3 = wx.StaticBox(id=wxID_REGEXEDITORFRMSTATICBOX3,
              label='Groups', name='staticBox3', parent=self.panel1,
              pos=wx.Point(5, 0), size=wx.Size(558, 221), style=0)
        self.staticBox3.SetConstraints(LayoutAnchors(self.staticBox3, True,
              True, True, True))

        self.splitterWindow2 = wx.SplitterWindow(id=wxID_REGEXEDITORFRMSPLITTERWINDOW2,
              name='splitterWindow2', parent=self.splitterWindow1,
              pos=wx.Point(0, 0), size=wx.Size(569, 428),
              style=wx.SP_LIVE_UPDATE)
        self.splitterWindow2.SetMinimumPaneSize(150)
        self.splitterWindow1.SplitHorizontally(self.splitterWindow2,
              self.panel1, 428)

        self.panel2 = wx.Panel(id=wxID_REGEXEDITORFRMPANEL2, name='panel2',
              parent=self.splitterWindow2, pos=wx.Point(0, 212),
              size=wx.Size(569, 216), style=0)
        self.panel2.SetAutoLayout(True)

        self.rbAction = wx.RadioBox(choices=['search', 'match',
              'finditer'], id=wxID_REGEXEDITORFRMRBACTION, label='Action',
              majorDimension=1, name='rbAction', parent=self.panel2,
              pos=wx.Point(438, 25), size=wx.Size(112, 175),
              style=wx.RA_SPECIFY_COLS)
        self.rbAction.SetConstraints(LayoutAnchors(self.rbAction, False, True,
              True, True))
        self.rbAction.SetToolTipString(u'Action to perform using the regular expression')
        self.rbAction.Bind(wx.EVT_RADIOBOX, self.OnChange,
              id=wxID_REGEXEDITORFRMRBACTION)

        try: style = wx.TE_MULTILINE | wx.BORDER_THEME
        except: style = wx.TE_MULTILINE
        self.txtString = Editor(id=wxID_REGEXEDITORFRMTXTSTRING,
              name='txtString', parent=self.panel2, pos=wx.Point(15, 27),
              size=wx.Size(413, 176), style=style)
        self.txtString.SetConstraints(LayoutAnchors(self.txtString, True, True,
              True, True))
        self.txtString.SetToolTipString(u'A string to test the regular expression on')
        self.txtString.SetWrapMode(wx.stc.STC_WRAP_WORD)
        self.txtString.SetEdgeColumn(0)
        self.txtString.SetEdgeMode(wx.stc.STC_EDGE_NONE)
        self.txtString.SetEndAtLastLine(True)

        self.staticBox2 = wx.StaticBox(id=wxID_REGEXEDITORFRMSTATICBOX2,
              label='String (text)', name='staticBox2', parent=self.panel2,
              pos=wx.Point(5, 0), size=wx.Size(558, 216), style=0)
        self.staticBox2.SetConstraints(LayoutAnchors(self.staticBox2, True,
              True, True, True))

        self.panel = wx.Panel(id=wxID_REGEXEDITORFRMPANEL, name='panel',
              parent=self.splitterWindow2, pos=wx.Point(0, 0), size=wx.Size(569,
              208), style=0)
        self.panel.SetAutoLayout(True)
        self.splitterWindow2.SplitHorizontally(self.panel, self.panel2, 208)

        self.staticBox1 = wx.StaticBox(id=wxID_REGEXEDITORFRMSTATICBOX1,
              label='Regular expression', name='staticBox1', parent=self.panel,
              pos=wx.Point(5, 16), size=wx.Size(558, 192), style=0)
        self.staticBox1.SetConstraints(LayoutAnchors(self.staticBox1, True,
              True, True, True))

        self.staticText6 = wx.StaticText(id=wxID_REGEXEDITORFRMSTATICTEXT6,
              label='Tip: CTRL+mouse wheel zooms text in/out',
              name='staticText6', parent=self.panel, pos=wx.Point(8, 4),
              size=wx.Size(177, 11), style=0)
        self.staticText6.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))

        self.clbFlags = wx.CheckListBox(choices=['IGNORECASE', 'LOCALE',
              'MULTILINE', 'DOTALL', 'UNICODE', 'VERBOSE'],
              id=wxID_REGEXEDITORFRMCLBFLAGS, name='clbFlags',
              parent=self.panel, pos=wx.Point(440, 40), size=wx.Size(112, 160),
              style=0)
        self.clbFlags.SetConstraints(LayoutAnchors(self.clbFlags, False, True,
              True, True))
        self.clbFlags.SetToolTipString(u'Additional flags for the search/match/finditer action')
        self.clbFlags.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        self.clbFlags.Bind(wx.EVT_CHECKLISTBOX, self.OnChange,
              id=wxID_REGEXEDITORFRMCLBFLAGS)

        try: style = wx.TE_MULTILINE | wx.BORDER_THEME
        except: style = wx.TE_MULTILINE
        self.txtRegex = Editor(enh_menu=True, id=wxID_REGEXEDITORFRMTXTREGEX,
              name='txtRegex', parent=self.panel, pos=wx.Point(14, 40),
              size=wx.Size(413, 160), style=style)
        self.txtRegex.SetConstraints(LayoutAnchors(self.txtRegex, True, True,
              True, True))
        self.txtRegex.SetWrapMode(wx.stc.STC_WRAP_WORD)
        self.txtRegex.SetEdgeColumn(0)
        self.txtRegex.SetEdgeMode(wx.stc.STC_EDGE_NONE)
        self.txtRegex.SetEndAtLastLine(True)
        self.txtRegex.SetToolTipString(u'Regular expression')

        self.toolBar1 = wx.ToolBar(id=wxID_REGEXEDITORFRMTOOLBAR1,
              name='toolBar1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(569, 28),
              style=wx.TB_HORIZONTAL|wx.NO_BORDER|wx.TB_FLAT)
        self.toolBar1.SetToolBitmapSize(wx.Size(22, 22))
        self.SetToolBar(self.toolBar1)

    def __init__(self, parent, path=None):
        self._path = setpath(path)
        
        self._init_ctrls(parent)
        
        # Some variables
        self._maxgroups = 20
        self._tempitems = self._load_temp_items(TEMP_FILE)      # template menu items (read from templates.cfg)
        self._ischanged = False     # if re or text has changed
        self._fname = 'untitled'
        self._is_file_set = False
        self._tmp_editor_h = None   # handle to template editor window
        
        # Set the editors
        self.txtRegex.set_lexer(style=STYLE_DEFAULT, lexer='container',
                                lexer_style=LEXER_RE)
        self.txtRegex.set_braces()
        #self.txtRegex.set_tokens(_AC_TOKENS)
        self.txtRegex.Bind(wx.stc.EVT_STC_CHANGE, self.OnChange)
        self.txtRegex.enh_popup(insertitems=M_ITEMS, tempitems=self._tempitems,
                                on=True, path=self._path)
        self.txtRegex.SetViewEOL(False)
        
        self.txtString.set_lexer(style=STYLE_DEFAULT, lexer='null')
        self.txtString.set_braces()
        self.txtString.Bind(wx.stc.EVT_STC_CHANGE, self.OnChange)
        self.txtString.Bind(wx.EVT_KEY_UP, self.OnChange)
        self.txtString.enh_popup(insertitems=None, tempitems=None,
                                on=True, path=self._path)
        self.txtString.SetViewEOL(False)
        
        # Settings
        self._sett_file = os.path.join(self._path, 'pyreditor.cfg')
        self._sett = Settings(self._sett_file, SETT_KEYS)
        self.SetTitle(TITLE)
        
        # The standard (non-popup) menus and icons
        self._set_menus()

        # The main icon
        self._set_icon(self, r'pyreditor.ico')
        self.statusImages = [self._set_png(r'error.png'), self._set_png(r'ok.png')]

        rect = self.statusBar.GetFieldRect(0)
        self.sbImage = wx.StaticBitmap(self.statusBar, -1, self.statusImages[0],
            (rect.x+1, rect.y+1), (16, 16))

        self.winConfOption = 'PyReditor'
        
        # Some additional bindings
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.txtRegex.Bind(wx.EVT_UPDATE_UI, self.OnUpdateREEditUI)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        # 2 colors to display matches in the list
        self._color_yellow = YELLOW2
        self._color_green = GREEN2
        
        # Read and apply the settings
        self._read_sett()
        
        # Change some settings-dependent stuff
        self.txtRegex.set_maxgroups(maxgroups=self._maxgroups)
        self.txtString.set_maxgroups(maxgroups=self._maxgroups)
        
        # and the title
        self._update_title()
        
    def _load_temp_items(self, fname):
        # Loads and returns the template menu items. On error it shows
        # error dialog and returns None.
        try:
            tmp = Templates(os.path.join(self._path, fname))
            return tmp.load()
        except:
            errdlg(self, 'Templates error: check templates file "%s" and/or '\
                   'structure of this file.' % fname)
            return None
    
    def _update_title(self):
        if self._ischanged: indic = '*'
        else: indic = ''
        s = '%s - [%s%s]' % (TITLE, self._fname, indic)
        self.SetTitle(s)
        
    def _set_menus(self):
        # Sets all the menus as well as all the tools and sets
        # their bindings (callbacks)
        
        self._menu_ids = {}
        
        #----------
        # File menu
        #----------
        self.menu_file = wx.Menu(title='')
        
        # Load re
        self._menu_ids['load_re'] = wx.NewId()
        self._add_menu_item(self.menu_file, id=self._menu_ids['load_re'],
                            text=u'&Load re..\tCTRL+O', icon='fileopen_re.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_Load_Re, id=self._menu_ids['load_re'])
        
        # Save re
        self._menu_ids['save_re'] = wx.NewId()
        self._add_menu_item(self.menu_file, id=self._menu_ids['save_re'],
                            text=u'&Save re..\tCTRL+S', icon='filesave_re.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_Save_Re, id=self._menu_ids['save_re'])
        
        # Save as re
        self._menu_ids['save_as_re'] = wx.NewId()
        self._add_menu_item(self.menu_file, id=self._menu_ids['save_as_re'],
                            text=u'&Save as re..\tSHIFT+CTRL+S', icon='filesaveas_re.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_Save_As_Re, id=self._menu_ids['save_as_re'])
        
        self.menu_file.AppendSeparator()
        
        # Load text
        self._menu_ids['load_text'] = wx.NewId()
        self._add_menu_item(self.menu_file, id=self._menu_ids['load_text'],
                            text=u'&Load text..', icon='fileopen.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_Load_Text, id=self._menu_ids['load_text'])
        
        self.menu_file.AppendSeparator()
        
        # Exit
        self._menu_ids['exit'] = wx.NewId()
        self.menu_file.Append(help='', id=self._menu_ids['exit'], kind=wx.ITEM_NORMAL, text='Exit\tAlt+F4')
        self.Bind(wx.EVT_MENU, self.OnMenu_Exit, id=self._menu_ids['exit'])
        
        #----------
        # Edit menu (only edit items)
        #----------
        self.menu_edit = EditInsertMenu(self, self.txtRegex, self._path, hasedit=True, insertitems=None)
        edit_ids = self.menu_edit.get_ids()
        
        #----------
        # Insert menu (+ templates if available)
        #----------
        self.menu_insert = EditInsertMenu(self, self.txtRegex, self._path, hasedit=False, insertitems=M_ITEMS, tempitems=self._tempitems)
        
        #----------
        # Options menu
        #----------
        self.menu_opt = wx.Menu(title='')
        
        # New line visible (check)
        self._menu_ids['opt_nl'] = wx.NewId()
        mitem = wx.MenuItem(self.menu_opt, id=self._menu_ids['opt_nl'], text=u'RE newline visible', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnMenu_optnl, id=self._menu_ids['opt_nl'])
        self.menu_opt.AppendItem(mitem)
        
        # Save text (check)
        self._menu_ids['opt_savetext'] = wx.NewId()
        mitem = wx.MenuItem(self.menu_opt, id=self._menu_ids['opt_savetext'], text=u'Save text on save', kind=wx.ITEM_CHECK)
        self.menu_opt.AppendItem(mitem)
        
        # RE line numbers (check)
        self._menu_ids['opt_lines_re'] = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnMenu_opt_lnre, id=self._menu_ids['opt_lines_re'])
        mitem = wx.MenuItem(self.menu_opt, id=self._menu_ids['opt_lines_re'], text='RE line numbers', kind=wx.ITEM_CHECK)
        self.menu_opt.AppendItem(mitem)
        
        # Text line numbers (check)
        self._menu_ids['opt_lines_text'] = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnMenu_opt_lntext, id=self._menu_ids['opt_lines_text'])
        mitem = wx.MenuItem(self.menu_opt, id=self._menu_ids['opt_lines_text'], text=u'Text line numbers', kind=wx.ITEM_CHECK)
        self.menu_opt.AppendItem(mitem)
        
        # Auto indent (check)
        self._menu_ids['opt_autoindent'] = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnMenu_opt_autoindent, id=self._menu_ids['opt_autoindent'])
        mitem = wx.MenuItem(self.menu_opt, id=self._menu_ids['opt_autoindent'], text=u'RE auto indent', kind=wx.ITEM_CHECK)
        self.menu_opt.AppendItem(mitem)
        
        self.menu_opt.AppendSeparator()
        
        # Reset zoom
        self._menu_ids['opt_resetzoom'] = wx.NewId()
        self._add_menu_item(self.menu_opt, id=self._menu_ids['opt_resetzoom'],
                            text=u'Reset zoom', icon='resetzoom.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_opt_resetzoom, id=self._menu_ids['opt_resetzoom'])
        
        # Reload templates
        self._menu_ids['opt_reloadtemp'] = wx.NewId()
        self._add_menu_item(self.menu_opt, id=self._menu_ids['opt_reloadtemp'],
                            text=u'Reload templates', icon='reload.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_optreloadtemp, id=self._menu_ids['opt_reloadtemp'])
        
        self.menu_opt.AppendSeparator()
        
        # edit templates
        self._menu_ids['opt_edittemp'] = wx.NewId()
        self._add_menu_item(self.menu_opt, id=self._menu_ids['opt_edittemp'],
                            text=u'Edit templates', icon='kmenuedit.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_optedittemp, id=self._menu_ids['opt_edittemp'])
        
        #----------
        # Help menu
        #----------
        self.menu_help = wx.Menu(title='')
        
        # RE Help
        self._menu_ids['re_help'] = wx.NewId()
        self._add_menu_item(self.menu_help, id=self._menu_ids['re_help'],
                            text=u'RE help\tF1', icon='help.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_Help, id=self._menu_ids['re_help'])
        
        # Readme
        self._menu_ids['readme'] = wx.NewId()
        self._add_menu_item(self.menu_help, id=self._menu_ids['readme'],
                            text=u'Readme', icon='readme.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_Readme, id=self._menu_ids['readme'])
        
        # License
        self._menu_ids['license'] = wx.NewId()
        self._add_menu_item(self.menu_help, id=self._menu_ids['license'],
                            text=u'License', icon='lock.png')
        self.Bind(wx.EVT_MENU, self.OnMenu_License, id=self._menu_ids['license'])
        
        self.menu_help.AppendSeparator()
        
        # About
        self._menu_ids['about'] = wx.NewId()
        self._add_menu_item(self.menu_help, id=self._menu_ids['about'],
                            text=u'About')
        self.Bind(wx.EVT_MENU, self.OnMenu_About, id=self._menu_ids['about'])

        #-------------
        # The menu bar
        #-------------
        self.menubar = wx.MenuBar()
        self.menubar.SetEvtHandlerEnabled(True)
        
        self.menubar.Append(menu=self.menu_file, title=u'File')
        self.menubar.Append(menu=self.menu_edit, title=u'Edit')
        self.menubar.Append(menu=self.menu_insert, title=u'Insert')
        self.menubar.Append(menu=self.menu_opt, title=u'Options')
        self.menubar.Append(menu=self.menu_help, title=u'Help')
        
        self.SetMenuBar(self.menubar)
        
        # The toolbar
        #------------
        # Note that, as the tools that have a corresponding
        # menu item will have the same id, there is no need to bind them again as
        # this will be done automatically (see wxMenuBar help)
        self.toolBar1.ClearTools()
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'fileopen_re22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['load_re'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Load RE')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'filesave_re22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['save_re'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Save RE')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'filesaveas_re22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['save_as_re'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Save as RE')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'fileopen22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['load_text'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Load text/string from a file')
        
        self.toolBar1.AddSeparator()
        
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'undo22.png'), bmpDisabled=wx.NullBitmap,
              id=edit_ids['undo'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Undo')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'redo22.png'), bmpDisabled=wx.NullBitmap,
              id=edit_ids['redo'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Redo')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'editcut22.png'), bmpDisabled=wx.NullBitmap,
              id=edit_ids['cut'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Cut')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'editcopy22.png'), bmpDisabled=wx.NullBitmap,
              id=edit_ids['copy'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp='Copy')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'editpaste22.png'), bmpDisabled=wx.NullBitmap,
              id=edit_ids['paste'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp='Paste')
        
        self.toolBar1.AddSeparator()
        
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'resetzoom22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['opt_resetzoom'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Reset zoom')
        
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'kmenuedit22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['opt_edittemp'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Edit menu templates')
        
        self.toolBar1.AddSeparator()
        
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'readme22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['readme'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Readme')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'lock22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['license'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'Licensing terms')
        self.toolBar1.DoAddTool(bitmap=self._set_png(r'help22.png'), bmpDisabled=wx.NullBitmap,
              id=self._menu_ids['re_help'], kind=wx.ITEM_NORMAL, label='',
              longHelp='', shortHelp=u'RE Help')
              
        self.toolBar1.Realize()
        
    def _add_menu_item(self, menu, id, text, icon=None, submenu=None):
        # Adds a menu icon to the menu. If the icon does not exist, it simply
        # ignores this.
        mitem = wx.MenuItem(menu, id=id, text=text, subMenu=submenu)
        if icon != None:
            try: mitem.SetBitmap(self._set_png(icon))
            except: pass
        menu.AppendItem(mitem)

    def OnSplitterChanged(self, event):
        #TODO: ? this is important: do not evaluate this event=> otherwise, splitterwindow behaves strange
        event.Skip()
##        pass
        
#    def _set_reg_ex_textctrl(self):
#        # Sets the regular expression text control
#        
#        # Set the "none lexer"
#        self.txtRegex.SetLexer(wx.stc.STC_LEX_CONTAINER)
#        
#        # Event bindings. Important, self.OnUpdateUI should be "fired" when
#        # the stc is being updated and not when the frame is being updated.
#        # If not, the processor will work with 100% most of the time!
#        self.txtRegex.Bind(wx.stc.EVT_STC_CHANGE, self.OnChange)
#        self.txtRegex.Bind(wx.stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
#        self.txtRegex.Bind(wx.stc.EVT_STC_STYLENEEDED, self.OnStyleNeeded)
#        
#        # Faces (for font specification)
#        faces = {
#              'times': 'Times',
#              'mono' : 'Courier new',
#              'helv' : 'Helvetica',
#              'other': 'new century schoolbook',
#              'size' : 10,
#              'size2': 8
#              }
#        
#        # Default/common styles
#        self.txtRegex.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,     "face:%(mono)s,size:%(size)d" % faces)
#        self.txtRegex.StyleClearAll()
#        self.txtRegex.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
#        self.txtRegex.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
#        self.txtRegex.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,  "fore:#0000CE,back:#00F400,bold")
#        self.txtRegex.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,    "fore:#0000CE,back:#F30000,bold")
#            
#        # Some modified Python styles for our own "highlighter"
#        self.txtRegex.StyleSetSpec(wx.stc.STC_P_CLASSNAME,       "fore:#0000F3,back:#FFFFFF,bold")
#        self.txtRegex.StyleSetSpec(wx.stc.STC_P_DECORATOR,       "fore:#D81CD8,back:#FFFFFF")
#        self.txtRegex.StyleSetSpec(wx.stc.STC_P_DEFNAME,         "fore:#FF8306,back:#FFFFFF,bold")
#        self.txtRegex.StyleSetSpec(wx.stc.STC_P_OPERATOR,        "fore:#000000,back:#FFFFFF,bold")
#            
#        # Hide the lines margin
#        self.txtRegex.SetMarginWidth(1, 0)
#        
#        # Braces (for matching); \( is not a matching brace!
#        self.braces = r'()[]{}<>'
#        self.braces_patt = '[%s]' % string.join(['\\%s' % br for br in self.braces], '')
#        self.braces_patt = re.compile(self.braces_patt)
#        
#        # Patterns for matching/searching
#        patt_group = r'(?P<group>(?:(?:\((?:(?:\?<!)|(?:\?<=)|(?:\?=)|(?:\?[:!#])|(?:\?P\<\w+\>)|(?:\?P\=\w+)|(?:\?\(\w+\))|(?:\?[iLmsux]{1,6}(?=\W))?)))|(?:\)))'
#        patt_braces = r'(?P<br>(?:[\[\]\{\}]))'
#        patt_kw = r'(?P<kw>\\(?:(?:\d{3})|(?:x\d{2})|(?:[\\aAbBdDsSwWZntrvxf])))'
#        patt_special = r'(?P<spec>\\[\(\)\[\]\{\}])'
#        patt_op = r'(?P<op>(?:(?<!\\)[*+$^.|])|(?:(?<![\\\(])\?))'
#        
#        # The order below IS important!
#        self.all_patts = r'%s|%s|%s|%s|%s' % (patt_kw, patt_special, patt_group, patt_braces, patt_op)
#        self.all_patts = re.compile(self.all_patts)
        
#    def OnStyleNeeded(self, event):
#        """On style change.
#        """
#        # Get the first character that "needs styling", start
#        # and the last one that "needs styling", end
#        start = self.txtRegex.GetEndStyled()
#        end = event.GetPosition()
#        
#        # Get the line # corresponding to start and then the first
#        # position in that line
#        line_no = self.txtRegex.LineFromPosition(start)
#        start = self.txtRegex.PositionFromLine(line_no)
#        
#        # Get the text from the editor
#        s = self.txtRegex.GetTextRange(start, end)
#        
#        # Apply the default styling to the selection
#        self.txtRegex.StartStyling(start, 31)     
#        self.txtRegex.SetStyling(end-start+1, wx.stc.STC_STYLE_DEFAULT)
#        
#        # Iterate over all the matches according to self.all_patts and
#        # apply styling according to which group is being matched
#        iter = re.finditer(self.all_patts, s)
#        for it in iter:
#            (s1, s2) = it.span()
#            self.txtRegex.StartStyling(start+s1, 31)
#            if it.group('group'):
#                self.txtRegex.SetStyling(s2-s1, wx.stc.STC_P_CLASSNAME)
#            elif it.group('br'):
#                self.txtRegex.SetStyling(s2-s1, wx.stc.STC_P_DECORATOR)
#            elif it.group('kw'):
#                self.txtRegex.SetStyling(s2-s1, wx.stc.STC_P_DEFNAME)
#            elif it.group('spec'):
#                pass # ignore
#            elif it.group('op'):
#                self.txtRegex.SetStyling(s2-s1, wx.stc.STC_P_OPERATOR)
#            else:
#                raise Exception('Uknown group matched')

    def setDefaultDimensions(self):
        self.Center(wx.BOTH)

    def OnChange(self, event):
        # On text update in either txtString or txtRegex
        try:
            if event.GetKeyCode() in [wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP,
                                      wx.WXK_DOWN, wx.WXK_CANCEL, wx.WXK_HOME,
                                      wx.WXK_END, wx.WXK_PAGEDOWN, wx.WXK_PAGEUP,
                                      wx.WXK_PAUSE, wx.WXK_SCROLL, wx.WXK_CONTROL,
                                      wx.WXK_ALT, wx.WXK_SHIFT, 
                                      wx.WXK_NUMLOCK]:
                event.Skip()
                return
        except:
            pass
        self.update_editors()
        self._ischanged = True
        self._update_title()
        event.Skip()
        
    def OnUpdateREEditUI(self, event):
        # Some of the standard menu items are updated automatically
        ids = self.menu_edit.get_ids()
        if self.txtRegex.CanUndo(): self.toolBar1.EnableTool(ids['undo'], True)
        else: self.toolBar1.EnableTool(ids['undo'], False)
        if self.txtRegex.CanRedo(): self.toolBar1.EnableTool(ids['redo'], True)
        else: self.toolBar1.EnableTool(ids['redo'], False)
        if self.txtRegex.CanPaste(): self.toolBar1.EnableTool(ids['paste'], True)
        else: self.toolBar1.EnableTool(ids['paste'], False)
        event.Skip()
        
    def update_editors(self):
        string = self.txtString.GetText()
        regex = self.txtRegex.GetText()
        
        self.txtString.color_txtString(None)
        self.lcGroups.DeleteAllItems()

        flags = 0
        for idx in range(self.clbFlags.GetCount()):
            if self.clbFlags.IsChecked(idx):
                flags |= RE_FLAGS[self.clbFlags.GetString(idx)]

        try:
            ro = re.compile(regex, flags)
        except Exception, err:
            self.statusBar.SetStatusText('Error: %s: %s'%(err.__class__, err), 1)
            self.sbImage.SetBitmap(self.statusImages[0])
            return

        sel = self.rbAction.GetSelection()
        if sel == 0:
            # search
            mo = ro.search(string)
        elif sel == 1:
            # match
            mo = ro.match(string)
        else:
            # sel==2: finditer
            mo = ro.finditer(string)

        self.setStatus(mo)
        self.lcGroups.DeleteAllItems()
        if mo:
            # There is a match
            if sel == 2:
                # finditer
                mo = list(mo)
                sp = [m.span() for m in mo]
                self.txtString.color_txtString(sp)
            else:
                # search or match
                sp = mo.span()
                #s, e = sp
                self.txtString.color_txtString(sp)
                mo = [mo]
                
            # We want the named groups sorted in the order they appear in the re
            # so lets get the index, name and group into a list of lists - but
            # only if a group is non-None
            self.lcGroups.DeleteAllItems()
            iter_num = 0
            add = 0
            color = self._color_green
            
            gindex = ro.groupindex
            # gi2name is a group index to group name mapping; only for
            # named groups
            gi2name = dict([(v, k) for (k, v) in gindex.iteritems()])
            
            k = 0
            for m in mo:
                k += 1
                if color == self._color_green: color = self._color_yellow
                else: color = self._color_green
                groups = []
                
                # Looping through all the groups
                k = 0
                for gn in range(len(m.groups())):
                    if m.group(gn+1) is None: continue
                    try: name = gi2name[gn+1]
                    except: name = ''
                    groups += [[gn+1, name, m.group(gn+1)]]
                    k += 1

                # Now add the list items to lcGroups
                k = 0
                for idx, name, group in groups:
                    self.lcGroups.InsertStringItem(add+k, str(iter_num+1))
                    self.lcGroups.SetStringItem(add+k, 1, str(idx))
                    self.lcGroups.SetStringItem(add+k, 2, str(name))
                    self.lcGroups.SetStringItem(add+k, 3, str(group))
                    self.lcGroups.SetItemBackgroundColour(add+k, color)
                    k =+ 1
                iter_num += 1
                add += len(groups)
                
                if k >= self._maxgroups:
                    break

    def setStatus(self, mo):
        if mo:
            self.statusBar.SetStatusText('Match', 1)
            self.sbImage.SetBitmap(self.statusImages[1])
        else:
            self.statusBar.SetStatusText('Failed to match', 1)
            self.sbImage.SetBitmap(self.statusImages[0])
            
    def _read_sett(self):
        try:
            self._sett.load()
            
            # NL
            nl = self._sett.get('options', 'newline', defvalue=0, t='i')
            self.menu_opt.Check(self._menu_ids['opt_nl'], nl)
            self.txtRegex.SetViewEOL(nl)
            
            # line numbers
            ln = self._sett.get('options', 'lines_text', defvalue=1, t='i')
            self.txtString.linenums(ln==1)
            self.menu_opt.Check(self._menu_ids['opt_lines_text'], ln==1)
            
            ln = self._sett.get('options', 'lines_re', defvalue=0, t='i')
            self.txtRegex.linenums(ln==1)
            self.menu_opt.Check(self._menu_ids['opt_lines_re'], ln==1)
            
            # save text
            st = self._sett.get('options', 'savetext', defvalue=0, t='i')
            self.menu_opt.Check(self._menu_ids['opt_savetext'], st)
            
            # Auto indent
            ai = self._sett.get('options', 'autoindent', defvalue=0, t='i')
            self.txtRegex.autoindent(ai==1)
            self.menu_opt.Check(self._menu_ids['opt_autoindent'], ai==1)
            
            # pos
            x = self._sett.get('general', 'x', t='i')
            y = self._sett.get('general', 'y', t='i')
            w = self._sett.get('general', 'w', t='i')
            h = self._sett.get('general', 'h', t='i')
            self.SetPosition((x, y))
            self.SetSize((w, h))
            
            # sash
            sp1 = self._sett.get('general', 'sp1', t='i')
            sp2 = self._sett.get('general', 'sp2', t='i')
            self.splitterWindow1.SetSashPosition(sp1)
            self.splitterWindow2.SetSashPosition(sp2)
            
            # zoom
            zoom_re = self._sett.get('general', 'zoom_re', t='i')
            zoom_text = self._sett.get('general', 'zoom_text', t='i')
            if zoom_re > 20: zoom_re = 20
            if zoom_text > 20: zoom_text = 20
            if zoom_re < -10: zoom_re = -10
            if zoom_text < -10: zoom_text = -10
            self.txtRegex.SetZoom(zoom_re)
            self.txtString.SetZoom(zoom_text)
            
            # other
            self._maxgroups = self._sett.get('general', 'maxgroups', defvalue=20, t='i')
            self._maxgroups = abs(self._maxgroups)
            if self._maxgroups < 1: self._maxgroups = 10
        except:
            pass
    
    def _save_sett(self):
        try:
            # NL
            self._sett.set('options', 'newline', 1*self.menu_opt.IsChecked(self._menu_ids['opt_nl']))
            
            # line numbers
            self._sett.set('options', 'lines_text', 1*self.menu_opt.IsChecked(self._menu_ids['opt_lines_text']))
            self._sett.set('options', 'lines_re', 1*self.menu_opt.IsChecked(self._menu_ids['opt_lines_re']))
            
            # save text
            self._sett.set('options', 'savetext', 1*self.menu_opt.IsChecked(self._menu_ids['opt_savetext']))
            
            # Auto indent
            self._sett.set('options', 'autoindent', 1*self.menu_opt.IsChecked(self._menu_ids['opt_autoindent']))
            
            # pos
            (x, y) = self.GetPosition()
            (w, h) = self.GetSize()
            self._sett.set('general', 'x', x)
            self._sett.set('general', 'y', y)
            self._sett.set('general', 'w', w)
            self._sett.set('general', 'h', h)
            
            # sash
            self._sett.set('general', 'sp1', self.splitterWindow1.GetSashPosition())
            self._sett.set('general', 'sp2', self.splitterWindow2.GetSashPosition())
            
            # zoom
            self._sett.set('general', 'zoom_re', self.txtRegex.GetZoom())
            self._sett.set('general', 'zoom_text', self.txtString.GetZoom())
            
            self._sett.save()
        except:
            pass
            
    def OnMenu_About(self, event):
        msg = "PyReditor v. %s\nRelease: %s\n%s, %s\n\n"\
              "This program is based on RegexEditor\n"\
              "(part of Boa Constructor) and is licensed\n"\
              "under GPL (see Help|License for GPL terms and conditions)" %\
              (__version__, __release__, __author__, __authormail__)
        dlg = wx.MessageDialog(self, message=msg,
            style=wx.OK|wx.ICON_INFORMATION,
            caption='About')
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
            
    def OnMenu_Help(self, event):
        # Shows a dialog with the RE help
        self._text_dialog(u'Python RE Help', 'rehelp.txt', adv=True, modal=False)
        
    def OnMenu_Readme(self, event):
        # Shows a dialog with the readme help
        self._text_dialog(u'PyReditor README', 'readme.txt', adv=False)
            
    def OnMenu_License(self, event):
        # Shows a dialog with the License terms
        self._text_dialog(u'License', 'LICENSE.TXT')
            
    def OnMenu_Load_Re(self, event):
        # Load RE and any text as well (if a valid cfg file and if
        # confirmed so).
        file_flt = "RE files (*.re)|*.re|Text files (*.txt)|*.txt|ALL files (*.*)|*.*"
        dlg = wx.FileDialog(self, message='Load Regular Expression', wildcard=file_flt)
        try:
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                if self._ischanged:
                    if not self._conf_dlg('Unsaved changes. Really want to discard the changes?',):
                        return
                self._fname = dlg.GetPath()
                pf = ProjFile(self._fname)
                (re, reflags, text, action) = pf.load()
                self.txtRegex.SetText(re)
                if reflags != None:
                    for idx in range(self.clbFlags.GetCount()):
                        flag = self.clbFlags.GetString(idx)
                        self.clbFlags.Check(idx, reflags[flag])
                if text != None:
                    res = self._conf_dlg('Load accompanying text as well?')
                    if res:
                        self.txtString.SetText(text)
                self.rbAction.SetSelection(action)
                self._ischanged = False
                self._is_file_set = True
                self._update_title()
        finally:
            dlg.Destroy()
        self.update_editors()
            
    def OnMenu_Save_Re(self, event):
        # Save RE, flags and accompanying text as well
        save = False
        if not self._is_file_set:
            file_flt = "RE files (*.re)|*.re|Text files (*.txt)|*.txt|ALL files (*.*)|*.*"
            dlg = wx.FileDialog(self, message='Save Regular Expression',
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, wildcard=file_flt)
            try:
                res = dlg.ShowModal()
                if res == wx.ID_OK:
                    self._fname = dlg.GetPath()
                    save = True
            finally:
                dlg.Destroy()
        else:
            save = True
            
        if save:
            fp = ProjFile(self._fname)
            re = self.txtRegex.GetText()
            text = None
            if self.menu_opt.IsChecked(self._menu_ids['opt_savetext']):
                text = self.txtString.GetText()
            reflags = RE_FLAGS.copy()
            for idx in range(self.clbFlags.GetCount()):
                flag = self.clbFlags.GetString(idx)
                reflags[flag] = self.clbFlags.IsChecked(idx)
            action = self.rbAction.GetSelection()
            fp.save(re, reflags, text, action)
            self._ischanged = False
            self._is_file_set = True
            self._update_title()
            
    def OnMenu_Save_As_Re(self, event):
        # Save as RE, flags and accompanying text as well
        save = False
        file_flt = "RE files (*.re)|*.re|Text files (*.txt)|*.txt|ALL files (*.*)|*.*"
        dlg = wx.FileDialog(self, message='Save Regular Expression as',
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, wildcard=file_flt)
        try:
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                self._fname = dlg.GetPath()
                save = True
        finally:
            dlg.Destroy()
        
        if save:
            fp = ProjFile(self._fname)
            re = self.txtRegex.GetText()
            text = None
            if self.menu_opt.IsChecked(self._menu_ids['opt_savetext']):
                text = self.txtString.GetText()
            reflags = RE_FLAGS.copy()
            for idx in range(self.clbFlags.GetCount()):
                flag = self.clbFlags.GetString(idx)
                reflags[flag] = self.clbFlags.IsChecked(idx)
            action = self.rbAction.GetSelection()
            fp.save(re, reflags, text, action)
            self._ischanged = False
            self._is_file_set = True
            self._update_title()
            
    def OnMenu_optnl(self, event):
        self.txtRegex.SetViewEOL(event.IsChecked())
        
    def OnMenu_opt_resetzoom(self, event):
        self.txtRegex.SetZoom(0)
        self.txtString.SetZoom(0)
        
    def OnMenu_opt_lntext(self, event):
        self.txtString.linenums(event.IsChecked())
        
    def OnMenu_opt_lnre(self, event):
        self.txtRegex.linenums(event.IsChecked())
        
    def OnMenu_opt_autoindent(self, event):
        self.txtRegex.autoindent(event.IsChecked())
        
    def OnMenu_optreloadtemp(self, event):
        # Reload templates - reload all the menus. First, save settings (mainly
        # because some menu items may have checked/unchecked items), recreate
        # all the menus and reload the saved settings.        
        self._save_sett()
        self._tempitems = self._load_temp_items(TEMP_FILE)
        self.txtRegex.enh_popup(insertitems=M_ITEMS, tempitems=self._tempitems,
                                on=True, path=self._path)
        self._set_menus()
        self._read_sett()
    
    def OnMenu_optedittemp(self, event):
        # Edit templates 
        # If not open yet
        try:
            self._tmp_editor_h.Show()
        except:
            self._tmp_editor_h = Frame1(self, r'templates.cfg', path=self._path,
                                        onsave=self.OnMenu_optreloadtemp)
            self._tmp_editor_h.Show()
    
    def OnMenu_Load_Text(self, event):
        file_flt = "ALL files (*.*)|*.*|Text files (*.txt)|*.txt"
        dlg = wx.FileDialog(self, message='Load text', wildcard=file_flt)
        try:
            res = dlg.ShowModal()
            if res == wx.ID_OK:
                if self._ischanged:
                    if not self._conf_dlg('Unsaved changes. Really want to load new text?',
                                      style=wx.YES_NO|wx.ICON_QUESTION):
                        return
                dir = dlg.GetDirectory()
                fname = dlg.GetFilename()
                self.txtString.LoadFile(os.path.join(dir, fname))
        finally:
            dlg.Destroy()
        self.update_editors()

    def OnMenu_Exit(self, event):
        self.Close()
        
    def OnClose(self, event):
        if self._ischanged:
            if not self._conf_dlg('Really want to exit with unsaved changes?',
                                  style=wx.YES_NO|wx.ICON_QUESTION):
                return
        self._save_sett()
        self.Destroy()
        
    def _text_dialog(self, title, fname, w=600, h=600, adv=False, modal=True):
        # Shows a simple dialog with text and one button. The text is
        # loaded from a file
        fpath = os.path.join(self._path, fname)
        dlg = TextDialog(self, fpath=fpath, w=w, h=h, title=title, adv=adv)
        if modal:
            try: dlg.ShowModal()
            finally: dlg.Destroy()
        else:
            dlg.Show()
        
    def _conf_dlg(self, msg, style=wx.YES_NO|wx.ICON_QUESTION):
        # Confirmation dialog
        res = 0
        dlg = wx.MessageDialog(self, msg, caption='Message', style=style)
        try:
            res = (dlg.ShowModal() in [wx.ID_OK, wx.ID_YES])
        finally:
            dlg.Destroy()
        return res
        
    def _set_icon(self, frame, icfile):
        fld = os.path.join(self._path, r'Images/icons')
        fld = os.path.normpath(fld)
        frame.SetIcon(wx.Icon(os.path.join(fld, icfile), wx.BITMAP_TYPE_ICO))
            
    def _set_png(self, pngfile):
        return set_png(self._path, pngfile)


def openPyReditor(editor):
    frame = createPyreditor(editor)
    frame.Show()


def main():
    app = wx.PySimpleApp()
    openPyReditor(None)
    app.MainLoop()
    
    
if __name__ == '__main__':
    main()

