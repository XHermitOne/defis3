# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
from ic.components.user import icchecklistctrl

###########################################################################
## Class icPackScanDocPanelProto
###########################################################################

class icPackScanDocPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1185,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.import_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Импортировать из ПО БАЛАНС+", u"Импортировать из ПО БАЛАНС+", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.group_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-indent", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Групповая обработка", u"Групповая обработка", None ) 
		
		self.toggle_checkBox = wx.CheckBox( self.ctrl_toolBar, wx.ID_ANY, u"Вкл./Выкл. все", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ctrl_toolBar.AddControl( self.toggle_checkBox )
		self.n_pages_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-dnd-multiple", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Количество страниц", u"Количество страниц", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.view_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Просмотр", u"Просмотр", None ) 
		
		self.edit_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактирование", u"Редактирование", None ) 
		
		self.quick_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_REPORT_VIEW, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_CHECK, u"Режим быстрого ввода", u"Режим быстрого ввода", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.scan_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-preferences", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Сканирование", u"Сканирование", None ) 
		
		self.archive_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_TO_PARENT, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Переместить в архив", u"Переместить в архив", None ) 
		
		self.ctrl_toolBar.Realize() 
		
		bSizer12.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		self.docs_listCtrl = icchecklistctrl.icCheckListCtrl(parent=self, id=-1, component={'on_toggle_item': 'self.GetParent().onToggleDocItem(None)',
		'on_select_item': 'self.GetParent().onSelectDocItem(event)'})
		bSizer12.Add( self.docs_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Документов в обработке:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer14.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.doc_count_staticText = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.doc_count_staticText.Wrap( -1 )
		self.doc_count_staticText.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer14.Add( self.doc_count_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer14.AddStretchSpacer()
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Сканируемых листов:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		bSizer14.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.page_count_staticText = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.page_count_staticText.Wrap( -1 )
		self.page_count_staticText.SetFont( wx.Font( 18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer14.Add( self.page_count_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer14.AddStretchSpacer()
		
		
		bSizer12.Add( bSizer14, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer12 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onImportToolClicked, id = self.import_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onGroupToolClicked, id = self.group_tool.GetId() )
		self.toggle_checkBox.Bind( wx.EVT_CHECKBOX, self.onToggleCheckBox )
		self.Bind( wx.EVT_TOOL, self.onNPagesToolClicked, id = self.n_pages_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onViewToolClicked, id = self.view_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onQuickToolClicked, id = self.quick_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onScanToolClicked, id = self.scan_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onArchiveToolClicked, id = self.archive_tool.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onImportToolClicked( self, event ):
		event.Skip()
	
	def onGroupToolClicked( self, event ):
		event.Skip()
	
	def onToggleCheckBox( self, event ):
		event.Skip()
	
	def onNPagesToolClicked( self, event ):
		event.Skip()
	
	def onViewToolClicked( self, event ):
		event.Skip()
	
	def onEditToolClicked( self, event ):
		event.Skip()
	
	def onQuickToolClicked( self, event ):
		event.Skip()
	
	def onScanToolClicked( self, event ):
		event.Skip()
	
	def onArchiveToolClicked( self, event ):
		event.Skip()
	

