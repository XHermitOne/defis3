# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 16 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv

###########################################################################
## Class icGroupManipulationDlgProto
###########################################################################

class icGroupManipulationDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Групповая обработка", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Диапазон:" ), wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Первый номер:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.begin_spinCtrl = wx.SpinCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 1 )
		bSizer2.Add( self.begin_spinCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Последний номер:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer3.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.end_spinCtrl = wx.SpinCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 1 )
		bSizer3.Add( self.end_spinCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( sbSizer1, 1, wx.EXPAND, 5 )
		
		self.on_off_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Вкл./Выкл. обработки", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.on_off_checkBox.SetValue(True) 
		bSizer1.Add( self.on_off_checkBox, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.ext_options_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Дополнительные настройки:", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.ext_options_checkBox, 0, wx.ALL, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Параметры сканирования:" ), wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.pages_staticText = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Количество листов:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pages_staticText.Wrap( -1 )
		self.pages_staticText.Enable( False )
		
		bSizer4.Add( self.pages_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pages_spinCtrl = wx.SpinCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 100, 1 )
		self.pages_spinCtrl.Enable( False )
		
		bSizer4.Add( self.pages_spinCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		self.duplex_checkBox = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Двустроннее сканирование/дуплекс", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.duplex_checkBox.Enable( False )
		
		sbSizer2.Add( self.duplex_checkBox, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer5.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer5, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.begin_spinCtrl.Bind( wx.EVT_SPINCTRL, self.onBeginSpinCtrl )
		self.end_spinCtrl.Bind( wx.EVT_SPINCTRL, self.onEndSpinCtrl )
		self.ext_options_checkBox.Bind( wx.EVT_CHECKBOX, self.onExtOptionsCheckBox )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onBeginSpinCtrl( self, event ):
		event.Skip()
	
	def onEndSpinCtrl( self, event ):
		event.Skip()
	
	def onExtOptionsCheckBox( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

