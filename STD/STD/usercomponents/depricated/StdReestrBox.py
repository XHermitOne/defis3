#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Картотека реестров (StdReestrBox). Хранение в ODB(ObjectStorageSource).

StdReestrBox (MetaTree <DirStorage> )
|
+-->StdReestr (MetaItem <FileStorage>)
       |
       +-->StdReestrFolder (MetaItem <FileNodeStorage>)
              |
              StdReestrObj (MetaItem <FileNodeStorage>)
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import ic.PropertyEditor.icDefInf as icDefInf
from STD import reestr_img
from ic.components.user import ic_metaitem_wrp
import ic.engine.ic_user as ic_user

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CReestrBox')

ic_class_spc = {'name':'defaultPanel',
                'type':'StdReestrBox',
                'source':'reestr_storage',
                'pic':None, #Образ метакомпонента
                'pic2':None, #Дополнительный образ метакомпонента
                'nest':'MetaTree:ReestrBox',
                'can_contain':None,     #Разрешающее правило для типов документов
                'can_not_contain':None, #Запрещающее правило для типов документов
                '__attr_types__': {icDefInf.EDT_CHOICE:['source']},
                '__lists__':{'nest':['MetaTree:ReestrBox'],
                            'source':ic_user.get_res_name_list('odb')},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}
                
ic_class_pic = reestr_img.DocJournal
ic_class_pic2 = reestr_img.DocJournal
                
ic_can_contain = ['StdReestr']
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'report': None, 'storage_type': u'DirStorage', 'spc': {}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'source': u'reestr_storage', 'init': None, 'can_not_contain': None, 'type': u'MetaTree', 'description': None, '_uuid': u'f5d0db1eac3184b7c02d61f90b163df9', 'child': [], 'can_contain': u'None', 'edit_form': None, 'name': u'ReestrBox', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 2, 5)
###END SPECIAL BLOCK

class CReestrBox(ictemplate.icTemplateInterface):
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
        #   Доопределяем спецификацию
        self._init_spc(component)
        
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        # Имя MetaItem делаем таким же как и имя реестра, т.к. у MetaTree типы
        # узлов определяются по именам.
        self.resource['name'] = component['name']
        #self.resource['_uuid'] = component['_uuid']
        self.resource['description'] = component['description']
        self.resource['can_contain'] = component['can_contain']
        self.resource['can_not_contain'] = component['can_not_contain']
        
    def _init_spc(self, component):
        """
        Доопределяет спецификацию до нужного вида. Добаляются атрибуты
        'storage_type', 'container'.
        """
        component['storage_type'] = ic_metaitem_wrp.DIR_STORAGE_TYPE
        component['container'] = True
        
        if not component['pic']:
            component['pic'] = ic_class_pic
        if not component['pic2']:
            component['pic2'] = ic_class_pic2
            
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource

    def _build_resource(self):
        """
        Собирает ресурс из ресурса компонента и ресурса шаблона.
        """
        if self._templRes and 'child' in self._templRes:
            chld = self.resource['child']
            self.resource = copy.deepcopy(self._templRes)
            
            # Преобразуем дерево компонентов в список компонентов.
            # Для того, чтобы MetaTree правильно собрался
            ch = []
            for el in chld:
                if 'child' in el and el['child']:
                    ch += el['child']
                    el['child'] = []
            chld += ch
            
            # Ищем гнездо для вставления дочерних элементов (считаем, что у
            # нас односвязные компоненты)
            if chld and self._nest[1]:
                res = self._findres(self.GetResource(), self._nest[1], self._nest[0])
                
                if res:
                    optLst = list(set(res.keys()) & set(icDefInf.icContainerAttr))
                    
                    if optLst:
                        res[optLst[0]] = chld

        return self.resource
        
    def getReestrNameLst(self):
        """
        Возвращает список имен реестров.
        """
        regLst = self.GetContext()['_interfaces'].values()
        print('---------------> REG_LST=', regLst)
        lst = [x.name for x in regLst if x.type == 'StdReestr']
        return lst
        
    def init_component(self, context=None):
        """
        """
        #db_root = self.getRegObj('StorageE2')
        db_root = self.getRegObj(self.name)
        
        if not db_root.keys():
            lst = self.getReestrNameLst()
            print('---------------> LST=', lst)
            for el in lst:
                obj = db_root.Add('f'+el, el)
                #obj.Add('2006', 'YearZtr')
            
        db_root.closeStorage()
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CReestrBox.
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