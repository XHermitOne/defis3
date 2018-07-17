# ! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
ДЕПРИКАТЕД КОМПОНЕНТ!!!
Компонент реализующий основные функции навигации по таблице данных.
Содержит описание класса icDatasetNavigator, который по ресурсному описанию создает компонент
навигации и поиска по источнику данных.

@type SPC_IC_DATASET_NAVIGATOR: C{dictionary}
@var SPC_IC_DATASET_NAVIGATOR: Спецификация на ресурсное описание навигатора.
Описание ключей SPC_IC_DATASET_NAVIGATOR:

    - B{name = 'default'}: Имя окна.
    - B{type = 'DatasetNavigator'}: Тип компонента.
    - B{position = (-1,-1)}: Расположение компонента.
    - B{size = (200, 20)}: Размер компонента.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{object_link=None}: Имя объекта либо объект, к которому присоединен навигатор (обычно грид).
    - B{style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_NODIVIDER}: Используются все стили класса wx.ToolBar.
    - B{source=None}: Описание или ссылка на источник данных.
    - B{buttonUpdate=1}: Признак наличия кнопки 'сохранить'.
    - B{buttonAdd=1}: Признак наличия кнопки 'добавить'.
    - B{buttonDel=1}: Признак наличия кнопки 'удалить'.
    - B{buttonHelp=1}: Признак наличия кнопки 'помощь'.
    - B{buttonPrint=1}: Признак наличия кнопки 'печать'.
    - B{onDelete=None}: Выражение, вычисляемое при нажатии кнопки 'Удалить'. Если выражение вернет False, то функционал
        по умолчанию выполнятся не будет, если True, то выполняется функционал по умолчанию. По умолчанию при нажатии
        кнопки 'удалить' объект для каждого компонента формы вызывает функцию DelRows(<положение курсора>,
        <количество удаляемых строк>=1).
    - B{onUpdate=None}: Выражение, вычисляемое при нажатии кнопки 'Изменить'.
    - B{onAdd=None}: Выражение, вычисляемое при нажатии кнопки 'Добавить'. Если выражение вернет False, то функционал
        по умолчанию выполнятся не будет, если True, то выполняется функционал по умолчанию. По умолчанию при нажатии
        кнопки 'добавить' объект для каждого компонента формы вызывает функцию AddRows().
    - B{onHelp=None}: Выражение, вычисляемое при нажатии кнопки 'Помощь'.
    - B{onPrint=None}: Выражение, вычисляемое при нажатии кнопки 'Печать'.
    - B{refresh=None}: Выражение, возвращающее список обновляемых компонентов. Под обновлением понимается обновление
        представлений компонентов (для вычисляемых полей это соответствует вычислению выражения аттрибута 'getvalue').
        Если атрибут равен None, то обновляются все объекты работающие с классами данных.
"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
import ic.utils.util as util
from ic.imglib import common
from . import icfont
import os, cStringIO
from .icwidget import icWidget, SPC_IC_WIDGET
from ic.components.custom import ictoolbar
import ic.PropertyEditor.icDefInf as icDefInf
from ic.kernel import io_prnt

from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

_ = wx.GetTranslation

TBFLAGS = (wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)

#   Спецификация описания навигатора
SPC_IC_DATASET_NAVIGATOR = {'type': 'DatasetNavigator',
                            'name': 'default',

                            'position': (-1, -1),
                            'size': (200, 20),
                            'foregroundColor': None,
                            'backgroundColor': None,
                            'style': TBFLAGS,

                            'source': None,
                            'object_link': None,
                            'buttonUpdate': True,   # Признак кнопки сохранить
                            'buttonAdd': True,
                            'buttonDel': True,
                            'buttonHelp': False,
                            'buttonPrint': False,
                            'onDelete': None,
                            'onUpdate': None,
                            'onHelp': None,
                            'onPrint': None,
                            'refresh': None,
                            'onAdd': None,

                            '__attr_types__': {icDefInf.EDT_CHECK_BOX: ['buttonUpdate',
                                                                        'buttonAdd',
                                                                        'buttonDel',
                                                                        'buttonHelp',
                                                                        'buttonPrint'],
                                               icDefInf.EDT_USER_PROPERTY: ['object_link'],
                                               },
                            '__parent__': SPC_IC_WIDGET,
                            '__attr_hlp__': {'buttonUpdate': u'Признак кнопки сохранить',
                                             },
                            }

icDatasetNavigatorFont = {'size': 8,
                          'family': 'default',
                          'faceName': 'Tahoma',
                          'style': 'bold'}

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icComboType

#   Имя пользовательского класса
ic_class_name = 'icDatasetNavigator'

#   Описание стилей компонента
ic_class_styles = ictoolbar.ICToolbarStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_DATASET_NAVIGATOR
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtNavigator'
ic_class_pic2 = '@common.imgEdtNavigator'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.icdatasetnavigator.icDatasetNavigator-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 1, 3)


# --- Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('object_link',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('object_link',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('GridDataset', ):
                ic_dlg.icWarningBox(u'ОШИБКА', u'Тип выбранный объект не корректен.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('object_link',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icDatasetNavigator(icWidget, wx.ToolBar):
    """
    Класс реализует панель объектов, которые используются для поиска и навигации
    по таблице данных.
    """

    def __init__(self, parent, id, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None, step=1):
        """
        Конструктор для создания icDatasetNavigator.
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
        @type step: C{int}
        @param step: Шаг изменения курсора.
        """
        util.icSpcDefStruct(SPC_IC_DATASET_NAVIGATOR, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        # Параметры последнего поиска
        self._lastFindPar = None
        self.size = component['size']
        self.pos = component['position']
        self.style = component['style']
        self.ondelete = component['onDelete']
        self.onupdate = component['onUpdate']
        self.onadd = component['onAdd']
        self.onhelp = component['onHelp']
        self.onprint = component['onPrint']
        self.buttonUpdate = component['buttonUpdate']
        self.buttonAdd = component['buttonAdd']
        self.buttonDel = component['buttonDel']
        self.buttonHelp = component['buttonHelp']
        self.buttonPrint = component['buttonPrint']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        self.object_link = None
        objFont = icfont.icFont(icDatasetNavigatorFont)
        
        wx.ToolBar.__init__(self, parent, id, self.pos, self.size,
                            self.style, name=self.name)
        self.SetFont(objFont)
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))
        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        height = 20
        self.SetToolBitmapSize(wx.Size(16, 16))

        self.AddSeparator()
        self.txtCtrl = wx.StaticText(self, wx.NewId(), u'Запись ', size=(40, 12))
        self.txtCtrl.SetFont(objFont)
        self.txtCtrl.SetBackgroundColour(self.GetBackgroundColour())
        
        self.AddControl(self.txtCtrl)
        
        self.id_first = wx.NewId()
        self.AddTool(bitmap=common.imgFirstData, id=self.id_first)
        self.Bind(wx.EVT_TOOL, self.OnFirstData, id=self.id_first)
        
        self.id_prev = wx.NewId()
        self.AddTool(bitmap=common.imgPrevData, id=self.id_prev)
        self.Bind(wx.EVT_TOOL, self.OnPrevData, id=self.id_prev)
        
        self.id_cursor = wx.NewId()
        if self.dataset is not None:
            value = self.dataset.Recno()
        else:
            value = None
            
        self.cursor = wx.TextCtrl(self, self.id_cursor, value=str(value),
                                  size=(50, height-2),
                                  style=wx.SIMPLE_BORDER | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
                 
        self.AddControl(self.cursor)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnteredCursor, id=self.id_cursor)

        try:
            self.id_next = wx.NewId()
            self.AddTool(bitmap=common.imgNextData, id=self.id_next)
            self.Bind(wx.EVT_TOOL, self.OnNextData, id=self.id_next)
            
            self.id_last = wx.NewId()
            self.AddTool(bitmap=common.imgLastData, id=self.id_last)
            self.Bind(wx.EVT_TOOL, self.OnLastData, id=self.id_last)
            
            if self.dataset is not None:
                txt = u' из ' + str(self.dataset.getRecordCount() - 1) + u'      '
            else:
                txt = u'     '
            
            self.datasize = wx.StaticText(self, wx.NewId(), txt, size=(-1, 12))
            self.datasize.SetFont(objFont)
            self.AddControl(self.datasize)
            self.datasize.SetBackgroundColour(self.GetBackgroundColour())
            
            self.newrec = None
            self.delrec = None
            self.update = None
    
            if self.buttonAdd:
                self.id_add = wx.NewId()
                self.AddTool(bitmap=common.imgPlus, id=self.id_add, shortHelpString=u'Добавить')
                self.Bind(wx.EVT_TOOL, self.OnAddData, id=self.id_add)
                
            if self.buttonUpdate:
                self.id_update = wx.NewId()
                self.AddTool(bitmap=common.imgCheck, id=self.id_update, shortHelpString=u'Сохранить')
                self.Bind(wx.EVT_TOOL, self.OnUpdateData, id=self.id_update)
                
            if self.buttonDel:
                self.id_del = wx.NewId()
                self.AddTool(bitmap=common.imgMinus, id=self.id_del, shortHelpString=u'Удалить')
                self.Bind(wx.EVT_TOOL, self.OnDelData, id=self.id_del)
            
            self.AddSeparator()
            
            self.id_text_find = wx.NewId()
            
            self.nv_text_find = wx.SearchCtrl(self, self.id_text_find,
                                              size=(100, height-1),
                                              style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

            self.AddControl(self.nv_text_find)
            self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnteredFind, id=self.id_text_find)
            
            self.AddSeparator()
            
            self.id_search = wx.NewId()
            self.AddTool(bitmap=common.imgSearchData, id=self.id_search, shortHelpString=u'Поиск')
            self.Bind(wx.EVT_TOOL, self.OnSearchData, id=self.id_search)

            self.AddSeparator()

            if self.buttonHelp:
                self.id_help = wx.NewId()
                self.AddTool(bitmap=common.imgHelp, id=self.id_help, shortHelpString=u'Помощь')
                self.Bind(wx.EVT_TOOL, self.OnHelp, id=self.id_help)

            if self.buttonPrint:
                self.id_print = wx.NewId()
                self.AddTool(bitmap=common.imgPrint, id=self.id_print, shortHelpString=u'Печать')
                self.Bind(wx.EVT_TOOL, self.OnPrint, id=self.id_print)
        except:
            pass
        
        self.Realize()
        self.BindICEvt()

    def setDataset(self, dataset):
        self.dataset = dataset

    def setLink(self, object_link):
        """
        Установить связь с объектом грида и источником данных.
        @param object_link: Объект грида.
        """
        self.object_link = object_link
        if self.object_link is None:
            io_prnt.outWarning(u'DatasetNavigator. Object link is <None>')
            return None
        else:
            io_prnt.outLog(u'DatasetNavigator. Object link <%s>' % self.object_link)

        self.dataset = self.object_link.dataset
        self.UpdateViewFromDB()
        return self.object_link

    def get_object_link(self):
        """
        Возвращает связанный объект, обычно грид.
        """
        if self.object_link is None:
            psp = self.getICAttr('object_link')
            io_prnt.outLog(u'DatasetNavigator. Object link passport <%s>' % psp)
            object_link = self.GetKernel().getObjectByPsp(psp)
            self.setLink(object_link)
        return self.object_link
        
    def OnHelp(self, evt):
        """
        Обработка нажатия кнопки <Помощь>.
        """
        #   Заносим в пространство имен параметры функции для последующего использования
        self.evalSpace['evt'] = evt
        #   Выполняем функционал для удаления строки
        if self.onhelp:
            self.eval_attr('onHelp')
        evt.Skip()
        
    def OnPrint(self, evt):
        """
        Обработка нажатия кнопки <Печать отчета>.
        """
        #   Заносим в пространство имен параметры функции для последующего использования
        self.evalSpace['evt'] = evt
        #   Выполняем функционал для удаления строки
        if self.onprint:
            self.eval_attr('onPrint')
        evt.Skip()

    def OnFirstData(self, evt):
        """
        Переход на первую запись таблицы данных.
        """
        if self.dataset is not None:
            self.dataset.Move(0)
            self.cursor.SetValue(str(self.dataset.Recno()))
            self.cursor.Refresh()
            self.datasize.SetLabel(u' из ' + str(self.dataset.getRecordCount() - 1) + u'    ')
            self.datasize.Refresh()

            # --- Навигация по гриду
            object_link = self.get_object_link()
            if object_link:
                object_link.moveCursorFirst()
            self.UpdateViewFromDB()

    def OnPrevData(self, evt):
        """
        Переход на предыдущую запись таблицы данных.
        """
        if self.dataset is not None:
            self.dataset.Skip(-1)
            self.cursor.SetValue(str(self.dataset.Recno()))
            self.cursor.Refresh()
            self.datasize.SetLabel(u' из ' + str(self.dataset.getRecordCount() - 1) + u'    ')
            self.datasize.Refresh()

            # --- Навигация по гриду
            object_link = self.get_object_link()
            if object_link:
                object_link.moveCursorPrev()
                self.UpdateViewFromDB()

    def OnNextData(self, evt):
        """
        Переход на следующую запись таблицы данных.
        """
        if self.dataset is not None:
            self.dataset.Skip()
            self.cursor.SetValue(str(self.dataset.Recno()))
            self.cursor.Refresh()
            self.datasize.SetLabel(u' из ' + str(self.dataset.getRecordCount() - 1) + u'    ')
            self.datasize.Refresh()

            # --- Навигация по гриду
            object_link = self.get_object_link()
            if object_link:
                object_link.moveCursorNext()
                self.UpdateViewFromDB()

    def OnLastData(self, evt):
        """
        Переход на последнюю запись таблицы данных.
        """
        if self.dataset is not None:
            self.dataset.Move(-1)
            self.cursor.SetValue(str(self.dataset.Recno()))
            self.cursor.Refresh()
            self.datasize.SetLabel(u' из ' + str(self.dataset.getRecordCount() - 1) + u'    ')
            self.datasize.Refresh()

            # --- Навигация по гриду
            object_link = self.get_object_link()
            if object_link:
                object_link.moveCursorLast()
                self.UpdateViewFromDB()

    def OnAddData(self, evt):
        """
        Добавить новую запись в таблицу данных.
        """
        self.cursor.Refresh()
        if self.dataset is not None:
            #   Заносим в пространство имен параметры функции для последующего использования
            self.evalSpace['self'] = self
            self.evalSpace['evt'] = evt
            bRet = 1
            #   Выполняем функционал для удаления строки
            if self.onadd not in [None, '', 'None']:
                res, val = self.eval_attr('onAdd')
                if res:
                    try:
                        bRet = int(val)
                    except:
                        bRet = 1
            if bRet:
                object_link = self.get_object_link()
                if object_link is not None:
                    try:
                        object_link.AddRows()
                    except:
                        io_prnt.outWarning(u'Can\'t add row to the link object: <%s>' % object_link)
                else:
                    for key in self.evalSpace['_has_source'].keys():
                        try:
                            if key != self.name and self.dataset == self.evalSpace['_has_source'][key].dataset:
                                self.evalSpace['_has_source'][key].AddRows()
                                break
                        except:
                            io_prnt.outWarning(u'DatasetNavigator Add rows <%s>' % key)

                self.datasize.SetLabel(u' из ' + str(self.dataset.getRecordCount() - 1) + u'    ')
                self.datasize.Refresh()
                self.UpdateViewFromDB()

    def OnUpdateData(self, evt):
        """
        Сообщает другим компонентам формы о том, что данные изменились.
        """
        self.cursor.Refresh()
        if self.dataset is not None:
            #   Заносим в пространство имен параметры функции для последующего использования
            self.evalSpace['self'] = self
            self.evalSpace['evt'] = evt
            bRet = 1
            #   Выполняем функционал для обновления данных
            if self.onupdate not in [None, '']:
                res, val = self.eval_attr('onUpdate')
                if res:
                    try:
                        bRet = int(val)
                    except:
                        bRet = 1
            if bRet:
                #   Инициируем обновление данных
                self.dataset.update()
                for key in self.evalSpace['_has_source'].keys():
                    try:
                        if key != self.name:
                            self.evalSpace['_has_source'][key].UpdateDataRecord()
                    except:
                        pass

    def OnDelData(self, evt):
        """
        Удалить запись из таблицы данных.
        """
        self.cursor.Refresh()
        if self.dataset is not None:
            cur = self.dataset.Recno()
            #   Заносим в пространство имен параметры функции для последующего использования
            self.evalSpace['evt'] = evt
            self.evalSpace['row'] = cur
            bRet = 1
            #   Выполняем функционал для удаления строки
            if not self.ondelete in [None, '']:
                res, val = self.eval_attr('onDelete')
                if res:
                    try:
                        bRet = int(val)
                    except:
                        bRet = 1
            if bRet:
                object_link = self.get_object_link()
                if object_link is not None:
                    try:
                        object_link.DelRows(cur)
                    except:
                        io_prnt.outWarning(_('Can\'t delete row from the link object: <%s>') % object_link)
                else:
                    for key in self.evalSpace['_has_source'].keys():
                        try:
                            if key != self.name and self.dataset == self.evalSpace['_has_source'][key].dataset:
                                self.evalSpace['_has_source'][key].DelRows(cur)
                                break
                        except: 
                            pass
                self.datasize.SetLabel(u' из ' + str(self.dataset.getRecordCount() - 1) + u'    ')
                self.datasize.Refresh()
                self.UpdateViewFromDB()

    def OnSearchData(self, evt):
        """
        Ищет поле удовлетворяющее запросу и устанавливает курсор на эту
        запись.
        """
        if self.dataset is not None:
            try:
                val = self.nv_text_find.GetValue()
                rec = self.dataset.Recno()
                #   Сообщение о том, что ведется поиск
                self.datasize.SetLabel(u' Поиск... ')
                self.datasize.Refresh()
                #   Определяем поле, по которому будем искать значение
                objs = self.evalSpace['_has_source'].values()
                flt = [x for x in objs if x.source == self.source and x.type == 'GridDataset']
                fld = None
                bVirtual = False
                if flt:
                    col = flt[0].GetGridCursorCol()
                    rec = flt[0].GetGridCursorRow()
                    fields = [flt[0].GetTable().colNames[col]]
                    if flt[0].GetTable().exCols[col]['attr'] in ['C', 'CR']:
                        bVirtual = True
                else:
                    flt = [x for x in objs if x.source == self.source and x.type == 'ListDataset']
                    if flt:
                        fields = [flt[0].colNames[0]]
                        rec = -1
                        if flt[0].exCols[0]['attr'] in ['C', 'CR']:
                            bVirtual = True
                    else:
                        fields = None
                                
                io_prnt.outLog(u'__# FIELDS IN SEARCH: %s' % fields)

                #   Если определено поле
                if fields:
                    #   Если прошлый раз поиск по данному полю не удался, то поиск
                    #   ведем с первой записи
                    if self._lastFindPar and not self._lastFindPar[0] and self._lastFindPar[1] == fields[0]:
                        rec = 0

                    if self.dataset.dataclass is not None and not bVirtual:
                        if val and val[0] != '%' and val[-1] != '%':
                            val = '%'+val.strip()+'%'
                        fld, cur = self.dataset.FindRowString(val, rec, fields)
                    else:
                        fld, cur = self.FindRowString(flt[0], val, rec, fields)

                    self._lastFindPar = (fld, fields[0], cur)
                
                if fld is not None:
                    self.dataset.Move(cur)
                    self.cursor.SetValue(str(self.dataset.Recno()))
                    self.UpdateViewFromDB()
                    
                self.cursor.Refresh()
                self.nv_text_find.Refresh()
                self.datasize.SetLabel(u' из ' + str(self.dataset.getRecordCount() - 1) + u'    ')
                self.datasize.Refresh()
            except:
                io_prnt.outErr(u'Error in search')
    
    def OnTextEnteredCursor(self, evt):
        """
        Отлавливает сообщение EVT_ENTER от поля со значением положения
        курсора и устанавливает курсор в нужную позицию.
        """
        if self.dataset is not None:
            try:
                cur = int(self.cursor.GetValue())
                self.dataset.Move(cur)
                self.cursor.SetValue(str(self.dataset.Recno()))
                self.cursor.Refresh()
                self.UpdateViewFromDB()
            except:
                pass
        
        evt.Skip()
        
    def OnTextEnteredFind(self, evt):
        """
        Обрабатывает нажатия кнопки <поиск> - ищет поле, удовлетворяющее
        запросу и устанавливает курсор в эту позицию.
        """
        self.OnSearchData(evt)
        evt.Skip()
    
    def UpdateViewFromDB(self, db_name=None):
        """
        Обновляет данные в текстовом поле после изменения курсора в
        источнике данных.
        @type db_name: C{String}
        @param db_name: Имя источника данных.
        """
        #   Если класс данных не задан, то считаем, что объект необходимо обновить
        if db_name is None:
            db_name = self.dataset.name

        if self.dataset is not None and self.dataset.name == db_name and self.bStatusVisible:
            rec = self.dataset.Recno()
            self.cursor.SetValue(str(rec))
            self.cursor.Refresh()
            self.datasize.SetLabel(u' из ' + str(self.dataset.getRecordCount() - 1) + u'    ')
            self.datasize.Refresh()

            if rec == 0:
                self.EnableTool(self.id_first, False)
                self.EnableTool(self.id_prev, False)
                self.EnableTool(self.id_last, True)
                self.EnableTool(self.id_next, True)
            elif rec >= self.dataset.getRecordCount()-1:
                self.EnableTool(self.id_first, True)
                self.EnableTool(self.id_prev, True)
                self.EnableTool(self.id_last, False)
                self.EnableTool(self.id_next, False)
            else:
                self.EnableTool(self.id_first, True)
                self.EnableTool(self.id_prev, True)
                self.EnableTool(self.id_last, True)
                self.EnableTool(self.id_next, True)
        
    def FindRowString(self, obj, string, cursor, fields):
        """
        Функция ищет строку в массиве данных.
        @type data: C{icDataset}
        @param data: Объект доступа к источнику данных
        @type string: C{string}
        @param string: Строка поиска
        @type cur: C{int}
        @param cur: Начальное положение курсора.
        @type fields: C{dictionary}
        @param fields: Список полей по которым ведется поиск.
        @rtype: C{tuple}
        @return: Возвращает номер строку и название поля, где найдена искомая строка.
        """
        io_prnt.outLog(u'>>> FindRowString : fields=%s' % fields)
        if not string or not obj:
            return None, cursor

        string = str(string)
        bFirst = bLast = False
        #   Ищем специальные символы
        if string[0] == '%':
            bFirst = True
        elif string[-1] == '%' and len(string) > 1:
            bLast = True

        string = string.replace('%', '')
        if not string:
            return None, cursor

        cursor += 1
        if obj.type == 'GridDataset':
            rows = obj.GetNumberRows()-1
        elif obj.type == 'ListDataset':
            rows = obj.GetDataRows()

        for cur in xrange(cursor, rows):
            for fld in fields:
                value = obj.getNameValue(fld, cur)
                if bLast and value.find(string) == 0:
                    return fld, cur
                elif bFirst and value[-len(string):] == string:
                    return fld, cur
                elif not bLast and not bFirst and value.find(string) >= 0:
                    return fld, cur

        return None, 0


def test(par=0):
    """
    Тестируем класс Навигатор.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icDatasetNavigator Test')
    toolBar = icDatasetNavigator(frame, -1,
                                 {'keyDown': 'print(\'keyDown in navigator\')'})
    frame.SetToolBar(toolBar)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
