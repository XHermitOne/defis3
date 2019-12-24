#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Базовый класс объектов, которые могут хранится в системном хранилище.

Описание базового класса объектов, которые могут хранится в системном хранилище.
В хранилище храняться не сами объекты, а их метамодели. Под метомоделью понимается
описание объекта в терминах встроенных питоновский типов (int | string | tuple  | list | ...).
"""

import os
import os.path
import wx

from . import filefunc
from . import resfunc
from . import util
from . import lockfunc
from ic.engine import glob_functions
from ic.log import log

_ = wx.GetTranslation


__version__ = (1, 1, 1, 1)


class icPersistant:
    """
    Базовый класс объектов, которые могут хранится в системном хранилище.
    """
    def __init__(self, uniq_name, res_type='var', res_path=None, subsys='', przBuff=True):
        """
        Конструктор базового класса.

        :type uniq_name: C{string}
        :param uniq_name: Уникальное имя объекта.
        :type res_type: C{string}
        :param res_type: Тип хранилища - задает расширения файла.
        :type res_path: C{string}
        :param res_path: Путь до папки с хранилищем <res_path/resource.var>.
        :type subsys: C{string}
        :param subsys: Имя подсистемы.
        :type przBuff: C{bool}
        :param przBuff: Признак работы с буфером.
        """
        self.name = uniq_name
        self.res_path = res_path
        self.subsys = subsys
        self.res_type = res_type
        self.przBuff = przBuff
        
        #   Метамодель объекта
        self._model = None
        
    def UpdateDict(self, obj, *args, **kwargs):
        """
        Переопределяемый метод, который определяет каким образом объединяются
        метамодели одного класса, наследованного от icPersistant.
        """
        pass

    def GetModel(self):
        """
        Возвращает указатель на объект модели.
        """
        return self._model
       
    def LoadPersistent(self, przBuff=None):
        """
        Читает объект.

        :rtype: C{...}
        :return: Возвращает сохраненный объект.
        """
        if przBuff is None:
            przBuff = self.przBuff
            
        obj = self.getRes(self.res_path, self.name, self.res_type)
        if obj:
            self.UpdateDict(obj)
            return self.GetModel()
        else:
            return self.GetModel()
      
    def getRes(self, res_path, res_name, res_type='var'):
        """
        Получить ресурс.

        :param res_path: путь к ресурсным файлам (d:/aaa/fff).
        :param res_name: имя ресурса.
        :param res_type: тип ресурса.
        :return: Возвращает ресурс или None в случае ошибки.
        """
        local_dir = filefunc.getPrjProfilePath() if res_path is None else res_path
        full_file_name = os.path.join(local_dir, res_name.replace(':', '_')+'.'+res_type)
        log.debug(u'Получение ресурса >>> name=%s, dir=%s, filename=%s' % (self.name, local_dir, full_file_name))
        if os.path.exists(full_file_name):
            return util.readAndEvalFile(full_file_name)
        return None
        
    def SavePersistent(self, przBuff=None):
        """
        Сохраняет объект в хранилище.

        :type obj: C{стандартные питоновские типы, которые серилизует cPickle}
        :param obj: Метамодель объекта в представлении питоновских типов.
        :rtype: C{bool}
        :return: Признак успешного завершения операции.
        """
        if przBuff is None:
            przBuff = self.przBuff
        
        ret = self.setRes(self._model, self.res_path, self.name, self.res_type)
        log.debug(u'Сохранение объекта в хранилище >>> name=%s, result=%s' % (self.name, str(ret)))
        return ret
        
    def setRes(self, res, res_path, res_name, res_type='var'):
        """
        Установить ресурс.

        :param res: Сам ресурс.
        :param res_path: путь к ресурсным файлам (d:/aaa/fff).
        :param res_name: имя ресурса.
        :param res_type: тип ресурса.
        :return: Возвращает True или False в случае ошибки.
        """
        try:
            local_dir = filefunc.getPrjProfilePath() if res_path is None else res_path
            full_file_name = os.path.join(local_dir, res_name.replace(':', '_')+'.'+res_type)
            lock_file_name = os.path.join(local_dir, '#lock', res_name.replace(':', '_') + lockfunc.LOCK_FILE_EXT)
            if not lockfunc.IsLockedFile(lock_file_name):
                try:
                    lock_rec = {'computer': lockfunc.ComputerName(),
                                'user': glob_functions.getVar('UserName')}
                    lockfunc.LockFile(lock_file_name, lock_rec)
                    resfunc.saveResourcePickle(full_file_name, res)
                    lockfunc.UnLockFile(lock_file_name)
                except:
                    log.fatal(u'Ошибка сохранение ресурсного файла <%s>' % full_file_name)
                    lockfunc.UnLockFile(lock_file_name)
            else:
                log.warning(u'Файл <%s> заблокирован для записи' % full_file_name)
                return False
            
            return True
        except:
            log.fatal(u'Ошибка установки ресурса')
            return False
