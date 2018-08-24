# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
from NSI.usercomponents import spravtreecomboctrl
from NSI.usercomponents import spravchoicecomboctrl
from ic.components.user import icchecklistctrl

###########################################################################
## Class icEditDocPanelProto
###########################################################################

class icEditDocPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1150,778 ), style = wx.TAB_TRAVERSAL )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.scan_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_MESSAGE_BOX ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer19.Add( self.scan_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Файл скана:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		bSizer19.Add( self.m_staticText18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.scan_filename_staticText = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.scan_filename_staticText.Wrap( -1 )
		self.scan_filename_staticText.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer19.Add( self.scan_filename_staticText, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"№ документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer3.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.ndoc_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.ndoc_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Дата док.:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer3.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.doc_datePicker = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		bSizer3.Add( self.doc_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"№ док. контрагента:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		bSizer3.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.nobj_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.nobj_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"Дата док. контрагента:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		bSizer3.Add( self.m_staticText61, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.obj_datePicker = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		bSizer3.Add( self.obj_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Наименование:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer4.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.docname_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.docname_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Тип документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer5.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.doc_type_ctrl = spravtreecomboctrl.icSpravTreeComboCtrl(parent=self, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_doc_type', None, 'nsi_archive.mtd', 'archive'),),  'level_enable': 1})
		bSizer5.Add( self.doc_type_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Контрагент:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer6.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.contragent_ctrl = spravchoicecomboctrl.icSpravChoiceComboCtrl(parent=self, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_c_agent', None, 'nsi_archive.mtd', 'archive'),), 'view_fields': ['inn', 'kpp', 'full_name'], 'search_fields': ['inn', 'kpp', 'full_name']})
		bSizer6.Add( self.contragent_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"Подразделение:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		bSizer51.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.entity_ctrl = spravtreecomboctrl.icSpravTreeComboCtrl(parent=self, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_entity', None, 'nsi_archive.mtd', 'archive'),),  'level_enable': 1})
		bSizer51.Add( self.entity_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer51, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Описание:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer7.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.description_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer7.Add( self.description_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Дополнительные комментарии:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer8.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		self.comment_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer8.Add( self.comment_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer8, 1, wx.EXPAND, 5 )
		
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
		
		
		bSizer11.Add( sbSizer1, 0, wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Связь с документами" ), wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.add_link_button = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Добавить", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.add_link_button, 0, wx.ALL, 5 )
		
		self.del_link_button = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Удалить", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.del_link_button, 0, wx.ALL, 5 )
		
		
		sbSizer2.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		self.link_listCtrl = wx.ListCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		sbSizer2.Add( self.link_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer11 )
		self.Layout()
		
		# Connect Events
		self.scan_bpButton.Bind( wx.EVT_BUTTON, self.onReScanButtonClick )
		self.docname_textCtrl.Bind( wx.EVT_TEXT, self.onDocNameText )
		self.docname_textCtrl.Bind( wx.EVT_TEXT_ENTER, self.onDocNameTextEnter )
		self.add_link_button.Bind( wx.EVT_BUTTON, self.onAddLinkButtonClick )
		self.del_link_button.Bind( wx.EVT_BUTTON, self.onDelLinkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onReScanButtonClick( self, event ):
		event.Skip()
	
	def onDocNameText( self, event ):
		event.Skip()
	
	def onDocNameTextEnter( self, event ):
		event.Skip()
	
	def onAddLinkButtonClick( self, event ):
		event.Skip()
	
	def onDelLinkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class icEditDocDlgProto
###########################################################################

class icEditDocDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Редактирование атрибутов документа", pos = wx.DefaultPosition, size = wx.Size( 988,830 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer25 = wx.BoxSizer( wx.VERTICAL )
		
		self.edit_doc_panel = icEditDocPanelProto(parent=self)
		bSizer25.Add( self.edit_doc_panel, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer24.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.save_button = wx.Button( self, wx.ID_ANY, u"Сохранить", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer24.Add( self.save_button, 0, wx.ALL, 5 )
		
		
		bSizer25.Add( bSizer24, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer25 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.save_button.Bind( wx.EVT_BUTTON, self.onSaveButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onSaveButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class icPackScanDocPanelProto
###########################################################################

class icPackScanDocPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1185,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.import_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Импортировать из ПО БАЛАНС+", u"Импортировать из ПО БАЛАНС+", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.group_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-indent", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Групповая обработка", u"Групповая обработка", None ) 
		
		self.toggle_checkBox = wx.CheckBox( self.ctrl_toolBar, wx.ID_ANY, u"Вкл./Выкл. все", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ctrl_toolBar.AddControl( self.toggle_checkBox )
		self.n_pages_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-dnd-multiple", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Количество страниц", u"Количество страниц", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.view_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Просмотр", u"Просмотр", None ) 
		
		self.edit_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактирование", u"Редактирование", None ) 
		
		self.quick_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_REPORT_VIEW, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_CHECK, u"Режим быстрого ввода", u"Режим быстрого ввода", None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.scan_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-preferences", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Сканирование", u"Сканирование", None ) 
		
		self.archive_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_TO_PARENT, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Переместить в архив", u"Переместить в архив", None ) 
		
		self.ctrl_toolBar.Realize() 
		
		bSizer12.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Тип документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer5.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.doc_type_ctrl = spravtreecomboctrl.icSpravTreeComboCtrl(parent=self, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_doc_type', None, 'nsi_archive.mtd', 'archive'),),  'level_enable': 1, 'on_change': 'self.GetParent().onChangeDocType(None)'})
		bSizer5.Add( self.doc_type_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.clear_doc_type_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-clear", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.clear_doc_type_bpButton, 0, wx.ALL, 5 )
		
		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Доп. признак:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		bSizer5.Add( self.m_staticText20, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		tag_choiceChoices = [ wx.EmptyString, u"ЕГАИС", u"Склад 1", u"Склад 2", u"Склад 3", u"Склад 5", u"Склад 6", u"Склад 8", u"Склад 10", u"Реализация", u"Склад 41", u"Склад 55", u"Склад 77", u"Склад 136", u"Склад 179", u"Склад 180", u"Материалы", u"Счет 76-01", u"Счет 76-06", u"Затраты на производство", u"Основные средства" ]
		self.tag_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, tag_choiceChoices, 0 )
		self.tag_choice.SetSelection( 0 )
		bSizer5.Add( self.tag_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		ext_tag_choiceChoices = [ wx.EmptyString, u"с НДС", u"без НДС" ]
		self.ext_tag_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ext_tag_choiceChoices, 0 )
		self.ext_tag_choice.SetSelection( 0 )
		bSizer5.Add( self.ext_tag_choice, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Контрагент:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer5.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.contragent_ctrl = spravchoicecomboctrl.icSpravChoiceComboCtrl(parent=self, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_c_agent', None, 'nsi_archive.mtd', 'archive'),), 'view_fields': ['inn', 'kpp', 'full_name'], 'search_fields': ['inn', 'kpp', 'full_name'], 'on_select': 'self.GetParent().onChangeContragent(None)'})
		bSizer5.Add( self.contragent_ctrl, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.clear_contragent_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-clear", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.clear_contragent_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"Диапазон дат:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )
		bSizer20.Add( self.m_staticText27, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.start_datePicker = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		bSizer20.Add( self.start_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		bSizer20.Add( self.m_staticText28, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.end_datePicker = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		bSizer20.Add( self.end_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		sort_radioBoxChoices = [ u"По номеру документа", u"По наименованию контрагента", u"По дате документа", u"По инвентарному номеру (ОС)" ]
		self.sort_radioBox = wx.RadioBox( self, wx.ID_ANY, u"Сортировка", wx.DefaultPosition, wx.DefaultSize, sort_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.sort_radioBox.SetSelection( 0 )
		bSizer20.Add( self.sort_radioBox, 0, wx.ALL, 5 )
		
		group_radioBoxChoices = [ u"Нет", u"По наименованию контрагента" ]
		self.group_radioBox = wx.RadioBox( self, wx.ID_ANY, u"Группировка", wx.DefaultPosition, wx.DefaultSize, group_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.group_radioBox.SetSelection( 0 )
		self.group_radioBox.Hide()
		
		bSizer20.Add( self.group_radioBox, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer20, 0, wx.EXPAND, 5 )
		
		self.docs_listCtrl = icchecklistctrl.icCheckListCtrl(parent=self, id=-1, component={'on_toggle_item': 'self.GetParent().onToggleDocItem(None)',
		'on_select_item': 'self.GetParent().onSelectDocItem(event)'})
		bSizer12.Add( self.docs_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Документов в обработке:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer14.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.doc_count_staticText = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.doc_count_staticText.Wrap( -1 )
		self.doc_count_staticText.SetFont( wx.Font( 16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer14.Add( self.doc_count_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer14.AddSpacer( 5 )
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Сканируемых листов:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		bSizer14.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.page_count_staticText = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.page_count_staticText.Wrap( -1 )
		self.page_count_staticText.SetFont( wx.Font( 18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer14.Add( self.page_count_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer14.AddSpacer( 5 )
		
		
		bSizer12.Add( bSizer14, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer12 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onImportToolClicked, id = self.import_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onGroupToolClicked, id = self.group_tool.GetId() )
		self.toggle_checkBox.Bind( wx.EVT_CHECKBOX, self.onToggleCheckBox )
		self.Bind( wx.EVT_TOOL, self.onNPagesToolClicked, id = self.n_pages_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onViewToolClicked, id = self.view_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onQuickToolClicked, id = self.quick_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onScanToolClicked, id = self.scan_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onArchiveToolClicked, id = self.archive_tool.GetId() )
		self.clear_doc_type_bpButton.Bind( wx.EVT_BUTTON, self.onClearDocTypeButtonClick )
		self.tag_choice.Bind( wx.EVT_CHOICE, self.onTagChoice )
		self.ext_tag_choice.Bind( wx.EVT_CHOICE, self.onTagChoice )
		self.clear_contragent_bpButton.Bind( wx.EVT_BUTTON, self.onClearContragentButtonClick )
		self.start_datePicker.Bind( wx.adv.EVT_DATE_CHANGED, self.onStartDateChanged )
		self.end_datePicker.Bind( wx.adv.EVT_DATE_CHANGED, self.onEndDateChanged )
		self.sort_radioBox.Bind( wx.EVT_RADIOBOX, self.onSortRadioBox )
		self.group_radioBox.Bind( wx.EVT_RADIOBOX, self.onGroupRadioBox )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onImportToolClicked( self, event ):
		event.Skip()
	
	def onGroupToolClicked( self, event ):
		event.Skip()
	
	def onToggleCheckBox( self, event ):
		event.Skip()
	
	def onNPagesToolClicked( self, event ):
		event.Skip()
	
	def onViewToolClicked( self, event ):
		event.Skip()
	
	def onEditToolClicked( self, event ):
		event.Skip()
	
	def onQuickToolClicked( self, event ):
		event.Skip()
	
	def onScanToolClicked( self, event ):
		event.Skip()
	
	def onArchiveToolClicked( self, event ):
		event.Skip()
	
	def onClearDocTypeButtonClick( self, event ):
		event.Skip()
	
	def onTagChoice( self, event ):
		event.Skip()
	
	
	def onClearContragentButtonClick( self, event ):
		event.Skip()
	
	def onStartDateChanged( self, event ):
		event.Skip()
	
	def onEndDateChanged( self, event ):
		event.Skip()
	
	def onSortRadioBox( self, event ):
		event.Skip()
	
	def onGroupRadioBox( self, event ):
		event.Skip()
	

###########################################################################
## Class icQuickEntryPackScanPanelProto
###########################################################################

class icQuickEntryPackScanPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.TAB_TRAVERSAL )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.docname_staticText = wx.StaticText( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.docname_staticText.Wrap( -1 )
		self.docname_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )
		
		bSizer19.Add( self.docname_staticText, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.ndoc_staticText = wx.StaticText( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.ndoc_staticText.Wrap( -1 )
		self.ndoc_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		self.ndoc_staticText.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer19.Add( self.ndoc_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer15.Add( bSizer19, 0, wx.EXPAND, 5 )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"от", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		self.m_staticText23.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )
		
		bSizer22.Add( self.m_staticText23, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.docdate_staticText = wx.StaticText( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.docdate_staticText.Wrap( -1 )
		self.docdate_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		self.docdate_staticText.SetMinSize( wx.Size( 150,-1 ) )
		
		bSizer22.Add( self.docdate_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer15.Add( bSizer22, 0, wx.ALIGN_RIGHT, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cagent_ndoc_staticText = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.cagent_ndoc_staticText.Wrap( -1 )
		self.cagent_ndoc_staticText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )
		self.cagent_ndoc_staticText.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer21.Add( self.cagent_ndoc_staticText, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cagent_docdate_staticText = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cagent_docdate_staticText.Wrap( -1 )
		self.cagent_docdate_staticText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, "Sans" ) )
		self.cagent_docdate_staticText.SetMinSize( wx.Size( 150,-1 ) )
		
		bSizer21.Add( self.cagent_docdate_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer15.Add( bSizer21, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Количество листов:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		bSizer17.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.npages_spinCtrl = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 500, 1 )
		bSizer17.Add( self.npages_spinCtrl, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( bSizer17, 0, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.duplex_checkBox = wx.CheckBox( self, wx.ID_ANY, u"2-стороннее сканирование / Дуплекс", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.duplex_checkBox, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer15 )
		self.Layout()
	
	def __del__( self ):
		pass
	

