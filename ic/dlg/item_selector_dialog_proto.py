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
## Class icItemSelectorPanelProto
###########################################################################

class icItemSelectorPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 881,654 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )
		
		self.list_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.record_listCtrl = wx.ListCtrl( self.list_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer2.Add( self.record_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.list_panel.SetSizer( bSizer2 )
		self.list_panel.Layout()
		bSizer2.Fit( self.list_panel )
		self.selector_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.on_label_staticText = wx.StaticText( self.selector_panel, wx.ID_ANY, u"Присутствуют", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.on_label_staticText.Wrap( -1 )
		self.on_label_staticText.SetForegroundColour( wx.Colour( 0, 128, 0 ) )
		
		bSizer4.Add( self.on_label_staticText, 0, wx.ALL, 5 )
		
		on_checkListChoices = []
		self.on_checkList = wx.CheckListBox( self.selector_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, on_checkListChoices, 0 )
		self.on_checkList.SetForegroundColour( wx.Colour( 0, 128, 0 ) )
		
		bSizer4.Add( self.on_checkList, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.off_all_button = wx.Button( self.selector_panel, wx.ID_ANY, u">>", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.off_all_button.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		self.off_all_button.SetForegroundColour( wx.Colour( 128, 0, 0 ) )
		
		bSizer5.Add( self.off_all_button, 0, wx.ALL, 5 )
		
		self.off_button = wx.Button( self.selector_panel, wx.ID_ANY, u">", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.off_button.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		self.off_button.SetForegroundColour( wx.Colour( 128, 0, 0 ) )
		
		bSizer5.Add( self.off_button, 0, wx.ALL, 5 )
		
		self.on_button = wx.Button( self.selector_panel, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.on_button.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		self.on_button.SetForegroundColour( wx.Colour( 0, 128, 0 ) )
		
		bSizer5.Add( self.on_button, 0, wx.ALL, 5 )
		
		self.on_all_button = wx.Button( self.selector_panel, wx.ID_ANY, u"<<", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.on_all_button.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		self.on_all_button.SetForegroundColour( wx.Colour( 0, 128, 0 ) )
		
		bSizer5.Add( self.on_all_button, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer5, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.off_label_staticText = wx.StaticText( self.selector_panel, wx.ID_ANY, u"Отсутствуют", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.off_label_staticText.Wrap( -1 )
		self.off_label_staticText.SetForegroundColour( wx.Colour( 128, 0, 0 ) )
		
		bSizer6.Add( self.off_label_staticText, 0, wx.ALL, 5 )
		
		off_checkListChoices = []
		self.off_checkList = wx.CheckListBox( self.selector_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, off_checkListChoices, 0 )
		self.off_checkList.SetForegroundColour( wx.Colour( 128, 0, 0 ) )
		
		bSizer6.Add( self.off_checkList, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		self.selector_panel.SetSizer( bSizer3 )
		self.selector_panel.Layout()
		bSizer3.Fit( self.selector_panel )
		self.panel_splitter.SplitHorizontally( self.list_panel, self.selector_panel, 0 )
		bSizer1.Add( self.panel_splitter, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.record_listCtrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.onRecordListItemSelected )
		self.off_all_button.Bind( wx.EVT_BUTTON, self.onOffAllButtonClick )
		self.off_button.Bind( wx.EVT_BUTTON, self.onOffButtonClick )
		self.on_button.Bind( wx.EVT_BUTTON, self.onOnButtonClick )
		self.on_all_button.Bind( wx.EVT_BUTTON, self.onOnAllButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onRecordListItemSelected( self, event ):
		event.Skip()
	
	def onOffAllButtonClick( self, event ):
		event.Skip()
	
	def onOffButtonClick( self, event ):
		event.Skip()
	
	def onOnButtonClick( self, event ):
		event.Skip()
	
	def onOnAllButtonClick( self, event ):
		event.Skip()
	
	def panel_splitterOnIdle( self, event ):
		self.panel_splitter.SetSashPosition( 0 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )
	

###########################################################################
## Class icItemSelectorDialogProto
###########################################################################

class icItemSelectorDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 873,703 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.browse_panel = icItemSelectorPanelProto(parent=self)
		bSizer7.Add( self.browse_panel, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer7.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer7 )
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
	

