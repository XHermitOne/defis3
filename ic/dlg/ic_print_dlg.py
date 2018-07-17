#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Диалоговая форма выбора параметров печати.
Диалоговая форма взята из сервиса UPrint проекта icservices.
"""

import os
import os.path
import wx
from . import uprint_dlg
from ic.log import log
from ic.utils import ic_file
from ic.utils import ini
from ic.utils import printerfunc

DEFAULT_OPTIONS_FILENAME = 'printer_options.ini'

# Размер точки печати.
# Поля печати задаются в точках 1 точка 1.72 дюйма или 0.35мм
MARGIN_POINT_SIZE = 0.35


class icPrintDlg(uprint_dlg.icUPrintDlgProto):
    """
    Основное окно выбора параметров печати.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        uprint_dlg.icUPrintDlgProto.__init__(self, *args, **kwargs)

        self.args = None

        self.init()

        self.opt_filename = None

        self.printer = None

        self.size = None
        self.orientation = None
        self.width = None
        self.height = None
        self.order = None
        self.pages = None
        self.copies = None
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        self.lines = None
        self.use_font = None

        self.print_filename = None

        self.loadPrintOptions()
        self.showPrintOptions()

    def get_img_path(self):
        """
        Папка образов.
        """
        my_dir = os.path.dirname(__file__)
        if not my_dir:
            my_dir = os.getcwd()
        return os.path.join(my_dir, 'img')

    def init(self):
        """
        Инициализация контролов.
        """
        self.initComboBoxPrinters()

        img_filename = os.path.join(self.get_img_path(), u'A4P.png')
        self.paper_comboBox.Append(u'A4 книжная ориентация', wx.Image.ConvertToBitmap(wx.Image(img_filename)));
        img_filename = os.path.join(self.get_img_path(), u'A4L.png')
        self.paper_comboBox.Append(u'A4 альбомная ориентация', wx.Image.ConvertToBitmap(wx.Image(img_filename)));
        img_filename = os.path.join(self.get_img_path(), u'A3L.png')
        self.paper_comboBox.Append(u'A3 альбомная ориентация', wx.Image.ConvertToBitmap(wx.Image(img_filename)));
        img_filename = os.path.join(self.get_img_path(), u'A3P.png')
        self.paper_comboBox.Append(u'A3 книжная ориентация', wx.Image.ConvertToBitmap(wx.Image(img_filename)));
        self.paper_comboBox.SetSelection(0)

        img_filename = os.path.join(self.get_img_path(), u'Page.png')
        bitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        self.m_bitmap1.SetBitmap(bitmap)

        option_notebookImageSize = wx.Size(16, 16)
        option_notebookIndex = 0
        option_notebookImages = wx.ImageList(option_notebookImageSize.GetWidth(), option_notebookImageSize.GetHeight())
        self.option_notebook.AssignImageList(option_notebookImages)

        img_filename = os.path.join(self.get_img_path(), u'printer.png')
        option_notebookBitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        if (option_notebookBitmap.Ok()):
            option_notebookImages.Add(option_notebookBitmap)
            self.option_notebook.SetPageImage(option_notebookIndex, option_notebookIndex)
            option_notebookIndex += 1

        img_filename = os.path.join(self.get_img_path(), u'border-outside-thick.png')
        option_notebookBitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        if (option_notebookBitmap.Ok()):
            option_notebookImages.Add(option_notebookBitmap)
            self.option_notebook.SetPageImage(option_notebookIndex, option_notebookIndex)
            option_notebookIndex += 1

        self.ok_button.SetFocus()

    def setPrintOptions(self, args, bShow=True):
        """
        Установить параметры печати из списка аргументов.
        @param args: Список аргументов.
        @param bShow: Обновить в диалоговом окне контролы?
        """
        if isinstance(args, dict):
            self.args = args
        elif isinstance(args, list):
            self.args = dict(args)
        else:
            log.error(u'Wrong type arguments <%s>' % type(args))
            return

        for option, arg in self.args.items():
            if option in ('--printer',):
                self.printer = arg
            elif option in ('--A4', '--a4'):
                self.size = 'a4'
            elif option in ('--A3', '--a3'):
                self.size = 'a3'
            elif option in ('--portrait', '-P'):
                self.orientation = 'portrait'
            elif option in ('--landscape', '-L'):
                self.orientation = 'landscape'
            elif option in ('--width', '-w'):
                self.width = int(arg)
            elif option in ('--height', '-h'):
                self.height = int(arg)
            elif option in ('--all',):
                self.order = 'all'
            elif option in ('--even',):
                self.order = 'even'
            elif option in ('--odd',):
                self.order = 'odd'
            elif option in ('--pages',):
                self.pages = arg
            elif option in ('--copies',):
                self.copies = int(arg)
            elif option in ('--left', '-l'):
                self.left = int(arg)
            elif option in ('--right', '-r'):
                self.right = int(arg)
            elif option in ('--top', '-t'):
                self.top = int(arg)
            elif option in ('--bottom', '-b'):
                self.bottom = int(arg)
            elif option in ('--lines',):
                self.lines = int(arg)
            elif option in ('--use_font',):
                self.use_font = True
            elif option in ('--dlg',):
                pass
            elif option in ('--file',):
                self.print_filename = arg
            else:
                log.warning(u'Not defined option <%s>' % option)

        if bShow:
            self.showPrintOptions()

    def genOptFileName(self):
        """
        Генерация имени файла параметров печати.
        """
        if self.opt_filename is None:
            self.opt_filename = os.path.join(ic_file.getProfilePath(), DEFAULT_OPTIONS_FILENAME)
        return self.opt_filename

    def loadPrintOptions(self, sFileName=None):
        """
        Загрузить параметры печати из конфигурационного файла.
        @param sFileName: Имя файла параметров печати.
        """
        if sFileName is None:
            sFileName = self.genOptFileName()

        ini_dict = ini.INI2Dict(sFileName)
        if ini_dict:
            self.printer = ini_dict['OPTIONS'].get('printer', None)
            self.size = ini_dict['OPTIONS'].get('size', None)
            self.orientation = ini_dict['OPTIONS'].get('orientation', None)
            self.width = ini_dict['OPTIONS'].get('width', None)
            self.height = ini_dict['OPTIONS'].get('height', None)
            self.order = ini_dict['OPTIONS'].get('order', None)
            # self.pages = ini_dict['OPTIONS'].get('pages', None)
            self.copies = ini_dict['OPTIONS'].get('copies', None)
            self.left = ini_dict['OPTIONS'].get('left', None)
            self.right = ini_dict['OPTIONS'].get('right', None)
            self.top = ini_dict['OPTIONS'].get('top', None)
            self.bottom = ini_dict['OPTIONS'].get('bottom', None)
            self.lines = ini_dict['OPTIONS'].get('lines', None)
            self.use_font = ini_dict['OPTIONS'].get('use_font', None)

    def savePrintOptions(self, sFileName=None):
        """
        Записать параметры печати в конфигурационный файл.
        @param sFileName: Имя файла параметров печати.
        """
        if sFileName is None:
            sFileName = self.genOptFileName()

        ini_dict = self.getOptions()
        ini.Dict2INI(ini_dict, sFileName)

    def showPrintOptions(self):
        """
        Выставить параметры печати в контролах окна.
        """
        if self.printer:
            self.printer = self.printer if type(self.printer) in (str, unicode) else str(self.printer)
            self.printer_comboBox.SetStringSelection(self.printer)

        if self.size and self.orientation:
            i = 0
            if self.size == 'a4' and self.orientation == 'portrait':
                i = 0
            elif self.size == 'a4' and self.orientation == 'landscape':
                i = 1
            elif self.size == 'a3' and self.orientation == 'landscape':
                i = 2
            elif self.size == 'a3' and self.orientation == 'portrait':
                i = 3
            self.paper_comboBox.Select(i)

        if self.pages:
            self.pages_textCtrl.SetValue(self.pages)
        else:
            self.pages_textCtrl.SetValue('1-9999')

        if self.copies:
            self.copies_spinCtrl.SetValue(self.copies)
        else:
            self.copies_spinCtrl.SetValue(1)

        i_dict = {'all': 0, 'even': 1, 'odd': 2}
        self.page_radioBox.SetSelection(i_dict.get(self.order, 0))

        if self.left:
            self.left_spinCtrl.SetValue(self.left)
        else:
            self.left_spinCtrl.SetValue(0)

        if self.right:
            self.right_spinCtrl.SetValue(self.right)
        else:
            self.right_spinCtrl.SetValue(0)

        if self.top:
            self.top_spinCtrl.SetValue(self.top)
        else:
            self.top_spinCtrl.SetValue(0)

        if self.bottom:
            self.bottom_spinCtrl.SetValue(self.bottom)
        else:
            self.bottom_spinCtrl.SetValue(0)

    def readPrintOptions(self):
        """
        Считать с контролов параметры печати.
        """
        self.printer = self.printer_comboBox.GetStringSelection()

        i = self.paper_comboBox.GetSelection()
        if i == 0:
            self.size = 'a4'
            self.orientation = 'portrait'
        elif i == 1:
            self.size = 'a4'
            self.orientation = 'landscape'
        elif i == 2:
            self.size = 'a3'
            self.orientation = 'landscape'
        if i == 3:
            self.size = 'a3'
            self.orientation = 'portrait'

        self.pages = self.pages_textCtrl.GetValue()

        self.copies = self.copies_spinCtrl.GetValue()

        i_dict = {0: 'all', 1: 'even', 2: 'odd'}
        self.order = i_dict.get(self.page_radioBox.GetSelection(), 0)

        self.left = self.left_spinCtrl.GetValue()
        self.right = self.right_spinCtrl.GetValue()
        self.top = self.top_spinCtrl.GetValue()
        self.bottom = self.bottom_spinCtrl.GetValue()

    def getOptions(self):
        """
        Параметры печати в виде словаря.
        """
        options_dict = dict()
        options_dict['OPTIONS'] = dict()
        options_dict['OPTIONS']['printer'] = self.printer
        options_dict['OPTIONS']['size'] = self.size
        options_dict['OPTIONS']['orientation'] = self.orientation
        options_dict['OPTIONS']['width'] = self.width
        options_dict['OPTIONS']['height'] = self.height
        options_dict['OPTIONS']['order'] = self.order
        # ini_dict['OPTIONS']['pages'] = '\''+self.pages+'\''
        options_dict['OPTIONS']['copies'] = self.copies
        options_dict['OPTIONS']['left'] = self.left
        options_dict['OPTIONS']['right'] = self.right
        options_dict['OPTIONS']['top'] = self.top
        options_dict['OPTIONS']['bottom'] = self.bottom
        options_dict['OPTIONS']['lines'] = self.lines
        options_dict['OPTIONS']['use_font'] = self.use_font
        return options_dict

    def onCanceButtonClick(self, event):
        """
        Обработчик нажатия кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOKButtonClick(self, event):
        """
        Обработчик нажатия кнопки <Печать>.
        """
        ctrl_args = self._getCtrlArgs()
        self.args.update(ctrl_args)

        # Сохранить те параметры которые выбрали
        self.readPrintOptions()
        self.savePrintOptions()

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onPreviewButtonClick(self, event):
        """
        Обработчик нажатия кнопки <Печать>.
        """
        ctrl_args = self._getCtrlArgs()
        self.args.update(ctrl_args)

        # Сохранить те параметры которые выбрали
        self.readPrintOptions()
        self.savePrintOptions()

        self.EndModal(wx.OK)
        event.Skip()

    _noNixPrintArgs = ('--dlg', '--printer')

    def _getArgsStr(self, dArgs=None):
        """
        Получить аргументы в виде строки.
        """
        if dArgs is None:
            dArgs = self.args

        return ' '.join([name + '=' + value if value else name for name, value in dArgs.items() if
                         name not in self._noNixPrintArgs])

    def _getCtrlArgs(self):
        """
        Получить аргументы для коммандной строки из контролов.
        """
        result = {}

        printer = self.printer_comboBox.GetValue()
        result['--printer'] = printer

        paper = self.paper_comboBox.GetSelection()
        if paper == 1:
            # A4 landscape
            result['--landscape'] = ''
        elif paper == 2:
            # A3 landscape
            result['--landscape'] = ''
            result['--A3'] = ''
        elif paper == 3:
            # A3 portrait
            result['--portrait'] = ''
            result['--A3'] = ''

        pages = self.pages_textCtrl.GetValue()
        if pages and pages != '1-9999':
            result['--pages'] = pages

        copies = self.copies_spinCtrl.GetValue()
        if copies > 1:
            result['--copies'] = str(copies)

        page = self.page_radioBox.GetSelection()
        if page == 1:
            # Нечетные
            result['--odd'] = ''
        elif page == 2:
            # Четные
            result['--even'] = ''

        border = self.left_spinCtrl.GetValue()
        if border:
            result['--left'] = str(border)
        border = self.right_spinCtrl.GetValue()
        if border:
            result['--right'] = str(border)
        border = self.top_spinCtrl.GetValue()
        if border:
            result['--top'] = str(border)
        border = self.bottom_spinCtrl.GetValue()
        if border:
            result['--bottom'] = str(border)

        return result

    def initComboBoxPrinters(self, sSelectPrinter=None):
        """
        Инициализация комбобокса списка принтеров системы.
        @param sSelectPrinter: Какой принтер выбрать после
        инициализации комбобокса, если None то выбирается принтер по умолчанию.
        """
        printers_info = printerfunc.getPrintersInfo()

        self.printer_comboBox.Clear()

        if printers_info:
            default_select = 0
            i = 0
            for default, printer_name in printers_info:

                img_filename = os.path.join(self.get_img_path(), u'printer.png')
                if default:
                    img_filename = os.path.join(self.get_img_path(), u'printer--arrow.png')
                    if sSelectPrinter is None:
                        default_select = i
                if printer_name == sSelectPrinter:
                    default_select = i

                self.printer_comboBox.Append(printer_name, wx.Image.ConvertToBitmap(wx.Image(img_filename)))
                i += 1

            self.printer_comboBox.Select(default_select)


def get_print_option_dlg(parent=None):
    """
    Вызвать диалоговое окно параметров печати.
    @param parent: Родительское окно.
    @return:
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = icPrintDlg(parent=parent)
    result = dlg.ShowModal()
    ret =None
    if result == wx.ID_OK:
        ret = dlg.getOptions()
    dlg.Destroy()
    return ret


def showPrintDialog(args):
    app = wx.PySimpleApp()

    dlg = icPrintDlg(None)
    dlg.setPrintOptions(args)
    result = dlg.ShowModal()
    log.info('Result: %s OK: %s' % (result, wx.OK))
    # app.MainLoop()

    dlg.Destroy()
    dlg = None

    return result == wx.OK


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    dlg = icPrintDlg(None)
    log.debug('Default printer: %s' % printerfunc.getDefaultPrinter())
    log.debug('Printers: %s' % printerfunc.getPrinters())
    log.debug('Printers info: %s' % printerfunc.getPrintersInfo())
    dlg.ShowModal()
    dlg.Destroy()
    dlg = None
    app.MainLoop()


if __name__ == '__main__':
    test()
