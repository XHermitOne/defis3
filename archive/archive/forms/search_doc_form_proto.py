# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv
from NSI.usercomponents import spravtreecomboctrl
from NSI.usercomponents import spravmultiplechoicecomboctrl
from ic.components.user import icchecklistctrl

###########################################################################
## Class icSearchCritPanelProto
###########################################################################

class icSearchCritPanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.crit_scrolledWindow = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.crit_scrolledWindow.SetScrollRate( 5, 5 )
		bSizer23 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText8 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"№ документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer2.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.docnum_textCtrl = wx.TextCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.docnum_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		docnum_radioBoxChoices = [ u"По вхождению", u"Точное совпадение" ]
		self.docnum_radioBox = wx.RadioBox( self.crit_scrolledWindow, wx.ID_ANY, u"Искать:", wx.DefaultPosition, wx.DefaultSize, docnum_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.docnum_radioBox.SetSelection( 0 )
		bSizer2.Add( self.docnum_radioBox, 0, wx.ALL, 5 )


		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText13 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"№ документа контрагента:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		bSizer2.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.nobj_textCtrl = wx.TextCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.nobj_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		nobj_radioBoxChoices = [ u"По вхождению", u"Точное совпадение" ]
		self.nobj_radioBox = wx.RadioBox( self.crit_scrolledWindow, wx.ID_ANY, u"Искать:", wx.DefaultPosition, wx.DefaultSize, nobj_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.nobj_radioBox.SetSelection( 0 )
		bSizer2.Add( self.nobj_radioBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer23.Add( bSizer2, 0, wx.EXPAND, 2 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.date_checkBox = wx.CheckBox( self.crit_scrolledWindow, wx.ID_ANY, u"Дата документа", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.date_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText10 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"с:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer22.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.start_datePicker = wx.adv.DatePickerCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		self.start_datePicker.Enable( False )

		bSizer22.Add( self.start_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText9 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"по:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer22.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.end_datePicker = wx.adv.DatePickerCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		self.end_datePicker.Enable( False )

		bSizer22.Add( self.end_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.one_date_checkBox = wx.CheckBox( self.crit_scrolledWindow, wx.ID_ANY, u"На определенноую дату", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.one_date_checkBox.Enable( False )

		bSizer22.Add( self.one_date_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer22.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.obj_date_checkBox = wx.CheckBox( self.crit_scrolledWindow, wx.ID_ANY, u"Дата док. контрагента", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.obj_date_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText101 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"с:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText101.Wrap( -1 )

		bSizer22.Add( self.m_staticText101, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.obj_start_datePicker = wx.adv.DatePickerCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		self.obj_start_datePicker.Enable( False )

		bSizer22.Add( self.obj_start_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText91 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"по:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )

		bSizer22.Add( self.m_staticText91, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.obj_end_datePicker = wx.adv.DatePickerCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		self.obj_end_datePicker.Enable( False )

		bSizer22.Add( self.obj_end_datePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.obj_one_date_checkBox = wx.CheckBox( self.crit_scrolledWindow, wx.ID_ANY, u"На определенноую дату", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.obj_one_date_checkBox.Enable( False )

		bSizer22.Add( self.obj_one_date_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer23.Add( bSizer22, 0, wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"Наименование:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer3.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.docname_textCtrl = wx.TextCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.docname_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer23.Add( bSizer3, 0, wx.EXPAND, 2 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.doc_type_checkBox = wx.CheckBox( self.crit_scrolledWindow, wx.ID_ANY, u"Тип документа:", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.doc_type_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.doc_type_ctrl = spravtreecomboctrl.icSpravTreeComboCtrl(parent=self.crit_scrolledWindow, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_doc_type', None, 'nsi_archive.mtd', 'archive'),),  'level_enable': 1, 'on_change': 'self.findGrandParent(\'icPrintDocPanel\', is_subclass=False).onDocTypeChange(event)'})
		self.doc_type_ctrl.Enable( False )

		bSizer4.Add( self.doc_type_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.entity_checkBox = wx.CheckBox( self.crit_scrolledWindow, wx.ID_ANY, u"Подразделение:", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.entity_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.entity_ctrl = spravtreecomboctrl.icSpravTreeComboCtrl(parent=self.crit_scrolledWindow, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_entity', None, 'nsi_archive.mtd', 'archive'),),  'level_enable': 1})
		self.entity_ctrl.Enable( False )

		bSizer4.Add( self.entity_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer23.Add( bSizer4, 0, wx.EXPAND, 2 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.contragent_checkBox = wx.CheckBox( self.crit_scrolledWindow, wx.ID_ANY, u"Контрагенты:", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.contragent_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.contragent_ctrl = spravmultiplechoicecomboctrl.icSpravMultipleChoiceComboCtrl(parent=self.crit_scrolledWindow, id=wx.NewId(), component={'sprav': (('Sprav', 'nsi_c_agent', None, 'nsi_archive.mtd', 'archive'),), 'view_fields': ['inn', 'kpp', 'full_name'], 'search_fields': ['inn', 'kpp', 'full_name']})
		self.contragent_ctrl.Enable( False )

		bSizer5.Add( self.contragent_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer23.Add( bSizer5, 0, wx.EXPAND, 2 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"Описание:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer6.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.description_textCtrl = wx.TextCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.description_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer23.Add( bSizer6, 0, wx.EXPAND, 2 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.crit_scrolledWindow, wx.ID_ANY, u"Дополнительные комментарии:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer7.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.comment_textCtrl = wx.TextCtrl( self.crit_scrolledWindow, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.comment_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer23.Add( bSizer7, 0, wx.EXPAND, 2 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.crit_scrolledWindow, wx.ID_ANY, u"Теги:" ), wx.VERTICAL )

		gSizer1 = wx.GridSizer( 2, 5, 0, 0 )

		self.tag0_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag0_textCtrl, 0, wx.ALL, 5 )

		self.tag1_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag1_textCtrl, 0, wx.ALL, 5 )

		self.tag2_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag2_textCtrl, 0, wx.ALL, 5 )

		self.tag3_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag3_textCtrl, 0, wx.ALL, 5 )

		self.tag4_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag4_textCtrl, 0, wx.ALL, 5 )

		self.tag5_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag5_textCtrl, 0, wx.ALL, 5 )

		self.tag6_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag6_textCtrl, 0, wx.ALL, 5 )

		self.tag7_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag7_textCtrl, 0, wx.ALL, 5 )

		self.tag8_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag8_textCtrl, 0, wx.ALL, 5 )

		self.tag9_textCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.tag9_textCtrl, 0, wx.ALL, 5 )


		sbSizer2.Add( gSizer1, 1, wx.EXPAND, 5 )


		bSizer10.Add( sbSizer2, 1, wx.EXPAND, 5 )

		tag_radioBoxChoices = [ u"И", u"ИЛИ" ]
		self.tag_radioBox = wx.RadioBox( self.crit_scrolledWindow, wx.ID_ANY, u"Искать:", wx.DefaultPosition, wx.DefaultSize, tag_radioBoxChoices, 1, wx.RA_SPECIFY_COLS )
		self.tag_radioBox.SetSelection( 0 )
		bSizer10.Add( self.tag_radioBox, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer23.Add( bSizer10, 1, wx.EXPAND, 2 )


		self.crit_scrolledWindow.SetSizer( bSizer23 )
		self.crit_scrolledWindow.Layout()
		bSizer23.Fit( self.crit_scrolledWindow )
		bSizer1.Add( self.crit_scrolledWindow, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Сортировка результатов:" ), wx.HORIZONTAL )

		orderby_choiceChoices = [ wx.EmptyString, u"По номеру документа", u"По наименованию документа", u"По дате документа" ]
		self.orderby_choice = wx.Choice( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, orderby_choiceChoices, 0 )
		self.orderby_choice.SetSelection( 0 )
		sbSizer3.Add( self.orderby_choice, 1, wx.ALL, 5 )

		self.orderby_checkBox = wx.CheckBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"По убыванию", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer3.Add( self.orderby_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer9.Add( sbSizer3, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer9, 0, wx.EXPAND, 2 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.clear_button = wx.Button( self, wx.ID_ANY, u"Очистить", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.clear_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer11.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.search_button = wx.Button( self, wx.ID_ANY, u"Искать", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.search_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer11, 0, wx.ALIGN_RIGHT|wx.EXPAND, 2 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		# Connect Events
		self.date_checkBox.Bind( wx.EVT_CHECKBOX, self.onDateCheckBox )
		self.start_datePicker.Bind( wx.adv.EVT_DATE_CHANGED, self.onStartDatePickerChanged )
		self.end_datePicker.Bind( wx.adv.EVT_DATE_CHANGED, self.onEndDatePickerChanged )
		self.one_date_checkBox.Bind( wx.EVT_CHECKBOX, self.onOneDateCheckBox )
		self.obj_date_checkBox.Bind( wx.EVT_CHECKBOX, self.onObjDateCheckBox )
		self.obj_start_datePicker.Bind( wx.adv.EVT_DATE_CHANGED, self.onObjStartDatePickerChanged )
		self.obj_end_datePicker.Bind( wx.adv.EVT_DATE_CHANGED, self.onObjEndDatePickerChanged )
		self.obj_one_date_checkBox.Bind( wx.EVT_CHECKBOX, self.onObjOneDateCheckBox )
		self.doc_type_checkBox.Bind( wx.EVT_CHECKBOX, self.onDocTypeCheckBox )
		self.entity_checkBox.Bind( wx.EVT_CHECKBOX, self.onEntityCheckBox )
		self.contragent_checkBox.Bind( wx.EVT_CHECKBOX, self.onContragentCheckBox )
		self.clear_button.Bind( wx.EVT_BUTTON, self.onClearButtonClick )
		self.search_button.Bind( wx.EVT_BUTTON, self.onSearchButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onDateCheckBox( self, event ):
		event.Skip()

	def onStartDatePickerChanged( self, event ):
		event.Skip()

	def onEndDatePickerChanged( self, event ):
		event.Skip()

	def onOneDateCheckBox( self, event ):
		event.Skip()

	def onObjDateCheckBox( self, event ):
		event.Skip()

	def onObjStartDatePickerChanged( self, event ):
		event.Skip()

	def onObjEndDatePickerChanged( self, event ):
		event.Skip()

	def onObjOneDateCheckBox( self, event ):
		event.Skip()

	def onDocTypeCheckBox( self, event ):
		event.Skip()

	def onEntityCheckBox( self, event ):
		event.Skip()

	def onContragentCheckBox( self, event ):
		event.Skip()

	def onClearButtonClick( self, event ):
		event.Skip()

	def onSearchButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class icSearchDocPanelProto
###########################################################################

class icSearchDocPanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )

		self.search_panel1 = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer141 = wx.BoxSizer( wx.VERTICAL )

		self.search_crit_panel = icSearchCritPanelProto(self.search_panel)
		bSizer141.Add( self.search_crit_panel1, 1, wx.ALL|wx.EXPAND, 5 )


		self.search_panel1.SetSizer( bSizer141 )
		self.search_panel1.Layout()
		bSizer141.Fit( self.search_panel1 )
		self.docs_panel1 = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer151 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar1 = wx.ToolBar( self.docs_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.collapse_tool1 = self.ctrl_toolBar1.AddLabelTool( wx.ID_ANY, u"Свернуть", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Свернуть", u"Свернуть", None )

		self.expand_tool1 = self.ctrl_toolBar1.AddLabelTool( wx.ID_ANY, u"Развернуть", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Развернуть", u"Развернуть", None )

		self.ctrl_toolBar1.AddSeparator()

		self.view_tool1 = self.ctrl_toolBar1.AddLabelTool( wx.ID_ANY, u"Просмотр", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Просмотр", u"Просмотр", None )

		self.edit_tool1 = self.ctrl_toolBar1.AddLabelTool( wx.ID_ANY, u"Редактирование", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактирование", u"Редактирование", None )

		self.ctrl_toolBar1.AddSeparator()

		self.scheme_tool1 = self.ctrl_toolBar1.AddLabelTool( wx.ID_ANY, u"Схема связей", wx.ArtProvider.GetBitmap( u"gtk-dnd-multiple", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Схема связей", u"Схема связей", None )

		self.links_tool = self.ctrl_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-unindent", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Связи документа", u"Связи документа", None )

		self.ctrl_toolBar1.Realize()

		bSizer151.Add( self.ctrl_toolBar1, 0, wx.EXPAND, 5 )

		self.docs_listCtrl1 = wx.ListCtrl( self.docs_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer151.Add( self.docs_listCtrl1, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.docs_panel1, wx.ID_ANY, u"Найдено документов:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer30.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.search_count_staticText = wx.StaticText( self.docs_panel1, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.search_count_staticText.Wrap( -1 )

		self.search_count_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer30.Add( self.search_count_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer151.Add( bSizer30, 0, wx.EXPAND, 5 )


		self.docs_panel1.SetSizer( bSizer151 )
		self.docs_panel1.Layout()
		bSizer151.Fit( self.docs_panel1 )
		self.panel_splitter.SplitHorizontally( self.search_panel1, self.docs_panel1, 500 )
		bSizer13.Add( self.panel_splitter, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer13 )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool1.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool1.GetId() )
		self.Bind( wx.EVT_TOOL, self.onViewToolClicked, id = self.view_tool1.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool1.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSchemeToolClicked, id = self.scheme_tool1.GetId() )
		self.Bind( wx.EVT_TOOL, self.onLinksToolClicked, id = self.links_tool.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked( self, event ):
		event.Skip()

	def onExpandToolClicked( self, event ):
		event.Skip()

	def onViewToolClicked( self, event ):
		event.Skip()

	def onEditToolClicked( self, event ):
		event.Skip()

	def onSchemeToolClicked( self, event ):
		event.Skip()

	def onLinksToolClicked( self, event ):
		event.Skip()

	def panel_splitterOnIdle( self, event ):
		self.panel_splitter.SetSashPosition( 500 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )


###########################################################################
## Class icSearchDocDlgProto
###########################################################################

class icSearchDocDlgProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Поиск и выбор документа", pos = wx.DefaultPosition, size = wx.Size( 967,814 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )

		self.search_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.search_crit_panel = icSearchCritPanelProto(self.search_panel)
		bSizer14.Add( self.search_crit_panel, 1, wx.ALL|wx.EXPAND, 5 )


		self.search_panel.SetSizer( bSizer14 )
		self.search_panel.Layout()
		bSizer14.Fit( self.search_panel )
		self.docs_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self.docs_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.collapse_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Свернуть", u"Свернуть", None )

		self.expand_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Развернуть", u"Развернуть", None )

		self.ctrl_toolBar.Realize()

		bSizer15.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.docs_listCtrl = wx.ListCtrl( self.docs_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer15.Add( self.docs_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )


		self.docs_panel.SetSizer( bSizer15 )
		self.docs_panel.Layout()
		bSizer15.Fit( self.docs_panel )
		self.panel_splitter.SplitHorizontally( self.search_panel, self.docs_panel, 500 )
		bSizer16.Add( self.panel_splitter, 1, wx.EXPAND, 5 )

		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.cancel_button, 0, wx.ALL, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.ok_button, 0, wx.ALL, 5 )


		bSizer16.Add( bSizer17, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool.GetId() )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked( self, event ):
		event.Skip()

	def onExpandToolClicked( self, event ):
		event.Skip()

	def onCancelButtonClick( self, event ):
		event.Skip()

	def onOkButtonClick( self, event ):
		event.Skip()

	def panel_splitterOnIdle( self, event ):
		self.panel_splitter.SetSashPosition( 500 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )


###########################################################################
## Class icChoiceDocsDlgProto
###########################################################################

class icChoiceDocsDlgProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Поиск и выбор документов", pos = wx.DefaultPosition, size = wx.Size( 1328,814 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )

		self.search_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.search_crit_panel = icSearchCritPanelProto(self.search_panel)
		bSizer14.Add( self.search_crit_panel, 1, wx.ALL|wx.EXPAND, 5 )


		self.search_panel.SetSizer( bSizer14 )
		self.search_panel.Layout()
		bSizer14.Fit( self.search_panel )
		self.docs_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self.docs_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.collapse_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Свернуть", u"Свернуть", None )

		self.expand_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Развернуть", u"Развернуть", None )

		self.ctrl_toolBar.AddSeparator()

		self.all_checkBox = wx.CheckBox( self.ctrl_toolBar, wx.ID_ANY, u"Выделить все", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ctrl_toolBar.AddControl( self.all_checkBox )
		self.ctrl_toolBar.Realize()

		bSizer15.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.docs_listCtrl = icchecklistctrl.icCheckListCtrl(parent=self.docs_panel, id=-1, component={})
		bSizer15.Add( self.docs_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )


		self.docs_panel.SetSizer( bSizer15 )
		self.docs_panel.Layout()
		bSizer15.Fit( self.docs_panel )
		self.panel_splitter.SplitHorizontally( self.search_panel, self.docs_panel, 500 )
		bSizer16.Add( self.panel_splitter, 1, wx.EXPAND, 5 )

		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.cancel_button, 0, wx.ALL, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.ok_button, 0, wx.ALL, 5 )


		bSizer16.Add( bSizer17, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool.GetId() )
		self.all_checkBox.Bind( wx.EVT_CHECKBOX, self.onAllCheckBox )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked( self, event ):
		event.Skip()

	def onExpandToolClicked( self, event ):
		event.Skip()

	def onAllCheckBox( self, event ):
		event.Skip()

	def onCancelButtonClick( self, event ):
		event.Skip()

	def onOkButtonClick( self, event ):
		event.Skip()

	def panel_splitterOnIdle( self, event ):
		self.panel_splitter.SetSashPosition( 500 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )


###########################################################################
## Class icPrintDocPanelProto
###########################################################################

class icPrintDocPanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.SetSashGravity( 0 )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )

		self.search_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.search_crit_panel = icSearchCritPanelProto(self.search_panel)
		bSizer14.Add( self.search_crit_panel, 1, wx.ALL|wx.EXPAND, 5 )


		self.search_panel.SetSizer( bSizer14 )
		self.search_panel.Layout()
		bSizer14.Fit( self.search_panel )
		self.docs_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self.docs_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.collapse_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Свернуть", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Свернуть", u"Свернуть", None )

		self.expand_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Развернуть", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Развернуть", u"Развернуть", None )

		self.ctrl_toolBar.AddSeparator()

		self.view_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Просмотр", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Просмотр", u"Просмотр", None )

		self.edit_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Редактирование", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактирование", u"Редактирование", None )

		self.ctrl_toolBar.AddSeparator()

		self.scheme_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Схема связей", wx.ArtProvider.GetBitmap( u"gtk-dnd-multiple", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Схема связей", u"Схема связей", None )

		self.links_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-unindent", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Связи документа", u"Связи документа", None )

		self.ctrl_toolBar.AddSeparator()

		self.all_checkBox = wx.CheckBox( self.ctrl_toolBar, wx.ID_ANY, u"Выбрать все", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ctrl_toolBar.AddControl( self.all_checkBox )
		self.print_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Печать", wx.ArtProvider.GetBitmap( wx.ART_PRINT, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Печать", u"Печать", None )

		self.save_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE_AS, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Сохранить", u"Сохранить", None )

		self.ctrl_toolBar.AddSeparator()

		self.report_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_REPORT_VIEW, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Список документов", u"Список документов", None )

		self.ctrl_toolBar.Realize()

		bSizer15.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.docs_listCtrl = icchecklistctrl.icCheckListCtrl(parent=self.docs_panel, id=-1, component={})
		bSizer15.Add( self.docs_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.docs_panel, wx.ID_ANY, u"Найдено документов:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer30.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.search_count_staticText = wx.StaticText( self.docs_panel, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.search_count_staticText.Wrap( -1 )

		self.search_count_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer30.Add( self.search_count_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer15.Add( bSizer30, 0, wx.EXPAND, 5 )


		self.docs_panel.SetSizer( bSizer15 )
		self.docs_panel.Layout()
		bSizer15.Fit( self.docs_panel )
		self.panel_splitter.SplitHorizontally( self.search_panel, self.docs_panel, 500 )
		bSizer13.Add( self.panel_splitter, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer13 )
		self.Layout()
		bSizer13.Fit( self )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onViewToolClicked, id = self.view_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSchemeToolClicked, id = self.scheme_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onLinksToolClicked, id = self.links_tool.GetId() )
		self.all_checkBox.Bind( wx.EVT_CHECKBOX, self.onAllCheckBox )
		self.Bind( wx.EVT_TOOL, self.onPrintToolClicked, id = self.print_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSaveToolClicked, id = self.save_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onReportToolClicked, id = self.report_tool.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked( self, event ):
		event.Skip()

	def onExpandToolClicked( self, event ):
		event.Skip()

	def onViewToolClicked( self, event ):
		event.Skip()

	def onEditToolClicked( self, event ):
		event.Skip()

	def onSchemeToolClicked( self, event ):
		event.Skip()

	def onLinksToolClicked( self, event ):
		event.Skip()

	def onAllCheckBox( self, event ):
		event.Skip()

	def onPrintToolClicked( self, event ):
		event.Skip()

	def onSaveToolClicked( self, event ):
		event.Skip()

	def onReportToolClicked( self, event ):
		event.Skip()

	def panel_splitterOnIdle( self, event ):
		self.panel_splitter.SetSashPosition( 500 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )


###########################################################################
## Class icCtrlDocPanelProto
###########################################################################

class icCtrlDocPanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.SetSashGravity( 0 )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )

		self.search_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.search_crit_panel = icSearchCritPanelProto(self.search_panel)
		bSizer14.Add( self.search_crit_panel, 1, wx.ALL|wx.EXPAND, 5 )


		self.search_panel.SetSizer( bSizer14 )
		self.search_panel.Layout()
		bSizer14.Fit( self.search_panel )
		self.docs_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self.docs_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.collapse_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Свернуть", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Свернуть", u"Свернуть", None )

		self.expand_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Развернуть", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Развернуть", u"Развернуть", None )

		self.ctrl_toolBar.AddSeparator()

		self.view_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Просмотр", wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Просмотр", u"Просмотр", None )

		self.edit_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Редактирование", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактирование", u"Редактирование", None )

		self.del_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Удаление", u"Удаление", None )

		self.all_checkBox = wx.CheckBox( self.ctrl_toolBar, wx.ID_ANY, u"Выбрать все", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ctrl_toolBar.AddControl( self.all_checkBox )
		self.ctrl_toolBar.AddSeparator()

		self.scheme_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"Схема связей", wx.ArtProvider.GetBitmap( u"gtk-dnd-multiple", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Схема связей", u"Схема связей", None )

		self.links_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-unindent", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Связи документа", u"Связи документа", None )

		self.clear_links_tool = self.ctrl_toolBar.AddLabelTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-clear", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Удаление не существующих ссылок", u"Удаление не существующих ссылок", None )

		self.ctrl_toolBar.Realize()

		bSizer15.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.docs_listCtrl = icchecklistctrl.icCheckListCtrl(parent=self.docs_panel, id=-1, component={})
		bSizer15.Add( self.docs_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.docs_panel, wx.ID_ANY, u"Найдено документов:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer30.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.search_count_staticText = wx.StaticText( self.docs_panel, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.search_count_staticText.Wrap( -1 )

		self.search_count_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer30.Add( self.search_count_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer15.Add( bSizer30, 0, wx.EXPAND, 5 )


		self.docs_panel.SetSizer( bSizer15 )
		self.docs_panel.Layout()
		bSizer15.Fit( self.docs_panel )
		self.panel_splitter.SplitHorizontally( self.search_panel, self.docs_panel, 500 )
		bSizer13.Add( self.panel_splitter, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer13 )
		self.Layout()
		bSizer13.Fit( self )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onViewToolClicked, id = self.view_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelToolClicked, id = self.del_tool.GetId() )
		self.all_checkBox.Bind( wx.EVT_CHECKBOX, self.onAllCheckBox )
		self.Bind( wx.EVT_TOOL, self.onSchemeToolClicked, id = self.scheme_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onLinksToolClicked, id = self.links_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onClearLinksToolClicked, id = self.clear_links_tool.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked( self, event ):
		event.Skip()

	def onExpandToolClicked( self, event ):
		event.Skip()

	def onViewToolClicked( self, event ):
		event.Skip()

	def onEditToolClicked( self, event ):
		event.Skip()

	def onDelToolClicked( self, event ):
		event.Skip()

	def onAllCheckBox( self, event ):
		event.Skip()

	def onSchemeToolClicked( self, event ):
		event.Skip()

	def onLinksToolClicked( self, event ):
		event.Skip()

	def onClearLinksToolClicked( self, event ):
		event.Skip()

	def panel_splitterOnIdle( self, event ):
		self.panel_splitter.SetSashPosition( 500 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )


