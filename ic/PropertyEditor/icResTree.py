#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Редактор ресурсов.
"""

import wx
from wx.lib.agw import flatmenu
import ic
import os
import os.path
import time
import shutil
import gettext
import copy
import ic.imglib
from ic.imglib import common
# from ic.dlg.msgbox import Ask
import ic.components as components
# from ic.log.iclog import MsgLastError, LogLastError
import ic.utils.resource as resource
from ic.utils import ic_uuid
from ic.db import icdataset
import ic.components.icResourceParser as icResourceParser
from ic.PropertyEditor.icDefInf import *
from ic.PropertyEditor.icPanelEditor import *
import ic.components.icwidget as icwidget

import ic.PropertyEditor.icDefInf as icDefInf
import ic.components.user.objects.icpanelgroupedt as icpanelgroupedt
from ic.PropertyEditor import icpropertyeditmanager

import ic.prj.PrjTree as PrjTree
import ic.engine.ic_user as ic_user
import ic.components.user as user
import ic.components.icEvents as icEvents
import ic.dlg.ic_logo_dlg as ic_logo_dlg
import ic.utils.ic_file as ic_file
from ic.dlg import ic_dlg
from ic.kernel import io_prnt
from ic.PropertyEditor.icProjectNotebook import icProjectNB

_ = wx.GetTranslation
__version__ = (1, 0, 2, 2)

# Список идентификаторов дерева, храним для того, чтобы контролировать уникальность
# идентификаторов
BUFF_TREE_ID_LIST = []

# -------------------------------------------------------------------------------
# Буффер для копирования ресурсных описаний
Res_copyBuff = None


def getCopyBuffEdt():
    return Res_copyBuff


def setCopyBuffEdt(obj):
    global Res_copyBuff
    Res_copyBuff = obj

# Словарь идентификаторов узлов дерева
OpenTreeItemIdDict = {}


def addOpenTreeItemId(key, id):
    """
    Добавляет идентификатор открытого узла дерева.
    @type key: C{string}
    @param key: Ключ по которому будет храниться идентификатор.
    """
    global OpenTreeItemIdDict
    OpenTreeItemIdDict[key] = id


def getOpenTreeItemId(key):
    """
    Добавляет идентификатор открытого узла дерева.
    @type key: C{string}
    @param key: Ключ по, которому будет храниться идентификатор.
    """
    if key in OpenTreeItemIdDict:
        return OpenTreeItemIdDict[key]

    return None


def getResKey(res):
    """
    Возвращает уникальный ключ ресурсного описания формы.
    """
    try:
        key = res['type']+res['name']
    except:
        key = None
    return key


# -------------------------------------------------------------------------------
_ResCard = u'Ресурсы (*.frm)|*.frm|All files (*.*)|*.*| IcObj files (*.py)|*.py'

SPC_IC_RESTREE = {'name': 'tree',
                  'type': 'ResTree',
                  'position': (-1, -1),
                  'size': (-1, -1),
                  'resource': None,
                  'foregroundColor': None,
                  'backgroundColor': None,
                  'style': wx.TR_HAS_BUTTONS}

# Словарь описание компонентов поддерживаемых редактором. В качестве ключей содержит типы компонентов,
# в качестве значений картеж описания:
#       1 эл-т.  - Тип группы.
#       2        - Картинка для отображения компонента в дереве объектов (свенутый узел).
#       3        - Картинка для отображения компонента в дереве объектов (развернутый узел).
#       4           - Спецификация компонента.
#       5           -  Если компонент является контейнером, то список типов, которые могут содержаться в
#                        контейнере. Если = -1, то используется третий параметр - спиок компонентов, которые
#                        не могут содержатсься в контейнере.
#       6           -  Если компонент является контейнером и второй параметр = -1, то содержит спиок
#                        компонентов, которые не могут содержаться в контейнере.
#       7       - модуль

ObjectsInfo = None


def GetObjectsInfo():
    global ObjectsInfo
    if not ObjectsInfo:
        InitObjectsInfo()

    return ObjectsInfo


def GetObjectModule(obj_typ):
    """
    Возвращает модуль компонента.
    """
    ifs = GetObjectsInfo()
    info = ifs.get(obj_typ, None)
    if info:
        return info[-1]


def GetObjectClass(obj_typ):
    modl = GetObjectModule(obj_typ)
    if modl:
        return getattr(modl, modl.ic_class_name)


def MyExec(s):
    exec s


#   Спецификация на объект группы
SPC_IC_GROUP = {'name': 'default',
                'prim': '',
                'type': 'Group',
                'child': [],
                '__styles__': {'DEFAULT': 0},
                '__parent__': icwidget.SPC_IC_SIMPLE}


def InitObjectsInfo(bRefresh=False):
    """
    Функция инициализации иформационной структуры описания поддерживаемых
    редактором компонентов.
    !!! Функция должна вызываться только после того как создан объект приложения.
    """
    t1 = time.clock()
    global ObjectsInfo
    ObjectsInfo = {'Root': (-1, -1, -1, {}, -1, None, None),
                   'ResTree': (-1, -1, -1, {}, -1, None, None)}

    spc = copy.deepcopy(components.icgrid.SPC_IC_CELL)
    spc = icSpcDefStruct(spc, spc, True)
    ObjectsInfo['GridCell'] = (icDefInf._icComboType, common.imgEdtCell, common.imgEdtCell, spc, [], None, None)

    ObjectsInfo['ToolBarTool'] = (icDefInf._icComboType, common.imgEdtTBTool, common.imgEdtTBTool,
                                  components.custom.ictoolbar.SPC_IC_TB_TOOL, [], None, None)
    ObjectsInfo['Separator'] = (icDefInf._icComboType, common.imgEdtSeparator, common.imgEdtSeparator,
                                components.custom.ictoolbar.SPC_IC_TB_SEPARATOR, [], None, None)

    spc = SPC_IC_GROUP
    spc = icSpcDefStruct(spc, spc, True)
    ObjectsInfo['Group'] = (icDefInf._icServiceType, common.imgFolder, common.imgFolderOpen, spc, -1, [], None)

    spc = icdataset.SPC_IC_DATALINK
    ObjectsInfo['DataLink'] = (icDefInf._icServiceType, common.imgEdtDataLink,
                               common.imgEdtDataLink, spc, [], None, icdataset)

    # Ищем системные компоненты
    mod_list = ic.components.icGetSysModulDict()
    count = 0

    for name, modl in mod_list.items():
        count += 1
        try:
            ic_logo_dlg.SetLoadProccessBoxLabel(u'Импорт системного компонента <%s>' % name, 100*count/len(mod_list))
            spc = copy.deepcopy(modl.ic_class_spc)
            img = ic.imglib.get_image_by_expr(modl.ic_class_pic)
            img2 = ic.imglib.get_image_by_expr(modl.ic_class_pic2)
            key = spc['type']

            # Дополняем спецификацию с учетом наследования
            spc = icSpcDefStruct(spc, spc, False)
            ObjectsInfo[key] = (modl.ic_class_type,
                                img, img2, spc,
                                modl.ic_can_contain,
                                modl.ic_can_not_contain, modl)
        except:
            io_prnt.outErr(u'MODULE IMPORT ERROR: module= <%s>' % modl)

    # Чистим словарь групп
    icDefInf.ClearUserGroup()
    user.icClearUserModulDict()

    modDct = user.icGetUserModulDict(bRefresh=bRefresh)
    subsys_lst = []

    for mod in modDct.values():
        spc = copy.deepcopy(mod.ic_class_spc)
        key = spc['type']
        img = ic.imglib.get_image_by_expr(mod.ic_class_pic)
        img2 = ic.imglib.get_image_by_expr(mod.ic_class_pic2)
        # Дополняем спецификацию с учетом наследования
        spc = icSpcDefStruct(spc, spc, False)

        # Регестрируем новую группу
        if key in ObjectsInfo.keys():
            group_key = None
        elif mod.user_subsys and mod.user_subsys not in subsys_lst:
            subsys_lst.append(mod.user_subsys)
            group_key = icDefInf.RegComponentGroup(u'Компоненты ' + mod.user_subsys)
        elif mod.user_subsys:
            group_key = icDefInf.GetGroupIdByName(u'Компоненты ' + mod.user_subsys)
        else:
            group_key = mod.ic_class_type

        # Если новая группа зарегестрирована, то добавлям ее в словарь описаний
        if group_key:
            ObjectsInfo[key] = (group_key,
                                img, img2, spc,
                                mod.ic_can_contain,
                                mod.ic_can_not_contain, mod)

    t2 = time.clock()


def OnFile(evt):
    """
    Выбирает имя файла.
    """
    card = u'All files (*.*)|*.*'
    dlg = wx.FileDialog(None, u'Выберите имя файла', u'', u'', card, wx.OPEN)
    path = ''
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPaths()[0]
        obj = evt.GetEventObject().editor
        obj.nameValue.value = path
        obj.nameValue.oldValue = obj.value
        obj.nameValue.edit_ctrl.SetValue(obj.nameValue.GetStr())

    return path


def getStyleFromDict(style_dict, allstyles):
    """
    Вычисляет стиль компонента из словарного представления.
    @type style_dict: C{dictionary}
    @param style_dict: Ресурсное описание компонета.
    @type allstyles: C{dictionary}
    @param allstyles: Словарь всех стилей компонента.
    @rtype: C{long}
    @return: Стиль компонента.
    """
    bFind = False
    style = 0
    for key in style_dict:
        if style_dict[key] > 0:
            if key in allstyles.keys():
                stl = allstyles[key]
                style = style | allstyles[key]
            elif key in ICWindowStyle.keys():
                style = style | ICWindowStyle[key]
    return style


def getComponentStyleDict(component):
    """
    Возвращает стиль компонента в виде словаря.
    """
    spc = ObjectsInfo[component['type']][3]
    if isinstance(spc, dict) and '__styles__' in spc:
        style_dict = spc['__styles__']
        if not style_dict:
            style_dict = icwindow.ICWindowStyle
    else:
        style_dict = icwindow.ICWindowStyle

    return style_dict


def findSpcStruct(component):
    """
    Функция достраивает ресурсное описание до спецификации.
    @type component: C{dictionary}
    @param component: Ресурсное описание компонета.
    @rtype: C{tuple}
    @return: Полное ресурсное описание и спецификацию.
    """
    spc = None
    # Гриды и их объекты
    if component['type'] == 'GridDataset':
        spc = components.icgriddataset.SPC_IC_GRID_DATASET
        icSpcDefStruct(components.icgriddataset.SPC_IC_GRID_DATASET, component, True)
        icSpcDefStruct(components.icgrid.SPC_IC_CELLATTR, component['cell_attr'], True)
        icSpcDefStruct(components.icfont.SPC_IC_FONT, component['cell_attr']['font'], True)
        icSpcDefStruct(components.icgrid.SPC_IC_LABELATTR, component['label_attr'], True)
        icSpcDefStruct(components.icfont.SPC_IC_FONT, component['label_attr']['font'], True)

        # Так как служебный атрибут '__styles__'  не наследуется
        component['__styles__'] = spc['__styles__']

    elif component['type'] == 'ListDataset':
        spc = components.iclistdataset.SPC_IC_LIST_DATASET
        icSpcDefStruct(components.iclistdataset.SPC_IC_LIST_DATASET, component, True)
        icSpcDefStruct(components.icfont.SPC_IC_FONT, component['font'], True)

    elif component['type'] == 'GridCell':
        spc = components.icgrid.SPC_IC_CELL
        icSpcDefStruct(components.icgrid.SPC_IC_CELL, component, True)
        icSpcDefStruct(components.icgrid.SPC_IC_CELLATTR, component['cell_attr'], True)
        icSpcDefStruct(components.icfont.SPC_IC_FONT, component['cell_attr']['font'], True)

    elif component['type'] == 'cell_attr':
        spc = components.icgrid.SPC_IC_CELLATTR
        icSpcDefStruct(components.icgrid.SPC_IC_CELLATTR, component, True)
        icSpcDefStruct(components.icfont.SPC_IC_FONT, component['font'], True)

    elif component['type'] == 'label_attr':
        spc = components.icgrid.SPC_IC_LABELATTR
        icSpcDefStruct(components.icgrid.SPC_IC_LABELATTR, component, True)
        icSpcDefStruct(components.icfont.SPC_IC_FONT, component['font'], True)

    # Пользовательские компоненты
    elif component['type'] in ObjectsInfo.keys():
        spc = ObjectsInfo[component['type']][3]
        icSpcDefStruct(spc, component, True)

    #   Если уникальный идентификатор не опрделен, то генерируем его
    if '_uuid' in component and not component['_uuid']:
        component['_uuid'] = ic_uuid.get_uuid()

    return component, spc


class icResTree(icwidget.icWidget, wx.TreeCtrl):
    """
    Дерево объектов ресурсного описания.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace=None):
        """
        Конструктор для создания дерева объектов.
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
        if id == -1:
            id = icwidget.icNewId()

        icSpcDefStruct(SPC_IC_RESTREE, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        size = component['size']
        pos = component['position']
        style = component['style']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        self.res = component['resource']
        self.lastSel = None

        # Указатель на редактор ресурсов (icResourceEditor)
        self.editor = None
        # Указатель на панель групп
        self._groupPanel = None

        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self._initPicDict()

        # Счетчик идентификаторов дерева
        self._treeItemId = -1
        self._lastTreeId = None
        
        # ССылки на правое меню
        self.menuDict = {}
        self._right_menu = None
        self._menu_groups = {}      # буфер элементов меню
        
        # Словарь соответствий между счетчиком узла (идентификатор ресурсного описания)
        # и внутренним идентификатором узла дерева (компонента)
        self._dictResTreeId = {}

        # Признак изменения текущего объекта в графическом редакторе при изменении
        # текущего редактируемого объекта в редакторе свойств
        self.bSelInGraphEdt = True

        self.root = self.AddRoot(u'Метаданные')
        self.SetPyData(self.root, component)
        self.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        # Атрибут поиска
        self.finddata = wx.FindReplaceData()
        self.lastfindItem = None

        # Обработчики событий
        # Поиск в дереве ресурса
        self.Bind(wx.EVT_COMMAND_FIND, self.OnFind)
        self.Bind(wx.EVT_COMMAND_FIND_NEXT, self.OnFind)
        self.Bind(wx.EVT_COMMAND_FIND_CLOSE, self.OnFindClose)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=id)
        # self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnRightClick)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def _get_item_name(self, res):
        """
        Возвращает имя элемента дерева.
        """
        info = GetObjectsInfo().get(res['type'], None)
        if info:
            _spc = info[3]
            _lst = [res.get(attr, u'') or u'' for attr in _spc.get('__brief_attrs__', ['type', 'name'])] or (res['type'], res['name'])
        else:
            _lst = (res['type'], res['name'])

        return u': '.join(_lst)

    def addBranch(self, root, res, bActive=True):
        """
        Добавляет ветку в дерево.
        """
        try:
            if res['type'] not in self.dictPicIndx:
                self._initPicDict()

            id_pic, id_exp_pic = self.dictPicIndx[res['type']]
        except:
            id_pic, id_exp_pic = (self.fileidx, self.fileidx)

        item_name = self._get_item_name(res)
        root = self.AppendItem(root, item_name, id_pic)
        self.SetItemImage(root, id_exp_pic, wx.TreeItemIcon_Expanded)

        self._treeItemId += 1
        res['__item_id'] = self._treeItemId

        # Проверяем совпадает ли идентификатор с идентификатором в буфере.
        # Если совпадает, то запоминаем этот идентификатор узла.
        key = getResKey(self.res)
        if key:
            lastid = getOpenTreeItemId(key)
            if lastid == self._treeItemId:
                self._lastTreeId = root

        # Устанавливем цвет узлов
        if not bActive or ('activate' in res and res['activate'] in ['0', 'False']):
            self.SetItemTextColour(root, wx.Colour(*DEACTIVATE_COLOR))
            bActive = False
        else:
            self.SetItemTextColour(root, wx.Colour(*ACTIVATE_COLOR))

        self.SetPyData(root, res)
        self._dictResTreeId[self._treeItemId] = root

        BUFF_TREE_ID_LIST.append(res['name'])

        if 'child' in res:
            for item in res['child']:
                self.addBranch(root, item, bActive)

        if 'cols' in res and isinstance(res['cols'], list):
            for item in res['cols']:
                self.addBranch(root, item, bActive)

        if 'win1' in res and res['win1'] is not None:
            self.addBranch(root, res['win1'])

        if 'win2' in res and res['win2'] is not None:
            self.addBranch(root, res['win2'], bActive)

        if 'cell_attr' in res:
            res['cell_attr']['name'] = ''
            res['cell_attr']['type'] = 'cell_attr'
            self.addBranch(root, res['cell_attr'], bActive)

        if 'label_attr' in res:
            res['label_attr']['name'] = ''
            res['label_attr']['type'] = 'label_attr'
            self.addBranch(root, res['label_attr'], bActive)

        return root

    def AddItem(self, item, res_obj, bNewName = True, bRefreshEditor=True):
        """
        Добавляет ресурсное описание в контейнер.
        @type item: C{wx.TreeItem}
        @param item: Узел дерева, куда добавляется элемент.
        @type res_obj: C{dictionary}
        @param res_obj: Ресурсное описание объекта, который добавляется.
        @type bNewName: C{string}
        @param bNewName: Признак того, что необходимо сгененрировать новое имя объекта (используется при копировании).
        @type bRefreshEditor: C{bool}
        @param bRefreshEditor: Признак обновления графического редактора.
        """
        # Инициализируем ресурс
        cls = self._get_res_class(res_obj)
        if cls:
            edt_mngr = cls.GetEditorResourceManager()
            if edt_mngr:
                res_obj = edt_mngr.InitResource(res_obj) or res_obj
                
        if bNewName:
            res_obj['name'] = res_obj['name']+'_'+str(icwidget.icNewId())

        # В случае корневого элемента
        if item == self.root and not self.GetChildrenCount(self.root):
            self.editor.res = res_obj
            self.addBranch(item, res_obj)
        else:
            res = self.GetPyData(item)
            if 'child' in res:
                res['child'].append(res_obj)
                self.addBranch(item, res_obj)
            else:
                # Предупредить о не корректной спецификации
                log.warning(u'Спецификация компонента <%s> не поддерживает добавление дочерних элементов' % res['type'])

            if 'cols' in res and isinstance(res['cols'], list):
                res['cols'].append(res_obj)
                self.addBranch(item, res_obj)

            if 'win1' in res and res['win1'] is None:
                res['win1'] = res_obj
                self.addBranch(item, res_obj)

            elif 'win2' in res and res['win2'] is None:
                res['win2'] = res_obj
                self.addBranch(item, res_obj)

        self.Expand(item)

        # Обновляем графический редактор
        if bRefreshEditor:
            self.GetResEditor().RefreshGraphEditor()
            wx.CallAfter(self.OnSelChanged, None, item)

    def AddTypeItem(self, res_id, obj_type, pos=(-1, -1), size=(-1, -1), bRefreshEditor=True):
        """
        Добавляет описание объекта в ресурс зная узел и тип добавляемого объекта.
        @type res_id: C{int}
        @param res_id: Внутренний идентификатор узла дерева.
        @type obj_type: C{string}
        @param obj_type: Тип объекта.
        @type pos: C{wx.Point}
        @param pos: Позиция, где объект будет распологаться.
        @type size: C{wx.Size}
        @param size: Размеры объекта.
        @rtype: C{bool}
        @return: Признак успешного добавления.
        """
        # Проверяем можно добавить в указанный узел объект заданного типа или нельзя
        spc_res = ObjectsInfo[obj_type][3]
        res_obj = copy.deepcopy(spc_res)

        if pos != (-1, -1):
            res_obj['position'] = pos

        if size != (-1, -1):
            res_obj['size'] = size

        try:
            item = self._dictResTreeId[res_id]
        except:
            item = self.root

        self.AddItem(item, res_obj, bRefreshEditor=bRefreshEditor)
        return True

    def ChangeSelGraphProperty(self, property, value):
        """
        Изменяет свойства (размер, расположение, способ выравнивания) объекта в
        графическом редакторе.
        @type property: C{string}
        @param property: Имя свойства.
        @type value: C{...}
        @param value: Новое значение свойства.
        """
        if self.GetResEditor().graphEditor:
            pnl = self.GetResEditor().graphEditor.GetEditorPanel()
            item = self.lastSel
            iditem = self.GetPyData(item)['__item_id']
            # Изменяем свойство объекта
            if not pnl.ChangeItemProperty(iditem, property, value) and pnl.isItemInEditor(iditem):
                # Если свойство напрямую изменить нельзя, то делаем
                # полное обновления графического редактора
                return False
            else:
                return True

        return False

    def ChangePropertyId(self, id, property, value, bRefresh=True):
        """
        Изменяет заданное свойство ресурсного описания объекта, который определяется
        по ресурсному идентификатору узла.
        @type id: C{int}
        @param id: Ресурсный идентификатор узла.
        @type property: C{string}
        @param property: Имя свойства.
        @type value: C{...}
        @param value: Новое значение свойства.
        @type bRefresh: C{bool}
        @param bRefresh: Признак обновления редактора свойств.
        """
        try:
            item = self._dictResTreeId.get(id, None)
            if item:
                data = self.GetPyData(item)
                data[property] = value
                self.SetPyData(item, data)

            if bRefresh:
                item = item or self.root
                if self.lastSel != item:
                    # Таким способом избегаем обновления из редактора свойств
                    self.lastSel = None
                    self.EnsureVisible(item)
                    self.SelectItem(item)
                elif property in ('flag',):
                    self.lastSel = None
                    self.SelectItem(item)
                # Меняем свойство в редакторе
                elif self.editor:
                    self.editor.notebook.GetPropertyEditor().SelectPropertyPage(1)
                else:
                    self.lastSel = None
                    self.SelectItem(item)
        except:
            io_prnt.outErr(u'ChangePropertyId ERROR id=%s, property=%s, value=%s' % (id, property, value))

    def _get_res_class(self, res):
        """
        Определяет класс объекта по его ресурсу.
        """
        obj_typ = res['type']
        return GetObjectClass(obj_typ)
        
    def DeleteItem(self, item, bRefreshEditor=True):
        """
        Удаляет узел из ресурса.
        @type item: C{wx.TreeItem}
        @param item: Идентификатор узла дерева.
        @type bRefreshEditor: C{bool}
        @param bRefreshEditor: Признак обновления графического редактора.
        """
        if item == self.root:
            return

        data = self.GetPyData(item)
        parent_item = self.GetItemParent(item)
        res = self.GetPyData(parent_item)
        
        # Проверяем можно удалить объект из ресурса или нет
        # сначало проверяем у родителя
        cls = self._get_res_class(res)
        if cls:
            edt_mngr = cls.GetEditorResourceManager()
            if edt_mngr:
                if not edt_mngr.DeleteChild(res, data):
                    return
        
        if 'child' in res:
            res['child'].remove(data)
        # Грид с особенностями
        if 'cols' in res and isinstance(res['cols'], list) and data in res['cols']:
            res['cols'].remove(data)
        if 'win1' in res and data == res['win1']:
            res['win1'] = res['win2']
            res['win2'] = None
        if 'win2' in res and data == res['win2']:
            res['win2'] = None

        if self.editor.res == data:
            self.editor.res = None

        # Удаляем имя из списка, используемых имен
        self.Delete(item)

        # Обновляем графический редактор
        if bRefreshEditor:
            self.GetResEditor().RefreshGraphEditor()

    def findInItem(self, item, findStr):
        """
        Ищет подстроку в ресурсном описании компонента.
        @type item: C{TreeCtrlItemId}
        @param item: Узел, с которого ведется поиск.
        @type findStr: C{string}
        @param findStr: Текст, который ищется в описании.
        @rtype: C{bool}
        @return: Признак успешного поиска.
        """
        data = self.GetPyData(item)
        for key, val in data.items():
            if type(val) in (str, unicode) and findStr in val.lower():
                self.EnsureVisible(item)
                self.SelectItem(item)
                self.editor.notebook.GetPropertyEditor().SelectPropertyEdt(key)
                return True
        return False

    def findItem(self, prnt, findStr):
        """
        Ищет в ресурсном описании формы подстроку текста.
        @type prnt: C{TreeCtrlItemId}
        @param prnt: Узел, с которого ведется поиск.
        @type findStr: C{string}
        @param findStr: Текст, который ищется в описании.
        @rtype: C{bool}
        @return: Признак успешного поиска.
        """
        # Начинаем вести рекурсивный поиск
        if not prnt:
            return False

        if not self.lastfindItem:
            child, ck = self.GetFirstChild(prnt)

            if child.IsOk():
                if self.findInItem(child, findStr):
                    self.lastfindItem = (child, ck)
                    return True
                if self.ItemHasChildren(child):
                    self.lastfindItem = None
                    if self.findItem(child, findStr):
                        return True
        else:
            child, ck = self.lastfindItem

            data = self.GetPyData(child)
            _type = data['type']
            _name = data['name']

            if self.ItemHasChildren(child):
                self.lastfindItem = None
                if self.findItem(child, findStr):
                    return True

        # Создаем список копируемых элементов
        while 1:
            child, ck = self.GetNextChild(prnt, ck)

            if child.IsOk():
                if self.findInItem(child, findStr):
                    self.lastfindItem = (child, ck)
                    return True
                if self.ItemHasChildren(child):
                    self.lastfindItem = None
                    if self.findItem(child, findStr):
                        return True
            else:
                break

        return False

    def GetIdObj(self, id):
        """
        Возврвщает объект, привязанный к ресурсному идентификатору узла.
        @type id: C{int}
        @param id: Ресурсный идентификатор узла.
        @return: Возврвщает объект, привязанный к ресурсному идентификатору узла.
        """
        try:
            item = self._dictResTreeId[id]
            data = self.GetPyData(item)
        except:
            io_prnt.outErr(u'GetIdObj ERROR')

    def GetPanelGroup(self):
        """
        Возвращает указатель на панель групп.
        """
        return self._groupPanel

    def GetResEditor(self):
        """
        Возвращает указатель на редактор ресурса.
        """
        return self.editor

    def GetObjectsInfo(self):
        """
        Возвращает указатль на информационную структуру,
        описывающую компоненты системы.
        """
        return GetObjectsInfo()

    def GetTypeModule(self, typObj=None):
        """
        Возвращает модуль компонента заданного типа.
        @type typObj: C{string}
        @param typObj: Тип объекта.
        """
        module = self.GetObjectsInfo()[typObj][-1]
        if module is None:
            log.warning(u'Не определен модуль для компонента <%s>' % typObj)
        return module

    def GetChildNameList(self, item=None):
        """
        Функция у узла определяет список имен дочерних элементов,
        кроме текущего.
        """
        if item is None:
            item = self.GetSelection()

        nameList = []
        try:
            data = self.GetPyData(item)
            parent_item = self.GetItemParent(item)
            res = self.GetPyData(parent_item)

            if 'child' in res:
                for x in res['child']:
                    if data != x:
                        nameList.append(x['name'])
            if 'cols' in res and isinstance(res['cols'], list):
                for x in res['cols']:
                    if data != x:
                        nameList.append(x['name'])
            if 'win1' in res and data != res['win1']:
                nameList.append(res['win1']['name'])
            if 'win2' in res and data != res['win2']:
                nameList.append(res['win2']['name'])
        except:
            log.fatal(u'No parent in icResTree.GetChildNameList()')

        return nameList

    def HelpItem(self):
        """
        Помощь.
        """
        item = self.GetSelection()
        data = self.GetPyData(item)
        # Создаем окно помощи
        try:
            doc_path = ic_file.DirName(ic.utils.resource.icGetICPath())
            from ic.components import icIEHtmlWin
            # Старый способ
            if 'docstr' in data:
                fileDoc = doc_path + os.sep + data['docstr']
            elif '__doc__' in data and data['__doc__']:
                fileDoc = doc_path + os.sep + data['__doc__']
            else:
                fileDoc = doc_path + os.sep + 'ic.components.ic'+data['type'].lower()+'-module.html'

            print(fileDoc)
            if os.path.isfile(fileDoc):
                if wx.Platform == '__WXMSW__':
                    icIEHtmlWin.startMiniHtmlBrows(fileDoc)
                elif wx.Platform == '__WXGTK__':
                    if 'BROWSER' in os.environ:
                        www_browser = os.environ['BROWSER']
                    else:
                        www_browser = 'firefox'
                    cmd = www_browser + ' ' + fileDoc.replace('\\', '/')
                    os.system(cmd)
                else:
                    cmd = 'start explorer ' + fileDoc.replace('/', '\\')
                    os.system(cmd)
            else:
                io_prnt.outWarning(u'Help file %s is not found' % fileDoc)
        except:
            io_prnt.outLastErr(u'View Help Error!')

    def _initPicDict(self):
        """
        Создает словварь картинок. Ключи - типы компонентов,
        значения картинки.
        """
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = il.Add(common.imgFolder)
        self.fldropenidx = il.Add(common.imgFolderOpen)
        self.fileidx = il.Add(common.imgElement)
        self.dictPicIndx = {}

        # Заполняем картинками для представления объектов в дереве
        for ds in ObjectsInfo.keys():
            if ds != -1:
                if type(ObjectsInfo[ds][1]) == type(common.imgPage):
                    id_pic = il.Add(ObjectsInfo[ds][1])
                elif ObjectsInfo[ds][1] == -1:
                    id_pic = self.fileidx
                elif ObjectsInfo[ds][1] == 0:
                    id_pic = self.fldridx

                if type(ObjectsInfo[ds][2]) == type(common.imgPage):
                    id_exp_pic = il.Add(ObjectsInfo[ds][2])
                elif ObjectsInfo[ds][2] == -1:
                    id_exp_pic = self.fileidx
                elif ObjectsInfo[ds][2] == 0:
                    id_exp_pic = self.fldropenidx

                self.dictPicIndx[ds] = (id_pic, id_exp_pic)

        self.AssignImageList(il)

    def InsItem(self, item, res_obj=None, insType=0, bRefreshEditor=True):
        """
        Вставляет ресурсное описание в контейнер в нужное место.
        @type pos: C{int}
        @param pos: Позиция куда вставляется объект.
        @type item: C{wx.TreeItem}
        @param item: Узел дерева, куда добавляется элемент.
        @type res_obj: C{dictionary}
        @param res_obj: Ресурсное описание объекта, который добавляется.
        @type insType: C{int}
        @param insType: Тип вставки (0 - вставлять перед текущим элементом, 1 - после, 2 - вместо).
        @type bRefreshEditor: C{bool}
        @param bRefreshEditor: Признак обновления графического редактора.
        """
        pos = -1
        prnt = self.GetItemParent(item)
        ck = 0
        child, ck = self.GetFirstChild(prnt)
        _copyList = []
        _labelList = []
        _dataList = []

        if child == item:
            pos = 0
            if not self.GetPyData(child)['type'] in ['cell_attr', 'label_attr']:
                _copyList.append(child)
                _dataList.append(copy.deepcopy(self.GetPyData(child)))
                _labelList.append(self.GetItemText(child))

        count = 0
        # Создаем список копируемых элементов
        while 1:
            child, ck = self.GetNextChild(prnt, ck)
            if child.IsOk():
                count += 1
                if child == item:
                    pos = count
                if pos >= 0:
                    if not self.GetPyData(child)['type'] in ['cell_attr', 'label_attr']:
                        _copyList.append(child)
                        _dataList.append(copy.deepcopy(self.GetPyData(child)))
                        _labelList.append(self.GetItemText(child))
            else:
                break

        # В зависимости от типа вставки корректируем буфферные списки
        if insType == 1:
            _copyList = _copyList[1:]
            _dataList = _dataList[1:]
        elif insType == 2:
            _dataList = _dataList[1:]

        # Удаляем
        _copyList.reverse()
        for item in _copyList:
            try:
                self.DeleteItem(item, bRefreshEditor=False)
            except:
                pass

        # Вставляем из буффера
        self.AddItem(prnt, res_obj, bRefreshEditor=False)

        # Вставляем все, что удалили
        for res in _dataList:
            self.AddItem(prnt, res, False, bRefreshEditor=False)

        self.Expand(prnt)

        # Обновляем графический редактор
        if bRefreshEditor:
            self.GetResEditor().RefreshGraphEditor()

    def OnFind(self, event):
        """
        Поиск подстроки в значениях атрибутов дерева ресурсов.
        """
        findStr = self.finddata.GetFindString().lower()
        try:
            item = self.GetSelection()
        except:
            item = self.root

        if not self.findItem(item, findStr):
            self.lastfindItem = None
            if not self.findItem(self.root, findStr):
                ic_dlg.icWarningBox(ParentWin_=self,
                                    Title_=u'ВНИМАНИЕ',
                                    Text_=u'Не найдена подстрока \'%s\' в ресурсе' % findStr)
                if self.finddlg:
                    self.finddlg.SetFocus()

                return

    def OnFindNext(self, event):
        """
        Продолжает поиск (по Ctrl-G).
        """
        if self.finddata.GetFindString():
            self.OnFind(event)
        else:
            self.OnHelpFind()

    def OnFindClose(self, event):
        event.GetDialog().Destroy()

    def OnKeyDown(self, evt):
        """
        Обрабатывает нажатие клавиши.
        """
        if evt.GetKeyCode() in (ord(u'f'), ord(u'F'), ord(u'А'), ord(u'а')) and evt.ControlDown():
            self.OnHelpFind()
        elif evt.GetKeyCode() in (ord(u'g'), ord(u'G'), ord(u'П'), ord(u'п')) and evt.ControlDown():
            self.OnFindNext(evt)

        if not self.editor.isToggleEnable():
            evt.Skip()
            return

        if evt.GetKeyCode() == wx.WXK_DELETE and not evt.ControlDown() and not evt.ShiftDown() \
           and not evt.AltDown():
            if ic_dlg.icAskDlg(u'УДАЛЕНИЕ', u'Действительно удалить объект?') == wx.ID_YES:
                self.OnDeleteItem(None)
        elif evt.GetKeyCode() == wx.WXK_INSERT and evt.ControlDown():
            self.OnCopyItem(None)

        elif evt.GetKeyCode() == wx.WXK_INSERT and evt.ShiftDown():
            self.OnPasteItem(None)

        evt.Skip()

    def OnSize(self, evt):
        try:
            h = self.editor.GetSashPosition()
            sz = self.editor.notebook.GetSize()
            self.editor.notebook.SetSize((sz[0], h-27))
        except:
            pass

        evt.Skip()

    def OnRightClick(self, evt, bgr_win=None):
        """
        Обрабатывается нажатие на правую кнопку мыши. Выводится
        меню с объектами которые могут быть добавлены в ресурсное
        описание.
        @param evt: Event.
        @param bgr_win: Окно, на которое выводится меню.
        """
        bgr_win = bgr_win or self
        global ObjectsInfo
        if not self.editor.isToggleEnable():
            return

        Res_copyBuff = getCopyBuffEdt()
        # Словарь идентификаторов объектов
        menuGroup = flatmenu.FlatMenu()
        item = self.GetSelection()
        if not item:
            return

        data = self.GetPyData(item)
        # Если ресурс пуст, то в корень можно добавить описание любого объекта
        if item == self.root and self.editor.res is None:
            info = (-1, -1, -1, {}, -1, [], None)
        # В корень ничего нельзя добавить пока ресурс содержит описание
        # какого-либо объекта
        elif item == self.root and self.editor.res is not None:
            info = (-1, -1, -1, {}, [], [], None)
        # В зависимости от типа объекта настраиваем фильтр, который
        # отсекает объекты, которые не могут быть добавлены в объект
        else:
            info = ObjectsInfo.get(data['type'], None)

        if not info:
            return

        # Определяем список разрешенных элементах
        mod = info[-1]
        NonObjList = []

        if mod and hasattr(mod, 'get_can_contain_lst'):
            ObjList = mod.get_can_contain_lst(self.GetResEditor())

        elif info[4] == -1 or info[4] is None:
            if len(info) > 5:
                NonObjList = info[5]
            ObjList = ObjectsInfo.keys()
        else:
            ObjList = info[4]

        if not self._right_menu:
            menu = flatmenu.FlatMenu()
            self.menuIdDict = {}
            self._menuGrp = {}
            # Цикл по группам
            if (ObjectsInfo is not None) and (ObjList is not None) and (NonObjList is not None):
                for group in icDefInf.GroupsInfo.keys():
                    menuObj = flatmenu.FlatMenu()
                    self._menuGrp[group] = menuObj
                    # Цикл по элементам группы
                    for key in [key for key, el in ObjectsInfo.items() if el[0] == group]:

                        comp_type = ObjectsInfo[key][3]['type']
                        if comp_type in ObjList and comp_type not in NonObjList:
                            id = icwidget.icNewId()
                            item = flatmenu.FlatMenuItem(menuObj, id, key, normalBmp=ObjectsInfo[key][1])
                            menuObj.AppendItem(item)

                            self.menuDict[id] = comp_type
                            self.menuIdDict[comp_type] = id
                            bgr_win.Bind(wx.EVT_MENU, self.OnAddItem, id=id)

                    id = icwidget.icNewId()
                    menuGroup.AppendMenu(id, icDefInf.GroupsInfo[group], menuObj)

                id = icwidget.icNewId()
                menu.AppendMenu(id, u'Добавить', menuGroup)  # Добаить

            id = icwidget.icNewId()
            menu.Append(id, u'Сгенерировать компонент по ресурсу')
            bgr_win.Bind(wx.EVT_MENU, self.OnTempl, id=id)

            self._menu_inherit_comp = id = icwidget.icNewId()
            menu.Append(id, u'Наследовать компонент')
            bgr_win.Bind(wx.EVT_MENU, self.OnInheritComponent, id=id)

            id = icwidget.icNewId()
            menu.Append(id, u'Редактировать модуль объекта')
            bgr_win.Bind(wx.EVT_MENU, self.OnObjModule, id=id)

            id = icwidget.icNewId()
            menu.Append(id, u'Удалить (Del)')  # Удалить
            bgr_win.Bind(wx.EVT_MENU, self.OnDeleteItem, id=id)

            id = icwidget.icNewId()
            item = flatmenu.FlatMenuItem(menu, id, u'Копировать (Ctrl - Ins)', normalBmp=common.imgEdtMnuCopy)
            menu.AppendItem(item)
            bgr_win.Bind(wx.EVT_MENU, self.OnCopyItem, id=id)

            id = icwidget.icNewId()
            item = flatmenu.FlatMenuItem(menu, id, u'Копировать дочерние элементы')
            menu.AppendItem(item)
            bgr_win.Bind(wx.EVT_MENU, self.OnCopyChildItems, id=id)

            self._menu_past_cld_id = id = icwidget.icNewId()
            item = flatmenu.FlatMenuItem(menu, id, u'Вставить дочерние элементы')
            menu.AppendItem(item)
            bgr_win.Bind(wx.EVT_MENU, self.OnPasteChildItems, id=id)

            self._menu_insert_before_id = id = icwidget.icNewId()
            item = flatmenu.FlatMenuItem(menu, id, u'Вставить до (Shift - Ins)', normalBmp=common.imgEdtMnuInsertBefore)
            menu.AppendItem(item)
            bgr_win.Bind(wx.EVT_MENU, self.OnPasteItem, id=id)

            self._menu_insert_after_id = id = icwidget.icNewId()
            item = flatmenu.FlatMenuItem(menu, id, u'Вставить после', normalBmp=common.imgEdtMnuInsertAfter)
            menu.AppendItem(item)
            bgr_win.Bind(wx.EVT_MENU, self.OnPasteItemAfter, id=id)

            self._menu_insert_inst_id = id = icwidget.icNewId()
            item = flatmenu.FlatMenuItem(menu, id, u'Вставить вместо')
            menu.AppendItem(item)
            bgr_win.Bind(wx.EVT_MENU, self.OnPasteItemInstead, id=id)

            id = icwidget.icNewId()
            item = flatmenu.FlatMenuItem(menu, id, u'Сгенерировать класс-обертку')
            menu.AppendItem(item)
            bgr_win.Bind(wx.EVT_MENU, self.OnGenClass, id=id)
        else:
            menu = self._right_menu

        # Включаем нужные компоненты

        if self.GetSelection() == self.root:
            item = menu.FindItem(self._menu_inherit_comp)
            item.Enable(True)
        else:
            item = menu.FindItem(self._menu_inherit_comp)
            item.Enable(False)

        if Res_copyBuff is None:
            item = menu.FindItem(self._menu_past_cld_id)
            item.Enable(False)
            item = menu.FindItem(self._menu_insert_before_id)
            item.Enable(False)
            item = menu.FindItem(self._menu_insert_after_id)
            item.Enable(False)
            item = menu.FindItem(self._menu_insert_inst_id)
            item.Enable(False)

        menu.Popup(evt.GetPosition(), bgr_win)

    def OnGenClass(self, evt):
        """
        Генерирует класс по ресурсу при выборе соответствующего пункта меню.
        """
        # Определяем имя класса
        className = 'className'
        dlg_inp = wx.TextEntryDialog(self, u'Введите имя класса', u'', className)

        if dlg_inp.ShowModal() == wx.ID_OK:
            className = dlg_inp.GetValue()

            if resource.icGetResPath():
                mod_dir = resource.icGetResPath()
            else:
                mod_dir = resource.icGetICPath() + '/components/user/objects'

            module_name = mod_dir + '/ic'+className.lower()+'.py'
            ic_dlg.icMsgBox(u'СООБЩЕНИЕ', u'Класс <%s> в модуле <%s>' % (className, module_name))
            # Удаляем из ресурса служебную информацию
            item = self.GetSelection()
            data = self.GetPyData(item)
            res = copy.deepcopy(data)
            text = resource.genClassFromRes(className, res)
            f = open(module_name, 'wb')
            f.write(text.encode('utf-8'))
            f.close()

        dlg_inp.Destroy()

    def OnObjModule(self, evt):
        """
        Создание модуля объекта.
        """
        item = self.GetSelection()
        data = self.GetPyData(item)
        fn = None
        # Если модуль объекта определен, открываем его
        if data['obj_module']:
            fn = self.GetResEditor().get_obj_module_name(data['obj_module'])
            if os.path.isfile(fn):
                return self.GetResEditor().OpenIDEFile(fn)

        # Если модуль объекта не определен предлагаем создать его
        if 1:
            # Выбираем пакет, где будет распологаться модуль
            if resource.icGetResPath():
                pt = resource.icGetResPath().replace('\\', '/')
                dlg = wx.DirDialog(self, u'Выберите пакет модуля (%s)' % resource.icGetSubsys(),
                                   style=wx.DD_DEFAULT_STYLE)
            else:
                pt = __file__.replace('\\', '/')
                pt = pt.replace('/ic/PropertyEditor/icResTree', '').replace('.pyc', '').replace('.py', '')
                dlg = wx.DirDialog(self, u'Выберите пакет модуля', style=wx.DD_DEFAULT_STYLE)

            dlg.SetPath(pt)

            # If the user selects OK, then we process the dialog's data.
            # This is done by getting the path data from the dialog - BEFORE
            # we destroy it.
            path = None

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()

            # Only destroy a dialog after you're done with it.
            dlg.Destroy()

            # Выбираем имя модуля
            if path:
                rmn = self.GetResEditor().get_res_module_name()
                obj_name = 'type:%s name:%s resource: %s' % (data['type'], data['name'], self.GetResEditor().file)

                name = data['name']+'.py'
                dlg_inp = wx.TextEntryDialog(self,
                                             u'Пакет <%s>' % path,
                                             u'Введите имя модуля:', name)

                if dlg_inp.ShowModal() == wx.ID_OK:
                    name = dlg_inp.GetValue()

                    if '.py' in name.lower():
                        path = path + '/' + name
                    else:
                        path = path + '/' + name + '.py'

                    # Создаем модуль объекта
                    self.GetResEditor().create_obj_module(obj_name, path.replace('\\', '/'))

                    # Прописываем ссылку в модуле ресурса
                    if rmn and os.path.isfile(rmn):
                        resource.updateImporsObjModule(rmn, path)

                    # Прописываем имя модуля объекта в ресурсе
                    path = path.replace('\\', '/')
                    data['obj_module'] = path.replace(pt, '').replace('\\', '/')
                    self.GetResEditor().RefreshPropertySelObj()

                    if not os.path.exists(fn):
                        log.warning(u'Файл <%s> не найден' % fn)
                    else:
                        self.GetResEditor().OpenIDEFile(fn)

                dlg_inp.Destroy()
            else:
                return

    def OnTempl(self, evt):
        """
        Вызывает функцию генерации компонента по ресурсу.
        """
        # Определяем тип компонента
        compType = 'defaultType'
        dlg_inp = wx.TextEntryDialog(self,
                                     u'Введите тип компонента', u'', compType)

        if dlg_inp.ShowModal() == wx.ID_OK:
            compType = dlg_inp.GetValue()
            import ic.utils.modulGenerator as gen
            item = self.GetSelection()
            data = self.GetPyData(item)
            res = copy.deepcopy(data)

            gen.GenComponent(compType, res=res)

        dlg_inp.Destroy()

    def OnInheritComponent(self, evt):
        """
        Наследует компонент от другого компонента системы.
        """
        compType = u'defaultType'
        dlg_inp = wx.TextEntryDialog(self,
                                     u'Пример: MyComponentType',
                                     u'Введите тип компонента', compType)
        if dlg_inp.ShowModal() == wx.ID_OK:
            compType = dlg_inp.GetValue()
            if compType:
                prnt_dlg = wx.TextEntryDialog(self,
                                              u'Пример: ic.components.custom.icbutton',
                                              u'Введите модуль родительского компонента', u'')
                if prnt_dlg.ShowModal() == wx.ID_OK:
                    prntModule = prnt_dlg.GetValue()
                    if prntModule:
                        import ic.utils.modulGenerator as gen
                        gen.InheritComponent(compType.encode('utf-8'), prntModule.encode('utf-8'))
                    else:
                        wx.MessageBox(u'ОШИБКА. Модуль родительского компонента не определен.', style=wx.wx.ICON_ERROR)
            else:
                wx.MessageBox(u'ОШИБКА. Тип компонента не определен', style=wx.wx.ICON_ERROR)

            prnt_dlg.Destroy()
        dlg_inp.Destroy()

    def OnCopyItem(self, evt):
        """
        Копирует описание объекта в буффер.
        """
        if not self.editor.isToggleEnable():
            return

        item = self.GetSelection()
        setCopyBuffEdt(self.GetPyData(item))

    def OnCopyChildItems(self, evt):
        if not self.editor.isToggleEnable():
            return
        item = self.GetSelection()
        data = self.GetPyData(item)
        if 'child' in data and data['child']:
            setCopyBuffEdt(self.GetPyData(item))
        else:
            wx.MessageBox(u'Компонент не имеет дочерних элементов')

    def _isCanContain(self, typ, typIns):
        """
        Возвращает разрешающий признак для возможности вставить объект
        одного тива в другой.

        @param typ: Тип объекта, в который вставляется.
        @param typIns: Тип объекта, который вставляется.
        """
        info = self.GetObjectsInfo()[typ]
        mod = info[-1]
        NonObjList = []

        if mod and hasattr(mod, 'get_can_contain_lst'):
            ObjList = mod.get_can_contain_lst(self.GetResEditor())

        elif info[4] == -1 or info[4] is None:
            if len(info) > 5:
                NonObjList = info[5]
            ObjList = self.GetObjectsInfo().keys()
        else:
            ObjList = info[4]

        # Проверяем можно ли скопировать в текущий объект
        if typIns in ObjList and typIns not in NonObjList:
            return True

        return False

    def OnPasteChildItems(self, evt):
        """
        Вставляем в ресурс дочерние элементы скопированного ресурса.
        """
        # Берем объект из буффера
        insObj = getCopyBuffEdt()
        item = self.GetSelection()
        res = self.GetPyData(item)
        lst = insObj.get('child', [])
        for el in lst:
            res_obj = copy.deepcopy(el)
            res_obj, spc = findSpcStruct(res_obj)
            if self._isCanContain(res['type'], el['type']) and res != self.resource:
                self.AddItem(item, res_obj, bRefreshEditor=False)
            else:
                ic_dlg.icWarningBox(u'ОШИБКА',
                                    u'Не возможно вставить объект %s в %s' % (el['type'], res['type']))

        if lst:
            self.GetResEditor().RefreshGraphEditor()

    def OnPasteItem(self, evt):
        """
        Вставляет описание объекта из буффера перед текущим элементом
        описания.
        """
        # Берем объект из буффера
        insObj = getCopyBuffEdt()

        if not self.editor.isToggleEnable() or insObj is None:
            return

        sel = self.GetSelection()
        item = self.GetItemParent(sel)
        res = self.GetPyData(item)

        if self._isCanContain(res['type'], insObj['type']) and res != self.resource:
            self.InsItem(sel, copy.deepcopy(insObj))
        else:
            ic_dlg.icWarningBox(u'ОШИБКА',
                                u'Не возможно вставить объект %s в %s' % (insObj['type'], res['type']))

    def OnPasteItemAfter(self, evt):
        """
        Вставляет описание объекта из буффера после текущего
        элемента описания.
        """
        # Берем объект из буффера
        insObj = getCopyBuffEdt()

        if not self.editor.isToggleEnable() or insObj is None:
            return

        sel = self.GetSelection()
        item = self.GetItemParent(sel)
        res = self.GetPyData(item)

        if self._isCanContain(res['type'], insObj['type']) and res != self.resource:
            self.InsItem(sel, copy.deepcopy(insObj), 1)
        else:
            ic_dlg.icWarningBox(u'ОШИБКА',
                                u'Не возможно вставить объект %s в %s' % (insObj['type'], res['type']))

    def OnPasteItemInstead(self, evt):
        """
        Вставляет описание объекта из буффера вместо текущего элемента описания.
        """
        # Берем объект из буффера
        insObj = getCopyBuffEdt()

        if not self.editor.isToggleEnable() or insObj is None:
            return

        sel = self.GetSelection()
        item = self.GetItemParent(sel)
        res = self.GetPyData(item)

        if self._isCanContain(res['type'], insObj['type']) and res != self.resource:
            self.InsItem(sel, copy.deepcopy(insObj), 2)
        else:
            ic_dlg.icWarningBox(u'ОШИБКА',
                                u'Не возможно вставить объект %s в %s' % (insObj['type'], res['type']))

    def OnAddItem(self, evt):
        """
        Добавляет описание объекта в ресурс.
        """
        id = evt.GetId()
        obj_type = self.menuDict[id]
        item = self.GetSelection()
        res = self.GetPyData(item)

        spc_res = ObjectsInfo[obj_type][3]
        res_obj = copy.deepcopy(spc_res)
        res_obj, spc = findSpcStruct(res_obj)
        self.AddItem(item, res_obj)
        
    def OnDeleteItem(self, evt):
        """
        Удаляет из ресурса описание объекта.
        """
        self.lastSel = self.root
        item = self.GetSelection()
        self.DeleteItem(item)

    def OnSelChanged(self, evt, item=None):
        """
        Функция отрабатывает при изменении выбранного пункта дерева.
        """
        if evt:
            item = evt.GetItem()
            
        if not item:
            return

        data = self.GetPyData(item)
        if data and '__item_id' in data:
            iditem = data['__item_id']

            # Запоминаем идентификатор выбранного узла.
            key = getResKey(self.res)
            if key:
                addOpenTreeItemId(key, iditem)

        # Обновляем ресурсное описание
        if self.editor is not None:
            if item != self.root and data:
                # Дополняем ресурсное описание до спецификации
                data, spc = findSpcStruct(data)
                # Ссылка на файл документации обновляем, т. к. его название
                # и расположение может меняться
                if spc and 'docstr' in spc:
                    data['docstr'] = spc['docstr']
                # Заполняем редактор новыми свойствами
                prnt_item = self.GetItemParent(item)
                prnt_res = self.GetPyData(prnt_item)
                self.editor.notebook.GetPropertyEditor().setResource(data, spc, prnt_res)

                # В графическом редакторе находим нужный объект и делаем его текущим
                # если задан соответствующий признак
                if self.GetResEditor().graphEditor and self.bSelInGraphEdt:
                    pnl = self.GetResEditor().graphEditor.GetEditorPanel()
                    pnl.SelectObjId(iditem)

                self.bSelInGraphEdt = True
            elif item == self.root:
                self.editor.notebook.GetPropertyEditor().setResource(None)
                if self.GetResEditor() and self.GetResEditor().graphEditor:
                    pnl = self.GetResEditor().graphEditor.GetEditorPanel()
                    if self.GetCount() > 1:
                        pnl.toolpanel.EnableAllType(False)
                    else:
                        pnl.toolpanel.EnableAllType(True)

        self.lastSel = item
        if evt:
            evt.Skip()

    def OnHelpFind(self):
        """
        Создает диалог для поиска.
        """
        self.lastfindItem = None
        self.finddlg = wx.FindReplaceDialog(self, self.finddata, 
                                            u'Поиск в дереве',
                                            wx.FR_NOUPDOWN |
                                            wx.FR_NOMATCHCASE |
                                            wx.FR_NOWHOLEWORD)
        self.finddlg.Show(True)

    def parseTree(self, res):
        """
        Функция по ресурсному описанию строит дерево описаниея.
        @type res: C{dictionary}
        @param res: Ресурсное описание формы.
        @rtype: C{bool}
        @return: Признок успешного выполнения.
        """
        # Чистим буфер идентификаторов объектов дерева
        self._initPicDict()
        self._treeItemId = -1
        self._lastTreeId = None

        try:
            self.res = res
            self.lastSel = self.root

            if isinstance(res, list):
                for item in res:
                    self.addBranch(self.root, item)
            elif res is not None and res != {}:
                self.addBranch(self.root, res)
        except:
            ic_dlg.icFatalBox(u'ОШИБКА')
            return False

        if self._lastTreeId:
            self.EnsureVisible(self._lastTreeId)
            self.SelectItem(self._lastTreeId)

        return True

    def SetTextColor(self, parent, bActive=True):
        """
        Устанавливает цвет текста в зависимости от атрибута <activate>.
        """
        ck = 0
        data = self.GetPyData(parent)
        if data is None:
            return

        if not bActive or ('activate' in data and data['activate'] in [0, '0', 'False']):
            self.SetItemTextColour(parent, wx.Colour(*DEACTIVATE_COLOR))
            bActive = False
        else:
            self.SetItemTextColour(parent, wx.Colour(*ACTIVATE_COLOR))

        # Создаем список дочерних элементов
        while 1:
            if ck == 0:
                child, ck = self.GetFirstChild(parent)
            else:
                child, ck = self.GetNextChild(parent, ck)

            if child.IsOk():
                self.SetTextColor(child, bActive)
            else:
                break

    def SelectResId(self, res_id, bSelInGraphEdt=False):
        """
        Выбирает элемент дерева по идентификатору ресурса.
        @type res_id: C{int}
        @param res_id: идентификатор ресурса.
        @type bSelInGraphEdt: C{Bool}
        @param bSelInGraphEdt: Признак обновления текущего выбора в графическом редакторе.
        """
        try:
            if self.GetResEditor().graphEditor:
                self.bSelInGraphEdt = bSelInGraphEdt
            treeId = self._dictResTreeId[res_id]
            self.EnsureVisible(treeId)
            self.SelectItem(treeId)
            return True
        except:
            io_prnt.outErr(u'Элемент с id = %s не найден' % str(res_id))

        return False

    def SetPanelGroup(self, panel):
        """
        Устанавливает указатель на панель групп.
        """
        self._groupPanel = panel

    def SetResEditor(self, edt):
        """
        Устанавливает указатель на редактор ресурса.
        """
        self.editor = edt


SPC_IC_RESNOTEBOOK = {'name': 'resnotebook',
                      'type': 'ResNotebook',
                      'res': {},                    # Ресурсное описание компонента, который редактируется
                      'position': (-1, -1),
                      'size': (-1, -1),
                      'foregroundColor': None,
                      'backgroundColor': None,
                      'style': 0
                      }


class icPropertyNotebookGrp:
    """
    Компонент позволяет редактировать аттрибуты компонента, выбранного в дереве
    ресурсного описание формы. Атрибуты сгруппированы по трем группам: 'базовые',
    'специальные', 'все'.
    """

    def __init__(self, parent, sizer=None, logType=0):
        """
        Конструктор для создания редактора атрибутов компонента.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        """
        self._propEditor = icpropertyeditmanager.icPropertyEditorManager(parent)
        if sizer:
            sizer.Add(self._propEditor, 1, wx.EXPAND)

    def GetPropertyEditor(self):
        """
        Возвращает указатель на редактор свойств.
        """
        return self._propEditor


SPC_IC_RESEDITOR = {'name': 'res',
                    'type': 'ResEditor',
                    'res': None,
                    'position': (-1, -1),
                    'size': (250, -1),
                    'foregroundColor': None,
                    'backgroundColor': None,
                    'file': None,
                    'style_work': None,
                    'style': wx.SP_3D
                    }
TBFLAGS = (wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)


class icResourceEditor(icwidget.icWidget, wx.SplitterWindow):
    """
    Редактор ресурсов форм.
    """

    def __init__(self, parent, id, component={}, logType=0, evalSpace={}):
        """
        Конструктор для создания редактора ресурсов.
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
        # Инициализируем информационную структуру об объектах формы.
        common.img_init()
        if not GetObjectsInfo():
            InitObjectsInfo()

        self.spc = SPC_IC_RESEDITOR
        icSpcDefStruct(self.spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        size = component['size']
        pos = component['position']
        style = component['style']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        self.res = component['res']
        self.file = component['file']

        # Имя редактируемой формы
        self._formName = None
        self._version = None
        #
        self._positionEditor = 0, 0
        self._sizeEditor = (-1, -1)

        # Указатель на интерфайс взаимодействия со средой разработки (в частности drFrame)
        self._IDEEditorInterface = None
        # Указатель на панель инструментов
        self._toolpanel = None

        wx.SplitterWindow.__init__(self, parent, id, pos, size, style)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.SetSize(size)

        panel = wx.Panel(self, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(self, -1)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        self.tree = icResTree(panel, -1)
        self.tree.parseTree(self.res)
        self.tree.Expand(self.tree.root)

        self.SplitHorizontally(panel, panel2, 100)

        self.toolbar = wx.ToolBar(panel, icwidget.icNewId(), pos=(0, 0), size=(300, -1),
                                  style = TBFLAGS)
        self.toolbar.SetToolBitmapSize(wx.Size(16, 16))
        # ВНИМАНИЕ!!! Устанавливать цвет фона не надо, иначе он прорисовывается на кнопках!!!

        # В режиме самостоятельного редактора появляются кнопки для
        # работы с файлами ресурсов (Создать, открыть, сохранить, ...).
        if component['style_work'] == 'single':
            id = icwidget.icNewId()
            self.toolbar.AddTool(bitmap=common.imgFolderOpen,  shortHelpString=u'Открыть', id=id)
            self.Bind(wx.EVT_TOOL, self.OnLoad, id=id)

            id = icwidget.icNewId()
            self.toolbar.AddTool(bitmap=common.imgSave, shortHelpString=u'Сохранить', id=id)
            self.Bind(wx.EVT_TOOL, self.OnSave, id=id)

            id = icwidget.icNewId()
            self.toolbar.AddTool(bitmap=common.imgSaveAs, shortHelpString=u'Сохранить как ...', id=id)
            self.Bind(wx.EVT_TOOL, self.OnSaveAs, id=id)

        id = icwidget.icNewId()
        self.toolbar.AddTool(bitmap=common.imgTrash, shortHelpString=u'Удалить', id=id)
        self.Bind(wx.EVT_TOOL, self.OnDelete, id=id)

        id = icwidget.icNewId()
        self.toolbar.AddSeparator()
        self.toolbar.AddTool(bitmap=common.imgPlay, shortHelpString=u'Тестировать', id=id)
        self.Bind(wx.EVT_TOOL, self.OnTest, id=id)

        self.toolbar.AddSeparator()

        # Кнопка для вызова графического редактора
        id = icwidget.icNewId()
        self.toolbar.AddTool(bitmap=common.imgDesigner, shortHelpString=u'Дизайнер', id=id)
        self.Bind(wx.EVT_TOOL, self.OnGraphEditor, id=id)

        # Кнопка для генерации пользовательского класса
        id = icwidget.icNewId()
        self.toolbar.AddTool(bitmap=common.imgEdtComponent,
                             shortHelpString=u'Создать пользовательский компонент', id=id)
        self.Bind(wx.EVT_TOOL, self.OnUserClass, id=id)

        id = icwidget.icNewId()
        self.toolbar.AddTool(bitmap=common.imgEdtResModule, shortHelpString=u'Модуль ресурса', id=id)
        self.Bind(wx.EVT_TOOL, self.OnPyScript, id=id)

        self.toolbar.Realize()

        # Редактор свойств
        self.sizer.Add(self.toolbar, 0, wx.EXPAND)
        self.sizer.Add(self.tree, 1, wx.EXPAND)
        panel.SetSizer(self.sizer)

        self.notebook = icPropertyNotebookGrp(panel2)
        sizer2.Add(self.notebook.GetPropertyEditor(), 1, wx.EXPAND)
        panel2.SetSizer(sizer2)
        self.notebook.GetPropertyEditor().setResTree(self.tree)

        # Устанавливаем ссылки на редактор
        self.notebook.editor = self
        self.tree.SetResEditor(self)
        self.__editorEnable = True
        # Признак активности графического редактора
        self.__enableGraphEditor = False
        # Ссылка на графический редактор
        self.graphEditor = None
        # Признак работы редактор как самостоятельного приложения
        self.isSingleMode = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.parent.Bind(wx.EVT_CLOSE, self.OnClose)

        # При необходимости открываем ресурсный файл
        if self.file is not None:
            self.LoadRes(self.file)

        # Если в в буфере есть идентификатор последнего выбранного узла,
        # то выбираем его в качестве текущего
        if self.tree._lastTreeId:
            self.tree.EnsureVisible(self.tree._lastTreeId)
            self.tree.SelectItem(self.tree._lastTreeId)

        # Пользоваетльское событие для вызова графического редактора
        self.Bind(icEvents.EVT_POST_INIT, self.OnGraphEditor)

    def SetSingleMode(self, mode=True):
        """
        Устанавливает признак самостоятельного приложения. Если этот признак
        установлен в True, то происходит автоматическая разстановка панельей редактора,
        в противном случае нет.
        """
        self.isSingleMode = mode

    def SetIDEInterface(self, interface):
        """
        Устанавливает указатель на интерфайс взаимодействия со средой разработки
        (в частности с drPython).
        """
        self._IDEEditorInterface = interface

    def GetIDEInterface(self):
        """
        Возвращает указатель на интерфайс взаимодействия со средой разработки
        (в частности с drPython).
        """
        return self._IDEEditorInterface

    # Работа с ресурсами
    def CloseResource(self, bSave=True, bSaveAs=True, bCloseGrpEdt=True):
        """
        Закрывает существующий ресурс.
        """
        # Если редактор был привязан к дереву свойств, то пытаемся
        # отвязвться - в редакторе свойств соответствующий указатель
        # устанавливается в None.
        if self.graphEditor and bCloseGrpEdt:
            self.graphEditor.Close(True)

        # Сохраняем старый ресурс
        if bSave:
            if self.GetResource() and self.isToggleEnable():
                self.OnSave(None, bSaveAs=bSaveAs)

        # Чистим переменные
        self.res = None
        self.file = None
        self._formName = None
        self._version = None

        # Обновляем дерево
        self.RefreshTree()

    def CreateResource(self, nameRes, filePath, fileName, fileExt, templ=None, bRecreate=False):
        """
        Создает ресурс заданного типа.
        @type nameRes: C{string}
        @param nameRes: Имя ресурса в ресурсном файле.
        @type filePath: C{string}
        @param filePath: Полный путь до ресурсного файла.
        @type fileName: C{string}
        @param fileName: Имя фйла ресурса без расширения.
        @type fileExt: C{string}
        @param fileExt: Расширение файла ресурса.
        @type templ: C{string}
        @param templ: Шаблон ресурса.
        @type bRecreate: C{bool}
        @param bRecreate: Признак пересоздания.
        @rtype: C{int}
        @return: Код завершения операции: 1 - ресурс успешно создан; 0 - ресурс с
            таким именем в заданном ресурсном файле существует; -1 - директория не найдена.
        """
        path = '%s/%s.%s' % (filePath, fileName, fileExt)
        path = path.replace('\\', '/').replace('//', '/')
        # Если ресурс является прикладным компонентом (питоновским модулем)
        if fileExt == 'py':
            if os.path.isdir(filePath) and (not os.path.isfile(path) or bRecreate):
                text = resource.genClassFromRes(nameRes, templ)
                file_obj = open(path, 'wb')
                file_obj.write(text.encode('utf-8'))
                file_obj.close()
                return 1
            elif not os.path.isdir(filePath):
                return -1

            elif os.path.isfile(path):
                return 0
        # Словарно - списковой структурой
        else:
            if os.path.isdir(filePath) and (not os.path.isfile(path) or bRecreate):
                _res = {nameRes: templ}
                text = str(_res)
                file_obj = open(path, 'wb')
                file_obj.write(text)
                file_obj.close()
                return 1
            elif not os.path.isdir(filePath):
                return -1
            elif os.path.isfile(path):
                _res = util.readAndEvalFile(path, bRefresh=True)
                # Проверяем существует ли в заданном файле ресурс с заданным именем.
                if nameRes in _res.keys():
                    return 0
                else:
                    _res[nameRes] = None
                    text = str(_res)
                    file_obj = open(path, 'wb')
                    file_obj.write(text)
                    file_obj.close()
                    return 1

    def get_res_module_name(self, rn=None):
        """
        Возвращает имя модуля ресурса.
        @param rn: Имя ресурса.
        """
        if not rn:
            rn = self.file

        rn = rn.replace('\\', '/')
        if rn:
            p, nm = os.path.split(rn)
            fn = p + '/'+nm.replace('.', '_')+'.py'
        else:
            return rn

        return fn

    def get_obj_module_name(self, name='', rn=None):
        """
        Возвращает имя модуля объекта.
        @param name: Имя ресурса.
        @param rn: Имя объекта.
        """
        if not rn:
            rn = self.file

        if rn:
            p, nm = os.path.split(rn)
            fn = p + '/' + name
        else:
            return rn

        return fn

    def create_res_module(self, rn=None):
        """
        Создает модуль ресурса.
        @type rn: C{unicode}
        @param rn: Имя ресурса.
        """
        # Определяем имя модуля ресурса.
        fn = self.get_res_module_name(rn)
        if os.path.isfile(fn):
            return fn

        txt = resource.genResModuleHead(rn, fn)
        file_obj = open(fn, 'wb')
        file_obj.write(txt)
        file_obj.close()
        return fn

    def create_obj_module(self, name, fn=None):
        """
        Создает модуль ресурса.
        @param fn: Имя файла ресурса.
        """
        if os.path.isfile(fn):
            ic_dlg.icMsgBox(u'СООБЩЕНИЕ', u'Файл <%s> существует' % fn)
            return fn

        txt = resource.genObjModuleHead(name, fn)
        f = open(fn, 'wb')
        f.write(txt)
        f.close()
        return fn

    def Destroy(self):
        """
        Обновляет структуру ресурсного описания и удаляет окно.
        """
        # Если редактор был привязан к дереву свойств, то пытаемся
        # отвязвться - в редакторе свойств соответствующий указатель
        # устанавливается в None.
        if self.graphEditor:
            if self.graphEditor.toolpanel:
                self.graphEditor.toolpanel.Close(True)
            self.graphEditor.Close(True)
        paneltool = GetPanelToolBuff()
        if paneltool:
            paneltool.Destroy()
        SetPanelToolBuff(None)
        wx.SplitterWindow.Destroy(self)

    def CloseResource2(self, bSaveAs=True):
        """
        Выгружает ресурс из реадктора.
        """
        if self.GetResource() and self.isToggleEnable():
            self.OnSave(None, bSaveAs=bSaveAs)

        # Чистим переменные
        self.res = None
        self.file = None
        self._formName = None
        self._version = None
        self.RefreshTree()

    def GetResource(self):
        """
        Возвращает на ресурсное описание без служебных ключей.
        """
        if self.res:
            res = copy.deepcopy(self.res)
            resource.delResServiceInfo(res)
            return res

    def GetResFileName(self):
        """
        Возвращает имя файла, где хранится ресурс.
        """
        return self.file

    def GetResName(self):
        """
        Возвращает имя ресурса.
        """
        return self._formName

    def SetResource(self, nameRes, filePath, fileName, fileExt, bEnable=True):
        """
        Устанавливает ресурс на редактирование.
        @type nameRes: C{string}
        @param nameRes: Имя ресурса в ресурсном файле.
        @type filePath: C{string}
        @param filePath: Полный путь до ресурсного файла.
        @type fileName: C{string}
        @param fileName: Имя фйла ресурса без расширения.
        @type fileExt: C{string}
        @param fileExt: Расширение файла ресурса.
        @type bEnable: C{bool}
        @param bEnable: Признак возможности редактирования.
        """
        # Сохраняем старый ресурс
        if self.GetResource() and self.isToggleEnable():
            self.OnSave(None)

        fname = '%s/%s.%s' % (filePath, fileName, fileExt)
        fname = fname.replace('\\', '/').replace('//', '/')
        self.LoadRes(fname, nameRes)
        #
        if isinstance(self.parent, icProjectNB):
            self.parent.SetSelection(1)
            
        self.ToggleEnable(bEnable)

    def RenameResource(self, oldNameRes, oldFileName, nameRes, fileName):
        """
        Переименовывает имя ресурса и имя файла ресурсов.
        @type oldNameRes: C{string}
        @param oldNameRes: Старое имя ресурса.
        @type oldFileName: C{string}
        @param oldFileName:  Старое имя ресурсного файла.
        @type nameRes: C{string}
        @param nameRes:  Новое имя ресурса.
        @type fileName: C{string}
        @param fileName: Новое имя ресурсного файла.
        @rtype: C{bool}
        @return: Возвращает признак успешного переименования.
        """
        if ic_file.SamePathWin(self.file, oldNameRes) or ic_file.SamePathWin(self.file, fileName):
            self.CloseResource(bSaveAs=False, bCloseGrpEdt=False)

        # Читаем старый ресурс
        if fileName[-3:] == '.py':
            try:
                shutil.copyfile(oldFileName, fileName)
                os.remove(oldFileName)
            except:
                io_prnt.outErr(u'###')
                return False
        else:
            res = util.readAndEvalFile(oldFileName, bRefresh=True)
            old_mod = self.get_res_module_name(oldFileName)
            new_mod = self.get_res_module_name(fileName)

            if res and oldNameRes in res:
                obj_res = res.pop(oldNameRes)

                if obj_res:
                    obj_res['name'] = nameRes
                    obj_res['res_module'] = new_mod.split('/')[-1]

                res = {}
                res[nameRes] = obj_res

            else:
                io_prnt.outLog(u'Не найден ресурс <%s> в <%s>' % (oldNameRes, oldFileName),
                               Device_=io_prnt.IC_LOG_CONSOLE)
                return False

            # Сохраняем измененный ресурс
            try:
                f = open(fileName, 'wb')
                f.write(str(res))
                f.close()
                io_prnt.outLog(u'Переименовать ресурс <%s> в <%s>' % (oldFileName, fileName),
                               Device_=io_prnt.IC_LOG_CONSOLE)
                self.file = fileName
                self.res = obj_res
                self._formName = nameRes

                # Удаляем старый ресурсный файл
                if oldFileName != fileName:
                    #   Переименовываем модуль ресурса
                    if os.path.isfile(old_mod):
                        os.rename(old_mod, new_mod)
                        io_prnt.outLog(u'Переименовать модуль ресурса <%s> в <%s>' % (old_mod, new_mod),
                                       Device_=io_prnt.IC_LOG_CONSOLE)

                    # Удаляем старые файлы ресурса
                    os.remove(oldFileName)
                    io_prnt.outLog(u'Удалить файл: %s' % oldFileName, Device_=io_prnt.IC_LOG_CONSOLE)

                    if '.' in oldFileName:
                        pkl = oldFileName.replace('.', '_pkl.')
                    else:
                        pkl = oldFileName+'_pkl'

                    # Удаляем старый скомпилированный ресурсный файл
                    os.remove(pkl)
                    io_prnt.outLog(u'<pkl> файл <%s> удален' % pkl, Device_=io_prnt.IC_LOG_CONSOLE)

                # Убираем ресурс из буфера
                util.clearResourceBuff()
            except:
                io_prnt.outErr(u'Ошибка создания файла <%s>' % fileName,
                               Device_=io_prnt.IC_LOG_CONSOLE)
                return False

        return True

    def InitObjectsInfo(self, bRefresh=False):
        """
        Инициализация информации о компонентах.
        """
        InitObjectsInfo(bRefresh=bRefresh)

    def isToggleEnable(self):
        """
        Возвращает признак редактирования.
        """
        return not self.notebook.GetPropertyEditor().isReadOnly()

    def GraphEditor(self):
        """
        Вызов графического редактора.
        """
        if self.graphEditor:
            self._positionEditor = tx, ty = self.graphEditor.GetPosition()
            self._sizeEditor = sx, sy = self.graphEditor.GetSize()
            self.graphEditor.Close(True)
        else:
            tx, ty = self._positionEditor
            sx, sy = self._sizeEditor

        # Инициализируем пространство имен формы
        evalSpace = icwidget.icResObjContext()
        # Чистим буффер ресурсов
        util.clearResourceBuff()
        # Устанавливаем режим редактирования и передаем указатель на редактор форм
        icResourceParser.setEditorPoint(self)
        # Создаем форму
        prsObj = icResourceParser.CreateForm(u'Редактор форм',
                                             formRes=copy.deepcopy(self.res), parent=self, bIndicator=False)

        # Для оконных компонентов надо вызвать метод Show
        if prsObj:
            self.graphEditor = prsObj.evalSpace['_root_obj']
            self.graphEditor.GetEditorPanel().SetPointer(self)
            self.graphEditor.Show()
            # Создаем панель инструментов
            self.graphEditor.CreateToolPanel(GetObjectsInfo())
        if self.graphEditor and self.graphEditor.toolpanel:
            dx, dy = self.graphEditor.toolpanel.GetSize()
        else:
            dx, dy = (0, 0)

        if self.graphEditor:
            if self.isSingleMode:
                self.parent.SetPosition((0, dy))
                self.graphEditor.SetPosition((tx, ty))
                self.graphEditor.SetSize((sx, sy))
                self.graphEditor.SetFocus()
                self.graphEditor.Show()
            else:
                self.parent.Refresh()
                self.graphEditor.SetPosition((tx, ty))
                self.graphEditor.SetSize((sx, sy))
                self.graphEditor.SetFocus()
                self.graphEditor.Show()

            # Устанавливаем текущий объект редактирования
            pnl = self.graphEditor.GetEditorPanel()
            item = self.tree.lastSel
            if pnl and item:
                iditem = self.tree.GetPyData(item)['__item_id']
                pnl.SelectObjId(iditem)

    def is_res_module(self, path):
        """
        Признак того, что ресурс хранится в питоновском модуле.
        """
        if path and os.path.split(path)[1].endswith('.py'):
            return True
        else:
            return False
            
    def LoadRes(self, path, formName=None):
        """
        Загружает ресурсное описание.
        @type path: C{string}
        @param path: Путь до файла.
        @rtype: C{bool}
        @return: Признак успешного выполнения.
        """
        # Если редактор был привязан к дереву свойств, то пытаемся
        # отвязвться - в редакторе свойств соответствующий указатель
        # устанавливается в None.
        if self.graphEditor:
            self.graphEditor.Close(True)
        try:
            #
            # Если расширение объекта 'py', то импортируем модуль - ресурс
            # берем из атрибута модуля 'resource'
            if self.is_res_module(path):
                self.res, self._formName, self._version = resource.getICObjectResource(path)
            else:
                _res = util.readAndEvalFile(path, bRefresh=True)
                if formName and formName in _res.keys():
                    self.res = _res[formName]
                    self._formName = formName
                elif formName and formName not in _res.keys():
                    ic_dlg.icWarningBox(u'ОШИБКА',
                                        u'Не найдена форма <%s> в <%s>' % (formName, path))
                elif len(_res.keys()) == 1:
                    self._formName = _res.keys()[0]
                    self.res = _res[self._formName]
                else:
                    # Выбор нужного ресурсного описания
                    dlg = wx.SingleChoiceDialog(self,
                                                u'Выберите форму', u'Форма', _res.keys(), wx.OK | wx.CANCEL)
                    try:
                        if dlg.ShowModal() == wx.ID_OK:
                            key = dlg.GetStringSelection()
                            self.res = _res[key]
                            self._formName = key
                    except:
                        key = None

                    dlg.Destroy()
                    if key is None:
                        return False
            self.file = path
            self.RefreshTree()
        except:
            io_prnt.outErr(u'Ошибка в LoadRes')
            return False

        return True

    def OnClose(self, evt):
        """
        Обрабатываем сообщение о закрытии окна  <EVT_CLOSE>.
        """
        # Если редактор был привязан к дереву свойств, то пытаемся
        # отвязвться - в редакторе свойств соответствующий указатель
        # устанавливается в None.
        if self.graphEditor:
            self.graphEditor.Close(True)

        evt.Skip()

    def open_ide_py_module(self, py_filename=None):
        """
        Открываем на редактирование модуль Python с менеджером ресурса.
        @param py_filename: Модуль питона с менеджером ресурса.
        @return: True/False.
        """
        res_name = None
        if py_filename is None:
            if self.file and '.py' in self.file:
                py_filename = self.file.replace('\\', '/')
            elif self.file:
                res_name = self.file.replace('\\', '/')
                py_filename = None

        if py_filename is None and res_name:
            py_filename = self.create_res_module(res_name)
            py_path, py_name = os.path.split(py_filename)
            # Проверяем если имя модуля не проставлено в ресурсе, то проставляем его
            res = self.GetResource()
            if not ('res_module' in res and res['res_module']):
                self.res['res_module'] = py_name
                self.RefreshTree()
        if py_filename:
            self.OpenIDEFile(py_filename)
            return True
        return False

    def OnPyScript(self, evt):
        """
        Вызывает на редактирование обработчик событий для ресурсов, оформленных в виде
        питоновского модуля.
        """
        self.open_ide_py_module()

    def OpenIDEFile(self, fl):
        """
        Загружает либо выбирает модуль для редактирования.
        """
        ide = self.GetIDEInterface()
        if ide:
            alreadyopen = ide.GetAlreadyOpen()
            if fl not in alreadyopen:
                ide.OpenFile(fl, True)
            else:
                ide.SelectFile(fl)

    def OnGraphEditor(self, evt):
        """
        Обработка нажатия кнопки вызова графического редактора.
        """
        if self.isToggleEnable():
            return self.open_formeditor_doc()

    def open_formeditor_doc(self):
        ide = self.GetIDEInterface()
        if ide:
            icResourceParser.ClearComponentModulDict()
            icResourceParser.setEditorPoint(self)
            edt = ide.OpenFormEditor(copy.deepcopy(self.res), self)
            icResourceParser.setDesignMode(False)
            self.graphEditor = edt or self.graphEditor
            main_win = ide.GetIDEFrame()
            mgr = main_win.GetFrameManager()
            if self.graphEditor and not self._toolpanel:
                self._toolpanel = self.graphEditor.CreateToolPanel(ObjectsInfo=GetObjectsInfo(), parent=main_win)
                if self._toolpanel:
                    mgr.AddPane(self._toolpanel, wx.aui.AuiPaneInfo().
                                Name(u'DefisToolPanel').
                                Caption(u'Defis Tool Panel').Right().
                                Layer(1).
                                CloseButton(True).MaximizeButton(False).
                                BestSize(wx.Size(200, 500)))
            # Востанавливаем ссылку на редактор
            elif self.graphEditor:
                self.graphEditor.designer.toolpanel = self._toolpanel
                self._toolpanel.SetGraphEditor(self.graphEditor.designer)

            mgr.GetPane(u'DefisToolPanel').Show()
            mgr.Update()

    def OnUserClass(self, evt):
        """
        Генерирует пользовательский компонент.
        """
        if self.isToggleEnable():
            import ic.components.icUserClassCreator as ur
            ur.RunWizard(self)
            #   Обновляем информацию о компонентах системы
            InitObjectsInfo()

    def OnHelp(self, evt):
        """
        Вызов справки на компонент.
        """
        self.tree.HelpItem()

    def OnEditor(self, evt):
        """
        Вызов редактора.
        """
        frame = ic_pyed.icPyEditorFrame(None, {'name': 'editor', 'type': 'PyEditor',
                                               'position': (50, 50), 'size': (500, 500)})
        frame.Show()
        evt.Skip()

    def OnLoad(self, evt):
        """
        Загружает ресурсное описание из выбранного файла.
        """
        dlg = wx.FileDialog(self,
                            u'Выберите имя ресурсного файла', u'', u'', _ResCard, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            self.LoadRes(path)
            # Если редактор встроен в IDE - открываем файл в редакторе
            self.OnPyScript(None)

        evt.Skip()

    def OnSave(self, evt, bSaveAs=True):
        """
        Обрабатывает нажатие кнопки 'сохранить'.
        """
        if self.file is None or self.file == '' and bSaveAs:
            #
            if ic_dlg.icAskBox(u'ВНИМАНИЕ', u'Сохранить изменения в ресурсе?'):
                self.OnSaveAs(evt)
        elif self.is_res_module(self.file):
            resource.updateICObject(self.file, self._formName, self.GetResource(), self._version)
            ide = self.GetIDEInterface()
            if ide:
                fl = self.file.replace('\\', '/')
                alreadyopen = ide.GetAlreadyOpen()
                if fl in alreadyopen and not ide.GetModify(fl):
                    ide.ReloadFile(fl)
                elif fl in alreadyopen and ic_dlg.icAskBox(u'ВНИМАНИЕ',
                                                           u'Будет перегружет текущий <%s> файл.\nИзменения будут потеряны.\nУверены?' % fl):
                    ide.ReloadFile(fl)
        else:
            self.SaveRes(self.file)

    def OnSaveAs(self, evt):
        """
        Обрабатывает нажатие кнопки 'сохранить как'.
        """
        dlg = wx.FileDialog(self,
                            u'Выберите имя ресурсного файла', u'', u'', _ResCard, wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            #   Если расширение объекта 'py', то сохраняем как системный объект
            if self.is_res_module(path):
                ret = wx.ID_YES
                if os.path.isfile(path):
                    ret = ic_dlg.icAskDlg(u'ВНИМАНИЕ',
                                          u'Файл существует. Переписать?')
                if ret == wx.ID_YES:
                    #   Ввод имени класса
                    dlg_inp = wx.TextEntryDialog(self,
                                                 u'Введите имя класса', u'', u'')
                    if self._formName not in [None, '']:
                        dlg_inp.SetValue(self._formName)
                    if dlg_inp.ShowModal() == wx.ID_OK:
                        self._formName = dlg_inp.GetValue()
                    else:
                        self._formName = None

                    dlg_inp.Destroy()
                    resource.saveICObject(path, self._formName, self.GetResource())
            else:
                # Ввод нового имени формы
                dlg_inp = wx.TextEntryDialog(self,
                                             u'Введите имя формы', u'', u'')
                if self._formName not in [None, '']:
                    dlg_inp.SetValue(self._formName)
                if dlg_inp.ShowModal() == wx.ID_OK:
                    self._formName = dlg_inp.GetValue()
                else:
                    self._formName = None

                dlg_inp.Destroy()
                self.SaveRes(path, True)
            self.file = path
            if self._formName is not None:
                text_old = u'Имя ресурса: %s' % self._formName
            else:
                text_old = u'Имя ресурса'

            self.tree.SetItemText(self.tree.root, text_old + ' ( ' + path.split('\\')[-1] + ' )')

    def OnDelete(self, evt):
        """
        Удаляет объект из ресурсного описания.
        """
        if self.isToggleEnable():
            self.tree.OnDeleteItem(None)

    def OnTest(self, evt):
        """
        Тестируем компонент, который строится по ресурсному описанию.
        """
        evalSpace = icwidget.icResObjContext(resource.icGetKernel())
        # Чистим буффер ресурсов
        util.clearResourceBuff()
        # Удаляем, импортируемые во время работы модули,
        # из пространства имен.
        ic_user.clearImports()
        icResourceParser.ClearComponentModulDict()
        # Устанавливаем для конструктора форм режим отладки
        icResourceParser.setTestMode(True)
        icResourceParser.setEditorPoint(None, False)
        bExcept = True
        res = self.GetResource()
        # В случае если редактируется модуль
        if self.is_res_module(self.file):
            import imp
            import ic.interfaces.ictemplate as ictemplate
            mod = imp.load_source('testModule', self.file)
            cls = getattr(mod, mod.ic_class_name)(self)

            # В случае редактирования шаблона
            if issubclass(cls.__class__, ictemplate.icTemplateInterface):
                # Регестрируем интерфейс в пространстве имен и прописываем
                # имя используемого интерфейса обработчиков для того, чтобы работали
                # шаблонные обработчики
                cls.SetContext(evalSpace)
                evalSpace.register_wrapper(cls, cls.name)
                res = cls.GetResource()
                bExcept = True

            # В случае редактирования интерфейса
            else:
                obj = cls.getObject()
                try:
                    obj.Show(True)
                    obj.SetFocus()
                    bExcept = False
                except:
                    io_prnt.outErr(u'IMPORT ERROR')
                    bExcept = True

        # В случае если редактируется только ресурсное описание
        if bExcept:
            if res:
                res['__file_res'] = self.file
            mod = GetObjectsInfo()[res['type']][-1]
            cls = getattr(mod, mod.ic_class_name)
            try:
                cls.TestComponentResource(res, context=evalSpace, parent=self, parsemodule=icResourceParser)
            except:
                cls.TestComponentResource(res, context=evalSpace, parent=self)

    def OnSize(self, evt):
        """
        Обработка события на изменение размеров окна.
        """
        sz = evt.GetSize()
        h = self.GetSashPosition()
        self.notebook.GetPropertyEditor().Refresh()
        evt.Skip()

    def RefreshTree(self):
        """
        Обновляет представление дерева.
        """
        self.tree.DeleteChildren(self.tree.root)
        self.tree.parseTree(self.res)
        self.tree.Expand(self.tree.root)
        if self._version:
            v = ' '+str(self._version)
        else:
            v = ''

        if self._formName is not None:
            text_old = u'Имя ресурса: %s' % self._formName+v
        else:
            text_old = u'Имя ресурса'

        path = self.file

        if path:
            self.tree.SetItemText(self.tree.root, text_old + ' ( ' + path.split('\\')[-1] + ' )')
        else:
            self.tree.SetItemText(self.tree.root, text_old)

    def RefreshPropertySelObj(self):
        """
        Функция обновления редактора свойств текущего объекта.
        """
        if self.tree._lastTreeId:
            self.tree.SelectItem(self.tree._lastTreeId)

    def ReleasePointer(self):
        """
        Чистит ссылку на графический редактор.
        """
        if self.graphEditor:
            self._positionEditor = self.graphEditor.GetPosition()
            self._sizeEditor = self.graphEditor.GetSize()
        self.graphEditor = None

    def RefreshGraphEditor(self):
        """
        Обновляет графический редактор.
        """
        if self.graphEditor:
            # Эмулируем нажатие кнопки <графический редактор>
            event = icEvents.icPostInitEvent(icEvents.icEVT_POST_INIT, self.GetId())
            event.SetEventObject(self)
            self.GetEventHandler().AddPendingEvent(event)

    def SaveRes(self, path, bAsk=False):
        """
        Сохраняет ресурсное описание в файл.
        @type path: C{string}
        @param path: Путь до файла.
        @type bAsk: C{bool}
        @param bAsk: Признак запроса на перезапись формы.
        @rtype: C{bool}
        @return: Признак успешного выполнения.
        """
        file_obj = None
        try:
            _res = util.readAndEvalFile(path)
            if _res is None:
                _res = {}
            if self._formName in [None, ''] or (self._formName in _res.keys() and bAsk and ic_dlg.icAskDlg(u'ВНИМАНИЕ',
                u'Форма c таким именем уже существует, переписать?') != wx.ID_YES):
                # Ввод нового имени формы
                dlg = wx.TextEntryDialog(frame, 
                                         u'Введите имя формы', u'', u'')
                if self._formName not in [None, '']:
                    dlg.SetValue(self._formName)
                if dlg.ShowModal() == wx.ID_OK:
                    self._formName = dlg.GetValue()
                else:
                    self._formName = None

                dlg.Destroy()
            if self._formName is None:
                return False
            _res[self._formName] = self.GetResource()
            text = str(_res)
            file_obj = open(path, 'wb')
            file_obj.write(text)
            file_obj.close()
            io_prnt.outLog(u'Сохранить ресурс <%s> в <%s>' % (self._formName, path),
                           Device_=io_prnt.IC_LOG_CONSOLE)
        except IOError:
            if file_obj:
                file_obj.close()
        except:
            ic_dlg.icFatalBox(u'ОШИБКА', u'Ошибка в SaveRes ...')
            return False
        return True

    def ToggleEnable(self, bEnable = True):
        """
        Фунцкия разрешает/запрещает редактирование данных.
        @type bEnable: C{bool}.
        @param bEnable: Флаг разрешения редактирования.
        """
        if self.notebook.GetPropertyEditor():
            self.notebook.GetPropertyEditor().setReadOnly(not bEnable)
        if self.tree._lastTreeId:
            self.tree.SelectItem(self.tree._lastTreeId)


class ResourseEditorFrame(wx.Frame):
    """
    Фрейм для редактора проекта.
    """

    def __init__(self, parent, id=-1, title=u'Редактор форм',
                 size=(-1, -1), pos=(-1, -1), style=wx.DEFAULT_FRAME_STYLE):
        """
        Конструктор.
        """
        wx.Frame.__init__(self, parent, -1, title, size, pos, style)
        self.res_edt = icResourceEditor(self, -1, {'style_work': 'single', 'res': None, 'size': (300, 100)})
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, evt):
        """
        Обработка закрытия окна.
        """
        self.res_edt.Destroy()
        self.Destroy()


def init_locale():
    """
    Инициализация локали.
    """
    from ic.utils import ic_i18n
    the_locale = wx.Locale(ic_i18n.GetLangId('Russian'))

    if the_locale.GetCanonicalName() in ic_i18n.GetAvailLocales():
        the_locale.AddCatalogLookupPathPrefix(ic_i18n.LANG_DIR)
        r1 = the_locale.AddCatalog(ic_i18n.PROG_NAME)
        language = gettext.translation(ic_i18n.PROG_NAME,
                                       ic_i18n.LANG_DIR,
                                       [the_locale.GetCanonicalName()],
                                       fallback=True)
        language.install()
    else:
        del the_locale


def GetProjectEditorOLD(parent, drFrame=None, ifs=None):
    """
    Возвращает редактор проекта.
    @param parent: Родительское окно.
    @param drFrame: Главное окно ide.
    @param ifs: Интерфейс взаимодействия с ide.
    """
    common.img_init()
    if ifs is None:
        if drFrame:
            import ic.interfaces.drPythonInterface as dri
            from . import icPanelTool
            ifs = dri.drPythonInterface(drFrame)
        else:
            ifs = None
    
    # Создаем ядро
    from ic.kernel import ickernel
    ickernel.createEditorKernel()
    cls = icpanelgroupedt.icPanelGroupEdt(parent)
    panel = cls.getObject()
    win1 = cls.GetProjectPanel()
    win2 = cls.GetResourcePanel()
    parent.prj_edt = PrjTree.PrjTree(win1, ifs)
    parent.prj_edt.type = 'PrjTree'
    parent.res_edt = icResourceEditor(win2, -1, {'style_work': 'single', 'res': None, 'size': (300, 100)})

    # Устанавливаем указатель на редакторы
    parent.prj_edt.setResourceEditor(parent.res_edt)
    cls.SetProjectEditor(parent.prj_edt)
    cls.SetResourceEditor(parent.res_edt)
    # Устанавливаем указатель на IDE
    parent.res_edt.SetIDEInterface(ifs)
    # Устанавливаем указатель на панель групп
    parent.res_edt.tree.SetPanelGroup(panel)
    return panel


def GetProjectEditor(parent, drFrame=None, ifs=None):
    """
    Возвращает редактор проекта.
    @param parent: Родительское окно.
    @param drFrame: Главное окно ide (depricated).
    @param ifs: Интерфейс взаимодействия с ide.
    """
    # Инициализация системы журналирования
    from ic.log import log
    from ic.log import default_log_config
    log.init(default_log_config)

    common.img_init()

    # Создаем ядро
    from ic.kernel import ickernel
    ickernel.createEditorKernel()

    nb = icProjectNB(parent)
    prj_edt = parent.prj_edt = PrjTree.PrjTree(nb, ifs)
    res_edt = parent.res_edt = icResourceEditor(nb, -1, {'style_work': 'single', 'res': None, 'size': (300, 100)})
    nb.init_notebook(prj_edt, res_edt, ifs)
    return nb


class ResourseEditorFrame2(wx.Frame):
    """
    Фрейм для редактора проекта.
    """

    def __init__(self, parent, id=-1, title=u'Frame Editor',
                 size=(-1, -1), pos=(-1, -1), style=wx.DEFAULT_FRAME_STYLE):
        """
        Конструктра.
        """
        wx.Frame.__init__(self, parent, -1, title, size, pos, style)
        self._edt = GetProjectEditor(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, evt):
        """
        Обработка закрытия окна.
        """
        self.res_edt.Destroy()
        self.Destroy()


def editor_main(par=0, path=None):
    """
    Функция запуска редактора.
    """
    log.info(u'Запуск редактора проекта <%s>' % path)
    from . import icDesigner
    app = icDesigner.icDesignerApp(par)
    txt = u'Редактор форм'
    # ---------------------------------------------------------------------------
    # Устанавливаем окружение
    # до файлов с документацией
    ic.utils.resource.IC_DOC_PATH = os.getcwd().replace('PropertyEditor', '')+'doc'
    # Путь к файлам ресурсов
    if not path:
        path = 'C:/defis/'

    # ---------------------------------------------------------------------------
    evalSpace = icwidget.icResObjContext()
    frame = ResourseEditorFrame2(None, -1, u'Редактор форм', size=(350, 500),
                                 style=wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN)
    frame.SetIcon(common.icoFormEditor)

    app.SetTopWindow(frame)
    frame.Show()
    frame.SetSize((450, 600))
    frame.SetPosition((200, 50))
    app.MainLoop()


if __name__ == '__main__':
    """
    Тестируем класс icResTree.
    """
    editor_main(0)
