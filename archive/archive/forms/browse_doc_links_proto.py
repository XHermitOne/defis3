# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv

###########################################################################
## Class icBrowseDocLinksPanelProto
###########################################################################

class icBrowseDocLinksPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.view_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Просмотр", u"Просмотр", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.edit_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактирование", u"Редактирование", None ) 
		
		self.ctrl_toolBar.Realize() 
		
		bSizer1.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		self.links_treeListCtrl = wx.lib.gizmos.TreeListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		bSizer1.Add( self.links_treeListCtrl, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onViewToolClicked, id = self.view_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onViewToolClicked( self, event ):
		event.Skip()
	
	def onEditToolClicked( self, event ):
		event.Skip()
	

