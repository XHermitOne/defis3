# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.adv
import wx.propgrid as pg

from ic.bitmap import bmpfunc

###########################################################################
## Class icCreateComponentWizardProto
###########################################################################

class icCreateComponentWizardProto ( wx.adv.Wizard ):
	
	def __init__( self, parent ):
		wx.adv.Wizard.__init__ ( self, parent, id = wx.ID_ANY, title = u"Мастер создания компонента", bitmap = bmpfunc.createLibraryBitmap('py_component_wizard.png'), pos = wx.DefaultPosition, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.m_pages = []
		
		self.base_wizPage = wx.adv.WizardPageSimple( self , None, None, bmpfunc.createLibraryBitmap('py_component_wizard.png') )
		self.add_page( self.base_wizPage )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self.base_wizPage, wx.ID_ANY, u"Основные свойства компонента", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.base_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( self.base_wizPage, wx.ID_ANY, u"Определите основные параметры пользовательского компонента", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.base_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.attr_propertyGrid = pg.PropertyGrid(self.base_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE|wx.propgrid.PG_SPLITTER_AUTO_CENTER)
		self.name_propertyGridItem = self.attr_propertyGrid.Append( pg.StringProperty( u"(*) Имя класса", u"(*) Имя класса" ) ) 
		self.module_propertyGridItem = self.attr_propertyGrid.Append( pg.StringProperty( u"(*) Имя модуля", u"(*) Имя модуля" ) ) 
		self.description_propertyGridItem = self.attr_propertyGrid.Append( pg.StringProperty( u"Описание", u"Описание" ) ) 
		self.author_propertyGridItem = self.attr_propertyGrid.Append( pg.StringProperty( u"Автор", u"Автор" ) ) 
		self.copyright_propertyGridItem = self.attr_propertyGrid.Append( pg.StringProperty( u"Копирайт", u"Копирайт" ) ) 
		self.parentmodule_propertyGridItem = self.attr_propertyGrid.Append( pg.FileProperty( u"(*) Родительский модуль", u"(*) Родительский модуль" ) ) 
		self.parentclass_propertyGridItem = self.attr_propertyGrid.Append( pg.EditEnumProperty( u"(*) Родительский класс", u"(*) Родительский класс" ) ) 
		self.widget_propertyGridItem = self.attr_propertyGrid.Append( pg.BoolProperty( u"Виджет (видимый компонент)", u"Виджет (видимый компонент)" ) ) 
		self.icon_propertyGridItem = self.attr_propertyGrid.Append( pg.ImageFileProperty( u"Иконка", u"Иконка" ) ) 
		self.docfile_propertyGridItem = self.attr_propertyGrid.Append( pg.FileProperty( u"Файл документации", u"Файл документации" ) ) 
		bSizer1.Add( self.attr_propertyGrid, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline3 = wx.StaticLine( self.base_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.base_wizPage, wx.ID_ANY, u"(*) - обязательные к заполнению параметры", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.base_wizPage.SetSizer( bSizer1 )
		self.base_wizPage.Layout()
		bSizer1.Fit( self.base_wizPage )
		self.attr_wizPage = wx.adv.WizardPageSimple( self , None, None, bmpfunc.createLibraryBitmap('py_component_wizard.png') )
		self.add_page( self.attr_wizPage )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText4 = wx.StaticText( self.attr_wizPage, wx.ID_ANY, u"Атрибуты пользовательского класса", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		self.m_staticText4.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer2.Add( self.m_staticText4, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline4 = wx.StaticLine( self.attr_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.attr_wizPage, wx.ID_ANY, u"Определите аттрибуты пользовательского класса и значения по умолчанию", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer2.Add( self.m_staticText5, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline5 = wx.StaticLine( self.attr_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.ctrl_toolBar = wx.ToolBar( self.attr_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.add_attr_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Добавить", wx.EmptyString, None ) 
		
		self.del_attr_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Удалить", wx.EmptyString, None ) 
		
		self.ctrl_toolBar.AddSeparator()
		
		self.edit_attr_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактировать", u"Редактировать", None ) 
		
		self.ctrl_toolBar.Realize() 
		
		bSizer2.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )
		
		self.attr_listCtrl = wx.ListCtrl( self.attr_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer2.Add( self.attr_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.attr_wizPage.SetSizer( bSizer2 )
		self.attr_wizPage.Layout()
		bSizer2.Fit( self.attr_wizPage )
		self.event_wizPage = wx.adv.WizardPageSimple( self , None, None, bmpfunc.createLibraryBitmap('py_component_wizard.png') )
		self.add_page( self.event_wizPage )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self.event_wizPage, wx.ID_ANY, u"Сообщения пользовательского класса", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer3.Add( self.m_staticText7, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline7 = wx.StaticLine( self.event_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.event_wizPage, wx.ID_ANY, u"Установите параметры сообщений", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer3.Add( self.m_staticText8, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText81 = wx.StaticText( self.event_wizPage, wx.ID_ANY, u"Пример: keyDown | wx.EVT_KEY_DOWN | onKeyDown ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )
		self.m_staticText81.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer3.Add( self.m_staticText81, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText82 = wx.StaticText( self.event_wizPage, wx.ID_ANY, u"в тексте программы будет добавлен соответствующий обработчик:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText82.Wrap( -1 )
		self.m_staticText82.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer3.Add( self.m_staticText82, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText83 = wx.StaticText( self.event_wizPage, wx.ID_ANY, u"self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText83.Wrap( -1 )
		self.m_staticText83.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer3.Add( self.m_staticText83, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline8 = wx.StaticLine( self.event_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.event_toolBar = wx.ToolBar( self.event_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.add_event_tool = self.event_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Добавить", wx.EmptyString, None ) 
		
		self.del_event_tool = self.event_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Удалить", wx.EmptyString, None ) 
		
		self.event_toolBar.AddSeparator()
		
		self.edit_event_tool = self.event_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Редактировать", u"Редактировать", None ) 
		
		self.event_toolBar.Realize() 
		
		bSizer3.Add( self.event_toolBar, 0, wx.EXPAND, 5 )
		
		self.event_listCtrl = wx.ListCtrl( self.event_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer3.Add( self.event_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.event_wizPage.SetSizer( bSizer3 )
		self.event_wizPage.Layout()
		bSizer3.Fit( self.event_wizPage )
		self.gen_wizPage = wx.adv.WizardPageSimple( self , None, None, bmpfunc.createLibraryBitmap('py_component_wizard.png') )
		self.add_page( self.gen_wizPage )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText11 = wx.StaticText( self.gen_wizPage, wx.ID_ANY, u"Сгенерированный текст модуля компонента", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		self.m_staticText11.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer4.Add( self.m_staticText11, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline9 = wx.StaticLine( self.gen_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self.gen_wizPage, wx.ID_ANY, u"Можно внести изменения в текст модуля", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		self.m_staticText12.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer4.Add( self.m_staticText12, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline10 = wx.StaticLine( self.gen_wizPage, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.modulename_staticText = wx.StaticText( self.gen_wizPage, wx.ID_ANY, u"python_module_name.py", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.modulename_staticText.Wrap( -1 )
		self.modulename_staticText.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Sans" ) )
		
		bSizer4.Add( self.modulename_staticText, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.gen_wizPage.SetSizer( bSizer4 )
		self.gen_wizPage.Layout()
		bSizer4.Fit( self.gen_wizPage )
		self.Centre( wx.BOTH )
		
		
		# Connect Events
		self.Bind( wx.adv.EVT_WIZARD_FINISHED, self.onCreateComponentWizardFinished )
		self.Bind( wx.adv.EVT_WIZARD_PAGE_CHANGED, self.onCreateComponentWizardPageChanged )
		self.attr_propertyGrid.Bind( pg.EVT_PG_CHANGED, self.onAttrPropertyGridChanged )
		self.Bind( wx.EVT_TOOL, self.onAddAttrToolClicked, id = self.add_attr_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelAttrToolClicked, id = self.del_attr_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditAttrToolClicked, id = self.edit_attr_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onAddEventToolClicked, id = self.add_event_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelEventToolClicked, id = self.del_event_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditEventToolClicked, id = self.edit_event_tool.GetId() )
	def add_page(self, page):
		if self.m_pages:
			previous_page = self.m_pages[-1]
			page.SetPrev(previous_page)
			previous_page.SetNext(page)
		self.m_pages.append(page)
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCreateComponentWizardFinished( self, event ):
		event.Skip()
	
	def onCreateComponentWizardPageChanged( self, event ):
		event.Skip()
	
	def onAttrPropertyGridChanged( self, event ):
		event.Skip()
	
	def onAddAttrToolClicked( self, event ):
		event.Skip()
	
	def onDelAttrToolClicked( self, event ):
		event.Skip()
	
	def onEditAttrToolClicked( self, event ):
		event.Skip()
	
	def onAddEventToolClicked( self, event ):
		event.Skip()
	
	def onDelEventToolClicked( self, event ):
		event.Skip()
	
	def onEditEventToolClicked( self, event ):
		event.Skip()
	

###########################################################################
## Class icEditAttrDialogProto
###########################################################################

class icEditAttrDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Атрибут", pos = wx.DefaultPosition, size = wx.Size( 712,304 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Наименование:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		bSizer6.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.name_textCtrl = wx.TextCtrl( self, wx.ID_ANY, u"attr_name", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.name_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"Редактор:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		bSizer7.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		editor_choiceChoices = []
		self.editor_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, editor_choiceChoices, 0 )
		self.editor_choice.SetSelection( 0 )
		bSizer7.Add( self.editor_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"Значение по умолчанию:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		bSizer8.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.default_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.default_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer5.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"Описание:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		bSizer15.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.description_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.description_textCtrl, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer5.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer9.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer9, 1, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class icEditEventDialogProto
###########################################################################

class icEditEventDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Событие", pos = wx.DefaultPosition, size = wx.Size( 712,298 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Наименование:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		bSizer6.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.name_textCtrl = wx.TextCtrl( self, wx.ID_ANY, u"attr_name", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.name_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.event_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Событие:", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.event_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		event_choiceChoices = []
		self.event_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, event_choiceChoices, 0 )
		self.event_choice.SetSelection( 0 )
		self.event_choice.Enable( False )
		
		bSizer7.Add( self.event_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"Функция-обработчик:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		bSizer8.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.func_name_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.func_name_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer5.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"Описание:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		bSizer15.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.description_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.description_textCtrl, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer5.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer9.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer9, 1, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.name_textCtrl.Bind( wx.EVT_TEXT, self.onEventNameText )
		self.event_checkBox.Bind( wx.EVT_CHECKBOX, self.onEventCheckBox )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onEventNameText( self, event ):
		event.Skip()
	
	def onEventCheckBox( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

