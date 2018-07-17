#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса узла управления общей безопасностью проекта.
"""

# --- Подключение библиотек ---
import wx
import os
import os.path
import ic.imglib.common as imglib

import ic.utils.ic_file as ic_file
import ic.utils.ic_res as ic_res
import ic.dlg.ic_dlg as ic_dlg

from ic.kernel import io_prnt

from ic.engine import icUser
from . import prj_node
from . import prj_resource
from . import userRes

import ic

__version__ = (0, 0, 2, 1)

_ = wx.GetTranslation


class PrjSecurity(prj_node.PrjFolder):
    """
    Безопасность.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjFolder.__init__(self, Parent_)

        self.img = imglib.imgKey
        self.description = u'Безопасность'
        self.name = u'Безопасность'
        # Классы узлов, которые м.б. включены в текущий узел
        self.include_nodes = [PrjUserGroup, PrjRole]
        # Менеджер ресурса прав и пользователей
        self.usr_res_manager = userRes.UserResource()
        self.usr_res_manager.setResFileName(self.getUserResFileName())

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        from . import menuUserNode
        popup_menu = menuUserNode.icMenuUserNode(self)
        popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def getUserResFileName(self):
        """
        Генерация имени ресурса.
        """
        prj_file_name = self.getRoot().getPrjFileName()
        if prj_file_name is None:
            prj_name = self.getRoot().prj_res_manager.getPrjRootName()
            return ic_file.AbsolutePath(prj_name,
                                        os.path.dirname(self.getRoot().getPrjFileName()))+'/'+icUser.DEFAULT_USERS_RES_FILE
        else:
            return os.path.split(prj_file_name)[0]+'/'+icUser.DEFAULT_USERS_RES_FILE

    def save(self):
        """
        Созранить ресурс.
        """
        return self.usr_res_manager.save()
        
    def createUser(self, UserName_='new_user'):
        """
        Создать нового пользователя.
        @param UserName_: Имя пользователя.
        @return: Функция возвращает узел созданного пользователя
            или None в случае ошибки.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_editor.CloseResource(bSaveAs=True)
        
        self.usr_res_manager.setResFileName(self.getUserResFileName())

        ok = self.usr_res_manager.createUser(UserName_)
        # Для синхронизации дерева проекта
        self.getRoot().save()
        if ok:
            self.usr_res_manager.save()
            return self._addChildUser(UserName_)
        else:
            return None

    def createRole(self, RoleName_='new_role'):
        """
        Создать новую роль.
        @param RoleName_: Имя роли.
        @return: Функция возвращает узел созданной роли
            или None в случае ошибки.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_editor.CloseResource(bSaveAs=True)
        
        node = self._addChildRole(RoleName_)
        node.create()
 
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return node

    def createUserGroup(self, UserGrpName_='new_user_grp'):
        """
        Создать новой группы пользователей.
        @param UserGrpName_: Имя группы пользователей.
        @return: Функция возвращает узел созданной группы пользователей
            или None в случае ошибки.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_editor.CloseResource(bSaveAs=True)
        
        self.usr_res_manager.setResFileName(self.getUserResFileName())

        ok = self.usr_res_manager.createUserGroup(UserGrpName_)
        # Для синхронизации дерева проекта
        self.getRoot().save()
        if ok:
            self.usr_res_manager.save()
            return self._addChildUserGroup(UserGrpName_)
        else:
            return None
            
    def _addChildUser(self, UserName_):
        """
        Добавление узла пользователя.
        @param UserName_: Имя пользователя.
        @return: Функция возвращает узел созданного пользователя
            или None в случае ошибки.
        """
        try:
            usr = PrjUser(self)
            usr.name = UserName_
            self.addChild(usr)
            return usr
        except:
            io_prnt.outErr(u'Ошибка. Класс PrjSecurity Метод _addChildUser')
            return None
        
    def _addChildRole(self, RoleName_):
        """
        Добавление узла роли.
        @param RoleName_: Имя роли.
        @return: Функция возвращает узел созданной роли
            или None в случае ошибки.
        """
        try:
            role = PrjRole(self)
            role.name = RoleName_
            # Сразу поменять имя в спецификации
            role.template['name'] = role.name
            self.addChild(role)
            # Создать ресурс роли
            return role
        except:
            io_prnt.outErr(u'ERROR. Class: PrjSecurity Method: _addChildRole')
            return None
            
    def _addChildUserGroup(self, UserGrpName_):
        """
        Добавление узла группы пользователей.
        @param UserGrpName_: Имя группы пользователей.
        @return: Функция возвращает узел созданного пользователя
            или None в случае ошибки.
        """
        try:
            usr = PrjUserGroup(self)
            usr.name = UserGrpName_
            self.addChild(usr)
            return usr
        except:
            io_prnt.outErr(u'Ошибка. Класс PrjSecurity Метод _addChildUserGroup')
            return None
        
    def openRoles(self):
        """
        Открытие файлов ролей.
        """
        prj_dir = ic.icGet('PRJ_DIR')
        role_files = ic_file.GetFilesByExt(prj_dir, '.rol')
        # Сразу отфильтровать Pkl файлы
        role_files = [role_file for role_file in role_files if '_pkl.rol' not in role_file.lower()]

        for role_file in role_files:
            role_node_name = os.path.splitext(os.path.basename(role_file))[0]
            self._addChildRole(role_node_name)

    def openUsers(self):
        """
        Открытие файла прав и пользователей.
        """
        usr_res_file_name = self.getUserResFileName()
        self.usr_res_manager.setResFileName(usr_res_file_name)
        self.usr_res_manager.load(usr_res_file_name)
        # Создать пользователей
        user_list = self.usr_res_manager.getUserNameTypeDict().items()
        for user_name, user_type in user_list:
            if user_type == 'User':
                user_res = self.usr_res_manager.getUserRes(user_name)
                if ('group' not in user_res) or (not user_res['group']):
                    self._addChildUser(user_name)
                else:
                    usr_grp_node = self._openBranch(user_res['group'])
                    usr_grp_node._addChildUser(user_name)
            elif user_type == 'UserGroup':
                pass
            else:
                io_prnt.outLog(u'ERROR: Unknown type <%s>' % user_type)

    def _openBranch(self, UserGroupName_):
        """
        Открыть ветку группы пользователей.
        """
        user_res = self.usr_res_manager.getUserRes(UserGroupName_)
        if user_res['group']:
            parent_usr_grp_node = self._openBranch(user_res['group'])
        else:
            parent_usr_grp_node = self
            
        usr_grp_node = parent_usr_grp_node.getChild(UserGroupName_)
        if not usr_grp_node:
            usr_grp_node = parent_usr_grp_node._addChildUserGroup(UserGroupName_)
        return usr_grp_node
        
    def delUser(self, UserName_):
        """
        Удаление пользователя.
        @param UserName_: Имя пользователя.
        @return: Возвращает результат выполнения операции True/False.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_editor.CloseResource(bSaveAs=True)

        ok = self.usr_res_manager.delUser(UserName_)
        if ok:
            self._delChildUser(UserName_)
            self.usr_res_manager.save()
        return ok
        
    def _delChildUser(self, UserName_):
        """
        Удалить дочерний узел пользователя.
        @param UserName_: Имя пользователя.
        """
        for i_child in range(len(self.children)):
            child = self.children[i_child]
            if child.name == UserName_:
                del self.children[i_child]
                return


class PrjUserPrototype(prj_node.PrjNode):
    """
    Пользователь.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjNode.__init__(self, Parent_)
        self.img = imglib.imgUser
        self.description = u'Пользователь'
        self.name = 'admin'
        self.typ = 'acc'
        # Менеджер управления ресурсао прав и пользователей
        self.usr_res_manager = Parent_.usr_res_manager

    def design(self):
        """
        Запуск дизайнера.
        """
        pass

    def onNodeActivated(self, event):
        """
        Активация узла (двойной щелчок мыши на узле).
        """
        self.createRes()
        self.edit()

    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        from . import menuUserNode
        popup_menu = menuUserNode.icMenuUserNode(self)
        popup_menu.Popup(wx.GetMousePosition(), self._root.getParent())

    def getResName(self):
        """
        Имя текущего пользователя.
        """
        return self.name

    def getResPath(self):
        """
        Генерация пути ресурса.
        """
        prj_file_name = self.getRoot().getPrjFileName()
        if prj_file_name is None:
            prj_name = self.getRoot().prj_res_manager.getPrjRootName()
            return ic_file.AbsolutePath(prj_name,
                                        os.path.dirname(self.getRoot().getPrjFileName()))
        else:
            return os.path.split(prj_file_name)[0]
        
    def getResFileName(self):
        """
        Генерация имени файла ресурса.
        """
        return 'users'
    
    def getResFileExt(self):
        """
        Генерация расширения файла ресурса.
        """
        return self.typ
       
    def edit(self):
        """
        Запуск ресурса на редактирование.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_name = self.getResName()
            res_path = self.getResPath()
            res_file = self.getResFileName()
            res_ext = self.getResFileExt()

            self.getRoot().unlockResInResEditor(res_editor)
            if not self.readonly:
                is_lock = ic_res.isLockRes(res_name, res_file, res_ext,
                                           self.getRoot().lock_dir)
                if not is_lock:
                    # Если ресурс не заблокирован, то заблокировать его
                    # и отдать на редактирование
                    ic_res.lockRes(res_name, res_file, res_ext,
                                   self.getRoot().lock_dir)
                    return res_editor.SetResource(res_name,
                                                  res_path, res_file, res_ext,
                                                  bEnable=True)
                else:
                    lock_rec = ic_res.getLockResRecord(res_name, res_file,
                                                       res_ext, self.getRoot().lock_dir)
                    ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                    u'msgid "Resource %s is locked by user %s. Computer: %s."' % (res_name,
                                                                                                  lock_rec['user'],
                                                                                                  lock_rec['computer']))
                    return None
            else:
                return res_editor.SetResource(res_name,
                                              res_path, res_file, res_ext,
                                              bEnable=False)
        
        return None

    def createRes(self):
        """
        Создать файл ресурсов прав и пользователей.
        """
        res_path = self.getResPath()
        res_name = self.getResFileName()
        res_ext = self.getResFileExt()
        res_file_name = '%s/%s.%s' % (res_path, res_name, res_ext)
        self.usr_res_manager.createRes(res_file_name)
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return True
            
    def rename(self, OldName_, NewName_):
        """
        Переименование пользователя.
        @param OldName_: Старое имя.
        @param NewName_: Новое имя.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            old_res_name = self.getResName()
            old_res_file = self.getResPath()+'/'+self.getResFileName()+'.'+self.getResFileExt()
            self.name = NewName_
            new_res_name = self.getResName()
            new_res_file = self.getResPath()+'/'+self.getResFileName()+'.'+self.getResFileExt()
            # Если открыт в редакторе ресурсов, то поменять и в нем
            res_editor.CloseResource(bSaveAs=False, bCloseGrpEdt=False)
            
            # Переименовать в ресурсе
            self.usr_res_manager.renameUser(old_res_name, new_res_name)
            self.usr_res_manager.save()
                
            # Для синхронизации дерева проекта
            self.getRoot().save()
            # И запустить на редактирование
            self.edit()
            return True
                
        return False

    def getPopupHelpText(self):
        """
        Получить текст всплывающей помощи.
        """
        if self.usr_res_manager:
            res = self.usr_res_manager.getUserRes(self.name)
            if res:
                description = res.get('description', u'')
                return description
        return u''


class PrjUser(PrjUserPrototype):
    """
    Пользователь.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjUserPrototype.__init__(self, Parent_)
        self.img = imglib.imgUser
        self.description = u'Пользователь'
        self.name = 'admin'
        self.typ = 'acc'


class PrjUserGroup(prj_node.PrjFolder, PrjUserPrototype):
    """
    Группа пользователей.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjUserPrototype.__init__(self, Parent_)
        prj_node.PrjFolder.__init__(self, Parent_)
        
        self.img = imglib.imgUsers
        self.description = u'Группа пользователей'
        self.name = 'user_group'
        self.typ = 'acc'
        # Классы узлов, которые м.б. включены в текущий узел
        self.include_nodes = [PrjUser]

    def createUser(self, UserName_='new_user'):
        """
        Создать нового пользователя.
        @param UserName_: Имя пользователя.
        @return: Функция возвращает узел созданного пользователя
            или None в случае ошибки.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_editor.CloseResource(bSaveAs=True)
        
        security = self.getParent()
        security.usr_res_manager.setResFileName(security.getUserResFileName())

        ok = security.usr_res_manager.createUser(UserName_)
        
        # Прописать группу в пользователе
        usr_res = security.usr_res_manager.getRes()[UserName_]
        usr_res['group'] = self.name

        # Для синхронизации дерева проекта
        self.getRoot().save()
        if ok:
            security.usr_res_manager.save()
            return self._addChildUser(UserName_)
        else:
            return None

    def _addChildUser(self, UserName_):
        """
        Добавление узла пользователя.
        @param UserName_: Имя пользователя.
        @return: Функция возвращает узел созданного пользователя
            или None в случае ошибки.
        """
        try:
            usr = PrjUser(self)
            usr.name = UserName_
            self.addChild(usr)
            return usr
        except:
            io_prnt.outErr(u'ОШИБКА. Класс PrjUserGroup Функция _addChildUser')
            return None

    def createUserGroup(self, UserGrpName_='new_user_grp'):
        """
        Создать новой группы пользователей.
        @param UserGrpName_: Имя группы пользователей.
        @return: Функция возвращает узел созданной группы пользователей
            или None в случае ошибки.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_editor.CloseResource(bSaveAs=True)
        
        security = self.getParent()
        security.usr_res_manager.setResFileName(self.getUserResFileName())

        ok = security.usr_res_manager.createUserGroup(UserGrpName_)
        
        # Прописать группу в группе
        usr_grp_res = security.usr_res_manager.getUserRes(UserGrpName_)
        usr_res['group'] = self.name

        # Для синхронизации дерева проекта
        self.getRoot().save()
        if ok:
            security.usr_res_manager.save()
            return self._addChildUserGroup(UserGrpName_)
        else:
            return None
            
    def _addChildUserGroup(self, UserGrpName_):
        """
        Добавление узла группы пользователей.
        @param UserGrpName_: Имя группы пользователей.
        @return: Функция возвращает узел созданного пользователя
            или None в случае ошибки.
        """
        try:
            usr = PrjUserGroup(self)
            usr.name = UserGrpName_
            self.addChild(usr)
            return usr
        except:
            io_prnt.outErr(u'ОШИБКА. Класс PrjUserGroup Функция _addChildUserGroup')
            return None


from ic.components.user import ic_role_wrp


class PrjRole(prj_resource.PrjResource):
    """
    Роль.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_resource.PrjResource.__init__(self, Parent_)
        self.description = u'Роль'
        self.name = 'new_role'
        self.img = imglib.imgRole
        self.typ = 'rol'
        # Шаблон для заполнения по умолчанию
        self.template = ic_role_wrp.ic_class_spc
        self.template['name'] = self.name
