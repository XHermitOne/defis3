#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wxToolBar. Генерирует панель инструментов
по ресурсному описанию. В панеле инструментов
может находится: кнопка,  разделитель, текст, текст с выбором.

@type SPC_IC_TOOLBAR: C{dictionary}
@var SPC_IC_TOOLBAR: Спецификация на ресурсное описание панели инструментов. Описание ключей:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'ToolBar'}: Тип объекта.
    - B{position = (-1,-1)}: Расположение компонента на родительском окне.
    - B{size = (-1,-1)}: Размер картинки.
    - B{image_list=None} : Паспорт списка картинок (icImageList).
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{style = wx.TB_HORIZONTAL | wx.NO_BORDER}: Стиль панели инструментов. Стили:
        - TB_FLAT - Плоский вид панели (только Windows 95 и GTK 1.2).
        - TB_DOCKABLE  - Перемещаемая панель (только GTK).
        - TB_HORIZONTAL - Определяет горизонтальное расположение.
        - TB_VERTICAL  - Определяет вертикальное расположение.
        - TB_3DBUTTONS  - Придает кнопкам панели 3D вид.
        - TB_TEXT  - Показывает текст на кнопках; по умолчанию показываются только иконки.
        - TB_NOICONS  - Определяет, что не надо показывать иконки на кнопках; по умолчанию они показываются.
        - TB_NODIVIDER  - Убирает разделитель над кнопками (только Windows).
        - TB_NOALIGN  - Отминяет выравнивание по родительскому окну (Windows only).

@type ICToolbarStyle: C{dictionary}
@var ICToolbarStyle: Словарь специальных стилей компонента.
        
@type SPC_IC_TB_SEPARATOR: C{Dictionary}
@var SPC_IC_TB_SEPARATOR: Спецификация на ресурсное описание резделителя между гуппами инструментов.
Описание ключей:

    - B{name = ''}: Имя объекта.
    - B{type = 'Separator'}: Тип объекта.
    - B{size = 5}: Размер разделителя, устанавливаемого ф-ией: wx.ToolBar.SetToolSeparation(obj, size).

@type SPC_IC_TB_TOOL: C{Dictionary}
@var SPC_IC_TB_TOOL: Спецификация на ресурсное описание инструмента панели инструментов. Описание ключей:

    - B{name = 'default'}: Имя объекта.
    - B{type = 'ToolBarTool'}: Тип объекта.
    - B{toolType=0}: Тип инструмента (0 - кнопка, 1- checkbox, 2- radiobutton).
    - B{label=''}: Подпись инструмента.
    - B{bitmap=None}: Картинка на кнопке.
    - B{pushedBitmap=None}: Картинка на нажатой кнопки инструмента.
    - B{img_indx:-1}: Индекс картинки из списка картинок, заданного в атрибуте 
        'image_list' родительского компонента. Если -1, то картинки берутся по порядку.
    - B{isToggle=0}:
    - B{shortHelpString='icButton'}: Короткая строка описания.
    - B{longHelpString=''}: Длинная строка описания. Она появляетс в статусбаре родительского окна при наведении курсора мышкой.
    - B{OnTool=None}: Указатель на функцию, которая отрабатывается после нажатия на кнопку инструмента.
"""
        
import wx
import ic.utils.util as util
from ic.bitmap.icbitmap import icBitmapType
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
from ic.components import icwidget
from ic.kernel import io_prnt
import ic.utils.coderror as coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

TBFLAGS = (wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)

ICToolbarStyle = {'TB_FLAT': wx.TB_FLAT,
                  'TB_DOCKABLE': wx.TB_DOCKABLE,
                  'TB_HORIZONTAL': wx.TB_HORIZONTAL,
                  'TB_VERTICAL': wx.TB_VERTICAL,
                  'TB_3DBUTTONS': wx.TB_3DBUTTONS,
                  'TB_TEXT': wx.TB_TEXT,
                  'TB_NOICONS': wx.TB_NOICONS,
                  'TB_NODIVIDER': wx.TB_NODIVIDER,
                  'TB_NOALIGN': wx.TB_NOALIGN,
                  'DEFAULT': TBFLAGS,
                  }


SPC_IC_TOOLBAR = {'type': 'ToolBar',
                  'name': 'DefaultName',
                  'activate': True,
                  'child': [],

                  'position': (-1, -1),
                  'size': (-1, -1),
                  'image_list': None,
                  'bitmap_size': (16, 16),
                  'foregroundColor': None,
                  'backgroundColor': None,
                  'style': wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_NODIVIDER,

                  '__attr_types__': {icDefInf.EDT_SIZE: ['bitmap_size'],
                                     icDefInf.EDT_USER_PROPERTY: ['image_list'],
                                     icDefInf.EDT_CHECK_BOX: ['activate'],
                                     },
                  '__parent__': icwidget.SPC_IC_WIDGET,
                  }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icComboType

#   Имя пользовательского класса
ic_class_name = 'icToolBar'

#   Описание стилей компонента
ic_class_styles = ICToolbarStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_TOOLBAR
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtToolBar'
ic_class_pic2 = '@common.imgEdtToolBar'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.ictoolbar.icToolBar-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBar', 'DatasetNavigator', 'GridCell']


SPC_IC_TB_SEPARATOR = {'type': 'Separator',
                       'name': '',
                       'activate': True,
                       '_uuid': None,
                       'init_expr': None,

                       'size': 5,

                       '__attr_types__': {icDefInf.EDT_PY_SCRIPT: ['init_expr'],
                                          icDefInf.EDT_TEXTFIELD: ['name', 'type', '_uuid'],
                                          icDefInf.EDT_NUMBER: ['size'],
                                          icDefInf.EDT_CHECK_BOX: ['activate'],
                                          },
                       }

#   Типы инструментов
icTBButton = 0
icTBCheckBox = 1
icTBRadio = 2

SPC_IC_TB_TOOL = {'type': 'ToolBarTool',
                  'name': 'default',
                  'activate': True,
                  'init_expr': None,
                  '_uuid': None,

                  'toolType': icTBButton,
                  'label': '',
                  'bitmap': '',
                  'disabledBitmap': None,
                  'pushedBitmap': None,
                  'shortHelpString': 'icButton',
                  'img_indx': -1,
                  'push_img_indx': -1,
                  'dis_img_indx': -1,
                  'longHelpString': '',
                  'isToggle': False,
                  'onTool': None,

                  '__events__': {'onTool': ('wx.EVT_TOOL', 'OnToolClick', False),
                                 },
                  '__attr_types__': {icDefInf.EDT_PY_SCRIPT: ['init_expr'],
                                     icDefInf.EDT_NUMBER: ['toolType', 'img_indx',
                                                           'dis_img_indx', 'push_img_indx'],
                                     icDefInf.EDT_TEXTFIELD: ['name', 'type', 'label', '_uuid'],
                                     icDefInf.EDT_CHECK_BOX: ['activate', 'isToggle'],
                                     },
                  }

#   Версия компонента
__version__ = (1, 0, 0, 10)


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('image_list',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('image_list',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('icImageList', ):
                ic_dlg.icWarningBox(u'ОШИБКА', u'Выбранный объект не является списком картинок icImageList.')
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('image_list',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icToolBar(icwidget.icWidget, wx.ToolBar):
    """
    Интерфейс к классу wx.ToolBar.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wxWindow}
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
        util.icSpcDefStruct(SPC_IC_TOOLBAR, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        size = component['size']
        pos = component['position']
        style = component['style']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        image_list = component['image_list']
        
        if image_list:
            self.image_list = self.GetImageList(image_list)
        else:
            self.image_list = None
            
        #   Словарь выполяняемых выражений для разных инструментов панели
        self._onToolDict = {}
        
        wx.ToolBar.__init__(self, parent, id, pos, size, style, name=self.name)

        sz = component['bitmap_size']
        self.SetToolBitmapSize(wx.Size(sz[0], sz[1]))
        
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))
            
        self.BindICEvt()
        
        # Словарь соответствий между именами и идентификаторами инструментов
        self._tool_name_id = {}

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            indx = 0
            for el in self.child:
                if not el['activate'] in (0, '0', None, 'None', 'False', 'false'):
                    if el['type'] == 'ToolBarTool':
                        img_indx = el.get('img_indx', -1)
                        if img_indx < 0:
                            img_indx = indx
                        self.AddToolRes(icwidget.icNewId(), el, img_indx)
                        indx += 1
                    elif el['type'] == 'Separator':
                        self.AddSeparator()
                    else:
                        res = self.GetKernel().parse_resource(self, [el], None, context=self.evalSpace,
                                                              bCounter=bCounter, progressDlg=progressDlg)
                        
                        nm = el['name']
                        if nm in self.components:
                            obj = self.components[nm]
                            self.AddControl(obj)
            
            self.Realize()
    
    def GetImageList(self, image_list_psp=None):
        """
        По паспорту создаем объект icImageList.
        """
        if image_list_psp is None:
            image_list_psp = self.image_list
        imagelist = self.GetKernel().Create(image_list_psp)
        return imagelist

    def _get_bitmap(self, id, component, indx, push_indx=-1, dis_indx=-1):
        """
        Возвращает картинки инструмента.
        """
        if self.image_list:
            if indx < self.image_list.GetImageCount():
                bmp = self.image_list.GetBitmap(indx)
            else:
                bmp = None

            if bmp is None:
                bmp = common.imgEdtTBTool

            push_bmp, dis_bmp = wx.NullBitmap, wx.NullBitmap
            if push_indx >= 0:
                push_bmp = self.image_list.GetBitmap(push_indx)
            if dis_indx >= 0:
                dis_bmp = self.image_list.GetBitmap(dis_indx)
            return bmp, push_bmp, dis_bmp

        # Активная картинка
        bitmap = util.getICAttr(component['bitmap'], self.evalSpace, msg='ERROR')
        if not (bitmap and issubclass(bitmap.__class__, wx.Bitmap)):
            bitmap = ic_bmp.createBitmap(component['bitmap'])
            if not bitmap:
                bitmap = common.imgEdtImage
        # Неактивная картинка
        dis_bitmap = util.getICAttr(component['disabledBitmap'], self.evalSpace, msg='ERROR')
        if not (dis_bitmap and issubclass(bitmap.__class__, wx.Bitmap)):
            dis_bitmap = ic_bmp.createBitmap(component['disabledBitmap'])
            if not dis_bitmap:
                dis_bitmap = wx.NullBitmap
        #   Картинка в нажатом состоянии
        push_bitmap = util.getICAttr('pushedBitmap', self.evalSpace, msg='ERROR')
        if not (push_bitmap and issubclass(push_bitmap.__class__, wx.Bitmap)):
            push_bitmap = ic_bmp.createBitmap(component['pushedBitmap'])
            if not push_bitmap:
                push_bitmap = wx.NullBitmap
        
        return bitmap, push_bitmap, dis_bitmap
        
    def AddToolRes(self, id, component, indx=0):
        """
        Добавляет инструмент в панель по ресурсному описанию.
        @type id: C{int}
        @param id: Идентификатор инструмента.
        @type component: C{dictionary}
        @param component: Словарь описания компонента согласно спецификации, описанной в SPC_IC_TB_TOOL.
        """
        util.icSpcDefStruct(SPC_IC_TB_TOOL, component)
        
        #   Создаем bitmap
        self.evalSpace['common'] = common
        bitmap, push_bitmap, dis_bitmap = self._get_bitmap(id, component, indx, 
                                                           component['push_img_indx'], component['dis_img_indx'])
        kind = wx.ITEM_NORMAL
        
        # Запомнить идентификатор инструмента
        self._tool_name_id[component['name']] = id
        
        #   Добавляем в панель инструментов
        if component['toolType'] == icTBCheckBox:
            self.AddCheckTool(bitmap=bitmap, id=id)
        elif component['toolType'] == icTBRadio:
            self.AddRadioTool(bitmap=bitmap, id=id)
        else:
            kind = wx.ITEM_NORMAL
            if component['isToggle']: 
                kind = wx.ITEM_CHECK
            self.DoAddTool(bitmap=bitmap, id=id, label=component['label'],
                           kind=kind, longHelp=component['longHelpString'],
                           bmpDisabled=dis_bitmap,
                           shortHelp=component['shortHelpString'])

        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=id)
        self._onToolDict[id] = component['onTool']
        self.Realize()
        
    def getToolId(self, ToolName_):
        """
        Идентификатор инструмента по его имени.
        @param ToolName_: Имя инструмента.
        """
        try:
            return self._tool_name_id[ToolName_]
        except:
            return None
            
    def enableTool(self, ToolName_, Enable_=True):
        """
        Вкл./выкл. инструмент по имени.
        @param ToolName_: Имя инструмента.
        @param Enable_: True/False.
        """
        return self.EnableTool(self.getToolId(ToolName_), Enable_)
        
    def OnToolClick(self, evt):
        """
        Обрабатываем нажатие кнопки соответствующего инструмента панели.
        """
        id = evt.GetId()
        if id in self._onToolDict:
            self.evalSpace['evt'] = evt
            self.evalSpace['self'] = self
            
            if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
                self.eval_expr(self._onToolDict[id], 'onTool'+str(id))
        evt.Skip()


def test(par=0):
    """
    Тестируем класс icFrame.
    """
    import cStringIO
    
    def getBitmap(imgDataString):
        return wx.BitmapFromImage(getImage(imgDataString))

    def getImage(imgDataString):
        stream = cStringIO.StringIO(imgDataString)
        return wx.ImageFromStream(stream)

    imgLastData = '''\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0c\x00\x00\x00\x0c\x08\x06\
\x00\x00\x00Vu\\\xe7\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\
\x00DIDATx\x9cc\x14\x10\x10` \x050\x91\xa4\x1a]\xc3\x87\x0f\x1f\xfe\xa3+@\
\x17\xc3\xb0\x01\x9b&\x82N\xc2\xa7\t\xa7\x1fpi\xa2\xcc\xd3\xc8@@@\x80\x91h\r\
\xb8\x14c\xd5\x80O1\x03\x03\x03\x03#\xcdc\x1a\x00Z?\x14\x15@\xe1\xee\x13\x00\
\x00\x00\x00IEND\xaeB`\x82'''

    from ic.components.ictestapp import TestApp
    app = TestApp(par)

    frame = wx.Frame(None, -1, 'ToolBar Test')
    print(common.icoDialog)
    frame.SetIcon(common.icoDialog)
    
    toolBar = icToolBar(frame, -1)
    toolBar.AddTool(bitmap=getBitmap(imgLastData), id=wx.NewId())
    toolBar.Realize()
    frame.SetToolBar(toolBar)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
