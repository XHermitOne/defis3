#!/usr/bin/env python
# -*- coding: cp1251 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! ������ ���� �������� �� ������������� !!!!
###BEGIN SPECIAL BLOCK
#   ��������� �������� ������
resource={'activate': 1, 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'description': None, 'onClose': None, '_uuid': '5e6455a9c5728678c5e459766c5ccb35', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': 'defaultWindow_1204', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   ������ �������
__version__ = (1, 0, 0, 4)
###END SPECIAL BLOCK

#   ��� ������
ic_class_name = 'new_form'

class new_form(icobjectinterface.icObjectInterface):
    def __init__(self, parent):
        """
        ����������� ����������.
        """
        #
        
        #   �������� ����������� �������� ������
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
            
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    ��������� ����� new_form.
    """
    pass
    
if __name__ == '__main__':
    test()