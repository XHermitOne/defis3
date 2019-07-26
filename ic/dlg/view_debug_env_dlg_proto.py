# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.aui

###########################################################################
## Class icViewDebugEnvDialogProto
###########################################################################

class icViewDebugEnvDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Пространство имен", pos = wx.DefaultPosition, size = wx.Size( 889,557 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.view_auinotebook = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )
		self.local_page_panel = wx.Panel( self.view_auinotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.local_treeListCtrl = wx.dataview.TreeListCtrl( self.local_page_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.TL_DEFAULT_STYLE|wx.dataview.TL_SINGLE )
		self.local_treeListCtrl.AppendColumn( u"Наименование", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.local_treeListCtrl.AppendColumn( u"Значение", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.local_treeListCtrl.AppendColumn( u"Тип", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		
		bSizer2.Add( self.local_treeListCtrl, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.local_page_panel.SetSizer( bSizer2 )
		self.local_page_panel.Layout()
		bSizer2.Fit( self.local_page_panel )
		self.view_auinotebook.AddPage( self.local_page_panel, u"locals", True, wx.ArtProvider.GetBitmap( u"gtk-leave-fullscreen", wx.ART_FRAME_ICON ) )
		self.global_page_panel = wx.Panel( self.view_auinotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.global_treeListCtrl = wx.dataview.TreeListCtrl( self.global_page_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.TL_DEFAULT_STYLE|wx.dataview.TL_SINGLE )
		self.global_treeListCtrl.AppendColumn( u"Наименование", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.global_treeListCtrl.AppendColumn( u"Значение", wx.COL_WIDTH_AUTOSIZE, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		self.global_treeListCtrl.AppendColumn( u"Тип", wx.COL_WIDTH_DEFAULT, wx.ALIGN_LEFT, wx.COL_RESIZABLE )
		
		bSizer3.Add( self.global_treeListCtrl, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.global_page_panel.SetSizer( bSizer3 )
		self.global_page_panel.Layout()
		bSizer3.Fit( self.global_page_panel )
		self.view_auinotebook.AddPage( self.global_page_panel, u"globals", False, wx.ArtProvider.GetBitmap( u"gtk-fullscreen", wx.ART_FRAME_ICON ) )
		
		bSizer1.Add( self.view_auinotebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer4.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.local_treeListCtrl.Bind( wx.dataview.EVT_TREELIST_SELECTION_CHANGED, self.onLocalSelectionChange )
		self.global_treeListCtrl.Bind( wx.dataview.EVT_TREELIST_SELECTION_CHANGED, self.onGlobalSelectionChange )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onLocalSelectionChange( self, event ):
		event.Skip()
	
	def onGlobalSelectionChange( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

