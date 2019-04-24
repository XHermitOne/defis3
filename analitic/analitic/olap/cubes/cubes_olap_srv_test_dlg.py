# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.stc

###########################################################################
## Class icCubesOLAPSrvTestDialogProto
###########################################################################

class icCubesOLAPSrvTestDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"OLAP сервер", pos = wx.DefaultPosition, size = wx.Size( 870,631 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Куб:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		cube_choiceChoices = []
		self.cube_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cube_choiceChoices, 0 )
		self.cube_choice.SetSelection( 0 )
		bSizer2.Add( self.cube_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Функция:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		func_choiceChoices = []
		self.func_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, func_choiceChoices, 0 )
		self.func_choice.SetSelection( 0 )
		bSizer2.Add( self.func_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer2.AddStretchSpacer()
		
		self.refresh_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer2.Add( self.refresh_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		self.json_scintilla = wx.stc.StyledTextCtrl(parent=self, id=wx.NewId())
		bSizer1.Add( self.json_scintilla, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.close_button = wx.Button( self, wx.ID_ANY, u"Закрыть", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.close_button, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer3, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.refresh_bpButton.Bind( wx.EVT_BUTTON, self.onRefreshButtonClick )
		self.close_button.Bind( wx.EVT_BUTTON, self.onCloseButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onRefreshButtonClick( self, event ):
		event.Skip()
	
	def onCloseButtonClick( self, event ):
		event.Skip()
	

