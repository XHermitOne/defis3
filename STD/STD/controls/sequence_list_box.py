# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class icSequenceListBoxProto
###########################################################################

class icSequenceListBoxProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.first_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-goto-first", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.prev_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-go-back", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.move_up_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.move_down_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.next_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-go-forward", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.last_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-goto-last", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.ctrl_toolBar.Realize() 
		
		bSizer8.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		sequence_listBoxChoices = []
		self.sequence_listBox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, sequence_listBoxChoices, wx.LB_SINGLE )
		bSizer8.Add( self.sequence_listBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer8 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onFirstToolClicked, id = self.first_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onPrevToolClicked, id = self.prev_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onMoveUpToolClicked, id = self.move_up_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onMoveDownToolClicked, id = self.move_down_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onNextToolClicked, id = self.next_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onLastToolClicked, id = self.last_tool.GetId() )
		self.sequence_listBox.Bind( wx.EVT_LISTBOX, self.onSequenceSelectListBox )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onFirstToolClicked( self, event ):
		event.Skip()
	
	def onPrevToolClicked( self, event ):
		event.Skip()
	
	def onMoveUpToolClicked( self, event ):
		event.Skip()
	
	def onMoveDownToolClicked( self, event ):
		event.Skip()
	
	def onNextToolClicked( self, event ):
		event.Skip()
	
	def onLastToolClicked( self, event ):
		event.Skip()
	
	def onSequenceSelectListBox( self, event ):
		event.Skip()
	

