# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.stc
import wx.grid

###########################################################################
## Class icCubesOLAPSrvTestDialogProto
###########################################################################

class icCubesOLAPSrvTestDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"OLAP сервер", pos = wx.DefaultPosition, size = wx.Size( 870,734 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )
		
		self.request_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText6 = wx.StaticText( self.request_panel, wx.ID_ANY, u"Запрос:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer10.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.request_panel, wx.ID_ANY, u"Куб:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		cube_choiceChoices = []
		self.cube_choice = wx.Choice( self.request_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cube_choiceChoices, 0 )
		self.cube_choice.SetSelection( 0 )
		bSizer2.Add( self.cube_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText2 = wx.StaticText( self.request_panel, wx.ID_ANY, u"Метод:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		method_choiceChoices = []
		self.method_choice = wx.Choice( self.request_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, method_choiceChoices, 0 )
		self.method_choice.SetSelection( 0 )
		bSizer2.Add( self.method_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.request_panel, wx.ID_ANY, u"Измерение:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		dimension_choiceChoices = []
		self.dimension_choice = wx.Choice( self.request_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dimension_choiceChoices, 0 )
		self.dimension_choice.SetSelection( 0 )
		bSizer2.Add( self.dimension_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer2.AddStretchSpacer()
		
		self.refresh_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer2.Add( self.refresh_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self.request_panel, wx.ID_ANY, u"Параметры:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer12.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cut_checkBox = wx.CheckBox( self.request_panel, wx.ID_ANY, u"cut", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cut_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cut_textCtrl = wx.TextCtrl( self.request_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cut_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cut_hlp_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer9.Add( self.cut_hlp_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer12.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.drilldown_checkBox = wx.CheckBox( self.request_panel, wx.ID_ANY, u"drilldown", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.drilldown_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.drilldown_textCtrl = wx.TextCtrl( self.request_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.drilldown_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.drilldown_hlp_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer101.Add( self.drilldown_hlp_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer12.Add( bSizer101, 0, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.aggregates_checkBox = wx.CheckBox( self.request_panel, wx.ID_ANY, u"aggregates", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.aggregates_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.aggregates_textCtrl = wx.TextCtrl( self.request_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.aggregates_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.aggregates_hlp_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer11.Add( self.aggregates_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.measures_checkBox = wx.CheckBox( self.request_panel, wx.ID_ANY, u"measures", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.measures_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.measures_textCtrl = wx.TextCtrl( self.request_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.measures_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.measures_hlp_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer111.Add( self.measures_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer111, 1, wx.EXPAND, 5 )
		
		bSizer1111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.page_checkBox = wx.CheckBox( self.request_panel, wx.ID_ANY, u"page", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1111.Add( self.page_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.page_textCtrl = wx.TextCtrl( self.request_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1111.Add( self.page_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.page_hlp_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer1111.Add( self.page_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer1111, 1, wx.EXPAND, 5 )
		
		bSizer11111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.pagesize_checkBox = wx.CheckBox( self.request_panel, wx.ID_ANY, u"pagesize", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11111.Add( self.pagesize_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pagesize_textCtrl = wx.TextCtrl( self.request_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11111.Add( self.pagesize_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pagesize_hlp_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer11111.Add( self.pagesize_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer11111, 1, wx.EXPAND, 5 )
		
		bSizer11112 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.order_checkBox = wx.CheckBox( self.request_panel, wx.ID_ANY, u"order", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11112.Add( self.order_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.order_textCtrl = wx.TextCtrl( self.request_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11112.Add( self.order_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.order_hlp_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer11112.Add( self.order_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer11112, 1, wx.EXPAND, 5 )
		
		bSizer11113 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.split_checkBox = wx.CheckBox( self.request_panel, wx.ID_ANY, u"split", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11113.Add( self.split_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.split_textCtrl = wx.TextCtrl( self.request_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11113.Add( self.split_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.split_hlp_bpButton = wx.BitmapButton( self.request_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer11113.Add( self.split_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer11113, 1, wx.EXPAND, 5 )
		
		
		bSizer10.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		self.request_panel.SetSizer( bSizer10 )
		self.request_panel.Layout()
		bSizer10.Fit( self.request_panel )
		self.response_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.response_splitter = wx.SplitterWindow( self.response_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.response_splitter.Bind( wx.EVT_IDLE, self.response_splitterOnIdle )
		
		self.json_panel = wx.Panel( self.response_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText4 = wx.StaticText( self.json_panel, wx.ID_ANY, u"Результат:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer7.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.json_scintilla = wx.stc.StyledTextCtrl(parent=self.json_panel, id=wx.NewId())
		bSizer7.Add( self.json_scintilla, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.json_panel.SetSizer( bSizer7 )
		self.json_panel.Layout()
		bSizer7.Fit( self.json_panel )
		self.spreadsheet_panel = wx.Panel( self.response_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText5 = wx.StaticText( self.spreadsheet_panel, wx.ID_ANY, u"Результат в табличной форме:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.spreadsheet_grid = wx.grid.Grid( self.spreadsheet_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.spreadsheet_grid.CreateGrid( 5, 5 )
		self.spreadsheet_grid.EnableEditing( True )
		self.spreadsheet_grid.EnableGridLines( True )
		self.spreadsheet_grid.EnableDragGridSize( False )
		self.spreadsheet_grid.SetMargins( 0, 0 )
		
		# Columns
		self.spreadsheet_grid.EnableDragColMove( False )
		self.spreadsheet_grid.EnableDragColSize( True )
		self.spreadsheet_grid.SetColLabelSize( 0 )
		self.spreadsheet_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.spreadsheet_grid.EnableDragRowSize( True )
		self.spreadsheet_grid.SetRowLabelSize( 0 )
		self.spreadsheet_grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.spreadsheet_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer8.Add( self.spreadsheet_grid, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.spreadsheet_panel.SetSizer( bSizer8 )
		self.spreadsheet_panel.Layout()
		bSizer8.Fit( self.spreadsheet_panel )
		self.response_splitter.SplitVertically( self.json_panel, self.spreadsheet_panel, 250 )
		bSizer5.Add( self.response_splitter, 1, wx.EXPAND, 5 )
		
		
		self.response_panel.SetSizer( bSizer5 )
		self.response_panel.Layout()
		bSizer5.Fit( self.response_panel )
		self.panel_splitter.SplitHorizontally( self.request_panel, self.response_panel, 0 )
		bSizer1.Add( self.panel_splitter, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.close_button = wx.Button( self, wx.ID_ANY, u"Закрыть", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.close_button, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer3, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cube_choice.Bind( wx.EVT_CHOICE, self.onCubeChoice )
		self.refresh_bpButton.Bind( wx.EVT_BUTTON, self.onRefreshButtonClick )
		self.cut_checkBox.Bind( wx.EVT_CHECKBOX, self.onCutCheckBox )
		self.cut_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onCutHelpButtonClick )
		self.drilldown_checkBox.Bind( wx.EVT_CHECKBOX, self.onDrilldownCheckBox )
		self.drilldown_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onDrilldownHelpButtonClick )
		self.aggregates_checkBox.Bind( wx.EVT_CHECKBOX, self.onAggregatesCheckBox )
		self.aggregates_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onAggregatesHelpButtonClick )
		self.measures_checkBox.Bind( wx.EVT_CHECKBOX, self.onMeasuresCheckBox )
		self.measures_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onMeasuresHelpButtonClick )
		self.page_checkBox.Bind( wx.EVT_CHECKBOX, self.onPageCheckBox )
		self.page_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onPageHelpButtonClick )
		self.pagesize_checkBox.Bind( wx.EVT_CHECKBOX, self.onPagesizeCheckBox )
		self.pagesize_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onPagesizeHelpButtonClick )
		self.order_checkBox.Bind( wx.EVT_CHECKBOX, self.onOrderCheckBox )
		self.order_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onOrderHelpButtonClick )
		self.split_checkBox.Bind( wx.EVT_CHECKBOX, self.onSplitCheckBox )
		self.split_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onSplitHelpButtonClick )
		self.close_button.Bind( wx.EVT_BUTTON, self.onCloseButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCubeChoice( self, event ):
		event.Skip()
	
	def onRefreshButtonClick( self, event ):
		event.Skip()
	
	def onCutCheckBox( self, event ):
		event.Skip()
	
	def onCutHelpButtonClick( self, event ):
		event.Skip()
	
	def onDrilldownCheckBox( self, event ):
		event.Skip()
	
	def onDrilldownHelpButtonClick( self, event ):
		event.Skip()
	
	def onAggregatesCheckBox( self, event ):
		event.Skip()
	
	def onAggregatesHelpButtonClick( self, event ):
		event.Skip()
	
	def onMeasuresCheckBox( self, event ):
		event.Skip()
	
	def onMeasuresHelpButtonClick( self, event ):
		event.Skip()
	
	def onPageCheckBox( self, event ):
		event.Skip()
	
	def onPageHelpButtonClick( self, event ):
		event.Skip()
	
	def onPagesizeCheckBox( self, event ):
		event.Skip()
	
	def onPagesizeHelpButtonClick( self, event ):
		event.Skip()
	
	def onOrderCheckBox( self, event ):
		event.Skip()
	
	def onOrderHelpButtonClick( self, event ):
		event.Skip()
	
	def onSplitCheckBox( self, event ):
		event.Skip()
	
	def onSplitHelpButtonClick( self, event ):
		event.Skip()
	
	def onCloseButtonClick( self, event ):
		event.Skip()
	
	def panel_splitterOnIdle( self, event ):
		self.panel_splitter.SetSashPosition( 0 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )
	
	def response_splitterOnIdle( self, event ):
		self.response_splitter.SetSashPosition( 250 )
		self.response_splitter.Unbind( wx.EVT_IDLE )
	

