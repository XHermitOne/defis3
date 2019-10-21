# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import ic

###########################################################################
## Class icTestNSICtrlPanelProto
###########################################################################

class icTestNSICtrlPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"SpravMultipleChoiceComboCtrl:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice1 = ic.metadata.NSI.frm.nsi_product_choice.create(parent=self)
		bSizer2.Add( self.choice1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice2 = ic.metadata.NSI.frm.ref_product_choice.create(parent=self)
		bSizer2.Add( self.choice2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"SpravTreeComboCtrl:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer21.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice11 = ic.metadata.NSI.frm.nsi_spravtreecomboctrl.create(parent=self)
		bSizer21.Add( self.choice11, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice21 = ic.metadata.NSI.frm.ref_spravtreecomboctrl.create(parent=self)
		bSizer21.Add( self.choice21, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer21, 0, wx.EXPAND, 5 )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"SpravSingleLevelChoiceCtrl:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer22.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.choice12 = ic.metadata.NSI.frm.nsi_spravsinglelevelchoicectrl.create(parent=self)
		bSizer22.Add( self.choice12, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.choice22 = ic.metadata.NSI.frm.ref_spravsinglelevelchoicectrl.create(parent=self)
		bSizer22.Add( self.choice22, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer22, 1, wx.EXPAND, 5 )
		
		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"ExtSpravTreeChoice:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		bSizer23.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice13 = ic.metadata.NSI.frm.nsi_extspravtreechoice.create(parent=self)
		bSizer23.Add( self.choice13, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice23 = ic.metadata.NSI.frm.ref_extspravtreechoice.create(parent=self)
		bSizer23.Add( self.choice23, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer23, 0, wx.EXPAND, 5 )
		
		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"SpravLevelChoiceCtrl:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		bSizer24.Add( self.m_staticText14, 0, wx.ALL, 5 )
		
		self.choice14 = ic.metadata.NSI.frm.nsi_spravlevelchoicectrl.create(parent=self)
		bSizer24.Add( self.choice14, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.choice24 = ic.metadata.NSI.frm.ref_spravlevelchoicectrl.create(parent=self)
		bSizer24.Add( self.choice24, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer24, 1, wx.EXPAND, 5 )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"SpravChoiceComboCtrl:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		bSizer25.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice15 = ic.metadata.NSI.frm.nsi_spravchoicecomboctrl.create(parent=self)
		bSizer25.Add( self.choice15, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.choice25 = ic.metadata.NSI.frm.ref_spravchoicecomboctrl.create(parent=self)
		bSizer25.Add( self.choice25, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer25, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
	
	def __del__( self ):
		pass
	

