#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Модуль классов узлов ресурсов проекта.
"""

# Подключение библиотек
import wx
import copy
import os
import os.path

import ic.imglib.common as imglib
import ic.utils.ic_file as ic_file
import ic.utils.ic_res as ic_res
import ic.utils.util as util
import ic.dlg.ic_dlg as ic_dlg
from ic.kernel import io_prnt

# Необходимо для определений спецификаций
import ic.components.user.ic_tab_wrp as ic_tab
import ic.components.user.ic_mainwin_wrp as ic_mainwin
import ic.components.user.ic_auimainwin_wrp as ic_auimainwin
import ic.components.user.ic_sqlite_wrp as ic_sqlite
import ic.components.user.ic_postgres_wrp as ic_postgres
import ic.components.user.ic_mysql_wrp as ic_mysql
import ic.components.user.ic_mssql_wrp as ic_mssql
import ic.components.user.ic_odbc_wrp as ic_odbc
from ic.components.user import ic_sqlalchemy_scheme_wrp
import ic.components.user.ic_obj_storage_src_wrp as ic_obj_storage_src
import ic.components.user.ic_obj_storage_wrp as ic_obj_storage
import ic.components.user.ic_menubar_wrp as ic_menubar_wrp
import ic.components.user.ic_flatmenubar_wrp as ic_flatmenubar_wrp
from ic.components.user import ic_flatmenu_wrp
import ic.components.user.ic_mth_wrp as ic_mth

from . import prj_node
from . import menuPrjNode
from . import menuImpNode

__version__ = (0, 0, 2, 2)

_ = wx.GetTranslation


class PrjResources(prj_node.PrjFolder):
    """
    Ресурсы.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjFolder.__init__(self, Parent_)
        self.img_extended = imglib.imgFolderOpen
        self.description = u'Ресурсы'
        self.name = u'Ресурсы'
        # Классы узлов, которые м.б. включены в текущий узел
        self.include_nodes = [PrjTabRes, PrjDBRes,
                              PrjObjStorageRes,
                              PrjFrmRes, PrjWinRes,
                              PrjMenuRes, PrjTemplate, PrjMethod, PrjMetaDataRes]
        self.include_folder = PrjResources
        
    def isMainFolder(self):
        """
        Проверка является ли эта папка главной.
        """
        return self.getParent() == self.getRoot()
        
    def create(self):
        """
        Создать папку.
        """
        # Прописать в родительской папке
        self.getParent().addChild(self)
        # Добавить в проект
        if not self.getParent().isMainFolder():
            ok = self.getRoot().prj_res_manager.addFolder(self.name, self.getParent().name)
        else:
            ok = self.getRoot().prj_res_manager.addFolder(self.name, self.getRoot().name)
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return ok
       
    def delete(self):
        """
        Удаление папки.
        """
        # Главную папку удалить нельзя
        if self.isMainFolder():
            return False
        # Удалить из проекта
        self.getRoot().prj_res_manager.delFolder(self.name)
        # Удалить из дерева
        return prj_node.PrjNode.delete(self)

    def rename(self, OldName_, NewName_):
        """
        Переименование папки.
        @param OldName_: Старое имя папки.
        @param NewName_: Новое имя папки.
        """
        # Переименовать в проекте
        self.getRoot().prj_res_manager.renameRes(OldName_, NewName_)
        self.name = NewName_
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return True

    def importChild(self, ResFileName_=None):
        """
        Импортировать ресурс, как дочерний узел.
        @param ResFileName_: Имя импортируемого ресурсного файла.
        @return: Возвращает вновь созданный узел или None.
        """
        new_node = None
        if os.path.exists(ResFileName_):
            # Сделать новое имя файла
            new_res_file_name = ic_file.AbsolutePath('./%s/%s' % (self.getRoot().name,
                                                     os.path.basename(ResFileName_)))
            # Если новый файл существут, то спросить о его перезаписи
            if not ic_file.SamePathWin(ResFileName_, new_res_file_name):
                # Скопировать файл
                ic_file.icCopyFile(ResFileName_, new_res_file_name, True)
            # Создать узел
            res_file_name_split = os.path.splitext(new_res_file_name)
            typ = res_file_name_split[1][1:]
            node_name = os.path.basename(res_file_name_split[0])
            new_node = self.getRoot().buildPrjRes(self, typ, node_name)
            # Добавить ресурс в ресурс проекта
            self.getRoot().prj_res_manager.addRes(node_name, typ, self.name)
            # Для синхронизации дерева проекта
            self.getRoot().save()
        return new_node


class PrjResource(prj_node.PrjNode):
    """
    Ресурс.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        prj_node.PrjNode.__init__(self, Parent_)
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = ''
        # Шаблон для заполнения по умолчанию
        self.template = None

    def getResPath(self):
        """
        Генерация пути ресурса.
        """
        prj_file_name = self.getRoot().getPrjFileName()
        if prj_file_name is None:
            prj_name = self.getRoot().prj_res_manager.getPrjRootName().strip()
            return ic_file.icAbsolutePath(prj_name,
                                          os.path.dirname(self.getRoot().getPrjFileName()))
        else:
            return ic_file.Split(prj_file_name)[0].strip()

    def getPath(self):
        """
        Путь к ресурсу узла.
        """
        return self.getResPath()
    
    def getResFileName(self):
        """
        Генерация имени файла ресурса.
        """
        return self.name.strip()

    def getResFileExt(self):
        """
        Генерация расширения файла ресурса.
        """
        return self.typ.strip()
        
    def getFullResFileName(self):
        """
        Полное имя файла ресурса.
        """
        return ic_file.NormPathUnix(self.getResPath()+'/'+self.getResFileName()+'.'+self.getResFileExt())
        
    def getResName(self):
        """
        Имя ресурса.
        """
        return self.name.strip()
        
    def create(self):
        """
        Функция создания ресурса.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_name = self.getResName()
            res_path = self.getResPath()
            ic_file.MakeDirs(res_path)
            res_file = self.getResFileName()
            res_ext = self.getResFileExt()
            # Если ресурс/папка с таким именем уже есть в проекте, то
            # не создавать ресурс, а вывести сообщение.
            if self.getRoot().prj_res_manager.isResByNameANDType(res_name, res_ext):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', 
                                u'Ресурс/папка <%s> существует в проекте!' % res_name)
                return None
            # Добавить ресурс в ресурс проекта
            self.getRoot().prj_res_manager.addRes(res_name, res_ext, self._Parent.name)
            self.getRoot().save()
            return res_editor.CreateResource(res_name, res_path, res_file, res_ext,
                                             copy.deepcopy(self.template), bRecreate=True)
        return False
        
    def createResClass(self):
        """
        Функция создания ресурсного класса.
        """
        try:
            self.img = imglib.imgEdtModule
            self.typ = 'py'
            res_name = self.getResName()
            mod_path = self.getParent().getPath()
            # Создать инит файл, если его нет
            ic_res.CreateInitFile(mod_path)
            mod_file = self.getResFileName()
            mod_ext = self.getResFileExt()
            # Есть уже модуль с таким именем?
            if self.getRoot().prj_res_manager.isModByName(mod_file):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', 
                                u'Модуль <%s> уже существует!' % mod_file)
                return False
            # Добавить модуль в ресурс проекта
            ok = self.getRoot().getParent().res_editor.CreateResource(res_name, mod_path, mod_file, mod_ext,
                                                                      copy.deepcopy(self.template), bRecreate=True)
            # Для синхронизации дерева проекта
            self.getRoot().synchroPrj(Refresh_=True)
            return ok
        except:
            io_prnt.outErr(u'Create resource class error <%s>' % self.name)
            return None

    def edit(self):
        """
        Запуск ресурса на редактирование.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_name = self.getResName()
            res_path = self.getResPath()
            ic_file.MakeDirs(res_path)
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
                    return res_editor.SetResource(res_name, res_path, res_file, res_ext,
                                                  bEnable=True)
                else:
                    lock_rec = ic_res.getLockResRecord(res_name, res_file,
                                                       res_ext, self.getRoot().lock_dir)
                    ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                    u'Resource <%s> is locked by user <%s>. Computer: <%s>.' % (res_name,
                                                                                                lock_rec['user'], 
                                                                                                lock_rec['computer']))
                    # Открыть только для чтения
                    self.readonly = True
                    return res_editor.SetResource(res_name, res_path, res_file, res_ext,
                                                  bEnable=False)
            else:
                return res_editor.SetResource(res_name, res_path, res_file, res_ext,
                                              bEnable=False)
        return None

    def rename(self, OldName_, NewName_):
        """
        Переименование ресурса.
        @param OldName_: Старое имя ресурса.
        @param NewName_: Новое имя ресурса.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            old_res_name = self.getResName()
            old_res_file = self.getResPath()+'/'+self.getResFileName()+'.'+self.getResFileExt()

            # Снять блокировку со старого ресурса
            res_name = self.getResName()
            res_file = self.getResFileName()
            res_ext = self.getResFileExt()
            is_lock = ic_res.isLockRes(res_name, res_file, res_ext,
                                       self.getRoot().lock_dir)
            if is_lock:
                ic_res.unlockRes(res_name, res_file, res_ext,
                                 self.getRoot().lock_dir)
            
            self.name = NewName_
            new_res_name = self.getResName()
            new_res_file = self.getResPath()+'/'+self.getResFileName()+'.'+self.getResFileExt()
            # Переименовать в проекте
            self.getRoot().prj_res_manager.renameRes(old_res_name, new_res_name)
            # Для синхронизации дерева проекта
            self.getRoot().save()
            # Если открыт в редакторе ресурсов, то поменять и в нем
            res_editor.RenameResource(old_res_name, old_res_file, new_res_name, new_res_file)
            # И запустить на редактирование
            self.edit()
            return True
        return False

    def save(self):
        """
        Сохранить ресурс/спецификацию.
        """
        return self.create()
  
    def cut(self):
        """
        Вырезать узел.
        @return: Возвращает указхатель на удаленный узел.
        """
        # Переименовать файл ресурса, если он есть
        res_file_name = self.getResPath()+'/'+self.getResFileName()+'.'+self.getResFileExt()
        res_pkl_file_name = self.getResPath()+'/'+self.getResFileName()+'_pkl.'+self.getResFileExt()
        ic_file.icChangeExt(res_file_name, '.bak')
        ic_file.icChangeExt(res_pkl_file_name, '.bak')
        # Удалить из проекта
        self.delete()
        # Удалить из дерева
        return prj_node.PrjNode.cut(self)
        
    def copy(self):
        """
        Копировать.
        """
        node = prj_node.PrjNode.copy(self)
        # Скопировать файл ресурса во временный файл
        res_file_name = self.getResPath()+'/'+self.getResFileName()+'.'+self.getResFileExt()
        copy_res_file_name = node.getResPath()+'/'+node.getResFileName()+'.bak'
        ic_file.icCopyFile(res_file_name, copy_res_file_name)
        # Кроме копирования файла необходимо
        # поменять имя ресурса в этом файле
        res = ic_res.ReadAndEvalFile(copy_res_file_name)
        res[node.name] = res[self.name]
        del res[self.name]
        copy_res_file = None
        try:
            copy_res_file = open(copy_res_file_name, 'w')
            copy_res_file.write(str(res))
            copy_res_file.close()
        except:
            if copy_res_file:
                copy_res_file.close()
            io_prnt.outErr()
        return node
        
    def paste(self, Node_):
        """
        Вставить.
        @param Node_: Вставляемый узел.
        """
        # Поменять расширение у bak файлов.
        res_file_name = Node_.getResPath()+'/'+Node_.getResFileName()+'.bak'
        res_pkl_file_name = Node_.getResPath()+'/'+Node_.getResFileName()+'_pkl.bak'
        to_res_file_name = self.getResPath()+'/'+Node_.getResFileName()+'.'+Node_.typ
        to_res_pkl_file_name = self.getResPath()+'/'+Node_.getResFileName()+'_pkl.''.'+Node_.typ
        
        ic_file.icCopyFile(res_file_name, to_res_file_name)
        ic_file.icCopyFile(res_pkl_file_name, to_res_pkl_file_name)
        
        # Прописать его в проекте
        self.getRoot().prj_res_manager.addRes(Node_.name, Node_.typ, self._Parent.name)
        # Вставить в проект
        return prj_node.PrjNode.paste(self, Node_)
        
    def delete(self):
        """
        Удалить ресурс.
        """
        # Сначала удалить из файла *.pro
        self.getRoot().prj_res_manager.delRes(self.name, self.typ)
        # Затем удалить из дерева
        prj_node.PrjNode.delete(self)
        # И в конце удалить файл ресурса, если он есть
        res_file_name = os.path.join(self.getResPath(), self.getResFileName()+'.'+self.getResFileExt())
        res_pkl_file_name = os.path.join(self.getResPath(), self.getResFileName()+'_pkl.'+self.getResFileExt())
        
        # Выгрузить из редактора
        edit_res_file_name = self.getRoot().getParent().res_editor.GetResFileName()
        if edit_res_file_name and \
            ic_file.SamePathWin(res_file_name, edit_res_file_name):
            # Закрыть и разблокировать
            self.getRoot().getParent().res_editor.CloseResource()
            self.getRoot().unlockResInResEditor(self.getRoot().getParent().res_editor)
            
        if os.path.exists(res_file_name):
            # ВНИМАНИЕ! Ресурс сам удаляем!!! Но чтобы можно было его
            # восстановить оставляем его бекапную версию!!!
            ic_file.icCreateBAKFile(res_file_name)
            os.remove(res_file_name)
        if os.path.exists(res_pkl_file_name):
            os.remove(res_pkl_file_name)
        # Для синхронизации дерева проекта
        self.getRoot().save()
   
    def onNodePopup(self, event):
        """
        Вызов всплывающего меню узла.
        """
        my_root = self.getRoot()
        # Если узел может только редактироваться (находится в импортируемой подсистеме)
        # то копировать его хотя бы можно
        if self.readonly:
            popup_menu = menuImpNode.icMenuImpResNode(self)
            popup_menu.Popup(wx.GetMousePosition(), my_root.getParentRoot().getParent())
        else:
            popup_menu = menuPrjNode.icMenuPrjNode(self)
            popup_menu.Popup(wx.GetMousePosition(), my_root.getParent())

    def getViewer(self, parent):
        """
        Просмотрщик узла.
        """
        from . import icresviewer
        return icresviewer.icResPrjNodeViewer(parent, self)
        
    def getMyRes(self):
        """
        Получить ресурс узла.
        """
        full_res_file_name = self.getFullResFileName()
        res = util.readAndEvalFile(full_res_file_name)
        return res
        
    def getPopupHelpText(self):
        """
        Получить текст всплывающей помощи.
        """
        res = self.getMyRes()
        if res:
            res_root = res[res.keys()[0]]
            description = res_root.get('description', u'')
            return description
        return u''


class PrjTabRes(PrjResource):
    """
    Таблица.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = _('Table')
        self.name = 'new_tab'
        self.img = imglib.imgEdtTable
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'tab'
        # Шаблон для заполнения по умолчанию
        self.template = ic_tab.ic_class_spc

    def delete(self):
        """
        Удалить узел. Удалить таблицу из БД тоже.
        """
        if ic_dlg.icAskDlg(u'ВНИМАНИЕ!', 
                           u'Удалить таблицу из БД?') == wx.YES:
            del_cascade = False
            if ic_dlg.icAskDlg(u'ВНИМАНИЕ!',
                               u'Удалить дочерние таблицы из БД?') == wx.YES:
                del_cascade = True
            import ic.db.icsqlalchemy
            try: 
                tab = ic.db.icsqlalchemy.icSQLAlchemyTabClass(self.name)
                tab.drop(del_cascade)
            except:
                io_prnt.outErr(u'Ошибка удаления таблицы из БД при удалении ресурса')
            
        return PrjResource.delete(self)

    def rename(self, OldName_, NewName_):
        """
        Переименование ресурса.
        @param OldName_: Старое имя ресурса.
        @param NewName_: Новое имя ресурса.
        """
        new_name = NewName_.lower()
        old_name = OldName_.lower()
        if new_name != NewName_ or OldName_ != old_name:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'All table, field and link name must be in lower case')
        return PrjResource.rename(self, old_name, new_name)


# Словарь выбора БД
DBTypeChoice = {'SQLite DB': ic_sqlite.ic_class_spc,
                'PostgreSQL DB': ic_postgres.ic_class_spc,
                'MSSQL DB': ic_mssql.ic_class_spc,
                'Object Storage': ic_obj_storage_src.ic_class_spc,
                'ODBC data source': ic_odbc.ic_class_spc,
                'SQLAlchemy scheme': ic_sqlalchemy_scheme_wrp.ic_class_spc,
                'MySQL DB': ic_mysql.ic_class_spc,
                None: None,
                }


class PrjDBRes(PrjResource):
    """
    БД.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = u'Data source/DB'
        self.name = 'new_db'
        self.img = imglib.imgDb
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'src'
        # Шаблон для заполнения по умолчанию
        self.template = None

    def create(self):
        """
        Создание ресурса.
        """
        # Сначал спросить какую БД будем создавать а затем создать ее
        global DBTypeChoice
        self.template = DBTypeChoice[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                              _('Choose DB'), _('DB list:'),
                                                              [txt for txt in DBTypeChoice.keys() if type(txt) in (str, unicode)])]
        # Создать
        return PrjResource.create(self)
        
    def createResClass(self):
        """
        Создание ресурсного класса.
        """
        # Сначал спросить какую БД будем создавать а затем создать ее
        global DBTypeChoice
        self.template = DBTypeChoice[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                              _('Choose DB'), _('DB list:'),
                                                              [txt for txt in DBTypeChoice.keys() if type(txt) in (str, unicode)])]
        # Создать
        return PrjResource.createResClass(self)

    def extend(self):
        """
        Дополнительные инструменты узла.
        """
        # Данном случае проверка связи с БД
        res = self.getMyRes()
        name = res.keys()[0]
        spc = res.get(name, dict())
        yes = ic_dlg.icAskBox(u'Проверка связи с БД', u'Поверить связь с БД <%s : %s>?' % (spc['name'], spc['type']))
        if yes:
            from ic.db import icsqlalchemy
            db_url = icsqlalchemy.createDBUrl(spc)
            check_connect = icsqlalchemy.checkDBConnect(db_url)
            msg = u'Связь с БД <%s> успешно установлена' % db_url if check_connect else u'Нет связи с БД <%s>' % db_url
            ic_dlg.icMsgBox(u'Проверка связи с БД', msg)


class PrjSQLiteRes(PrjResource):
    """
    БД SQLite.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = 'SQLite DB'
        self.name = 'new_sqlite'
        self.img = imglib.imgEdtSQLite
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'sqt'
        # Шаблон для заполнения по умолчанию
        self.template = ic_sqlite.ic_class_spc


class PrjPostgreSQLRes(PrjResource):
    """
    БД PostgreSQL.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = 'PostgreSQL DB'
        self.name = 'new_postgres'
        self.img = imglib.imgEdtPostgreSQL
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'pgs'
        # Шаблон для заполнения по умолчанию
        self.template = ic_postgres.ic_class_spc

    def extend(self):
        """
        Дополнительные инструменты узла.
        """
        # Данном случае проверка связи с БД
        yes = ic_dlg.icAskBox(u'Поверить связь с БД?')
        if yes:
            from ic.db import icsqlalchemy
            res = self.getMyRes()
            db_url = icsqlalchemy.createDBUrl(res)
            check_connect = icsqlalchemy.checkDBConnect(db_url)
            msg = u'Связь с БД <%s> успешно установлена' % db_url if check_connect else u'Нет связи с БД <%s>' % db_url
            ic_dlg.icMsgBox(u'Проверка связи с БД', msg)


class PrjFrmRes(PrjResource):
    """
    Форма.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = u'Форма'
        self.name = 'new_form'
        self.img = imglib.imgEdtFrame
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'frm'


class PrjObjStorageRes(PrjResource):
    """
    Хранилище ObjectStorage.
    """
    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = 'Object Storage'
        self.name = 'new_storage'
        self.img = imglib.imgEdtObjStorage
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'odb'
        # Шаблон для заполнения по умолчанию
        self.template = ic_obj_storage.ic_class_spc
 
# Словарь выбора главных окон
WinTypeChoice = {'Standart main window': ic_mainwin.ic_class_spc,
                 'AUI main window': ic_auimainwin.ic_class_spc,
                 None: None,
                 }


class PrjWinRes(PrjResource):
    """
    Главное окно.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = u'Главное окно'
        self.name = 'new_win'
        self.img = imglib.imgEdtMainWin
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'win'
        # Шаблон для заполнения по умолчанию
        self.template = ic_auimainwin.ic_class_spc

    def create(self):
        """
        Создание ресурса.
        """
        # Сначал спросить какую БД будем создавать а затем создать ее
        global WinTypeChoice
        self.template = WinTypeChoice[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                               _('Choose main window type'),
                                                               _('Main window type list:'),
                                                               [txt for txt in WinTypeChoice.keys() if type(txt) in (str, unicode)])]
        # Создать
        return PrjResource.create(self)
        
    def createResClass(self):
        """
        Создание ресурсного класса.
        """
        # Сначал спросить какую БД будем создавать а затем создать ее
        global WinTypeChoice
        self.template = WinTypeChoice[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                               _('Choose main window type'),
                                                               _('Main window type list:'),
                                                               [txt for txt in WinTypeChoice.keys() if type(txt) in (str, unicode)])]
        # Создать
        return PrjResource.createResClass(self)

# Словарь выбора типов меню
MenuTypeChoice = {'Standart menu bar': ic_menubar_wrp.ic_class_spc,
                  'Flat menu bar': ic_flatmenubar_wrp.ic_class_spc,
                  'Flat popup menu': ic_flatmenu_wrp.ic_class_spc,
                  None: None,
                  }


class PrjMenuRes(PrjResource):
    """
    Меню.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = u'Меню'
        self.name = 'new_menu'
        self.img = imglib.imgEdtMenuBar
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'mnu'
        # Шаблон для заполнения по умолчанию
        self.template = None
        
    def create(self):
        """
        Создание ресурса.
        """
        # Сначал спросить какую меню будем создавать а затем создать ее
        global MenuTypeChoice
        self.template = MenuTypeChoice[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                                _('Choose menu type'), _('Menu type list:'),
                                                                [txt for txt in MenuTypeChoice.keys() if type(txt) in (str, unicode)])]
        # Создать
        return PrjResource.create(self)
        
    def createResClass(self):
        """
        Создание ресурсного класса.
        """
        # Сначал спросить какую меню будем создавать а затем создать ее
        global MenuTypeChoice
        self.template = MenuTypeChoice[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                                _('Choose menu type'),
                                                                _('Menu type list:'),
                                                                [txt for txt in MenuTypeChoice.keys() if type(txt) in (str, unicode)])]
        # Создать
        return PrjResource.createResClass(self)


class PrjTemplate(PrjResource):
    """
    Шаблон.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = u'Шаблон'
        self.name = 'new_template'
        self.enable = False     # Выключить шаблоны для использования
        self.typ = 'ftl'
        self.img = imglib.imgEdtTemplate
        # Шаблон для заполнения по умолчанию
        self.template = None


class PrjMethod(PrjResource):
    """
    Метод.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = u'Метод'
        self.name = 'new_method'
        self.enable = False     # Выключить методы для использования
        self.typ = 'mth'
        self.img = imglib.imgEdtMethod

        # Шаблон для заполнения по умолчанию
        self.template = ic_mth.ic_class_spc


class PrjMetaDataRes(PrjResource):
    """
    Дерево метаклассов/Метаданные.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        """
        PrjResource.__init__(self, Parent_)
        self.description = u'Метаданные'
        self.name = 'new_metadata'
        self.typ = 'mtd'
        self.img = imglib.imgEdtMetaData

    def _getExtendToolList(self):
        """
        Список дополнительных инструментов узла.
        @return: Список словарей:
            [{
                'name': Наименование инструмента,
                'label': Надпись в диалоговом окне выбора инструмента,
                'func': Функция передачи управления инструменту.
            }, ...]
        """
        ext_tools = list()
        # Инструмент первый
        # Генератор форм wxFormBuilder бизнес объекта/документа
        try:
            from work_flow.fb_form_generator import fb_form_gen
        except ImportError:
            # Если нет возможности импортировать,
            # то и инструмент не доступен
            io_prnt.outWarning(u'''Не доступен дополнительный инструмент
<Генератор форм wxFormBuilder бизнес объекта/документа>.
Для его активации подключите/обновите подсистему <work_flow>''')
            fb_form_gen = None

        if fb_form_gen:
            # Функция обработки инструмента
            def fb_form_gen_tool():
                # Определить ресурс
                res = self.getMyRes()
                # Генерация имени файла по умолчанию
                fbp_base_filename = res.values()[0]['name'].lower() + '_frm_proto.fbp'
                # Выбор имени файла проекта
                fbp_dir = ic_dlg.icDirDlg(self.getPrjTreeCtrl(),
                                          u'Выбор файла папки хранения проекта wxFormBuilder для генерации',
                                          DefaultPath_=self.getPath())
                if not fbp_dir:
                    # Нажали отмену
                    return

                fbp_filename = os.path.join(fbp_dir, fbp_base_filename)

                # Произвести обновление проекта?
                do_refresh = not os.path.exists(fbp_filename)

                # Запуск генерации
                if fb_form_gen.gen_wxfb_prj(self.getPrjTreeCtrl(), res, fbp_filename):
                    if do_refresh:
                        # обновить дерево проекта
                        root = self.getRoot()
                        root.openPrj(root.getPrjFileName())
                        root.getPrjTreeCtrl().Refresh()

            tool = dict(name='fb_form_gen',
                        label=u'Генератор форм wxFormBuilder бизнес объекта/документа',
                        func=fb_form_gen_tool)
            ext_tools.append(tool)

        return ext_tools

    def extend(self):
        """
        Дополнительные инструменты узла.
        """
        ext_tools = self._getExtendToolList()
        if ext_tools:
            choices = [tool['label'] for tool in ext_tools]
            i_select = ic_dlg.icSingleChoiceIdxDlg(self.getPrjTreeCtrl(),
                                                   u'Дополнительные инструменты',
                                                   u'Выберите операцию с ресурсом:',
                                                   choices)
            if i_select >= 0:
                func = ext_tools[i_select]['func']
                func()
        else:
            io_prnt.outWarning(u'Не предусмотрены дополнительные инструменты для ресурса <%s>' % self.getResName())
