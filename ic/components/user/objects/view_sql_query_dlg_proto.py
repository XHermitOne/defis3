# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.propgrid as pg

###########################################################################
## Class icViewSQLQueryDialogProto
###########################################################################

class icViewSQLQueryDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Просмотр результатов SQL запроса", pos = wx.DefaultPosition, size = wx.Size( 856,619 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )
		
		self.query_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.query_splitter = wx.SplitterWindow( self.query_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.query_splitter.Bind( wx.EVT_IDLE, self.query_splitterOnIdle )
		
		self.var_panel = wx.Panel( self.query_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self.var_panel, wx.ID_ANY, u"Переменные:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer5.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.var_propertyGrid = pg.PropertyGrid(self.var_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		bSizer5.Add( self.var_propertyGrid, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.var_panel.SetSizer( bSizer5 )
		self.var_panel.Layout()
		bSizer5.Fit( self.var_panel )
		self.sql_panel = wx.Panel( self.query_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self.sql_panel, wx.ID_ANY, u"SQL запрос:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer6.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.sql_textCtrl = wx.TextCtrl( self.sql_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer6.Add( self.sql_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.sql_panel.SetSizer( bSizer6 )
		self.sql_panel.Layout()
		bSizer6.Fit( self.sql_panel )
		self.query_splitter.SplitVertically( self.var_panel, self.sql_panel, 300 )
		bSizer3.Add( self.query_splitter, 1, wx.EXPAND, 5 )
		
		
		self.query_panel.SetSizer( bSizer3 )
		self.query_panel.Layout()
		bSizer3.Fit( self.query_panel )
		self.table_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self.table_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.collapse_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Свернуть панель", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Свернуть панель", u"Свернуть панель", None ) 
		
		self.expand_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Развернуть панель", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Развернуть панель", u"Развернуть панель", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.refresh_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Обновить результаты запроса", wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Обновить результаты запроса", u"Обновить результаты запроса", None ) 
		
		self.ctrl_toolBar.Realize() 
		
		bSizer4.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		self.records_listCtrl = wx.ListCtrl( self.table_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer4.Add( self.records_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.table_panel.SetSizer( bSizer4 )
		self.table_panel.Layout()
		bSizer4.Fit( self.table_panel )
		self.panel_splitter.SplitHorizontally( self.query_panel, self.table_panel, 0 )
		bSizer1.Add( self.panel_splitter, 1, wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer2.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onRefreshToolClicked, id = self.refresh_tool.GetId() )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked( self, event ):
		event.Skip()
	
	def onExpandToolClicked( self, event ):
		event.Skip()
	
	def onRefreshToolClicked( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	
	def panel_splitterOnIdle( self, event ):
		self.panel_splitter.SetSashPosition( 0 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )
	
	def query_splitterOnIdle( self, event ):
		self.query_splitter.SetSashPosition( 300 )
		self.query_splitter.Unbind( wx.EVT_IDLE )
	

