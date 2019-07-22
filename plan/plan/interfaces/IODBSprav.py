#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Справочник модмификаций планов.
"""

import wx

import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
import ic.utils.system_cache as ic_cache

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'can_contain': None, 'storage_type': u'DirStorage', 'spc': {}, 'gen_new_name': None, 'description': None, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'source': u'sprav_odb_storage', 'init': None, 'can_not_contain': None, 'type': u'MetaTree', 'res_module': None, 'const_spc': {}, '_uuid': u'81cd9be2dafc884e8de8d142488b3612', 'child': [{'activate': 1, 'pic': None, 'can_contain': u'None', 'storage_type': u'FileStorage', 'spc': {'modifications': []}, 'gen_new_name': None, 'description': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0439 \u0441\u0438\u0441\u0442\u0435\u043c \u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'res_module': None, 'const_spc': {}, '_uuid': u'6d8e2593d15d77e374c43446c53e057a', 'child': [], 'report': None, 'edit_form': None, 'name': u'planModif', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}], 'report': None, 'edit_form': None, 'name': u'Sprav', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 1, 1, 1)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IODBSprav'
#   Идентификатор справочника модификаций планов
id_modif_sprav = 'Modif'


class IODBSprav(icobjectinterface.icObjectInterface):
    def __init__(self, parent):
        """
        Конструктор интерфейса.
        """
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
            
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK


def getModifLst(bBuff=False, plan_sys=id_modif_sprav):
    """
    Возвращает список, описывающий модификации плана:
        [[<идентификатор плана>, <описание модификации>, <расположение>,
            <описание структуры модификации>], ...]
    Модификация описывается списком состоящим из перечисления типов узлов плана.
    Порядок в списке задает также порядок включения узлов.
        Пример: ['maetaplan_tree', 'mYear', 'mMonth', 'mVidProd', 'mReg', 'mMenager']
        
    @type bBuff: C{bool}.
    @param bBuff: Признак разрешающий брать значения из буфера.
    @param plan_sys: Имя системы планирования, определяет имя хранилища, где
            будут храниться описания модификаций планов.
    """
    if bBuff and ic_cache.systemCache.hasObject(ic_class_name, plan_sys):
        buff = ic_cache.systemCache.get(ic_class_name, plan_sys)
        if buff:
            return buff
        
    cls = IODBSprav(None)
    sprav = cls.getObject()
    
    if plan_sys in sprav:
        #   Сохраняем в системном буфере
        ic_cache.systemCache.add(ic_class_name, plan_sys, sprav[plan_sys].value.modifications)
        return sprav[plan_sys].value.modifications


def getModifPlanStructById(id_modif, bBuff=False):
    """
    Возвращает структуру модификации плана по идентификатору плана.
    
    @param id_modif: Идентификатор плана.
    @type bBuff: C{bool}.
    @param bBuff: Признак разрешающий брать значения из буфера.
    """
    lst = getModifLst(bBuff)
    
    if lst:
        for r in lst:
            if r[0] == id_modif:
                return r[3]


def test(par=0):
    """
    Тестируем класс new_form.
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
