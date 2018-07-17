# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import wx.dataview
from NSI.usercomponents import spravlevelchoicectrl
from NSI.usercomponents import spravtreecomboctrl

###########################################################################
## Class icWMSTruckConstructorPanelProto
###########################################################################

class icWMSTruckConstructorPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1055,570 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		
		self.m_panel7 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.constructor_splitter = wx.SplitterWindow( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.constructor_splitter.Bind( wx.EVT_IDLE, self.constructor_splitterOnIdle )
		
		self.constructor_panel = wx.Panel( self.constructor_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		constructor_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		
		self.constructor_panel.SetSizer( constructor_sizer )
		self.constructor_panel.Layout()
		constructor_sizer.Fit( self.constructor_panel )
		self.meter_panel = wx.Panel( self.constructor_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		meter_sizer = wx.StaticBoxSizer( wx.StaticBox( self.meter_panel, wx.ID_ANY, u"Нагрузка на оси (кг):" ), wx.HORIZONTAL )
		
		self.meter_listCtrl = wx.grid.Grid( meter_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.meter_listCtrl.CreateGrid( 0, 5 )
		self.meter_listCtrl.EnableEditing( False )
		self.meter_listCtrl.EnableGridLines( True )
		self.meter_listCtrl.EnableDragGridSize( False )
		self.meter_listCtrl.SetMargins( 0, 0 )
		
		# Columns
		self.meter_listCtrl.EnableDragColMove( False )
		self.meter_listCtrl.EnableDragColSize( True )
		self.meter_listCtrl.SetColLabelSize( 30 )
		self.meter_listCtrl.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.meter_listCtrl.EnableDragRowSize( True )
		self.meter_listCtrl.SetRowLabelSize( 0 )
		self.meter_listCtrl.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.meter_listCtrl.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		meter_sizer.Add( self.meter_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.meter_panel.SetSizer( meter_sizer )
		self.meter_panel.Layout()
		meter_sizer.Fit( self.meter_panel )
		self.constructor_splitter.SplitHorizontally( self.constructor_panel, self.meter_panel, 500 )
		bSizer8.Add( self.constructor_splitter, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.calc_button = wx.Button( self.m_panel7, wx.ID_ANY, u"Расчитать", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.calc_button, 0, wx.ALL, 5 )
		
		
		bSizer8.Add( bSizer3, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel7.SetSizer( bSizer8 )
		self.m_panel7.Layout()
		bSizer8.Fit( self.m_panel7 )
		self.m_panel8 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.box_toolBar = wx.ToolBar( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.moveup_tool = self.box_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Переместить вниз", u"Переместить вниз", None ) 
		
		self.movedown_tool = self.box_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Переместить вниз", u"Переместить вниз", None ) 
		
		self.box_toolBar.Realize() 
		
		bSizer10.Add( self.box_toolBar, 0, wx.EXPAND, 5 )
		
		self.box_ListCtrl = wx.dataview.DataViewListCtrl( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_SINGLE )
		self.n_column = self.box_ListCtrl.AppendTextColumn( u"№" )
		self.nomenklature_column = self.box_ListCtrl.AppendTextColumn( u"Наименование" )
		self.row_column = self.box_ListCtrl.AppendTextColumn( u"Ряд." )
		self.madedate_column = self.box_ListCtrl.AppendTextColumn( u"Дата" )
		self.weight_column = self.box_ListCtrl.AppendTextColumn( u"Вес (кг)" )
		bSizer10.Add( self.box_ListCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel8.SetSizer( bSizer10 )
		self.m_panel8.Layout()
		bSizer10.Fit( self.m_panel8 )
		self.m_splitter2.SplitVertically( self.m_panel7, self.m_panel8, 850 )
		bSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.calc_button.Bind( wx.EVT_BUTTON, self.onCalcButtonClick )
		self.Bind( wx.EVT_TOOL, self.onMoveUpToolClicked, id = self.moveup_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onMoveDownToolClicked, id = self.movedown_tool.GetId() )
		self.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.onBoxListCtrlSelectionChanged, id = wx.ID_ANY )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCalcButtonClick( self, event ):
		event.Skip()
	
	def onMoveUpToolClicked( self, event ):
		event.Skip()
	
	def onMoveDownToolClicked( self, event ):
		event.Skip()
	
	def onBoxListCtrlSelectionChanged( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 850 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def constructor_splitterOnIdle( self, event ):
		self.constructor_splitter.SetSashPosition( 500 )
		self.constructor_splitter.Unbind( wx.EVT_IDLE )
	

###########################################################################
## Class icAddBoxDialogProto
###########################################################################

class icAddBoxDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Добавление нового паллета", pos = wx.DefaultPosition, size = wx.Size( 633,346 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.nomenklature_choice = spravlevelchoicectrl.icSpravLevelChoiceCtrl(self, wx.NewId(), {'sprav': (('Sprav', 'nomenklature', None, 'nsi_product.mtd', 'ayan_product'),), 'size': (-1, 160)})
		bSizer4.Add( self.nomenklature_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Рядность:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.row_edit = spravtreecomboctrl.icSpravTreeComboCtrl(self.m_scrolledWindow1, wx.NewId(), {'sprav': (('Sprav', 'pallet', None, 'nsi_product.mtd', 'ayan_product'),)})
		fgSizer1.Add( self.row_edit, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText2 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Дата розлива:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.made_datePicker = wx.DatePickerCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
		fgSizer1.Add( self.made_datePicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		self.m_scrolledWindow1.SetSizer( fgSizer1 )
		self.m_scrolledWindow1.Layout()
		fgSizer1.Fit( self.m_scrolledWindow1 )
		bSizer4.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

