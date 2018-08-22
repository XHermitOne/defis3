# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 16 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from NSI.usercomponents import spravtreecomboctrl
from NSI.usercomponents import spravchoicecomboctrl

###########################################################################
## Class icNewDocPanelProto
###########################################################################

class icNewDocPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 716,723 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.scan_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_CMN_DIALOG ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.scan_bpButton.SetToolTipString( u"Сканировать" )
		self.scan_bpButton.SetHelpText( u"Сканировать" )
		
		bSizer2.Add( self.scan_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Исходный документ:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.select_filePicker = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Выберите файл документа", u"Все|*.*|Файлы PDF|*.pdf|Файлы JPEG|*.jpg|Файлы TIFF|*.tiff|Файлы Microsoft Word|*.doc|Файлы LibreOffice Writer|*.odt", wx.DefaultPosition, wx.DefaultSize, wx.FLP_CHANGE_DIR|wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
		bSizer2.Add( self.select_filePicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Номер документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer3.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.ndoc_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.ndoc_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Дата документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer3.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.doc_datePicker = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
		bSizer3.Add( self.doc_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"№ документа контрагента:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		bSizer31.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.nobj_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.nobj_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"Дата документа контрагента:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		bSizer31.Add( self.m_staticText61, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.obj_datePicker = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
		bSizer31.Add( self.obj_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer31, 1, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Наименование:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer4.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.docname_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.docname_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Тип документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer5.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.doc_type_ctrl = spravtreecomboctrl.icSpravTreeComboCtrl(parent=self, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_doc_type', None, 'nsi_archive.mtd', 'ayan_archive'),),  'level_enable': 1})
		bSizer5.Add( self.doc_type_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"Подразделение:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		bSizer5.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entity_ctrl = spravtreecomboctrl.icSpravTreeComboCtrl(parent=self, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_entity', None, 'nsi_archive.mtd', 'ayan_archive'),), 'level_enable': 1})
		bSizer5.Add( self.entity_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Контрагент:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer6.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.contragent_ctrl = spravchoicecomboctrl.icSpravChoiceComboCtrl(parent=self, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_c_agent', None, 'nsi_archive.mtd', 'ayan_archive'),), 'view_fields': ['inn', 'kpp', 'full_name'], 'search_fields': ['inn', 'kpp', 'full_name']})
		bSizer6.Add( self.contragent_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Описание:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer7.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.description_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer7.Add( self.description_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Дополнительные комментарии:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer8.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		self.comment_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer8.Add( self.comment_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Теги" ), wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 2, 5, 0, 0 )
		
		self.tag0_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag0_textCtrl, 0, wx.ALL, 5 )
		
		self.tag1_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag1_textCtrl, 0, wx.ALL, 5 )
		
		self.tag2_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag2_textCtrl, 0, wx.ALL, 5 )
		
		self.tag3_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag3_textCtrl, 0, wx.ALL, 5 )
		
		self.tag4_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag4_textCtrl, 0, wx.ALL, 5 )
		
		self.tag5_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag5_textCtrl, 0, wx.ALL, 5 )
		
		self.tag6_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag6_textCtrl, 0, wx.ALL, 5 )
		
		self.tag7_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag7_textCtrl, 0, wx.ALL, 5 )
		
		self.tag8_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag8_textCtrl, 0, wx.ALL, 5 )
		
		self.tag9_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gSizer1.Add( self.tag9_textCtrl, 0, wx.ALL, 5 )
		
		
		sbSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( sbSizer1, 0, wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Связь с документами" ), wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.add_link_button = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Добавить", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.add_link_button, 0, wx.ALL, 5 )
		
		self.del_link_button = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Удалить", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.del_link_button, 0, wx.ALL, 5 )
		
		
		sbSizer2.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		self.link_listCtrl = wx.ListCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		sbSizer2.Add( self.link_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.reg_button = wx.Button( self, wx.ID_ANY, u"Зарегистрировать", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.reg_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer12, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.scan_bpButton.Bind( wx.EVT_BUTTON, self.onScanButtonClick )
		self.docname_textCtrl.Bind( wx.EVT_TEXT, self.onDocNameText )
		self.docname_textCtrl.Bind( wx.EVT_TEXT_ENTER, self.onDocNameTextEnter )
		self.tag0_textCtrl.Bind( wx.EVT_TEXT, self.onTag0Text )
		self.tag1_textCtrl.Bind( wx.EVT_TEXT, self.onTag1Text )
		self.tag2_textCtrl.Bind( wx.EVT_TEXT, self.onTag2Text )
		self.tag3_textCtrl.Bind( wx.EVT_TEXT, self.onTag3Text )
		self.tag4_textCtrl.Bind( wx.EVT_TEXT, self.onTag4Text )
		self.tag5_textCtrl.Bind( wx.EVT_TEXT, self.onTag5Text )
		self.tag6_textCtrl.Bind( wx.EVT_TEXT, self.onTag6Text )
		self.tag7_textCtrl.Bind( wx.EVT_TEXT, self.onTag7Text )
		self.tag8_textCtrl.Bind( wx.EVT_TEXT, self.onTag8Text )
		self.tag9_textCtrl.Bind( wx.EVT_TEXT, self.onTag9Text )
		self.add_link_button.Bind( wx.EVT_BUTTON, self.onAddLinkButtonClick )
		self.del_link_button.Bind( wx.EVT_BUTTON, self.onDelLinkButtonClick )
		self.reg_button.Bind( wx.EVT_BUTTON, self.onRegButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onScanButtonClick( self, event ):
		event.Skip()
	
	def onDocNameText( self, event ):
		event.Skip()
	
	def onDocNameTextEnter( self, event ):
		event.Skip()
	
	def onTag0Text( self, event ):
		event.Skip()
	
	def onTag1Text( self, event ):
		event.Skip()
	
	def onTag2Text( self, event ):
		event.Skip()
	
	def onTag3Text( self, event ):
		event.Skip()
	
	def onTag4Text( self, event ):
		event.Skip()
	
	def onTag5Text( self, event ):
		event.Skip()
	
	def onTag6Text( self, event ):
		event.Skip()
	
	def onTag7Text( self, event ):
		event.Skip()
	
	def onTag8Text( self, event ):
		event.Skip()
	
	def onTag9Text( self, event ):
		event.Skip()
	
	def onAddLinkButtonClick( self, event ):
		event.Skip()
	
	def onDelLinkButtonClick( self, event ):
		event.Skip()
	
	def onRegButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class icCorrectScanDocPanelProto
###########################################################################

class icCorrectScanDocPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.prev_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_BACK, wx.ART_CMN_DIALOG ), wx.NullBitmap, wx.ITEM_NORMAL, u"Предыдущий", u"Предыдущий", None ) 
		
		self.next_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_CMN_DIALOG ), wx.NullBitmap, wx.ITEM_NORMAL, u"Следующий", u"Следующий", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.view_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_CMN_DIALOG ), wx.NullBitmap, wx.ITEM_NORMAL, u"Просмотр", u"Просмотр", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.edit_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_CMN_DIALOG ), wx.NullBitmap, wx.ITEM_CHECK, u"Редактировать", u"Редактировать", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.save_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE, wx.ART_CMN_DIALOG ), wx.NullBitmap, wx.ITEM_NORMAL, u"Сохранить", u"Сохранить", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.card_spinCtrl = wx.SpinCtrl( self.ctrl_toolBar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,40 ), wx.SP_ARROW_KEYS, 0, 1000, 0 )
		self.card_spinCtrl.SetFont( wx.Font( 20, 74, 90, 92, False, "Sans" ) )
		
		self.ctrl_toolBar.AddControl( self.card_spinCtrl )
		self.idx_staticText = wx.StaticText( self.ctrl_toolBar, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.idx_staticText.Wrap( -1 )
		self.idx_staticText.SetFont( wx.Font( 24, 74, 90, 92, False, "Sans" ) )
		
		self.ctrl_toolBar.AddControl( self.idx_staticText )
		self.ctrl_toolBar.Realize() 
		
		bSizer11.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		self.doc_card_panel = icNewDocPanelProto(parent=self)
		bSizer11.Add( self.doc_card_panel, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer11 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onPrevToolClicked, id = self.prev_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onNextToolClicked, id = self.next_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onViewToolClicked, id = self.view_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSaveToolClicked, id = self.save_tool.GetId() )
		self.card_spinCtrl.Bind( wx.EVT_TEXT, self.onCardSpinCtrlText )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onPrevToolClicked( self, event ):
		event.Skip()
	
	def onNextToolClicked( self, event ):
		event.Skip()
	
	def onViewToolClicked( self, event ):
		event.Skip()
	
	def onEditToolClicked( self, event ):
		event.Skip()
	
	def onSaveToolClicked( self, event ):
		event.Skip()
	
	def onCardSpinCtrlText( self, event ):
		event.Skip()
	

###########################################################################
## Class icCorrectFilterDlgProto
###########################################################################

class icCorrectFilterDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Фильтр документов", pos = wx.DefaultPosition, size = wx.Size( 782,412 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Начальная дата создания документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		bSizer13.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.begin_datePicker = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
		bSizer13.Add( self.begin_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Конечная дата создания документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer13.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.end_datePicker = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.DP_DEFAULT )
		bSizer13.Add( self.end_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer12.Add( bSizer13, 0, wx.EXPAND, 5 )
		
		self.sql_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		bSizer12.Add( self.sql_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer15.Add( self.ok_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer12.Add( bSizer15, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer12 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.begin_datePicker.Bind( wx.EVT_DATE_CHANGED, self.onBeginDateChanged )
		self.end_datePicker.Bind( wx.EVT_DATE_CHANGED, self.onEndDateChanged )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onBeginDateChanged( self, event ):
		event.Skip()
	
	def onEndDateChanged( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

