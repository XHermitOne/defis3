#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Абстрактное хранилище типовых объектов.
По сути своей это интерфейc взаимодействия 
с любым хранилищем объектов.
"""

# --- Подключение библиотек ---
import os
import os.path

from ic.utils import filefunc
from ic.utils import ic_util
from ic.interfaces import StorageInterface as storage_interface
from . import storesrc

# --- Константы ---
# --- Спецификации ---
# Тип объекта хранилища
OBJ_STORAGE_TYPE = 'ObjectStorage'
# Спецификация вида хранения
SPC_IC_OBJ_STORAGE = {'type': OBJ_STORAGE_TYPE,
                      'storage_src': None,
                      }

__version__ = (0, 1, 1, 1)


# --- Функции ---
def CreateObjectStorageByDir(Dir_):
    """
    Создает хранилище типовых объектов.
    @param Dir_: Папка - хранилище.
    """
    return icObjectStorageDir(Dir_)


class icObjectStorageDir(storesrc.icTreeDirStorage,
                         storage_interface.icObjectStorageInterface):
    """
    Абстрактное хранилище типовых объектов.
    """

    def __init__(self, Dir_):
        """
        Конструктор.
        @param Dir_: Папка - хранилище.
        """
        # Привести относительные пути к папке проекта
        Dir_ = filefunc.get_absolute_path(Dir_)
        storage_interface.icObjectStorageInterface.__init__(self, None)
        storesrc.icTreeDirStorage.__init__(self, Dir_)
        self.name = os.path.basename(Dir_)
        self.Open()


class icObjectStorage(storesrc.icObjStorageSrc,
                      storage_interface.icObjectStorageInterface):
    """
    Абстрактное хранилище типовых объектов.
    """

    def __init__(self, Resource_=None):
        """
        Конструктор.
        @param Resource_: Ресурс описания объекта.
        """
        storage_interface.icObjectStorageInterface.__init__(self, Resource_)
        self._spc = ic_util.SpcDefStruct(SPC_IC_OBJ_STORAGE, self._res)
        # self._storage_src_name = ic_exec.execute_code(self._spc['storage_src'], self)
        self._storage_src_psp = self._spc['storage_src']
        self._storage_src_name = self._storage_src_psp[0][1]
        storesrc.icObjStorageSrc.__init__(self, self._storage_src_name)
