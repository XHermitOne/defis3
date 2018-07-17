#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import ic.utils.util as util


def ConvertRes(old_res_fl, path, ext=None):
    """
    Функция конвертирует и 'режит' ресурсы старых версий в новые.

    @type old_res_fl: C{string}
    @param old_res_fl: Полный путь до ресурса старой версии.
    @type path: C{string}
    @param path: Полный путь до папки, куда положить новые ресурсы.
    """
    pth, fileName = os.path.split(old_res_fl)

    #   Определяем расширение
    if not ext:
        try:
            ext = fileName.split('.')[1]
        except:
            ext = None

    # ---- Проверяем существует ли заданный файл ресурса и директория, куда
    #   будут ложиться файлы сконвертированных ресурсов
    if os.path.isdir(path) and os.path.isfile(old_res_fl):
        res = util.readAndEvalFile(old_res_fl)
        
        for nm in res:
            fn = path + '/%s.%s' % (nm, ext)
            
            if not os.path.isfile(fn):
                f = open(fn, 'wb')
                
                if ext == 'tab':
                
                    #   Удаляем атрибут 'uuid'
                    if 'scheme' in res[nm]:
                        for fld in res[nm]['scheme']:
                            if 'uuid' in fld:
                                fld.pop('uuid')
                                
                    txt = '{\'%s\': %s}' % (nm, str(res[nm]))
                    txt = txt.replace('scheme', 'child').replace('icField', 'Field').\
                        replace('icLink', 'Link').replace('icDataClass', 'Table')
                else:
                    txt = '{\'%s\': %s}' % (nm, str(res[nm]))
                    
                f.write(txt)
                f.close()
                print('>>> Write new resource file:', fn)
            else:
                print('### File always %s exist!' % fn)
            
    return True


if __name__ == '__main__':
    ConvertRes('C:/!/res/resource.ftl', 'C:/!/res')
