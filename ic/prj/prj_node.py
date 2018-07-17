#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль абстрактных классов узлов дерева проекта.
Базовые классы дерева проекта.
"""

# Подключение библиотек
import wx
import ic.imglib.common as imglib
from ic.utils import ic_res

__version__ = (0, 0, 1, 1)


class PrjNode:
    """
    Узел проекта.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        self._Parent = Parent_
        
        # Имя узла
        self.description = ''
        # Имя узла при добавлении в дерево проекта
        self.name = ''
        
        # Включен ресурс для использования его в проекте или нет
        self.enable = True
        
        # строковая типизация узла дерева проекта
        # она же и ресширение ресурсного файла
        self.typ = ''
        # Всплывающая подсказка
        self.hint = ''
        # Образы
        self.img = None
        self.img_extended = None
        # Прикрепленный к данному узлу дизайнер,
        # наследник класса interfaces.designer.Designer.
        self._designer = None
        # Корень
        self._root = None
        if issubclass(self._Parent.__class__, PrjNode):
            self._root = self._Parent.getRoot()
        # Идентификатор дерева
        self.tree_id = None
        # Признак того что узел не может редактироваться
        self.readonly = False

    def isShowPopupHelp(self):
        """
        Надо показывать всплывающие подсказки о ресурсах, модулях и компонентах?
        """
        root = self.getRoot()
        if root:
            try:
                return root.show_popup_help
            except AttributeError:
                # Скорее всего подсистема
                return root.getParent().getRoot().show_popup_help
        return False

    def getPopupHelpText(self):
        """
        Получить текст всплывающей помощи.
        """
        return None
        
    def onNodeActivated(self, event):
        """
        Активация узла (двойной щелчок мыши на узле).
        """
        self.edit()
        
    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        from . import menuPrjNode
        popup_menu = menuPrjNode.icMenuPrjNode(self)
        popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def getLevel(self, CurLevel_=0):
        """
        Уровень в дереве проекта.
        """
        from . import prj_root
        if not issubclass(self.__class__, prj_root.PrjRoot):
            return self.getParent().getLevel(CurLevel_+1)
        else:
            return CurLevel_

    def Default(self):
        """
        Инициализация узла по умолчанию.
        """
        pass

    def getChildrenCount(self):
        return 0

    def getChildren(self):
        return []

    def design(self):
        """
        Метод запуска дизайнера.
        """
        pass

    def edit(self):
        """
        Метод запуска редактирования в редакторе ресурсов.
        """
        pass
        
    def run(self):
        """
        Метод запуска на тестирование.
        """
        pass

    def rename(self, OldName_, NewName_):
        """
        Метод переименования узла.
        @param OldName_: Старое имя.
        @param NewName_: Новое имя.
        """
        pass

    def create(self):
        """
        Функция создания ресурса.
        """
        return True

    def createResClass(self):
        """
        Функция создания ресурсного класса.
        """
        pass

    def save(self):
        """
        Сохранение ресурса.
        """
        pass

    def load(self, ResFileName_):
        """
        Загрузка ресурса из файла.
        """
        pass

    def extend(self):
        """
        Дополнительные инструменты узла.
        """
        pass

    def getRoot(self):
        return self._root

    def setRoot(self, Root_):
        self._root = Root_

    def getParentRoot(self):
        return self.getRoot()
        
    def getParent(self):
        return self._Parent

    def getPrjTreeCtrl(self):
        return self.getRoot().getParent()

    def readonlyChildren(self, ReadOnly_=True):
        """
        Установить флаг запрета редактирования
        у всех дочерних узлов.
        @param ReadOnly_: Флаг запрета редактирования.
        """
        self.readonly = ReadOnly_

    def cut(self):
        """
        Вырезать узел.
        @return: Возвращает указхатель на удаленный узел.
        """
        # Удалить сначала в дереве узлов
        self._Parent.delChild(self)
        # Затем удалить в контроле дереве проекта
        tree_prj = self.getRoot().getParent()
        # ВНИМАНИЕ! Здесь необходимо производить проверку иначе
        # вываливается в <Segmentation Fault>
        if self.tree_id is not None:
            tree_prj.Delete(self.tree_id)
            self.tree_id = None
        return self
        
    def copy(self):
        """
        Копирвать в клипбоард.
        @return: Возвращает указатель узел.
        """
        new_node = self.__class__(self._Parent)
        new_node.name = self.name+ic_res.getNewID()
        new_node.description = self.description
        return new_node

    def paste(self, Node_):
        """
        Вставить.
        @param Node_: Вставляемый узел.
        """
        if Node_:
            self._Parent.addChild(Node_)
            return True
        return False
        
    def clone(self):
        """
        Клонировать с указанным именем.
        """
        new_node_clone = self.copy()
        ok = self.paste(new_node_clone)
        if ok:
            return new_node_clone
        return None
        
    def delete(self):
        """
        Удалить узел.
        """
        return PrjNode.cut(self)
        
    def getViewer(self, parent):
        """
        Просмотрщик узла.
        """
        return None
      
    def getFullResFileName(self):
        """
        Полное имя файла ресурса.
        """
        return None

    def getMyRes(self):
        """
        Получить ресурс узла.
        """
        return {}

    def getPath(self):
        """
        Путь к ресурсу узла.
        """
        return None


class PrjFolder(PrjNode):
    """
    Папка проекта.
    """
    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjNode.__init__(self, Parent_)
        # Образы
        self.img = imglib.imgFolder
        self.img_extended = None

        self.description = 'new_folder'
        # Имя узла при добавлении в дерево проекта
        self.name = 'new_folder'
        # Классы узлов, которые м.б. включены в текущий узел
        self.include_nodes = []
        self.include_folder = None
        # Дочерние узлы
        self.children = []
        
    def getChildrenCount(self):
        return len(self.children)

    def getChildren(self):
        return self.children
        
    def getChild(self, ChildName_):
        """
        Получить дочерний узел по имени.
        @param ChildName_: Имя дочернего узла.
        @return: Возвращает объект узла или None,
            если узел с таким именем не найден.
        """
        find = [child for child in self.children if child.name == ChildName_]
        if find:
            return find[0]
        return None

    def isChild(self, ChildName_):
        """
        Проверить есть ли дочерний узел с таким именем.
        @param ChildName_: Имя дочернего узла.
        @return: Возвращает True/False.
        """
        return bool(self.getChild(ChildName_))
        
    def addChild(self, Node_):
        """
        Добавить дочерний узел.
        """
        if Node_:
            # Для начала установить у него корень
            Node_.setRoot(self.getRoot())
            # ну и добавить в общий список
            self.children.append(Node_)
        return Node_

    def delChild(self, Node_):
        """
        Удалить дочерний узел.
        """
        if Node_:
            try:
                find = self.children.index(Node_)
            except ValueError:
                find = -1
            if find >= 0:
                del self.children[find]

    def delChildByName(self, NodeName_=None):
        """
        Удалить дочерний узел по его имени.
        @param NodeName_: Имя узла.
        """
        if NodeName_:
            children_names = [child.name for child in self.children]
            try:
                find = children_names.index(NodeName_)
            except ValueError:
                find = -1
            if find >= 0:
                del self.children[find]
                
    def readonlyChildren(self, ReadOnly_=True):
        """
        Установить флаг запрета редактирования
        у всех дочерних узлов.
        @param ReadOnly_: Флаг запрета редактирования.
        """
        PrjNode.readonlyChildren(self, ReadOnly_)
        for child in self.children:
            child.readonlyChildren(ReadOnly_)

    def importChild(self, ResFileName_=None):
        """
        Импортировать ресурс, как дочерний узел.
        @param ResFileName_: Имя импортируемого ресурсного файла.
        """
        pass
