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
import  wx.gizmos

###########################################################################
## Class icSpravChoiceListDlgProto
###########################################################################

class icSpravChoiceListDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 698,421 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.path_statictext = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.path_statictext.Wrap( -1 )
		bSizer1.Add( self.path_statictext, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.dlg_toolbar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.return_tool = self.dlg_toolbar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_TO_PARENT, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.dlg_toolbar.AddSeparator()
		
		self.m_staticText2 = wx.StaticText( self.dlg_toolbar, wx.ID_ANY, u"Найти:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.dlg_toolbar.AddControl( self.m_staticText2 )
		self.search_textctrl = wx.TextCtrl( self.dlg_toolbar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
		self.search_textctrl.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		self.dlg_toolbar.AddControl( self.search_textctrl )
		self.search_tool = self.dlg_toolbar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.dlg_toolbar.Realize() 
		
		bSizer1.Add( self.dlg_toolbar, 0, wx.EXPAND, 5 )
		
		self.sprav_list_ctrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer1.Add( self.sprav_list_ctrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onReturnToolClick, id = self.return_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSearchToolClick, id = self.search_tool.GetId() )
		self.sprav_list_ctrl.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.onSpravListItemActive )
		self.sprav_list_ctrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.onSpravListItemSelect )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onReturnToolClick( self, event ):
		event.Skip()
	
	def onSearchToolClick( self, event ):
		event.Skip()
	
	def onSpravListItemActive( self, event ):
		event.Skip()
	
	def onSpravListItemSelect( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class icSpravEditDlgProto
###########################################################################

class icSpravEditDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Редактирование справочника", pos = wx.DefaultPosition, size = wx.Size( 1097,408 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panel1 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.search_toolBar = wx.ToolBar( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_staticText4 = wx.StaticText( self.search_toolBar, wx.ID_ANY, u"Найти:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		self.search_toolBar.AddControl( self.m_staticText4 )
		self.search_textCtrl = wx.TextCtrl( self.search_toolBar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.search_toolBar.AddControl( self.search_textCtrl )
		self.search_tool = self.search_toolBar.AddLabelTool( wx.ID_ANY, u"Найти", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Найти", u"Найти", None ) 
		
		self.search_toolBar.Realize() 
		
		bSizer4.Add( self.search_toolBar, 0, wx.EXPAND, 5 )
		
		self.sprav_treeCtrl = wx.TreeCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		bSizer4.Add( self.sprav_treeCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer4 )
		self.m_panel1.Layout()
		bSizer4.Fit( self.m_panel1 )
		self.m_panel2 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.add_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Добавить", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Добавить", u"Добавить", None ) 
		
		self.edit_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Редактировать", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактировать", u"Редактировать", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.del_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Удалить", wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Удалить", u"Удалить", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.m_staticText41 = wx.StaticText( self.ctrl_toolBar, wx.ID_ANY, u"Найти:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		self.ctrl_toolBar.AddControl( self.m_staticText41 )
		self.find_textCtrl = wx.TextCtrl( self.ctrl_toolBar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.ctrl_toolBar.AddControl( self.find_textCtrl )
		self.find_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Найти", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Найти", u"Найти", None ) 
		
		self.ctrl_toolBar.Realize() 
		
		bSizer5.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		self.recs_listCtrl = wx.ListCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer5.Add( self.recs_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer5 )
		self.m_panel2.Layout()
		bSizer5.Fit( self.m_panel2 )
		self.m_splitter1.SplitVertically( self.m_panel1, self.m_panel2, 400 )
		bSizer3.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer11.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer11, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.search_textCtrl.Bind( wx.EVT_TEXT, self.onSearchText )
		self.Bind( wx.EVT_TOOL, self.onSearchToolClicked, id = self.search_tool.GetId() )
		self.sprav_treeCtrl.Bind( wx.EVT_TREE_ITEM_COLLAPSED, self.onSpravTreeItemCollapsed )
		self.sprav_treeCtrl.Bind( wx.EVT_TREE_ITEM_EXPANDED, self.onSpravTreeItemExpanded )
		self.sprav_treeCtrl.Bind( wx.EVT_TREE_SEL_CHANGED, self.onSpravTreeSelChanged )
		self.Bind( wx.EVT_TOOL, self.onAddToolClicked, id = self.add_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelToolClicked, id = self.del_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onFindToolClicked, id = self.find_tool.GetId() )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSearchText( self, event ):
		event.Skip()
	
	def onSearchToolClicked( self, event ):
		event.Skip()
	
	def onSpravTreeItemCollapsed( self, event ):
		event.Skip()
	
	def onSpravTreeItemExpanded( self, event ):
		event.Skip()
	
	def onSpravTreeSelChanged( self, event ):
		event.Skip()
	
	def onAddToolClicked( self, event ):
		event.Skip()
	
	def onEditToolClicked( self, event ):
		event.Skip()
	
	def onDelToolClicked( self, event ):
		event.Skip()
	
	def onFindToolClicked( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 400 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	

###########################################################################
## Class icSpravRecEditDlgProto
###########################################################################

class icSpravRecEditDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Редактирование записи справочника", pos = wx.DefaultPosition, size = wx.Size( 479,467 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.record_propertyGrid = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		bSizer7.Add( self.record_propertyGrid, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer6 )
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
	

###########################################################################
## Class icSpravChoiceTreeDlgProto
###########################################################################

class icSpravChoiceTreeDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 953,439 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.search_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		search_field_choiceChoices = []
		self.search_field_choice = wx.Choice( self.search_toolBar, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,-1 ), search_field_choiceChoices, 0 )
		self.search_field_choice.SetSelection( 0 )
		self.search_toolBar.AddControl( self.search_field_choice )
		self.search_toolBar.AddSeparator()
		
		self.m_staticText2 = wx.StaticText( self.search_toolBar, wx.ID_ANY, u"Найти:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.search_toolBar.AddControl( self.m_staticText2 )
		self.search_textCtrl = wx.TextCtrl( self.search_toolBar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
		self.search_textCtrl.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		self.search_toolBar.AddControl( self.search_textCtrl )
		self.search_tool = self.search_toolBar.AddLabelTool( wx.ID_ANY, u"Найти", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Найти", u"Найти", None ) 
		
		self.search_toolBar.Realize() 
		
		bSizer9.Add( self.search_toolBar, 0, wx.EXPAND, 5 )
		
		self.sprav_treeListCtrl = wx.gizmos.TreeListCtrl(parent=self, id=-1, style=wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT)
		bSizer9.Add( self.sprav_treeListCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.edit_button = wx.Button( self, wx.ID_ANY, u"Редактирование...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.edit_button, 0, wx.ALL, 5 )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer10.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer9.Add( bSizer10, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_ACTIVATE, self.onActivateDlg )
		self.Bind( wx.EVT_CLOSE, self.onCloseDlg )
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDlg )
		self.search_textCtrl.Bind( wx.EVT_TEXT, self.onSearchText )
		self.Bind( wx.EVT_TOOL, self.onSearchToolClicked, id = self.search_tool.GetId() )
		self.edit_button.Bind( wx.EVT_BUTTON, self.onEditButtonClick )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onActivateDlg( self, event ):
		event.Skip()
	
	def onCloseDlg( self, event ):
		event.Skip()
	
	def onInitDlg( self, event ):
		event.Skip()
	
	def onSearchText( self, event ):
		event.Skip()
	
	def onSearchToolClicked( self, event ):
		event.Skip()
	
	def onEditButtonClick( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

