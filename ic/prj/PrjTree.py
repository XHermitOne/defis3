#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль классов панели проекта.
"""

# Подключение библиотек
import wx
from ic.utils import ic_file
from ic.kernel import io_prnt
from ic.components import icwidget
from . import prj_root
from ic.bitmap import ic_bmp

__version__ = (0, 0, 1, 2)

# Константы
hyNodeImgWidth = 16
hyNodeImgHeight = 16

_ = wx.GetTranslation


class ImgList(wx.ImageList):
    """
    Список образов, ориентированный на образы комопнентов.
    """

    def __init__(self, Parent_):
        """
        Конструктор.
        """
        self._Parent = Parent_
        # Вызов консктруктора предка
        self._img_lst = wx.ImageList(hyNodeImgWidth, hyNodeImgHeight)
        # Используемые образы компонентов
        self._NodeImgIdx = {}
        # Используемые образы компонентов
        self._NodeImgExtendedIdx = {}
       
    def getImageList(self):
        return self._img_lst

    def SetNodeImgIdx(self, Node_):
        """
        Установить компонент для редактирования.
        @param Node_: Компонент.
        """
        node_class = Node_.__class__.__name__
        node_name = Node_.name
        # Если тип компонента не зарегистрирован, то зарегистрировать его
        if node_class not in self._NodeImgIdx:
            # Образ типа компонента
            self._NodeImgIdx[node_class] = self.SetNodeImg(Node_.img)
            if Node_.img_extended:
                self._NodeImgExtendedIdx[node_class] = self.SetNodeImg(Node_.img_extended)

    def GetNodeImgIdx(self, Node_):
        """
        Получить данные о компоненте для редактирования.
        @param Node_: Компонент.
        """
        # Если тип компонента не зарегистрирован, то зарегистрировать его
        self.SetNodeImgIdx(Node_)

        node_class = Node_.__class__.__name__
        return self._NodeImgIdx[node_class]

    def GetNodeImgExtendedIdx(self, Node_):
        """
        Получить данные о компоненте для редактирования.
        @param Node_: Компонент.
        """
        # Если тип компонента не зарегистрирован, то зарегистрировать его
        self.SetNodeImgIdx(Node_)

        node_class = Node_.__class__.__name__
        if node_class in self._NodeImgExtendedIdx:
            return self._NodeImgExtendedIdx[node_class]
        return -1

    def SetNodeImg(self, Img_, ImgIdx_=-1):
        """
        Добавить картинку компонента в список образов.
        @param Img_: Имя файла образа компонента или сам образ.
        @param ImgIdx_: Указание на какое место поместить картинку.
        @return: Возвращает индекс соответствующий этому образу.
        """
        # Заменять картинку в списке не надо
        if ImgIdx_ < 0:
            # Добавить в список образ
            if isinstance(Img_, str):
                # Указание файла
                return self._img_lst.Add(ic_bmp.createBitmap(Img_))
            elif issubclass(Img_.__class__, wx.Bitmap):
                # Указание непосредственно картинки
                return self._img_lst.Add(Img_)
        # Надо заменить картинку на ImgIdx_
        else:
            # Заменить в списке образ
            if isinstance(Img_, str):
                # Указание файла
                return self.ReplaceImg(ImgIdx_, ic_bmp.createBitmap(Img_))
            elif issubclass(Img_.__class__, wx.Bitmap):
                # Указание непосредственно картинки
                return self.ReplaceImg(ImgIdx_, Img_)
        return -1

    def ReplaceImg(self, ImgIdx_, Img_):
        """
        Заменить образ в списке образов.
        @param ImgIdx_: Индекс заменяемого образа.
        @param Img_: Сам wx.Bitmap образ.
        @return: Функция возвращает новый индекс образа.
        """
        try:
            self._img_lst.Replace(ImgIdx_, Img_)
        except:
            io_prnt.outErr(u'%s from %s %s ' % (ImgIdx_, self._img_lst.GetImageCount(), Img_))
        return ImgIdx_


class PrjTree(wx.TreeCtrl):
    """
    Визуальное дерево проекта.
    """

    def __init__(self, Parent_, IDE_=None):
        """
        Конструктор.
        @param Parent_: Родитель-панель.
        @param IDE_: Указатель на объект IDE.
        """
        # Окно всплывающих подсказок
        self._helpWin = None
        
        # Интерфейсный объект работы с IDE
        self.ide = IDE_
        # Главное окно IDE
        if IDE_:
            self.ide_frame = IDE_.GetIDEFrame()
        else:
            self.ide_frame = None

        if Parent_ is None:
            Parent_ = self.ide_frame
            
        # ВНИМАНИЕ! стиль редактирования ярлыков дерева под Linux нельзя использовать
        if wx.Platform == '__WXMSW__':
            style = wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS
        else:
            style = wx.TR_DEFAULT_STYLE
        wx.TreeCtrl.__init__(self, Parent_, wx.NewId(), style=style)

        # Установка списка образов компонентов
        self._img_list = ImgList(self)
        self.SetImageList(self._img_list.getImageList())

        # Определение событий
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated, self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndItemLabelEdit)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginItemLabelEdit)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)

        # Флаг разрешения редактирования имен/ярлыков узлов дерева
        self.canEditItemLabel = True
        # Флаг редактирования имени узла дерева
        self.editItemLabel = False

        # Указатель на редактор ресурсов
        self.res_editor = None
        # Корень
        self._Root = None

        self._Prj = prj_root.PrjRoot(self)
        self.setRoot()

    def getIDE(self):
        return self.ide
    
    def getIDEFrame(self):
        return self.ide_frame
    
    def getPrj(self):
        """
        Корневой объект проекта.
        """
        return self._Prj

    def setRoot(self, Prj_=None):
        """
        Функция по ресурсному описанию строит дерево описаниея.
        @param Prj_: Корень дерева проекта.
        """
        try:
            if not Prj_:
                Prj_ = self._Prj
            else:
                self._Prj = Prj_
                self.DeleteAllItems()
            self._Root = self.GetRootItem()

            if Prj_:
                self.AddBranch(self._Root, Prj_)
            # Распахнуть содержание компонента
            if self._Root:
                self.Expand(self._Root)
            return True
        except:
            io_prnt.outErr(u'Build project tree error!')
            return False

    def getRoot(self):
        """
        """
        return self._Root
        
    def expandAllWithoutRoot(self, CurItem_=None, Refresh_=True):
        """
        Раскрыть все ветки дерева (когда корень скрыт).
        @param CurItem_: Текущий узел дерева.
            Если None, то корень.
        @param Refresh_: Флаг обновления дерева.
        """
        if (CurItem_ is None) or (CurItem_ == self.GetRootItem()):
            # Начать с корня
            CurItem_ = self.GetRootItem()
            cur_item = self.GetFirstChild(CurItem_)[0]
            while cur_item:
                self.expandAllWithoutRoot(cur_item, False)
                cur_item = self.GetNextSibling(cur_item)
        else:
            # Отдельная ветка
            if self.ItemHasChildren(CurItem_):
                if not self.IsExpanded(CurItem_):
                    self.Expand(CurItem_)
                cur_item = self.GetFirstChild(CurItem_)[0]
                while cur_item:
                    self.expandAllWithoutRoot(cur_item, False)
                    cur_item = self.GetNextSibling(cur_item)
        if Refresh_:
            self.Refresh()

    def expandAll(self, CurItem_=None, Refresh_=True):
        """
        Раскрыть все ветки дерева.
        @param CurItem_: Текущий узел дерева.
            Если None, то корень.
        @param Refresh_: Флаг обновления дерева.
        """
        if CurItem_ is None:
            # Начать с корня
            CurItem_ = self.GetRootItem()
        # Отдельная ветка
        if self.ItemHasChildren(CurItem_):
            if not self.IsExpanded(CurItem_):
                self.Expand(CurItem_)
            cur_item = self.GetFirstChild(CurItem_)[0]
            while cur_item:
                self.expandAll(cur_item, False)
                cur_item = self.GetNextSibling(cur_item)
        if Refresh_:
            self.Refresh()

    def AddBranch(self, Root_, Node_):
        """
        Добавляет ветку в дерево.
        @param Node_: компонент.
        @return: Возвращает узел дерева.
        """
        # Определить образ компонента
        img_idx = self._img_list.GetNodeImgIdx(Node_)
        img_extended_idx = self._img_list.GetNodeImgExtendedIdx(Node_)

        # Определить текст надписи
        if not isinstance(Node_.name, unicode):
            txt = unicode(str(Node_.name.strip()), 'utf-8')
        else:
            txt = Node_.name.strip()

        # Определить цвет
        txt_color = wx.Colour(0, 0, 0)
        # Установить элемент/узел дерева
        if not self._Root:
            io_prnt.outLog(u'Add root <%s>' % txt)
            self._Root = self.AddRoot(txt)
            Root_ = self._Root
            # Установить картинки у корневого элемента
            self.SetItemImage(Root_, img_idx, wx.TreeItemIcon_Normal)
            if img_extended_idx >= 0:
                self.SetItemImage(Root_, img_extended_idx, wx.TreeItemIcon_Expanded)
            
            self.SetPyData(Root_, Node_)
        else:
            # ВНИМАНИЕ! Когда поставил этот print
            # прекратилась ошибка <Segmentation Fault>
            # io_prnt.outLog(u'Append item %s.<%s>' % (Root_, txt))
            Root_ = self.AppendItem(Root_, txt)
            self.SetItemImage(Root_, img_idx, wx.TreeItemIcon_Normal)
            if img_extended_idx >= 0:
                self.SetItemImage(Root_, img_extended_idx, wx.TreeItemIcon_Expanded)
            # Связать компонент с вновь добавленным узлом
            self.SetPyData(Root_, Node_)
            
        # Установить цвет
        self.SetItemTextColour(Root_, txt_color)
        
        # Прописать идентификатор в дереве.
        Node_.tree_id = Root_

        # Обработка внутренних компонентов
        if Node_.getChildrenCount():
            for cur_node in Node_.getChildren():
                self.AddBranch(Root_, cur_node)

        return Root_

    def AddBranchInSelection(self, Node_):
        """
        Добавляет ветку в дерево в текущий выделенный узел.
        @param Node_: Описание/спецификация компонента.
        @return: Возвращает узел дерева.
        """
        item = self.AddBranch(self.GetSelection(), Node_)
        # Прописать идентификатор в узле
        Node_.tree_id = item
        # Добавить компонент в описание родительского компонента
        root = self.GetItemParent(item)
        if root:
            self.GetPyData(root).addChild(Node_)
        self.Expand(self.GetSelection())
        return item

    def AddBranchInParentSelection(self, Node_):
        """
        Добавляет ветку в дерево в родителя выделенного узел.
        @param Node_: Описание/спецификация компонента.
        @return: Возвращает узел дерева.
        """
        item = self.AddBranch(self.GetItemParent(self.GetSelection()), Node_)
        # Прописать идентификатор в узле
        Node_.tree_id = item
        # Добавить компонент в описание родительского компонента
        root = self.GetItemParent(item)
        if root:
            self.GetPyData(root).addChild(Node_)
        return item

    def getSelectionNode(self):
        """
        Получить текущий выбранный узел дерева.
        """
        item_id = self.GetSelection()
        return self.GetPyData(item_id)

    def delSelectionNode(self):
        """
        Удалить текущий выбранный узел дерева.
        """
        item_id = self.GetSelection()
        return self.Delete(item_id)
        
    def RefreshObj(self, Root_=None, Refresh_=True):
        """
        Обновить изображения дерева объекта.
        @param Root_: Указание корня откуда начинать обновление.
        @param Refresh_: Признак обновления самого объекта-дерева.
        """
        if Root_ is None:
            Root_ = self.GetRootItem()

        node = self.GetPyData(Root_)
        # Сначала обновить рут, а затем все дочерние узлы.
        node_class = node.getClassType().split('.')[-1]
        # Надпись
        self.SetItemText(Root_, node_class+' : '+node.name)
        # Образ
        i_img = self._img_list.GetNodeImgIdx(node)
        self.SetItemImage(Root_, i_img)
        
        if self.ItemHasChildren(Root_):
            child, cookie = self.GetFirstChild(Root_)
            while child.IsOk():
                self.RefreshObj(child, False)
                child, cookie = self.GetNextChild(Root_, cookie)

        # Обновить сам объект
        if Refresh_:
            self.Refresh()

    def RefreshSelection(self):
        """
        Обновить надпись выделенного объекта.
        """
        selection = self.GetSelection()
        if selection:
            node = self.GetPyData(selection)
            # Сначала обновить рут, а затем все дочерние узлы.
            self.SetItemText(selection,
                             node.getClassType()+' : '+node.name)
            # Образ
            i_img = self._img_list.GetNodeImgIdx(node)
            self.SetItemImage(selection, i_img)

    def setResourceEditor(self, ResEditor_=None):
        """
        Запомнить указатель на редактор ресурсов.
        @param ResEditor_: Редактор ресурсов.
        """
        self.res_editor = ResEditor_

    def OnMouseRightClick(self, event):
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
                    node = self.GetPyData(item)
                    if node:
                        node.onNodePopup(event)

    def OnSelectChanged(self, event):
        """
        Изменение выделенного компонента.
        """
        if self._Prj:
            self._Prj.synchroPrj()
            
            # Всплывающие подсказки
            # Если старое окно уже создано и отображается, то удалить его
            if self._helpWin:
                self._helpWin.Show(False)
                self._helpWin.Destroy()
                self._helpWin = None
                
            item = event.GetItem()
            node = self.GetPyData(item)
            if node and node.isShowPopupHelp():
                help_txt = node.getPopupHelpText()
                if help_txt:
                    item_rect = self.GetBoundingRect(item)
                    # Создать и отобразить окно всплывающих подсказок
                    self._helpWin = icwidget.icShortHelpString(self, help_txt,
                                                               (item_rect.right, item_rect.top), 5000)
                    
        event.Skip()
    
    def OnItemActivated(self, event):
        """
        Активация элемента дерева.
        """
        item = event.GetItem()
        node = self.GetPyData(item)
        if node:
            node.onNodeActivated(event)
        event.Skip()

    def OnBeginItemLabelEdit(self, event):
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

    def _checkLegalLabel(self, Label_):
        """
        Проверка допустимости имени узла.
        @param Label_: Имя узла.
        @return: Возвращает True/False.
        """
        if not Label_:
            return False
        # проверить допустимость имени
        for s in list(Label_):
            r = ord(s)
            # Цифры
            # Большие латинские буквы
            # Маленькие латинские буквы
            # Знак подчеркивания
            if not ((r >= 48 and r <= 57) or (r >= 65 and r <= 90) or (r >= 97 and r <= 122) or (r == 95)):
                return False
        return True

    def OnEndItemLabelEdit(self, event):
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
            wx.MessageBox(u'Не корректное наименование',
                          u'Сообщение',
                          wx.OK | wx.ICON_INFORMATION)
            event.Veto()
            return
        # освободить перехваченную мышь
        if self.editItemLabel:
            self.ReleaseMouse()
            # закончить редактирование
            self.editItemLabel=False
            # индеск элемента в структуре PRO
            item = event.GetItem()
            node = self.GetPyData(item)
            node.rename(self.GetItemText(item), label)
            # Обновить дерево проекта
            self.Refresh()

    def OnKeyPressed(self, event):
        """
        Нажатие клавиши.
        """
        # Определить нажатую клавишу
        # key = event.GetKeyCode()
        # if key == wx.WXK_RETURN:
        #     item = self.GetSelection()
        event.Skip()

    def OnMouseLeftDown(self, event):
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

    def OnItemExpanded(self, event):
        """
        Раскрытие узла по +.
        """
        item = event.GetItem()
        node = self.GetPyData(item)
        if node.__class__.__name__ == 'PrjImportSys' and not node.isBuild():
            try:
                # Затем построить дерево подсистемы
                sub_sys_dir = node.getPathInPrj()
                sub_sys_prj = ic_file.GetFilesByExt(sub_sys_dir, '.pro')[0]
                node.buildSubSysTree(sub_sys_prj)
            
                # Удалить все дочерние элементы
                self.DeleteChildren(item)
            
                # Построить ветку узлов дерева подсистемы
                for child in node.getChildren():
                    self.AddBranch(item, child)
            except:
                io_prnt.outErr(u'Open subsystem error')
                wx.MessageBox(u'Open subsystem error',
                              u'ОШИБКА',
                              wx.OK | wx.ICON_ERROR)
        
        event.Skip()
        

class icPrjTreeViewer(PrjTree):
    """
    Класс просмотрщика проекта.
    """

    def __init__(self, Parent_, IDE_=None):
        """
        Конструктор.
        """
        PrjTree.__init__(self, Parent_, IDE_)
        self._item_label = None
        # Пустая панель в родительском сплиттере
        self._none_panel = wx.Panel(Parent_, wx.NewId())
   
    def getNonePanel(self):
        """
        Пустая панель.
        """
        return self._none_panel
        
    def OnMouseRightClick(self, event):
        """
        Обработчик нажатия правой кнопки мыши.
        """
        event.Skip()

    def OnSelectChanged(self, event):
        """
        Изменение выделенного компонента.
        """
        if self._Prj:
            try:
                item = event.GetItem()
                node = self.GetPyData(item)
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
                io_prnt.outErr()
                
        event.Skip()
    
    def OnItemActivated(self, event):
        """
        Активация элемента дерева.
        """
        event.Skip()
        
    def OnBeginItemLabelEdit(self, event):
        """
        Начало редактирования имени узла.
        """
        self._item_label = event.GetLabel()
        event.Skip()
        
    def OnEndItemLabelEdit(self, event):
        """
        Окончание редактирования имени узла.
        """
        if self._item_label:
            item = event.GetItem()
            self.SetItemText(item, self._item_label)
        event.Skip()
      
    def OnKeyPressed(self, event):
        """
        Нажатие клавиши.
        """
        event.Skip()

    def OnMouseLeftDown(self, event):
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
    prj_tree = PrjTree(main_frm)
    prj_tree.setRoot()
    main_frm.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
