# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from STD.usercomponents import metatreelistctrl

###########################################################################
## Class icStdMetaTreeBrowserPanelProto
###########################################################################

class icStdMetaTreeBrowserPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.browser_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.browser_splitter.Bind( wx.EVT_IDLE, self.browser_splitterOnIdle )
		
		self.metatree_panel = wx.Panel( self.browser_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.metatree_list_ctrl = metatreelistctrl.icMetaTreeListCtrl(id=wx.NewId, component={})
		bSizer2.Add( self.metatree_list_ctrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.metatree_panel.SetSizer( bSizer2 )
		self.metatree_panel.Layout()
		bSizer2.Fit( self.metatree_panel )
		self.metaitem_panel = wx.Panel( self.browser_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.metaitem_panel.SetSizer( bSizer3 )
		self.metaitem_panel.Layout()
		bSizer3.Fit( self.metaitem_panel )
		self.browser_splitter.SplitHorizontally( self.metatree_panel, self.metaitem_panel, 0 )
		bSizer1.Add( self.browser_splitter, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
	
	def __del__( self ):
		pass
	
	def browser_splitterOnIdle( self, event ):
		self.browser_splitter.SetSashPosition( 0 )
		self.browser_splitter.Unbind( wx.EVT_IDLE )
	

