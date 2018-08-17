# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from wx.lib import masked

###########################################################################
## Class icLogBrowserPanelProto
###########################################################################

class icLogBrowserPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 933,372 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.log_filePicker = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Выберите файл журнала сообщений", u"*.log", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer3.Add( self.log_filePicker, 0, wx.ALL|wx.EXPAND, 5 )
		
		dtSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.start_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Вкл.", wx.DefaultPosition, wx.DefaultSize, 0 )
		dtSizer.Add( self.start_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.start_datePicker = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
		self.start_datePicker.Enable( False )
		
		dtSizer.Add( self.start_datePicker, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.start_timeControl = masked.TimeCtrl(self, -1, fmt24hr=True)
		self.start_timeControl.Enable( False )
		
		dtSizer.Add( self.start_timeControl, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.start_spinBtn = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.start_spinBtn.Enable( False )
		
		dtSizer.Add( self.start_spinBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		dtSizer.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.stop_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Вкл.", wx.DefaultPosition, wx.DefaultSize, 0 )
		dtSizer.Add( self.stop_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.stop_datePicker = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
		self.stop_datePicker.Enable( False )
		
		dtSizer.Add( self.stop_datePicker, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.stop_timeControl=masked.TimeCtrl(self, -1, fmt24hr=True)
		self.stop_timeControl.Enable( False )
		
		dtSizer.Add( self.stop_timeControl, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.stop_spinBtn = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stop_spinBtn.Enable( False )
		
		dtSizer.Add( self.stop_spinBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		
		bSizer3.Add( dtSizer, 0, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.info_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Информация", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.info_checkBox.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.info_checkBox.SetForegroundColour( wx.Colour( 9, 79, 9 ) )
		
		bSizer5.Add( self.info_checkBox, 0, wx.ALL, 5 )
		
		self.warning_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Предупреждения", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.warning_checkBox.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.warning_checkBox.SetForegroundColour( wx.Colour( 120, 120, 9 ) )
		
		bSizer5.Add( self.warning_checkBox, 0, wx.ALL, 5 )
		
		self.error_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Ошибки", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.error_checkBox.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.error_checkBox.SetForegroundColour( wx.Colour( 79, 9, 9 ) )
		
		bSizer5.Add( self.error_checkBox, 0, wx.ALL, 5 )
		
		self.fatal_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Критические", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fatal_checkBox.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.fatal_checkBox.SetForegroundColour( wx.Colour( 120, 9, 9 ) )
		
		bSizer5.Add( self.fatal_checkBox, 0, wx.ALL, 5 )
		
		self.debug_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Отладка", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.debug_checkBox.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.debug_checkBox.SetForegroundColour( wx.Colour( 9, 9, 79 ) )
		
		bSizer5.Add( self.debug_checkBox, 0, wx.ALL, 5 )
		
		self.service_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Сервисные", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.service_checkBox.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.service_checkBox.SetForegroundColour( wx.Colour( 9, 79, 79 ) )
		
		bSizer5.Add( self.service_checkBox, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		filter_checkListChoices = []
		self.filter_checkList = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, filter_checkListChoices, 0 )
		bSizer8.Add( self.filter_checkList, 1, wx.ALL|wx.EXPAND, 5 )
		
		logic_radioBoxChoices = [ u"И", u"ИЛИ" ]
		self.logic_radioBox = wx.RadioBox( self, wx.ID_ANY, u"Условие выбора", wx.DefaultPosition, wx.DefaultSize, logic_radioBoxChoices, 1, wx.RA_SPECIFY_COLS )
		self.logic_radioBox.SetSelection( 0 )
		bSizer8.Add( self.logic_radioBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer3.Add( bSizer8, 0, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		self.refresh_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_CMN_DIALOG ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.refresh_bpButton.SetDefault() 
		bSizer2.Add( self.refresh_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		self.msg_listCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer1.Add( self.msg_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.start_checkBox.Bind( wx.EVT_CHECKBOX, self.onStartCheckBox )
		self.stop_checkBox.Bind( wx.EVT_CHECKBOX, self.onStopCheckBox )
		self.refresh_bpButton.Bind( wx.EVT_BUTTON, self.onRefreshButtonClick )
		self.msg_listCtrl.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.onMsgListItemActivated )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onStartCheckBox( self, event ):
		event.Skip()
	
	def onStopCheckBox( self, event ):
		event.Skip()
	
	def onRefreshButtonClick( self, event ):
		event.Skip()
	
	def onMsgListItemActivated( self, event ):
		event.Skip()
	

###########################################################################
## Class icLogBrowserDialogProto
###########################################################################

class icLogBrowserDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Список сообщений программы", pos = wx.DefaultPosition, size = wx.Size( 1220,475 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.browser_panel = icLogBrowserPanelProto(parent=self)
		bSizer6.Add( self.browser_panel, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.ok_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer6.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onOkButtonClick( self, event ):
		event.Skip()
	

