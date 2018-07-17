#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Функции тестирования функционала основных классов подсистемы WORKFLOW.
Author(s): Колчанов А.В.
"""

# Version
__version__ = (0, 0, 0, 1)

#--- Imports ---
import ic

from . import test_icworkobj
from . import test_icregister

#--- Constants ---
THIS_PRJ_DIR=ic.utils.ic_file.DirName(ic.utils.ic_file.GetCurDir())

#--- Functions ---
def test_all():
    """
    Запустить все тесты.
    """
    try:
        #Сразу установить режим отладки для отображения всех
        #вспомогательных сообщений
        ic.utils.ic_mode.setDebugMode()

        print('LOGIN PROJECT:',THIS_PRJ_DIR)
        if ic.Login('tester','',THIS_PRJ_DIR,True):
            print('LOGIN - OK')
            print('ENVIRONMENT:')
            ic.printEnvironmentTable()
            print('START ALL TESTS...')
            test_icworkobj.testComponent()
            test_icregister.testComponent()
            test_icregister.testComponentAccumulating()
            print('...STOP ALL TESTS')
        else:
            print('LOGIN - FAILED')
        ic.Logout()
    except:
        ic.Logout()
        raise    
    
if __name__=='__main__':
    test_all()
