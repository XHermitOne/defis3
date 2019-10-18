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
		
		self.choice1 = ic.metadata.THIS.frm.nsi_product_choice.create(parent=self)
		bSizer2.Add( self.choice1, 1, wx.ALL, 5 )
		
		self.choice2 = ic.metadata.THIS.frm.ref_product_choice.create(parent=self)
		bSizer2.Add( self.choice2, 1, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
	
	def __del__( self ):
		pass
	

