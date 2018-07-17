# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.lib.masked

###########################################################################
## Class icDateTimeCtrlProtoDepricate
###########################################################################

class icDateTimeCtrlProtoDepricate ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 300,37 ), style = wx.TAB_TRAVERSAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.dateEdit = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_ALLOWNONE|wx.DP_DEFAULT )
		bSizer7.Add( self.dateEdit, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.timeEdit = wx.lib.masked.TimeCtrl(self, -1, name="24hCtrl", fmt24hr=True)
		bSizer7.Add( self.timeEdit, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.timeSpinButton = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.timeSpinButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class icDateTimeCtrlProto
###########################################################################

class icDateTimeCtrlProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Дата" ), wx.HORIZONTAL )
		
		self.dateEdit = wx.DatePickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_ALLOWNONE|wx.DP_DEFAULT )
		sbSizer1.Add( self.dateEdit, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		
		bSizer7.Add( sbSizer1, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Время" ), wx.HORIZONTAL )
		
		self.h_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"00", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		sbSizer2.Add( self.h_textCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.h_spinBtn = wx.SpinButton( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.h_spinBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_staticText1 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u":", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		sbSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"00", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		sbSizer2.Add( self.m_textCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_spinBtn = wx.SpinButton( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.m_spinBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_staticText2 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u":", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		sbSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.s_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"00", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		sbSizer2.Add( self.s_textCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.s_spinBtn = wx.SpinButton( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		sbSizer2.Add( self.s_spinBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		
		bSizer7.Add( sbSizer2, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		bSizer7.Fit( self )
		
		# Connect Events
		self.h_textCtrl.Bind( wx.EVT_TEXT, self.onHText )
		self.h_spinBtn.Bind( wx.EVT_SPIN, self.onHSpin )
		self.m_textCtrl.Bind( wx.EVT_TEXT, self.onMText )
		self.m_spinBtn.Bind( wx.EVT_SPIN, self.onMSpin )
		self.s_textCtrl.Bind( wx.EVT_TEXT, self.onSText )
		self.s_spinBtn.Bind( wx.EVT_SPIN, self.onSSpin )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onHText( self, event ):
		event.Skip()
	
	def onHSpin( self, event ):
		event.Skip()
	
	def onMText( self, event ):
		event.Skip()
	
	def onMSpin( self, event ):
		event.Skip()
	
	def onSText( self, event ):
		event.Skip()
	
	def onSSpin( self, event ):
		event.Skip()
	

