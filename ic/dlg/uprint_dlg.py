# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.combo

###########################################################################
## Class icUPrintDlgProto
###########################################################################

class icUPrintDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Печать", pos = wx.DefaultPosition, size = wx.Size( 633,401 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.option_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		option_notebookImageSize = wx.Size( 16,16 )
		option_notebookIndex = 0
		option_notebookImages = wx.ImageList( option_notebookImageSize.GetWidth(), option_notebookImageSize.GetHeight() )
		self.option_notebook.AssignImageList( option_notebookImages )
		self.option_panel = wx.Panel( self.option_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.option_panel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText8 = wx.StaticText( self.option_panel, wx.ID_ANY, u"Принтер:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer9.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.printer_comboBox = wx.combo.BitmapComboBox( self.option_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, "", wx.CB_READONLY ) 
		self.printer_comboBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer9.Add( self.printer_comboBox, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.option_panel, wx.ID_ANY, u"Бумага:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer5.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.paper_comboBox = wx.combo.BitmapComboBox( self.option_panel, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, "", wx.CB_READONLY ) 
		self.paper_comboBox.SetSelection( 0 )
		self.paper_comboBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer5.Add( self.paper_comboBox, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.Add( bSizer5, 0, wx.EXPAND|wx.ALL, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText6 = wx.StaticText( self.option_panel, wx.ID_ANY, u"Диапазон:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pages_textCtrl = wx.TextCtrl( self.option_panel, wx.ID_ANY, u"1-9999", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pages_textCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.pages_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText7 = wx.StaticText( self.option_panel, wx.ID_ANY, u"Копий:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.copies_spinCtrl = wx.SpinCtrl( self.option_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10, 1 )
		self.copies_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.copies_spinCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		page_radioBoxChoices = [ u"Все", u"Нечетные", u"Четные" ]
		self.page_radioBox = wx.RadioBox( self.option_panel, wx.ID_ANY, u"Страницы", wx.DefaultPosition, wx.DefaultSize, page_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.page_radioBox.SetSelection( 0 )
		self.page_radioBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer8.Add( self.page_radioBox, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer8, 0, wx.EXPAND, 5 )
		
		
		self.option_panel.SetSizer( bSizer4 )
		self.option_panel.Layout()
		bSizer4.Fit( self.option_panel )
		self.option_notebook.AddPage( self.option_panel, u"Параметры печати", True )
		self.border_panel = wx.Panel( self.option_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmap1 = wx.StaticBitmap( self.border_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_CMN_DIALOG ), wx.DefaultPosition, wx.Size( 128,128 ), 0 )
		gbSizer1.Add( self.m_bitmap1, wx.GBPosition( 2, 2 ), wx.GBSpan( 2, 2 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.left_spinCtrl = wx.SpinCtrl( self.border_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0 )
		self.left_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.left_spinCtrl, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.left_text = wx.StaticText( self.border_panel, wx.ID_ANY, u"Слева (мм):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.left_text.Wrap( -1 )
		self.left_text.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.left_text, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		self.right_text = wx.StaticText( self.border_panel, wx.ID_ANY, u"Справа (мм):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.right_text.Wrap( -1 )
		self.right_text.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.right_text, wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		self.right_spinCtrl = wx.SpinCtrl( self.border_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0 )
		self.right_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.right_spinCtrl, wx.GBPosition( 3, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.top_text = wx.StaticText( self.border_panel, wx.ID_ANY, u"Сверху (мм):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.top_text.Wrap( -1 )
		self.top_text.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.top_text, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.top_spinCtrl = wx.SpinCtrl( self.border_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.top_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.top_spinCtrl, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.border_panel, wx.ID_ANY, u"Снизу (мм):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.m_staticText5, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.bottom_spinCtrl = wx.SpinCtrl( self.border_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.bottom_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.bottom_spinCtrl, wx.GBPosition( 4, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		self.border_panel.SetSizer( gbSizer1 )
		self.border_panel.Layout()
		gbSizer1.Fit( self.border_panel )
		self.option_notebook.AddPage( self.border_panel, u"Поля", False )
		
		bSizer1.Add( self.option_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cancel_button.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer2.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.preview_button = wx.Button( self, wx.ID_ANY, u"Предварительный просмотр ...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.preview_button.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer2.Add( self.preview_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"Печать", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer2.Add( self.ok_button, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCanceButtonClick )
		self.preview_button.Bind( wx.EVT_BUTTON, self.onPreviewButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOKButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCanceButtonClick( self, event ):
		pass
	
	def onPreviewButtonClick( self, event ):
		pass
	
	def onOKButtonClick( self, event ):
		pass
	

