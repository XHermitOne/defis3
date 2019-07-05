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
from ic.utils import ic_extend

__version__ = (0, 1, 1, 1)

# Класс базовой модели.
# От этого класса должны наследоваться все модели
icBaseModel = sqlalchemy.ext.declarative.declarative_base()

SCHEME_DIR_NAME = 'scheme'


INIT_PY_TEXT = u'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Пакет схемы данных в виде моделей для управления данными с помощью SQLAlchemy.
\"\"\"

__version__ = (0, 0, 0, 1)
'''


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

    result = ic_file.MakeDirs(scheme_dirname)

    # Т.к. папка схемы является пакетом,
    # то необходимо проверить наличие __init__.py файла
    init_py_filename = os.path.join(scheme_dirname, '__init__.py')
    if not os.path.exists(init_py_filename):
        # Создать файл если его нет
        return ic_extend.save_file_text(init_py_filename, INIT_PY_TEXT)

    return result


def genModelModuleFilename(name, bFullName=True):
    """
    Генерация имени файла модуля модели по имени.
    @param name: Имя на основе которого производится генерация.
    @param bFullName: Генерировать полное имя файла (с полным путем хранения)?
    @return: Имя файла модуля модели.
    """
    base_filename = '%s_model.py' % name
    if bFullName:
        return os.path.join(getSchemeDir(), base_filename)
    return base_filename


def genModelModuleManagerFilename(name, bFullName=True):
    """
    Генерация имени файла модуля менеджера модели по имени.
    @param name: Имя на основе которого производится генерация.
    @param bFullName: Генерировать полное имя файла (с полным путем хранения)?
    @return: Имя файла модуля менеджера модели.
    """
    base_filename = '%s_manager.py' % name
    if bFullName:
        return os.path.join(getSchemeDir(), base_filename)
    return base_filename

