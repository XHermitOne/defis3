#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Модуль классов узлов ресурсов проекта.
"""

# Подключение библиотек
import wx
import copy
import os
import os.path

from ic.imglib import common as imglib
from ic.utils import ic_file
from ic.utils import ic_res
from ic.utils import resfunc
from ic.utils import util
from ic.dlg import ic_dlg
from ic.log import log

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

from . import new_metadata_resource_dlg

__version__ = (0, 1, 4, 1)

_ = wx.GetTranslation


class icPrjResources(prj_node.icPrjFolder):
    """
    Ресурсы.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        prj_node.icPrjFolder.__init__(self, parent)
        self.img_extended = imglib.imgFolderOpen
        self.description = u'Ресурсы'
        self.name = u'Ресурсы'
        # Классы узлов, которые м.б. включены в текущий узел
        self.include_nodes = [icPrjTabRes, icPrjDBRes,
                              icPrjObjStorageRes,
                              icPrjFrmRes, icPrjWinRes,
                              icPrjMenuRes, icPrjTemplate, icPrjMethod, icPrjMetaDataRes]
        self.include_folder = icPrjResources
        
    def isMainFolder(self):
        """
        Проверка является ли эта папка главной.
        """
        return self.getParent() == self.getRoot()
        
    def create(self, new_name=None):
        """
        Создать папку.
        @param new_name: Указание нового имени созданного узла.
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
        return prj_node.icPrjNode.delete(self)

    def rename(self, old_name, new_name):
        """
        Переименование папки.
        @param old_name: Старое имя папки.
        @param new_name: Новое имя папки.
        """
        # Переименовать в проекте
        self.getRoot().prj_res_manager.renameRes(old_name, new_name)
        self.name = new_name
        # Для синхронизации дерева проекта
        self.getRoot().save()
        return True

    def importChild(self, res_filename=None):
        """
        Импортировать ресурс, как дочерний узел.
        @param res_filename: Имя импортируемого ресурсного файла.
        @return: Возвращает вновь созданный узел или None.
        """
        new_node = None
        if os.path.exists(res_filename):
            # Сделать новое имя файла
            new_res_file_name = ic_file.get_absolute_path(os.path.join('.', self.getRoot().name,
                                                                       os.path.basename(res_filename)))
            # Если новый файл существут, то спросить о его перезаписи
            if not ic_file.isSamePathWin(res_filename, new_res_file_name):
                # Скопировать файл
                ic_file.copyFile(res_filename, new_res_file_name, True)
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


class icPrjResource(prj_node.icPrjNode):
    """
    Ресурс.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        prj_node.icPrjNode.__init__(self, parent)
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
            return ic_file.getAbsolutePath(prj_name,
                                           os.path.dirname(self.getRoot().getPrjFileName()))
        else:
            return os.path.split(prj_file_name)[0].strip()

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
        return os.path.normpath(os.path.join(self.getResPath(),
                                             self.getResFileName()+'.'+self.getResFileExt()))
        
    def getResName(self):
        """
        Имя ресурса.
        """
        return self.name.strip()

    def _setTemplateSpc(self, spc, new_name):
        """
        Вспомогательная функция установки шаблона заполнения ресурса по спецификации.
        @param spc: Спецификция компонента.
        @param new_name: Новое имя ресурса.
        @return: True/False.
        """
        if spc:
            self.template = copy.deepcopy(spc)
            if not new_name:
                new_name = ic_dlg.icTextEntryDlg(self.getPrjTreeCtrl(), title=u'НАИМЕНОВАНИЕ',
                                                 prompt_text=u'Введите наименование ресурса', default_value=self.name)

            # У ресурса такое имя как и у ресурса
            self.template['name'] = new_name
            return True
        else:
            self.template = None
        return False

    def create(self, new_name=None):
        """
        Функция создания ресурса.
        @param new_name: Указание нового имени созданного узла.
        """
        # Ввести наименование при создании ресурса
        if not new_name:
            new_name = ic_dlg.icTextEntryDlg(self.getPrjTreeCtrl(), title=u'НАИМЕНОВАНИЕ',
                                             prompt_text=u'Введите наименование ресурса', default_value=self.name)
            if new_name is None:
                # Нажата ОТМЕНА
                return False

        if new_name:
            self.name = new_name

        # Изменили имя - обновили шаблон ресурса
        self._setTemplateSpc(self.template, new_name)

        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            res_name = self.getResName()
            res_path = self.getResPath()
            if not os.path.exists(res_path):
                os.makedirs(res_path)
            res_file = self.getResFileName()
            res_ext = self.getResFileExt()
            # Если ресурс/папка с таким именем уже есть в проекте, то
            # не создавать ресурс, а вывести сообщение.
            if self.getRoot().prj_res_manager.isResByNameANDType(res_name, res_ext):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', 
                                u'Ресурс/папка <%s.%s> существует в проекте!' % (res_name, res_ext))
                return None
            # Добавить ресурс в ресурс проекта
            self.getRoot().prj_res_manager.addRes(res_name, res_ext, self._Parent.name)
            self.getRoot().save()
            return res_editor.CreateResource(res_name, res_path, res_file, res_ext,
                                             self.template, bRecreate=True)
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
            self.getRoot().synchroPrj(bRefresh=True)
            return ok
        except:
            log.fatal(u'Ошибка создания ресурсного класса <%s>' % self.name)
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

            if not os.path.exists(res_path):
                try:
                    os.makedirs(res_path)
                except:
                    log.fatal(u'Ошибка создания папки <%s>' % res_path)

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
                    ic_dlg.icWarningBox(u'БЛОКИРОВКА',
                                        u'Ресурс <%s> заблокирован пользователем <%s> с компьютера <%s>.' % (res_name,
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

    def rename(self, old_name, new_name):
        """
        Переименование ресурса.
        @param old_name: Старое имя ресурса.
        @param new_name: Новое имя ресурса.
        """
        tree_prj = self.getRoot().getParent()
        res_editor = tree_prj.res_editor
        if res_editor:
            old_res_name = self.getResName()
            old_res_file = os.path.join(self.getResPath(),
                                        self.getResFileName()+'.'+self.getResFileExt())

            # Снять блокировку со старого ресурса
            res_name = self.getResName()
            res_file = self.getResFileName()
            res_ext = self.getResFileExt()
            is_lock = ic_res.isLockRes(res_name, res_file, res_ext,
                                       self.getRoot().lock_dir)
            if is_lock:
                ic_res.unlockRes(res_name, res_file, res_ext,
                                 self.getRoot().lock_dir)
            
            self.name = new_name
            new_res_name = self.getResName()
            new_res_file = os.path.join(self.getResPath(),
                                        self.getResFileName()+'.'+self.getResFileExt())
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
        res_file_name = os.path.join(self.getResPath(),
                                     self.getResFileName()+'.'+self.getResFileExt())
        res_pkl_file_name = os.path.join(self.getResPath(),
                                         self.getResFileName()+'_pkl.'+self.getResFileExt())
        ic_file.changeExt(res_file_name, '.bak')
        ic_file.changeExt(res_pkl_file_name, '.bak')
        # Удалить из проекта
        self.delete()
        # Удалить из дерева
        return prj_node.icPrjNode.cut(self)
        
    def copy(self):
        """
        Копировать.
        """
        node = prj_node.icPrjNode.copy(self)
        # Скопировать файл ресурса во временный файл
        res_file_name = os.path.join(self.getResPath(),
                                     self.getResFileName()+'.'+self.getResFileExt())
        copy_res_file_name = os.path.join(node.getResPath(),
                                          node.getResFileName()+'.bak')
        ic_file.copyFile(res_file_name, copy_res_file_name)
        # Кроме копирования файла необходимо
        # поменять имя ресурса в этом файле
        # ВНИМАНИЕ! Здесь нельзя использовать readAndEval,
        # т.к. эта функция создает *_pkl.* файл.
        # Работаем только с текстовым представлением
        res = resfunc.LoadResourceText(copy_res_file_name)
        res[node.name] = res[self.name]
        del res[self.name]
        # Поменять наименование объекта
        res[node.name]['name'] = node.name
        copy_res_file = None
        try:
            copy_res_file = open(copy_res_file_name, 'wt')
            copy_res_file.write(str(res))
            copy_res_file.close()
        except:
            if copy_res_file:
                copy_res_file.close()
            log.fatal(u'Ошибка сохранения файла <%s>' % copy_res_file_name)
        return node
        
    def paste(self, node):
        """
        Вставить.
        @param node: Вставляемый узел.
        """
        # Поменять расширение у bak файлов.
        res_file_name = os.path.join(node.getResPath(),
                                     node.getResFileName() + '.bak')
        to_res_file_name = os.path.join(self.getResPath(),
                                        node.getResFileName() + '.' + node.typ)

        try:
            os.rename(res_file_name, to_res_file_name)
            log.debug(u'Переименование файла <%s> -> <%s>' % (res_file_name, to_res_file_name))
        except:
            log.fatal(u'Ошибка переименования файла <%s> -> <%s>' % (res_file_name, to_res_file_name))

        # Прописать его в проекте
        self.getRoot().prj_res_manager.addRes(node.name, node.typ, self._Parent.name)
        self.getRoot().prj_res_manager.save()
        # Вставить в проект
        return prj_node.icPrjNode.paste(self, node)
        
    def delete(self):
        """
        Удалить ресурс.
        """
        # Сначала удалить из файла *.pro
        self.getRoot().prj_res_manager.delRes(self.name, self.typ)
        # Затем удалить из дерева
        prj_node.icPrjNode.delete(self)
        # И в конце удалить файл ресурса, если он есть
        res_file_name = os.path.join(self.getResPath(), self.getResFileName()+'.'+self.getResFileExt())
        res_pkl_file_name = os.path.join(self.getResPath(), self.getResFileName()+'_pkl.'+self.getResFileExt())
        
        # Выгрузить из редактора
        edit_res_file_name = self.getRoot().getParent().res_editor.GetResFileName()
        if edit_res_file_name and \
            ic_file.isSamePathWin(res_file_name, edit_res_file_name):
            # Закрыть и разблокировать
            self.getRoot().getParent().res_editor.CloseResource()
            self.getRoot().unlockResInResEditor(self.getRoot().getParent().res_editor)
            
        if os.path.exists(res_file_name):
            # ВНИМАНИЕ! Ресурс сам удаляем!!! Но чтобы можно было его
            # восстановить оставляем его бекапную версию!!!
            ic_file.createBAKFile(res_file_name)
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
            res_root = res[list(res.keys())[0]]
            description = res_root.get('description', u'')
            return description
        return u''


# Словарь выбора тиблиц
TableTypeChoice = {u'Стандартная таблица': ic_tab.ic_class_spc,
                   u'Таблица стандартного справочника': ic_tab.SPC_IC_NSI_TABLE,
                   None: None,
                   }


class icPrjTabRes(icPrjResource):
    """
    Таблица.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = _('Table')
        self.name = 'new_tab'
        self.img = imglib.imgEdtTable
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'tab'
        # Шаблон для заполнения по умолчанию
        self.template = ic_tab.ic_class_spc

    def create(self, new_name=None):
        """
        Создание ресурса.
        @param new_name: Указание нового имени созданного узла.
        """
        # Сначал спросить какую Таблицу будем создавать а затем создать ее
        global TableTypeChoice
        spc = TableTypeChoice[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                       u'ТИПЫ ТАБЛИЦ', u'Выберите из списка типов таблиц:',
                                                       [txt for txt in TableTypeChoice.keys() if isinstance(txt, str)])]
        if spc is None:
            # Нажата ОТМЕНА
            return False

        if not new_name:
            new_name = ic_dlg.icTextEntryDlg(self.getPrjTreeCtrl(), title=u'НАИМЕНОВАНИЕ',
                                             prompt_text=u'Введите наименование ресурса', default_value=self.name)
            if new_name is None:
                # Нажата ОТМЕНА
                return False

        self._setTemplateSpc(spc, new_name)

        # Создать
        return icPrjResource.create(self, new_name=new_name)

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
                log.fatal(u'Ошибка удаления таблицы из БД при удалении ресурса')
            
        return icPrjResource.delete(self)

    def rename(self, old_name, new_name):
        """
        Переименование ресурса.
        @param old_name: Старое имя ресурса.
        @param new_name: Новое имя ресурса.
        """
        new_name = new_name.lower()
        old_name = old_name.lower()
        if new_name != new_name or old_name != old_name:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'All table, field and link name must be in lower case')
        return icPrjResource.rename(self, old_name, new_name)

    def extend(self):
        """
        Дополнительные инструменты узла.
        """
        from . import gen_model_dialog
        from ic.db import icmodel

        # Данном случае возможна генерация модулей модели и
        # менеджера модели по ресурсу таблицы для работы с таблицей через SQLAlchemy
        tab_res_filename = self.getResFileName()

        name = self.getResName()
        # Проверяем наличие файлов модулей
        # для определения обновления дерева прокта
        model_module_filename = icmodel.genModelModuleFilename(name=name)
        model_manager_module_filename = icmodel.genModelModuleManagerFilename(name=name)
        is_prev = os.path.exists(model_module_filename) and os.path.exists(model_manager_module_filename)

        # Вызываем метод открытия диалогового окна управления генерацией
        # модйлей модели и менеджера модели
        gen_model_dialog.open_gen_model_dialog(tab_res_filename=tab_res_filename)

        # Определяем нужно ли обновлять дерево проекта
        is_post = os.path.exists(model_module_filename) and os.path.exists(model_manager_module_filename)
        if is_prev != is_post:
            # Обновляем дерево проекта
            self.getRoot().getParent().Refresh()


# Словарь выбора БД
DATABASE_TYPE_CHOICE = {'SQLite DB': ic_sqlite.ic_class_spc,
                        'PostgreSQL DB': ic_postgres.ic_class_spc,
                        'MSSQL DB': ic_mssql.ic_class_spc,
                        'Object Storage': ic_obj_storage_src.ic_class_spc,
                        'ODBC data source': ic_odbc.ic_class_spc,
                        'SQLAlchemy scheme': ic_sqlalchemy_scheme_wrp.ic_class_spc,
                        'MySQL DB': ic_mysql.ic_class_spc,
                        None: None,
                        }


class icPrjDBRes(icPrjResource):
    """
    БД.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = u'Data source/DB'
        self.name = 'new_db'
        self.img = imglib.imgDb
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'src'
        # Шаблон для заполнения по умолчанию
        self.template = None

    def create(self, new_name=None):
        """
        Создание ресурса.
        @param new_name: Указание нового имени созданного узла.
        """
        # Сначал спросить какую БД будем создавать а затем создать ее
        global DATABASE_TYPE_CHOICE
        spc = DATABASE_TYPE_CHOICE[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                    u'ТИПЫ БД', u'Выберите из списка типов БД:',
                                                            [txt for txt in DATABASE_TYPE_CHOICE.keys() if isinstance(txt, str)])]
        if spc is None:
            # Нажата ОТМЕНА
            return False
        if not new_name:
            new_name = ic_dlg.icTextEntryDlg(self.getPrjTreeCtrl(), title=u'НАИМЕНОВАНИЕ',
                                             prompt_text=u'Введите наименование ресурса', default_value=self.name)
            if new_name is None:
                # Нажата ОТМЕНА
                return False
        self._setTemplateSpc(spc, new_name)

        # Создать
        return icPrjResource.create(self, new_name=new_name)
        
    def createResClass(self):
        """
        Создание ресурсного класса.
        """
        # Сначал спросить какую БД будем создавать а затем создать ее
        global DATABASE_TYPE_CHOICE
        self.template = DATABASE_TYPE_CHOICE[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                                      _('Choose DB'), _('DB list:'),
                                                                      [txt for txt in DATABASE_TYPE_CHOICE.keys() if isinstance(txt, str)])]
        # Создать
        return icPrjResource.createResClass(self)

    def extend(self):
        """
        Дополнительные инструменты узла.
        """
        # Данном случае проверка связи с БД
        res = self.getMyRes()
        name = list(res.keys())[0]
        spc = res.get(name, dict())
        yes = ic_dlg.icAskBox(u'Проверка связи с БД', u'Поверить связь с БД <%s : %s>?' % (spc['name'], spc['type']))
        if yes:
            from ic.db import icdb
            db_url = icdb.createDBUrl(spc)
            check_connect = icdb.checkDBConnect(db_url)
            msg = u'Связь с БД <%s> успешно установлена' % db_url if check_connect else u'Нет связи с БД <%s>' % db_url
            ic_dlg.icMsgBox(u'Проверка связи с БД', msg)


class icPrjSQLiteRes(icPrjResource):
    """
    БД SQLite.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = 'SQLite DB'
        self.name = 'new_sqlite'
        self.img = imglib.imgEdtSQLite
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'sqt'
        # Шаблон для заполнения по умолчанию
        self.template = ic_sqlite.ic_class_spc


class icPrjPostgreSQLRes(icPrjResource):
    """
    БД PostgreSQL.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
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
            from ic.db import icdb
            res = self.getMyRes()
            db_url = icdb.createDBUrl(res)
            check_connect = icdb.checkDBConnect(db_url)
            msg = u'Связь с БД <%s> успешно установлена' % db_url if check_connect else u'Нет связи с БД <%s>' % db_url
            ic_dlg.icMsgBox(u'Проверка связи с БД', msg)


class icPrjFrmRes(icPrjResource):
    """
    Форма.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = u'Форма'
        self.name = 'new_form'
        self.img = imglib.imgEdtFrame
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'frm'


class icPrjObjStorageRes(icPrjResource):
    """
    Хранилище ObjectStorage.
    """
    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = 'Object Storage'
        self.name = 'new_storage'
        self.img = imglib.imgEdtObjStorage
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'odb'
        # Шаблон для заполнения по умолчанию
        self.template = copy.deepcopy(ic_obj_storage.ic_class_spc)
 

# Словарь выбора главных окон
WINDOW_TYPE_CHOICE = {'Standart main window': ic_mainwin.ic_class_spc,
                      'AUI main window': ic_auimainwin.ic_class_spc,
                      None: None,
                      }


class icPrjWinRes(icPrjResource):
    """
    Главное окно.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = u'Главное окно'
        self.name = 'new_win'
        self.img = imglib.imgEdtMainWin
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'win'
        # Шаблон для заполнения по умолчанию
        self.template = ic_auimainwin.ic_class_spc

    def create(self, new_name=None):
        """
        Создание ресурса.
        @param new_name: Указание нового имени созданного узла.
        """
        # Сначал спросить какую БД будем создавать а затем создать ее
        global WINDOW_TYPE_CHOICE
        spc = WINDOW_TYPE_CHOICE[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                     u'ВИДЫ ГЛАВНОГО ОКНА',
                                                     u'Выберите из списка типов главного окна:',
                                                          [txt for txt in WINDOW_TYPE_CHOICE.keys() if isinstance(txt, str)])]
        if spc is None:
            # Нажата ОТМЕНА
            return False
        if not new_name:
            new_name = ic_dlg.icTextEntryDlg(self.getPrjTreeCtrl(), title=u'НАИМЕНОВАНИЕ',
                                             prompt_text=u'Введите наименование ресурса', default_value=self.name)
            if new_name is None:
                # Нажата ОТМЕНА
                return False

        self._setTemplateSpc(spc, new_name)

        # Создать
        return icPrjResource.create(self, new_name=new_name)
        
    def createResClass(self):
        """
        Создание ресурсного класса.
        """
        # Сначал спросить какую БД будем создавать а затем создать ее
        global WINDOW_TYPE_CHOICE
        self.template = WINDOW_TYPE_CHOICE[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                                    _('Choose main window type'),
                                                                    _('Main window type list:'),
                                                                    [txt for txt in WINDOW_TYPE_CHOICE.keys() if isinstance(txt, str)])]
        # Создать
        return icPrjResource.createResClass(self)


# Словарь выбора типов меню
MENU_TYPE_CHOICE = {'Standart menu bar': ic_menubar_wrp.ic_class_spc,
                    'Flat menu bar': ic_flatmenubar_wrp.ic_class_spc,
                    'Flat popup menu': ic_flatmenu_wrp.ic_class_spc,
                    None: None,
                    }


class icPrjMenuRes(icPrjResource):
    """
    Меню.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = u'Меню'
        self.name = 'new_menubar'
        self.img = imglib.imgEdtMenuBar
        # Тип ресурса 'tab', 'frm' и т.п.
        self.typ = 'mnu'
        # Шаблон для заполнения по умолчанию
        self.template = None
        
    def create(self, new_name=None):
        """
        Создание ресурса.
        @param new_name: Указание нового имени созданного узла.
        """
        # Сначал спросить какую меню будем создавать а затем создать ее
        global MENU_TYPE_CHOICE
        spc = MENU_TYPE_CHOICE[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                      u'ВИДЫ ГЛАВНОГО МЕНЮ',
                                                      u'Выберите из списка видов главного меню:',
                                                        [txt for txt in MENU_TYPE_CHOICE.keys() if isinstance(txt, str)])]
        if spc is None:
            # Нажата ОТМЕНА
            return False
        if not new_name:
            new_name = ic_dlg.icTextEntryDlg(self.getPrjTreeCtrl(), title=u'НАИМЕНОВАНИЕ',
                                             prompt_text=u'Введите наименование ресурса', default_value=self.name)
            if new_name is None:
                # Нажата ОТМЕНА
                return False
        self._setTemplateSpc(spc, new_name)

        # Создать
        return icPrjResource.create(self, new_name=new_name)
        
    def createResClass(self):
        """
        Создание ресурсного класса.
        """
        # Сначал спросить какую меню будем создавать а затем создать ее
        global MENU_TYPE_CHOICE
        self.template = MENU_TYPE_CHOICE[ic_dlg.icSingleChoiceDlg(self.getRoot().getParent(),
                                                                  _('Choose menu type'),
                                                                  _('Menu type list:'),
                                                                  [txt for txt in MENU_TYPE_CHOICE.keys() if isinstance(txt, str)])]
        # Создать
        return icPrjResource.createResClass(self)


class icPrjTemplate(icPrjResource):
    """
    Шаблон.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = u'Шаблон'
        self.name = 'new_template'
        self.enable = False     # Выключить шаблоны для использования
        self.typ = 'ftl'
        self.img = imglib.imgEdtTemplate
        # Шаблон для заполнения по умолчанию
        self.template = None


class icPrjMethod(icPrjResource):
    """
    Метод.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
        self.description = u'Метод'
        self.name = 'new_method'
        self.enable = False     # Выключить методы для использования
        self.typ = 'mth'
        self.img = imglib.imgEdtMethod

        # Шаблон для заполнения по умолчанию
        self.template = ic_mth.ic_class_spc


class icPrjMetaDataRes(icPrjResource):
    """
    Дерево метаклассов/Метаданные.
    """

    def __init__(self, parent=None):
        """
        Конструктор.
        """
        icPrjResource.__init__(self, parent)
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
                'function': Функция передачи управления инструменту.
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
            log.warning(u'''Не доступен дополнительный инструмент
<Генератор форм wxFormBuilder бизнес объекта/документа>.
Для его активации подключите/обновите подсистему <work_flow>''')
            fb_form_gen = None

        if fb_form_gen:
            # Функция обработки инструмента
            def fb_form_gen_tool():
                # Определить ресурс
                res = self.getMyRes()
                # Генерация имени файла по умолчанию
                fbp_base_filename = list(res.values())[0]['name'].lower() + '_frm_proto.fbp'
                # Выбор имени файла проекта
                fbp_dir = ic_dlg.icDirDlg(self.getPrjTreeCtrl(),
                                          u'Выбор файла папки хранения проекта wxFormBuilder для генерации',
                                          default_path=self.getPath())
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
                func = ext_tools[i_select]['function']
                func()
        else:
            log.warning(u'Не предусмотрены дополнительные инструменты для ресурса <%s>' % self.getResName())

    def create(self, new_name=None):
        """
        Функция создания ресурса.
        @param new_name: Указание нового имени созданного узла.
        """
        default_name = new_name if new_name else self.name
        new_name, res = new_metadata_resource_dlg.new_metadata_resource_dlg(parent=self.getPrjTreeCtrl(),
                                                                            default_resource_name=default_name)
        if new_name is None and res is None:
            # Нажата ОТМЕНА
            return False

        if res:
            self.template = res

        # Создать
        return icPrjResource.create(self, new_name=new_name)
