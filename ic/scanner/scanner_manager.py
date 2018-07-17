#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Система управления запуском внешней
программы сканирования документов icScanner.
"""

import os
import os.path
import wx
from . import config
# from ic.kernel import io_prnt
from ic.log import log

__version__ = (0, 0, 3, 1)


class icScannerManager(object):
    """
    Класс менеджера управления запуском внешней
    программы сканирования документов icScanner.
    """

    def __init__(self, scanner_exec_filename=None):
        """
        Конструктор.
        @param scanner_exec_filename: Полный путь до исполняемого файла <icscanner.py>.
            Если не определен, то берется из конфигурационного файла.
        """
        self._scanner_exec_filename = config.get_glob_var('DEFAULT_SCANNER_EXEC_FILENAME') if scanner_exec_filename is None else scanner_exec_filename

    def getScannerExec(self):
        return self._scanner_exec_filename

    def getScanPath(self):
        return config.get_glob_var('DEFAULT_SCAN_PATH')

    def do_scan(self):
        """
        Запуск сканирования документа.
        @return: True/False.
        """
        if os.path.exists(self._scanner_exec_filename):
            cmd = 'python2 %s' % self._scanner_exec_filename
            try:
                log.info(u'Запуск внешней программы <%s>' % cmd)
                os.system(cmd)
                return True
            except:
                log.fatal(u'Запуск программы <icScanner>: <%s>' % cmd)
        else:
            log.warning(u'Запускаемый модуль программы <icScanner> : <%s> не найден' % self._scanner_exec_filename)
        return False

    def do_scan_preview(self):
        """
        Запуск сканирования документа с просмотром результата сканирования.
        @return: True/False.
        """
        if os.path.exists(self._scanner_exec_filename):
            cmd = 'python2 %s --preview' % self._scanner_exec_filename
            try:
                log.info(u'Запуск внешней программы <%s>' % cmd)
                os.system(cmd)
                return True
            except:
                log.fatal(u'Запуск программы <icScanner> в режиме просмотра результата сканирования: <%s>' % cmd)
        else:
            log.warning(u'Запускаемый модуль программы <icScanner> : <%s> не найден' % self._scanner_exec_filename)
        return False

    def do_scan_export(self, scan_filename):
        """
        Запуск сканирования документа с
        сохранением в определенном файле.
        @param scan_filename: Имя файла скана документа.
        @return: True/False.
        """
        if os.path.exists(self._scanner_exec_filename):
            scan_dir = os.path.dirname(scan_filename)
            file_name = os.path.splitext(os.path.basename(scan_filename))[0]
            file_type = os.path.splitext(os.path.basename(scan_filename))[1].replace('.', '').upper()
            cmd = 'python2 %s --scan_dir=%s --file_name=%s --file_type=%s' % (self._scanner_exec_filename,
                                                                              scan_dir, file_name, file_type)
            try:
                log.info(u'Запуск внешней программы <%s>' % cmd)
                os.system(cmd)
                return True
            except:
                log.fatal(u'Запуск программы <icScanner> в режиме экспорта: <%s>' % cmd)
        else:
            log.warning(u'Запускаемый модуль программы <icScanner> : <%s> не найден' % self._scanner_exec_filename)
        return False

    def do_scan_pack(self, *scan_filenames):
        """
        Запуск сканирования пакета документов.
        @param scan_filenames: Список имен файлов документов сканирования 
            с указанием количества страниц каждого документа (не обязательно)  
            и признаком 2-стороннего сканирования (не обязательно).
            Например:
            ('/tmp/scan001.pdf', 2, True), ('/tmp/scan002.pdf', ), ('/tmp/scan003.pdf', 1), ...
        @return: True/False.
        """
        # Проверка корректности входных данных
        if not scan_filenames:
            log.warning(u'Не определен список сканируемых файлов при пакетном сканировании')
            return False
        if not min([type(scan_option) in (list, tuple) for scan_option in scan_filenames]):
            log.warning(u'Ошибка типа входных параметров метода <doc_scan_pack> менеджера сканирования')
            return False        

        # ВНИМАНИЕ! Перед запуском удалить все ранее отсканированные страницы
        full_scan_filenames = [scan[0] for scan in scan_filenames]
        self.deleteScanFiles(*full_scan_filenames)
        
        # Подготовить данные к обработке
        scan_filenames = [(scan, 1, False) if len(scan) == 1 else (tuple(list(scan)+[False]) if len(scan) == 2 else scan) for scan in scan_filenames]        
        if os.path.exists(self._scanner_exec_filename):
            # Папку сканирования и тип файла сканирования определяем по первому файлу
            scan_dir = os.path.dirname(scan_filenames[0][0])
            file_type = os.path.splitext(os.path.basename(scan_filenames[0][0]))[1].replace('.', '').upper()

            filename_list = [os.path.splitext(os.path.basename(scan_filename))[0] for scan_filename, n_page, is_duplex in scan_filenames]
            filenames = ';'.join(filename_list)
            n_pages = ';'.join([str(n_page) + (u'/1' if is_duplex else u'') for scan_filename, n_page, is_duplex in scan_filenames])
            cmd = 'python2 %s --scan_dir=%s --file_type=%s --pack_mode --file_name=\"%s\" --pack_pages=\"%s\"' % (self._scanner_exec_filename,
                                                                                                                  scan_dir,
                                                                                                                  file_type,
                                                                                                                  filenames,
                                                                                                                  n_pages)
            try:
                log.info(u'Запуск внешней программы <%s>' % cmd)
                os.system(cmd)
                return True
            except:
                log.fatal(u'Запуск программы <icScanner>: <%s>' % cmd)
        else:
            log.warning(u'Запускаемый модуль программы <icScanner> : <%s> не найден' % self._scanner_exec_filename)
        return False

    def deleteScanFiles(self, *scan_filenames):
        """
        Удалить файлы сканировани.
        @param scan_filenames: Список имен файлов документов сканирования.
        """
        for scan_filename in scan_filenames:
            if os.path.exists(scan_filename):
                # Удалить старый файл сканирования
                try:
                    os.remove(scan_filename)
                    log.info(u'Удален файл <%s>' % scan_filename)
                except OSError:
                    log.fatal(u'Ошибка удаления файла <%s>' % scan_filename)
            