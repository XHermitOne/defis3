#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
По ресурсному описанию формирует описание типов данных, выводимых гридом.
"""

import wx
import wx.grid
import copy
import string

from ic.dlg.msgbox import MsgBox

from ic.db import icdataset
from ic.db import icsimpledataset

from .icFieldTempl import *
from .icgrid import icGrid
from .icgrid import SPC_IC_GRID
from .icgrid import SPC_IC_CELLATTR
from .icgrid import getIdAlignment
from .icgrid import GRID_SELECTION_MODES
from .icgrid import SPC_IC_CELL
from .icfont import *
from ic.log.iclog import *
from . import icwidget
from . import icEvents
import ic.utils.frequencydict as frequencydict
import ic.utils.associationdict as associationdict

import ic.utils.util as util
from ic.utils import ic_uuid
from ic.utils.coderror import *
import ic.utils.translate as translate
import ic.utils.lock as ic_lock
from . import icGridCellEditors as icEdt
from ic.kernel import io_prnt
from . import icgriddataset_erm
from ic.kernel import icContext
import ic
import ic.PropertyEditor.icDefInf as icDefInf

_ = wx.GetTranslation

SPC_IC_GRID_DATASET = copy.deepcopy(SPC_IC_GRID)
SPC_IC_GRID_DATASET['type'] = 'GridDataset'

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icComboType

#   Имя пользовательского класса
ic_class_name = 'icGridDataset'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_GRID_DATASET
ic_class_spc['__styles__'] = ic_class_styles
ic_class_spc['enable_freq_dict'] = False
ic_class_spc['__attr_types__'][icDefInf.EDT_CHECK_BOX] = ['enable_freq_dict']

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtDBGrid'
ic_class_pic2 = '@common.imgEdtDBGrid'

#   Путь до файла документации
ic_class_doc = None

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['GridCell']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 8)

#   Атрибуты редактируемых ячеек
icAttrEditCell = {'backgroundColor': (255, 255, 255),
                  'foregroundColor': (0, 0, 0),
                  'font': {},
                  'alignment': ('left', 'middle'),
                  }

#   Буфер для атрибутов ячеек грида
icGridAttrBuff = {}
icimagebutton = None


def get_ext_btn(prnt, pos):
    global icimagebutton
    if not icimagebutton:
        from ic.components.custom import icimagebutton as lib
        icimagebutton = lib
    btn = icimagebutton.get_ext_btn(prnt, pos)
    return btn


def cmpRows(x, y):
    """
    Функция сравнения для сортировки данных в гриде (в порядке уменьшения) по
    вычисляемому полю.
    """
    if x[1] > y[1]:
        return -1
    elif x[1] < y[1]:
        return 1
    else:
        return 0


def getAttrKey(attrRes):
    """
    Формирует ключ аттрибута.
    @type attrRes: C{dictionary}
    @param attrRes: Описание аттрибута ячейки.
    """
    fk = util.icSpcDefStruct(SPC_IC_FONT, attrRes['font'])
    font_key = unicode(fk['size']) + unicode(fk['family']) + unicode(fk['faceName']) + unicode(fk['style']) + unicode(fk['underline'])
    key = (unicode(attrRes['foregroundColor']) + unicode(attrRes['backgroundColor']) +
           font_key + unicode(attrRes['alignment']))
    if 'readonly' in attrRes:
        key += unicode(attrRes['readonly'])
    return key


def getAttrBuff(attrRes):
    """
    Достает нужный аттрибут ячееки.
    @type attrRes: C{dictionary}
    @param attrRes: Описание аттрибута ячейки.
    """
    global icGridAttrBuff
    attrRes = util.icSpcDefStruct(SPC_IC_CELLATTR, attrRes)
    key = getAttrKey(attrRes)
    if key in icGridAttrBuff:
        attr = icGridAttrBuff[key]
        attr.IncRef()
    else:
        attr = createAttr(attrRes)
        setAttrBuff(attrRes, attr)
    return attr


def setAttrBuff(attrRes, attr):
    """
    Кладет в буфер атрибут ячейки грида.
    @type attrRes: C{dictionary}
    @param attrRes: Описание аттрибута ячейки.
    """
    global icGridAttrBuff
    attrRes = util.icSpcDefStruct(SPC_IC_CELLATTR, attrRes)
    key = getAttrKey(attrRes)
    attr.IncRef()
    icGridAttrBuff[key] = attr


def createAttr(attrRes):
    """
    Создает атрибут ячейки.
    @type attrRes: C{dictionary}
    @param attrRes: Описание аттрибута ячейки.
    """
    attr = wx.grid.GridCellAttr()
    #   По ресурсному описанию определяем атрибут
    clr = attrRes['backgroundColor']
    if isinstance(clr, wx.Colour):
        attr.SetBackgroundColour(clr)
    elif clr:
        attr.SetBackgroundColour(wx.Colour(*clr))

    clr = attrRes['foregroundColor']
    if isinstance(clr, wx.Colour):
        attr.SetTextColour(clr)
    elif clr:
        attr.SetTextColour(wx.Colour(* clr))

    #   Устанавливаем шрифт ячеек по умолчанию
    if attrRes['font']:
        attr.SetFont(icFont(attrRes['font']))
    #   Устанавливаем способ выравнивания по умолчанию
    if attrRes['alignment']:
        aln = attrRes['alignment']
        if type(aln[0]) in (str, unicode):
            aln = getIdAlignment(*aln)

        attr.SetAlignment(* aln)

    if 'readonly' in attrRes and attrRes['readonly']:
        attr.SetReadOnly()

    return attr


def iter_rowcol(gridData, lstBgColor, lstTextColor=None):
    """
    Функция возвращает атрибут ячейки в зависимости от номера строки. Цвета
    задает параметр lstColor.
    @type gridData: C{icGridDatasetData}
    @param gridData: Указатель на объект данных грида.
    @type lstBgColor: C{dictionary}
    @param lstBgColor: Список цветов, которые задают цвета фонов строк.
    @type lstTextColor: C{dictionary}
    @param lstTextColor: Список цветов, которые задают цвета фонов строк.
        Пример: C{iter_rowcol(self, [(200,200,200), (250, 250,250)], [(0,0,0),(0,0,0)])}
    """
    if lstBgColor in [None, []]:
        return {}
    try:
        #   Устанавливаем цвет фона ячеек по умолчанию
        row = gridData.evalSpace['row']
        indx = row % len(lstBgColor)
        clrBg = lstBgColor[indx]
        #   Устанавливаем цвет текста ячеек по умолчанию
        try:
            clr = lstTextColor[indx]
        except:
            clr = None
        attrRes = {'backgroundColor': clrBg, 'foregroundColor': clr}
        return attrRes
    except:
        io_prnt.outErr('iter_rowcol error')
    return {}


def GetColFromName(cols, name):
    """
    По имени колонки определяет ее реальный номер в гриде.
    @param cols: Описание колонок
    @type cols: C{list}
    @param name: Имя колонки
    @type name: C{string}
    @return: Номер колонки в гриде
    @rtype: C{int}
    """
    i = 0
    for col in cols:
        if col['name'] == name:
            return i
        # Скрытые колонки не учитываются
        if col['attr'] != 'UV' and col['show']:
            i += 1


class icGridDatasetData(wx.grid.PyGridTableBase):
    """
    Класс описания и доступа к данным. Доступ к данным осуществляется через объект
    icTable, который является интерфейсом к реальному источнику данных. Интерфейс
    описывается функциями getValue, setValue, addRecord, delRecord. Данный интерфейс
    позволяе организовать доступ к большим (> 2Gb) таблицам.
    """

    def GetDataCol(self, col):
        """
        Функция находит фактический номер колонки в источнике данных,
        поскольку в описании ресурса могут быть скрытые колонки (['attr'] == 'UV')
        @param col: Номер колонки
        @type col: C{int}
        @return: Возвращает соответствующий номер колонки в источнике данных.
        @rtype: C{int}
        """
        try:
            if not self.colNames:
                io_prnt.outWarning(u'Не определены колонки для грида <%s>' % self.grid.name)
                return None
            name = self.colNames[col]
            for count, oCol in enumerate(self.cols):
                if oCol['name'] == name:
                    return count
        except:
            io_prnt.outLastErr(u'### icGridDatasetData ERROR: GetDataCol [%d]' % col)
        return None

    def defData(self, cols, dataset=None):
        """
        Функция подготавливает данные, которые будут отображаться в гриде. Если
        внешний объект данных не определен, то будет использоваться внутренний объект
        данных icSimpleDataset.
        @param cols: Описание колонок.
        @type cols: C{list}
        @param dataset: Указатель на объект данных, если он известен.
        @type dataset: C{icSQLObjDataSet}
        @return: Возвращает указатель на объект данных.
        @rtype: C{icTable}
        """
        #   Заполняем служебные структуры
        self.dataTypes = list()
        self.colLabels = list()
        self.colNames = list()
        self.exCols = list()
        self.uvColNames = list()

        #   Определяем подписи и типы колонок
        for col in cols:
            if col['attr'] != 'UV' and col['show']:
                self.colNames.append(col['name'])
                self.colLabels.append(col['label'])
                self.dataTypes.append(self.defDataType(col))
                self.exCols.append(col)
            else:
                self.uvColNames.append(col['name'])

        #   Получаем курсор на источник данных
        if dataset is None:
            #   Если источник данных прописан
            if self.grid.source:
                MsgBox(self.grid, _('icGridDataset: Data source %s is not defined in the object context.') % unicode(self.link_res, 'utf-8'))
            #   В противном случае используем стандартный icSimpleDataset
            else:
                dataset = icsimpledataset.icSimpleDataset(icwidget.icNewId(),
                                                          {'description': self.exCols,
                                                           'wxGridTypes': self.dataTypes})
                self.grid.dataset = dataset
        else:
            dataset = self.grid.dataset

        #   Определяем внутренний указатель на объект данных
        self.dataset = dataset

    def defDataType(self, col):
        """
        Определяет типы форматов ячеек определенной колонки.
        @param col: Словарь описывающий параметры колонки.
        @type col: C{dictionary}
        @return: Возвращает тип ячейки.
        @rtype: C{int}
        """
        #   Для внешних выражений объекты icGridDatasetData должен выступать как
        #   составная часть icGridDataset
        self.evalSpace['self'] = self.grid
        #   Вычисляем атрибут шаблона вывода 'pic'
        pic = util.getICAttr(col['pic'], self.evalSpace, 'Error in icGridDataSet.defDataType(..)<pic>')
        if not pic:
            pic = 'S'
        #   Вычисляем атрибут 'valid', определяющий список возможных значений
        #   для выпадающего списка (Choice) и spinner-а
        valid = ''
        if not col['valid'] in [None, '']:
            valid = util.getICAttr(col['valid'], self.evalSpace, 'Error in icGridDataSet.defDataType(..)<valid>')

        col['spctype'], type = defPicType(pic, valid)
        return type

    def __init__(self, logType, _grid, cols, link_res=None, evalSpace=None, dataset=None):
        """
        Конструктор объекта описания данных.
        @param logType: Тип доступа к логу.
        @type logType: C{int}
        @param grid: Окно грида.
        @type grid: C{icGrid}
        @param cols: Описание колонок. Берется из ресурсного файла.
        @type cols: C{List}
        @param link_res: Ссылка на ресурсное описание источника данных.
        @type link_res: C{Dictionary}
        @param evalSpace: Пространство имен, необходимых для вычисления выражений.
        @type evalSpace: C{dictionary}
        @param dataset: Внешний объект данных.
        @type dataset: C{icSQLObjDataSet}
        @return: Возвращает созданный объект.
        @rtype: C{icGridData}
        """
        self.log = logType
        self.parent = _grid.parent
        self.grid = _grid
        self.bUpdate = True
        self.cols = cols
        self.link_res = link_res

        #   Буфферные переменные, которые хранят последние значения передаваемых параметров
        #   необходимы для обеспечения их видимости для внешних процедур
        self.row = 0
        self.col = 0
        self.value = None
        self.oldVar = ''
        if evalSpace is None:
            evalSpace = icContext.Context()
        self.context = self.evalSpace = evalSpace

        #   Номер последней редактируемой строки
        self.oldEditRow = None
        #   Определяется self.dataset и заполняются служебные структуры
        self.defData(self.cols, dataset)
        wx.grid.PyGridTableBase.__init__(self)
        #   Добавляем в пространство имен объект доступа к данным
        evalSpace['data'] = self.dataset
        evalSpace['dataset'] = self.dataset
        #   Для совместимости
        self.data = self.dataset
        #   Добавляем в пространство имен значения некоторых аттрибутов
        evalSpace['row'] = self.row
        evalSpace['col'] = self.col
        evalSpace['value'] = self.value
        #   Добавляем в пространство имен некоторые функции
        self.evalSpace['iter_rowcol'] = iter_rowcol
        #   Буфер результатов определенных действий. Ключ - имя атрибута, значение
        #   результат. Атрибуты, которые анализируются у грида delRec, changed, init.
        self.action_res_buff = {}

    def GetTable(self):
        """
        Возвращет указатель на объект таблицы.
        """
        return self

    def GetDataset(self):
        """
        Возвращает указатель на dataset.
        """
        return self.dataset

    def get_res_module(self):
        """
        Возвращает модуль ресурса.
        """
        return self.GetView().get_res_module()

    # Функции обновления данных

    def IsChanged(self, row=None):
        """
        Проверяем произошли ли изменения в гриде или нет.
        @type row: C{int}
        @param row: Номер строки.
        """
        if row is None:
            row = self.GetDataset().Recno()
        if self.GetDataset().isChangeRowBuff(row):
            return True
        return False

    def Update(self, row=None, bAsk=False):
        """
        Сохраняет буфер строки в базе.
        @type row: C{int}
        @param row: Номер строки.
        @return: Возвращает код контроля.
        @type bAsk: C{bool}
        @param bAsk: Признак подтверждения.
        """
        cod_ctrl = None
        if self.IsChanged(row):
            ret = wx.ID_YES
            #   Если определн признак подтверждения
            if bAsk:
                ret = MsgBox(self.GetView(), u'Сохранить изменения в <%s>?' % self.GetView().name,
                             style=wx.YES_NO | wx.NO_DEFAULT)
            if ret != wx.ID_YES:
                # Чистим буфер
                self.GetDataset().clearChangeRowBuff(row)
            else:
                #   Если определен аттрибут changed, проводим контроль на изменения строки
                if not self.GetView().changed in [None, '', 'None']:
                    res, cod_ctrl = self.GetView().eval_attr('changed')

                bUpd = True
                if cod_ctrl == IC_CTRL_REPL and not bAsk:
                    if MsgBox(self.parent, u'Сохранить изменения? (IC_CTRL_REPL)',
                              style=wx.YES_NO | wx.NO_DEFAULT) == wx.ID_NO:
                        bUpd = False
                elif cod_ctrl == IC_CTRL_FAILED:
                    bUpd = False
                    MsgBox(self.parent, u'Update record control is failed')
                elif cod_ctrl == IC_CTRL_FAILED_IGNORE:
                    bUpd = False

                if bUpd:
                    cod_ctrl = self.GetDataset().update(rec=row)

                    # -------------------------------------------
                    #   Сохраняем строку в ассоциативных словарях
                    if self.GetView()._asscDict and cod_ctrl in (IC_CTRL_REPL,
                                                                 IC_CTRL_OK):
                        for key, dct in self.GetView()._asscDict.items():
                            #   Создаем строку ассоциации
                            lst_val = [self.GetView().getNameValue(fld) for fld in dct.GetValueTuple()]
                            #   Создаем ключевой картеж
                            lst_key = range(len(key))
                            for indx, fld in enumerate(key):
                                if not fld in self.colNames:
                                    val = self.GetDataset().getNameValue(fld, row)
                                else:
                                    val = self.GetView().getNameValue(fld, row)
                                lst_key[indx] = val

                            #   Добавляем в словарь
                            dct.AddInAsscDict(tuple(lst_key), lst_val)
                    # -------------------------------------------
        else:
            cod_ctrl = IC_CTRL_OK

        self.action_res_buff['changed'] = cod_ctrl
        return cod_ctrl

    def UpdateRow(self, row, col, value):
        """
        Обновление значения ячеки (depricared). См. UpdateCell.
        """
        return self.UpdateCell(row, col, value)

    def UpdateCell(self, row, col, value):
        """
        Вызывается методом SetValue для обнавления значения поля в источнике данных.
        @param row: Номер стоки.
        @type row: C{int}
        @param col: Номер колонки.
        @type col: C{int}
        @param value: Новое значение.
        @return: Возвращает код контроля.
        @rtype: C{int}
        """
        #   Добавляем в пространство имен значения некоторых аттрибутов
        self.oldVar = self.GetValue(row, col)
        self.evalSpace['row'] = row
        self.evalSpace['col'] = col
        self.evalSpace['value'] = value
        self.evalSpace['val'] = value
        self.evalSpace['self'] = self
        self.evalSpace['old_value'] = self.oldVar
        fld_name = self.colNames[col]

        # SetValue на уровне грида
        self.oldEditRow = row
        txt = value

        #   Если определен аттрибут setvalue колoнки, то пытаемся по нему вычислить значение ячейки
        if (not self.exCols[col]['setvalue'] in [None, '', 'None']) and self.exCols[col]['attr'] in ['C', 'CR']:
            keyExpr = self.GetView().GetUUIDAttr('setvalue', fld_name)
            res, val = util.ic_eval(self.exCols[col]['setvalue'], 0, self.evalSpace,
                                    'Exception icGridDataSet.SetValue()',
                                    compileKey=keyExpr)
            if res:
                txt = val
            else:
                txt = ''

        #   Если задан структурный фильтр, то значение берется из фильтра
        flt = self.GetDataset().filter
        if isinstance(flt, dict) and fld_name in flt.keys():
            txt = translate.InitValidValue(flt, fld_name, txt)

        self.evalSpace['value'] = txt
        # Контроль ввода на уровне грида
        ctrl_val = IC_CTRL_OK
        result = False
        ctrl = self.exCols[col]['ctrl']
        #   Выполняем выражение на контроль значения
        if ctrl not in [None, '', 'None']:
            keyExpr = self.GetView().GetUUIDAttr('ctrl', fld_name)
            res, ctrl_ret = util.ic_eval(ctrl, 0, self.evalSpace,
                                         'Exception icGridDatasetData.UpdateCell()',
                                         compileKey=keyExpr)
            if res:
                try:
                    #   Если тип выражения картеж, то первый
                    #   элемент код контроля, второй словарь значений
                    if isinstance(ctrl_ret, tuple):
                        io_prnt.outLog('>>> $$$# CTRL COL ctrl_ret=%s, value=%s' % (str(ctrl_ret), value))
                        ctrl_val, values = ctrl_ret
                        if ctrl_val in [IC_CTRL_OK, IC_CTRL_REPL] and isinstance(values, dict):
                            for fld in values:
                                val = values[fld]
                                #   По имени поля ищем номер колонки
                                if fld in self.colNames:
                                    column = self.colNames.index(fld)
                                    ctrl_val = self.UpdateCell(row, column, val)
                                    if ctrl_val not in [IC_CTRL_OK, IC_CTRL_REPL]:
                                        break
                                else:
                                    ctrlFld = self.GetDataset().setNameValue(fld, val, row)
                                    if ctrlFld == IC_CTRL_FAILED:
                                        MsgBox(self.parent, _('Invalid field value %s, col=%d, row=%d')
                                               % (fld, col, row))
                    else:
                        ctrl_val = int(ctrl_ret)
                except:
                    io_prnt.outErr(u'INVALID RETURN CODE in UpdateCell')
                    ctrl_val = IC_CTRL_OK

                if ctrl_val == IC_CTRL_FAILED:
                    MsgBox(self.parent, _('Invalid field value %s, row=%d, col=%d')
                           % (fld_name, row, col))
        if txt is not None and ctrl_val in [IC_CTRL_OK, IC_CTRL_REPL]:
            ctrl_val = self.GetDataset().setNameValue(fld_name, txt, row)
            self.grid.Refresh()
            #   Анализируем код возврата
            if ctrl_val == IC_CTRL_FAILED:
                MsgBox(self.parent, _('Dataset attribute control: Invalid value, row=%d, col=%d') % (row, col))

            # ----------------------------------
            #   Заполняем частотный словарь
            elif ctrl_val in [IC_CTRL_OK, IC_CTRL_REPL] and self.GetView().IsEnableFreqDict():
                try:
                    if self.GetView()._freqDict and self.exCols[col]['spctype'] in (IC_N_STRING_FORMAT,
                                                                                    IC_STRING_FORMAT):
                        self.GetView()._freqDict.AddWordInFreqDict(fld_name, value)
                except:
                    io_prnt.outErr(u'FREQUENCY DICTIONARY ERROR')
            # ----------------------------------

        # -------------------------------------------------------------------------------
        #   Изменение одного поля может приводить к автоматическому пересчету других полей.
        #   Описание атрибута класса данных должно содержать список пересчитываемых атрибутов.
        #   По списку изменяемых полей вызываем соответствующие методы пересчета.
        return ctrl_val

    def AddRow(self, row, col, value):
        """
        Вызывается при добавлении новой записи. Запускается функция инициализации
        значений ячеек строки, а затем записвается в источник данных
        @param row: Номер стоки
        @type row: C{int}
        @param col: Номер колонки
        @type col: C{int}
        @param value: Новое значение
        @return: Возвращает признак успешного выполнения.
        @rtype: C{bool}
        """
        fld = self.colNames[col]
        #   Формируем в пространство имен
        self.evalSpace['self'] = self.grid
        self.evalSpace['row'] = row
        self.evalSpace['value'] = value
        self.evalSpace['fld'] = fld

        # -----------------------------------------------------------------------
        #   Проверяем буфер записи, если он заполнен, то спрашиваем пользователя
        #   сохранять его в базе или нет
        if row < self.GetNumberRows()-1:
            self.Update(row, True)

        # -----------------------------------------------------------------------
        #   Выполняем выражение, записанное в описании каждой колонки атрибута
        #   <init>.
        for indx, x in enumerate(self.cols):
            lst_rec = self.GetNumberRows()-1
            #   Проверяем есть ли в буфере запись данном поле, если нет, то
            #   вычисляем значение с использованием атрибута <init>
            try:
                isInit = x['name'] in self.GetDataset().changeRowBuff[lst_rec]
            except:
                isInit = False

            if not isInit:
                self.evalSpace['col'] = indx
                val = None
                if x['init'] not in [None, '', 'None']:
                    keyExpr = self.GetView().GetUUIDAttr('init', x['name'])
                    val = util.getICAttr(x['init'], self.evalSpace,
                                         'Exception icGridDataSet.AddRows()<init> col:%s' % x['name'],
                                          compileKey=keyExpr)

                #   Если задан структурный фильтр, то значение берется из фильтра
                flt = self.GetDataset().filter
                if isinstance(flt, dict) and x['name'] in flt.keys():
                    val = translate.InitValidValue(flt, x['name'], val)

                if val is not None:
                    #   По имени поля ищем номер колонки
                    if x['name'] in self.colNames:
                        column = self.colNames.index(x['name'])
                        ctrlFld = self.UpdateCell(lst_rec, column, val)
                    else:
                        ctrlFld = self.GetDataset().setNameValue(x['name'], val, lst_rec)
                        if ctrlFld == IC_CTRL_FAILED:
                            MsgBox(self.GetView(), _('Invalid field value %s, col=%d, row=%d') % (x['name'], indx, lst_rec))

                    if ctrlFld not in [IC_CTRL_OK, IC_CTRL_REPL]:
                        return False
        # ----------------------------------------------------------------------
        #   Выполняем выражение, записанное в атрибуте 'addRec'.
        #   Если выражение возвращает False, то запись не добавляется, если True,
        #   то добавляется.
        bRet = 1
        if not self.GetView().resource['init'] in [None, '']:
            res, val = self.GetView().eval_attr('init')
            if res:
                try:
                    bRet = int(val)
                except:
                    bRet = 1

            self.action_res_buff['init'] = bRet

        if bRet:
            #   Из буфера берем значения введенных полей
            keyExpr = ic_uuid.get_uuid_attr(self.GetView().GetUUID(), 'post_init')
            bRet = self.GetDataset().addRecord(postAddExpr=self.GetView().post_addrec,
                                               uuid_postAddExpr=keyExpr)
            # ---------------------------------------------
            #   Сохраняем строку в ассоциативных словарях
            if self.GetView()._asscDict and bRet:
                for key, dct in self.GetView()._asscDict.items():
                    #   Создаем строку ассоциации
                    lst_val = [self.GetView().getNameValue(fld) for fld in dct.GetValueTuple()]
                    #   Создаем ключевой картеж
                    lst_key = range(len(key))
                    for indx, fld in enumerate(key):
                        if fld not in self.colNames:
                            val = self.GetDataset().getNameValue(fld, row)
                        else:
                            val = self.GetView().getNameValue(fld, row)

                        lst_key[indx] = val

                    #   Добавляем в словарь
                    dct.AddInAsscDict(tuple(lst_key), lst_val)
        return bRet

    def GetNumberRows(self):
        """
        Определяет количество сток грида.
        """
        return self.GetDataset().getRecordCount() + 1

    def GetNumberCols(self):
        """
        Определяет количество колонок грида.
        """
        ncol = len(self.colNames)
        return ncol

    def IsEmptyCell(self, row, col):
        """
        Определяет пустая ли ячейка
        @param row: Номер стоки
        @type row: C{int}
        @param col: Номер колонки
        @type col: C{int}
        @return: Возвращает признак пустой строки.
        @rtype: C{bool}
        """
        fld = self.colNames[col]
        if row < self.GetNumberRows() - 1:
            return not self.GetDataset().getNameValue(fld, row)
        else:
            return True

    def GetPlainValue(self, row, col):
        pass

    def GetValue(self, row, col):
        """
        Функция возвращает значение ячейки. Позволяет организовать виртуальный грид.
        Данные грузятся не сразу в компонент, а подгружаются по мере необходимость.
        @param row: Номер стоки
        @type row: C{int}
        @param col: Номер колонки
        @type col: C{int}
        @return: Возвращает значение ячейки.
        """
        if row == self.GetNumberRows()-1:
            bLast = True
        else:
            bLast = False

        self.evalSpace['row'] = row
        self.evalSpace['col'] = col
        self.row, self.col = (row, col)
        try:
            fld = self.colNames[col]
            value = self.GetDataset().getNameValue(fld, row)
            self.evalSpace['value'] = value
            #   Если определен аттрибут getvalue колoнки, то пытаемся по нему вычислить значение ячейки
            if (not self.exCols[col]['getvalue'] in [None, '', 'None']) and self.exCols[col]['attr'] in ['C', 'CR']:
                keyExpr = self.GetView().GetUUIDAttr('getvalue', fld)
                res, val = util.ic_eval(self.exCols[col]['getvalue'], 0,
                                        self.evalSpace, 'Exception icGridDataSet.GetValue()',
                                        compileKey=keyExpr)
                if res:
                    value = val
            val = value
            templ = self.exCols[col]['pic']

            #   Форматируем значение по шаблону
            if value is not None and self.CanGetValueAs(row, col, wx.grid.GRID_VALUE_STRING):
                try:
                    value, point = setTempl(templ, value, -1)
                except:
                    MsgLastError(self.parent, u'Exception in setTempl()')
        except:
            io_prnt.outErr(u'Error in GetValue')
            value = ''
            val = ''

        self.evalSpace['value'] = value
        self.evalSpace['val'] = val
        #   Проверяем удалена ли запись из источника данных
        try:
            if self.GetDataset().isDeleted(row):
                self.GetDataset().delRecord(row)
                self.GetView().SendDelMess(row, 1)
        except:
            io_prnt.outLastErr(u'GridDataset. Check del rec')
        #   Проверяем не появились ли в источнике данных новые записи.
        try:
            if self.GetDataset().isAdded():
                #   Добавляем в наш объект идентификаторы записей , добавленных другими пользователями либо другим
                #   объектом данных.
                num = self.GetDataset().AddExternal()
                self.GetView().SendAddMess(num)
        except:
            io_prnt.outLastErr(u'GridDataset. Check new rec')
        return value

    def SetValue(self, row, col, value):
        """
        Функция преобразует значения ячеек к нужному виду и записывает в
        источник данных.
        @param row: Номер стоки
        @type row: C{int}
        @param col: Номер колонки
        @type col: C{int}
        @param value: Новое значение
        @return: Возвращает признак успешного выполнения.
        @rtype: C{bool}
        """
        self.evalSpace['txt'] = value
        #   Там где надо убираем признаки форматирования;
        #   в базе данных храним не форматированные значения
        try:
            templ = self.exCols[col]['pic']
            txt = delTempl(templ, value)
        except Exception:
            txt = value
        #   Преобразуем типы
        if self.exCols[col]['spctype'] in (IC_C_FLOAT_FORMAT, IC_FLOAT_FORMAT):
            txt = float(txt)
        if self.exCols[col]['spctype'] in (IC_C_NUMBER_FORMAT, IC_NUMBER_FORMAT):
            txt = int(txt)
        ctrl_val = self.UpdateCell(row, col, txt)
        return ctrl_val

    def DeleteRows(self, row, num=1, bAsk=True):
        """
        Функция вызывает метод хранилища данных для удаления записи
        @param row: Номер стоки.
        @type row: C{int}
        @param num: Количество строк.
        @type num: C{int}
        @return: Возвращает признак успешного выполнения.
        @type bAsk: C{bool}
        @param bAsk: Признак того, что необходимо вывести предупреждающее сообщение.
        @rtype: C{bool}
        """
        cod_del = IC_DEL_OK
        #   Выполняем выражение, записанное в атрибуте 'delRec'
        #   Если выражение равно == 0, то запись не удаляется
        #   == 1 - выводится стандартный диалог запрашивающий разрешение на удаление записи
        #   == 2 - запись удаляется без уведомления
        if not self.GetView().resource['delRec'] in [None, '', 'None']:
            #   Заносим в пространство имен параметры функции для последующего использования
            self.evalSpace['self'] = self
            self.evalSpace['row'] = row
            self.evalSpace['num'] = num
            self.evalSpace['bAsk'] = bAsk
            res, val = self.GetView().eval_attr('delRec')
            if res:
                try:
                    cod_del = int(val)
                except:
                    cod_del = IC_DEL_OK
            self.action_res_buff['delRec'] = cod_del
        if bAsk and cod_del == IC_DEL_OK and MsgBox(self.GetView(), u'Удалить запись?',
           style=wx.YES_NO | wx.NO_DEFAULT) != wx.ID_YES:
            cod_del = IC_DEL_FAILED_IGNORE
            self.action_res_buff['delRec'] = cod_del
        elif cod_del == IC_DEL_FAILED:
            MsgBox(self.GetView(), u'Не возможно удалить запись')
        elif cod_del == IC_DEL_USER:
            self.GetView().RefreshGrid()
            self.GetView().eval_attr('post_del')

        #   Удаляем записи
        if cod_del == IC_DEL_OK and row < self.GetNumberRows() - 1:
            self.row = row
            cod_del = self.GetDataset().delRecord(row)
            if cod_del == IC_DEL_OK:
                self.GetView().SendDelMess(row, num)

        #   Обрабатываем post_del в не зависимости от того, прошло удаление или нет
        self.action_res_buff['delRec'] = cod_del
        self.GetView().eval_attr('post_del')
        return cod_del

    def GetColLabelValue(self, col):
        """
        Called when the grid needs to display labels.
        Функция возвращает подпись колонки.
        @param col: Номер колонки
        @type col: C{int}
        @return: Возвращает подпись колонки.
        @rtype: C{string}
        """
        col_label = util.getICAttr(self.colLabels[col], self.evalSpace,
                                   'Error in GetColLabel(), col=%d' % col).replace('\\r\\n', '\n').replace('\\n','\n')
        #   Проверяем есть ли по данной колонке индексное выражение либо
        #   выражение для сортировки (атрибут 'sort')
        rescol = self.exCols[col]
        return col_label

    def GetTypeName(self, row, col):
        """
        Called to determine the kind of editor/renderer to use by
        default, doesn't necessarily have to be the same type used
        nativly by the editor/renderer if they know how to convert.
        Функция возвращает тип ячейки.
        @param row: Номер стоки
        @type row: C{int}
        @param col: Номер колонки
        @type col: C{int}
        @return: Возвращает тип ячейки.
        @rtype: C{string}
        """
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        """
        Called to determine how the data can be fetched and stored by the
        editor and renderer.  This allows you to enforce some type-safety
        in the grid.
        Функция возвращает признак того, что данная ячейка содержит значение
        определенного типа.
        @param row: Номер стоки
        @type row: C{int}
        @param col: Номер колонки
        @type col: C{int}
        @param typeName: Проверяемый тип
        @type typeName: C{string}
        @return: Возвращает признак того, что данная ячейка содержит значение определенного тип
        @rtype: C{bool}
        """
        colType = string.split(self.dataTypes[col], ':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        """
        Проверяет можно ли записать в ячейку значение определенного типа
        @param row: Номер стоки
        @type row: C{int}
        @param col: Номер колонки
        @type col: C{int}
        @param typeName: тип ячейки
        @type typeName: C{string}
        @return: Возвращает признак того, что в ячейку можно записать значение определенного типа
        @rtype: C{bool}
        """
        return self.CanGetValueAs(row, col, typeName)

    def GetAttr(self, row, col, par):
        """
        Определяет аттрибуты ячейки
        @param row: Номер записи
        @type row: C{int}
        @param col: Номер колонки
        @type col: C{int}
        @param par: ?
        @type par: C{int}
        @return: Аттрибут ячейки
        @rtype:  C{wx.grid.GridCellAttr}
        """
        self.evalSpace['row'] = row
        self.evalSpace['col'] = col
        self.evalSpace['self'] = self
        i = self.GetDataCol(col)
        attr = None
        attrRes = {}
        if i is None:
            return attr

        col = self.cols[i]
        #   Устанавливаем аттрибуты ячеек и колонок
        if row >= self.GetNumberRows()-1:
            #   Добавляем признак 'только для чтения'
            if col['attr'] in ['R', 'O', 'CR']:
                icAttrEditCell['readonly'] = 1
            else:
                icAttrEditCell['readonly'] = 0
            attr = getAttrBuff(icAttrEditCell)
        else:
            try:
                col_attr = col['cell_attr']
                #   Добавляем признак 'только для чтения'
                if col['attr'] in ['R', 'O', 'CR']:
                    col_attr['readonly'] = 1
                #   Сначала пытаемся вычислить аттрибут ячейки по спец. выражению в getattr
                if not self.GetView().getattr in [None, '']:
                    keyExpr = self.GetView().GetUUIDAttr('cell_attr', col['name'])
                    res, val = util.ic_eval(self.GetView().getattr, 0,
                                            self.evalSpace, 'Exception icGridDataSet.SetAttr()',
                                            compileKey=keyExpr)
                    if res:
                        attrRes = val

                if isinstance(attrRes, dict) or attrRes is None:
                    attrRes = util.icSpcDefStruct(col_attr, attrRes)
                    attr = getAttrBuff(attrRes)
                else:
                    attr = attrRes
            except:
                io_prnt.outErr(u'Error in GetAttr:')
                return None
        return attr

    def SetDataset(self, dataset):
        """
        Устанавливаем dataset.
        """
        self.dataset = dataset
        self.GetView().dataset = dataset


class icGridDataset(icGrid):
    """
    Класс представления данных в виде гида. Описание компонента и его функциональности
    ведется через списочную структуру ресурса. Данный класс включает в себя объект icGridDatasetData,
    который осуществляет взаимодействие с таблицей данных, которая в свою очередь устанавливает
    соединение с конкретным источником данных.
    """

    edt_resource_manager = None
    
    @staticmethod
    def GetEditorResourceManager():
        """
        Указатель на класс управления ресурсом в редакторе ресурсов.
        """
        if not icGridDataset.edt_resource_manager:
            icGridDataset.edt_resource_manager = icgriddataset_erm.ERMGridDataset
            icGridDataset.edt_resource_manager.component_class = icGridDataset
            
        return icGridDataset.edt_resource_manager
    
    def init_attr(self):
        """
        Функция устанавливает аттрибуты грида.
        """
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        wcols = self.LoadUserProperty('wcols')
        # Устанавливаем аттрибуты колонок и ячеек
        for col in self.cols:
            if col['attr'] != 'UV' and col['show']:
                #   Устанавливаем ширину колонок
                try:
                    i = GetColFromName(self.cols, col['name'])
                    try:
                        width = wcols[col['name']]
                    except:
                        width = util.getICAttr(col['width'], self.evalSpace,
                                               'ERROR in getICAttr() attr<width>=%s' % col['width'])
                    self.SetColSize(i, int(width))
                except:
                    io_prnt.outLastErr(u'GridDataset. Set col size')
        # Устанавливаем атрибуты ячеек по умолчанию
        if isinstance(self.cell_attr, dict):
            attr = self.cell_attr
            #   Устанавливаем шрифт ячеек по умолчанию
            if attr['font'] is not None:
                self.SetDefaultCellFont(icFont(attr['font']))
            if attr['alignment'] is not None:
                self.SetDefaultCellAlignment(attr['alignment'][0], attr['alignment'][1])
            #   Устанавливаем цвет фона ячеек по умолчанию
            clr = attr['backgroundColor']
            if clr:
                self.SetDefaultCellBackgroundColour(wx.Colour(*clr))
            else:
                self.SetDefaultCellBackgroundColour(
                    self.GetParent().GetBackgroundColour())
            #   Устанавливаем цвет текста ячеек по умолчанию
            clr = attr['foregroundColor']
            if clr:
                self.SetDefaultCellTextColour(wx.Colour(*clr))

        # Устанавливаем атрибуты шапки
        if isinstance(self.label_attr, dict):
            attr = self.label_attr
            #   Устанавливаем шрифт ячеек по умолчанию
            if attr['font'] is not None:
                self.SetLabelFont(icFont(attr['font']))
            #   Устанавливаем цвет фона ячеек по умолчанию
            clr = attr['backgroundColor']
            if clr is not None:
                self.SetLabelBackgroundColour(wx.Colour(clr[0], clr[1], clr[2]))
            #   Устанавливаем цвет текста ячеек по умолчанию
            clr = attr['foregroundColor']
            if clr is not None:
                self.SetLabelTextColour(wx.Colour(clr[0], clr[1], clr[2]))

        # Цвет сетки грида
        clr = self.line_color
        self.SetGridLineColour(wx.Colour(clr[0], clr[1], clr[2]))
        # Устанавливаем высоту шапки
        self.SetColLabelSize(self.label_height)
        # Определяем можно ли изменять мышкой рамеры колонок и строк
        self.EnableDragColSize(not self.resource['fixColSize'])
        self.EnableDragRowSize(not self.resource['fixRowSize'])
        # Определяем дополнительные редакторы
        self.RegisterDataType(wx.grid.GRID_VALUE_DATETIME,
                              wx.grid.GridCellStringRenderer(),
                              icEdt.icGridCellDateEditor())
        self.RegisterDataType(wx.grid.GRID_VALUE_STRING,
                              wx.grid.GridCellAutoWrapStringRenderer(),
                              icEdt.icDatasetComboCellEditor())
        self.RegisterDataType(GRID_TEXT_FORMAT,
                              wx.grid.GridCellAutoWrapStringRenderer(),
                              wx.grid.GridCellTextEditor())
        self.RegisterDataType(wx.grid.GRID_VALUE_STRING,
                              wx.grid.GridCellStringRenderer(),
                              icEdt.icGridCellNSIEditor())

        self.SetColMinimalAcceptableWidth(5)

        # Установить режим выбора
        self.SetSelectionMode(self.getSelectionModeAttr())

    def __init__(self, parent, id, res, logType=0, evalSpace=None, bCounter=False, progressDlg=None, data=None):
        """
        Конструктор класса.
        @param parent: Указатель на подительское окно. Обязательный параметр.
        @type parent: C{wx.Windows}
        @param id: Идентификатор компонента.
        @type id: C{int}
        @param res: Ресурсное описание компонента.
        @type res: C{Dictionary}
        @param logType: Тип доступа к логу.
        @type logType: C{int}
        @param evalSpace: Пространство имен формы, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @param data: Объек данных. Если он не указан (==None), то объект данных ищется по ресурсному описанию в пространстве имен формы.
        @type data: C{int}
        @return: Возвращает указатель на созданный объект
        @rtype: C{icGridBrows}
        """
        #   Каждая колонка грида может иметь свой редактор. Словарь editors хранит
        #   ссылки на редакторы по номеру колонки
        self.editors = {}
        self.last_editor = None
        icGrid.__init__(self, parent, id, res, evalSpace=evalSpace)
        self.SetSize(self.size)
        self.SetPosition(self.pos)
        if data:
            self.dataset = data
        #   Если имя таблицы не определено, описание берем из ресурса
        table = icGridDatasetData(logType, self, self.cols, self.source, evalSpace, self.dataset)
        if evalSpace is None:
            evalSpace = icContext.Context()
        self.evalSpace = evalSpace
        self.oldSelRow = 0
        self.saveChangeProperty = True
        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(table, True)
        self.table = table
        self.init_attr()
        #   Организуем пространство имен пользователя
        #   Добавляем все аттрибуты грида в пространство имен пользователя
        self.evalSpace['self'] = self
        self.evalSpace['data'] = self.dataset
        self.evalSpace['dataset'] = self.dataset
        try:
            self.evalSpace['dataclass'] = self.dataset.dataclass
        except:
            io_prnt.outLastErr(u'GridDataset. Set dataclass')

        # Обработчики событий
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.grid.EVT_GRID_EDITOR_CREATED, self.OnEditorCreat)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnSelected)
        self.Bind(wx.EVT_CLOSE, self.OnClose, parent)
        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnShownEditor)
        self.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN, self.OnHiddenEditor)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.Bind(icEvents.EVT_GRID_DESTROY, self.OnDestroyGrid)

        #   Сообщение post_select
        self.Bind(icEvents.EVT_GRID_POST_SELECT, self.OnPostSelect)
        #   Используется для того, чтобы предаставить пользователю вариант текста,
        #   который пользователь уже вводил
        self.Bind(icEvents.EVT_AUTO_TEXT_FILL, self.OnAutoTextFill)
        #   Флаг блокирующий обработку сообщения  <EVT_GRID_SELECT_CELL>
        self._isIgnoreSelectedAttr = False
        #   Флаг блокирующий обработку сообщения  <EVT_KEY_DOWN>
        self._isIgnoreKeyDown = False
        #   Первоначальный размер грида
        self.oldSize = self.dataset.getRecordCount()
        self.SetFocus()

        #
        #   Читаем служебные словари (частотный и ассоциативный
        #   словарь ввода)
        #
        #   Частотный словарь
        #   Признак разрешающий работать с частотным словарем
        self._enableFreqDict = self.resource.get('enable_freq_dict', False)

        if self.GetDataset() and self._enableFreqDict:
            freqDictName = 'dataclass_frequency_dict:'+self.GetDataset().name
            self._freqDict = frequencydict.icFrequencyDict(freqDictName)
        else:
            self._freqDict = None

        #   Словарь ассоциативных словарей, в качестве ключей, используется
        #   картеж, ключевых полей
        self._asscDict = None
        #
        #   Устанавливаем курсор в начало грида. За одно инициируем сообщение <EVT_GRID_SELECT_CELL>.
        #   Это необходимо для первоначальной фильрации данных, которая происходит по данному событию.
        try:
            self.SetCursor(self.oldSize)
        except:
            self.SetGridCursor(0, 0)

    def IsEnableFreqDict(self):
        """
        Возвращает значение признака, разрешающего работать с частотным
        словарем.
        """
        return self._enableFreqDict

    def EnableFreqDict(self, bEnable=True):
        """
        Включает или отклчает частотный словарь.
        """
        self._enableFreqDict = bEnable

    def AddAssociation(self, key_tuple, val_tuple, bPublicAssc=True):
        """
        Добавляет новую ассоциацию в грид.
        @type key_tuple: C{tuple}
        @param key_tuple: Ключевые поля ассоциации.
        @type val_tuple: C{tuple}
        @param val_tuple: Картеж полей значений ассоциации.
        @type bPublicAssc: C{bool}
        @param bPublicAssc: Признак таго, что будет использоваться сетевой словарь.
        @rtype: C{bool}
        @return: Признак успешного добавления.
        """
        if not self._asscDict:
            self._asscDict = {}

        if self.GetDataset():
            asscDictName = 'dataclass_association_dict:'+self.GetDataset().name+unicode(key_tuple)
            asscDict = associationdict.icAssociationDict(asscDictName, key_tuple, val_tuple)
            self._asscDict[key_tuple] = asscDict

    def OnAutoTextFill(self, evt):
        """
        Обрабатывает сообщение <icEvents.EVT_TEXT_TEMPL>. Используется для
        того, чтобы предаставить пользователю вариант текста, который он уже вводил.
        """
        if self._freqDict and self.IsEnableFreqDict():
            ctrl = evt.GetEventObject().GetTextCtrl()
            self._freqDict.AutoTextFill(ctrl, evt.GetData())

        evt.Skip()

    def GetColName(self, col):
        """
        Возвращает имя колонки.
        """
        try:
            return self.GetTable().colNames[col]
        except:
            io_prnt.outErr(u'### GRIDDATASET ERROR')

    def getNameValue(self, col_name, row=None):
        """
        Функция возвращает значение ячейки по номеру строки и имени поля.
        @param col_name: Имя колонки.
        @type col_name: C{int}
        @param row: Номер стоки. Если номер строки не задан, то значение берется из
            текущей строки.
        @type row: C{int}
        @return: Возвращает значение ячейки.
        """
        if row is None:
            row = self.GetGridCursorRow()

        col = self.GetTable().colNames.index(col_name)
        value = None
        if col >= 0 and row >= 0:
            value = self.GetTable().GetValue(row, col)

        return value

    def setNameValue(self, col_name, val, row=None):
        """
        Функция записывает значение ячейки по номеру строки и имени поля.
        @param col_name: Имя колонки.
        @type col_name: C{int}
        @param val: Значение.
        @type val: C{...}
        @param row: Номер стоки. Если номер строки не задан, то берется текущая строки.
        @type row: C{int}
        @return: Возвращает значение ячейки.
        """
        if row is None:
            row = self.GetGridCursorRow()
        col = self.GetTable().colNames.index(col_name)
        res = None
        if col >= 0 and row >= 0:
            res = self.GetTable().SetValue(row, col, val)

        return res

    def setColLabels(self, labelsDct):
        """
        Устанавливает новые значения заголовков колонок.
        @type lebelsDct: C{dictionary}
        @param labelDct: Словарь замен. Ключи - имена полей грида, значения -
            новые заголовки. Значения могут быть вычисляемыми.
        """
        for name, val in labelsDct.items():
            if name in self.GetTable().colNames:
                col = self.GetTable().colNames.index(name)
                self.GetTable().colLabels[col] = val
        self.Refresh()

    def ClearSortPrz(self):
        """
        Сбрасывает приознак сортировки у всех колонок.
        """
        try:
            for col, val in enumerate(self.cols):
                rndr = self.GetColLabelRenderer(col)
                rndr.sortDirection = 0
        except:
            io_prnt.outLog(u'Not found renderer for col=%d' % col)

    def SortCol(self, col, direction=None):
        """
        Функция сортирует заданную колонку.
        @type col: C{int}
        @param col: Номер колонки.
        @type direction: C{int}
        @param direction: Направление сортировки. 1 - по возрастанию, -1 по убыванию.
            Если не указано, то сортровка направления чередуются.
        """
        if self.GetDataset() is not None:
            fld = self.GetTable().colNames[col]
            rescol = self.GetTable().exCols[col]
            #   Проверяем есть ли по данной колонке индексное выражение либо
            #   выражение для сортировки (атрибут 'sort')
            if (not rescol['sort'] in [None, 0, '0', 'False', 'None']
                    or self.GetDataset().isFieldIndexed(fld)):
                #   Если поле вычисляемое, то честно вычисляем каждое поле, затем
                #   сортируем буфер идентификаторов в нужном нам порядке
                if rescol['attr'] in ['C', 'CR'] and fld not in self.GetDataset().getFieldList():
                    if not direction:
                        if self.GetDataset()._isSortDESC:
                            self.GetDataset()._isSortDESC = False
                        else:
                            self.GetDataset()._isSortDESC = True
                    else:
                        if direction == -1:
                            self.GetDataset()._isSortDESC = True
                        else:
                            self.GetDataset()._isSortDESC = False
                    sl = []
                    indexBuff = self.GetDataset().getIndexBuff()
                    for row in xrange(self.GetNumberRows()-1):
                        val = self.GetTable().GetValue(row, col)
                        sl.append((indexBuff[row], val))
                    #   Сортируем список, а затем собираем новый буфер идентификаторов
                    sl.sort(cmpRows)
                    newIndx = [x[0] for x in sl]
                    if self.GetDataset()._isSortDESC:
                        newIndx.reverse()
                    #   Устанавливаем новый буфер идентификаторов
                    self.GetDataset().setIndexBuff(newIndx)
                else:
                    self.GetDataset().SortField(fld, direction)

                try:
                    rndr = self.GetColLabelRenderer(col)
                    if self.GetDataset()._isSortDESC:
                        rndr.sortDirection = -1
                    else:
                        rndr.sortDirection = 1
                except:
                    io_prnt.outLog(u'Not found renderer for col=%d' % col)

                #   Обновляем грид
                self.ForceRefresh()

    def GetNumberRows(self):
        """
        Вычисляет количество строк в гриде.
        """
        return self.GetTable().GetNumberRows()

    def GetNumberCols(self):
        """
        Вычисляет количество строк в гриде.
        """
        return self.GetTable().GetNumberCols()

    def OnDClickEditor(self, evt):
        """
        Обрабатываем сообщение EVT_LEFT_DCLICK на редакторе ячейки.
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.eval_attr('dclickEditor')

        evt.Skip()

    def OnLabelRightClick(self, evt):
        """
        Обрабатываем сообщение EVT_GRID_LABEL_RIGHT_CLICK.
        """
        col = evt.GetCol()
        title = self.GetTable().exCols[col]['shortHelpString']
        if not title:
            title = self.GetTable().exCols[col]['label']

        x, y = evt.GetPosition()
        self._helpWin = icwidget.icShortHelpString(self, title, (x, y), 1500)
        evt.Skip()

    def OnLabelClick(self, evt):
        """
        Обрабатываем сообщение EVT_GRID_LABEL_LEFT_CLICK. Отменяем стандартную
        обработку этого сообщения. Для больших объемов информации в сетевом
        режиме выделение колонки может длится очень долго. Навешиваем на это
        событие сортировку таблицы, если в описании класса данных на данное
        поле стоит признак индекса. При первом нажатии сортируем по возрастанию,
        при втором по убыванию.
        """
        #   Определяем колонку
        col = evt.GetCol()
        self.SortCol(col)

    def GetDataset(self):
        """
        Возвращает указатель на объект данных icSQLObjDataSet.
        """
        return self.GetTable().dataset

    def OnDestroyGrid(self, evt=None):
        """
        Вызывается перед уничтожением грида.
        """
        row = self.GetGridCursorRow()
        #   Если данные в текущей строке были изменены запрашиваем подтверждение
        #   на сохранение изменений
        self.GetTable().Update(row, True)
        #   Убираем блокировки
        try:
            self.GetDataset().UnlockAll()
        except:
            io_prnt.outLastErr(u'GridDataset. UnlockAll')
        #
        #   Сохраняем системные настройки и настройки пользователя
        #
        #   Сохраняем размеры колонок грида
        wcols = {}
        for col in self.cols:
            try:
                i = GetColFromName(self.cols, col['name'])
                wcols[col['name']] = self.GetColSize(i)
            except:
                io_prnt.outLastErr(u'GridDataset. Save col size')

        self.SaveUserProperty('wcols', wcols)
        #   Сохраняем частотный словарь ввода
        if self._freqDict:
            self._freqDict.SaveDict()

        #   Сохраняем ассоциативные словари
        if self._asscDict:
            for dict_key in self._asscDict.keys():
                self._asscDict[dict_key].SaveDict()

        self.icGrid.Destroy()

    def ObjDestroy(self):
        """
        Функция уничтожения грида.
        """
        self.OnDestroyGrid()

    def OnPostSelect(self, evt):
        """
        Обрабатываем сообщение, которое генерируется после выбора ячейки.
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.eval_attr('post_select')
        evt.Skip()

    def OnSelected(self, evt):
        """
        Обрабатываем сообщение о выборе новой ячейки.
        """
        self.SetFocus()
        icGrid.OnSelected(self, evt)
        bPostsel = False
        #   В некоторых случаях эти сообщения генерируются функцией PostSelect, когда компонент
        #   еще не готов к работе
        try:
            row = evt.GetRow()
            col = evt.GetCol()
        except:
            row = self._selEventRow
            col = self._selEventCol
            bPostsel = True

        #
        #   Генерируем сообщение post_select
        event = icEvents.icGridPostSelectEvent(icEvents.icEVT_GRID_POST_SELECT, self.GetId())
        event.SetData((row, col))
        self.GetEventHandler().AddPendingEvent(event)
        #
        #   Вычисляем выражение, записанное в атрибуте 'selected'
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.evalSpace['row'] = row
        self.evalSpace['col'] = col
        #   Если установлен флаг блокировки обработку сообщения  <EVT_GRID_SELECT_CELL>,
        #   то функционал не обрабатываем
        if not self._isIgnoreSelectedAttr:
            self.eval_attr('selected')

        evt.Skip()
        #   Если изменился номер строки, то обновляем данные в базе и перемещаем
        #   курсор объекта данных в новое положение
        if self.dataset is not None:
            if self.oldSelRow != row:
                if self.oldSelRow < self.dataset.getRecordCount():
                    # Обновляем старую запись
                    self.GetTable().Update(self.oldSelRow)
                elif self.oldSelRow != row and self.dataset.isChangeRowBuff(self.oldSelRow):
                    #   Запрашиваем согласие на добавление записи
                    self.AddRows()
                self.dataset.Move(row)
        #   Уведомляем другие компоненты формы о том, что необходимо обновить
        #   представление
        self.UpdateRelObj()
        self.oldSelRow = row
        #
        #   Если заданы ассоциации, предлагаем вариант заполнения поля
        if not bPostsel and self._asscDict and self.GetTable().IsEmptyCell(row, col):
            fld_name = self.GetTable().colNames[col]
            for key, dct in self._asscDict.items():
                flds = dct.GetValueTuple()
                if fld_name in flds:
                    #   Создаем ключевой картеж
                    key_lst = range(len(key))
                    for indx, fld in enumerate(key):
                        if fld not in self.GetTable().colNames:
                            val = self.GetDataset().getNameValue(fld, row)
                        else:
                            val = self.GetView().getNameValue(fld, row)
                        key_lst[indx] = val

                    #   Ищем вариант
                    val = dct.GetAssociateFld(tuple(key_lst), fld_name)
                    #   Если нашли вариант, то открываем редактор ячейки
                    #   заносим найденое значение и выделяем его
                    if val:
                        ret = self.GetView().setNameValue(fld_name, val, row)
                        #   Если вариант не прошел контроль, то выкидываем его из
                        #   словаря ассоциаций
                        if ret not in (IC_CTRL_OK, IC_CTRL_REPL):
                            result = dct.DelAssociation(tuple(key_lst))
                            break

    def OnEditorCreat(self, evt):
        """
        Отлавливаем сообщение на создание редактора, чтобы перенаправить обработку в свою функцию.
        Сообщение на создание редактора всегда генерируется после обработки
        события <EVT_GRID_EDITOR_SHOWN> в функции OnShownEditor().
        @param evt: Обработчик событий
        @type evt: C{wx.grid.GridEvent}
        """
        row = evt.GetRow()
        col = evt.GetCol()
        if self.GetTable().CanGetValueAs(row, col, wx.grid.GRID_VALUE_STRING):
            self.GetTable().row = row
            self.GetTable().col = col
            self.GetTable().oldVar = self.GetTable().GetValue(row, col)
            editor = evt.GetControl()
            # ВНИМАНИЕ! Для редактора НСИ необходимо
            # сделать привязку к справочнику
            if self.GetTable().exCols[col]['pic'] == 'NSI':
                try:
                    editor.setNSIPsp(self.GetTable().exCols[col]['nsi_psp'])
                except:
                    io_prnt.outLastErr(u'Set NSI external grid cell editor')
            #   Если не поставить такой стиль, то в диалоговом окне ENTER в
            #   редакторе не отрабатывает
            style = editor.GetTextCtrl().GetWindowStyle()
            editor.GetTextCtrl().SetWindowStyle(style | wx.TE_PROCESS_ENTER)
            self.editors[col] = editor
            self.last_editor = editor

            #   Для всех однотипных ячеек проставим созданный редактор
            for i, typ in enumerate(self.GetTable().dataTypes):
                if i != col and i not in self.editors and typ == self.GetTable().GetTypeName(None, col):
                    self.editors[i] = editor
            editor.Bind(wx.EVT_KEY_DOWN, self.OnKeyDownEditor)
            editor.GetTextCtrl().Bind(wx.EVT_LEFT_DCLICK, self.OnDClickEditor)
            sx, sy = self.GetColSize(col), self.GetDefaultRowSize()

    def OnShownEditor(self, evt):
        """
        Обрабатывает сообщение о начале редактирования.
        """
        # Если поставить Skip, то данное сообщение будет обрабатываться
        # и другими гридам. Это может приводить к проблемам с блокировками
        row = evt.GetRow()
        col = evt.GetCol()
        #   Блокируем запись для редактирования, если позволяет объект данных
        if self.GetDataset():
            try:
                result = self.GetDataset().Lock(row)
                if not result:
                    msg = ic_lock.readMessage(self.GetDataset().getDBTableName(), self.dataset.getId(row))
                    try:
                        msg = eval(msg)
                        msg = msg['user']
                    except:
                        io_prnt.outLastErr(u'GridDataset. read lock message')
                    MsgBox(self.GetView(), u'Запись заблокирована пользователем: <%s>' % unicode(msg, 'utf-8'))
            except:
                io_prnt.outErr(u'GRIDDATASET LOCK ERROR')
        try:
            editor = self.editors[col]
        #   Если для колонки спец. редактора нет, то пробуем взять последний созданный
        except:
            editor = self.last_editor

        if editor is not None and editor.GetButton():
            if self.GetTable().exCols[col]['hlp'] in [None, '', 'None']:
                editor.GetButton().Enable(False)
            else:
                editor.GetButton().Enable(True)

        evt.Skip()

    def OnKeyDownEditor(self, evt):
        """
        Функция обработки нажатия клавиши в редакторе (компонент wx.TextCtrl).
        @param evt: Обработчик событий
        @type evt: C{wx.CommandEvent}
        """
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        self.GetTable().row = row
        self.GetTable().col = col
        #   Определяем формат ввода данных ячейки
        try:
            if col not in self.editors and not self.IsCellEditControlEnabled():
                self.EnableCellEditControl()
                return
            editor = self.editors[col]
            type = self.GetTable().exCols[col]['spctype']
            if self.IsCellEditControlEnabled():
                text = editor.GetValue()
            else:
                text = ''

            kcod = evt.GetKeyCode()
            bCtrl = evt.ControlDown()
            bShift = evt.ShiftDown()
            bAlt = evt.AltDown()
            templ = self.GetTable().exCols[col]['pic']
            if (kcod not in (wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_BACK, wx.WXK_UP, wx.WXK_DOWN,
                wx.WXK_HOME, wx.WXK_DELETE, wx.WXK_END) and not bAlt
                and not (kcod == wx.WXK_INSERT and bShift)
                and not (kcod == wx.WXK_INSERT and bCtrl)
                and not bCtrl and kcod != wx.WXK_F1):
                #   Проверяем соответствут вводимый символ шаблону вывода
                #   При необходимости вставляет символы форматирования
                if not PrepareTextByTempl(editor.GetTextCtrl(), type, templ, text, kcod):
                    return
                # --------------------------------------------
                #   Посылаем сообщение для поиска вариантов
                #   продолжения текста
                if self.IsEnableFreqDict() and type in (IC_N_STRING_FORMAT, IC_STRING_FORMAT):
                    event = icEvents.icAutoTextFillEvent(icEvents.icEVT_AUTO_TEXT_FILL, self.GetId())
                    event.SetData(self.GetTable().exCols[col]['name'])
                    event.SetEventObject(editor)
                    self.GetEventHandler().AddPendingEvent(event)
                # --------------------------------------------

            elif kcod in [wx.WXK_UP, wx.WXK_DOWN] and not bCtrl and not bShift and not bAlt:
                self.DisableCellEditControl()
                if kcod == wx.WXK_UP:
                    self.MoveCursorUp(False)
                else:
                    self.MoveCursorDown(False)
            elif kcod == wx.WXK_DELETE:
                pass
        except:
            io_prnt.outErr(u'KEYDOWN EDITOR ERROR')

        evt.Skip()

    def OnHiddenEditor(self, evt):
        """
        Обработка сообщения о закрытии редактра
        @param evt: Обработчик событий
        @type evt: C{wx.grid.GridEvent}
        """
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        try:
            editor = self.editors[col]
        except:
            editor = self.last_editor

        if editor is not None and hasattr(editor, 'buttonF1') and editor.buttonF1 is not None:
            editor.buttonF1.Enable(False)

        #   Разблокируем запись для редактирования, если объект данных поддерживает блокировки
        try:
            self.GetDataset().Unlock(row)
        except:
            io_prnt.outLastErr(u'GridDataset. Unlock row <%s>' % row)

        evt.Skip()

    def OnButtonExtend(self, evt):
        """
        Нажатие кнопки внешнего редектора.
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        x, y = evt.GetPosition()
        #   Приходится извращается так как кнопка может перехватывать сообщение
        #   EVT_LEFT_DOWN c EVT_BUTTON вообще перестало работать с
        #   версии wx 2.6.1.0
        if x >= 0 and y >= 0:
            self.OnExtend()
        else:
            self.DisableCellEditControl()
            evt.Skip()

    def OnExtend(self):
        """
        Обрабатывается клавиша F1 (help) и нажатие кнопки в редакторе ячейки.
        """
        self.DisableCellEditControl()
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        self.val = self.GetTable().GetValue(row, col)

        #   Устанавливаем буфферные переменные
        self.GetTable().row = row
        self.GetTable().col = col
        self.GetTable().value = self.val
        result = None
        try:
            hlp = self.GetTable().exCols[col]['hlp']
            try:
                attr = self.GetTable().exCols[col]['attr']
            except KeyError:
                attr = 'W'

            if hlp not in [None, ''] and not attr in ['R', 'O', 'CR']:
                keyExpr = self.GetUUIDAttr('hlp', self.GetTable().exCols[col]['name'])
                ret, val = util.ic_eval(hlp, 0, self.evalSpace, 'hlp:' + hlp,
                                        compileKey=keyExpr)
                if ret and val is not None:
                    #   Если возвращаемое значение картеж, то первый элемент
                    #   код выбора, второй значение выбора в виде картежа, третий словарь
                    #   полей, которые надо дополнительно заполнить, четвертый
                    #   занчение в виде строки.
                    flds_vals = None
                    if isinstance(val, tuple):
                        if len(val) >= 4:
                            codHlp, ret_val, flds_vals, strval = val
                            ret_val = strval.rstrip()
                        elif len(val) == 3:
                            codHlp, ret_val, flds_vals = val
                        else:
                            # Нет редактора для этого типа
                            codHlp = IC_HLP_FAILED_IGNORE

                        if codHlp == IC_HLP_OK or (codHlp == IC_HLP_REPL and MsgBox(self.GetView(),
                                _('Do you really want choose value: %s?') % ret_val,
                                style=wx.YES_NO | wx.ICON_QUESTION) == wx.ID_YES):
                            bChoose = True
                        else:
                            bChoose = False
                    else:
                        ret_val = val
                        bChoose = True

                    #   Если возвращено значение для заполнения
                    if bChoose and ret_val is not None:
                        #   Если возвращаемое значение картеж, то собираем из
                        #   него строку
                        if isinstance(ret_val, tuple):
                            ret_val = ''.join([unicode(x) for x in ret_val])
                        else:
                            ret_val = unicode(ret_val)
                        ctrl_cod = self.GetTable().UpdateCell(row, col, ret_val)
                        self.Refresh()
                        #   Если указан словарь дополнительных значений, то
                        #   устанавливаем их
                        if ctrl_cod in [IC_CTRL_OK, IC_CTRL_REPL] and flds_vals:
                            for fld in flds_vals.keys():
                                val = flds_vals[fld]
                                #   По имени поля ищем номер колонки
                                if fld in self.GetTable().colNames:
                                    column = self.GetTable().colNames.index(fld)
                                    self.GetTable().UpdateCell(row, column, val)
                                else:
                                    ctrlFld = self.dataset.setNameValue(fld, val, row)
                                    if ctrlFld == IC_CTRL_FAILED:
                                        MsgBox(self, _('Invalid field value %s, col=%d, row=%d') % (fld, col, row))
        except:
            io_prnt.outErr(_('Analize return code error <hlp>: %s') % val)

        self.SetFocus()
        self.SetCursor(row)

    def OnKeyDown(self, evt):
        """
        Обработка нажатия клавиш в гриде.
        @param evt: Обработчик событий
        @type evt: C{wx.grid.GridEvent}
        """
        if self._isIgnoreKeyDown:
            return

        self.evalSpace['evt'] = evt
        keycod = evt.GetKeyCode()
        bCtrl = evt.ControlDown()
        bShift = evt.ShiftDown()
        #
        #   Выполняем выражение обработки нажатия клавиш клавиатуры. Пока работает
        #   обработчик блокируем обработку сообщений от клавиатуры.
        self._isIgnoreKeyDown = True
        bSkip = True
        if self.keydown:
            ret, val = self.eval_attr('keyDown')
            if ret and not val is None:
                try:
                    bSkip = bool(val)
                except:
                    LogLastError(u'')
                    bSkip = True

        self._isIgnoreKeyDown = False
        if not bSkip:
            return

        #   Закончилт вычислять атрибут keyDown
        #
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        #   Стандартный вызов функции справки
        if keycod == wx.WXK_F1:
            self.OnExtend()
        #   Вызываем процедуру удаления строки
        elif keycod == wx.WXK_DELETE:
            self.GetTable().DeleteRows(row)
        #   Запрашиваем разрешение на удаление буфера строки
        elif keycod == wx.WXK_ESCAPE:
            row = self.GetGridCursorRow()
            if self.GetTable().data.isChangeRowBuff(row):
                retmsg = MsgBox(self.GetView(), u'Отменить изменения (GridDataset)?',
                                style=wx.YES_NO | wx.ICON_QUESTION)
                if retmsg == wx.ID_YES:
                    self.GetTable().data.clearChangeRowBuff(row)
                    self.UpdateRelObj()
                    self.DisableCellEditControl()
                else:
                    self.GetTable().Update()
            evt.Skip()
        elif keycod == 83 and evt.ControlDown():
            self.GetTable().Update()
        elif keycod in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            self.DisableCellEditControl()
            success = self.MoveCursorRight(False)
            if not success:
                if row + 1 < self.GetTable().GetNumberRows():
                    self.SetGridCursor(row+1, 0)
                    self.MakeCellVisible(row+1, 0)
                else:
                    if self.AddRows():
                        self.SetGridCursor(row+1, 0)
                        self.MakeCellVisible(row+1, 0)
                    else:
                        self.SetGridCursor(row, 0)
                        self.MakeCellVisible(row, 0)
            self.PostSelect()
            self._isIgnoreKeyDown = False
            return

        # Ctrl-Home
        elif keycod == wx.WXK_HOME and evt.ControlDown():
            self.SetGridCursor(0, 0)
            self.MakeCellVisible(0, 0)
            self.PostSelect()
        # Ctrl-End
        elif keycod == wx.WXK_END and evt.ControlDown():
            maxrow = self.GetNumberRows()
            maxcol = self.GetNumberCols()
            if maxcol > 0:
                self.SetGridCursor(maxrow-1, maxcol-1)
                self.MakeCellVisible(maxrow-1, maxcol-1)
            self.PostSelect()

        elif keycod == wx.WXK_HOME:
            self.SetGridCursor(row, 0)
            self.MakeCellVisible(row, 0)
            self.PostSelect()
        elif keycod == wx.WXK_END:
            maxcol = self.GetTable().GetNumberCols()
            if maxcol > 0:
                self.SetGridCursor(row, maxcol-1)
                self.MakeCellVisible(row, maxcol-1)
            self.PostSelect()
        elif keycod == wx.WXK_TAB:
            self.DisableCellEditControl()
            evt.Skip()
        elif keycod == wx.WXK_INSERT and not evt.ControlDown() and not evt.ShiftDown() and not evt.AltDown():
            self.DisableCellEditControl()
            self.AddRows()
        elif keycod == wx.WXK_INSERT and evt.ControlDown() and self.CanEnableCellControl():
            self.EnableCellEditControl()
            #   Копируем значение в Clipboard
            try:
                self.editors[col].Copy()
            except:
                io_prnt.outLastErr(u'GridDataset. Copy clipboard')
        elif keycod == wx.WXK_INSERT and evt.ShiftDown() and self.CanEnableCellControl():
            self.EnableCellEditControl()
            #   Копируем значение из Clipboard
            try:
                self.editors[col].Paste()
            except:
                io_prnt.outLastErr(u'GridDataset. Paste clipboard')
        elif keycod in (wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP, wx.WXK_DOWN):
            evt.Skip()
        else:
            evt.Skip()

    def SetCursor(self, row, col=-1):
        """
        Устанавливает курсор в нужную позицию.
        @type row: C{int}
        @param row: Номер записи.
        @type col: C{int}
        @param col: Номер колонки.
        """
        cur_row = self.GetGridCursorRow()
        cur_col = self.GetGridCursorCol()
        if col < 0:
            col = cur_col
        if row < 0:
            row = 0
        rows = self.GetTable().GetNumberRows()
        if row >= rows:
            row = rows - 1

        self._selEventRow = row
        self._selEventCol = col
        self.SetGridCursor(row, col)
        self.MakeCellVisible(row, col)

    def RefreshGrid(self):
        """
        Перечитывает данные и перерисовывает грид.
        """
        self.GetDataset().Refresh()
        name = self.GetDataset().name
        self.UpdateDataView(name)

    def Update(self, row=None, bAsk=False):
        """
        Записываем изменения данных в строке.
        """
        return self.GetTable().Update(row, bAsk)

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
            db_name = self.GetDataset().name

        codCtrl = IC_CTRL_FAILED
        if self.dataset is not None and self.dataset.name == db_name:
            codCtrl = IC_CTRL_OK

        return codCtrl

    def UpdateViewFromDB(self, db_name=None):
        """
        Обновляет данные в текстовом поле после изменения курсора в источнике данных.
        @type db_name: C{String}
        @param db_name: Имя объекта данных.
        """
        #   Если класс данных не задан, то считаем, что объект необходимо обновить
        if db_name is None:
            db_name = self.dataset.name

        if self.dataset is not None and self.dataset.name == db_name and self.bStatusVisible:
            if self.dataset.Recno() != self.GetGridCursorRow():
                self.SetCursor(self.dataset.Recno())

    def UpdateDataView(self, db_name):
        """
        Обновляет вид грида после изменения размеров таблицы данных.
        @type db_name: C{String}
        @param db_name: Имя объекта данных.
        """
        #   Если размер грида не совпадает с размерами данных, то подстраиваем размер грида
        try:
            if self.GetDataset() is not None and self.GetDataset().name == db_name:
                cur = self.GetDataset().getRecordCount()
                oldSize, dataSize = self.oldSize, cur
                num = oldSize - dataSize
                if oldSize > dataSize:
                    self.SendDelMess(cur, num)
                elif oldSize < dataSize:
                    num = dataSize - oldSize
                    self.SendAddMess(num)

                self.ForceRefresh()
        except:
            io_prnt.outLog(u'Exception in UpdateDataView')

    def AddRows(self, num=1, bAddData=True):
        """
        Добавляет несколько рядов в грид.
        @type num: C{int}
        @param num: Количество добавляемых рядов.
        @type bAddData: C{bool}
        @param bAddData: Признак того, что в источник данных необходимо добавить записи. В противном случае будут
            добавляться только строки грида.
        """
        count = num
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        #   Для начала перемещаем курсор на последнюю строку
        maxrow = self.GetTable().GetNumberRows()
        if maxrow-1 > row:
            self.SetGridCursor(maxrow-1, col)
            self.MakeCellVisible(maxrow-1, col)
        #   Делаем через представление таблицы для того, чтобы вычислить выражения ресурса
        if bAddData:
            count = 0
            for i in range(num):
                count += int(self.GetTable().AddRow(row, col, None))

        ret = self.SendAddMess(count)
        return ret

    def DelRows(self, cur, num=1):
        """
        Удаляет несколько рядов из грида.
        @type cur: C{int}
        @param cur: Номер строки, которую надо удалить .
        @type num: C{int}
        @param num: Количество удаляемых рядов.
        """
        self.GetTable().DeleteRows(cur, num)

    def getCurrentRow(self):
        """
        Номер текущей выделенной строки.
        """
        return self.GetGridCursorRow()

    def getCurrentCol(self):
        """
        Номер текущей выделенной колонки.
        """
        return self.GetGridCursorCol()

    def addRow(self):
        """
        Добавить одну строку.
        """
        return self.AddRows()

    def delCurrentRow(self):
        """
        Удалить текущую строку.
        """
        row = self.getCurrentRow()
        return self.DelRows(row)

    def SendAddMess(self, num):
        """
        Функция посылает сообщение на добавление строк в грид.
        """
        if num <= 0:
            return False

        try:
            msg = wx.grid.GridTableMessage(self.GetTable(), wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, num)
            self.ProcessTableMessage(msg)
        except:
            return False

        if self.dataset:
            self.oldSize = self.dataset.getRecordCount()

        return True

    def SendDelMess(self, cur, num):
        """
        Функция посылает сообщение на добавление строк в грид.
        """
        if num <= 0 or cur < 0:
            return False
        try:
            msg = wx.grid.GridTableMessage(self.GetTable(), wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, cur, num)
            self.ProcessTableMessage(msg)
        except Exception:
            io_prnt.outLog(u'Exception, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED')
            return False

        if self.dataset:
            self.oldSize = self.dataset.getRecordCount()

        return True

    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()

    def OnClose(self, evt):
        if self.data is not None:
            self.data.Close()
        evt.Skip()

    def set_struct_filter(self, **flt):
        """
        Устанавливаем структурный фильтр на нужный объект данных,
        к которому присоединен грид.
        """
        if flt:
            return self.SetFilter(self.resource['source'], flt, True, False)

    def SetFilter(self, clsName, flt=None, isUpdSelf=False, bReplNames=True):
        """
        Устанавливаем фильтр на нужный объект данных.
        @type clsName: C{string}
        @param clsName: Имя класса данных на который устанавливается фильтр.
        @type filter: C{string | dictionary}
        @param filter: Фильтр, накладываемый на класс данных.
        @type isUpdSelf: C{bool}
        @param isUpdSelf: Признак того, что необходимо обновлять и состояние
            текущего объекта.
        @type bReplNames: C{bool}
        @param bReplNames: Признак того, что предварительно необходимо провести
            замену имен из SQLObject представления в представление SQL базы.
        """
        try:
            dataset = self.evalSpace['_sources'][clsName]
            real_name = dataset.name
            gridList = []
            try:
                #   Находим список гридов, в которых необходимо сделать Update
                gridList = [x for x in self.evalSpace['_has_source'].values() if x.type == 'GridDataset' and x.source == real_name]
                for gr in gridList:
                    gr.GetTable().Update()
            except:
                io_prnt.outErr(u'')

            #   Если буфер заполнен, то необходимо запросить потверждение на
            #   обновление данных и обновить данные. В противном случае изменения
            #   будут потеряны
            if not gridList and not dataset.IsEOF() and dataset.isChangeRowBuff() and MsgBox(self.GetView(),
               u'Сохранить изменения?', style=wx.YES_NO | wx.ICON_QUESTION) == wx.ID_YES:
                dataset.update()

            if flt:
                dataset.FilterFields(flt, bReplNames=bReplNames)

            #   Уведомляем другие компоненты формы о том, что
            #   состояние объекта данных могло измениться
            for key in self.evalSpace['_has_source'].keys():
                try:
                    if key != self.name or isUpdSelf:
                        self.evalSpace['_has_source'][key].UpdateViewFromDB(real_name)
                        #   Обновляем связанные гриды
                        self.evalSpace['_has_source'][key].UpdateDataView(real_name)
                except:
                    io_prnt.outLastErr(u'GridDataset. Update view')
        except KeyError:
            MsgBox(self.GetView(), _('Dataclass %s is not defined in context.') % clsName)
        except:
            io_prnt.outErr(u'Error in ic.components.iclistdataset.setFilter')

    def SetFilterField(self, clsName, fieldName, value=None, bReplNames=True):
        """
        Устанавливаем фильтр на объект группы (связь один ко многим).
        @type clsName: C{string}
        @param clsName:  Имя класса данных, который фильтруется
        @type fieldName: C{string}
        @param fieldName: Поле в классе данных, по которому фильтруем.
        @type value: C{int}
        @param value: Значение поля.
        @type bReplNames: C{bool}
        @param bReplNames: Признак того, что предварительно необходимо провести
            замену имен из SQLObject представления в представление SQL базы.
        """
        try:
            dataset = self.evalSpace['_sources'][clsName]
            real_name = dataset.name
            gridList = []
            try:
                #   Находим список гридов, в которых необходимо сделать Update
                gridList = [x for x in self.evalSpace['_has_source'].values() if x.source == real_name and x.type == 'GridDataset']
                for gr in gridList:
                    gr.GetTable().Update()
            except:
                LogLastError(u'')

            #   Если буфер заполнен, то необходимо запросить потверждение на
            #   обновление данных и обновить данные. В противном случае изменения
            #   будут потеряны
            if not gridList and dataset.isChangeRowBuff() and MsgBox(self.GetView(),
               u'Сохранить изменения?', style=wx.YES_NO | wx.ICON_QUESTION) == wx.ID_YES:
                dataset.update()

            dataset.FilterField(fieldName, value, bReplNames=bReplNames)
            #   Уведомляем другие компоненты формы о том, что состояние объекта данных могло измениться
            for key in self.evalSpace['_has_source'].keys():
                try:
                    if key != self.name:
                        self.evalSpace['_has_source'][key].UpdateViewFromDB(clsName)
                        self.evalSpace['_has_source'][key].UpdateDataView(clsName)
                except:
                    io_prnt.outLastErr(u'GridDataset. Update view')
        except KeyError:
            MsgBox(self.GetView(), _('Dataclass %s is not defined in context.') % clsName)
        except:
            io_prnt.outErr(u'Error in ic.components.icgriddataset.SetFilterField')

    def GetView(self):
        return self


def defColDBDescription(col):
    """
    По описанию колонки грида генерирует описание поля базы данных.
    @type col: C{Dictionary}
    @param col: Ресурсное описание колонки грида.
    @rtype: C{Dictionary}
    @return: Описание поля для таблицы данных.
    """
    cell_type, wx_type = defPicType(col['pic'], col['valid'])
    if col['attr'] in (u'c', u'C', u'cr', u'CR'):
        attr = icdataset.icVirtualFieldType
    else:
        attr = icdataset.icNormalFieldType

    if cell_type in ICDB_StringType:
        cell_type = icdataset.icTextFieldType
    elif cell_type in ICDB_NumberType:
        cell_type = icdataset.icNumberFieldType
    elif cell_type in ICDB_DoubleType:
        cell_type = icdataset.icDoubleFieldType
    elif cell_type in ICDB_DateTimeType:
        cell_type = icdataset.icDateTimeFieldType

    def_field = {'type': cell_type, 'attr': attr, 'setvalue': col['setvalue'],
                 'getvalue': col['getvalue'], 'init': col['init']}
    return def_field


def createSimpleGrid(parent, *columns):
    """
    Создание простого грида (c icSimpleDataset).
    @param parent: Родительское wx.Window.
    @param columns: Описания колонок в формате:
        {'name': Латинское наименование колонки.
        'label': Надпись колонки,
        'width': Ширина колонки,
        'pic': Шаблон заполнения значений колонки,
        'nsi_psp': Паспорт cправочника, если не надо то None}
    @return: Объект icGridDataset.
    """
    fields_res = list()
    for column in columns:
        spc = copy.deepcopy(SPC_IC_CELL)
        spc['name'] = column.get('name', 'default_field')
        fields_res.append(spc)
    dataset_res = dict(description=fields_res)
    dataset = icsimpledataset.icSimpleDataset(-1, dataset_res)

    grid_res = copy.deepcopy(SPC_IC_GRID_DATASET)
    grid_columns = list()
    for column in columns:
        spc = copy.deepcopy(SPC_IC_CELL)
        spc['name'] = column.get('name', 'default_col')
        spc['pic'] = column.get('pic', 'S')
        spc['label'] = column.get('label', 'col')
        spc['width'] = column.get('width', 100)
        nsi_psp = column.get('nsi_psp', None)
        if nsi_psp:
            spc['pic'] = 'CH'
            sprav = ic.getKernel().Create(nsi_psp)
            choice_tree = sprav.getDataTree()

            def _get_choice_list(tree, choice_list):
                for rec in tree:
                    cod = rec['name']
                    name = rec['__record__'][1]
                    choice_list.append(u'%s %s' % (cod, name))
                    # Обработка дочерних элементов
                    if rec['child']:
                        choice_list = _get_choice_list(rec['child'], choice_list)
                return choice_list
            choice_list = _get_choice_list(choice_tree, [])
            spc['valid'] = u','.join(choice_list)

        grid_columns.append(spc)
    grid_res['cols'] = grid_columns

    grid = icGridDataset(parent, -1, grid_res, data=dataset)
    return grid


if __name__ == '__main__':
    pass
