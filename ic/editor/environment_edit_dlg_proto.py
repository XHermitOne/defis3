# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.aui

###########################################################################
## Class icEditEnvironmentDlgProto
###########################################################################

class icEditEnvironmentDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Контекст / Окружение проекта", pos = wx.DefaultPosition, size = wx.Size( 856,352 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.env_auinotebook = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.base_panel = wx.Panel( self.env_auinotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.base_listCtrl = wx.ListCtrl( self.base_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer3.Add( self.base_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.base_panel.SetSizer( bSizer3 )
		self.base_panel.Layout()
		bSizer3.Fit( self.base_panel )
		self.env_auinotebook.AddPage( self.base_panel, u"Основные", True, wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_BUTTON ) )
		self.ext_panel = wx.Panel( self.env_auinotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self.ext_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.add_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Добавить", u"Добавить", None ) 
		
		self.del_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Удалить", u"Удалить", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.save_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Сохранить", u"Сохранить", None ) 
		
		self.ctrl_toolBar.Realize() 
		
		bSizer4.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		self.ext_listCtrl = wx.ListCtrl( self.ext_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer4.Add( self.ext_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.ext_panel.SetSizer( bSizer4 )
		self.ext_panel.Layout()
		bSizer4.Fit( self.ext_panel )
		self.env_auinotebook.AddPage( self.ext_panel, u"Дополнительные", False, wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_BUTTON ) )
		
		bSizer1.Add( self.env_auinotebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.close_button = wx.Button( self, wx.ID_ANY, u"Закрыть", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.close_button, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onAddToolClicked, id = self.add_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelToolClicked, id = self.del_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSaveToolClicked, id = self.save_tool.GetId() )
		self.close_button.Bind( wx.EVT_BUTTON, self.onCloseButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onAddToolClicked( self, event ):
		event.Skip()
	
	def onDelToolClicked( self, event ):
		event.Skip()
	
	def onSaveToolClicked( self, event ):
		event.Skip()
	
	def onCloseButtonClick( self, event ):
		event.Skip()
	

