#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Стандартный объект реестра (StdReestrObj). Наследуется от MetaItem.
Привязка документов производится по атрибуту <doc_type>. Документы должны быть
описаны в метаданных (файл *.mtd) проекта. В этом случае расширенный редактор свойств
позволит выбрать один из описанных документов.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
from STD import reestr_img
from ic.components.user import ic_metaitem_wrp
import ic.PropertyEditor.icDefInf as icDefInf
import ic.engine.ic_user as ic_user
import ic.utils.resource as resmod
import ic.kernel.io_prnt as io_prnt
import ic.components.icResourceParser as prs
import uuid

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdReestrObj')

ic_class_spc = {'name':'defaultObj',
                'type':'StdReestrObj',
                'doc_type':None, #Тип документа
                'pic':None, #Образ метакомпонента
                'pic2':None, #Дополнительный образ метакомпонента
                'can_contain':None,     #Разрешающее правило
                'can_not_contain':None, #Запрещающее правило
                'nest':'MetaItem:ReestrObj',
                '__attr_types__': {icDefInf.EDT_CHOICE:['doc_type']},
                '__lists__':{'nest':['MetaItem:ReestrObj'],
                             'doc_type':ic_user.get_names_in_res_by_types(('mtd',), ('StdDoc','Document'))},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

ic_class_pic = reestr_img.imgReestrObj
ic_class_pic2 = reestr_img.imgReestrObj
ic_can_contain = ['StdReestrFolder','StdReestrObj']

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'can_contain': u'[]', 'storage_type': u'FileNodeStorage', 'spc': {'doc_uuid': None, 'data': {}}, 'const_spc': {}, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'description': None, '_uuid': u'35fc0c00afce41626073ee53be16596f', 'child': [], 'report': None, 'edit_form': None, 'name': u'ReestrObj', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 2, 4)
###END SPECIAL BLOCK

pic_script = """@from STD import reestr_img
return reestr_img.imgReestrObj
"""

class CStdReestrObj(ictemplate.icTemplateInterface):
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
        
        #   Указатель на объект документа
        self.doc = None
        self.doc_type = component['doc_type']
        
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        # Имя MetaItem делаем таким же как и имя реестра, т.к. у MetaTree типы
        # узлов определяются по именам.
        self.resource['name'] = component['name']
        #self.resource['_uuid'] = component['_uuid']
        self.resource['description'] = component['description']
        self.resource['can_contain'] = component['can_contain']
        self.resource['can_not_contain'] = component['can_not_contain']
        self.resource['pic'] = component['pic']
        self.resource['pic2'] = component['pic2']
        self.resource['const_spc']['doc_type'] = self.doc_type
        self.resource['spc'] = {'data':None,'doc_uuid':None}
        self.resource['gen_new_name'] = """GetInterface().gen_reestrobj_id()"""
        
        # Создаем документ
        self._creat_doc(evalSpace)
            
    def _creat_doc(self, evalSpace):#, bCounter, progressDlg):
        """
        Функция создает объект документа.
        """
        if self.doc_type:
            res = resmod.icGetRes(None, 'mtd', nameRes=self.doc_type)
            ifs = prs.icBuildObject(None, res, evalSpace = evalSpace, bIndicator=False)
            #self.doc = ifs.GetComponentInterface()
            if not ifs.GetComponentInterface():
                self.doc = ifs
            else:
                self.doc = ifs.GetComponentInterface()
            
#            self.doc = prs.icResourceParser(None, [res], None, evalSpace = evalSpace,
#                                bCounter = False, progressDlg = None)
            #io_prnt.outLog('=========== Создан документ:%s,%s' % (self.doc_type, self.doc.name))

    def _init_spc(self, component):
        """
        Доопределяет спецификацию.
        """
        component['storage_type'] = ic_metaitem_wrp.FILE_NODE_STORAGE_TYPE
        component['container'] = True
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource

    def gen_reestrobj_id(self):
        """
        Генерируем идентификатор объекта реестра.
        """
        id=str(uuid.uuid1())
        print('>>>--------- REESTROBJ GEN ID:', id)
        return id
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CStdReestrObj.
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