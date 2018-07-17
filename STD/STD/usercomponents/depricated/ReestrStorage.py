#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
ODB хранилище реестров.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import ic.PropertyEditor.icDefInf as icDefInf
import ic.engine.ic_user as ic_user
import copy

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CReestrStorage')

ic_class_spc = {'name':'defaultReestr',
                'type':'ReestrStorage',
                'source':'reestr_storage',
                '__attr_types__': {icDefInf.EDT_CHOICE:['source']},
                '__lists__':{'source':ic_user.getPrjRoot().getResNamesByTypes('odb')},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}
ic_can_contain = []

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'can_contain': u"['ReestrType']", 'storage_type': u'DirStorage', 'spc': {}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'source': u'reestr_storage', 'init': None, 'can_not_contain': None, 'type': u'MetaTree', 'description': None, '_uuid': u'f4c22c1e772f1bc8192dd6abff6cf9b4', 'child': [{'activate': 1, 'pic': None, 'can_contain': u"['ReestrFolder', 'ReestrObj']", 'storage_type': u'FileStorage', 'spc': {'data': []}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'description': None, '_uuid': u'dfba4a6a2a4a7526f5620f7916c78c9f', 'child': [], 'report': None, 'edit_form': None, 'name': u'ReestrType', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': None, 'report': None, 'storage_type': u'FileNodeStorage', 'spc': {'data': []}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'description': None, '_uuid': u'20f4a4af6b63670317bdb06c034adb5a', 'child': [], 'can_contain': u"['ReestrFolder', 'ReestrObj']", 'edit_form': None, 'name': u'ReestrFolder', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': None, 'report': None, 'storage_type': u'FileNodeStorage', 'spc': {'data': []}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'description': None, '_uuid': u'35fc0c00afce41626073ee53be16596f', 'child': [], 'can_contain': u'[]', 'edit_form': None, 'name': u'ReestrObj', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}], 'report': None, 'edit_form': None, 'name': u'ReestrTree', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 3, 1)
###END SPECIAL BLOCK

reestr_file_name = 'odb_reestr'
reestr_item_type = 'ReestrType'
folder_item_type = 'ReestrFolder'

class CReestrStorage(ictemplate.icTemplateInterface):
    """
    Описание пользовательского компонента.
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        self.source = component['source']
        
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        #   Указатель на узел, где будет хранится реестр
        self.metaReestr = None
        
        #   Подменяем источник данных
        res = self.GetObjectResource('ReestrTree')
        
        if res:
            res['source'] = self.source
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
        
    def init_component(self, context=None):
        """
        """
        if not context:
            context = self.GetContext()
            
        #   Получаем указатель на хранилище реестра.
        reestr = self.getRegObj('ReestrTree')
        print('##### reestr=', reestr)
        print('>>>>> obj Dict=', self.getRegObjDict(), reestr.keys())
        if reestr_file_name not in reestr:
            obj = reestr.Add(reestr_file_name, reestr_item_type)
            self.metaReestr = obj.Add(self.name, folder_item_type)
        else:
            self.metaReestr = reestr[reestr_file_name][self.name]
            
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CReestrStorage.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()