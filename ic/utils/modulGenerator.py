#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль содержит функции генерации специальных модулей.
"""

import os
import os.path
import wx

from . import resource
from ic.log import log

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

component_template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:

import wx
import ic.interfaces.ictemplate as ictemplate
from ic.utils import util
import copy

### Standart component interface
ictemplate.init_component_interface(globals(), ic_class_name = '%s')

### !!!! Not change block !!!!
###BEGIN SPECIAL BLOCK
#   Object resource
resource=%s

#   Object version
__version__ = %s
###END SPECIAL BLOCK

ic_class_spc = dict({'name': 'defaultPanel',
                     'type': '%s',
                     '__lists__': {'nest': [resource['type']+':'+resource['name']]},
                     '__parent__': ictemplate.SPC_IC_TEMPLATE})

NON_REPLACE_KEYS = ('type',)
REPLACE_SPC_KEYS = [key for key in ic_class_spc.keys() if not key in NON_REPLACE_KEYS and not key.startswith('_')]

class %s(ictemplate.icTemplateInterface):
    \"\"\"
    User component class.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
        - B{type='defaultType'}:
        - B{name='default'}:
    \"\"\"

    component_spc = ic_class_spc
    # resource replace attributes list
    replace_spc_keys = REPLACE_SPC_KEYS
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None, bCounter=False, progressDlg=None):
        \"\"\"
        Interface constructor.
        \"\"\"
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
                
    def _init_template_resource(self):
        \"\"\"
        Init template resource.
        \"\"\"
        self._templRes = resource
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK


def test(par=0):
    \"\"\"
    Test class %s.
    \"\"\"
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    #
    # Test code
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
'''

inherit_component_template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:

import wx
import ic.interfaces.ictemplate as ictemplate
from ic.utils import util
import copy
import %s as parentModule

### Standart component interface
ictemplate.inherit_component_interface(globals(), parentModule, ic_class_name = '%s')

#   Component version
__version__ = (1, 0, 0, 1)

ic_class_spc = dict({'name': 'default',
                     'type': '%s',
                     '__parent__': parentModule.ic_class_spc})

parentClass = getattr(parentModule, parentModule.ic_class_name)


class %s(parentClass):
    \"\"\"
    User component class.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
        - B{type='defaultType'}:
        - B{name='default'}:
    \"\"\"
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None, bCounter=False, progressDlg=None):
        \"\"\"
        Interface constructor.
        \"\"\"
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        parentClass.__init__(self, parent, id, component, logType, evalSpace,
                             bCounter, progressDlg)
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])


def test(par=0):
    \"\"\"
    Test class %s.
    \"\"\"
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    #
    # Test code
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
'''


def GenComponent(componentType, modulName=None, res=None):
    """
    Функция генерирует модуль в интерфейсе компонента системы.
    """
    if not modulName:
        mod_path = resource.icGetResPath()
        if mod_path:
            mod_path = os.path.join(mod_path, 'usercomponents')
            modulName = os.path.join(mod_path, '%s.py' % componentType)
        if mod_path and not os.path.isdir(mod_path):
            # Создаем пакет usercomponents
            from ic.utils import resfunc
            resfunc.createPackage(mod_path)
            log.info(_('INFO') +
                     _('Create package %s') % mod_path)
            wx.MessageBox(_('WARRNING') + '! ' + _('Create package %s') % mod_path)
        elif not mod_path:
            log.info(_('WARRNING') +
                     _('Subsystem component directory <%s> is not found.') % mod_path)
            mod_path = resource.icGetUserClassesPath()
            modulName = os.path.join(mod_path, '%s.py' % componentType)
    
    className = 'C%s' % componentType
    log.info(_('Generate component module: module :%s, type:%s.') % (modulName, componentType))
    text = component_template % (className, str(res), '(1, 0, 0, 1)', componentType, className, className)
    #   Сохраняем сгенерированный текст модуля компонента
    f = open(modulName, 'wt')
    f.write(text)
    f.close()
    wx.MessageBox(_('Component %s  is created successfuly!') % modulName)


def InheritComponent(componentType, parentModule, modulName=None):
    """
    Функция генерирует модуль в интерфейсе компонента системы.
    """
    if not modulName:
        mod_path = resource.icGetResPath()
        if mod_path:
            mod_path = os.path.join(mod_path, 'usercomponents')
            modulName = os.path.join(mod_path, '%s.py' % componentType)
        if mod_path and not os.path.isdir(mod_path):
            # Создаем пакет usercomponents
            from ic.utils import resfunc
            resfunc.createPackage(mod_path)
            log.info(_('INFO') + _('Create package %s') % mod_path)
            wx.MessageBox(_('WARRNING') + '! ' + _('Create package %s') % mod_path)
        elif not mod_path:
            log.info(_('WARRNING') + '! ' + _('Subsystem component directory <%s> is not found.') % mod_path)
            mod_path = resource.icGetUserClassesPath()
            modulName = os.path.join(mod_path, '%s.py' % componentType)
    
    className = 'C%s' % componentType
    log.info(_('Generate component module: modul:%s, type:%s.') % (modulName, componentType))
    text = inherit_component_template % (parentModule,
                                         className,
                                         componentType,
                                         className,
                                         className)
    #   Сохраняем сгенерированный текст модуля компонента
    if not os.path.isfile(modulName):
        f = open(modulName, 'wt')
        f.write(text)
        f.close()
        wx.MessageBox(_('Component %s  is created successfuly!') % modulName)
    else:
        wx.MessageBox(_('Warrning! Module %s already exist!') % modulName, style=wx.ICON_ERROR)


def test1():
    """
    Тест.
    """
    GenComponent('ReestrFolder', 'V:/pythonprj/defis/STD/STD/usercomponents/reestrfolder.py')


def test2():
    """
    Тест.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(0)
    InheritComponent('XPGrid', 'ic.components.user.icsimplegrid')


if __name__ == '__main__':
    test2()
