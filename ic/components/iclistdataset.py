#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Многоколоночный список для просмотра табличных данных.
Содержит класс для создания многоколоночного списка табличных данных.

@type SPC_IC_LIST_DATASET: C{Dictionary}
@var SPC_IC_LIST_DATASET: Спецификация на ресурсное описание аттрибутов ячеек данных.
Описание ключей SPC_IC_LIST_DATASET:

    - B{type='ListDataset'}: Тип компонента.
    - B{name='ListDataset'}: Имя компонента.
    - B{style=wx.SIMPLE_BORDER | wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES |wx.LC_VRULES}: Стиль окна (стили wx.Window + wx.ListCtrl).
    - B{font={}}: Шрифт.
    - B{position=(-1, -1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размеры компонента.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{indxFldFind=None}: Индекс поля поиска.
    - B{selected=None}:  Выражение, выполняемое после установки фокуса на новую строку.
    - B{activated=None}: Выражение, выполняемое после выбора строки.
    - B{keyDown=None}: Выражение, выполняемое после нажатия клавиши.
    - B{getattr=None}:Выражение, выполняемое при запросе на аттрибут строки списка.
    - B{source=None}: Описание или ссылка на источник данных.
    - B{cols=None}: Описание колонок листа - такое же как и у грида.
    - B{refresh=None}: Выражение, возвращающее список обновляемых компонентов. Под обновлением понимается обновление
        представлений компонентов (для вычисляемых полей это соответствует вычислению выражения аттрибута 'getvalue').
        Если атрибут равен None, то обновляются все объекты работающие с классами данных.
    - B{recount=None}: Выражение, возвращающее список пересчитываемых компонентов. Под этим понимается пересчет
        значений хранимых в базе данных. Стадии пересчета вычисляемого поля:
            - вычисление представления поля (по атрибуту 'getvalue')
            - отрабатывает контроль значения поля(по атрибуту 'ctrl')
            - Если контроль проходит запись в базу вычисленного значения (по атрибуту 'setvalue')
            - обновление представления поля (по атрибуту 'getvalue')

@type ICListStyle: C{dictionary}
@var ICListStyle: Словарь специальных стилей компонента. Описание ключей ICListStyle:

    - C{wx.LC_LIST}:  Могоколоночный список, с обычными иконками. Ширина колонок вычисляются
        автоматически если не указан стиль wx.LC_REPORT.
    - C{wx.LC_REPORT}:  Одно или многоколоночный список с обычным заголовком.
    - C{wx.LC_VIRTUAL}:  Виртуальный компонент, используется только с wx.LC_REPORT.
    - C{wx.LC_ICON}:  Большие иконки с обычными надписями.
    - C{wx.LC_SMALL_ICON}:  Маленькие иконки с обычными надписями.
    - C{wx.LC_ALIGN_TOP}:  Иконки выравниваются по верхней границе. Ставится по умолчанию, Используется только под Win32.
    - C{wx.LC_ALIGN_LEFT}:  Иконки выравниваются по левому краю.
    - C{wx.LC_AUTOARRANGE}:  Иконки сами выравниваются. Только по Win32.
    - C{wx.LC_EDIT_LABELS}:  Значения редактируемые: приложение будет определять, когда начинать редактирование.
    - C{wx.LC_NO_HEADER}:  Без заголовков колонок. Только под Win32.
    - C{wx.LC_SINGLE_SEL}:  Выбрать можно только одну строку списка.
    - C{wx.LC_SORT_ASCENDING}:  Сортировка по возрастанию.
    - C{wx.LC_SORT_DESCENDING}:  Сортировка по убыванию.
    - C{wx.LC_HRULES}:  Прорисовка горизонтальных границ строки с wx.LC_REPORT.
    - C{wx.LC_VRULES}:   Прорисовка вертикальных границ строки с wx.LC_REPORT.
"""

import wx
from ic.dlg.msgbox import MsgBox
import ic.utils.util as util
from ic.utils.coderror import *
from . import icwidget
import os, copy
from .icgriddataset import defColDBDescription
from .icgrid import *
from .icfont import icFont, SPC_IC_FONT
from ic.log.iclog import *
from .icFieldTempl import *
import ic.db.icsimpledataset as icsimpledataset
from ic.kernel import io_prnt
import ic.PropertyEditor.icDefInf as icDefInf

_ = wx.GetTranslation

ICListStyle = {'LC_LIST': wx.LC_LIST,
               'LC_REPORT': wx.LC_REPORT,
               'LC_VIRTUAL': wx.LC_VIRTUAL,
               'LC_ICON': wx.LC_ICON,
               'LC_SMALL_ICON': wx.LC_SMALL_ICON,
               'LC_ALIGN_TOP': wx.LC_ALIGN_TOP,
               'LC_ALIGN_LEFT': wx.LC_ALIGN_LEFT,
               'LC_AUTOARRANGE': wx.LC_AUTOARRANGE,
               'LC_EDIT_LABELS': wx.LC_EDIT_LABELS,
               'LC_NO_HEADER': wx.LC_NO_HEADER,
               'LC_SINGLE_SEL': wx.LC_SINGLE_SEL,
               'LC_SORT_ASCENDING': wx.LC_SORT_ASCENDING,
               'LC_SORT_DESCENDING': wx.LC_SORT_DESCENDING,
               'LC_HRULES': wx.LC_HRULES,
               'LC_VRULES': wx.LC_VRULES}

SPC_IC_LIST_DATASET = {'type': 'ListDataset',
                       'name': 'ListDataset',
                       'style': wx.SIMPLE_BORDER | wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES,

                       'font': {},
                       'position': (-1, -1),
                       'size': (-1, -1),
                       'foregroundColor': None,
                       'backgroundColor': None,
                       'indxFldFind': 0,
                       'getattr': None,
                       'selected': None,
                       'activated': None,
                       'keyDown': None,
                       'source': None,
                       'refresh': None,
                       'recount': [],
                       'cols': [],

                       '__events__': {'selected': ('wx.EVT_LIST_ITEM_SELECTED', 'OnItemSelected', False),
                                      'activated': ('wx.EVT_LIST_ITEM_ACTIVATED', 'OnItemActivated', False),
                                      },
                       '__attr_types__': {icDefInf.EDT_NUMBER: ['indxFldFind'],
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
ic_class_name = 'icListDataset'

#   Описание стилей компонента
ic_class_styles = ICListStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_LIST_DATASET
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtListDataset'
ic_class_pic2 = '@common.imgEdtListDataset'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.iclistdataset.icListDataset-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['GridCell', 'DataLink']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

__version__ = (1, 0, 0, 8)


class icListDataset(icwidget.icWidget, wx.ListCtrl):
    """
    Объект не редактируемой таблицы данных.
    """

    def RefreshData(self, data=None):
        """
        Функция обновляет данные в таблице.
        """
        self.ClearAll()
        self.colLabels = []
        self.colNames = []
        self.exCols = []
        self.retInfo = [0, []]
        i = 0
        #   Определяем подписи и типы колонок
        for col in self.cols:
            bShow = True
            try:
                attr_show = '@' + col['show']
                bShow = util.getICAttr(attr_show, self.evalSpace,
                                       'Error in getICAttr in iclistdataset <show>=%s' % col['show'])
            except:
                pass
            
            if col['attr'] != 'UV' and bShow:
                self.colNames.append(col['name'])
                self.colLabels.append(col['label'])
                self.exCols.append(col)
                self.InsertColumn(i, col['label'])
                if 'width' in col:
                    try:
                        self.SetColumnWidth(i, col['width'])
                    except:
                        pass

                i += 1

        #   Получаем курсор на источник данных
        if self.dataset is None:
            log.debug(u'icListDataset RefreshData: %s Source: <%s>' % (data, self.source))
            #   Если источник данных прописан
            if self.source:
                MsgBox(self.grid,
                       _('icListDataset: Data source %s is not defined in the object context.') % self.link_res)
            #   В обратном случае используем стандартный icSimpleDataset
            else:
                self.dataset = icsimpledataset.icSimpleDataset(icwidget.icNewId(),
                                                               {'description': self.exCols})
        elif data and not self.source:
            self.dataset.SetDataBuff(data)
            
        #   Обновляем данные в буффере
        try:
            self.dataset.Refresh()
        except:
            msg = _('Refrsh data error. <dataset=%s>') % self.dataset.name
            MsgBox(None, msg)

        #   Определяем количество строк
        self.SetItemCount(self.dataset.getRecordCount())
        self.Refresh()

    def __init__(self, parent, id, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None, dataset = None):
        """
        Конструктор для создания icListDataset - многоколоночный список для
        просмотра табличных данных.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонент.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type dataset: C{icDataset}
        @param dataset Объект данных.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(SPC_IC_LIST_DATASET, component)
        util.icSpcDefStruct(SPC_IC_FONT, component['font'])
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)
        self.currentItem = -1
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        pos = component['position']
        size = component['size']
        style = component['style']
        font = component['font']
        self.source = component['source']
        self.cols = copy.deepcopy([x for x in component['cols'] if util.isAcivateRes(x, evalSpace)
                                         and x['type'] == 'GridCell'])
        self.selected = component['selected']
        self.activated = component['activated']
        #   Атрибут содержит буфер текщей строки
        self.rowDict = {}
        style = style | wx.LC_REPORT | wx.CLIP_SIBLINGS
        wx.ListCtrl.__init__(self, parent, id, pos, size, style=style)
        
        #   Дополняем до спецификации описание колонок и создаем колонки
        i = 0
        for col in self.cols:
            #   Заменяем все имена колонок на алиасы
            if 'alias' in col and col['alias'] not in [None, '', 'None']:
                col['name'] = col['alias']

            util.icSpcDefStruct(SPC_IC_CELL, col)
            util.icSpcDefStruct(SPC_IC_CELLATTR, col['cell_attr'])
            
        self.RefreshData()
        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.SetFont(icFont(font))
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, id=self.GetId())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, id=self.GetId())
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, id=self.GetId())
        
        #####
        self.Bind(wx.EVT_COMMAND_LEFT_CLICK, self.OnCommandLeftClick, id=self.GetId())
        self.BindICEvt()

        self.SetFocus()
        self.SetCursor(0)
        
    def OnCommandLeftClick(self, evt):
        """
        Обрабатываем сообщение <EVT_COMMAND_LEFT_CLICK>.
        """
        try:
            self.OnLeftUp()
        except:
            pass
        
        evt.Skip()
        
    def OnColClick(self, evt):
        """
        Обрабатываем сообщение <EVT_LIST_COL_CLICK>.
        """
        if self.dataset is not None:
            #   Определяем колонку
            col = evt.GetColumn()
            fld = self.colNames[col]
            #   Проверяем есть ли по данной колонке индексное выражение либо
            #   выражение для сортировки (атрибут 'sort')
            if (self.exCols[col]['sort'] not in [None, 0, '0', 'None']) or self.dataset.isFieldIndexed(fld):
                self.dataset._sortExprList = [fld]
                if self.dataset._isSortDESC:
                    self.dataset._isSortDESC = False
                else:
                    self.dataset._isSortDESC = True
                    
                self.dataset.FilterData()
                self.Refresh()

        evt.Skip()
        
    def OnItemSelected(self, evt):
        """
        Обрабатываем сообщение о выборе строки списка.
        """
        self.SetFocus()
        evt.Skip()
        result = True
        self.currentItem = evt.m_itemIndex
        #   Формируем пространство имен
        self.evalSpace['evt'] = evt
        self.evalSpace['row'] = self.currentItem

        #   Уведомляем другие компоненты формы о том, что положение курсора изменилось
        if self.dataset is not None:
            row = evt.GetIndex()
            self.dataset.Move(row)
            self.UpdateRelObj()
        
        try:
            self.rowDict.update(self.dataset.getDict(self.currentItem, True))
        except:
            LogLastError(u'OnItemSelected ERROR:')
            self.rowDict = {}
        
        self.evalSpace['values'] = self.rowDict
        self.evalSpace['_lfp'] = {'func': 'OnItemSelected',
                                  'evt': evt,
                                  'currentItem': self.currentItem,
                                  'row': self.currentItem,
                                  'self': self}
        
        if self.selected not in [None, '', 'None']:
            ret, val = self.eval_attr('selected')
            if ret:
                result = bool(val)

    def OnItemActivated(self, evt):
        """
        Активация (Enter/DobleClick) строки.
        """
        currentItem = evt.m_itemIndex
        rowData = []
        #   Формируем пространство имен
        self.evalSpace['evt'] = evt
        self.evalSpace['row'] = currentItem
        try:
            self.rowDict.update(self.dataset.getDict(currentItem, True))
        except:
            io_prnt.outErr(u'OnItemActivated ERROR:')
            self.rowDict = {}
        
        self.evalSpace['values'] = self.rowDict
        self.evalSpace['_lfp'] = {'func': 'OnItemActivated',
                                  'evt': evt,
                                  'currentItem': currentItem,
                                  'result': self.rowDict,
                                  'self': self}
        self.eval_attr('activated')
        evt.Skip()
   
    def getColumnText(self, index, col):
        """
        Возвращает заголовк колонки.
        """
        item = self.GetItem(index, col)
        return item.GetText()

    def getNameValue(self, col_name, row=None):
        """
        Функция возвращает значение ячейки по номеру строки и имени поля.
        @param col_name: Имя колонки.
        @type col_name: C{int}
        @param row: Номер стоки. Если номер строки не задан, то значение берется 
            из текущей строки.
        @type row: C{int}
        @return: Возвращает значение ячейки.
        """
        if row is None:
            row = self.currentItem
            
        col = self.colNames.index(col_name)
        value = None
        
        if col >= 0 and row >= 0:
            value = self.OnGetItemText(row, col)
            
        return value

    # ---------------------------------------------------
    # These methods are callbacks for implementing the
    # 'virtualness' of the list...
    def OnGetItemText(self, item, col):
        """
        Определяет текст определенной ячейки.
        @type item: C{int}
        @param item: Номер строки.
        @type col:  C{int}
        @param col: Номер колонки.
        @rtype: C{string}
        @return: Текст нужной ячейки.
        """
        try:
            fld = self.colNames[col]
            value = self.dataset.getNameValue(fld, item)
            #   Если определен аттрибут getvalue колoнки, то пытаемся по нему вычислить значение ячейки
            self.evalSpace['value'] = value
            if (self.exCols[col]['getvalue'] not in [None, '', 'None']) and self.exCols[col]['attr'] in ['C', 'CR']:
                keyExpr = self.GetUUIDAttr('getvalue', fld)
                res, val = util.ic_eval(self.exCols[col]['getvalue'],
                                        0, self.evalSpace,
                                        'Exception icListDataset.OnGetItemText()',
                                        compileKey=keyExpr)
                if res:
                    value = val
            
            templ = self.exCols[col]['pic']
            try:
                value, point = setTempl(templ, value, -1)
            except Exception:
                io_prnt.outErr(u'>> setTempl Error in OnGetItemText col=%d pic=%s' % (col, templ))

        except IndexError:
            io_prnt.outErr(u'>> Key Error in OnGetItemText col=%d pic=%s' % (col, templ))
            value = ''

        return value

    def OnGetItemImage(self, item):
        return 0

    def OnGetItemAttr(self, item):
        return None

    def GetDataset(self):
        """
        Возвращает объект данных.
        """
        return self.dataset

    def GetDataRows(self):
        """
        Определяет количество сток в данных.
        """
        return self.dataset.getRecordCount()
        
    def SetCursor(self, row, col=-1):
        """
        Устанавливает курсор в нужную позицию.
        @type row: C{int}
        @param row: Номер записи.
        @type col: C{int}
        @param col: Номер колонки. Параметр введен для совместимости с 
            аналогичной функции грида.
        """
        if self.currentItem >= 0:
            self.Select(self.currentItem, 0)

        if row < 0:
            row = 0

        if row >= self.GetItemCount():
            row = self.GetItemCount() - 1

        self.Select(row, 1)
        self.Focus(row)
        
    def UpdateViewFromDB(self, db_name=None):
        """
        Обновляет данные в текстовом поле после изменения курсора в
        источнике данных.
        @type link_key: C{String}
        @param link_key: Имя источника данных.
        """
        #   Если класс данных не задан, то считаем, что объект необходимо обновить
        if db_name is None:
            db_name = self.dataset.name

        if self.dataset is not None and self.dataset.name == db_name and self.bStatusVisible:
            self.SetCursor(self.dataset.Recno())
            
    def SetFilter(self, clsName, flt=None, isUpdSelf=False):
        """
        Устанавливаем фильтр на нужный объект данных.
        @type clsName: C{string}
        @param clsName: Имя класса данных на который устанавливается фильтр.
        @type filter: C{string | dictionary}
        @param filter: Фильтр, накладываемый на класс данных.
        @type isUpdSelf: C{bool}
        @param isUpdSelf: Признак того, что необходимо обновлять и состояние
            текущего объекта.
        """
        try:
            dataset = self.evalSpace['_sources'][clsName]
            real_name = dataset.name
            #   Если буфер заполнен, то необходимо запросить потверждение на
            #   обновление данных и обновить данные. В противном случае изменения
            #   будут потеряны
            if not dataset.IsEOF() and dataset.isChangeRowBuff() and MsgBox(None, 
                                                                            _('Save changes?'),
                                                                            style=wx.YES_NO | wx.ICON_QUESTION) == wx.ID_YES:
                dataset.update()

            if flt:
                dataset.FilterFields(flt)
            
            #   Уведомляем другие компоненты формы о том, что состояние объекта данных могло измениться
            for key in self.evalSpace['_has_source'].keys():
                try:
                    if key != self.name or isUpdSelf:
                        self.evalSpace['_has_source'][key].UpdateViewFromDB(real_name)
                        #   Обновляем связанные гриды
                        self.evalSpace['_has_source'][key].UpdateDataView(real_name)
                except:
                    pass
        except KeyError:
            MsgBox(None, _('Dataclass %s is not defined in context.') % clsName)
        except:
            io_prnt.outErr(u'Error in ic.components.iclistdataset.setFilter')
    
    def SetFilterField(self, clsName, fieldName, row):
        """
        Устанавливаем фильтр на объект группы (связь один ко многим).
        @type clsName: C{string}
        @param clsName:  Имя класса данных, который фильтруется
        @type fieldName: C{string}
        @param fieldName: Поле в классе данных, по которому фильтруем.
        @type row: C{int}
        @param row: Текущий номер строки в списке. Будут отобраны те строки класса данных, значения полей <fieldName> которых,
            будут соответствовать идентификатору текущей записи.
        """
        try:
            dataset = self.evalSpace['_sources'][clsName]
            #   Если буфер заполнен, то необходимо запросить потверждение на
            #   обновление данных и обновить данные. В противном случае изменения
            #   будут потеряны
            if dataset.isChangeRowBuff() and MsgBox(None, _('Save changes?'),
                                                    style=wx.YES_NO | wx.ICON_QUESTION) == wx.ID_YES:
                dataset.update()
            
            id = self.dataset.getId(row, True)
            dataset.FilterField(fieldName, id)
       
            #   Уведомляем другие компоненты формы о том, что состояние объекта данных могло измениться
            for key in self.evalSpace['_has_source'].keys():
                try:
                    if key != self.name:
                        self.evalSpace['_has_source'][key].UpdateViewFromDB(clsName)
                        #   Обновляем связанные гриды
                        self.evalSpace['_has_source'][key].UpdateDataView(clsName)
                except:
                    pass
        except KeyError:
            MsgBox(None, _('Dataclass %s is not defined in context.') % clsName)
        except:
            io_prnt.outErr(u'Error in ic.components.iclistdataset.SetFilterField')
            
if __name__ == '__main__':
    pass
