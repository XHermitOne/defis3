#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Система управления запуском внешней
программы генераторов отчетов icReport.
"""

import sys
import os
import os.path
import wx

from . import config
from ic.engine import glob_functions
from ic.utils import extfunc
from ic.utils import resfunc
from ic.utils import strfunc
from ic.log import log

from . import icreportactiondlg

__version__ = (0, 1, 1, 1)

DEFAULT_REPORT_FILE_EXT = '.rprt'

DEFAULT_INIT_PY_FMT = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Пакет отчетов прикладной системы <%s>.
\"\"\"

__version__ = (0, 0, 0, 1)

'''

# Комманды пост обработки сгенерированног отчета
DO_COMMAND_PRINT = 'print'
DO_COMMAND_PREVIEW = 'preview'
DO_COMMAND_EXPORT = 'export'
DO_COMMAND_SELECT = 'select'


class icReportManager(object):
    """
    Класс менеджера управления запуском внешней
    программы генераторов отчетов icReport.
    """

    def __init__(self, report_exec_filename=None, report_dir=None):
        """
        Конструктор.
        :param report_exec_filename: Полный путь до исполняемого файла <icreport.py>.
            Если не определен, то берется из конфигурационного файла.
        :param report_dir: Папка отчетов, если не определена, то
            будет использоваться папка reports d папке текущего проекта.
        """
        self._report_exec_filename = config.get_glob_var('DEFAULT_REPORT_EXEC_FILENAME') if report_exec_filename is None else report_exec_filename

        self._report_dir = None
        if report_dir and os.path.exists(report_dir):
            self._report_dir = report_dir

    def getReportExec(self):
        return self._report_exec_filename

    def design(self):
        """
        Запуск режима конструирования отчетов.
        """
        try:
            if os.path.exists(self._report_exec_filename):
                cmd = '%s %s --editor --path=%s &' % (sys.executable,
                                                      self._report_exec_filename,
                                                      self.getReportDir())
                try:
                    log.info(u'Запуск внешней программы <%s>' % cmd)
                    os.system(cmd)
                except:
                    log.fatal(u'Запуск программы <icReport> в режиме конструктора отчетов: <%s>' % cmd)
            else:
                log.warning(u'Запускаемый модуль программы <icReport> : <%s> не найден' % self._report_exec_filename)
        except:
            log.fatal(u'Ошибка запуска режима конструктора отчетов')

    def getReportDir(self):
        """
        Папка отчетов.
        Папка отчетов по умолчанию всегда находиться в папке проекта.
        Например: /defis/NSI/NSI/reports.
        :return: Полный путь до директории отчетов.
        """
        if self._report_dir is None:
            prj_dir = glob_functions.getVar('PRJ_DIR')
            self._report_dir = os.path.join(prj_dir,
                                            config.get_glob_var('DEFAULT_REPORT_DIRNAME'))
            # Проверить сразу существует ли папка
            if not os.path.exists(self._report_dir):
                try:
                    os.makedirs(self._report_dir)
                    log.info(u'Cоздание папки <%s>' % self._report_dir)
                    description_filename = os.path.join(self._report_dir, 'descript.ion')
                    prj_name = os.path.basename(prj_dir)
                    extfunc.save_file_text(description_filename,
                                             u'Отчеты прикладной системы <%s>' % prj_name)
                    init_filename = os.path.join(self._report_dir, '__init__.py')
                    extfunc.save_file_text(init_filename,
                                           DEFAULT_INIT_PY_FMT % prj_name)
                except IOError:
                    log.warning(u'Ошибка создания папки <%s>' % self._report_dir)
        return self._report_dir

    def report_print(self, report_filename,
                     db_url=None, sql=None, command=None,
                     stylelib_filename=None, variables=None):
        """
        Запуск генерации отчета и вывод его на печать.
        :param report_filename: Имя файла шаблона отчета.
            Пути задаются относительно папки отчетов.
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Запрос SQL.
        :param command: Комманда после генерации. print/preview/export.
        :param stylelib_filename: Файл библиотеки стилей.
        :param variables: Словарь переменных для заполнения отчета.
        :return: True/False.
        """
        try:
            if os.path.exists(self._report_exec_filename):
                cmd = '%s %s --print=%s --path=%s' % (sys.executable,
                                                      self._report_exec_filename,
                                                      report_filename,
                                                      self.getReportDir())
                cmd = self._addCmdExtArgs(cmd, db_url, sql, command,
                                          stylelib_filename, variables)
                # if isinstance(cmd, unicode):
                #    cmd = cmd.encode(config.DEFAULT_ENCODING)
                msg_cmd = strfunc.toUnicode(cmd, config.DEFAULT_ENCODING)
                try:
                    log.info(u'Запуск внешней программы <%s>' % msg_cmd)
                    os.system(cmd)
                except:
                    log.fatal(u'Запуск программы <icReport> в режиме печати отчета: <%s>' % msg_cmd)
            else:
                log.warning(u'Запускаемый модуль программы <icReport> : <%s> не найден' % self._report_exec_filename)
        except:
            log.fatal(u'Ошибка печати отчета <%s>' % report_filename)

    def report_preview(self, report_filename,
                       db_url=None, sql=None, command=None,
                       stylelib_filename=None, variables=None):
        """
        Запуск генерации отчета с предварительным просмотром.
        :param report_filename: Имя файла шаблона отчета.
            Пути задаются относительно папки отчетов.
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Запрос SQL.
        :param command: Комманда после генерации. print/preview/export.
        :param stylelib_filename: Файл библиотеки стилей.
        :param variables: Словарь дополнительных переменных.
        :return: True/False.
        """
        try:
            if os.path.exists(self._report_exec_filename):
                cmd = '%s %s --preview=%s --path=%s' % (sys.executable,
                                                        self._report_exec_filename,
                                                        report_filename,
                                                        self.getReportDir())
                cmd = self._addCmdExtArgs(cmd, db_url, sql, command,
                                          stylelib_filename, variables)
                # if isinstance(cmd, unicode):
                #    cmd = cmd.encode(config.DEFAULT_ENCODING)
                msg_cmd = strfunc.toUnicode(cmd, config.DEFAULT_ENCODING)
                try:
                    log.info(u'Запуск внешней программы <%s>' % msg_cmd)
                    os.system(cmd)
                except:
                    log.fatal(u'Запуск программы <icReport> в режиме предварительного просмотра отчета: <%s>' % msg_cmd)
            else:
                log.warning(u'Запускаемый модуль программы <icReport> : <%s> не найден' % self._report_exec_filename)
        except:
            log.fatal(u'Ошибка предварительного просмотра отчета <%s>' % report_filename)

    def report_export(self, report_filename,
                      db_url=None, sql=None, command=None,
                      stylelib_filename=None, variables=None):
        """
        Запуск генерации отчета с конвертацией в офисную программу.
        :param report_filename: Имя файла шаблона отчета.
            Пути задаются относительно папки отчетов.
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Запрос SQL.
        :param command: Комманда после генерации. print/preview/export.
        :param stylelib_filename: Файл библиотеки стилей.
        :param variables: Словарь дополнительных переменных.
        :return: True/False.
        """
        try:
            if os.path.exists(self._report_exec_filename):
                cmd = '%s %s --export=%s --path=%s' % (sys.executable,
                                                       self._report_exec_filename,
                                                       report_filename, self.getReportDir())

                cmd = self._addCmdExtArgs(cmd, db_url, sql, command,
                                          stylelib_filename, variables)
                # if isinstance(cmd, unicode):
                #    cmd = cmd.encode(config.DEFAULT_ENCODING)
                msg_cmd = strfunc.toUnicode(cmd, config.DEFAULT_ENCODING)
                try:
                    log.info(u'Запуск внешней программы <%s>' % msg_cmd)
                    os.system(cmd)
                except:
                    log.fatal(u'Запуск программы <icReport> в режиме экспорта отчета: <%s>' % msg_cmd)
            else:
                log.warning(u'Запускаемый модуль программы <icReport> : <%s> не найден' % self._report_exec_filename)
        except:
            log.fatal(u'Ошибка экспорта отчета <%s>' % report_filename)

    def post_select_action(self, report_filename, parent=None,
                           db_url=None, sql=None, command=None,
                           stylelib_filename=None, variables=None):
        """
        Выбрать действие, которое хотим сделать с отчетом, после генерации отчета.
        :param report_filename: Имя файла шаблона отчета.
            Пути задаются относительно папки отчетов.
        :param parent: Родительское wxWindow окно для диалога.
            Если не указано, то береться wx.GetAppt().GetTopWindow().
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Запрос SQL.
        :param command: Комманда после генерации. print/preview/export.
        :param stylelib_filename: Файл библиотеки стилей.
        :param variables: Словарь дополнительных переменных.
        :return: True/False.
        """
        try:
            if os.path.exists(self._report_exec_filename):
                cmd = '%s %s --select=%s --path=%s' % (sys.executable,
                                                       self._report_exec_filename,
                                                       report_filename,
                                                       self.getReportDir())
                cmd = self._addCmdExtArgs(cmd, db_url, sql, command,
                                          stylelib_filename, variables)
                msg_cmd = strfunc.toUnicode(cmd, config.DEFAULT_ENCODING)
                try:
                    log.info(u'Запуск внешней программы <%s>' % msg_cmd)
                    os.system(cmd)
                except:
                    log.fatal(u'Запуск программы <icReport> в режиме выбора действия над отчетом отчета: <%s>' % msg_cmd)
            else:
                log.warning(u'Запускаемый модуль программы <icReport> : <%s> не найден' % self._report_exec_filename)
        except:
            log.fatal(u'Ошибка режима выбора действия с отчетом <%s>' % report_filename)

    def _addCmdVars(self, cmd, variables=None):
        """
        Добавить дополнительные переменные в командную строку.
        :param cmd: Строка команды.
        :param variables: Словарь дополнительных переменных.
        :return: Строка команды с дополнительными параметрами.
        """
        if variables:
            cmd += ' ' + ' '.join(['--var="%s=%s"' % (var_name, var_value) for var_name, var_value in variables.items()])
        return cmd

    def _addCmdDBURL(self, cmd, db_url=None):
        """
        Добавить БД URL в командную строку.
        :param cmd: Строка команды.
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :return: Строка команды с дополнительными параметрами.
        """
        if db_url:
            cmd += ' --db="%s"' % db_url
        return cmd

    def _addCmdSQL(self, cmd, sql=None):
        """
        Добавить SQL в командную строку.
        :param cmd: Строка команды.
        :param sql: Запрос SQL.
        :return: Строка команды с дополнительными параметрами.
        """
        if sql:
            cmd += ' --sql="%s"' % sql
        return cmd

    def _addCmdPostCommand(self, cmd, command=None):
        """
        Добавить команду после генерации в командную строку.
        :param cmd: Строка команды.
        :param command: Комманда после генерации.
            Все возможне команды определены константами в данном модуле:
                DO_COMMAND_PRINT = 'print'
                DO_COMMAND_PREVIEW = 'preview'
                DO_COMMAND_EXPORT = 'export'
                DO_COMMAND_SELECT = 'select'
        :return: Строка команды с дополнительными параметрами.
        """
        if command:
            cmd += ' --%s' % command
        return cmd

    def _addCmdStyleLib(self, cmd, stylelib_filename=None):
        """
        Добавить файл библиотеки стилей в командную строку.
        :param cmd: Строка команды.
        :param stylelib_filename: Файл библиотеки стилей.
        :return: Строка команды с дополнительными параметрами.
        """
        if stylelib_filename:
            cmd += ' --stylelib="%s"' % stylelib_filename
        return cmd

    def _addCmdExtArgs(self, cmd, db_url=None, sql=None, command=None,
                       stylelib_filename=None, variables=None):
        """
        Добавление в командную строку дополнительных параметров запуска.
        :param cmd: Строка команды.
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Запрос SQL.
        :param command: Комманда после генерации. print/preview/export.
        :param stylelib_filename: Файл библиотеки стилей.
        :param variables: Словарь дополнительных переменных.
        :return: Строка команды с дополнительными параметрами.
        """
        cmd = self._addCmdDBURL(cmd, db_url)
        cmd = self._addCmdSQL(cmd, sql)
        cmd = self._addCmdPostCommand(cmd, command)
        cmd = self._addCmdStyleLib(cmd, stylelib_filename)
        cmd = self._addCmdVars(cmd, variables)
        return cmd

    def prev_select_action(self, report_filename, parent=None,
                           db_url=None, sql=None, command=None,
                           stylelib_filename=None, variables=None):
        """
        Сначала выбрать действие, которое хотим сделать с отчетом.
        :param report_filename: Имя файла шаблона отчета.
            Пути задаются относительно папки отчетов.
        :param parent: Родительское wxWindow окно для диалога.
            Если не указано, то береться wx.GetAppt().GetTopWindow().
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Запрос SQL.
        :param command: Комманда после генерации. print/preview/export.
        :param stylelib_filename: Файл библиотеки стилей.
        :param variables: Словарь дополнительных переменных.
        :return: True/False.
        """
        try:
            if parent is None:
                parent = wx.GetApp().GetTopWindow()

            description = self.getReportDescription(report_filename)
            dlg = None
            try:
                dlg = icreportactiondlg.icReportActionDialog(parent)
                dlg.setReportNameTitle(description)
                dlg.ShowModal()
                result = dlg.getSelectedAction()
                dlg.Destroy()
                dlg = None

                if result == icreportactiondlg.PRINT_ACTION_ID:
                    return self.report_print(report_filename, db_url=db_url, sql=sql,
                                             command=command, stylelib_filename=stylelib_filename, variables=variables)
                elif result == icreportactiondlg.PREVIEW_ACTION_ID:
                    return self.report_preview(report_filename, db_url=db_url, sql=sql,
                                               command=command, stylelib_filename=stylelib_filename, variables=variables)
                elif result == icreportactiondlg.EXPORT_ACTION_ID:
                    return self.report_export(report_filename, db_url=db_url, sql=sql,
                                              command=command, stylelib_filename=stylelib_filename, variables=variables)
            except:
                if dlg:
                    dlg.Destroy()
                log.fatal(u'Ошибка выбора действия над отчетом <%s>' % report_filename)
        except:
            log.fatal(u'Ошибка выбора действия над отчетом <%s>' % report_filename)
        return False

    def getReportResourceFilename(self, report_filename='', report_dir=''):
        """
        Получить полное имя файла шаблона отчета.
        :param report_filename: Имя файла отчета в кратком виде.
        :param report_dir: Папка отчетов.
        :return: Полное имя файла отчета.
        """
        # Проверить расширение
        if not report_filename.endswith(DEFAULT_REPORT_FILE_EXT):
            report_filename = os.path.splitext(report_filename)[0]+DEFAULT_REPORT_FILE_EXT

        if os.path.exists(report_filename):
            # Проверить может быть задано абсолютное имя файла
            filename = report_filename
        else:
            # Задано скорее всего относительное имя файла
            # относительно папки отчетов
            filename = os.path.join(report_dir, report_filename)
            if not os.path.exists(filename):
                # Нет такого файла
                log.warning(u'Файл шаблона отчета <%s> не найден' % filename)
                filename = None
        return filename

    def loadReportResource(self, report_filename=''):
        """
        Загрузить ресурс шаблона отчета.
        :param report_filename: Полное имя файла шаблона отчета.
        :return: Данные шаблона отчета.
        """
        return resfunc.loadResource(report_filename)

    def getReportDescription(self, report_filename):
        """
        Получить описание отчета
        :param report_filename: Имя шаблона отчета.
        :return: Описание отчета или имя файла отчета, если не определено описание.
        """
        res_filename = self.getReportResourceFilename(report_filename, self.getReportDir())
        report_res = self.loadReportResource(res_filename)
        description = report_res.get('description', u'') if report_res and report_res.get('description', None) else report_filename
        return strfunc.toUnicode(description)
