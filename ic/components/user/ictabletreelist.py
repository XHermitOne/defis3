#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Иерархический справочник.
Класс пользовательского визуального компонента.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import copy
import wx
import wx.gizmos as parentModule

import ic.components.icwidget as icwidget
import ic.utils.util as util
from ic.log import log
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
from ic.dlg.msgbox import MsgBox

#   Тип компонента
ic_class_type = icDefInf._icComboType

#   Имя класса
ic_class_name = 'icTableTreeList'

#   Описание стилей компонента
ic_class_styles = {'TR_NO_BUTTONS': wx.TR_NO_BUTTONS,
                   'TR_HAS_BUTTONS': wx.TR_HAS_BUTTONS,
                   'TR_NO_LINES': wx.TR_NO_LINES,
                   'TR_LINES_AT_ROOT': wx.TR_LINES_AT_ROOT,
                   'TR_SINGLE': wx.TR_SINGLE,
                   'TR_MULTIPLE': wx.TR_MULTIPLE,
                   'TR_EXTENDED': wx.TR_EXTENDED,
                   'TR_HAS_VARIABLE_ROW_HEIGHT': wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                   'TR_EDIT_LABELS': wx.TR_EDIT_LABELS,
                   'TR_HIDE_ROOT': wx.TR_HIDE_ROOT,
                   'TR_ROW_LINES': wx.TR_ROW_LINES,
                   'TR_FULL_ROW_HIGHLIGHT': wx.TR_FULL_ROW_HIGHLIGHT,
                   'TR_DEFAULT_STYLE': wx.TR_DEFAULT_STYLE,
                   'TR_TWIST_BUTTONS': wx.TR_TWIST_BUTTONS,
                   'TR_MAC_BUTTONS': wx.TR_MAC_BUTTONS}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'TableTreeList',
                'name': 'default',

                'fields': [],
                'labels': [u'Структура'],
                'codfield': [],
                'filterExpr': None,
                'selected': None,
                'activated': None,
                'titleRoot': '',
                'init_sprav_buff': None,
                'wcols': [],
                'style': wx.TR_DEFAULT_STYLE,

                '__styles__': ic_class_styles,
                '__events__': {'selected': ('wx.EVT_TREE_SEL_CHANGED', 'OnSelected', False),
                               'activated': ('wx.EVT_TREE_ITEM_ACTIVATED', 'OnActivated', False),
                               'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDWN', False),
                               },
                '__attr_types__': {0: ['name', 'type', 'mask', 'titleRoot', 'orderBy'],
                                   icDefInf.EDT_TEXTLIST: ['fields', 'labels', 'codfield', 'wcols'],
                                   12: ['selected', 'activated'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTreeListCtrl'
ic_class_pic2 = '@common.imgEdtTreeListCtrl'

#   Путь до файла документации
ic_class_doc = 'ic.components.user.icspravtreelist.SpravTreeList-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 3)

# --- Идентификаторы состояний строки
ROW_STATE_NORMAL = 0
ROW_STATE_RED = 1
ROW_STATE_YELLOW = 2


def _example_state_func(row):
    """
    """
    try:
        if row[2] < 0:
            return ROW_STATE_RED
        elif row[2] > 10000:
            return ROW_STATE_YELLOW
    except:
        pass
    
    return ROW_STATE_NORMAL


class icTableTreeList(icwidget.icWidget, parentModule.TreeListCtrl):
    """
    Класс представления таблицы в виде дерева. Используется для отображения
    небольших таблиц (максимум несколько тысяч записей), поскольку все записи
    буферизируются.
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{name='default'}:
        - B{labels=[]}: Список заголовков колонок.
        - B{wcols=[]}: Список размеров колонок. C{Пример:[100,20]}.
        - B{fields=[]}: Список дополнительных отображаемых полей. C{Пример: ['n1']}.
        - B{codfield=[]}: Список описаний аналитических полей. Описание поля является
            картежем; первый элемент имя поля, второй описание, подстроки, которая
            содержит аналитическую информацию; None означает, что в качестве
            структурной строки берется все значение поля; третий элемент
            описывает ссылку на справочник (<тип справочника>, <поле значения>);
            пример:
            [('cod',(0,2), None), ('cod',(2,4), None), ('field1',None, ('agent','s1')),
                ('field2',None, None)]
            
        - B{filterExpr=''}: Выражение (В синтаксисе SQLObject), по которому
            обираются строки таблицы.
            Пример 1 (SQL syntax): 'table.type='PR' and table.cod='ER''
            Пример 2 (SQLBuilder syntax): 'AND(Table.q.type=='PR', Table.q.cod=='ER')'
            
        - B{init_sprav_buff=None}: Выражение, возвращающее буфер необходимых
            справочников.
        - B{titleRoot=''}: Заголовок корневого элемента.
        - B{selected=None}: Выражение после выбора элемента.
        - B{activated=None}: Выражение после выбора элемента по <Enter> или двойному щелчку
            мыши.
        - B{type='TableTreeList'}: Тип компонента.
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

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
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.TreeListCtrl.__init__(self, self.parent, id, self.position, self.size,
                                           style=self.style)

        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        
        self.fldridx = fldridx = il.Add(common.imgFolder)
        self.fldropenidx = fldropenidx = il.Add(common.imgFolderOpen)
        self.fileidx = fileidx = il.Add(common.imgEdtTBTool)
        self.smileidx = smileidx = il.Add(common.imgPage)
        
        self.folderRedIdx = il.Add(common.imgFolderRed)
        self.folderYellIdx = il.Add(common.imgFolderYell)
        self.folderOpenRedIdx = il.Add(common.imgFolderOpenRed)
        self.folderOpenYellIdx = il.Add(common.imgFolderOpenYell)
        self.fileidxItemRed = il.Add(common.imgEdtTBToolRed)
        self.fileidxItemYell = il.Add(common.imgEdtTBToolYell)

        self.SetImageList(il)
        self.il = il
        
        #   Словарь связывает структурный код и узел дерева
        self._codItemDict = {}

        #   Буфер справочников. В качестве ключей типы
        #   справочников, в качестве значений списки словарей, у которых имена
        #   полей являются ключами.
        #   Пример: {'agent':[{'cod':'PD01', 'fio':'Петров А.П.'}, ...], ...}
        self._spravBuff = None

        #   Признак инициализации дерева
        self._bInit = 0
        self._indicator = None
        
        #   Указатель на функцию оценки состояния
        self._stateFunction = None
        
        # create some columns
        if not self.fields:
            self.fields = ['name']
            
        #   Читаем сохраненные настройки пользователя
        wcols = self.LoadUserProperty('wcols')
        if wcols:
            self.wcols = wcols
            
        self.SetMainColumn(0)   # the one with the tree in it...
        
        for indx, label in enumerate(self.labels):
            self.AddColumn(label)
            
            if len(self.wcols) > indx:
                self.SetColumnWidth(indx, self.wcols[indx])

        self.root = self.AddRoot(self.titleRoot)
        self.SetItemImage(self.root, fldridx, which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, fldropenidx, which=wx.TreeItemIcon_Expanded)

        if not self.source:
            for x in range(15):
                txt = 'Item %d' % x
                child = self.AppendItem(self.root, txt)
                self.SetItemText(child, txt + '(c1)', 1)
                self.SetItemImage(child, fldridx, which=wx.TreeItemIcon_Normal)
                self.SetItemImage(child, fldropenidx, which=wx.TreeItemIcon_Expanded)
    
                for y in range(5):
                    txt = 'item %d-%s' % (x, chr(ord('a')+y))
                    last = self.AppendItem(child, txt)
                    self.SetItemText(last, txt + '(c1)', 1)
                    self.SetItemText(last, txt + '(c2)', 2)
                    self.SetItemImage(last, fileidx, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(last, smileidx, which=wx.TreeItemIcon_Selected)
        else:
            #   Подготавливаем буфер справочников
            ret, buff = self.eval_attr('init_sprav_buff')
            if ret and buff:
                self.SetSpravBuff(buff)
            
            #   Создаем дерево таблицы
            self.timer = wx.PyTimer(self.OnTimer)
            self.timer.Start(100)

        self.Expand(self.root)
        
        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelected)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDWN)
        self.BindICEvt()

    def ObjDestroy(self):
        """
        Функция уничтожения компонента.
        """
        #   Сохраняем размеры колонок грида
        wcols = []
        for indx, label in enumerate(self.labels):
            try:
                w = self.GetColumnWidth(indx)
                wcols.append(w)
            except:
                pass

        self.SaveUserProperty('wcols', wcols)
        
    def AddCodItem(self, parent_item, cod_mask, level, levelLenList, rows_dict):
        """
        Добавляет в определенный узел дочерние элементы, которые определяются
        по маске кода.
        
        @type parent_item: C{wx.CtrlTreeItem}
        @param parent_item: Узел, куда добавляются дочерние элементы.
        @type cod_mask: C{string}
        @param cod_mask: Маска кода справочника, по которой определяются дочерние
            элементы.
        @type level: C{int}
        @param level: Номер уровня кода родительского элемента.
        @type levelLenList: C{list}
        @param levelLenList: Список размеров уровней. Индекс списка соответствует номеру
            уровня кода.
        @type rows_dict: C{dictionary}
        @param rows_dict: Словарь записей из справочника. В качестве ключей размеры кодов,
            в качестве значений список записей с данным размером кода.
        @rtype: C{bool}
        @return: Признак того, что в узел добавлены дочерние элементы.
        """
        if level >= len(rows_dict):
            return False
        
        bret = False

        for row in rows_dict[level]:
            if level > 0:
                prnt_cod = row[0][:level]
            else:
                prnt_cod = None
            
            cod = row[0][:level+1]
            name = row[1]
            
            if not cod_mask or prnt_cod == cod_mask:
                bret = True
                child = self.AppendItem(parent_item, name)
                self.SetPyData(child, row)
                st = self.GetStateRow(row, level)

                #   Заполняем дополнительные поля
                for indx in range(2, len(row)):
                    val = row[indx]
                    if val is None:
                        val = ''
                        
                    self.SetItemText(child, str(val), indx-1)
                
                if self.AddCodItem(child, cod, level+1, None, rows_dict):
                    if st == ROW_STATE_NORMAL:
                        self.SetItemImage(child, self.fldridx, which=wx.TreeItemIcon_Normal)
                        self.SetItemImage(child, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
                    elif st == ROW_STATE_RED:
                        self.SetItemImage(child, self.folderRedIdx, which=wx.TreeItemIcon_Normal)
                        self.SetItemImage(child, self.folderOpenRedIdx, which=wx.TreeItemIcon_Expanded)
                    elif st == ROW_STATE_YELLOW:
                        self.SetItemImage(child, self.folderYellIdx, which=wx.TreeItemIcon_Normal)
                        self.SetItemImage(child, self.folderOpenYellIdx, which=wx.TreeItemIcon_Expanded)
                    else:
                        log.warning(u'Invalid STATE ROW state = <%s>' % st)
                        
                elif st == ROW_STATE_RED:
                    self.SetItemImage(child, self.fileidxItemRed, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(child, self.smileidx, which=wx.TreeItemIcon_Selected)
                elif st == ROW_STATE_YELLOW:
                    self.SetItemImage(child, self.fileidxItemYell, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(child, self.smileidx, which=wx.TreeItemIcon_Selected)
                else:
                    self.SetItemImage(child, self.fileidx, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(child, self.smileidx, which=wx.TreeItemIcon_Selected)

        return bret
        
    def GetStateRow(self, row, *argw, **kwarg):
        """
        Определяем состояние строки.
        
        @type row: C{list}
        @param row: Буфер строки; первый элемент структурный код в виде картежа,
            второй название элемента дерева, остальные элементы дополнительные
            отображаемые поля.
        @rtype: C{int}
        @return: Идентификатор состояния (ROW_STATE_NORMAL, ROW_STATE_RED, ...).
        """
        if self._stateFunction:
            return self._stateFunction(self, row, *argw, **kwarg)
        else:
            return ROW_STATE_NORMAL
            
    def getIndxPrntCod(self, cod_dict, cod_lst):
        """
        Возвращаем список индексов родительских кодов.
        
        @type cod_dict: C{dictionary}
        @param cod_dict: Словарь списков кодов записей добвленных в структуру
            дерева. Ключи - номера уровней кода.
        @type cod_lst: C{list}
        @param cod_lst: Структура кода проверяемой записи.
        @rtype: C{list}
        @return: Список индексов записей, в которых надо учесть сумму.
        """
        indx_lst = []
        
        for lev, lst in cod_dict.items():
            for i, cod_buff in enumerate(lst):
                if cod_buff[:lev+1] == cod_lst[:lev+1]:
                    indx_lst.append((lev, i))
        
        return indx_lst
        
    def GetSpravBuff(self):
        """
        Возвращает буфер справочников.
        """
        return self._spravBuff
        
    def GetValFromSpravBuff(self, typSprav, cod):
        """
        Возвращает значение поля из буфера справочника.
        
        @type typSprav: C{string}
        @param typSprav: Тип справочника.
        @type cod: C{string}
        @param cod: Код записи из справочника.
        @return: Возвращает значение поля из справочника по коду.
        """
        if self._spravBuff:
            try:
                return self._spravBuff[typSprav][cod]
            except KeyError:
                log.warning(u'KeyError: typSprav = <%s>, cod = <%s>' % (typSprav, cod))
                return cod
            
    def LoadTableTree(self, root):
        """
        Создает дерево со структрурой заданной аналитическими полями.
        """
        #   Получаем ссылку на интерфейс работы с классом данных
        cl = self.idataclass
        
        if not cl:
            return None
            
        # --- Отбираем нужные записи
        #   Формируем список полей сортировки
        self.orderBy = [getattr(cl.q, x[0]) for x in self.codfield]
        
        if '.q.' in self.filterExpr:
            ret, val = self.eval_attr('filterExpr', bReUse=False)
            if ret:
                rs = cl.select(val, orderBy=self.orderBy)
            else:
                rs = cl.select(orderBy=self.orderBy)
                
        elif self.filterExpr:
            rs = cl.select(self.filterExpr, orderBy=self.orderBy)
        else:
            rs = cl.select(orderBy=self.orderBy)

        #   Словарь значений
        rows_dict = {}

        #   Словарь кодов
        cod_dict = {}
        cod_lst = [None for x in range(len(self.codfield))]
        old_lst = None
        fld_buff = [0 for x in range(len(self.fields))]
        max_level = len(self.codfield) - 1
        
        # --- Буфферизируем таблицу - раскидываем по разным уровням кода
        for r in rs:
            # --- Собираем структурный код
            cod = ''
            cod_lst = list(cod_lst)
            for i, obj in enumerate(self.codfield):
                fld, df, spr = obj
                if df:
                    cod_lst[i] = str(getattr(r, fld))[df[0]:df[1]]
                else:
                    cod_lst[i] = str(getattr(r, fld))
            
            # --- Находим уровень кода где произошли изменения
            if not old_lst:
                cod_level = 0
            elif old_lst != cod_lst:
                for i, scd in enumerate(cod_lst):
                    old = old_lst[i]
                    if scd != old:
                        cod_level = i
                        break
            else:
                cod_level = len(cod_lst)-1
            
            old_lst = copy.deepcopy(cod_lst)

            # --- Читаем значения дополнительных полей
            #   Если код такой уже есть в буфере, то значения дополнительных
            #   полей прибавляются к значениям из буфера
            for i, fld in enumerate(self.fields):
                fld_buff[i] = val = getattr(r, fld)

            # --- Вычисляем суммы в родительских строках
            indx_lst = self.getIndxPrntCod(cod_dict, cod_lst)
            bAdd = False
            
            if indx_lst:
                for (lev, indx) in indx_lst:
                    r = rows_dict[lev][indx]
                    
                    for i, val in enumerate(fld_buff):
                        if val is None:
                            r[i+2] = None
                        elif r[i+2] is not None:
                            r[i+2] += val
            for lev in range(cod_level, max_level+1):
                # В зависимости от размера кода читаем из справочника значение кода
                if lev not in cod_dict or cod_lst not in cod_dict[lev]:
                    row_buff = range(len(self.fields)+2)
                    row_buff[0] = tuple(cod_lst)
                    spr = self.codfield[lev][2]
                    
                    if spr:
                        typ, fld = spr
                        row_buff[1] = self.GetValFromSpravBuff(typ, cod_lst[lev])
                    else:
                        row_buff[1] = cod_lst[lev]
    
                    for i, val in enumerate(fld_buff):
                        row_buff[i+2] = val
                
                    if lev in rows_dict:
                        rows_dict[lev].append(row_buff)
                        cod_dict[lev].append(cod_lst)
                    else:
                        rows_dict[lev] = [row_buff]
                        cod_dict[lev] = [cod_lst]
        
        #   Заполняем дерево
        self.AddCodItem(self.root, '', 0, None, rows_dict)
    
    def SetSpravBuff(self, buff):
        """
        Устанавливает внешний буфер справочников в качестве текущего.
        
        @type buff: C{dictionary}
        @param buff: Подготовленный буфер справочников. В качестве ключей типы
            справочников, в качестве значений словрь соответствий значений одного
            поля по значениям другого.
        """
        self._spravBuff = buff
    
    def SelectItemByCod(self, cod):
        """
        Выбирает элемент дерева по структурному коду.
        
        @type cod: C{string}
        @param cod: Структурный код.
        @rtype: C{bool}
        @return: Возвращает признак успешного выполнения.
        """
        if cod in self._codItemDict:
            item = self._codItemDict[cod]
            self.EnsureVisible(item)
            self.SelectItem(item)
            return True
            
        return False
        
    def SetStateFunction(self, func):
        """
        Устанавливаем функцию определения состояния.
        """
        self._stateFunction = func
        
    # --- Обработчики событий
    def OnSelected(self, evt):
        """
        Обработчик события wx.EVT_TREE_SEL_CHANGED, атрибут=selected
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('selected')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def OnActivated(self, evt):
        """
        Обработчик события wx.EVT_TREE_ITEM_ACTIVATED, атрибут=activated
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('activated')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def OnKeyDWN(self, evt):
        """
        Обработчик события wx.EVT_KEY_DOWN, атрибут=keyDown
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('keyDown')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def OnTimer(self):
        """
        """
        if self.timer:
            self.timer.Stop()
            self.timer = None
            self.PostOnInitEvent()


def test(par=0):
    """
    Тестируем пользовательский класс.
    
    @type par: C{int}
    @param par: Тип консоли.
    """
    
    import ic.components.ictestapp as ictestapp
    
    app = ictestapp.TestApp(par)
    common.img_init()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    ctrl = icTableTreeList(win, -1, {'position': (0, 0),
                                     'size': (300, 300),
                                     'labels': ['tree', 'par1']})
    
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()
