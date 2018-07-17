#!/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Функции-комманды управления процессом изменения конфигурации.
"""

# --- Imports ---
import os
import stat
import os.path
import shutil

from ic.log import log
from ic.log import log_console
from ic.dlg import ic_dlg


#
DEFAULT_V8UNPACK_PATH = os.path.join('v8unpack', 'v8unpack')

CUR_CF_DIR = None


def gen_cf_dir(cf_filename):
    """
    Генерация директории, в которую будет происходить парсинг.
    @param cf_filename: Полное имя CF файла конфигурации 1c.
    """
    return os.path.join(os.path.dirname(cf_filename), os.path.basename(cf_filename).replace('.', '_'))


def run_parser(v8unpack_filename, cf_filename, cf_dirname, txt_ctrl=None):
    """
    Запуск парсера на исполнение.
    @param v8unpack_filename: Полное имя файла парсера.
    @param cf_filename: Файл CF конфигурации.
    @param cf_dirname: Папка в которую будет производиться вывод метаобъектов.
    @param txt_ctrl: Контрол wxTextCtrl для вывода сообщений утилиты парсера.
    @return:  True/False.
    """
    if not os.path.exists(v8unpack_filename):
        log.warning(u'Файл парсера конфигурации 1С <%s> не найден' % v8unpack_filename)
        return False

    # Перед запуском проверить права доступа на запуск утилиты парсера
    if not os.access(v8unpack_filename, os.X_OK):
        os.chmod(v8unpack_filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        log.info(u'Установка прав на исполнение для файла: <%s>' % v8unpack_filename)

    try:
        cmd = '%s -PARSE "%s" "%s"' % (v8unpack_filename, cf_filename, cf_dirname)

        log.info(u'RUN COMMAND: <%s>' % cmd)
        log_console.log_cmd(cmd, txt_ctrl=txt_ctrl)
        return True
    except:
        log.fatal(u'Ошибка выполнения парсинга конфигурационного файла <%s>' % cf_filename)
    return False


def parse_cf_file(cf_filename, cf_dirname=None, txt_ctrl=None):
    """
    Парсинг файла конфигурации 1с.
    @param cf_filename: Полное имя CF файла конфигурации 1c.
    @param cf_dirname: Директория, в которую будет происходить парсинг.
    @param txt_ctrl: Объект wxTxtCtrl для вывода результатов выполнения комманды парсинга.
    """
    try:
        if not os.path.exists(cf_filename):
            log.warning(u'ERROR! CF file <%s> not exists!' % cf_filename)
            ic_dlg.icWarningBox(u'ОШИБКА', u'CF файл <%s> не найден!' % cf_filename)
            return
        else:
            if cf_dirname is None:
                global CUR_CF_DIR
                CUR_CF_DIR = gen_cf_dir(cf_filename)
                cf_dirname = CUR_CF_DIR

        if os.path.exists(cf_dirname):
            if not ic_dlg.icAskBox(Title_=u'ВНИМАНИЕ',
                                   Text_=u'Папка <%s> распарсенного файла конфигурации уже существует. Заменить?' % cf_dirname):
                return
            # Удалить папку конфигурации, если она существует
            shutil.rmtree(cf_dirname, True)
            log.info(u'DELETE DIRECTORY: <%s>' % cf_dirname)

        v8unpack_filename = os.path.join(os.path.dirname(__file__), DEFAULT_V8UNPACK_PATH)
        v8unpack_filename = os.path.abspath(v8unpack_filename)
        if not os.path.exists(v8unpack_filename):
            log.warning(u'ERROR! V8Unpack file <%s> not exists!' % v8unpack_filename)
            ic_dlg.icWarningBox(u'ОШИБКА', u'V8Unpack файл <%s> не найден!' % v8unpack_filename)
            return

        run_parser(v8unpack_filename, cf_filename, cf_dirname, txt_ctrl)
    except:
        log.fatal(u'ERROR! Error in parse_cf_file function')
