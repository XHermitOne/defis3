#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Стандартный документ реестра.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import STD.interfaces.reestr.objectInterface as ifs
import ic.PropertyEditor.icDefInf as icDefInf
from STD import reestr_img
import ic.engine.ic_user as ic_user

form_name_lst = ic_user.get_res_name_list('frm')#getPrjRoot().getResNamesByTypes('frm')

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdDoc')

ic_class_spc = {'name':'defaultPanel',
                'type':'StdDoc',
                'nest':'Unit:attributes',
                'edit_form':None,
                'view_form':None,
                '__attr_types__': {icDefInf.EDT_CHOICE:['edit_form', 'view_form']},
                '__lists__':{'nest':['Unit:attributes'],
                             'edit_form':form_name_lst,
                             'view_form':form_name_lst},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}
                
ic_class_pic = reestr_img.Document
ic_class_pic2 = reestr_img.Document
ic_can_contain = ['StdDocSpc','Attribute']
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'style': 0, 'activate': 1, 'name': u'Doc', 'component_module': None, '_uuid': u'493ff84acf1987e07be0415f639c1a85', 'value': None, 'alias': None, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'name': u'StdAttributes', 'component_module': None, '_uuid': u'd2c05060313a682213a15a990552ad26', 'value': None, 'alias': None, 'init_expr': None, 'child': [{'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430 (uuid)', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'cca4f658716ec773cedf0dd4beb6f67f', 'proportion': 0, 'flag': 0, 'name': u'doc_id', 'alias': None, 'init': None, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'border': 0, 'size': (-1, -1)}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0418\u043c\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'2ce76da24a0e94b742c548d3c5d96edd', 'proportion': 0, 'flag': 0, 'name': u'doc_name', 'alias': None, 'init': None, 'init_expr': None, 'child': [], 'position': (-1, -1), 'size': (-1, -1), 'border': 0, 'sprav_type': None}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u041d\u043e\u043c\u0435\u0440 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'28ea37997fc765082e31dee245aee00c', 'proportion': 0, 'name': u'doc_num', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'size': (-1, -1), 'border': 0, 'sprav_type': None}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0414\u0430\u0442\u0430 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'3ddacf7df54b4794109599596d70e99f', 'proportion': 0, 'name': u'doc_date', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'size': (-1, -1), 'border': 0, 'sprav_type': None}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'9824995fabde0888489269efbeae8993', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'size': (-1, -1), 'border': 0, 'name': u'doc_title'}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'1538e5ffd5a731381154d6655297fb04', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'size': (-1, -1), 'border': 0, 'name': u'doc_description'}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'e902fe89cab37e90fb39bcd7b96f42e8', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'size': (-1, -1), 'border': 0, 'name': u'doc_state'}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0414\u0430\u0442\u0430/\u0412\u0440\u0435\u043c\u044f \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'9d8625bbd47ae8fb376763f4145239d5', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'size': (-1, -1), 'border': 0, 'name': u'doc_create_date'}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0414\u0430\u0442\u0430/\u0412\u0440\u0435\u043c\u044f \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f\r\n\u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'a68589e82d5d8fef7af535a28c55fc35', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'size': (-1, -1), 'border': 0, 'name': u'doc_edit_date'}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0410\u0432\u0442\u043e\u0440 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'10cef7d623339ebd197b74d0d8d47efd', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'size': (-1, -1), 'border': 0, 'name': u'doc_author'}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u0412\u043b\u0430\u0434\u0435\u043b\u0435\u0446 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'5ca4377ad802b89aff382acc27b43e91', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'size': (-1, -1), 'border': 0, 'name': u'doc_owner'}, {'attrType': u'text', 'style': 0, 'activate': 1, 'span': (1, 1), 'description': u'\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430', 'component_module': None, 'type': u'Attribute', 'nest': u'Unit:attributes', '_uuid': u'9fa2c2b114aa3d20f25d927dc3dce0e9', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [], 'position': (-1, -1), 'sprav_type': None, 'size': (-1, -1), 'border': 0, 'name': u'doc_note'}], 'type': u'Unit', 'description': u'\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0435 \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u044b \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430'}, {'style': 0, 'activate': 1, 'name': u'attributes', 'component_module': None, '_uuid': u'42d46718e37df3d399af0d64f865d02f', 'value': None, 'alias': None, 'init_expr': None, 'child': [], 'type': u'Unit', 'description': None}], 'type': u'Unit', 'description': None}

#   Версия объекта
__version__ = (1, 0, 3, 7)
###END SPECIAL BLOCK

class CStdDoc(ictemplate.icTemplateInterface, ifs.icBaseReestrObjectInterface):
    """
    Описание пользовательского компонента.
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}: Тип компонента.
        - B{name='default'}: Имя компонента.
        - B{nest='Unit:attributes'}: Гнездо по умолчанию.
        - B{edit_form=''}: Форма редактирования объекта реестра.
        - B{view_form=''}: Форма просмотра объекта реестра.
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        self.editForm = component['edit_form']
        self.viewForm = component['view_form']

        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
                                                
        ifs.icBaseReestrObjectInterface.__init__(self)
        
        #   Стандартные атрибуты
        self.std_attr_res = [x for x in self.GetObjectResource('StdAttributes', 'Unit')['child']]
        self.std_attr = [x['name'] for x in self.std_attr_res]

        #   Дополнительные артибуты
        self.add_attr_res = [x for x in self.GetObjectResource('attributes', 'Unit')['child']]
        self.add_attr = [x['name'] for x in self.add_attr_res]
        
        self.attr_res = self.std_attr_res + self.add_attr_res
        self.attr = self.std_attr + self.add_attr
        
        #   Инициализируем атрибуты документа
        for el in self.attr:
            setattr(self, el, None)
        
        #   Инициализируем спецификацию
        
        #   Курсор - указатель на объект хранения
        self.metaitem = None
        #   Буфер данных
        self._buff = None
        
    def init_component(self, context=None):
        """
        Инициализация компонента. Вызывается парсером после создания компонента.
        """
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
        
    def GetEditForm(self):
        """
        Возвращает форму редактирования.
        """
        return self.editForm
        
    def GetViewForm(self):
        """
        Возвращает форму просмотра.
        """
        return self.viewForm
    
    def init_doc(self, metaitem=None):
        """
        инициализация документа.
        """
        pass
        
    def add_doc(self, metaitem=None):
        """
        Добавление документа в хранилище.
        """
        pass
        
    def select(self, metaitem=None):
        """
        Находит и загружает содержимое документа из хранилища по идентификатору
        документа.
        """
        if metaitem:
            self.metaitem = metaitem
            
        self._buff = data_dct = self.metaitem.value.data
        self.doc_id = self.metaitem.value.name
        #self._buff['doc_id'] = self.doc_id = self.metaitem.value.name

        for el in self.attr:
            if data_dct and el in data_dct.keys():
                setattr(self, el, data_dct[el])

    def update(self, metaitem=None):
        """
        Обновляет содержимое документа.
        """
        if not metaitem:
            metaitem = self.metaitem
            
        if self.metaitem and not self.IsLock():
            if self.doc_id <> self._buff:
                pass
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CStdDoc.
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