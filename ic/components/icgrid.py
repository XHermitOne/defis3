#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Обкладка для компонента grid.Grid.
Данный модуль содержит только описание класса icGrid. Привязка к данным
реализуется в классе icGridDataset.

:type SPC_IC_CELLATTR: C{Dictionary}
:var SPC_IC_CELLATTR: Спецификация на ресурсное описание аттрибутов ячеек данных. Описание ключей:

    - B{backgroundColor=wx.Colour(255, 255, 255)}: Цвет подложки.
    - B{foregroundColor=wx.Colour(0, 0, 0)}: Цвет текста.
    - B{font=None}: Шрифт (см. описание icFont).
    - B{alignment=('left','middle')}: Способ выравниввания ('centred','left', 'right', 'middle', 'top', 'bottom').

:type SPC_IC_LABELATTR: C{Dictionary}
:var SPC_IC_LABELATTR: Спецификация на ресурсное описание аттрибутов ячеек шапки. Описание ключей:

    - B{backgroundColor=wx.Colour(100, 100, 100)}: Цвет подложки.
    - B{foregroundColor=wx.Colour(255, 255, 255)}: Цвет текста.
    - B{font=None}: Шрифт (см. описание icFont).
    - B{alignment=('left','middle')}: Способ выравниввания ('centred','left', 'right', 'middle', 'top', 'bottom').

:type SPC_IC_GRID: C{Dictionary}
:var SPC_IC_GRID: Спецификация на ресурсное описание грида. Описание ключей:

    - B{name='default'}: Имя компонента.
    - B{label='Grid'}: Заголовок грида (не используется).
    - B{source=None}: Идентификатор таблицы данных.
    - B{import=\{\}}: Словарь импортируемых имен ({'module':[names], ... }).
    - B{position=(-1,-1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размер компонента.
    - B{style=wx.SIMPLE_BORDER}: Стиль компонента (см. стили icWindow/wxWindow).
    - B{line_color=wx.Colour(200, 200, 200)}: Цвет линий гида.
    - B{cell_attr=SPC_IC_CELLATTR}: Аттрибуты ячеек данных по умолчанию (см. описание SPC_IC_CELLATTR).
    - B{label_attr=SPC_IC_LABELATTR}: Аттрибуты ячеек заголовка (см. описание SPC_IC_LABELATTR).
    - B{label_height=20}: Высота ячеек шапки.
    - B{fixColSize=0}: признак фиксации ширины колонок.
    - B{fixRowSize=0}: признак фиксации высоты строк.
    - B{getattr=None}: Выражение, выполняемое при запросе на аттрибут ячейки (см. SPC_IC_CELLATTR), позволяет динмически
        устанавливать аттрибутами определенной ячейки. Выполняемое выражение должно вернуть объект типа grid.GridCellAttr. Для
        выражения доступны следующие переменные col, row, value, self - указатель на icGrid, data - указатель на icDataset.
    - B{keyDown=None}: Выражение, выполняемое после нажатия кнопки - реакция на событие EVT_KEYDOWN. Если выражение возвращает:
        IC_CTRLKEY_OK - Все действия по умолчанию тоже проделыватся (анализ на F1, Del и т. д.);
        IC_CTRLKEY_FAILED - Выход из функции обработки нажатия клавишь без Skip();
        IC_CTRLKEY_FAILED_SKIP - Выход из функции обработки нажатия клавишь со Skip();
    - B{dclickEditor=None}: Выражение выполняется после двойного нажатия кнопки мыши на редакторе ячейки.
    - B{selected=None}: Выражение, выполняемое после выбора ячейки.
    - B{post_select=None}: Выражение, выполняемое после выбора ячейки, когда установится
        фокус на новую ячейку.
    - B{changed=None}: Выражение, выполняется после изменения текущей строки. Возвращает код контроля.
    - B{cols=[]}: Cписок описания колонок.
    - B{delRec=None}: Выражение, выполняемое при удалении записи.
        Если выражение равно == 0, то запись не удаляется;
        == 1 - выводится стандартный диалог запрашивающий разрешение на удаление записи;
        == 2 - запись удаляется без уведомления.
    - B{init=None}: Выражение, выполняемое при добавлении записи. Если выражение возвращает False,
        то запись не добавляется, если True, то добавляется.
    - B{post_init=None}: Выражение, выполняемое после добавлении записи. Если выражение возвращает False,
        то добавленная запись удаляется.
    - B{post_del=None}: Выражение, выполняемое после попытки удаления записи. В этом выражении можно обработать
        ситуацию, когда удаление по каким-либо причинам не прошло, например, нарушение целостности данных.
        Для этого можно проанализировать словарь action_res_buff. По ключу 'delRec' находится код
        возврата функции удалени записи.
    - B{refresh=None}: Выражение, возвращающее список обновляемых компонентов. Под обновлением понимается обновление
        представлений компонентов (для вычисляемых полей это соответствует вычислению выражения аттрибута 'getvalue').
        Если атрибут равен None, то обновляются все объекты работающие с классами данных.
    - B{recount=None}: Выражение, возвращающее список пересчитываемых компонентов. Под этим понимается пересчет
        значений хранимых в базе данных. Стадии пересчета вычисляемого поля:
            - вычисление представления поля (по атрибуту 'getvalue')
            - отрабатывает контроль значения поля(по атрибуту 'ctrl')
            - Если контроль проходит запись в базу вычисленного значения (по атрибуту 'setvalue')
    
:type SPC_IC_CELL: C{Dictionary}
:var SPC_IC_CELL: Спецификация на ресурсное описание колонок грида.

    - B{name=default}: Идентификатор столбца.
    - B{label='col'}: Имя колонки. Имя колонки может быть многострочным. Символы
        '\\n', '\\n\\r' задают конец строки.
    - B{width=50}: Ширина колонки.
    - B{attr=None}: Атрибуты редактирования ячейки.
    - B{pic='S'}: Шаблон вывода. (S (строковый), T (текстовый), N(integer),F(float), X(строковые шаблоны),
        9(числовые шаблоны),DT(datatime), B(bool), CH(choice, см. описания valid))
    - B{cell_attr=SPC_IC_CELLATTR}: Аттрибуты представления ячейки.
    - B{getvalue=None}: Выражение, вычисляющее значение ячейки для вывода на форму.
    - B{setvalue=None}: Выражение, вычисляющее значение для записи в базу данных.
    - B{hlp=None}: Выражение, выполняемое после вызова справки (F1 или кнопка редактора) на значение поля.
    - B{ctrl=None}: Выражение, выполяемое после потери фокуса на определенную ячейку.
    - B{init=None}: Выражение, выполяемое при создании ячейки (например при добавлении строки в грид).
    - B{recount=None}: Выражение, вычисляющее список объектов, которые необходимо пересчитать после изменения значения ячейки.
    - B{valid=None}: Выражение, фильтрующее возможные значения ячейки (при использовании Choice(pic=CH)).
        Строки отделяются ','. Пример: 1,2,3.
    - B{keyDown=None}: Выражение, выполняемое при нажатии любой клавиши.
    - B{onSize=None}: Выражение, выполняемое при изменении размера грида.
    - B{shortHelpString:''}: Строка подсказки на колонку грида, выводится по нажатию
         правой кнопки мыши на заголовок.
    - B{sort=None}: Выражение, возыращающее признак (True | False) сортировки колонки. Если
        соответствующее поле объекта данных индексируемое, то индексация производится через
        SQL - выражение. Индексация вычисляемого поля не привязанного не к одному полю
        класса данный производится прямым вычислением всех значений данного поля и последующей
        сортировкой всех записей, согласно вычисленным значениям. Понятно, что время выполнения
        сортировки в этом случае значительо больше. Поэтому данный вид сортировки не рекомендуется
        для таблиц с большим количетвом записей и сложной алгоритмикой вычисления полей.
"""
import wx
import copy
from wx import grid
from wx.lib.mixins import gridlabelrenderer

from ic.utils import util
from . import icwidget
from .icfont import SPC_IC_FONT
from ic.PropertyEditor import icDefInf
from ic.log import log
from ic.dlg import dlgfunc
from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#  Словарь аттрибутов ячеек данных
SPC_IC_CELLATTR = {'type': 'cell_attr',
                   'name': 'default',
                   '_uuid': None,

                   'backgroundColor': None,
                   'foregroundColor': None,
                   'font': {},
                   'alignment': ('left', 'top'),

                   '__lists__': {'alignment': ['(\'left\', \'top\')',
                                               '(\'right\', \'top\')',
                                               '(\'centre\', \'top\')',
                                               '(\'left\', \'centre\')',
                                               '(\'right\', \'centre\')',
                                               '(\'centre\', \'centre\')',
                                               '(\'left\', \'bottom\')',
                                               '(\'right\', \'bottom\')',
                                               '(\'centre\', \'bottom\')',
                                               ],
                                 },
                   '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'alias', '_uuid'],
                                      icDefInf.EDT_COLOR: ['foregroundColor', 'backgroundColor'],
                                      icDefInf.EDT_FONT: ['font'],
                                      icDefInf.EDT_CHOICE: ['alignment'],
                                      }
                   }

#  Словарь аттрибутов ячеек шапки
SPC_IC_LABELATTR = {'type': 'label_attr',
                    'name': 'default',
                    '_uuid': None,

                    'backgroundColor': None,
                    'foregroundColor': None,
                    'font': {},
                    'alignment': ('centre', 'centre'),

                    '__lists__': {'alignment': ['(\'centre\', \'centre\')',
                                                '(\'left\', \'top\')',
                                                '(\'right\', \'top\')',
                                                '(\'centre\', \'top\')',
                                                '(\'left\', \'centre\')',
                                                '(\'right\', \'centre\')',
                                                '(\'left\', \'bottom\')',
                                                '(\'right\', \'bottom\')',
                                                '(\'centre\', \'bottom\')',
                                                ],
                                  },
                    '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'alias', '_uuid'],
                                       icDefInf.EDT_COLOR: ['foregroundColor', 'backgroundColor'],
                                       icDefInf.EDT_FONT: ['font'],
                                       icDefInf.EDT_CHOICE: ['alignment'],
                                       }
                    }

# Режимы выбора
GRID_SELECTION_MODES = {'cells': grid.Grid.GridSelectCells if wx.VERSION >= (4, 1, 1) else grid.Grid.wxGridSelectCells,
                        'rows': grid.Grid.GridSelectRows if wx.VERSION >= (4, 1, 1) else grid.Grid.wxGridSelectRows,
                        'columns': grid.Grid.GridSelectColumns if wx.VERSION >= (4, 1, 1) else grid.Grid.wxGridSelectColumns,
                        }
    
#   Спецификация описания грида
SPC_IC_GRID = {'type': 'Grid',         # тип ресурса
               'name': 'default',      # идентификатор
               'cols': [],             # список колонок

               'label': 'Grid',        # подпись грида
               'position': (-1, -1),   # расположение на родительском окне
               'size': (-1, -1),       # размер
               'style': 0,
               'line_color': None,  # цвет линий гида
               'fixColSize': 0,
               'fixRowSize': 0,
               'selection_mode': 'cells',
               # -------- Аттрибуты ячеек ---------------------------------------------
               'cell_attr': copy.deepcopy(SPC_IC_CELLATTR),
               # -------- Аттрибуты шапки ---------------------------------------------
               'label_attr': copy.deepcopy(SPC_IC_LABELATTR),
               'label_height': 20,     # высота шапки
               'row_height': 20,
               'getattr': None,
               'keyDown': None,
               'dclickEditor': None,
               'onSize': None,
               'selected': None,
               'post_select': None,
               'changed': None,
               'init': None,
               'post_init': None,
               'post_del': None,
               'delRec': None,
               'source': None,
               'flag': wx.EXPAND | wx.GROW,
               'proportion': 1,
               'refresh': None,
               'docstr': 'ic.components.icgrid.html',

               '__styles__': {'DEFAULT': 0},
               '__events__': {'onSize': ('wx.EVT_SIZE', 'onSizeGrid', False),
                              'dclickEditor': ('wx.EVT_LEFT_DCLICK', 'OnDClickEditor', False),
                              },
               '__lists__': {'selection_mode': list(GRID_SELECTION_MODES.keys()),
                             },
               '__attr_types__': {icDefInf.EDT_COLOR: ['line_color'],
                                  icDefInf.EDT_NUMBER: ['label_height', 'row_height', 'fixRowSize', 'fixColSize'],
                                  icDefInf.EDT_CHOICE: ['selection_mode'],
                                  },
               '__parent__': icwidget.SPC_IC_WIDGET,
               }

#   Спецификация описания ячеек, распространяется на всю колонку
SPC_IC_CELL = {'type': 'GridCell',
               'name': 'default',

               'label': 'col',
               'width': 50,
               'attr': 'W',    # аттрибуты редактирования ячейки
               'pic': 'S',
               'cell_attr': copy.deepcopy(SPC_IC_CELLATTR),    # аттрибуты представления ячейки
               'getvalue': '',
               'setvalue': '',
               'hlp': None,
               'ctrl': None,
               'init': None,
               'recount': None,
               'valid': None,
               'sort': None,
               'nsi_psp': None,    # Паспорт справочника. Только для шаблона NSI
               'shortHelpString': '',
               'keyDown': None,
               'get_grp_key': None,    # Получение ключа группы
               'get_grp_title': None,  # Получение заголовка группы

               '__styles__': {'DEFAULT': 0},
               '__events__': {'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDown', False),
                              },
               '__lists__': {'attr': ['W', 'R', 'C', 'cr'],
                             'pic': ['S', 'TEXT', 'N', 'F', 'DT', 'B', 'CH', 'NSI', 'XXXX', '9999', '999,999.99'],
                             },
               '__attr_types__': {icDefInf.EDT_PY_SCRIPT: ['keyDown'],
                                  icDefInf.EDT_NUMBER: ['width'],
                                  icDefInf.EDT_CHOICE: ['attr', 'pic'],
                                  icDefInf.EDT_TEXTFIELD: ['pic', 'label'],
                                  icDefInf.EDT_USER_PROPERTY: ['nsi_psp'],
                                  },
               '__parent__': icwidget.SPC_IC_SIMPLE,
               }

#   Версия компонента
__version__ = (1, 1, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('nsi_psp',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('nsi_psp',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in ('Sprav',):
                dlgfunc.openWarningBox(u'ОШИБКА', u'Выбранный объект не является Справочником.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('nsi_psp',):
        return pspEdt.str_to_val_user_property(text, propEdt)


def getIdAlignment(horiz, vert):
    """
    Функция определяет идентификатор выравнивания по имени.

    :param horiz: Название горизонтального выравнивания ('left', 'right', 'centre').
    :type horiz: C{string}
    :param vert: Название вертикального выравнивания ('top', 'bottom', 'centre')
    :type vert: C{string}
    :return: Возвращает кортеж, состоящий из идентификаторов. Пример ('left', 'top')
    :rtype: C{tuple}
    """
    if isinstance(horiz, str):
        if horiz == u'left':
            iHoriz = wx.ALIGN_LEFT
        elif horiz == u'right':
            iHoriz = wx.ALIGN_RIGHT
        else:
            iHoriz = wx.ALIGN_CENTRE
    else:
        iHoriz = horiz

    if isinstance(vert, str):
        if vert == u'top':
            iVert = wx.ALIGN_TOP
        elif vert == u'bottom':
            iVert = wx.ALIGN_BOTTOM
        elif vert == u'centre':
            iVert = wx.ALIGN_TOP
        else:
            iVert = wx.ALIGN_TOP
    else:
        iVert = vert

    return iHoriz, iVert


class icGrid(icwidget.icWidget, grid.Grid,
             gridlabelrenderer.GridWithLabelRenderersMixin):
    """
    Класс создает грид по ресурсному описанию.
    """
    def __init__(self, parent, id, component, logType=0,
                 evalSpace=None, bCounter=False, progressDlg=None):
        """
        Конструктор для создания icGrid.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        """
        component = util.icSpcDefStruct(SPC_IC_GRID, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)
        self.pos = component['position']
        self.cols = copy.deepcopy([x for x in component['cols'] if util.isAcivateRes(x, evalSpace) and x['type'] == 'GridCell'])
        self.line_color = component['line_color']
        self.label_attr = copy.deepcopy(component['label_attr'])
        self.cell_attr = copy.deepcopy(component['cell_attr'])
        self.label_height = int(component['label_height'])

        self.getattr = component['getattr']
        self.keydown = component['keyDown']
        self.selected = component['selected']
        self.changed = component['changed']
        self.delrec = component['delRec']
        self.addrec = component['init']
        self.post_addrec = component['post_init']
        self.post_delrec = component['post_del']
        
        util.icSpcDefStruct(SPC_IC_LABELATTR, self.label_attr)
        util.icSpcDefStruct(SPC_IC_FONT, self.label_attr['font'])

        #   Преобразуем выравнивание
        if not isinstance(self.label_attr, str):
            aln = self.label_attr['alignment']
            if isinstance(aln, str):
                try:
                    aln = eval(aln)
                except:
                    aln = ('left', 'middle')
            if aln is not None:
                self.label_attr['alignment'] = getIdAlignment(aln[0], aln[1])

        util.icSpcDefStruct(SPC_IC_CELLATTR, self.cell_attr)
        util.icSpcDefStruct(SPC_IC_FONT, self.cell_attr['font'])

        #   Преобразуем выравнивание
        if not isinstance(self.cell_attr, str):
            aln = self.cell_attr['alignment']
            if isinstance(aln, str):
                try:
                    aln = eval(aln)
                except:
                    aln = ('left', 'middle')
            if aln is not None:
                self.cell_attr['alignment'] = getIdAlignment(aln[0], aln[1])

        #   Переводим значение аттрибутов колонок в верхний регистр
        for col in self.cols:
            #   Заменяем все имена колонок на алиасы
            if 'alias' in col and not col['alias'] in [None, '', 'None']:
                col['name'] = col['alias']
            
            util.icSpcDefStruct(SPC_IC_CELL, col)
            util.icSpcDefStruct(SPC_IC_CELLATTR, col['cell_attr'])
                        
            if isinstance(col['attr'], str):
                col['attr'] = col['attr'].upper()
                
            #   Преобразуем выравнивание для ячеек колоноки
            if 'cell_attr' in col and 'alignment' in col['cell_attr']:
                aln = col['cell_attr']['alignment']
                if isinstance(aln, str):
                    try:
                        aln = eval(aln)
                    except:
                        aln = ('left', 'middle')
                if aln is not None:
                    col['cell_attr']['alignment'] = getIdAlignment(aln[0], aln[1])
                    
            #   Вычисляем атрибут <show> колонки
            bShow = 1
            if 'show' in col:
                if isinstance(col['show'], str):
                    attr_show = '@' + col['show']
                    keyExpr = self.GetUUIDAttr('show', col['name'])
                    bShow = util.getICAttr(attr_show, evalSpace,
                                           u'Error in getICAttr in icgrid. col name=%s <show>=%s <key>=%s' %
                                           (col['name'], col['show'], keyExpr))
                else:
                    bShow = col['show']
            
            col['show'] = bShow

        grid.Grid.__init__(self, parent, id, self.pos, self.size, name=self.name, style=component['style'])
        gridlabelrenderer.GridWithLabelRenderersMixin.__init__(self)
        
        self.SetDefaultRowSize(component['row_height'])

        # Указатель на сложную шапку
        self.header = None
        #   Обработчики событий
        self.Bind(grid.EVT_GRID_COL_SIZE, self.onColSize)
        self.Bind(grid.EVT_GRID_SELECT_CELL, self.onSelected)
        self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.onScrollLineUp)
        self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.onScrollLineDown)
        self.Bind(wx.EVT_SCROLLWIN_PAGEUP, self.onScrollPageUp)
        self.Bind(wx.EVT_SCROLLWIN_PAGEDOWN, self.onScrollPageDown)
        self.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.onScrollTrack)
        self.Bind(wx.EVT_SIZE, self.onSizeGrid)
        #   Переменные где хранятся значения ряда и колонки, котрые выбираются
        #   после вызова функции doPostSelect().
        self._selEventRow = -1
        self._selEventCol = -1
        
    def getIndxFieldResource(self, indx):
        """
        Возвращает ресурсное описание поля по индиксу.
        """
        try:
            return self.resource['cols'][indx]
        except:
            log.fatal(u'Ошибка в функции getIndxFieldResource')
    
    def getWidthGrid(self):
        """
        Возвращает общий размер шапки.
        """
        self.labelsize = self.GetRowLabelSize()
        for col in range(self.GetNumberCols()):
            w = self.GetColSize(col)
            self.labelsize += w

        return self.labelsize

    def onSizeGrid(self, event):
        """
        Обрабатывает изменение размера грида.
        """
        self.doReconstructHeader()
        #   Для некоторых ситуаций необходимо
        self.doPostSelect()
        #   Обработчик на изменения размеров грида
        self.evalSpace['event'] = event
        self.evalSpace['evt'] = event
        self.eval_attr('onSize')
        event.Skip()

    def onSelected(self, event):
        """
        Выбор ячейки грида.
        """
        vx, vy = self.GetViewStart()
        dx, dy = self.GetScrollPixelsPerUnit()
        if self.header and self.header.scroll_pos[0] != vx*dx:
            self.doReconstructHeader()
            
        event.Skip()
        
    def onColSize(self, event):
        """
        Изменение размера колонки.
        """
        # ----------------------------------------------------
        #   В режиме редактирования надо отслеживать
        #   изменение размеров колонок
        col = event.GetRowOrCol()
        w = self.GetColSize(col)
        mode = self.GetRunTimeMode()
        if mode == util.IC_RUNTIME_MODE_EDITOR:
            res = self.GetTable().exCols[col]
            iditem = res['__item_id']
            self.evalSpace['_root_obj'].GetEditorPanel().ChangeResItemProperty(iditem, 'width', w)
        # ----------------------------------------------------
        event.Skip()
        vx, vy = self.GetViewStart()
        dx, dy = self.GetScrollPixelsPerUnit()
        self.doReconstructHeader()
        
    def onScrollLineUp(self, event):
        """
        """
        if event.GetOrientation() == wx.HORIZONTAL:
            vx, vy = self.GetViewStart()
            dx, dy = self.GetScrollPixelsPerUnit()
            if self.header and vx != 0:
                self.header.setViewStart(vx * dx - dx, 0)
        event.Skip()

    def onScrollLineDown(self, event):
        """
        """
        if event.GetOrientation() == wx.HORIZONTAL:
            vx, vy = self.GetViewStart()
            dx, dy = self.GetScrollPixelsPerUnit()
            w = self.getWidthGrid()
            sx, sy = self.GetSize()
            if self.header and vx*dx+dx <= w - sx+dx:
                self.header.setViewStart(vx * dx + dx, 0)
            else:
                self.doPostSelect()

        event.Skip()

    def onScrollPageUp(self, event):
        """
        """
        if event.GetOrientation() == wx.HORIZONTAL:
            vx, vy = self.GetViewStart()
            dx, dy = self.GetScrollPixelsPerUnit()
            sx, sy = self.GetSize()
            if self.header and vx != 0:
                if vx*dx > sx:
                    self.header.setViewStart(vx * dx - sx, 0)
                else:
                    self.header.setViewStart(0, 0)
        event.Skip()
        
    def onScrollPageDown(self, event):
        """
        """
        if event.GetOrientation() == wx.HORIZONTAL:
            self.doPostSelect()
            
        event.Skip()
        
    def onScrollTrack(self, event):
        """
        """
        if event.GetOrientation() == wx.HORIZONTAL:
            vx = event.GetPosition()
            dx, dy = self.GetScrollPixelsPerUnit()
            w = self.getWidthGrid()
            sx, sy = self.GetSize()
            if self.header and vx*dx <= w - sx + dx:
                self.header.setViewStart(vx * dx, 0)
            else:
                self.doPostSelect()
                
        event.Skip()

    def doPostSelect(self, row=-1, col=-1):
        """
        Посылает в очередь сообщение EVT_GRID_SELECT_CELL для выбора
        нужной ячейки.
        """
        if row < 0:
            row = self.GetGridCursorRow()
        if col < 0:
            col = self.GetGridCursorCol()

        self._selEventRow = row
        self._selEventCol = col

        select_event = grid.GridEvent(wx.NewId(), grid.wxEVT_GRID_SELECT_CELL, self, row, col)
        self.GetEventHandler().AddPendingEvent(select_event)
        
    def doReconstructHeader(self):
        """
        Функция перепривязывает шапку к гриду.
        """
        if not self.header:
            return

        row = self.header.getMaxRow()
        self.labelsize = 0
        for col in range(self.GetNumberCols()):
            cell = self.header.findCell(row, col)
            w = self.GetColSize(col)
            self.labelsize += w
            if cell:
                old_w, old_h = cell.GetSize()
                if col == 0:
                    cell.size = wx.Size(w + self.GetRowLabelSize(), old_h)
                else:
                    cell.size = wx.Size(w, old_h)
                    
                cell.SetSize(cell.size)
                
        self.header.reconstruct()

    def setHeader(self, header, bAuto=False, bHideOldHead=False):
        """
        Связывает шапку с гридом.

        :type bAuto: C{bool}
        :param bAuto: Признак автоматического создания стандартной шапки грида.
        :type bHideOldHead: C{bool}
        :param bHideOldHead: Признак скрытия старой шапки.
        """
        self.header = header
        try:
            header.connectGrid(self, bAuto, bHideOldHead)
        except:
            log.fatal(u'Can\'t connectGrid() in icGrid.setHeader')
        
    def getSelectionModeAttr(self):
        """
        Режим выбора элемента грида.
        """
        try:
            attr_value = self.getICAttr('selection_mode')
            if attr_value in GRID_SELECTION_MODES:
                return GRID_SELECTION_MODES[attr_value]
        except:
            log.warning(u'Not define attr selection_mode in Grid')
        return grid.Grid.GridSelectCells if wx.VERSION >= (4, 1, 1) else grid.Grid.wxGridSelectCells

    def moveCursorFirst(self):
        """
        Передвинуть курсор на первую строку.
        """
        return self.GoToCell(0, self.GetGridCursorCol())

    def moveCursorLast(self):
        return self.GoToCell(self.GetNumberRows()-1, self.GetGridCursorCol())

    def moveCursorNext(self):
        return self.MoveCursorDown(False)

    def moveCursorPrev(self):
        return self.MoveCursorUp(False)


class icColLabelRenderer(gridlabelrenderer.GridLabelRenderer):
    def __init__(self, bgcolor):
        self._bgcolor = bgcolor
        
    def Draw(self, grid, dc, rect, col):
        dc.SetBrush(wx.Brush(self._bgcolor))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangleRect(rect)
        hAlign, vAlign = grid.GetColLabelAlignment()
        text = grid.GetColLabelValue(col)
        self.DrawBorder(grid, dc, rect)
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)


def test(par=0):
    """
    Тестируем класс icGrid
    """
    from ic.components import ictestapp
    import ic.components.icGridCellEditors as icEdt
    
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'icGrid Test')
    win = wx.Panel(frame, -1)

    grid = icGrid(win, -1, {'size': (400, 300),
                            'keyDown': 'print(\'keyDown in Grid\')'})
    grid.CreateGrid(30, 7)
    grid.SetCellEditor(0, 0, icEdt.icGridCellDateEditor())
    grid.SetMargins(2,2)
    grid.SetColLabelRenderer(0, icColLabelRenderer('#e0ffe0'))
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test(0)
