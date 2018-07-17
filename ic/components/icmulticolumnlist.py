#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Описание класса многоколоночного списока.
Содержит описание класса icMultiColumnList для создания многоколоночноко списка.

@type SPC_IC_MCLIST: C{dictionary}
@var SPC_IC_MCLIST: Спецификация на ресурсное описание панели инструментов. Описание ключей SPC_IC_MCLIST:

    - B{type='MultiColumnList'}: Тип компонента.
    - B{name='default'}: Имя компонента.
    - B{fileds=[]}. Имена полей базы данных, которые отображает компонент.
    - B{style=wx.LC_HRULES | wx.LC_VRULES}: Стиль окна (стили wx.Window + wx.ListCtrl).
    - B{font={}}: Шрифт.
    - B{position=(-1, -1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размеры компонента.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{selected=None}:  Выражение, выполняемое после установки фокуса на новую строку.
    - B{activated=None}: Выражение, выполняемое после выбора строки.
    - B{keyDown=None}: Выражение, выполняемое после нажатия клавиши.
    - B{items=[]}: Список названий колонок.
    - B{col_width=[]}: Размеры колонок.
    - B{source=None}: Описание или ссылка на источник данных.
"""

import wx
from ic.log.iclog import *
from .icFieldTempl import *
import ic.utils.util as util
from .icwidget import icWidget, SPC_IC_WIDGET
import ic.PropertyEditor.icDefInf as icDefInf
from ic.kernel import io_prnt
import ic.PropertyEditor.icDefInf as icDefInf

_ = wx.GetTranslation

SPC_IC_MCLIST = {'type': 'MultiColumnList',
                 'name': 'default',

                 'style': wx.LC_HRULES | wx.LC_VRULES,
                 'position': (-1, -1),
                 'size': (-1, -1),
                 'font': {},
                 'foregroundColor': (0, 0, 0),
                 'backgroundColor': (255, 255, 255),
                 'selected': None,     # Выражение, выполняемое после установки фокуса на новую строку
                 'activated': None,    # Выражение, выполняемое после выбора строки
                 'keyDown': None,
                 'source': None,
                 'fields': [],
                 'items': [],
                 'col_width': [],

                 '__attr_types__': {icDefInf.EDT_TEXTLIST: ['items', 'fields', 'col_width'],
                                    },
                 '__events__': {'selected': ('wx.EVT_LIST_ITEM_SELECTED', 'OnItemSelected', True),
                                'activated': ('wx.EVT_LIST_ITEM_ACTIVATED', 'OnItemActivated', True),
                                },
                 '__parent__': SPC_IC_WIDGET,
                 '__attr_hlp__': {'selected': u'Выражение, выполняемое после установки фокуса на новую строку',
                                  'activated': u'Выражение, выполняемое после выбора строки',
                                  },
                 }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icMultiColumnList'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': wx.LC_HRULES | wx.LC_VRULES}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_MCLIST
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMCList'
ic_class_pic2 = '@common.imgEdtMCList'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.icmulticolumnlist.icMultiColumnList-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 4)


class icMultiColumnList(icWidget, wx.ListCtrl):
    """
    Класс icMulticolumnList реализует интерфейс для обработки многоколоночного
    списка как обкладку над компонентом wx.ListCtrl.
    """

    def __init__(self, parent, id, component={}, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания MultiColumnList.
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
        util.icSpcDefStruct(SPC_IC_MCLIST, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        items = component['items']
        flds = component['fields']
        col_width = component['col_width']
        pos = component['position']
        size = component['size']
        style = component['style']
        self.selected = component['selected']
        self.activated = component['activated']
        self.keydown = component['keyDown']
        
        style = style | wx.LC_REPORT | wx.CLIP_SIBLINGS
        wx.ListCtrl.__init__(self, parent, id, pos, size, style=style)

        self.currentItem = -1
        col = 0
        #   Заполняем список
        if flds is not None:
            for x in flds:
                self.InsertColumn(col, x)
                # Установить ширину колонки
                try:
                    self.SetColumnWidth(col, col_width[col])
                except IndexError:
                    pass
                col += 1

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, id=self.GetId())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, id=self.GetId())
        self.BindICEvt()

    def appendStringRec(self, *StringRec_):
        """
        Добавить запись строк.
        @param StringRec_: Запись из строк.
        @return: Возвращает индекс добавленной записи.
        """
        index = 0
        for i_string in range(len(StringRec_)):
            cell_str = StringRec_[i_string]
            if i_string:
                self.SetStringItem(index, i_string, str(cell_str))
            else:
                index = self.InsertStringItem(sys.maxint, str(cell_str))
        return index

    def getStringsByCol(self, *Columns_):
        """
        Получить список строк по коолнкам.
        @param Columns_: Номера колонок.
        @return: Список кортежей строк, если задано несколько колонок.
            Список строк,  если задана одна колонка.
            None в случае ошибки.
        """
        try:
            is_one_col = bool(len(Columns_) == 1)
            rec_count = self.GetItemCount()
            ret_strings = []
            for i_rec in range(rec_count):
                if is_one_col:
                    # Обработка одной колонки
                    string = self.GetItem(i_rec, Columns_[0]).GetText()
                    ret_strings.append(string)
                else:
                    # Обработка нескольких колонок
                    rec = [self.GetItem(i_rec, col).GetText() for col in Columns_]
                    ret_strings.append(tuple(rec))
            return ret_strings
        except:
            io_prnt.outErr(u'MULTICOLUMNLIST getStringsByCol ERROR')
            return None

    def moveStringRec(self, Index_=-1, Step_=1):
        """
        Передвинуть запись в списке.
        @param Index_: Номер записи. Если -1, то имеется в виду текущая.
        @param Step_: На сколько позиций передвинуть. 
            Если <0, то движение к началу.
            Если >0, то движение к концу.
        @return: True - если движение произошло.
            False - если движение не произошло.
            None в случае ошибки.
        """
        try:
            if Index_ < 0:
                Index_ = self.currentItem
                if Index_ < 0:
                    return False
            # Вычислить новое положение строки
            new_idx = min(self.GetItemCount()-1, max(0, Index_+Step_+int(Step_ > 0)))
            # Количество колонок
            col_count = self.GetColumnCount()
            # Список записи
            rec = [self.GetItem(Index_, col).GetText() for col in range(col_count)]
            # Вставить
            new_idx = self.InsertStringItem(new_idx, rec[0])
            for i_col in range(1, len(rec[1:])):
                col_str = rec[i_col]
                self.SetStringItem(new_idx, i_col, col_str)

            del_idx = Index_+int(Step_ < 0)
            # Выделить строку
            self.selectRec(del_idx, False)
            self.focusRec(new_idx)
            self.selectRec(new_idx)
            
            # Удалить старую запись
            self.DeleteItem(del_idx)
            return True
        except:
            io_prnt.outErr(u'MULTICOLUMNLIST moveStringRec ERROR')
            return None
        
    def focusRec(self, Index_):
        """
        Переместить фокус/выделение строки/записи.
        @param Index_: Номер записи.
        """
        Index_ = min(self.GetItemCount()-1, max(0, Index_))
        self.currentItem = Index_
        self.evalSpace['evt'] = None
        self.evalSpace[self.name+'_currentItem'] = self.currentItem
        self.eval_attr('selected')
        self.Focus(Index_)
        
    def selectRec(self, Index_, SelectOn_=True):
        """
        Выделить строку/запись с индексом.
        @param Index_: Номер записи.
        @param SelectOn_: Вкл/Выкл выделение.
        """
        Index_ = min(self.GetItemCount()-1, max(0, Index_))
        return self.Select(Index_, int(SelectOn_))
        
    def OnItemSelected(self, evt):
        """
        Обрабатываем выбор строки списка.
        """
        self.currentItem = evt.m_itemIndex
        self.evalSpace['evt'] = evt
        self.evalSpace[self.name+'_currentItem'] = self.currentItem
        self.eval_attr('selected')
        
    def OnItemActivated(self, evt):
        """
        Обрабатываем активацию (Enter | DblClick) строки списка.
        """
        self.evalSpace['evt'] = evt
        self.evalSpace[self.name+'_activatedItem'] = self.currentItem
        self.eval_attr('activated')
        evt.Skip()


def test(par=0):
    """
    Тестируем класс icMultiColumnList.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icMultiColumnList Test')
    listCtrl = icMultiColumnList(frame, -1, {'fields': [_('Help'), u'колонка 2', u'колонка 3']})
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
