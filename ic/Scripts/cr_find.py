# -*- coding:utf-8 -*-

# CR Format Test

import os.path

ext_files = ('.py',)


def walk_find_rus(rus_txt, dir_, files_):
    try:
        py_files = [os.path.join(dir_, file_name) for file_name in files_
                    if os.path.splitext(file_name)[1].lower() in ext_files]
            
        for py_file_name in py_files:
            py_file = open(py_file_name, 'rb')
            try:
                f_txt = py_file.read()
                
                if f_txt.find('\r\n') >= 0:
                    write_file = open(py_file_name, 'wb')
                    try:
                        f_txt = f_txt.replace('\r\n', '\n')
                        write_file.write(f_txt)
                        write_file.close()
                    except:
                        write_file.close()
                    print(py_file_name + ' ERROR CR')
                else:
                    pass

                py_file.close()
            except:
                print('ERROR')
                py_file.close()
    except:
        raise


def find_rus_module(dir_):
    """
    @param dir_:
    @return:
    """
    rus = '���������������������������������'
    return os.path.walk(dir_, walk_find_rus, rus)

if __name__ == '__main__':
    find_rus_module('P:\\defis\\ic\\')
    print('OK')
