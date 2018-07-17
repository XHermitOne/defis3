#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wx.StaicBitmap. Генерирут объект по ресурсному описанию.

@type SPC_IC_BITMAP: C{Dictionary}
@var SPC_IC_BITMAP: Спецификация на ресурсное описание компонента. Описание ключей:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{field_name=None}: Имя поля базы данных, которое отображает компонент.
    - B{type = 'Image'}: Тип объекта.
    - B{file}: Полный путь до файла хранения картинки.
    - B{position = (-1,-1)}: Расположение компонента на родительском окне.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{hlp=None}: Выражение, выполняемое после нажатия кнопки редактирования.
    - B{size = (-1,-1)}: Размер картинки.
    - B{style = 0}: Стиль окна (все стили icWindow/wx.Window).
    - B{source=None}: Описание или ссылка на источник данных.
    - B{refresh=None}: Выражение, возвращающее список обновляемых компонентов. Под обновлением понимается обновление
        представлений компонентов (для вычисляемых полей это соответствует вычислению выражения аттрибута 'getvalue').
        Если атрибут равен None, то обновляются все объекты работающие с классами данных.
    - B{recount=None}: Выражение, возвращающее список пересчитываемых компонентов. Под этим понимается пересчет
        значений хранимых в базе данных. Стадии пересчета вычисляемого поля:
            - Вычисление представления поля (по атрибуту 'getvalue').
            - Отрабатывает контроль значения поля(по атрибуту 'ctrl').
            - Если контроль проходит запись в базу вычисленного значения (по атрибуту 'setvalue').
            - Обновление представления поля (по атрибуту 'getvalue').
"""

import os
import os.path
import cStringIO
import wx
import ic.utils.util as util
from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.components.icwidget import icWidget,  SPC_IC_WIDGET
from ic.bitmap.icbitmap import icBitmapType
import ic.imglib.common as common
from ic.components import icwindow
import ic.PropertyEditor.icDefInf as icDefInf


def getBitmap(img_data):
    return wx.BitmapFromImage(getImage(img_data))


def getImage(img_data):
    stream = cStringIO.StringIO(img_data)
    return wx.ImageFromStream(stream)


imgcard = 'GIF (*.gif)|*.gif|JPG (*.jpg)|*.jpg|PNG (*.png)|*.png|BMP (*.bmp)|*.bmp|All files (*.*)|*.*'


SPC_IC_BITMAP = {'type': 'Image',
                 'name': 'DefaultName',

                 'field_name': None,
                 'file': None,
                 'hlp': None,
                 'position': (-1, -1),
                 'size': (-1, -1),
                 'foregroundColor': None,
                 'backgroundColor': None,
                 'style': 0,
                 'refresh': [],
                 'recount': [],
                 'source': None,

                 '__parent__': SPC_IC_WIDGET,
                 }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------
#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icStaticBitmap'

#   Описание стилей компонента
ic_class_styles = icwindow.ic_class_styles

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_BITMAP
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtImage'
ic_class_pic2 = '@common.imgEdtImage'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icstaticbitmap.icStaticBitmap-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 4)


class icStaticBitmap(icWidget, wx.StaticBitmap):
    """
    Класс реализует интерфейс к классу wx.StaticBitmap
    через ресурсное описание.
    """
    def __init__(self, parent=None, id=-1, component={}, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icStaticBitmap.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        self.editor = None
        
        util.icSpcDefStruct(SPC_IC_BITMAP, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        pos = component['position']
        style = component['style']
        size = component['size']
        self.hlp = component['hlp']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        img = None
        
        if component['field_name'] is None:
            self.field_name = self.name
        else:
            self.field_name = component['field_name']
   
        try:
            self.file = self.dataset.getNameValue(self.field_name)
        except:
            self.file = component['file']
            img = util.getICAttr(component['file'], self.evalSpace, msg='ERROR')

        if img and issubclass(img.__class__, wx.Bitmap):
            pass
        else:
            self.file = util.getICAttr(component['file'], self.evalSpace, msg='ERROR')
            bmptype = icBitmapType(self.file)

            if bmptype is not None and os.path.isfile(self.file):
                img = wx.Image(self.file, bmptype).ConvertToBitmap()
            else:
                img = common.icDefaultStaticPic
            
        if size == (-1, -1):
            size = wx.Size(img.GetWidth(), img.GetHeight())
                
        wx.StaticBitmap.__init__(self, parent, id, img, pos, size, style=style, name=self.name )

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.Bind(wx.EVT_LEFT_DOWN, self.OnSelect)
        self.BindICEvt()
        
    def OnSelect(self, evt):
        """
        Обрабатываем установку фокуса на компонент
        """
        if self.editor is None and self.hlp not in (None, 'None', ''):
            #   Блокируем запись для редактирования, если позволяет объект данных
            try:
                err = self.dataset.Lock()
            
                if err in [1, 2]:
                    ic_dlg.icWarningBox(u'ОШИБКА', u'Запись заблокирована err=%s' % str(err))
            except:
                pass

            id = wx.NewId()
            self.editor = wx.Button(self, id, size=(15, 15), label='>')
            self.Bind(wx.EVT_BUTTON, self.OnHelp, self.editor, id)
            
        elif self.editor is not None:
            self.editor.Destroy()
            self.editor = None
                        
            #   Разблокируем запись для редактирования, если объект данных поддерживает блокировки
            try:
                self.dataset.Unlock()
            except:
                pass
            
    def OnHelp(self, evt):
        """
        Обрабатываем нажатия кнопки выбора новой картинки.
        """
        dlg = wx.FileDialog(self, u'Выбери картинку', '', '', imgcard, wx.OPEN)
        
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            ret = self.SetValue(paths[0])
            
            if self.dataset is not None and ret:
                try:
                    ret = self.dataset.setNameValue(self.field_name, self.file)
                    
                    #   Обновляем предсавления других объектов
                    if ret in [coderror.IC_CTRL_OK, coderror.IC_CTRL_REPL]:
                        self.UpdateRelObj()
                except:
                    pass

        evt.Skip()
                
    def GetValue(self):
        """
        Возвращает имя файла картинки.
        """
        return self.file
    
    def SetValue(self, new_file):
        """
        Устанавливает новое значение картинки.
        @type new_file: C{string}
        @param new_file: Новое имя файла картинки.
        @rtype: C{bool}
        @return: Признак успешного выполнения - если файл найден и картинка создана.
        """
        self.file = new_file
        bmptype = icBitmapType(new_file)
            
        if bmptype is not None and os.path.isfile(new_file):
                
            img = wx.Image(new_file, bmptype).ConvertToBitmap()
            self.SetSize(wx.Size(img.GetWidth(), img.GetHeight()))
            self.SetBitmap(img)
            return True
        
        else:
            img = common.icDefaultStaticPic
            self.SetSize(wx.Size(img.GetWidth(), img.GetHeight()))
            self.SetBitmap(img)
        
        return False

    def UpdateDataDB(self, db_name=None, bRestore=False):
        """
        Обновляем данные в базе данных.
        
        @type db_name: C{String}
        @param db_name: Имя источника данных.
        @type bRestore: C{bool}
        @param bRestore: Признак обновления представления. Если True, то при
            неудачной попытки записи программа востановит значение поля по базе
        @rtype: C{int}
        @return: Возвращает код контроля на запись.
        """
        #   Если класс данных не задан, то считаем, что данные необходимо обновить
        if db_name is None:
            db_name = self.dataset.name

        codCtrl = coderror.IC_CTRL_FAILED
        
        if self.dataset is not None and self.dataset.name == db_name:

            value = self.GetValue()
            codCtrl = self.dataset.setNameValue(self.field_name, value)
                
            if bRestore and codCtrl in [coderror.IC_CTRL_FAILED, coderror.IC_CTRL_FAILED_IGNORE]:
                self.UpdateViewFromDB()
            
        return codCtrl
        
    def UpdateViewFromDB(self, db_name=None):
        """
        Обновляет данные в текстовом поле после изменения курсора в источнике данных.
        @type db_name: C{String}
        @param db_name: Имя источника данных.
        """
        #   Если класс данных не задан, то считаем, что объект необходимо обновить
        if db_name is None:
            db_name = self.dataset.name
            
        if self.dataset is not None and self.dataset.name == db_name and self.bStatusVisible:
            self.SetValue(self.dataset.getNameValue(self.field_name))


def test(par=0):
    """
    Тестируем icStaticBitmap.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icStaticBitmap Test', size=(200, 200))
    panel = wx.Panel(frame, -1)
    img = icStaticBitmap(panel, -1, {'position': (50, 50), 'hlp': '',
                                     'file': '''@import ic.imglib.common as common
_resultEval = common.icImageLibName('Project.gif')''',
                                     'keyDown': 'print \'keyDown in StaticBitmap\''})
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
