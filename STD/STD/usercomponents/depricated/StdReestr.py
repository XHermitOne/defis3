#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Страндартный древовидный реестр. Классификатор хранится в
ODB(ObjectStorageSource) хранилище.

StdReestr (MetaItem <FileStorage>)
|
+-->StdReestrFolder (MetaItem <FileNodeStorage>)
        |
       StdReestrObj (MetaItem <FileNodeStorage>)

"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
from STD import reestr_img
from ic.components.user import ic_metaitem_wrp
import ic.engine.ic_user as ic_user
import ic.components.icResourceParser as prs
import ic.utils.resource as resmod
import ic.PropertyEditor.icDefInf as icDefInf

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdReestr')

ic_class_spc = {'name':'defaultReestr',
                'type':'StdReestr',
                'nest':'MetaItem:Reestr',
                'doc_type':None, #Тип документа
                'view_form':None, #Форма чтения/просмотра
                'edit_form':None, #Форма редактирования/записи
                'max_level':-1, #Максимальное количество уровней 
                'report':None, #Форма печати/отчет
                'pic':None, #Образ метакомпонента
                'pic2':None, #Дополнительный образ метакомпонента
                'can_contain':None,     #Разрешающее правило для типов документов
                'can_not_contain':None, #Запрещающее правило для типов документов
                '__attr_types__': {icDefInf.EDT_NUMBER:['max_level']},
                '__lists__':{'nest':['MetaItem:Reestr'],
                            'doc_type':ic_user.get_names_in_res_by_types(('mtd',), ('StdDoc','Document'))},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

ic_class_pic = reestr_img.imgReestr
ic_class_pic2 = reestr_img.imgReestr
ic_can_contain = ['StdReestrFolder','StdReestrObj']

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'can_contain': u'None', 'storage_type': u'FileStorage', 'spc': {'data': []}, 'description': u'', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {}, '_uuid': u'f9cec909d909d09e14a8ad831eb75e06', 'child': [], 'report': None, 'edit_form': None, 'name': u'Reestr', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 2, 8)
###END SPECIAL BLOCK

pic_script = """@from STD import reestr_img
return reestr_img.imgReestr
"""

class CStdReestr(ictemplate.icTemplateInterface):
    """
    Описание пользовательского компонента.
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='StdReestr'}: Тип компонента.
        - B{name='default'}: Название компонента.
        - B{source=None}: Имя OODB источника данных, где будет хранится дерево реестра.
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
        
        #   Определяе максимальное количество уровней вложения в реестр
        try:
            self.max_level = int(component['max_level'])
        except:
            self.max_level = -1
        
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        # Имя MetaItem делаем таким же как и имя реестра, т.к. у MetaTree типы
        # узлов определяются по именам.
        self.resource['name'] = component['name']
        #self.resource['_uuid'] = component['_uuid']
        self.resource['description'] = component['description']
        self.resource['can_contain'] = component['can_contain']
        self.resource['can_not_contain'] = component['can_not_contain']
        self.resource['pic'] = pic_script
        self.resource['pic2'] = pic_script
        # Создаем документ
        self._creat_doc(evalSpace)
            
    def _creat_doc(self, evalSpace):#, bCounter, progressDlg):
        """
        Функция создает объект документа.
        """
        if not self.doc_type in (None,'None', ''):
            #print '>>>------------------- Reestr Doc_type=', self.doc_type
            res = resmod.icGetRes(None, 'mtd', nameRes=self.doc_type)
            ifs = prs.icBuildObject(None, res, evalSpace = evalSpace, bIndicator=False)
            if not ifs.GetComponentInterface():
                self.doc = ifs
            else:
                self.doc = ifs.GetComponentInterface()
        
            #print '>>> Reestr Doc=', self.doc
    def _init_spc(self, component):
        """
        Доопределяет спецификацию.
        """
        component['storage_type'] = ic_metaitem_wrp.FILE_STORAGE_TYPE
        component['container'] = True
        
#        if not component['pic']:
#            component['pic'] = ic_class_pic
#        if not component['pic2']:
#            component['pic2'] = ic_class_pic2
        
        if component['can_contain'] == None and component['can_not_contain'] == None:
            component['can_contain'] = [x['name'] for x in component['child'] if 'name' in x]
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
        
    def init_component(self, context=None):
        """
        """
#        # Получаем указатель на родительский интерфейс
#        ifs = self.GetComponentInterface()
#        print '------------> ifs=', ifs, ifs.name, context['_dict_obj'].keys()
#        db_root = ifs.getRegObj(ifs.name)
#        print '------------> db_root:', db_root
#        if not db_root.keys():
#            obj = db_root.Add('f'+self.name, self.name)
#            #obj.Add('2006', 'YearZtr')
#        db_root.closeStorage()
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CStdReestr.
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