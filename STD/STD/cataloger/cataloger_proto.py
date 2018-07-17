#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса прототипа каталогизатора.

Каталогизатор (Cataloger) - объект который берет
файл или строку, анализирует ее и
сохраняет результат в физичеком каталоге.
Каталог м.б. физичекий (physic catalog) и логический (logic catalog).
Физический каталог - физическая структура хранения данных
Например: папки и файлы на HDD.
Логический каталог - каталог с отличным (от физического каталога)
порядком вложенности уровней каталога (catalog level).
Уровень каталога - тип папкок каталога одного уровня,
определяющих один из признаков каталогизируемого объекта.

Например:
Физический путь:
    /контрагент/год/тип документа/файл-объект
        ^        ^        ^            ^
        Это уровни каталога            |
                    Каталогизируемый объект

Логический путь:
    /тип документа/год/контрагент/файл-объект
          ^        ^        ^           ^
          Это уровни каталога           |
                    Каталогизируемый объект

Объекты храняться по физическому пути, но обращаться к ним можно
как по физическому так и по логическому пути.
"""

import os
import os.path
import shutil
from ic.log import log
from . import level_proto

__version__ = (0, 0, 1, 4)


class icCatalogerProto(object):
    """
    Класс прототипа каталогизатора.

    self.physic_catalog - Список уровней физического каталога
    self.logic_catalogs - Словарь структур логических каталогов:
        {
        'Имя логического каталога': [список индексов уровней физического каталога],
        ...
        }
    Каталог по умолчанию храниться в обычной папочно-файловой структуре на диске, но
    чтобы имелась возможность поменять хранилище скажем на справочник
    заведены эти функции:
    self._put_physic_func(obj, physic_path) - Переопределенная функция помещения объекта в физический каталог
    self._get_physic_func(physic_path) - Переопределенная функция получения объекта из физического каталога
    self.physic_catalog_folder - Папка размещения физического каталога
    """

    def __init__(self):
        """
        Конструктор.
        """
        # Список уровней физического каталога
        self.physic_catalog = list()

        self.logic_catalogs = dict()

        self._put_physic_func = None
        self._get_physic_func = None

        # Папка размещения физического каталога
        self.physic_catalog_folder = None

        # Последний размещаемый в каталоге объект
        self.last_catalog_objpath = None

    def getLastObjPath(self):
        """
        Последний размещаемый в каталоге объект с полным путем.
        """
        return self.last_catalog_objpath

    def addPhysicCatalogLevel(self, catalog_level):
        """
        Добавить в каталогизатор уровень физического каталога.
        @param catalog_level: Объект уровня каталога.
        @return: True/False
        """
        if not issubclass(catalog_level.__class__, level_proto.icCatalogLevelProto):
            # Если объект не является объектом уровня каталога, то ошибка
            log.warning(u'Объект <%s> не является уровнем каталога')
            return False
        if self.physic_catalog is None:
            self.physic_catalog = list()
        self.physic_catalog.append(catalog_level)
        return True

    def addLogicCatalogSeries(self, logic_catalog_name, *index_series):
        """
        Добавить пос
        @param logic_catalog_name: Имя логического каталога.
        @param index_series: Последовательность индексов уровней физического каталога.
        @return: True/False
        """
        # Проверка типов входных данных
        check_arg = min([isinstance(idx, int) for idx in index_series])
        if not check_arg:
            log.warning(u'Не корректный тип индексов')
            return False

        if self.logic_catalogs is None:
            self.logic_catalogs = list()

        # Индексы не должны повторяться
        index_series = tuple([idx for i, idx in enumerate(index_series) if idx not in index_series[i+1:]])
        self.logic_catalogs[logic_catalog_name] = index_series
        return True

    def put_object(self, obj, do_remove=False):
        """
        Разместить объект в каталоге.
        Размещение производиться по признакам объекта
        по уровням физического каталога.
        @param obj: Размещаемый объект.
        @param do_remove: Произвести перенос объекта?
        @return: True/False.
        """
        phys_path = list()
        for level in self.physic_catalog:
            folder_name = level.getFolderName(obj)
            phys_path.append(folder_name)

        return self.put_obj_path(obj, phys_path, do_remove=do_remove)

    def logic2physic_path(self, logic_path, logic_catalog_name):
        """
        Преобразовать логический путь в физический.
        @param logic_path: Логический путь.
        @param logic_catalog_name: Имя логического каталога
        @return: Список имен папко физического пути.
            Либо None в случае ошибки.
        """
        logic_series = self.logic_catalogs.get(logic_catalog_name, None)
        if logic_series is None:
            log.warning(u'Не определен ряд логического каталога <%s>' % logic_catalog_name)
            return None
        if len(logic_path) != len(logic_series):
            log.warning(u'Путь не соответсвует ряду логического каталога')
            return None
        # Делаем физический путь из логического
        phys_path = [None] * len(self.physic_catalog)
        for i, idx in enumerate(logic_series):
            phys_path[idx] = logic_path[i]
        return phys_path

    def put_obj_path(self, obj, path, logic_catalog_name=None, do_remove=False):
        """
        Размещение объекта в каталоге по пути.
        @param obj: Размещаемый объект.
        @param path: Путь каталога для размещения.
            Путь каталога - список имен папок.
        @param logic_catalog_name: Имя логического каталога,
            если размещение производится по логическому каталогу.
            Если None, то считаем что размещение производиться
            по физическому каталогу.
        @param do_remove: Произвести перенос объекта?
        @return: True/False.
        """
        phys_path = path
        if logic_catalog_name:
            phys_path = self.logic2physic_path(path, logic_catalog_name)
            if phys_path is None:
                return False

        return self.put_obj_physic_path(obj, phys_path, do_remove=do_remove)

    def put_obj_physic_path(self, obj, physic_path, do_remove=False):
        """
        Размещение объекта в физическом каталоге по физическому пути.
        @param obj: Размещаемый объект
        @param physic_path: Физический путь в физическом каталоге.
            Путь каталога - список имен папок.
        @param do_remove: Произвести перенос объекта?
        @return: True/False.
        """
        self.last_catalog_objpath = None

        if self._put_physic_func:
            # Если определена внешняя функция, то
            # передать ей управление
            return self._put_physic_func(obj, physic_path)

        if self.physic_catalog_folder is None:
            log.warning(u'Не определена папка размещения физического каталога каталогизатора')
            return False
        real_path = os.path.join(self.physic_catalog_folder, *physic_path)

        if isinstance(obj, str) or isinstance(obj, unicode):
            # Если объект-строка, то считаем что это имя файла
            if not os.path.exists(obj):
                log.warning(u'Не найден файл <%s> для размещения в каталоге' % obj)
                return False
            filename = os.path.join(real_path, os.path.basename(obj))
            log.debug(u'Копирование файла <%s> в папку <%s>' % (obj, real_path))
            try:
                if not os.path.exists(real_path):
                    os.makedirs(real_path)
                if os.path.exists(filename) and not os.path.samefile(obj, filename):
                    # Удалить если уже сущетсвует такой файл в каталоге
                    log.warning(u'Файл <%s> уже существует в каталоге. Файл из каталога будет удален' % filename)
                    os.remove(filename)
                if not os.path.exists(filename) or not os.path.samefile(obj, filename):
                    shutil.copyfile(obj, filename)
                    log.info(u'Копирование <%s> -> <%s> ... ok' % (obj, filename))

                    if do_remove:
                        # Перенести можно только не совпадающие объекты
                        # После удачного переноса скана в каталог
                        # удалить файл в папке
                        try:
                            log.info(u'Удаление файла <%s>' % obj)
                            os.remove(obj)
                        except:
                            log.fatal(u'Ошибка удаления файла <%s>' % obj)
                else:
                    log.warning(u'Попытка не корректного копирования файла <%s> -> <%s>' % (obj, filename))
                # Запомнить полное имя последнего размещенного в каталоге файла
                self.last_catalog_objpath = filename
            except:
                log.fatal(u'Ошибка копирования файла <%s> в <%s>' % (obj, filename))
                return False
            return True
        else:
            log.warning(u'Не поддерживаемый тип размещаемого в каталоге объекта <%s>' % type(obj))
        return False

    def get_object(self, path, logic_catalog_name=None):
        """
        Получить объект по пути.
        @param path: Путь до объекта.
        @param logic_catalog_name: Имя логического каталога,
            если размещение производится по логическому каталогу.
            Если None, то считаем что размещение производиться
            по физическому каталогу.
        @return: Объект/Имя файла, размещенного в физическом каталоге.
        """
        if logic_catalog_name:
            path = self.logic2physic_path(path, logic_catalog_name)
        return self.get_obj_physic_path(path)

    def get_obj_physic_path(self, physic_path):
        """
        Получение объекта по пути в физическом каталоге.
        @return: Объект/Имя файла, размещенного в физическом каталоге.
        """
        if self._get_physic_func:
            # Если определена внешняя функция, то
            # передать ей управление
            return self._get_physic_func(physic_path)

        # Путь физического каталога, просто получаем путь до файла
        # и возвращаем его.
        real_path = os.path.join(*physic_path)
        if not os.path.exists(real_path):
            # Предупреждаем, что такого объекта нет
            # но реальный путь всетаки возвращаем
            log.warning(u'Не найден объект <%s> в физическом каталоге' % real_path)
        return real_path
