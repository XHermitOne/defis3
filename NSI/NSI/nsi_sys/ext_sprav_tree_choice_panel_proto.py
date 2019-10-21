# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
from . import icspravtreecomboctrl

###########################################################################
## Class icExtSpravTreeChoicePanelProto
###########################################################################

class icExtSpravTreeChoicePanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,30 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.sprav_tree_choice =  icspravtreecomboctrl.icSpravTreeComboCtrlPrototype(parent=self)
		bSizer1.Add( self.sprav_tree_choice, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.clear_button = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-clear", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer1.Add( self.clear_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.find_button = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer1.Add( self.find_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.edit_button = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer1.Add( self.edit_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.help_button = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer1.Add( self.help_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.clear_button.Bind( wx.EVT_BUTTON, self.onClearButtonClick )
		self.find_button.Bind( wx.EVT_BUTTON, self.onFindButtonClick )
		self.edit_button.Bind( wx.EVT_BUTTON, self.onEditButtonClick )
		self.help_button.Bind( wx.EVT_BUTTON, self.onHelpButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onClearButtonClick( self, event ):
		event.Skip()
	
	def onFindButtonClick( self, event ):
		event.Skip()
	
	def onEditButtonClick( self, event ):
		event.Skip()
	
	def onHelpButtonClick( self, event ):
		event.Skip()
	

