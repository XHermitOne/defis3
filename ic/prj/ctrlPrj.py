#!/usr/bin/env python3
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
from ic.utils import util
from ic.utils import resource
from ic.engine import glob_functions
from . import PrjRes

_ = wx.GetTranslation

__version__ = (0, 1, 1, 1)

# --- константы ---
OTHER_PRJ_FOLDER_NAME = u'Дополнительно'


# --- Описание классов ---
class icProjectResManager(object):
    """
    Класс управления ресурсами проекта.
    """

    def __init__(self, prj_name=None, prj_res_filename=None):
        """
        Конструктор.
        @param prj_name: Имя проекта.
        @param prj_res_filename: Имя файла ресурса проекта.
        """
        self.setPrj(prj_name, prj_res_filename)
        # Объект управления ресурсом проекта
        self._PrjRes = PrjRes.icPrjRes()
        
    def saveRes(self, res_name, res_type, res_data):
        """
        Записать ресурс в проект.
        @param res_name: Имя ресурса.
        @param res_type: Тип ресурса.
        @param res_data: Сам, записываемый ресурс.
        """
        self.makeFolderOther()
        if self._PrjRes:
            if not self._PrjRes.isResByNameANDType(res_name, res_type,
                                                   self._PrjRes.getFolderBody(OTHER_PRJ_FOLDER_NAME)):
                self._PrjRes.addRes(res_name, res_type,
                                    OTHER_PRJ_FOLDER_NAME)
                self._PrjRes.savePrj()
                    
        return resource.icSaveRes(res_name, res_type,
                                  nameRes=res_name, resData=res_data, ResFmt=1)

    def loadRes(self, res_name, res_type=None):
        """
        Прочитать ресурс из проекта.
        @param res_name: Имя загружаемого ресурса.
        @param res_type: Тип ресурса.
        @return: Содержимое ресурса или None в случае ошибки.
        """
        self.makeFolderOther()
        if self._PrjRes:
            # ВНИМАНИЕ! Производится глобальный поиск ресурса
            # а не только в папке <Дополнительные>
            # res_ref = self._PrjRes.getResRef(res_name, res_type,
            #                                  self._PrjRes.getFolderBody(OTHER_PRJ_FOLDER_NAME))
            res_ref = self._PrjRes.getResRef(res_name, res_type)
            return self._loadResFile(*res_ref)
        return None

    def loadResClone(self, res_name, res_type=None):
        """
        Прочитать ресурс из проекта для его последующего клонирования.
        @param res_name: Имя загружаемого ресурса.
        @param res_type: Тип ресурса.
        @return: Содержимое ресурса или None в случае ошибки.
        """
        if self._PrjRes:
            res_ref = self._PrjRes.getResRef(res_name, res_type)
            return self._loadResFile(*res_ref)
        return None
        
    def _loadResFile(self, res_name, res_type):
        """
        Открыть и загрузить файл ресурса.
        @return: Содержимое ресурса или None в случае ошибки.
        """
        res_file_name = os.path.join(self._PrjResDir, '%s.%s' % (res_name, res_type))
        if os.path.isfile(res_file_name):
            res_file = util.readAndEvalFile(res_file_name)
            res = res_file[res_name]
            return copy.deepcopy(res)
        return None
                
    def delRes(self, res_name, res_type):
        """
        Удалить ресурс из проекта.
        @param res_name: Имя ресурса.
        @param res_type: Тип ресурса.
        """
        self.makeFolderOther()
        if self._PrjRes:
            self._PrjRes.delRes(res_name, res_type)
            self._PrjRes.savePrj()
            
        res_file_name = os.path.join(self._PrjResDir, '%s.%s' % (res_name, res_type))
        if os.path.isfile(res_file_name):
            os.remove(res_file_name)
            return True
        return False

    def isRes(self, res_name, res_type=None):
        """
        Проверка соществования ресурса с именем и типом в проекте.
        @param res_name: Имя ресурса.
        @param res_type: Тип ресурса.
        """
        if self._PrjRes:
            return self._PrjRes.isResByNameANDType(res_name, res_type)
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

    def openPrj(self, prj_name=None, prj_res_filename=None):
        """
        Открыть проект.
        @param prj_name: Имя проекта.
        @param prj_res_filename: Имя файла ресурса проекта.
        """
        self.setPrj(prj_name, prj_res_filename)
        if self._PrjRes:
            self._PrjRes.openPrj(self._PrjResFileName)

    def savePrj(self, prj_name=None, prj_res_filename=None):
        """
        Сохранить проект.
        @param prj_name: Имя проекта.
        @param prj_res_filename: Имя файла ресурса проекта.
        """
        self.setPrj(prj_name, prj_res_filename)
        if self._PrjRes:
            self._PrjRes.savePrj()
        
    def refreshPrj(self, prj_name=None, prj_res_filename=None):
        """
        Обновить дерево проекта.
        """
        # Просто поменять время создания файла проекта
        self.setPrj(prj_name, prj_res_filename)
        if self._PrjRes:
            self._PrjRes.openPrj(self._PrjResFileName)
            self._PrjRes.savePrj()
        
    # --- Функции-свойства ---
    def getPrjName(self):
        """
        Имя проекта.
        """
        return self._PrjName
        
    def setPrjName(self, prj_name):
        self._PrjName = prj_name
        if self._PrjName is None:
            self._PrjName = glob_functions.getVar('PrjName')
        
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
        
    def setPrjResFileName(self, prj_res_filename):
        self._PrjResFileName = prj_res_filename
        if self._PrjResFileName is None:
            self._PrjResDir = glob_functions.getVar('PRJ_DIR')
            self._PrjResFileName = os.path.join(self._PrjResDir, '%s.pro' % self._PrjName)
        else:
            self._PrjResDir = os.path.dirname(self._PrjResFileName)
    
    def setPrj(self, prj_name, prj_res_filename):
        self.setPrjName(prj_name)
        self.setPrjResFileName(prj_res_filename)
