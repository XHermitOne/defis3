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
## Class icCubesOLAPSrvRequestPanelProto
###########################################################################

class icCubesOLAPSrvRequestPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 867,483 ), style = wx.TAB_TRAVERSAL )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer121 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Запрос:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer121.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.request_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer121.Add( self.request_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer10.Add( bSizer121, 0, wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Куб:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		cube_choiceChoices = []
		self.cube_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cube_choiceChoices, 0 )
		self.cube_choice.SetSelection( 0 )
		bSizer2.Add( self.cube_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Метод:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		method_choiceChoices = []
		self.method_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, method_choiceChoices, 0 )
		self.method_choice.SetSelection( 0 )
		bSizer2.Add( self.method_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Измерение:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		dimension_choiceChoices = []
		self.dimension_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dimension_choiceChoices, 0 )
		self.dimension_choice.SetSelection( 0 )
		bSizer2.Add( self.dimension_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer10.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Параметры:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer12.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cut_checkBox = wx.CheckBox( self, wx.ID_ANY, u"cut", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cut_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cut_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cut_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cut_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer9.Add( self.cut_hlp_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer12.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.drilldown_checkBox = wx.CheckBox( self, wx.ID_ANY, u"drilldown", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.drilldown_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.drilldown_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.drilldown_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.drilldown_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer101.Add( self.drilldown_hlp_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer12.Add( bSizer101, 0, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.aggregates_checkBox = wx.CheckBox( self, wx.ID_ANY, u"aggregates", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.aggregates_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.aggregates_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.aggregates_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.aggregates_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer11.Add( self.aggregates_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.measures_checkBox = wx.CheckBox( self, wx.ID_ANY, u"measures", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.measures_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.measures_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.measures_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.measures_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer111.Add( self.measures_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer111, 0, wx.EXPAND, 5 )
		
		bSizer1111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.page_checkBox = wx.CheckBox( self, wx.ID_ANY, u"page", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1111.Add( self.page_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.page_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1111.Add( self.page_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.page_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer1111.Add( self.page_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer1111, 0, wx.EXPAND, 5 )
		
		bSizer11111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.pagesize_checkBox = wx.CheckBox( self, wx.ID_ANY, u"pagesize", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11111.Add( self.pagesize_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pagesize_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11111.Add( self.pagesize_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pagesize_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer11111.Add( self.pagesize_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer11111, 0, wx.EXPAND, 5 )
		
		bSizer11112 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.order_checkBox = wx.CheckBox( self, wx.ID_ANY, u"order", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11112.Add( self.order_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.order_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11112.Add( self.order_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.order_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer11112.Add( self.order_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer11112, 0, wx.EXPAND, 5 )
		
		bSizer11113 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.split_checkBox = wx.CheckBox( self, wx.ID_ANY, u"split", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11113.Add( self.split_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.split_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11113.Add( self.split_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.split_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer11113.Add( self.split_hlp_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer11113, 0, wx.EXPAND, 5 )
		
		
		bSizer10.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer10 )
		self.Layout()
		
		# Connect Events
		self.cube_choice.Bind( wx.EVT_CHOICE, self.onCubeChoice )
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
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCubeChoice( self, event ):
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
	

###########################################################################
## Class icEditCubesOLAPSrvRequestDlgProto
###########################################################################

class icEditCubesOLAPSrvRequestDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Редактирование запроса к OLAP серверу", pos = wx.DefaultPosition, size = wx.Size( 874,736 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		self.request_panel = icCubesOLAPSrvRequestPanelProto(parent=self)
		bSizer13.Add( self.request_panel, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer13.Add( bSizer14, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer13 )
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
	

