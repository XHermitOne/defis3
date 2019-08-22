#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса управления ресурсом проекта.

Описание ресурсного файла проекта информационной системы:

<имя файла> :=   *.pro 
<описание проекта информационной системы> =
[
{<описание проекта текущей информационной системы>},
{<описание проекта импортируемой информационной системы 1> }, Е ,
{ <описание проекта импортируемой информационной системы N> }
] //список

<описание проекта текущей информационной системы> =
{ 
 'имя корневой папки проекта'     : <значение папки> ,
 '__py__' : <имя корневого пакета модулей питона, создаваемых в рамках текущего проекта>
'__ftl__' : <значение папки шаблонов форм>
'__mth__' : <значение папки методов>
'__env__' : <словарь дополнительных глобальных атрибутов проекта>
} // словарь

<значение папки> = 
[
{'имя папки':<значение папки> / <тип ресурса> значения: 'tab' / 'var' / 'win' / 'mnu' / 'svb' / 'frm ' / 'src'}, Е {} 
] //список словарей

<значение папки шаблонов форм> =
[
{'имя папки' : <значение папки> / <тип ресурса> значения: 'ftl'}, Е {} 
] //список словарей

<значение папки методов> =
[
{'имя папки' : <значение папки> / <тип ресурса> значения: 'mth'}, Е {}
] //список словарей

<описание проекта импортируемой информационной системы> = 
{  'имя корневой папки проекта'     : <значение папки> }                                   // словарь

<значение папки> =
{
'type':  <тип импортируемой информационной системы>
'name':  <имя импортируемой информационной системы>
 '__py__':  <имя корневого пакета модулей питона, созданных в импортируемой информационной системе>
'link':  <тип связи импортируемой информационной системы: определим тип связи  импортируемой системы как ССЫЛКА, если информационные ресурсы импортируемой системы расположены НЕ в директории информационных ресурсов текущей системы; определим тип связи  импортируемой системы как КОПИЯ, если информационные ресурсы импортируемой системы расположены в директории информационных ресурсов текущей системы; 1 - ССЫЛКА, 0 - КОПИЯ>
'path':  <путь к файлу *.pro, содержащему описание структуры импортируемой информационной системы; если link=1, то указан полный путь, он дополняется значением ключа __py__ и используется при сборке, если link=0, то при сборке значение этого ключа не используется, а используется ключ __py__ для получения пути для сборки ресурсов>
}

Пример текущей информационной системы:
{'__py__':'icmodule','бухучет': 
    [ { 'базы данных': 
           [{'первичные документы':
                                  [{'приходные':[{'ордер1':'tab'},{'фактура1':'tab'},{'счет-фактура1':'tab'}]},
                                   {'расходные':[{'ордер2':'tab'},{'фактура2':'tab'},{'счет-фактура2':'tab'}]}
                                  ] 
             },
             {'прочие':[{}, Е {}]}
           ]
        },
        {'переменные':[{},Е{}]}
    ]
}

<словарь дополнительных глобальных атрибутов проекта> =
{
'имя переменной' : <значение переменной хранимого типа>
}

Переменные и значения попадают в окружение проекта автоматически.
"""

# Подключение библиотек
import re
import os.path
import wx

from ic.dlg import dlgfunc
from ic.log import log

from ic.interfaces import resManager
from ic.utils import util
from ic.utils import ic_res
import ic

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

# Константы

DEFAULT_PRJ_NAME = 'new_prj'

# Типы ресурсов ('tab','var','win','mnu','svb','frm')


class icPrjRes(resManager.icResourceManagerInterface):
    """
    Класс управления ресурсом проекта.
    """

    def __init__(self):
        """
        Конструктор.
        """
        resManager.icResourceManagerInterface.__init__(self)

        # Файл проекта
        self.prj_file_name = None

        # Структура проекта
        self._prj = []

    def setResFileName(self, res_filename=None):
        self.prj_file_name = res_filename

    def newPrj(self, prj_name, py_pack=None, prj_template=None):
        """
        Создание нового проекта по умолчанию.
        @param prj_name: Имя проекта.
        @param py_pack: Макет модулей питона.
        @param prj_template: Шаблон для создания проекта.
        """
        # Файл проекта
        prj_res = {}
        if prj_template is None:
            prj_template = self._newPrjTemplate()
        prj_res[prj_name] = prj_template
        prj_res['__py__'] = py_pack
        prj_res['__env__'] = {'AutoLogin': 'admin',
                              'AutoPassword': '',
                              'db_auth': '0',
                              'db_engine': 'PostgreSQLDB',
                              'convert_unicode': 'UTF-8',
                              'dbname': None,
                              'host': '127.0.0.1',
                              'user': 'admin',
                              'sys_table_name': 'resource_tab',
                              'password': '',
                              'port': '5432',
                              'dbstore': '.acc',
                              }
        # Добавить в основную структуру
        self._prj = [prj_res]
        return prj_res

    def _newPrjTemplate(self):
        """
        Шаблон нового проекта по умолчанию.
        """
        return [{'DB': []},
                {'Tables': []},
                {'Menu': []},
                {'System': []},
                {'Forms': []},
                {'Metadata': []},
                ]
        
    def openPrj(self, prj_filename):
        """
        Открыть файл проекта.
        """
        path, name = os.path.split(prj_filename)
        ic.set_ini_file(path)
        self.prj_file_name = prj_filename
        if os.path.isfile(self.prj_file_name) and os.path.exists(self.prj_file_name):
            prj = util.readAndEvalFile(self.prj_file_name, bRefresh=True)
            self._prj = self._prepareDataPrj(prj)

    # Один метод под двумя именами
    load = openPrj

    def savePrj(self):
        """
        Сохранить проект.
        """
        if not self.prj_file_name:
            self.prj_file_name = dlgfunc.getFileDlg(None, u'Создание проекта',
                                                  u'Project file (*.pro)|*.pro')
        if self.prj_file_name:
            prj_path = os.path.dirname(self.prj_file_name.strip())
            if (not os.path.isdir(prj_path)) or \
               (not self._prj[0]['__py__']):
                # Если директории проекта не существует, то
                # сохранить ее в __py__
                self._prj[0]['__py__'] = prj_path
            return self._save_prj(self.prj_file_name.strip(), self._prepareDataPrj(self._prj))
        return False    

    # Один метод под двумя именами
    save = savePrj

    def _prepareDataPrj(self, project):
        """
        Подготовка данных проекта для записи/чтения.
        """
        if isinstance(project, dict):
            project = dict([(key.strip(), self._prepareDataPrj(value)) for key, value in project.items()])
        elif isinstance(project, list):
            project = [self._prepareDataPrj(value) for value in project]
        elif isinstance(project, tuple):
            project = tuple([self._prepareDataPrj(value) for value in project])
        elif isinstance(project, str):
            project = project.strip()
        return project

    def _save_prj(self, prj_filename, project=None):
        """
        Непосредственное сохранение проекта.
        @param prj_filename: Имя файла проекта.
        @param project: Структура проекта.
        @return: Возвращает результат выполнения True/False.
        """
        if project is None:
            project = self._prepareDataPrj(self._prj)
        ok = ic_res.SaveResourceText(prj_filename.strip(), project)
        # Кроме того, что сохраняем проект, еще делаем его пакетом
        ic_res.CreateInitFile(os.path.dirname(prj_filename.strip()))
        return ok

    def getPrjRes(self):
        return self._prj

    def addFolder(self, new_folder_name, dst_folder_name, cur_folder=None):
        """
        Добавить папку.
        @param new_folder_name: Имя новой папки.
        @param dst_folder_name: Имя папки или проекта,
            в которую будет добавляться новая папка.
        @param cur_folder: Текущая папка,  если None,
            то берется папка проекта.
        @return: Результат добавления True|False.
        """
        if cur_folder is None:
            cur_folder = self.getPrjRoot()
        # Если имя папки==имя проекта, то просто добавить
        # папку в проект
        if dst_folder_name == self.getPrjRootName():
            self.getPrjRoot().append({new_folder_name: []})
            return True
            
        ok = False
        for folder in cur_folder:
            folder_name = list(folder.keys())[0]
            # Проверять только папки
            if isinstance(folder[folder_name], list):
                if folder_name == dst_folder_name:
                    folder[folder_name].append({new_folder_name: []})
                    ok = True
                    return ok
                else:
                    add = self.addFolder(new_folder_name, dst_folder_name, folder[folder_name])
                    if add:
                        return add
        return ok

    def addRes(self, new_res_name, res_type, dst_folder_name, cur_folder=None):
        """
        Добавить ресурс.
        @param new_res_name: Имя нового ресурса.
        @param res_type: Тип ресурса ('tab','var','win','mnu','svb','frm').
        @param dst_folder_name: Имя папки или проекта,
            в которую будет добавляться новая папка.
        @param cur_folder: Текущая папка,  если None,
            то берется папка проекта.
        @return: Результат добавления True|False.
        """
        if cur_folder is None:
            cur_folder = self.getPrjRoot()
        ok = False
        for folder in cur_folder:
            folder_name = list(folder.keys())[0]
            # Проверять только папки
            if isinstance(folder[folder_name], list):
                if folder_name == dst_folder_name:
                    folder[folder_name].append({new_res_name: res_type})
                    return True
                else:
                    add = self.addRes(new_res_name, res_type, dst_folder_name, folder[folder_name])
                    if add:
                        return add
        return ok

    def delFolder(self, del_folder_name, cur_folder=None):
        """
        Удалить папку с именем.
        @param del_folder_name: Имя удаляемой папки.
        @param cur_folder: Текущая папка,  если None,
            то берется папка проекта.
        @return: True-успешное удаление. False-не удален.
        """
        if cur_folder is None:
            cur_folder = self.getPrjRoot()
        del_ok = False
        for i_folder in range(len(cur_folder)):
            folder = cur_folder[i_folder]
            folder_name = list(folder.keys())[0]
            # Проверять только папки
            if isinstance(folder[folder_name], list):
                if folder_name == del_folder_name:
                    del cur_folder[i_folder]
                    return True
                else:
                    delete_ok = self.delFolder(del_folder_name, folder[folder_name])
                    if delete_ok:
                        return delete_ok
        return del_ok

    def getFolder(self, folder_name, cur_folder=None):
        """
        Взять папку с именем.
        @param folder_name: Имя папки.
        @param cur_folder: Текущая папка,  если None,
            то берется папка проекта.
        @return: Список папки в ресурсе проекта.
        """
        if cur_folder is None:
            cur_folder = self.getPrjRoot()
        for i_folder in range(len(cur_folder)):
            folder = cur_folder[i_folder]
            cur_folder_name = list(folder.keys())[0]
            # Проверять только папки
            if isinstance(folder[cur_folder_name], list):
                if cur_folder_name == folder_name:
                    return cur_folder[i_folder]
                else:
                    find_fld = self.getFolder(folder_name, folder[cur_folder_name])
                    if find_fld is not None:
                        return find_fld
        return None

    def getFolderBody(self, folder_name, cur_folder=None):
        """
        Взять содержимое папки с именем.
        @param folder_name: Имя папки.
        @param cur_folder: Текущая папка,  если None,
            то берется папка проекта.
        @return: Список папки в ресурсе проекта.
        """
        if cur_folder is None:
            cur_folder = self.getPrjRoot()
        for i_folder in range(len(cur_folder)):
            folder = cur_folder[i_folder]
            cur_folder_name = list(folder.keys())[0]
            # Проверять только папки
            if isinstance(folder[cur_folder_name], list):
                if cur_folder_name == folder_name:
                    return cur_folder[i_folder][folder_name]
                else:
                    find_fld = self.getFolderBody(folder_name, folder[cur_folder_name])
                    if find_fld is not None:
                        return find_fld
        return None

    def delRes(self, res_name, res_type=None, cur_folder=None):
        """
        Удалить ресурс по имени и типу.
        @param res_name: Имя ресурса.
        @param res_type: Тип ресурса, если None,
            то проверка на тип не производится.
        @param cur_folder: Текущая папка,  если None,
            то берется папка проекта.
        @return: True-успешное удаление. False-не удален.
        """
        if cur_folder is None:
            # Отсечь импортитруемые подсистемы
            cur_folder = self.getPrjRoot()
        del_ok = False
        for i_res in range(len(cur_folder)):
            res = cur_folder[i_res]
            cur_res_name = list(res.keys())[0]
            # Проверять только папки
            if isinstance(res[cur_res_name], list):
                find_res = self.delRes(res_name, res_type, res[cur_res_name])
                if find_res:
                    return find_res
            else:
                if cur_res_name == res_name and res[cur_res_name] == res_type:
                    del cur_folder[i_res]
                    return True
                elif cur_res_name == res_name and not res_type:
                    del cur_folder[i_res]
                    return True
        return del_ok

    def getResRef(self, res_name, res_type=None, cur_folder=None):
        """
        Получить кортеж указания ресурса по имени и типу.
        @param res_name: Имя ресурса.
        @param res_type: Тип ресурса, если None,
            то проверка на тип не производится.
        @param cur_folder: Текущая папка,  если None,
            то берется папка проекта.
        @return: Кортеж (Имя ресурса, тип ресурса) или None в случае ошибки.
        """
        if cur_folder is None:
            # Отсечь импортитруемые подсистемы
            cur_folder = self.getPrjRoot()
        ret_res = None
        for res in cur_folder:
            cur_res_name = list(res.keys())[0]
            # Проверять только папки
            if isinstance(res[cur_res_name], list):
                find_res = self.getResRef(res_name, res_type, res[cur_res_name])
                if find_res:
                    return find_res
            else:
                if cur_res_name == res_name and res[cur_res_name] == res_type:
                    return cur_res_name, res[cur_res_name]
                elif cur_res_name == res_name and res_type is None:
                    return cur_res_name, res[cur_res_name]

        if ret_res is None:
            log.warning(u'Не найден ресурс <%s.%s> %s' % (res_name, res_type, str(cur_folder)))
        return ret_res

    def getImportSystems(self):
        """
        Список импортируемых подсистем.
        """
        return self._prj[1:]

    def getPyPackage(self):
        """
        Пакет модулей питона текущего проекта.
        """
        return self._prj[0]['__py__']
        
    def getPrjRootName(self):
        """
        Имя корневой папки проекта.
        """
        root = self._prj[0]
        names = [key for key in root.keys() if not key.startswith('_')]
        return names[0]

    def setPrjRootName(self, new_prj_root_name):
        """
        Имя корневой папки проекта.
        """
        new_prj_root_name = new_prj_root_name
        root = self._prj[0]
        names = [key for key in root.keys() if not key.startswith('_')]
        old_prj_root_name = names[0]
        prj_root = root[old_prj_root_name]
        del self._prj[0][old_prj_root_name]
        self._prj[0][new_prj_root_name] = prj_root

    def getPrjRoot(self):
        """
        Корневая папка проекта.
        """
        if not self._prj:
            self.newPrj(DEFAULT_PRJ_NAME)
        return self._prj[0][self.getPrjRootName()]

    def getPyPackageImportSys(self, import_sys):
        """
        Пакет модулей питона импортироуемой системы.
        """
        return None

    def addPackage(self, package_path, new_package_name=None):
        """
        Добавить пакет модулей в дерево проектов.
        @param package_path: Путь пакета.
        @param new_package_name: Имя нового пакета.
        @return: Результат добавления True|False.
        """
        cur_package_path = package_path
        if new_package_name:
            cur_package_path = os.path.join(cur_package_path, new_package_name)
        return ic_res.CreateInitFile(cur_package_path)

    def addModule(self, module_name, package_path):
        """
        Добавить модуль в дерево проектов.
        @param module_name: Имя модуля.
        @param package_path: Путь пакета.
        """
        pass

    def renameRes(self, old_name, new_name, cur_folder=None):
        """
        Переименовать ресурс/папку.
        @param old_name: Старое имя.
        @param new_name: Новое имя.
        @param cur_folder: Текущая папка,  если None, 
            то берется папка проекта.
        @return: Возвращает результат выполнения переименования.
        """
        if cur_folder is None:
            # Отсечь импортитруемые подсистемы
            cur_folder = self.getPrjRoot()
        rename_res = False
        for i_res in range(len(cur_folder)):
            res = cur_folder[i_res]
            res_name = list(res.keys())[0]
            if res_name == old_name:
                cur_folder[i_res] = {new_name: res[res_name]}
                return True
            elif isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                rename_res = self.renameRes(old_name, new_name, res[res_name])
                if rename_res:
                    return rename_res
        return rename_res

    def newSubSys(self, subsys_name, subsys_prj_filename, py_pack):
        """
        Создать новую импортируемую подсистему.
        @param subsys_name: Имя импортируемой подсистемы.
        @param subsys_prj_filename: Файл импортируемой подсистемы.
        @param py_pack: Пакет импортируемой подсистмы.
        """
        imp_sys = {'name': subsys_name,
                   'type': 'icSubSys',
                   '__py__': py_pack,
                   'link': 0,
                   'path': subsys_prj_filename}
        # Добавить в проект
        self._prj.append(imp_sys)
        return imp_sys

    def isResORFolderByName(self, name, cur_folder=None):
        """
        Проверка, есть ли ресурс или папка с таким именем в проекте.
        @param name: Имя.
        @return: Возвращает результат операции True/False.
        """
        if cur_folder is None:
            # Отсечь импортитруемые подсистемы
            cur_folder = self.getPrjRoot()
        find = False
        for i_res in range(len(cur_folder)):
            res = cur_folder[i_res]
            res_name = list(res.keys())[0]
            if res_name == name:
                return True
            elif isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.isResORFolderByName(name, res[res_name])
                if find_folder:
                    return find_folder
        return find

    def isResByNameANDType(self, name, res_type=None, cur_folder=None):
        """
        Проверка, есть ли ресурс с таким именем и типом в проекте.
        @param name: Имя.
        @param res_type: Строковое определение типа ресурса 'tab','frm',...
            Если тип None, то проверка по типу не делается.
        @return: Возвращает результат операции True/False.
        """
        if cur_folder is None:
            # Отсечь импортитруемые подсистемы
            cur_folder = self.getPrjRoot()
        find = False
        for i_res in range(len(cur_folder)):
            res = cur_folder[i_res]
            cur_res_name = list(res.keys())[0]
            cur_res_type = res[cur_res_name]
            if isinstance(res[cur_res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.isResByNameANDType(name, res_type, res[cur_res_name])
                if find_folder:
                    return find_folder
            elif cur_res_name == name and cur_res_type == res_type:
                return True
            elif cur_res_name == name and res_type is None:
                return True
        return find

    def getResNameListByType(self, res_type, cur_folder=None):
        """
        Список имен ресурсов в проекте по их типу.
        @param res_type: Строковое определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен ресурсов заданного типа.
        """
        if cur_folder is None:
            # Отсечь импортитруемые подсистемы
            cur_folder = self.getPrjRoot()
        
        find_list = []
        for i_res in range(len(cur_folder)):
            res = cur_folder[i_res]
            cur_res_name = list(res.keys())[0]
            cur_res_type = res[cur_res_name]
            if isinstance(res[cur_res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.getResNameListByType(res_type, res[cur_res_name])
                if find_folder:
                    find_list += find_folder
            elif cur_res_type == res_type:
                find_list.append(cur_res_name)
        return find_list
        
    def getResNameListByTypes(self, res_types, cur_folder=None):
        """
        Список имен ресурсов в проекте по их типу.
        @param res_types: Кортеж строковых определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен ресурсов заданных типов.
        """
        if cur_folder is None:
            # Отсечь импортитруемые подсистемы
            cur_folder = self.getPrjRoot()
        
        find_list = []
        for i_res in range(len(cur_folder)):
            res = cur_folder[i_res]
            cur_res_name = list(res.keys())[0]
            cur_res_type = res[cur_res_name]
            if isinstance(res[cur_res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.getResNameListByTypes(res_types, res[cur_res_name])
                if find_folder:
                    find_list += find_folder
            elif cur_res_type in res_types:
                find_list.append(cur_res_name)
        return find_list
        
    def getResNamesByTypes(self, *res_types):
        """
        Список имен ресурсов в проекте по их типу.
        @param res_types: Кортеж строковых определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен ресурсов заданных типов.
        """
        return self.getResNameListByTypes(*res_types)
        
    def getResFileNamesByResPattern(self, res_pattern, cur_folder=None):
        """
        Список имен файлов ресурсов по шаблону ресурса.
        @param res_pattern: Кортеж строковых определений шаблонов ресурса '.*\.tab',...
        @return: Список имен файлов ресурсов по шаблону ресурса.
        """
        if cur_folder is None:
            # Отсечь импортитруемые подсистемы
            cur_folder = self.getPrjRoot()
        
        find_list = []
        for i_res in range(len(cur_folder)):
            res = cur_folder[i_res]
            res_name = list(res.keys())[0]
            res_type = res[res_name]
            if isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.getResFileNamesByResPattern(res_pattern, res[res_name])
                if find_folder:
                    find_list += find_folder
            else:
                res_file_name = u''
                try:
                    res_file_name = res_name+'.'+res_type
                    if [pattern for pattern in res_pattern if re.match(pattern, res_file_name)]:
                        # Если имя файла подходит под какойлибо шаблон,
                        # то добавитьв выходной список
                        find_list.append(res_file_name)
                except:
                    log.fatal(u'Ошибка поиска файла <%s> по шаблону <%s>' % (res_file_name, res_pattern))
        return find_list

    def getObjectsByResPattern(self, *res_pattern):
        """
        Получить список кортежей (тип объекта,имя объекта) по шаблону ресурса.
        @param res_pattern: Кортеж строковых определений шаблонов ресурса '.*\.tab',...
        @return: Список кортежей (тип объекта,имя объекта) по шаблону ресурса.
        """
        obj_list = []
        res_file_names = self.getResFileNamesByResPattern(res_pattern)
        prj_dir = os.path.dirname(self.prj_file_name)
        for res_file_name in res_file_names:
            full_res_file_name = os.path.join(prj_dir, res_file_name)
            spc = util.readAndEvalFile(full_res_file_name, bRefresh=True)
            obj = (spc['type'], spc['name'], spc['description'])
            obj_list.append(obj)
        return obj_list
        
    def getObjNamesByResPattern(self, *res_pattern):
        """
        Имена объектов по шаблону ресурсов.
        """
        return [obj[1] for obj in self.getObjectsByResPattern(*res_pattern)]
        
    def getObjectsInResByType(self, res_filename, obj_type, cur_obj=None):
        """
        Поиск объектов в ресурсе по типу.
        @param res_filename: Имя файла ресурса.
        @param OBjType_: Тип объекта, например 'icButton'.
        @return: Список кортежей формата:
            [('тип объекта','имя объекта','описание'),...]
        """
        if cur_obj is None:
            spc = util.readAndEvalFile(res_filename, bRefresh=True)
            cur_obj = spc[list(spc.keys())[0]]

        find_list = []
        try:
            if cur_obj is None:
                # Ресурс пустой
                return find_list
            if cur_obj['type'] == obj_type:
                find_list.append((cur_obj['type'], cur_obj['name'], cur_obj['description']))
            if 'child' in cur_obj and cur_obj['child']:
                for child in cur_obj['child']:
                    find_grp = self.getObjectsInResByType(res_filename, obj_type, child)
                    find_list += find_grp
        except:
            log.fatal(u'Search error in function getObjectsInResByType: %s, %s, %s' % (res_filename, obj_type, cur_obj))
        return find_list
        
    def getObjectsInResByTypes(self, res_filename, obj_types, cur_obj=None):
        """
        Поиск объектов в ресурсе по типу.
        @param res_filename: Имя файла ресурса.
        @param OBjTypes_: Кортеж типов объектов, например ('icButton',).
        @return: Список кортежей формата:
            [('тип объекта','имя объекта','описание'),...]
        """
        if cur_obj is None:
            spc = util.readAndEvalFile(res_filename, bRefresh=True)
            cur_obj = spc[list(spc.keys())[0]]

        find_list = []
        try:
            if cur_obj is None:
                # Ресурс пустой
                return find_list
            if cur_obj['type'] in obj_types:
                find_list.append((cur_obj['type'], cur_obj['name'], cur_obj['description']))
            if 'child' in cur_obj and cur_obj['child']:
                for child in cur_obj['child']:
                    find_grp = self.getObjectsInResByTypes(res_filename, obj_types, child)
                    find_list += find_grp
        except:
            log.fatal(u'Search error in function getObjectsInResByTypes: (%s, %s, %s)' % (res_filename,
                                                                                          obj_types, cur_obj))
        return find_list
        
    def getObjByResPatternANDType(self, res_pattern, obj_type):
        """
        Получить список кортежей (тип объекта,имя объекта) по шаблону ресурса и типу объекта.
        @param res_pattern: Кортеж строковых определений шаблонов ресурса '.*\.tab',...
        @param obj_type: Тип объекта. Например 'icButton'.
        @return: Список кортежей (тип объекта,имя объекта) по шаблону ресурса и типу объекта.
        """
        obj_list = []
        res_file_names = self.getResFileNamesByResPattern(res_pattern)
        prj_dir = os.path.dirname(self.prj_file_name)
        for res_file_name in res_file_names:
            full_res_file_name = os.path.join(prj_dir, res_file_name)
            obj_lst = self.getObjectsInResByType(full_res_file_name, obj_type)
            obj_list += obj_lst
        return obj_list
        
    def getObjByResPatternANDTypes(self, res_pattern, obj_types):
        """
        Получить список кортежей (тип объекта,имя объекта) по шаблону ресурса и типу объекта.
        @param res_pattern: Кортеж строковых определений шаблонов ресурса '.*\.tab',...
        @param obj_types: Кортеж типов объектов, например ('icButton',).
        @return: Список кортежей (тип объекта,имя объекта) по шаблону ресурса и типу объекта.
        """
        obj_list = []
        res_file_names = self.getResFileNamesByResPattern(res_pattern)
        prj_dir = os.path.dirname(self.prj_file_name)
        for res_file_name in res_file_names:
            full_res_file_name = os.path.join(prj_dir, res_file_name)
            obj_lst = self.getObjectsInResByTypes(full_res_file_name, obj_types)
            obj_list += obj_lst
        return obj_list
        
    def isModByName(self, module_name):
        """
        Проверить, есть ли модуль с таким именем.
        @param module_name: Имя модуля.
        @return: Возвращает результат операции True/False.
        """
        return False
        
    def isImpSubSys(self, name):
        """
        Проверить, является ли name именем импортируемой подсистемы.
        @param name: Имя некого ресурса.
        @return: Возвращает True/False.
        """
        return bool([sub_sys for sub_sys in self.getImportSystems() if sub_sys['name'] == name])

    def getImpSubSysIdx(self, name):
        """
        Возвращает индекс импортируемой подсистемы по имени.
        @param name: Имя подсистемы.
        @return: Индекс в структуре ресурсного файла импортируемой подсистемы
            с именем name или -1, если такая подсистема в описании не найдена.
        """
        find_idx = -1
        try:
            name_list = ['']+[sub_sys['name'] for sub_sys in self.getImportSystems()]
            find_idx = name_list.index(name)
        except ValueError:
            log.fatal()
            find_idx = -1
            
        return find_idx
        
    def delImpSubSys(self, name, bAutoSave=True):
        """
        Удалить из файла *.pro импортируемую подсистему по имени.
        @param name: Имя подсистемы.
        @param bAutoSave: Автоматически сохранить файл *.pro после удаления.
        @return: Возвращает True/False.
        """
        try:
            sub_sys_idx = self.getImpSubSysIdx(name)
            if sub_sys_idx > 0:
                del self._prj[sub_sys_idx]
            if bAutoSave:
                self.save()
            return True
        except:
            log.fatal()
            return False
        
    def getPrjEnv(self):
        """
        Получить словарь дополнительных атрибутов проекта.
        """
        if '__env__' in self._prj[0]:
            return self._prj[0]['__env__']
        return {}
    
    def setPrjEnv(self, env):
        """
        Установить словарь дополнительных атрибутов проекта.
        """
        self._prj[0]['__env__'] = env


def test():
    """
    Функция тестирования.
    """
    prj_res = icPrjRes()
    prj_res.newPrj('root', None, None, None)
    print(prj_res.getPrjRes())
    prj_res.addRes('tab1', 'tab', u'Формы')
    print(prj_res.getPrjRes())


if __name__ == '__main__':
    test()
