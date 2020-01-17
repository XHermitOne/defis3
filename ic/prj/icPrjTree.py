#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль классов панели проекта.
"""

# Подключение библиотек
import wx

from ic.utils import filefunc
from ic.components import icwidget
from . import prj_root
from ic.bitmap import bmpfunc
from ic.log import log
from ic.dlg import dlgfunc
from ic.editor import ext_python_editor
from ic.PropertyEditor import icDefInf

from . import ImpNode

__version__ = (0, 1, 1, 1)

# Константы
hyNodeImgWidth = 16
hyNodeImgHeight = 16

_ = wx.GetTranslation


class icPrjTreeImgList(wx.ImageList):
    """
    Список образов, ориентированный на образы комопнентов.
    """

    def __init__(self, parent):
        """
        Конструктор.
        """
        self._Parent = parent
        # Вызов консктруктора предка
        self._img_lst = wx.ImageList(hyNodeImgWidth, hyNodeImgHeight)
        # Используемые образы компонентов
        self._NodeImgIdx = {}
        # Используемые образы компонентов
        self._NodeImgExtendedIdx = {}
       
    def getImageList(self):
        return self._img_lst

    def setNodeImgIdx(self, node):
        """
        Установить компонент для редактирования.

        :param node: Компонент.
        """
        node_class = node.__class__.__name__
        node_name = node.name
        # Если тип компонента не зарегистрирован, то зарегистрировать его
        if node_class not in self._NodeImgIdx:
            # Образ типа компонента
            self._NodeImgIdx[node_class] = self.setNodeImg(node.img)
            if node.img_extended:
                self._NodeImgExtendedIdx[node_class] = self.setNodeImg(node.img_extended)

    def getNodeImgIdx(self, node):
        """
        Получить данные о компоненте для редактирования.

        :param node: Компонент.
        """
        # Если тип компонента не зарегистрирован, то зарегистрировать его
        self.setNodeImgIdx(node)

        node_class = node.__class__.__name__
        return self._NodeImgIdx[node_class]

    def getNodeImgExtendedIdx(self, node):
        """
        Получить данные о компоненте для редактирования.

        :param node: Компонент.
        """
        # Если тип компонента не зарегистрирован, то зарегистрировать его
        self.setNodeImgIdx(node)

        node_class = node.__class__.__name__
        if node_class in self._NodeImgExtendedIdx:
            return self._NodeImgExtendedIdx[node_class]
        return -1

    def setNodeImg(self, img, img_idx=-1):
        """
        Добавить картинку компонента в список образов.

        :param img: Имя файла образа компонента или сам образ.
        :param img_idx: Указание на какое место поместить картинку.
        :return: Возвращает индекс соответствующий этому образу.
        """
        # Заменять картинку в списке не надо
        if img_idx < 0:
            # Добавить в список образ
            if isinstance(img, str):
                # Указание файла
                return self._img_lst.Add(bmpfunc.createBitmap(img))
            elif issubclass(img.__class__, wx.Bitmap):
                # Указание непосредственно картинки
                return self._img_lst.Add(img)
        # Надо заменить картинку на img_idx
        else:
            # Заменить в списке образ
            if isinstance(img, str):
                # Указание файла
                return self.replaceImg(img_idx, bmpfunc.createBitmap(img))
            elif issubclass(img.__class__, wx.Bitmap):
                # Указание непосредственно картинки
                return self.replaceImg(img_idx, img)
        return -1

    def replaceImg(self, img_idx, img):
        """
        Заменить образ в списке образов.

        :param img_idx: Индекс заменяемого образа.
        :param img: Сам wx.Bitmap образ.
        :return: Функция возвращает новый индекс образа.
        """
        try:
            self._img_lst.Replace(img_idx, img)
        except:
            log.fatal(u'%s from %s %s ' % (img_idx, self._img_lst.GetImageCount(), img))
        return img_idx


class icPrjTree(wx.TreeCtrl):
    """
    Визуальное дерево проекта.
    """

    def __init__(self, parent, ide=None):
        """
        Конструктор.

        :param parent: Родитель-панель.
        :param ide: Указатель на объект IDE.
        """
        # Окно всплывающих подсказок
        self._helpWin = None
        
        # Интерфейсный объект работы с IDE
        self.ide = ide
        # Главное окно IDE
        if ide:
            self.ide_frame = ide.getIDEFrame()
        else:
            self.ide_frame = None

        if parent is None:
            parent = self.ide_frame
            
        # ВНИМАНИЕ! стиль редактирования ярлыков дерева под Linux нельзя использовать
        if wx.Platform == '__WXMSW__':
            style = wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS
        else:
            style = wx.TR_DEFAULT_STYLE
        wx.TreeCtrl.__init__(self, parent, wx.NewId(), style=style)

        # Установка списка образов компонентов
        self._img_list = icPrjTreeImgList(self)
        self.SetImageList(self._img_list.getImageList())

        # Определение событий
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onItemActivated, self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onMouseRightClick)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPressed)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.onEndItemLabelEdit)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.onBeginItemLabelEdit)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onItemExpanded)

        # Флаг разрешения редактирования имен/ярлыков узлов дерева
        self.canEditItemLabel = True
        # Флаг редактирования имени узла дерева
        self.editItemLabel = False

        # Указатель на редактор ресурсов
        self.res_editor = None
        # Корень
        self._Root = None

        self._Prj = prj_root.icPrjRoot(self)
        self.setRoot()

    def getIDE(self):
        if self.ide is None:
            log.warning(u'Не определен IDE для редактрования модулей проекта')
            log.warning(u'Используется внешний редактор модулей Python')
            self.ide = ext_python_editor.icExtPythonEditor()
        return self.ide

    def getIDEFrame(self):
        return self.ide_frame
    
    def getPrj(self):
        """
        Корневой объект проекта.
        """
        return self._Prj

    def setRoot(self, prj=None):
        """
        Функция по ресурсному описанию строит дерево описания.

        :param prj: Корень дерева проекта.
        """
        try:
            if not prj:
                prj = self._Prj
            else:
                self._Prj = prj
                self.DeleteAllItems()
            self._Root = self.GetRootItem()

            if prj:
                self.addBranch(self._Root, prj)
                # log.debug(u'Дерево проекта построено')
            # Распахнуть содержание компонента
            # log.debug(u'Открытие дерева проекта...')
            if self._Root:
                self.Expand(self._Root)
            # log.debug(u'Открытие дерева проекта...ok')
            return True
        except:
            log.fatal(u'Ошибка построения дерева проекта')
        return False

    def getRoot(self):
        """
        """
        return self._Root
        
    def expandAllWithoutRoot(self, cur_item=None, bRefresh=True):
        """
        Раскрыть все ветки дерева (когда корень скрыт).

        :param cur_item: Текущий узел дерева.
            Если None, то корень.
        :param bRefresh: Флаг обновления дерева.
        """
        if (cur_item is None) or (cur_item == self.GetRootItem()):
            # Начать с корня
            cur_item = self.GetRootItem()
            item = self.GetFirstChild(cur_item)[0]
            while item:
                self.expandAllWithoutRoot(item, False)
                item = self.GetNextSibling(item)
        else:
            # Отдельная ветка
            if self.ItemHasChildren(cur_item):
                if not self.IsExpanded(cur_item):
                    self.Expand(cur_item)
                item = self.GetFirstChild(cur_item)[0]
                while item:
                    self.expandAllWithoutRoot(item, False)
                    item = self.GetNextSibling(item)
        if bRefresh:
            self.Refresh()

    def expandAll(self, cur_item=None, bRefresh=True):
        """
        Раскрыть все ветки дерева.

        :param cur_item: Текущий узел дерева.
            Если None, то корень.
        :param bRefresh: Флаг обновления дерева.
        """
        if cur_item is None:
            # Начать с корня
            cur_item = self.GetRootItem()
        # Отдельная ветка
        if self.ItemHasChildren(cur_item):
            if not self.IsExpanded(cur_item):
                self.Expand(cur_item)
            item = self.GetFirstChild(cur_item)[0]
            while item:
                self.expandAll(item, False)
                item = self.GetNextSibling(item)
        if bRefresh:
            self.Refresh()

    def addBranch(self, root, node):
        """
        Добавляет ветку в дерево.

        :param node: компонент.
        :return: Возвращает узел дерева.
        """
        # Определить образ компонента
        img_idx = self._img_list.getNodeImgIdx(node)
        img_extended_idx = self._img_list.getNodeImgExtendedIdx(node)

        # Определить текст надписи
        if not isinstance(node.name, str):
            txt = str(node.name.strip())
        else:
            txt = node.name.strip()

        # Определить цвет
        txt_color = wx.Colour(*icDefInf.getActivateColour())
        # Установить элемент/узел дерева
        if not self._Root:
            log.info(u'Добавление корневого элемента дерева проекта <%s>' % txt)
            self._Root = self.AddRoot(txt)
            root = self._Root
            # Установить картинки у корневого элемента
            self.SetItemImage(root, img_idx, wx.TreeItemIcon_Normal)
            if img_extended_idx >= 0:
                self.SetItemImage(root, img_extended_idx, wx.TreeItemIcon_Expanded)
            
            self.SetItemData(root, node)
        else:
            # ВНИМАНИЕ! Когда поставил этот print
            # прекратилась ошибка <Segmentation Fault>
            log.debug(u'Добавление элемента <%s : %s>' % (root.IsOk(), txt))
            root = self.AppendItem(root, txt)
            self.SetItemImage(root, img_idx, wx.TreeItemIcon_Normal)
            if img_extended_idx >= 0:
                self.SetItemImage(root, img_extended_idx, wx.TreeItemIcon_Expanded)
            # Связать компонент с вновь добавленным узлом
            self.SetItemData(root, node)
            
        # Установить цвет
        self.SetItemTextColour(root, txt_color)
        
        # Прописать идентификатор в дереве.
        node.tree_id = root

        # Обработка внутренних компонентов
        if node.getChildrenCount():
            for cur_node in node.getChildren():
                self.addBranch(root, cur_node)

        return root

    def addBranchInSelection(self, node):
        """
        Добавляет ветку в дерево в текущий выделенный узел.

        :param node: Описание/спецификация компонента.
        :return: Возвращает узел дерева.
        """
        item = self.addBranch(self.GetSelection(), node)
        # Прописать идентификатор в узле
        node.tree_id = item
        # Добавить компонент в описание родительского компонента
        root = self.GetItemParent(item)
        if root:
            self.GetItemData(root).addChild(node)
        self.Expand(self.GetSelection())
        return item

    def addBranchInParentSelection(self, node):
        """
        Добавляет ветку в дерево в родителя выделенного узел.

        :param node: Описание/спецификация компонента.
        :return: Возвращает узел дерева.
        """
        item = self.addBranch(self.GetItemParent(self.GetSelection()), node)
        # Прописать идентификатор в узле
        node.tree_id = item
        # Добавить компонент в описание родительского компонента
        root = self.GetItemParent(item)
        if root:
            self.GetItemData(root).addChild(node)
        return item

    def getSelectionNode(self):
        """
        Получить текущий выбранный узел дерева.
        """
        item_id = self.GetSelection()
        return self.GetItemData(item_id)

    def delSelectionNode(self):
        """
        Удалить текущий выбранный узел дерева.
        """
        item_id = self.GetSelection()
        return self.Delete(item_id)
        
    def refreshObj(self, root=None, bRefresh=True):
        """
        Обновить изображения дерева объекта.

        :param root: Указание корня откуда начинать обновление.
        :param bRefresh: Признак обновления самого объекта-дерева.
        """
        if root is None:
            root = self.GetRootItem()

        node = self.GetItemData(root)
        # Сначала обновить рут, а затем все дочерние узлы.
        node_class = node.getClassType().split('.')[-1]
        # Надпись
        self.SetItemText(root, node_class + ' : ' + node.name)
        # Образ
        i_img = self._img_list.getNodeImgIdx(node)
        self.SetItemImage(root, i_img)
        
        if self.ItemHasChildren(root):
            child, cookie = self.GetFirstChild(root)
            while child.IsOk():
                self.refreshObj(child, False)
                child, cookie = self.GetNextChild(root, cookie)

        # Обновить сам объект
        if bRefresh:
            self.Refresh()

    def refreshSelection(self):
        """
        Обновить надпись выделенного объекта.
        """
        selection = self.GetSelection()
        if selection:
            node = self.GetItemData(selection)
            # Сначала обновить рут, а затем все дочерние узлы.
            self.SetItemText(selection,
                             node.getClassType()+' : '+node.name)
            # Образ
            i_img = self._img_list.getNodeImgIdx(node)
            self.SetItemImage(selection, i_img)

    def setResourceEditor(self, res_editor=None):
        """
        Запомнить указатель на редактор ресурсов.

        :param res_editor: Редактор ресурсов.
        """
        self.res_editor = res_editor

    def onMouseRightClick(self, event):
        """
        Обработчик нажатия правой кнопки мыши.
        """
        item = self.GetSelection()
        if self.editItemLabel:
            # закончить редактирование
            self.editItemLabel = False
            self.EndEditLabel(item, True)
            # освободить перехваченную мышь
            self.ReleaseMouse()
        else:
            # определить элемент дерева
            hit_item = self.HitTest(event.GetPosition())
            # отобразить меню
            if hit_item[1] & wx.TREE_HITTEST_ONITEMLABEL:
                if self.GetSelection() == hit_item[0]:
                    node = self.GetItemData(item)
                    if node:
                        node.onNodePopup(event)

    def onSelectChanged(self, event):
        """
        Изменение выделенного компонента.
        """
        if self._Prj:
            self._Prj.synchroPrj()
            log.debug(u'Синхронизация проекта по выделеннию компонента')
            
            # Всплывающие подсказки
            # Если старое окно уже создано и отображается, то удалить его
            if self._helpWin:
                log.debug(u'Закрытие окна помощи')
                self._helpWin.Show(False)
                self._helpWin.Destroy()
                self._helpWin = None
                
            item = event.GetItem()
            log.debug(u'Определен элемент дерева')
            node = self.GetItemData(item)
            log.debug(u'Получены данные узла')
            if node and node.isShowPopupHelp():
                log.debug(u'Смена окна всплывающих подсказок')
                help_txt = node.getPopupHelpText()
                if help_txt:
                    item_rect = self.GetBoundingRect(item)
                    # Создать и отобразить окно всплывающих подсказок
                    self._helpWin = icwidget.icShortHelpString(self, help_txt,
                                                               (item_rect.right, item_rect.top), 5000)

        log.debug(u'Синхронизация проекта по выделеннию компонента...ok')
        event.Skip()
    
    def onItemActivated(self, event):
        """
        Активация элемента дерева.
        """
        item = event.GetItem()
        node = self.GetItemData(item)
        if node:
            node.onNodeActivated(event)
        event.Skip()

    def onBeginItemLabelEdit(self, event):
        """
        Начало редактирования имени узла.
        """
        if not self.canEditItemLabel:
            # Вот эта сволочь не работает, не запрещает редактирование.
            # Как с ней бороться я пока не знаю
            event.Veto()
        else:
            # перехват событий с мыши
            self.CaptureMouse()
            # сбросить флаг разрешения редактирования
            self.editItemLabel = True

    def _checkLegalLabel(self, label):
        """
        Проверка допустимости имени узла.

        :param label: Имя узла.
        :return: Возвращает True/False.
        """
        if not label:
            return False
        # проверить допустимость имени
        for s in list(label):
            r = ord(s)
            # Цифры
            # Большие латинские буквы
            # Маленькие латинские буквы
            # Знак подчеркивания
            if not ((48 <= r <= 57) or (65 <= r <= 90) or (97 <= r <= 122) or (r == 95)):
                return False
        return True

    def onEndItemLabelEdit(self, event):
        """
        Окончание редактирования имени узла.
        """
        if not self.editItemLabel:
            return

        label = event.GetLabel()
        # проверить допустимость имени
        legal_label = self._checkLegalLabel(label)
        # имя или пустое или в нем присутствуют запрещенные символы
        if not legal_label:
            # закончить редактирование
            self.editItemLabel = False
            # освободить перехваченную мышь
            self.ReleaseMouse()
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!', u'Не корректное наименование',
                                   parent=self)
            event.Veto()
            return
        # освободить перехваченную мышь
        if self.editItemLabel:
            self.ReleaseMouse()
            # закончить редактирование
            self.editItemLabel=False
            # индеск элемента в структуре PRO
            item = event.GetItem()
            node = self.GetItemData(item)
            node.rename(self.GetItemText(item), label)
            # Обновить дерево проекта
            self.Refresh()

    def onKeyPressed(self, event):
        """
        Нажатие клавиши.
        """
        # Определить нажатую клавишу
        # key = event.GetKeyCode()
        # if key == wx.WXK_RETURN:
        #     item = self.GetSelection()
        event.Skip()

    def onMouseLeftDown(self, event):
        """
        Левая кнопка мыши.
        """
        if self.editItemLabel:
            # закончить редактирование
            self.editItemLabel = False
            # item = self.GetSelection()
            # освободить перехваченную мышь
            self.ReleaseMouse()
        else:
            event.Skip()

    def onItemExpanded(self, event):
        """
        Раскрытие узла по +.
        """
        item = event.GetItem()
        node = self.GetItemData(item)
        if isinstance(node, ImpNode.icPrjImportSys) and not node.isBuild():
            try:
                # Затем построить дерево подсистемы
                sub_sys_dir = node.getPathInPrj()
                sub_sys_prj = filefunc.getFilenamesByExt(sub_sys_dir, '.pro')[0]
                node.buildSubSysTree(sub_sys_prj)
            
                # Удалить все дочерние элементы
                self.DeleteChildren(item)
            
                # Построить ветку узлов дерева подсистемы
                for child in node.getChildren():
                    self.addBranch(item, child)
            except:
                log.fatal(u'Ошибка открытия подсистемы')
                dlgfunc.openErrBox(u'ОШИБКА', u'Ошибка открытия подсистемы',
                                   parent=self)
        
        event.Skip()
        

class icPrjTreeViewer(icPrjTree):
    """
    Класс просмотрщика проекта.
    """
    def __init__(self, parent, ide=None):
        """
        Конструктор.
        """
        icPrjTree.__init__(self, parent, ide)
        self._item_label = None
        # Пустая панель в родительском сплиттере
        self._none_panel = wx.Panel(parent, wx.NewId())
   
    def getNonePanel(self):
        """
        Пустая панель.
        """
        return self._none_panel
        
    def onMouseRightClick(self, event):
        """
        Обработчик нажатия правой кнопки мыши.
        """
        event.Skip()

    def onSelectChanged(self, event):
        """
        Изменение выделенного компонента.
        """
        if self._Prj:
            try:
                item = event.GetItem()
                node = self.GetItemData(item)
                splitter = self.GetParent()
                viewer = node.getViewer(splitter)
                # Подменить окно
                if viewer:
                    panel = splitter.GetWindow2()
                    panel.Show(False)
                    splitter.ReplaceWindow(panel, viewer)
                else:
                    panel = self.getNonePanel()
                    panel.Show(True)
                    tree = splitter.GetWindow2()
                    tree.Show(False)
                    splitter.ReplaceWindow(tree, panel)

                try:
                    self.GetParent().GetParent().setPassportLabel()
                except:
                    self.GetParent().GetParent().setPassportLabel('')
            except:
                log.fatal()
                
        event.Skip()
    
    def onItemActivated(self, event):
        """
        Активация элемента дерева.
        """
        event.Skip()
        
    def onBeginItemLabelEdit(self, event):
        """
        Начало редактирования имени узла.
        """
        self._item_label = event.GetLabel()
        event.Skip()
        
    def onEndItemLabelEdit(self, event):
        """
        Окончание редактирования имени узла.
        """
        if self._item_label:
            item = event.GetItem()
            self.SetItemText(item, self._item_label)
        event.Skip()
      
    def onKeyPressed(self, event):
        """
        Нажатие клавиши.
        """
        event.Skip()

    def onMouseLeftDown(self, event):
        """
        Левая кнопка мыши.
        """
        event.Skip()


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp(0)
    main_frm = wx.Frame(None, wx.NewId())
    prj_tree = icPrjTree(main_frm)
    prj_tree.setRoot()
    main_frm.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
