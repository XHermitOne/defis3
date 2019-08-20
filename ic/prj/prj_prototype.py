#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль зарегистрированных классов узлов дерева проекта.
"""

from . import prj_root
from . import prj_env
from . import prj_security
from . import prj_report
from . import prj_resource
from . import prj_module
from . import ImpNode

__version__ = (0, 1, 1, 1)

# Константы
# Реестр узлов дерева проектов
# 'тип ресурса':класс узла
nodeReg = {'pro': prj_root.icPrjRoot,  # Проект
           'env': prj_env.icPrjEnv,  # Окружение
           'rol': prj_security.icPrjSecurity,  # Безопасность
           'rep': prj_report.icPrjReports,  # Отчеты
           'res': prj_resource.icPrjResources,  # Ресурсы
           'tab': prj_resource.icPrjTabRes,  # Таблицы
           'sqt': prj_resource.icPrjSQLiteRes,  # БД SQLite
           'pgs': prj_resource.icPrjPostgreSQLRes,  # БД PostgreSQL
           'odb': prj_resource.icPrjObjStorageRes,  # Хранилище ObjectStorage
           'src': prj_resource.icPrjDBRes,  # БД
           'frm': prj_resource.icPrjFrmRes,  # Формы
           'win': prj_resource.icPrjWinRes,  # Главное окно
           'mnu': prj_resource.icPrjMenuRes,  # Меню
           '__py__': prj_module.icPrjModules,  # Модули
           'py': prj_module.icPrjModule,  # Модуль
           'ftl': prj_resource.icPrjTemplate,  # Шаблон
           'mth': prj_resource.icPrjMethod,  # Метод
           'mtd': prj_resource.icPrjMetaDataRes,  # Дерево метакомпонент/Метаданные
           '__imp__': ImpNode.icPrjImportSystems,  # Импортируемы подсистемы
           'imp': ImpNode.icPrjImportSys,  # Импортируемая подсистема
           }
