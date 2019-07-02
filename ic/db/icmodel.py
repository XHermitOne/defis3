#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс поддержки моделей на основе SQLAlchemy.

Модули используются для низкоуровневого взаимодействия
(на уровне SQLAlchemy) с БД.

Конечная модель представляет собой следующую иерархию классов:

 icBaseModel        icModelManager
     |                     |
     |                     V
     |           icObjectModelManager
     |                |
     +-------+        |
             V        V
            icObjectModel
"""

import os.path
import sqlalchemy.ext.declarative

from ic.utils import ic_file

# Класс базовой модели.
# От этого класса должны наследоваться все модели
icBaseModel = sqlalchemy.ext.declarative.declarative_base()

SCHEME_DIR_NAME = 'scheme'


def getSchemeDir(bAutoCreate=True):
    """
    Функция получения пути хранения модулей моделей.
    @param bAutoCreate: Создать папку хранения модулей моделей если она не существует?
    @return: Папка хранения модулей моделей.
        Папка хранения модулей моделей - пакет в проекте с именем scheme.
    """
    prj_dir = ic_file.getProjectDir()
    scheme_dir = os.path.join(prj_dir, SCHEME_DIR_NAME)
    if bAutoCreate:
        createSchemeDir(scheme_dirname=scheme_dir)
    return scheme_dir


def createSchemeDir(scheme_dirname=None):
    """
    Создать папку хранения модулей моделей.
    @param scheme_dirname: Папка хранения модулей моделей.
        Если не определена, то генерируется.
    @return: True/False.
    """
    if scheme_dirname is None:
        scheme_dirname = getSchemeDir(bAutoCreate=False)

    return ic_file.MakeDirs(scheme_dirname)
