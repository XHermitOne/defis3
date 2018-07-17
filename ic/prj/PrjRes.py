#!/usr/bin/env python
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

from ic.dlg import ic_dlg
from ic.log import log

from ic.interfaces import resManager
from ic.utils import util
from ic.utils import ic_file
from ic.utils import ic_res
import ic

__version__ = (0, 0, 1, 1)

_ = wx.GetTranslation

# Константы

DEFAULT_PRJ_NAME = 'new_prj'

# Типы ресурсов ('tab','var','win','mnu','svb','frm')


class icPrjRes(resManager.ResourceManagerInterface):
    """
    Класс управления ресурсом проекта.
    """

    def __init__(self):
        """
        Конструктор.
        """
        resManager.ResourceManagerInterface.__init__(self)

        # Файл проекта
        self.prj_file_name = None

        # Структура проекта
        self._prj = []

    def setResFileName(self, ResFileName_=None):
        self.prj_file_name = ResFileName_

    def newPrj(self, PrjName_, PyPack_=None, PrjTemplate_=None):
        """
        Создание нового проекта по умолчанию.
        @param PrjName_: Имя проекта.
        @param PyPack_: Макет модулей питона.
        @param PrjTemplate_: Шаблон для создания проекта.
        """
        # Файл проекта
        prj_res = {}
        if PrjTemplate_ is None:
            PrjTemplate_ = self._newPrjTemplate()
        prj_res[PrjName_] = PrjTemplate_
        prj_res['__py__'] = PyPack_
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
        
    def openPrj(self, PrjFileName_):
        """
        Открыть файл проекта.
        """
        path, name = os.path.split(PrjFileName_)
        ic.set_ini_file(path)
        self.prj_file_name = PrjFileName_
        if ic_file.IsFile(self.prj_file_name) and \
           ic_file.Exists(self.prj_file_name):
            prj = util.readAndEvalFile(self.prj_file_name, bRefresh=True)
            self._prj = self._prepareDataPrj(prj)

    # Один метод под двумя именами
    load = openPrj

    def savePrj(self):
        """
        Сохранить проект.
        """
        if not self.prj_file_name:
            self.prj_file_name = ic_dlg.icFileDlg(None, u'Создание проекта',
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

    def _prepareDataPrj(self, Prj_):
        """
        Подготовка данных проекта для записи/чтения.
        """
        if isinstance(Prj_, dict):
            Prj_ = dict([(key.strip(), self._prepareDataPrj(value)) for key, value in Prj_.items()])
        elif isinstance(Prj_, list):
            Prj_ = [self._prepareDataPrj(value) for value in Prj_]
        elif isinstance(Prj_, tuple):
            Prj_ = tuple([self._prepareDataPrj(value) for value in Prj_])
        elif type(Prj_) in (str, unicode):
            Prj_ = Prj_.strip()
        return Prj_

    def _save_prj(self, PrjFileName_, Prj_=None):
        """
        Непосредственное сохранение проекта.
        @param PrjFileName_: Имя файла проекта.
        @param Prj_: Структура проекта.
        @return: Возвращает результат выполнения True/False.
        """
        if Prj_ is None:
            Prj_ = self._prepareDataPrj(self._prj)
        ok = ic_res.SaveResourcePickle(PrjFileName_.strip(), Prj_)
        # Кроме того, что сохраняем проект, еще делаем его пакетом
        ic_res.CreateInitFile(ic_file.DirName(PrjFileName_.strip()))
        return ok

    def getPrjRes(self):
        return self._prj

    def addFolder(self, NewFolderName_, FolderName_, CurFolder_=None):
        """
        Добавить папку.
        @param NewFolderName_: Имя новой папки.
        @param FolderName_: Имя папки или проекта,  
            в которую будет добавляться новая папка.
        @param CurFolder_: Текущая папка,  если None, 
            то берется папка проекта.
        @return: Результат добавления True|False.
        """
        if CurFolder_ is None:
            CurFolder_ = self.getPrjRoot()
        # Если имя папки==имя проекта, то просто добавить
        # папку в проект
        if FolderName_ == self.getPrjRootName() :
            self.getPrjRoot().append({NewFolderName_: []})
            return True
            
        ok=False
        for folder in CurFolder_:
            folder_name = folder.keys()[0]
            # Проверять только папки
            if isinstance(folder[folder_name], list):
                if folder_name == FolderName_:
                    folder[folder_name].append({NewFolderName_: []})
                    ok = True
                    return ok
                else:
                    add = self.addFolder(NewFolderName_, FolderName_, folder[folder_name])
                    if add:
                        return add
        return ok

    def addRes(self, NewResName_, ResType_, FolderName_, CurFolder_=None):
        """
        Добавить ресурс.
        @param NewResName_: Имя нового ресурса.
        @param ResType_: Тип ресурса ('tab','var','win','mnu','svb','frm').
        @param FolderName_: Имя папки или проекта,  
            в которую будет добавляться новая папка.
        @param CurFolder_: Текущая папка,  если None, 
            то берется папка проекта.
        @return: Результат добавления True|False.
        """
        if CurFolder_ is None:
            CurFolder_ = self.getPrjRoot()
        ok=False
        for folder in CurFolder_:
            folder_name = folder.keys()[0]
            # Проверять только папки
            if isinstance(folder[folder_name], list):
                if folder_name == FolderName_:
                    folder[folder_name].append({NewResName_: ResType_})
                    return True
                else:
                    add = self.addRes(NewResName_, ResType_, FolderName_, folder[folder_name])
                    if add:
                        return add
        return ok

    def delFolder(self, FolderName_, CurFolder_=None):
        """
        Удалить папку с именем.
        @param FolderName_: Имя удаляемой папки.
        @param CurFolder_: Текущая папка,  если None, 
            то берется папка проекта.
        @return: True-успешное удаление. False-не удален.
        """
        if CurFolder_ is None:
            CurFolder_ = self.getPrjRoot()
        del_ok = False
        for i_folder in range(len(CurFolder_)):
            folder = CurFolder_[i_folder]
            folder_name = folder.keys()[0]
            # Проверять только папки
            if isinstance(folder[folder_name], list):
                if folder_name == FolderName_:
                    del CurFolder_[i_folder]
                    return True
                else:
                    delete_ok = self.delFolder(FolderName_, folder[folder_name])
                    if delete_ok:
                        return delete_ok
        return del_ok

    def getFolder(self, FolderName_, CurFolder_=None):
        """
        Взять папку с именем.
        @param FolderName_: Имя папки.
        @param CurFolder_: Текущая папка,  если None, 
            то берется папка проекта.
        @return: Список папки в ресурсе проекта.
        """
        if CurFolder_ is None:
            CurFolder_ = self.getPrjRoot()
        for i_folder in range(len(CurFolder_)):
            folder = CurFolder_[i_folder]
            folder_name = folder.keys()[0]
            # Проверять только папки
            if isinstance(folder[folder_name], list):
                if folder_name == FolderName_:
                    return CurFolder_[i_folder]
                else:
                    find_fld = self.getFolder(FolderName_, folder[folder_name])
                    if find_fld is not None:
                        return find_fld
        return None

    def getFolderBody(self, FolderName_, CurFolder_=None):
        """
        Взять содержимое папки с именем.
        @param FolderName_: Имя папки.
        @param CurFolder_: Текущая папка,  если None, 
            то берется папка проекта.
        @return: Список папки в ресурсе проекта.
        """
        if CurFolder_ is None:
            CurFolder_ = self.getPrjRoot()
        for i_folder in range(len(CurFolder_)):
            folder = CurFolder_[i_folder]
            folder_name = folder.keys()[0]
            # Проверять только папки
            if isinstance(folder[folder_name], list):
                if folder_name == FolderName_:
                    return CurFolder_[i_folder][FolderName_]
                else:
                    find_fld = self.getFolderBody(FolderName_, folder[folder_name])
                    if find_fld is not None:
                        return find_fld
        return None

    def delRes(self, ResName_, ResType_=None, CurFolder_=None):
        """
        Удалить ресурс по имени и типу.
        @param ResName_: Имя ресурса.
        @param ResType_: Тип ресурса, если None, 
            то проверка на тип не производится.
        @param CurFolder_: Текущая папка,  если None, 
            то берется папка проекта.
        @return: True-успешное удаление. False-не удален.
        """
        if CurFolder_ is None:
            # Отсечь импортитруемые подсистемы
            CurFolder_ = self.getPrjRoot()
        del_ok = False
        for i_res in range(len(CurFolder_)):
            res = CurFolder_[i_res]
            res_name = res.keys()[0]
            # Проверять только папки
            if isinstance(res[res_name], list):
                find_res = self.delRes(ResName_, ResType_, res[res_name])
                if find_res:
                    return find_res
            else:
                if res_name == ResName_ and res[res_name] == ResType_:
                    del CurFolder_[i_res]
                    return True
                elif res_name == ResName_ and not ResType_:
                    del CurFolder_[i_res]
                    return True
        return del_ok

    def getResRef(self, ResName_, ResType_=None, CurFolder_=None):
        """
        Получить кортеж указания ресурса по имени и типу.
        @param ResName_: Имя ресурса.
        @param ResType_: Тип ресурса, если None, 
            то проверка на тип не производится.
        @param CurFolder_: Текущая папка,  если None, 
            то берется папка проекта.
        @return: Кортеж (Имя ресурса, тип ресурса) или None в случае ошибки.
        """
        if CurFolder_ is None:
            # Отсечь импортитруемые подсистемы
            CurFolder_ = self.getPrjRoot()
        ret_res = None
        for res in CurFolder_:
            res_name = res.keys()[0]
            # Проверять только папки
            if isinstance(res[res_name], list):
                find_res = self.getResRef(ResName_, ResType_, res[res_name])
                if find_res:
                    return find_res
            else:
                if res_name == ResName_ and res[res_name] == ResType_:
                    return res_name, res[res_name]
                elif res_name == ResName_ and ResType_ == None:
                    return res_name, res[res_name]
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
        return filter(lambda key: key[0] != '_', root.keys())[0]

    def setPrjRootName(self, NewPrjRootName_):
        """
        Имя корневой папки проекта.
        """
        NewPrjRootName_ = NewPrjRootName_
        root = self._prj[0]
        old_prj_root_name = filter(lambda key: key[0] != '_', root.keys())[0]
        prj_root = root[old_prj_root_name]
        del self._prj[0][old_prj_root_name]
        self._prj[0][NewPrjRootName_] = prj_root

    def getPrjRoot(self):
        """
        Корневая папкя проекта.
        """
        if not self._prj:
            self.newPrj(DEFAULT_PRJ_NAME)
        return self._prj[0][self.getPrjRootName()]

    def getPyPackageImportSys(self, ImportSys_):
        """
        Пакет модулей питона импортироуемой системы.
        """
        return None

    def addPackage(self, PackagePath_, NewPackageName_=None):
        """
        Добавить пакет модулей в дерево проектов.
        @param PackagePath_: Путь пакета.
        @param NewPackageName_: Имя нового пакета.
        @return: Результат добавления True|False.
        """
        package_path = PackagePath_
        if NewPackageName_:
            package_path += '/'+NewPackageName_
        return ic_res.CreateInitFile(package_path)

    def addModule(self, ModuleName_, PackagePath_):
        """
        Добавить модуль в дерево проектов.
        @param ModuleName_: Имя модуля.
        @param PackagePath_: Путь пакета.
        """
        pass

    def renameRes(self, OldName_, NewName_, CurFolder_=None):
        """
        Переименовать ресурс/папку.
        @param OldName_: Старое имя.
        @param NewName_: Новое имя.
        @param CurFolder_: Текущая папка,  если None, 
            то берется папка проекта.
        @return: Возвращает результат выполнения переименования.
        """
        if CurFolder_ is None:
            # Отсечь импортитруемые подсистемы
            CurFolder_ = self.getPrjRoot()
        rename_res = False
        for i_res in range(len(CurFolder_)):
            res = CurFolder_[i_res]
            res_name = res.keys()[0]
            if res_name == OldName_:
                CurFolder_[i_res] = {NewName_: res[res_name]}
                return True
            elif isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                rename_res = self.renameRes(OldName_, NewName_, res[res_name])
                if rename_res:
                    return rename_res
        return rename_res

    def newSubSys(self, SubSysName_, SubSysPrjFile_, PyPack_):
        """
        Создать новую импортируемую подсистему.
        @param SubSysName_: Имя импортируемой подсистемы.
        @param SubSysPrjFile_: Файл импортируемой подсистемы.
        @param PyPack_: Пакет импортируемой подсистмы.
        """
        imp_sys = {'name': SubSysName_,
                   'type': 'icSubSys',
                   '__py__': PyPack_,
                   'link': 0,
                   'path': SubSysPrjFile_}
        # Добавить в проект
        self._prj.append(imp_sys)
        return imp_sys

    def isResORFolderByName(self, Name_, CurFolder_=None):
        """
        Проверка, есть ли ресурс или папка с таким именем в проекте.
        @param Name_: Имя.
        @return: Возвращает результат операции True/False.
        """
        if CurFolder_ is None:
            # Отсечь импортитруемые подсистемы
            CurFolder_ = self.getPrjRoot()
        find = False
        for i_res in range(len(CurFolder_)):
            res = CurFolder_[i_res]
            res_name = res.keys()[0]
            if res_name == Name_:
                return True
            elif isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.isResORFolderByName(Name_, res[res_name])
                if find_folder:
                    return find_folder
        return find

    def isResByNameANDType(self, Name_, Type_=None, CurFolder_=None):
        """
        Проверка, есть ли ресурс с таким именем и типом в проекте.
        @param Name_: Имя.
        @param Type_: Строковое определение типа ресурса 'tab','frm',...
            Если тип None, то проверка по типу не делается.
        @return: Возвращает результат операции True/False.
        """
        if CurFolder_ is None:
            # Отсечь импортитруемые подсистемы
            CurFolder_ = self.getPrjRoot()
        find = False
        for i_res in range(len(CurFolder_)):
            res = CurFolder_[i_res]
            res_name = res.keys()[0]
            res_type = res[res_name]
            if isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.isResByNameANDType(Name_, Type_, res[res_name])
                if find_folder:
                    return find_folder
            elif res_name == Name_ and res_type == Type_:
                return True
            elif res_name == Name_ and Type_ is None:
                return True
        return find

    def getResNameListByType(self, Type_, CurFolder_=None):
        """
        Список имен ресурсов в проекте по их типу.
        @param Type_: Строковое определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен ресурсов заданного типа.
        """
        if CurFolder_ is None:
            # Отсечь импортитруемые подсистемы
            CurFolder_ = self.getPrjRoot()
        
        find_list = []
        for i_res in range(len(CurFolder_)):
            res = CurFolder_[i_res]
            res_name = res.keys()[0]
            res_type = res[res_name]
            if isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.getResNameListByType(Type_, res[res_name])
                if find_folder:
                    find_list += find_folder
            elif res_type == Type_:
                find_list.append(res_name)
        return find_list
        
    def getResNameListByTypes(self, Types_, CurFolder_=None):
        """
        Список имен ресурсов в проекте по их типу.
        @param Types_: Кортеж строковых определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен ресурсов заданных типов.
        """
        if CurFolder_ is None:
            # Отсечь импортитруемые подсистемы
            CurFolder_ = self.getPrjRoot()
        
        find_list = []
        for i_res in range(len(CurFolder_)):
            res = CurFolder_[i_res]
            res_name = res.keys()[0]
            res_type = res[res_name]
            if isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.getResNameListByTypes(Types_, res[res_name])
                if find_folder:
                    find_list += find_folder
            elif res_type in Types_:
                find_list.append(res_name)
        return find_list
        
    def getResNamesByTypes(self, *Types_):
        """
        Список имен ресурсов в проекте по их типу.
        @param Types_: Кортеж строковых определение типа ресурса 'tab','frm',...
        @return: Возвращает список имен ресурсов заданных типов.
        """
        return self.getResNameListByTypes(*Types_)
        
    def getResFileNamesByResPattern(self, ResPattern_, CurFolder_=None):
        """
        Список имен файлов ресурсов по шаблону ресурса.
        @param ResPattern_: Кортеж строковых определений шаблонов ресурса '.*\.tab',...
        @return: Список имен файлов ресурсов по шаблону ресурса.
        """
        if CurFolder_ is None:
            # Отсечь импортитруемые подсистемы
            CurFolder_ = self.getPrjRoot()
        
        find_list = []
        for i_res in range(len(CurFolder_)):
            res = CurFolder_[i_res]
            res_name = res.keys()[0]
            res_type = res[res_name]
            if isinstance(res[res_name], list):
                # Если это папка, то обработать все подпапки
                find_folder = self.getResFileNamesByResPattern(ResPattern_, res[res_name])
                if find_folder:
                    find_list += find_folder
            else:
                try:
                    res_file_name=res_name+'.'+res_type
                    if [pattern for pattern in ResPattern_ if re.match(pattern, res_file_name)]:
                        # Если имя файла подходит под какойлибо шаблон,
                        # то добавитьв выходной список
                        find_list.append(res_file_name)
                except:
                    log.fatal(u'File <%s> is not found by template <%s>' % (res_file_name, ResPattern_))
        return find_list

    def getObjectsByResPattern(self, *ResPattern_):
        """
        Получить список кортежей (тип объекта,имя объекта) по шаблону ресурса.
        @param ResPattern_: Кортеж строковых определений шаблонов ресурса '.*\.tab',...
        @return: Список кортежей (тип объекта,имя объекта) по шаблону ресурса.
        """
        obj_list = []
        res_file_names = self.getResFileNamesByResPattern(ResPattern_)
        prj_dir = os.path.dirname(self.prj_file_name)
        for res_file_name in res_file_names:
            full_res_file_name = prj_dir+'/'+res_file_name
            spc = util.readAndEvalFile(full_res_file_name, bRefresh=True)
            obj = (spc['type'], spc['name'], spc['description'])
            obj_list.append(obj)
        return obj_list
        
    def getObjNamesByResPattern(self, *ResPattern_):
        """
        Имена объектов по шаблону ресурсов.
        """
        return [obj[1] for obj in self.getObjectsByResPattern(*ResPattern_)]
        
    def getObjectsInResByType(self, ResFileName_, ObjType_, CurObj_=None):
        """
        Поиск объектов в ресурсе по типу.
        @param ResFileName_: Имя файла ресурса.
        @param OBjType_: Тип объекта, например 'icButton'.
        @return: Список кортежей формата:
            [('тип объекта','имя объекта','описание'),...]
        """
        if CurObj_ is None:
            spc = util.readAndEvalFile(ResFileName_, bRefresh=True)
            CurObj_ = spc[spc.keys()[0]]

        find_list = []
        try:
            if CurObj_ is None:
                # Ресурс пустой
                return find_list
            if CurObj_['type'] == ObjType_:
                find_list.append((CurObj_['type'], CurObj_['name'], CurObj_['description']))
            if 'child' in CurObj_ and CurObj_['child']:
                for child in CurObj_['child']:
                    find_grp = self.getObjectsInResByType(ResFileName_, ObjType_, child)
                    find_list += find_grp
        except:
            log.fatal(u'Search error in function getObjectsInResByType: %s, %s, %s' % (ResFileName_, ObjType_, CurObj_))
        return find_list
        
    def getObjectsInResByTypes(self, ResFileName_, ObjTypes_, CurObj_=None):
        """
        Поиск объектов в ресурсе по типу.
        @param ResFileName_: Имя файла ресурса.
        @param OBjTypes_: Кортеж типов объектов, например ('icButton',).
        @return: Список кортежей формата:
            [('тип объекта','имя объекта','описание'),...]
        """
        if CurObj_ is None:
            spc = util.readAndEvalFile(ResFileName_, bRefresh=True)
            CurObj_ = spc[spc.keys()[0]]

        find_list = []
        try:
            if CurObj_ is None:
                # Ресурс пустой
                return find_list
            if CurObj_['type'] in ObjTypes_:
                find_list.append((CurObj_['type'], CurObj_['name'], CurObj_['description']))
            if 'child' in CurObj_ and CurObj_['child']:
                for child in CurObj_['child']:
                    find_grp = self.getObjectsInResByTypes(ResFileName_, ObjTypes_, child)
                    find_list += find_grp
        except:
            log.fatal(u'Search error in function getObjectsInResByTypes: (%s, %s, %s)' % (ResFileName_,
                                                                                              ObjTypes_, CurObj_))
        return find_list
        
    def getObjByResPatternANDType(self, ResPattern_, ObjType_):
        """
        Получить список кортежей (тип объекта,имя объекта) по шаблону ресурса и типу объекта.
        @param ResPattern_: Кортеж строковых определений шаблонов ресурса '.*\.tab',...
        @param ObjType_: Тип объекта. Например 'icButton'.
        @return: Список кортежей (тип объекта,имя объекта) по шаблону ресурса и типу объекта.
        """
        obj_list = []
        res_file_names = self.getResFileNamesByResPattern(ResPattern_)
        prj_dir = os.path.dirname(self.prj_file_name)
        for res_file_name in res_file_names:
            full_res_file_name = prj_dir+'/'+res_file_name
            obj_lst = self.getObjectsInResByType(full_res_file_name, ObjType_)
            obj_list += obj_lst
        return obj_list
        
    def getObjByResPatternANDTypes(self, ResPattern_, ObjTypes_):
        """
        Получить список кортежей (тип объекта,имя объекта) по шаблону ресурса и типу объекта.
        @param ResPattern_: Кортеж строковых определений шаблонов ресурса '.*\.tab',...
        @param OBjTypes_: Кортеж типов объектов, например ('icButton',).
        @return: Список кортежей (тип объекта,имя объекта) по шаблону ресурса и типу объекта.
        """
        obj_list = []
        res_file_names = self.getResFileNamesByResPattern(ResPattern_)
        prj_dir = os.path.dirname(self.prj_file_name)
        for res_file_name in res_file_names:
            full_res_file_name = prj_dir+'/'+res_file_name
            obj_lst = self.getObjectsInResByTypes(full_res_file_name, ObjTypes_)
            obj_list += obj_lst
        return obj_list
        
    def isModByName(self, ModuleName_):
        """
        Проверить, есть ли модуль с таким именем.
        @param ModuleName_: Имя модуля.
        @return: Возвращает результат операции True/False.
        """
        return False
        
    def isImpSubSys(self, Name_):
        """
        Проверить, является ли Name_ именем импортируемой подсистемы.
        @param Name_: Имя некого ресурса.
        @return: Возвращает True/False.
        """
        return bool([sub_sys for sub_sys in self.getImportSystems() if sub_sys['name'] == Name_])

    def getImpSubSysIdx(self, Name_):
        """
        Возвращает индекс импортируемой подсистемы по имени.
        @param Name_: Имя подсистемы.
        @return: Индекс в структуре ресурсного файла импортируемой подсистемы
            с именем Name_ или -1, если такая подсистема в описании не найдена.
        """
        find_idx = -1
        try:
            name_list = ['']+[sub_sys['name'] for sub_sys in self.getImportSystems()]
            find_idx = name_list.index(Name_)
        except ValueError:
            log.fatal()
            find_idx = -1
            
        return find_idx
        
    def delImpSubSys(self, Name_, AutoSave_=True):
        """
        Удалить из файла *.pro импортируемую подсистему по имени.
        @param Name_: Имя подсистемы.
        @param AutoSave_: Автоматически сохранить файл *.pro после удаления.
        @return: Возвращает True/False.
        """
        try:
            sub_sys_idx = self.getImpSubSysIdx(Name_)
            if sub_sys_idx > 0:
                del self._prj[sub_sys_idx]
            if AutoSave_:
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
    
    def setPrjEnv(self, Env_):
        """
        Установить словарь дополнительных атрибутов проекта.
        """
        self._prj[0]['__env__'] = Env_


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
