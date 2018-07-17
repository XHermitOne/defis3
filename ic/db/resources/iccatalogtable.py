#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
import copy

### !!!! NO CHANGE !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource={'activate': 1, 'obj_module': None, 'table': None, 'style': 0, 'alias': None, 'source': (('PostgreSQLDB', 'links_pgs_db', None, 'links_pgs_db.src', 'tutorial'),), 'import': None, 'type': 'Table', 'res_module': u'catalog_tab.py', 'init_expr': None, 'description': None, '_uuid': '0fc0384e41392d7f710683849079c287', 'child': [{'default': u'', 'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'field': u'path', '_uuid': 'e2e02118560b86453d87041e870319ba', 'type_val': u'T', 'attr': 0, 'len': -1, 'label': u'path', 'alias': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'path'}, {'default': None, 'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'alias': None, '_uuid': '989f5bba832d775442da04ca3d382220', 'type_val': 'T', 'attr': 0, 'len': -1, 'label': u'pobj', 'field': u'pobj', 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'pobj'}, {'default': None, 'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'alias': None, '_uuid': '098c830dfa6cfed140fbee7f0098dab6', 'type_val': 'T', 'attr': 0, 'len': -1, 'label': '', 'field': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'otype'}, {'default': None, 'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'alias': None, '_uuid': '242d54b7d70d544b1074d33ea44fc941', 'type_val': 'T', 'attr': 0, 'len': -1, 'label': '', 'field': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'title'}, {'default': None, 'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'alias': None, '_uuid': '662f61f00cc679f0c4f3ee4dd6bee31d', 'type_val': 'T', 'attr': 0, 'len': -1, 'label': '', 'field': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'description'}, {'default': None, 'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'alias': None, '_uuid': '6149bd4125460b11d219b6e2d0a7c692', 'type_val': u'D', 'attr': 0, 'len': -1, 'label': '', 'field': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'reg_time'}, {'default': None, 'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'alias': None, '_uuid': '75a31f4b1a45d5cfbc434218a2b61bc5', 'type_val': u'D', 'attr': 0, 'len': -1, 'label': '', 'field': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'act_time'}, {'style': 0, 'activate': 1, 'obj_module': None, 'description': u'\u041f\u0443\u0442\u044c \u0434\u043e \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0438', 'idx': None, 'alias': None, 'default': None, '_uuid': 'b64f70d0fe0d72ebc678dacb0449088a', 'type_val': 'T', 'attr': 0, 'len': -1, 'label': '', 'field': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'pic'}, {'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'field': None, 'default': None, '_uuid': '2884907440f846f77e113fd93f3d619f', 'type_val': 'T', 'attr': 0, 'len': -1, 'label': '', 'alias': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'security'}, {'style': 0, 'activate': 1, 'obj_module': None, 'description': '', 'idx': None, 'alias': None, 'default': None, '_uuid': '8509fe116ddbd2c08b812e3fd884ef19', 'type_val': 'T', 'attr': 0, 'len': -1, 'label': '', 'field': None, 'dict': {}, 'init_expr': None, 'component_module': None, 'res_module': None, 'type': 'Field', 'store': None, 'name': u'data'}], 'scheme': None, 'name': u'catalog', 'idx': None, 'filter': None, 'component_module': None}

#   Version
__version__ = (1, 0, 0, 8)
###END SPECIAL BLOCK

#   Class name
ic_class_name = 'CatalogTable'

class CatalogTable(icobjectinterface.icObjectInterface):
    def __init__(self, parent, src=None, table=None):
        """ Constructor.
        @param scr: Паспорт источника данных.
        """
        #
        res = copy.deepcopy(resource)
        if src:
            res['source'] = src
            if table:
                res['table'] = table
        
        #   Base class constructor
        icobjectinterface.icObjectInterface.__init__(self, parent, res)
            
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Test CatalogResource class.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Test code #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()
    
    