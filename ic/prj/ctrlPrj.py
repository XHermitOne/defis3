#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль классов управления ресурсами проекта из скриптов.

Компонент управления ресурсами проекта работает только
с определенной папкой в проекте.
Папка проекта называется 'Другие'
Если такой папки нет, то она создается.
Компонент управления ресурсами не может работать
с другими папками проекта и не управляет 
другими ресурсами.
"""

# --- Подключение библиотек ---
import os
import os.path
import wx
import copy

from ic.log import log
from ic.utils import ic_file
from ic.utils import util
from ic.utils import resource
from ic.engine import ic_user
from . import PrjRes

_ = wx.GetTranslation

__version__ = (0, 0, 1, 1)

# --- константы ---
OTHER_PRJ_FOLDER_NAME = u'Дополнительно'


# --- Описание классов ---
class icProjectResController:
    """
    Класс управления ресурсами проекта.
    """

    def __init__(self, PrjName_=None, PrjResFileName_=None):
        """
        Конструктор.
        @param PrjName_: Имя проекта.
        @param PrjResFileName_: Имя файла ресурса проекта.
        """
        self.setPrj(PrjName_, PrjResFileName_)
        # Объект управления ресурсом проекта
        self._PrjRes = PrjRes.icPrjRes()
        
    def saveRes(self, ResName_, ResType_, Resource_):
        """
        Записать ресурс в проект.
        @param ResName_: Имя ресурса.
        @param ResType_: Тип ресурса.
        @param Resource_: Сам, записываемый ресурс.
        """
        self.makeFolderOther()
        if self._PrjRes:
            if not self._PrjRes.isResByNameANDType(ResName_, ResType_,
                                                   self._PrjRes.getFolderBody(OTHER_PRJ_FOLDER_NAME)):
                self._PrjRes.addRes(ResName_, ResType_,
                                    OTHER_PRJ_FOLDER_NAME)
                self._PrjRes.savePrj()
                    
        return resource.icSaveRes(ResName_, ResType_,
                                  nameRes=ResName_, resData=Resource_, ResFmt=1)

    def loadRes(self, ResName_, ResType_=None):
        """
        Прочитать ресурс из проекта.
        @param ResName_: Имя загружаемого ресурса.
        @param ResType_: Тип ресурса.
        @return: Содержимое ресурса или None в случае ошибки.
        """
        self.makeFolderOther()
        if self._PrjRes:
            res_ref = self._PrjRes.getResRef(ResName_, ResType_,
                                             self._PrjRes.getFolderBody(OTHER_PRJ_FOLDER_NAME))
            return self._loadResFile(*res_ref)
        return None

    def loadResClone(self, ResName_, ResType_=None):
        """
        Прочитать ресурс из проекта для его последующего клонирования.
        @param ResName_: Имя загружаемого ресурса.
        @param ResType_: Тип ресурса.
        @return: Содержимое ресурса или None в случае ошибки.
        """
        if self._PrjRes:
            res_ref = self._PrjRes.getResRef(ResName_, ResType_)
            return self._loadResFile(*res_ref)
        return None
        
    def _loadResFile(self, ResName_, ResType_):
        """
        Открыть и загрузить файл ресурса.
        @return: Содержимое ресурса или None в случае ошибки.
        """
        res_file_name = os.path.join(self._PrjResDir, '%s.%s' % (ResName_, ResType_))
        if ic_file.IsFile(res_file_name):
            res_file = util.readAndEvalFile(res_file_name)
            res = res_file[ResName_]
            return copy.deepcopy(res)
        return None
                
    def delRes(self, ResName_, ResType_):
        """
        Удалить ресурс из проекта.
        @param ResName_: Имя ресурса.
        @param ResType_: Тип ресурса.
        """
        self.makeFolderOther()
        if self._PrjRes:
            self._PrjRes.delRes(ResName_, ResType_)
            self._PrjRes.savePrj()
            
        res_file_name = self._PrjResDir+'/%s.%s' % (ResName_, ResType_)
        if ic_file.IsFile(res_file_name):
            ic_file.Remove(res_file_name)
            return True
        return False

    def isRes(self, ResName_, ResType_=None):
        """
        Проверка соществования ресурса с именем и типом в проекте.
        @param ResName_: Имя ресурса.
        @param ResType_: Тип ресурса.
        """
        if self._PrjRes:
            return self._PrjRes.isResByNameANDType(ResName_, ResType_)
        return False

    def getResourcesByType(self, res_type=None):
        """
        Получить список ресурсов по типу.
        @param res_type: Тип ресурса.
        @return: Список ресурсов указанного типа. В случае ошибки возвращается пустой список.
        """
        result = list()
        if res_type is None:
            log.warning(u'Не определен тип ресурса')
            return result

        if self._PrjRes:
            res_names = self._PrjRes.getResNameListByType(res_type)
            for res_name in res_names:
                res = self._loadResFile(res_name, res_type)
                result.append(res)
        else:
            log.warning(u'Не определен объект управления ресурсом проекта')
        return result

    def makeFolderOther(self):
        """
        Создать папку в проекте 'Другие' если ее нет в дереве проекта.
        """
        if self._PrjRes:
            # Если папки нет тогда добавить ее
            if not self._PrjRes.isResORFolderByName(OTHER_PRJ_FOLDER_NAME):
                self._PrjRes.addFolder(OTHER_PRJ_FOLDER_NAME,
                                       self._PrjRes.getPrjRootName())
                self._PrjRes.savePrj()

    def openPrj(self, PrjName_=None, PrjResFileName_=None):
        """
        Открыть проект.
        @param PrjName_: Имя проекта.
        @param PrjResFileName_: Имя файла ресурса проекта.
        """
        self.setPrj(PrjName_, PrjResFileName_)
        if self._PrjRes:
            self._PrjRes.openPrj(self._PrjResFileName)

    def savePrj(self, PrjName_=None, PrjResFileName_=None):
        """
        Сохранить проект.
        @param PrjName_: Имя проекта.
        @param PrjResFileName_: Имя файла ресурса проекта.
        """
        self.setPrj(PrjName_, PrjResFileName_)
        if self._PrjRes:
            self._PrjRes.savePrj()
        
    def refreshPrj(self, PrjName_=None, PrjResFileName_=None):
        """
        Обновить дерево проекта.
        """
        # Просто поменять время создания файла проекта
        self.setPrj(PrjName_, PrjResFileName_)
        if self._PrjRes:
            self._PrjRes.openPrj(self._PrjResFileName)
            self._PrjRes.savePrj()
        
    # --- Функции-свойства ---
    def getPrjName(self):
        """
        Имя проекта.
        """
        return self._PrjName
        
    def setPrjName(self, PrjName_):
        self._PrjName = PrjName_
        if self._PrjName is None:
            self._PrjName = ic_user.icGet('PrjName')
        
    def getPrjResFileName(self):
        """
        Файл ресурса проекта.
        """
        return self._PrjResFileName
        
    def getPrjResDir(self):
        """
        Папка ресурсов проекта.
        """
        return self._PrjResDir
        
    def setPrjResFileName(self, PrjResFileName_):
        self._PrjResFileName = PrjResFileName_
        if self._PrjResFileName is None:
            self._PrjResDir = ic_user.icGet('PRJ_DIR')
            self._PrjResFileName = self._PrjResDir+'/%s.pro' % self._PrjName
        else:
            self._PrjResDir = ic_file.DirName(self._PrjResFileName)
    
    def setPrj(self, PrjName_, PrjResFileName_):
        self.setPrjName(PrjName_)
        self.setPrjResFileName(PrjResFileName_)
