#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import sys
import os
import os.path

from ic.utils import resfunc
from ic.utils import toolfunc


__version__ = (0, 1, 1, 1)

PRJ_NAME = 'work_flow'


def LogLastError(beg_msg, logType=0, msg_encoding='utf-8'):
    """
    Записывает сообщение о последней ошибке в лог.

    :type beg_msg: C{string}
    :param beg_msg: Заголовок сообщения об ошибке.
    :type logType: C{int}
    :param logType: Тип лога (0 - консоль, 1 - файл, 2 - окно лога, 3 - окно сообщений)
    """
    trace = traceback.extract_tb(sys.exc_traceback)
    ltype = sys.exc_type
    last = len(trace) - 1
    msg = ''

    if last >= 0:
        lt = trace[last]
        if not isinstance(beg_msg, str):
            beg_msg = str(beg_msg)  # msg_encoding
        msg = beg_msg + u' in file: %s, function: %s, line: %i, text: \n%s\ntype:%s\ncomments:%s' % (lt[0], lt[2], lt[1],
                                                                                                 lt[3], str(ltype),
                                                                                                 str(sys.exc_info()))
        print(msg)

    return msg


def _toUnicodeResourcePyWalk(args, CurDir_, CurNames_):
    # Отфильтровать только файлы py
    py_files = [x for x in [os.path.join(CurDir_, x) for x in CurNames_] if os.path.isfile(x) and os.path.splitext(x)[1] == '.py']

    for py_file in py_files:
        f = None
        text = u''
        try:
            f = open(py_file, 'rt')
            text = f.read()
            f.close()
        except:
            print('ERROR open file', py_file)
            if f:
                f.close()

        n1 = text.find('###BEGIN')
        n = text.find('resource=')
        n_x = text.find('resource =')
        n2 = text.find('###END')
        if n1 > 0 and n2 > 0 and n > 0:
            n_ = text[n:].find('\n')
            replace_dict_txt = text[n+len('resource='):n+n_].strip()
            try:
                replace_dict = eval(replace_dict_txt)
                x_dict = toolfunc.recodeStructStr(replace_dict, 'cp1251', 'UNICODE')
                new_text = text.replace(replace_dict_txt, str(x_dict))
                print('>>', py_file, ' : ', x_dict)
                try:
                    f = open(py_file, 'w')
                    f.write(new_text)
                    f.close()
                except:
                    print('ERROR open file', py_file)
                    f.close()
            except:
                print('Error read', py_file, ' : ', replace_dict_txt)
        elif n1 > 0 and n2 > 0 and n_x > 0:
            print('!>', py_file)


def toUnicodeResourcePy():
    """
    Перекодировать все ресурсы в py файлах в unicode.
    """
    scan_dir = '/home/xhermit/develop/rep_py/rep_py/work/defis/%s/%s/' % (PRJ_NAME, PRJ_NAME)
    return os.walk(scan_dir, _toUnicodeResourcePyWalk, ())


RESOURCE_EXT = ['.frm', '.mtd', '.tab', '.src', '.mnu', '.odb', '.win', '.acc']


def _toUnicodeResourceWalk(args, CurDir_, CurNames_):
    # Отфильтровать только файлы ресурсов
    res_files = [x for x in [os.path.join(CurDir_, x) for x in CurNames_] if os.path.isfile(x) and os.path.splitext(x)[1].lower() in RESOURCE_EXT]

    for res_file in res_files:
        f = None
        text = u''
        try:
            f = open(res_file, 'rb')
            text = f.read()
            f.close()
        except:
            print('ERROR open file', res_file)
            if f:
                f.close()

        replace_dict_txt = text.strip()
        try:
            replace_dict = eval(replace_dict_txt)
            x_dict = toolfunc.recodeStructStr(replace_dict, 'cp1251', 'UNICODE')
            new_text = str(x_dict)
            print('>>', res_file, ' : ', x_dict)
            try:
                f = open(res_file, 'wt')
                f.write(new_text)
                f.close()
            except:
                print('ERROR open file', res_file)
                f.close()
        except:
            print('Error read', res_file, ' : ', replace_dict_txt)


def toUnicodeResource():
    """
    Перекодировать все ресурсы в unicode.
    """
    scan_dir = '/home/xhermit/develop/rep_py/rep_py/work/defis/%s/%s/' % (PRJ_NAME, PRJ_NAME)
    return os.walk(scan_dir, _toUnicodeResourceWalk, ())


def toUnicodeProject():
    pro_file = '/home/xhermit/develop/rep_py/rep_py/work/defis/%s/%s/%s.pro' % (PRJ_NAME, PRJ_NAME, PRJ_NAME)
    replace_dict = resfunc.loadResourcePickle(pro_file)
    x_dict = toolfunc.recodeStructStr(replace_dict, 'cp1251', 'UNICODE')
    print('>>', pro_file, ' : ', x_dict)
    ok = resfunc.saveResourcePickle(pro_file, x_dict)
    print('OK:', ok)

    
if __name__ == '__main__':
    toUnicodeProject()
