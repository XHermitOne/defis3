# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class icFilterChoiceDlgProto
###########################################################################

class icFilterChoiceDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор фильтров", pos = wx.DefaultPosition, size = wx.Size( 700,500 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		logicRadioBoxChoices = [ u"ИЛИ", u"И" ]
		self.logicRadioBox = wx.RadioBox( self, wx.ID_ANY, u"Условие", wx.DefaultPosition, wx.DefaultSize, logicRadioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.logicRadioBox.SetSelection( 0 )
		bSizer2.Add( self.logicRadioBox, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_toolBar1 = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.sort_tool = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Сортировать по возрастанию", wx.ArtProvider.GetBitmap( u"gtk-sort-ascending", wx.ART_OTHER ), wx.NullBitmap, wx.ITEM_NORMAL, u"Сортировать по возрастанию", u"Сортировать по возрастанию", None ) 
		
		self.sort_reverse_tool = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Сортировать по убыванию", wx.ArtProvider.GetBitmap( u"gtk-sort-descending", wx.ART_OTHER ), wx.NullBitmap, wx.ITEM_NORMAL, u"Сортировать по убыванию", u"Сортировать по убыванию", None ) 
		
		self.m_toolBar1.AddSeparator()
		
		self.move_up_tool = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Переместить вверх", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_OTHER ), wx.NullBitmap, wx.ITEM_NORMAL, u"Переместить вверх", u"Переместить вверх", None ) 
		
		self.move_down_tool = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Переместить вниз", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_OTHER ), wx.NullBitmap, wx.ITEM_NORMAL, u"Переместить вниз", u"Переместить вниз", None ) 
		
		self.m_toolBar1.Realize() 
		
		bSizer2.Add( self.m_toolBar1, 0, wx.EXPAND, 5 )
		
		filterCheckListChoices = []
		self.filterCheckList = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, filterCheckListChoices, 0 )
		bSizer2.Add( self.filterCheckList, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.limit_staticText = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.limit_staticText.Wrap( -1 )
		bSizer4.Add( self.limit_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.addButton = wx.Button( self, wx.ID_ANY, u"Добавить...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.addButton, 0, wx.ALL, 5 )
		
		self.delButton = wx.Button( self, wx.ID_ANY, u"Удалить", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.delButton, 0, wx.ALL, 5 )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onSortToolClick, id = self.sort_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSortReverseToolClick, id = self.sort_reverse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onMoveUpToolClick, id = self.move_up_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onMoveDownToolClick, id = self.move_down_tool.GetId() )
		self.addButton.Bind( wx.EVT_BUTTON, self.onAddButtonClick )
		self.delButton.Bind( wx.EVT_BUTTON, self.onDelButtonClick )
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSortToolClick( self, event ):
		event.Skip()
	
	def onSortReverseToolClick( self, event ):
		event.Skip()
	
	def onMoveUpToolClick( self, event ):
		event.Skip()
	
	def onMoveDownToolClick( self, event ):
		event.Skip()
	
	def onAddButtonClick( self, event ):
		event.Skip()
	
	def onDelButtonClick( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

