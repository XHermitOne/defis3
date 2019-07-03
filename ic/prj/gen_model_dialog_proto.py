# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class icGenModelDialogProto
###########################################################################

class icGenModelDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Генерация модулей", pos = wx.DefaultPosition, size = wx.Size( 569,226 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Сгенерировать:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Директория модулей:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer7.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.dst_dirPicker = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer7.Add( self.dst_dirPicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_REPORT_VIEW, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.model_button = wx.Button( self, wx.ID_ANY, u"Модуль модели", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.model_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap2 = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_bitmap2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.manager_button = wx.Button( self, wx.ID_ANY, u"Модуль менеджера модели", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.manager_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.close_button = wx.Button( self, wx.ID_ANY, u"Закрыть", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.close_button.SetDefault() 
		bSizer8.Add( self.close_button, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer1.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.dst_dirPicker.Bind( wx.EVT_DIRPICKER_CHANGED, self.onDstDirChanged )
		self.model_button.Bind( wx.EVT_BUTTON, self.onModelButtonClick )
		self.manager_button.Bind( wx.EVT_BUTTON, self.onManagerButtonClick )
		self.close_button.Bind( wx.EVT_BUTTON, self.onCloseButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onDstDirChanged( self, event ):
		event.Skip()
	
	def onModelButtonClick( self, event ):
		event.Skip()
	
	def onManagerButtonClick( self, event ):
		event.Skip()
	
	def onCloseButtonClick( self, event ):
		event.Skip()
	

