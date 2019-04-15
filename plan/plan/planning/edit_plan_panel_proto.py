# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from STD.usercomponents import icstdmetatreebrowser

###########################################################################
## Class icEditPlanPanelProto
###########################################################################

class icEditPlanPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.collapse_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Свернуть дерево плана", u"Свернуть дерево плана", None ) 
		
		self.expand_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Открыть дерево плана", u"Открыть дерево плана", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.ctrl_toolBar.Realize() 
		
		bSizer1.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		self.plan_browser = icstdmetatreebrowser.icStdMetaTreeBrowser(id=wx.NewId(), parent=self, component={})
		bSizer1.Add( self.plan_browser, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked( self, event ):
		event.Skip()
	
	def onExpandToolClicked( self, event ):
		event.Skip()
	

