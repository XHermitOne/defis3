#!/usr/bin/env python
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

# Константы
# Реестр узлов дерева проектов
# 'тип ресурса':класс узла
nodeReg = {'pro': prj_root.PrjRoot,                 # Проект
           'env': prj_env.PrjEnv,                   # Окружение
           'rol': prj_security.PrjSecurity,         # Безопасность
           'rep': prj_report.PrjReports,            # Отчеты
           'res': prj_resource.PrjResources,        # Ресурсы
           'tab': prj_resource.PrjTabRes,           # Таблицы
           'sqt': prj_resource.PrjSQLiteRes,        # БД SQLite
           'pgs': prj_resource.PrjPostgreSQLRes,    # БД PostgreSQL
           'odb': prj_resource.PrjObjStorageRes,    # Хранилище ObjectStorage
           'src': prj_resource.PrjDBRes,            # БД
           'frm': prj_resource.PrjFrmRes,           # Формы
           'win': prj_resource.PrjWinRes,           # Главное окно
           'mnu': prj_resource.PrjMenuRes,          # Меню
           '__py__': prj_module.PrjModules,         # Модули
           'py': prj_module.PrjModule,              # Модуль
           'ftl': prj_resource.PrjTemplate,         # Шаблон
           'mth': prj_resource.PrjMethod,           # Метод
           'mtd': prj_resource.PrjMetaDataRes,      # Дерево метакомпонент/Метаданные
           '__imp__': ImpNode.PrjImportSystems,     # Импортируемы подсистемы
           'imp': ImpNode.PrjImportSys,             # Импортируемая подсистема
           }
