#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Библиотека стандартных образов системы DEFIS.
Должна содержать только PNG образы 16x16.

ВНИМАНИЕ! Библиотека образов пополняется из источников (PNG 16x16):
1. Библиотека FatCow
    http://www.fatcow.com/free-icons
2. Библиотека famfamfam_silk
    http://www.famfamfam.com/lab/icons/silk/
3. Библиотека иконок fugue-icons
    http://p.yusukekamiyamane.com/
4. Иконки темы GNOME
    ftp://ftp.gnome.org/pub/gnome/sources/gnome-icon-theme/
5. Иконки темы Tango
    http://tango.freedesktop.org/Tango_Icon_Library/
6. Иконки темы Tango IDE Editra
    все *.png из папки ../Editra-0.7.20/pixmaps/theme/Tango

Менять имена файлов не рекомендуется!!!
При обновлении обновлять и перезаписывать файлы
в порядке указанного списка.
"""

import os
import os.path
import wx
import imp

__version__ = (0, 1, 1, 1)

# Ищем путь до модуля ic
fp, icpath, description = imp.find_module('ic')

if fp:
    fp.close()

path = os.path.join(icpath, 'imglib', 'common/')


def icImageLibName(file_name):
    """
    По имени файла библиотеки картинок возвращает полный путь до файла.
    """
    return path + file_name


imgFirstData = None
imgLastData = None
imgNextData = None
imgPrevData = None
imgSearchData = None
imgPreview = None
imgClone = None
imgInsert = None
imgEdit = None
imgEdit2 = None
imgTest = None
imgMenuIt = None
imgDown = None
imgUp = None
imgPy = None
imgPopup = None
imgPopupIt = None
imgToolbrIt = None
imgUser = None
imgUsers = None
imgRole = None
imgKey = None
imgAddRes = None
imgPlus = None
imgMinus = None
imgCheck = None
imgCut = None
imgRename = None
imgProperty = None
imgAdvanced = None
imgForma = None
imgMain = None
imgMenu = None
imgDb = None
imgExport = None
imgPastef = None
imgInsert4 = None
imgDataLink = None
imgList = None
imgBox = None
imgStorage = None
imgSyncDB = None
imgDumpDB = None
imgRestoreDB = None
imgElement = None

imgNew = None
imgExit = None
imgNewPrj = None
imgBlank = None
imgPage = None
imgOpen = None
imgSave = None
imgSaveAs = None
imgDelete = None
imgDeleteRed = None
imgTrash = None
imgTrashFull = None
imgFilter = None

imgFolder = None
imgFolderRed = None
imgFolderYell = None
imgFolderOpen = None
imgFolderOpenRed = None
imgFolderOpenYell = None
imgInputFolder = None
imgInputFolderOpen = None
imgOutputFolder = None
imgOutputFolderOpen = None

imgPackageClose = None
imgPackageOpen = None
imgHelp = None
imgHelpBook = None
imgPrint = None
imgPageSettings = None
imgToExcel = None
imgConvert = None
imgPlay = None
imgDesigner = None
imgForm = None
imgProperties = None
imgEvents = None
imgGoPrevPage = None
imgGoNextPage = None
imgGoHomePage = None
imgRefreshPage = None
imgStopPage = None
imgSearchPage = None
imgGraphEditor = None
imgUserClass = None
icDefaultStaticPic = None
imgInstall = None
imgDemo = None
imgCalculate = None
imgAddWidget = None
imgDelWidget = None

# Иконки для редакторов
icoPyEditor = None
icoFormEditor = None
icoFrame = None
icoDialog = None
icoReportBrowser = None
icoIC = None

# Картинки для редактора форм
imgEdtFrame = None
imgEdtDialog = None
imgEdtNotebook = None
imgEdtSplitter = None
imgEdtWindow = None
imgEdtScrolledWindow = None
imgEdtScrolledPanel = None
imgEdtPanel = None
imgEdtDataLink = None
imgEdtGrid = None
imgEdtDBGrid = None
imgEdtObjGrid = None
imgEdtBoxSizer = None
imgEdtStaticBoxSizer = None
imgEdtImport = None
imgEdtCell = None
imgEdtSizerSpacer = None
imgEdtSeparator = None
imgEdtTextField = None
imgEdtButton = None
imgEdtStaticText = None
imgEdtNavigator = None
imgEdtListDataset = None
imgEdtChoice = None
imgEdtCheckBox = None
imgEdtRadioButton = None
imgEdtImage = None
imgEdtImgLib = None
imgEdtRenderer = None
imgEdtGridSizer = None
imgEdtFlexGridSizer = None
imgEdtToolBar = None
imgEdtTreeListCtrl = None
imgEdtTreeCheckCtrl = None
imgEdtApp = None
imgEdtMenuBar = None
imgEdtMenu = None
imgEdtMenuItem = None
imgEdtMainWin = None
imgEdtSQLite = None
imgEdtPostgreSQL = None
imgEdtMSSQL = None
imgEdtODBC = None
imgEdtCOMSrv = None
imgEdtCOMClient = None
imgEdtTable = None
imgEdtTabView = None
imgEdtQuery = None
imgEdtField = None
imgEdtLink = None
imgEdtSQLDB = None
imgEdtDBScheme = None
imgEdtDBModel = None
imgEdtDBLink = None
imgEdtStorageSrc = None
imgEdtObjStorage = None
imgEdtMetaComponent = None
imgEdtMetaData = None
imgEdtMetaTree = None
imgEdtMetaItem = None
imgEdtMetaConst = None
imgEdtMetaAttr = None
imgEdtObjects = None
imgEdtPassport = None
imgEdtConnection = None
imgEdtSignal = None
imgEdtSlot = None
imgEdtObjLink = None

imgEdtHeader = None
imgEdtHeadCell = None

# Новые картинки
imgEdtSpinner = None
imgEdtImgButton = None
imgEdtMCList = None
imgEdtStaticLine = None
imgEdtStaticBox = None
imgEdtGauge = None
imgEdtTBTool = None
imgEdtTBToolRed = None
imgEdtTBToolYell = None
imgEdtListCheckBox = None
imgEdtCalendar = None
imgEdtTrend = None
imgEdtGraphic = None
imgEdtGrphPen = None
imgEdtDiagram = None
imgEdtFigures = None

imgEdtAlignLeft = None
imgEdtAlignRight = None
imgEdtAlignTop = None
imgEdtAlignBottom = None

imgEdtExpand = None
imgEdtGrow = None
imgEdtVCenter = None
imgEdtHCenter = None
imgEdtProportion = None
imgDefis = None

# Картинки для панелей инструментов и меню
imgEdtMnuCopy = None
imgEdtMnuPaste = None
imgEdtMnuDelete = None
imgEdtMnuInsertBefore = None
imgEdtMnuInsertAfter = None
imgEdtMnuInsertInstead = None
imgDbgPrompt = None
imgDebug = None

# Wizards
imgUserCompWizard = None
imgInstallWizard = None

# Проекты
imgEdtPrj = None
imgEdtImgBrowser = None
imgEdtEnv = None
imgEdtUser = None
imgEdtUsers = None
imgEdtReport = None
imgEdtReportXML = None
imgEdtReports = None
imgEdtResource = None
imgEdtModule = None
imgEdtComponent = None
imgEdtResModule = None
imgEdtImgModule = None
imgEdtInterface = None
imgEdtTemplate = None
imgEdtMethod = None
imgEdtPlugin = None
imgEdtPluginIn = None
imgEdtPluginOut = None
imgEdtPluginNot = None

# Картинки прикладных компонентов
imgArrowIndicator = None


def img_init():
    """
    функция инициализации картинок
    """
    global path
    global imgFirstData
    global imgLastData
    global imgNextData
    global imgPrevData
    global imgSearchData
    global imgPreview
    global imgClone
    global imgInsert
    global imgEdit
    global imgEdit2
    global imgTest
    global imgMenuIt
    global imgDown
    global imgUp
    global imgPy
    global imgPopup
    global imgPopupIt
    global imgToolbrIt
    global imgUser
    global imgUsers
    global imgRole
    global imgKey
    global imgAddRes
    global imgPlus
    global imgMinus
    global imgCheck
    global imgCut
    global imgRename
    global imgProperty
    global imgAdvanced
    global imgForma
    global imgMain
    global imgMenu
    global imgDb
    global imgExport
    global imgPastef
    global imgInsert4
    global imgDataLink
    global imgList
    global imgBox
    global imgStorage
    global imgSyncDB
    global imgDumpDB
    global imgRestoreDB
    global imgNew
    global imgExit
    global imgNewPrj
    global imgBlank
    global imgPage
    global imgOpen
    global imgSave
    global imgSaveAs
    global imgDelete
    global imgDeleteRed
    global imgTrash
    global imgTrashFull
    global imgFilter
    global imgElement

    global imgFolder
    global imgFolderRed
    global imgFolderYell
    global imgFolderOpen
    global imgFolderOpenRed
    global imgFolderOpenYell
    global imgInputFolder
    global imgInputFolderOpen
    global imgOutputFolder
    global imgOutputFolderOpen

    global imgPackageClose
    global imgPackageOpen
    global imgHelp
    global imgHelpBook
    global imgPrint
    global imgPageSettings
    global imgToExcel
    global imgConvert
    global imgPlay
    global imgDesigner
    global imgForm
    global imgProperties
    global imgEvents
    global imgGoPrevPage
    global imgGoNextPage
    global imgGoHomePage
    global imgRefreshPage
    global imgStopPage
    global imgSearchPage
    global imgGraphEditor
    global imgUserClass
    global icDefaultStaticPic
    global imgInstall
    global imgDemo
    global imgCalculate
    global imgAddWidget
    global imgDelWidget
    global icoPyEditor
    global icoFormEditor
    global icoFrame
    global icoDialog
    global icoReportBrowser
    global icoIC
    global imgEdtFrame
    global imgEdtDialog
    global imgEdtNotebook
    global imgEdtSplitter
    global imgEdtWindow
    global imgEdtScrolledWindow
    global imgEdtScrolledPanel
    global imgEdtPanel
    global imgEdtDataLink
    global imgEdtGrid
    global imgEdtDBGrid
    global imgEdtObjGrid
    global imgEdtBoxSizer
    global imgEdtStaticBoxSizer
    global imgEdtImport
    global imgEdtCell
    global imgEdtSizerSpacer
    global imgEdtSeparator
    global imgEdtTextField
    global imgEdtButton
    global imgEdtStaticText
    global imgEdtNavigator
    global imgEdtListDataset
    global imgEdtChoice
    global imgEdtCheckBox
    global imgEdtRadioButton
    global imgEdtImage
    global imgEdtImgLib
    global imgEdtRenderer
    global imgEdtGridSizer
    global imgEdtFlexGridSizer
    global imgEdtToolBar
    global imgEdtHeader
    global imgEdtHeadCell
    global imgEdtSpinner
    global imgEdtImgButton
    global imgEdtMCList
    global imgEdtStaticLine
    global imgEdtStaticBox
    global imgEdtGauge
    global imgEdtTBTool
    global imgEdtTBToolRed
    global imgEdtTBToolYell
    global imgEdtListCheckBox
    global imgEdtAlignLeft
    global imgEdtAlignRight
    global imgEdtAlignTop
    global imgEdtAlignBottom
    global imgEdtExpand
    global imgEdtGrow
    global imgEdtVCenter
    global imgEdtHCenter
    global imgEdtProportion
    global imgEdtMnuCopy
    global imgEdtMnuPaste
    global imgEdtMnuDelete
    global imgEdtMnuInsertBefore
    global imgEdtMnuInsertAfter
    global imgEdtMnuInsertInstead
    global imgEdtTreeListCtrl
    global imgEdtTreeCheckCtrl
    global imgUserCompWizard
    global imgInstallWizard
    global imgDbgPrompt
    global imgDebug

    global imgEdtApp
    global imgEdtMenuBar
    global imgEdtMenu
    global imgEdtMenuItem
    global imgEdtMainWin
    global imgEdtSQLite
    global imgEdtPostgreSQL
    global imgEdtMSSQL
    global imgEdtODBC
    global imgEdtCOMSrv
    global imgEdtCOMClient
    global imgEdtTable
    global imgEdtTabView
    global imgEdtQuery
    global imgEdtField
    global imgEdtLink
    global imgEdtSQLDB
    global imgEdtDBScheme
    global imgEdtDBModel
    global imgEdtDBLink
    global imgEdtStorageSrc
    global imgEdtObjStorage
    global imgEdtMetaComponent
    global imgEdtMetaData
    global imgEdtMetaTree
    global imgEdtMetaItem
    global imgEdtMetaConst
    global imgEdtMetaAttr
    global imgEdtObjects
    global imgEdtPassport
    global imgEdtConnection
    global imgEdtSignal
    global imgEdtSlot
    global imgEdtObjLink

    global imgEdtPrj
    global imgEdtImgBrowser
    global imgEdtEnv
    global imgEdtUser
    global imgEdtUsers
    global imgEdtReport
    global imgEdtReportXML
    global imgEdtReports
    global imgEdtResource
    global imgEdtModule
    global imgEdtComponent
    global imgEdtResModule
    global imgEdtImgModule
    global imgEdtInterface
    global imgEdtTemplate
    global imgEdtMethod
    global imgEdtPlugin
    global imgEdtPluginIn
    global imgEdtPluginOut
    global imgEdtPluginNot
    
    global imgEdtCalendar
    global imgEdtTrend
    global imgEdtGraphic
    global imgEdtGrphPen
    global imgEdtDiagram
    global imgEdtFigures
    global imgArrowIndicator
    global imgDefis
    wx.InitAllImageHandlers()

    imgDbgPrompt = wx.Image(os.path.join(path, 'bug_go.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDebug = wx.Image(os.path.join(path, 'bug_delete.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgFirstData = wx.Image(os.path.join(path, 'control-double-180.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgLastData = wx.Image(os.path.join(path, 'control-double.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgNextData = wx.Image(os.path.join(path, 'control.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPrevData = wx.Image(os.path.join(path, 'control-180.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgSearchData = wx.Image(os.path.join(path, 'binocular.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPreview = wx.Image(os.path.join(path, 'document-search-result.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgClone = wx.Image(os.path.join(path, 'page_white_stack.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgInsert = wx.Image(os.path.join(path, 'node-insert.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdit = wx.Image(os.path.join(path, 'page_white_edit.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdit2 = wx.Image(os.path.join(path, 'ui-text-field.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgTest = wx.Image(os.path.join(path, 'application-run.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgMenuIt = wx.Image(os.path.join(path, 'ui-menu.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgDown = wx.Image(os.path.join(path, 'arrow_down.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgUp = wx.Image(os.path.join(path, 'arrow_up.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDown = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_MENU)
    imgUp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU)
    imgPy = wx.Image(os.path.join(path, 'python.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPopup = wx.Image(os.path.join(path, 'ui-menu.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPopupIt = wx.Image(os.path.join(path, 'ui-menu-blue.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgToolbrIt = wx.Image(os.path.join(path, 'ui-check-box-mix.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgUser = wx.Image(os.path.join(path, 'user_gray.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgUsers = wx.Image(os.path.join(path, 'group.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgRole = wx.Image(os.path.join(path, 'group_key.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgKey = wx.Image(os.path.join(path, 'ic_key.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgAddRes = wx.Image(os.path.join(path, 'plugin_add.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgPlus = wx.Image(os.path.join(path, 'ic_add.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgMinus = wx.Image(os.path.join(path, 'ic_delete.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgCheck = wx.Image(os.path.join(path, 'accept.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPlus = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_MENU)
    imgMinus = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_MENU)
    imgCheck = wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_MENU)
    imgCut = wx.Image(os.path.join(path, 'cut_red.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgRename = wx.Image(os.path.join(path, 'textfield_rename.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgProperty = wx.Image(os.path.join(path, 'property-blue.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgAdvanced = wx.Image(os.path.join(path, 'advanced.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgForma = wx.Image(os.path.join(path, 'application-form.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgMain = wx.Image(os.path.join(path, 'application-blue.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgMenu = wx.Image(os.path.join(path, 'ui-menu.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDb = wx.Image(os.path.join(path, 'database.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgExport = wx.Image(os.path.join(path, 'document-export.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPastef = wx.Image(os.path.join(path, 'clipboard-paste.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgInsert4 = wx.Image(os.path.join(path, 'document-insert.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDataLink = wx.Image(os.path.join(path, 'plugin_link.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgList = wx.Image(os.path.join(path, 'ui-list-box-blue.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgBox = wx.Image(os.path.join(path, 'box.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgStorage = wx.Image(os.path.join(path, 'store.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgSyncDB = wx.Image(os.path.join(path, 'databases-relation.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDumpDB = wx.Image(os.path.join(path, 'database-export.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgRestoreDB = wx.Image(os.path.join(path, 'database-import.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgElement = wx.Image(os.path.join(path, 'control-stop-square-small.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    imgNew = wx.Image(os.path.join(path, 'new.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgExit = wx.Image(os.path.join(path, 'control-power.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgExit = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU)
    imgNewPrj = wx.Image(os.path.join(path, 'newwin.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgBlank = wx.Image(os.path.join(path, 'page_white.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPage = wx.Image(os.path.join(path, 'page_white_text.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgOpen = wx.Image(os.path.join(path, 'open.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgSave = wx.Image(os.path.join(path, 'ic_disk.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgSaveAs = wx.Image(os.path.join(path, 'page_save.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDelete = wx.Image(os.path.join(path, 'cross.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDeleteRed = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_MENU)
    imgTrash = wx.Image(os.path.join(path, 'delete.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgTrashFull = wx.Image(os.path.join(path, 'delete_all.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgFilter = wx.Image(os.path.join(path, 'funnel.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    imgFolder = wx.Image(os.path.join(path, 'folder.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgFolderOpen = wx.Image(os.path.join(path, 'folder-open.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgInputFolder = wx.Image(os.path.join(path, 'folder-import.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgInputFolderOpen = wx.Image(os.path.join(path, 'folder-import.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgOutputFolder = wx.Image(os.path.join(path, 'folder-export.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgOutputFolderOpen = wx.Image(os.path.join(path, 'folder-export.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    
    imgPackageClose = wx.Image(os.path.join(path, 'folder.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPackageOpen = wx.Image(os.path.join(path, 'folder-open.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgHelp = wx.Image(os.path.join(path, 'question-white.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgHelp = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_MENU)
    imgHelpBook = wx.Image(os.path.join(path, 'book-question.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPrint = wx.Image(os.path.join(path, 'printer.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPageSettings = wx.Image(os.path.join(path, 'printer--pencil.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgToExcel = wx.Image(os.path.join(path, 'document-excel-table.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgConvert = wx.Image(os.path.join(path, 'document-convert.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgPlay = wx.Image(os.path.join(path, 'resultset_next.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDesigner = wx.Image(os.path.join(path, 'application_form_edit.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgForm = wx.Image(os.path.join(path, 'application_form.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgProperties = wx.Image(os.path.join(path, 'table_gear.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEvents = wx.Image(os.path.join(path, 'table_lightning.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgGoPrevPage = wx.Image(os.path.join(path, 'control-180-small.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgGoNextPage = wx.Image(os.path.join(path, 'control-000-small.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgGoHomePage = wx.Image(os.path.join(path, 'home.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgGoPrevPage = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_MENU)
    imgGoNextPage = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_MENU)
    imgGoHomePage = wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_MENU)
    imgRefreshPage = wx.Image(os.path.join(path, 'arrow-circle-double.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    # imgStopPage = wx.Image(os.path.join(path, 'cross-circle.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgStopPage = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_MENU)
    # imgSearchPage = wx.Image(os.path.join(path, 'magnifier.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgSearchPage = wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_MENU)
    imgGraphEditor = wx.Image(os.path.join(path, 'application_edit.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgUserClass = wx.Image(os.path.join(path, 'application-document.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    icDefaultStaticPic = wx.Image(os.path.join(path, 'image.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgInstall = wx.Image(os.path.join(path, 'disc-label.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDemo = wx.Image(os.path.join(path, 'disc-case.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgCalculate = wx.Image(os.path.join(path, 'calculator.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgAddWidget = wx.Image(os.path.join(path, 'block--plus.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDelWidget = wx.Image(os.path.join(path, 'block--minus.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    # Иконки для редакторов
    icoPyEditor = wx.Icon(path+'ic.ico', wx.BITMAP_TYPE_ICO)
    icoFormEditor = wx.Icon(path+'ic.ico', wx.BITMAP_TYPE_ICO)
    icoFrame = wx.Icon(path+'application_form.ico', wx.BITMAP_TYPE_ICO)
    icoDialog = wx.Icon(path+'dialog.ico', wx.BITMAP_TYPE_ICO)
    icoReportBrowser = wx.Icon(path+'report_stack.ico', wx.BITMAP_TYPE_ICO)
    icoIC = wx.Icon(path+'ic.ico', wx.BITMAP_TYPE_ICO)

    # Картинки для редактора форм
    imgEdtFrame = wx.Image(os.path.join(path, 'application.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtDialog = wx.Image(os.path.join(path, 'application-dialog.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtNotebook = wx.Image(os.path.join(path, 'ui-tab-content.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtSplitter = wx.Image(os.path.join(path, 'ui-splitter.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtWindow = wx.Image(os.path.join(path, 'ui-scroll-pane-form.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtScrolledWindow = wx.Image(os.path.join(path, 'ui-scroll-pane-both.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtScrolledPanel = wx.Image(os.path.join(path, 'ui-scroll-pane.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtPanel = wx.Image(os.path.join(path, 'ui-panel.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtDataLink = wx.Image(os.path.join(path, 'plugin_link.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtGrid = wx.Image(os.path.join(path, 'ui-scroll-pane-table.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtDBGrid = wx.Image(os.path.join(path, 'table-money.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtObjGrid = wx.Image(os.path.join(path, 'table--arrow.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtBoxSizer = wx.Image(os.path.join(path, 'layout-3.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtStaticBoxSizer = wx.Image(os.path.join(path, 'layout-2.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtImport = wx.Image(os.path.join(path, 'import.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtCell = wx.Image(os.path.join(path, 'table-select.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtSizerSpacer = wx.Image(os.path.join(path, 'arrow-resize.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtSeparator = wx.Image(os.path.join(path, 'ui-separator.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTextField = wx.Image(os.path.join(path, 'ui-text-field.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtButton = wx.Image(os.path.join(path, 'ui-button.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtStaticText = wx.Image(os.path.join(path, 'ui-label.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtNavigator = wx.Image(os.path.join(path, 'compass.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtListDataset = wx.Image(os.path.join(path, 'ui-list-box-blue.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtChoice = wx.Image(os.path.join(path, 'ui-combo-box.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtCheckBox = wx.Image(os.path.join(path, 'ui-check-box.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtRadioButton = wx.Image(os.path.join(path, 'ui-radio-button.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtImage = wx.Image(os.path.join(path, 'image-sunset.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtImgLib = wx.Image(os.path.join(path, 'images-stack.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtRenderer = wx.Image(os.path.join(path, 'paint-brush.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtGridSizer = wx.Image(os.path.join(path, 'layout-6.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtFlexGridSizer = wx.Image(os.path.join(path, 'layout-3-mix.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtToolBar = wx.Image(os.path.join(path, 'ui-toolbar.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtApp = wx.Image(os.path.join(path, 'block.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMenuBar = wx.Image(os.path.join(path, 'ui-combo-box-blue.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMenu = wx.Image(os.path.join(path, 'ui-menu.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMenuItem = wx.Image(os.path.join(path, 'ui-menu-blue.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMainWin = wx.Image(os.path.join(path, 'application-blue.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtSQLite = wx.Image(os.path.join(path, 'database-sql.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtPostgreSQL = wx.Image(os.path.join(path, 'database-sql.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMSSQL = wx.Image(os.path.join(path, 'database-sql.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtODBC = wx.Image(os.path.join(path, 'sql.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtCOMSrv = wx.Image(os.path.join(path, 'zone.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtCOMClient = wx.Image(os.path.join(path, 'zone-share.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTable = wx.Image(os.path.join(path, 'table.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTabView = wx.Image(os.path.join(path, 'table-rotate.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtQuery = wx.Image(os.path.join(path, 'ic_lightning.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtField = wx.Image(os.path.join(path, 'table-join-column.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtLink = wx.Image(os.path.join(path, 'chain.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtSQLDB = wx.Image(os.path.join(path, 'database-sql.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtDBScheme = wx.Image(os.path.join(path, 'tables-relation.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtDBModel = wx.Image(os.path.join(path, 'tables-stacks.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtDBLink = wx.Image(os.path.join(path, 'tables-relation.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtStorageSrc = wx.Image(os.path.join(path, 'database-share.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtObjStorage = wx.Image(os.path.join(path, 'database.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMetaComponent = wx.Image(os.path.join(path, 'plugin.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMetaData = wx.Image(os.path.join(path, 'plugin.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMetaTree = wx.Image(os.path.join(path, 'node.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMetaItem = wx.Image(os.path.join(path, 'node-design.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMetaConst = wx.Image(os.path.join(path, 'tag-label-black.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMetaAttr = wx.Image(os.path.join(path, 'tag-label.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtObjects = wx.Image(os.path.join(path, 'block-share.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtPassport = wx.Image(os.path.join(path, 'tag-share.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtConnection = wx.Image(os.path.join(path, 'plug-connect.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtSignal = wx.Image(os.path.join(path, 'socket--arrow.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtSlot = wx.Image(os.path.join(path, 'socket.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtObjLink = wx.Image(os.path.join(path, 'brick_link.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    imgEdtHeader = wx.Image(os.path.join(path, 'layout-select.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtHeadCell = wx.Image(os.path.join(path, 'layout-select-sidebar.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    # Новые картинки
    imgEdtSpinner = wx.Image(os.path.join(path, 'ui-spin.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtImgButton = wx.Image(os.path.join(path, 'ui-button-image.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMCList = wx.Image(os.path.join(path, 'ui-scroll-pane-detail.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtStaticLine = wx.Image(os.path.join(path, 'ui-separator.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtStaticBox = wx.Image(os.path.join(path, 'ui-group-box.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtGauge = wx.Image(os.path.join(path, 'ui-progress-bar.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTBTool = wx.Image(os.path.join(path, 'ui-check-box-mix.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTBToolRed = wx.Image(os.path.join(path, 'status-busy.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTBToolYell = wx.Image(os.path.join(path, 'status-away.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtListCheckBox = wx.Image(os.path.join(path, 'ui-check-boxes.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTreeListCtrl = wx.Image(os.path.join(path, 'ui-scroll-pane-tree.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTreeCheckCtrl = wx.Image(os.path.join(path, 'ui-scroll-pane-tree.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtCalendar = wx.Image(os.path.join(path, 'calendar.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTrend = wx.Image(os.path.join(path, 'chart-up-color.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtGraphic = wx.Image(os.path.join(path, 'chart.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtGrphPen = wx.Image(os.path.join(path, 'chart--pencil.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtDiagram = wx.Image(os.path.join(path, 'sitemap.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtFigures = wx.Image(os.path.join(path, 'ruler-triangle.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    
    imgEdtAlignLeft = wx.Image(os.path.join(path, 'layers-alignment-left.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtAlignRight = wx.Image(os.path.join(path, 'layers-alignment-right.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtAlignTop = wx.Image(os.path.join(path, 'layers-alignment.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtAlignBottom = wx.Image(os.path.join(path, 'layers-alignment-bottom.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    
    imgEdtExpand = wx.Image(os.path.join(path, 'layer-resize-replicate.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtGrow = wx.Image(os.path.join(path, 'layer-resize-replicate-vertical.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtVCenter = wx.Image(os.path.join(path, 'layers-alignment-middle.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtHCenter = wx.Image(os.path.join(path, 'layers-alignment-center.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtProportion = wx.Image(os.path.join(path, 'layer-resize.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgDefis = wx.Image(os.path.join(path, 'icon.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    
    # Картинки для панелей инструментов и меню
    imgEdtMnuCopy = wx.Image(os.path.join(path, 'page_white_copy.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMnuPaste = wx.Image(os.path.join(path, 'page_white_paste.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMnuDelete = wx.Image(os.path.join(path, 'cross.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMnuInsertBefore = wx.Image(os.path.join(path, 'node-insert-previous.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMnuInsertAfter = wx.Image(os.path.join(path, 'node-insert-next.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMnuInsertInstead = wx.Image(os.path.join(path, 'node-insert-child.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    # Wizards
    imgUserCompWizard = wx.Image(os.path.join(path, 'py_component_wizard.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgInstallWizard = wx.Image(os.path.join(path, 'py_install_wizard.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    # Проект
    imgEdtPrj = wx.Image(os.path.join(path, 'bricks.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtImgBrowser = wx.Image(os.path.join(path, 'photo-album.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtEnv = wx.Image(os.path.join(path, 'page_white_world.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtUser = wx.Image(os.path.join(path, 'user.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtUsers = wx.Image(os.path.join(path, 'users.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtReport = wx.Image(os.path.join(path, 'report.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtReportXML = wx.Image(os.path.join(path, 'page_excel.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtReports = wx.Image(os.path.join(path, 'report_stack.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtResource = wx.Image(os.path.join(path, 'plugin_edit.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtModule = wx.Image(os.path.join(path, 'python.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtComponent = wx.Image(os.path.join(path, 'attribute.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtResModule = wx.Image(os.path.join(path, 'shell.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtImgModule = wx.Image(os.path.join(path, 'images.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtInterface = wx.Image(os.path.join(path, 'document-node.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtTemplate = wx.Image(os.path.join(path, 'document-code.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtMethod = wx.Image(os.path.join(path, 'category-item.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtPlugin = wx.Image(os.path.join(path, 'plug.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtPluginIn = wx.Image(os.path.join(path, 'plug--plus.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtPluginOut = wx.Image(os.path.join(path, 'plug--minus.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    imgEdtPluginNot = wx.Image(os.path.join(path, 'plug--exclamation.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    
    # Картинки прикладных систем
    imgArrowIndicator = wx.Image(os.path.join(path, 'dashboard.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
