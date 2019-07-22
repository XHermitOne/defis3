#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
import copy
from ic.bitmap import ic_bmp
import analitic.markalg.mapMark as mapMark
import analitic.interfaces.IStdIndicatorPanel as IStdIndicatorPanel
import plan.browsers as brws
import ic.storage.objstore as objstore

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'metatype': None, 'pic': None, 'can_contain': u"WrapperObj.can_containFuncmMonth('metadata_plan')", 'storage_type': u'DirStorage', 'spc': None, 'description': None, 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'source': u'monitor_storage', 'init': None, 'can_not_contain': None, 'type': u'MetaTree', 'const_spc': {'aggregate_ctrl': {'analitic': {'summa_path': [u'year', u'month', u'vidprod', u'reg', u'mens'], 'date_flags': [False, True, True, True, True], 'date_field': u'dtoper', 'description': u'\u0420\u0435\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f'}, 'zayavki': {'summa_path': [u'year', u'month', u'vidprod', u'reg', u'mens'], 'date_flags': [False, True, True, True, True], 'date_field': u'dtoper', 'description': u'\u0417\u0430\u044f\u0432\u043a\u0438'}, 'pay': {'summa_path': [u'year', u'month', u'vidprod', u'reg', u'mens'], 'date_flags': [False, True, True, True, True], 'date_field': u'dtoper', 'description': u'\u041e\u043f\u043b\u0430\u0442\u0430'}}}, '_uuid': u'3c29d5fd7018130c520f17d61aeccb2b', 'child': [{'activate': 1, 'metatype': None, 'pic': None, 'can_contain': u"WrapperObj.can_containFuncmMonth( 'mYear')", 'storage_type': u'DirStorage', 'spc': {'analitic': {'summa': [0, 0]}, 'ei': u'', 'description': u'2005 (\u0433\u043e\u0434\u043e\u0432\u043e\u0439 \u043f\u043b\u0430\u043d)', 'summa': 0, 'pay': {'summa': [0, 0]}, 'zayavki': {'summa': [0, 0]}, 'w': 1, 'w_kol': 1, 'marja': 0.20000000000000001, 'kol': 1}, 'description': u'\u0413\u043e\u0434\u043e\u0432\u043e\u0439 \u043f\u043b\u0430\u043d', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': u"prnt = self.getItemParent()\nmaxYear = 0\n\r\nif self.value.name.startswith('default'):\n    for y in prnt.keys():\n        try:\n            if int(y) > maxYear:\n                maxYear = int(y)\n        except:\n            pass\n    \n    if maxYear == 0:\n        maxYear = 2004\n    \n    self.rename(str(maxYear+1))\n\r\n_resultEval = True", 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {'color_zones': [(u'40%', u'RED'), (u'50%', (255, 200, 0)), (u'100%', (0, 180, 50))], 'factor': 1000000}, '_uuid': u'4e0fe3ca5c4ed523dce8559406964623', 'child': [], 'report': None, 'edit_form': u'plan.interfaces.IYearEdtPanel.IYearEdtPanel', 'name': u'mYear', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'metatype': None, 'pic': u'WrapperObj.getPic_mMonth(self)', 'report': None, 'storage_type': u'FileStorage', 'spc': {'analitic': {'summa': [0, 0]}, 'ei': u'', 'kol': 1, 'summa': 0, 'decadWeightKol': [1, 1, 1], 'w_kol': 1, 'zayavki': {'summa': [0, 0]}, 'decadWeight': [1, 1, 1], 'w': 1, 'pay': {'summa': [0, 0]}, 'marja': 0.20000000000000001, 'description': u'\u042f\u043d\u0432\u0430\u0440\u044c'}, 'description': u'\u041c\u0435\u0441\u044f\u0447\u043d\u044b\u0439 \u043f\u043b\u0430\u043d', 'style': 0, 'container': True, 'component_module': None, 'pic2': u'WrapperObj.getPic2_mMonth(self)', 'init': u"import plan.plan_service as serv\r\nprnt = self.getItemParent()\r\nmaxMnth = 0\r\n\r\nif not self.value.name.startswith('m'):\r\n    for y in prnt.keys():\r\n        try:\r\n            if int(y[1:3]) > maxMnth:\r\n                maxMnth = int(y[1:3])\r\n        except:\r\n            pass\r\n    \r\n    if maxMnth >= 12:\r\n        _resultEval = False\r\n    else:\r\n        codMnth = 'm'+('00'+str(maxMnth+1))[-2:]\r\n        \r\n        self.rename(codMnth)\r\n        self.value.description = serv.monthFileNameDict[codMnth]\r\n        _resultEval = True\r\nelse:\r\n    _resultEval = True", 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {'sprav': u'Months', 'color_zones': [(u'40%', u'RED'), (u'50%', (255, 200, 0)), (u'100%', (0, 180, 50))], 'factor': 1000000}, '_uuid': u'03ece0d8d3e7586f16788df1de38cb80', 'child': [], 'can_contain': u"WrapperObj.can_containFuncmMonth( 'mMonth')", 'edit_form': u'plan.interfaces.IAspectEdtPanel.IAspectEdtPanel', 'name': u'mMonth', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'metatype': None, 'pic': u'WrapperObj.getPic_mVidProd(self)', 'report': None, 'storage_type': u'FileNodeStorage', 'spc': {'analitic': {'summa': [0, 0]}, 'ei': u'', 'kol': 1, 'summa': 0, 'decadWeightKol': [1, 1, 1], 'pay': {'summa': [0, 0]}, 'zayavki': {'summa': [0, 0]}, 'decadWeight': [1, 1, 1], 'w': 1, 'w_kol': 1, 'marja': 0.20000000000000001, 'description': u'\u0412\u0438\u0434 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438'}, 'description': u'\u041f\u043b\u0430\u043d \u043f\u043e \u0432\u0438\u0434\u0443 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438', 'style': 0, 'container': True, 'component_module': None, 'pic2': u'WrapperObj.getPic2_mVidProd(self)', 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {'field': u'codt', 'sprav': u'Product', 'color_zones': [(u'40%', u'RED'), (u'50%', (255, 200, 0)), (u'100%', (0, 180, 50))], 'factor': None}, '_uuid': u'c3d3c631bd85beec46137dac09e7588a', 'child': [], 'can_contain': u"WrapperObj.can_containFuncmMonth( 'mVidProd')", 'edit_form': u'plan.interfaces.IAspectEdtPanel.IAspectEdtPanel', 'name': u'mVidProd', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'metatype': None, 'pic': u'WrapperObj.getPic_mReg(self)', 'can_contain': u"WrapperObj.can_containFuncmMonth( 'mReg')", 'storage_type': u'FileNodeStorage', 'spc': {'analitic': {'summa': [0, 0]}, 'ei': u'', 'kol': 1, 'summa': 0, 'decadWeightKol': [1, 1, 1], 'pay': {'summa': [0, 0]}, 'zayavki': {'summa': [0, 0]}, 'decadWeight': [1, 1, 1], 'w': 1, 'w_kol': 1, 'marja': 0.20000000000000001, 'description': u'\u0420\u0435\u0433\u0438\u043e\u043d'}, 'description': u'\u041f\u043b\u0430\u043d \u043f\u043e \u0440\u0435\u0433\u0438\u043e\u043d\u0443', 'style': 0, 'container': True, 'component_module': None, 'pic2': u'WrapperObj.getPic2_mReg(self)', 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {'field': u'reg', 'sprav': u'Region', 'color_zones': [(u'40%', u'RED'), (u'50%', (255, 200, 0)), (u'100%', (0, 180, 50))], 'factor': None}, '_uuid': u'2c9e5a65848ba1ac4b0e40dbaffb2a01', 'child': [], 'report': None, 'edit_form': u'plan.interfaces.IAspectEdtPanel.IAspectEdtPanel', 'name': u'mReg', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'metatype': None, 'pic': u'WrapperObj.getPic_mMenager(self)', 'can_contain': u"WrapperObj.can_containFuncmMonth( 'mMenager')", 'storage_type': u'FileNodeStorage', 'spc': {'analitic': {'summa': [0, 0]}, 'ei': u'', 'kol': 1, 'summa': 0, 'decadWeightKol': [1, 1, 1], 'pay': {'summa': [0, 0]}, 'zayavki': {'summa': [0, 0]}, 'decadWeight': [1, 1, 1], 'w': 1, 'w_kol': 1, 'marja': 0.20000000000000001, 'description': u'\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440'}, 'description': u'\u041f\u043b\u0430\u043d \u043f\u043e \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u0443', 'style': 0, 'container': True, 'component_module': None, 'pic2': u'WrapperObj.getPic2_mMenager(self)', 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {'field': u'mens', 'sprav': u'Menager', 'color_zones': [(u'40%', u'RED'), (u'50%', (255, 200, 0)), (u'100%', (0, 180, 50))], 'factor': None}, '_uuid': u'7d43dc6168080c4a1d06920116a7a0d8', 'child': [], 'report': None, 'edit_form': u'plan.interfaces.IAspectEdtPanel.IAspectEdtPanel', 'name': u'mMenager', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}], 'report': None, 'edit_form': None, 'name': u'metadata_plan', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 5, 3)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IMetaplan'

#   Описание структуры базового плана
basePlanDict = {'root': ['mYear'],
                'metadata_plan': ['mYear'],
                'mYear': ['mMonth'],
                'mMonth': ['mVidProd'],
                'mVidProd': ['mReg'],
                'mReg': ['mMenager'],
                'mMenager': []}

basePlanLst = ['metadata_plan',
               'mYear',
               'mMonth',
               'mVidProd',
               'mReg', 'mMenager']


class IMetaplan(icobjectinterface.icObjectInterface):
    def __init__(self, parent=None, forms=None, pics=None):
        """
        Конструктор интерфейса.
        """
        #   Пользовательские данные
        self._userData = None
        
        #   Словарь, описывающий структуру плана
        self.plan_struct_lst = basePlanLst
        
        #   Указатель на менаджер планов
        self.planMenager = None
        
        #   Список, описывающий структуру плана (упращенная форма описания,
        #   используемая пользователем - определяет последовательность вложений
        #   аспектов плана)
        self.plan_struct_dict = basePlanDict
        
        # Находим ссылку на описания метатипа
        self.res = copy.deepcopy(resource)
        
        if forms or pics:
            if not forms:
                forms = {}
            if not pics:
                pics = {}
            
            #   Получаем список объектов у которых будем изменять ресурс
            lst = list(set(forms.keys()) | set(pics.keys()))
            print('>>>>> Object List:', lst)
            for name in lst:
                res = self.GetObjectResource(nameObj=name, typeObj='MetaItem',  resource=self.res)

                if name in forms.keys():
                    res['edit_form'] = forms[name]
                    
                if name in pics.keys():
                    res['pic'], res['pic2'] = pics[name]

        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, self.res)

        #   Папка базового плана
        self._baseStorageName = self.getObject().getStorage().getNodeDir()
        # print('..... _baseStorageName=', self._baseStorageName)
        
    ###BEGIN EVENT BLOCK
    
    def getPic_mMonth(self, metaObj):
        """
        Атрибут <pic> на узлах mMonth.
        """
        data = self.GetUserData()
        if data and data['mode'] == 'monitoring':
            # print(' >>> getObject=', self.getObject())
            st = IStdIndicatorPanel.getMonitorState(metaObj)
            # print('>>> Node state:', st)
            return mapMark.getStateImage('calendar.gif', st)
        else:
            return ic_bmp.getUserBitmap('calendar.gif', 'plan')

    def getPic2_mMonth(self, metaObj):
        """
        Атрибут <pic2> на узлах mMonth.
        """
        # return lib.GetUserBitmap('calendar.gif', 'plan')
        return self.getPic_mMonth(metaObj)

    def getPic_mVidProd(self, metaObj):
        """
        Атрибут <pic> на узлах mVidProd.
        """
        data = self.GetUserData()
        if data and data['mode'] == 'monitoring':
            st = IStdIndicatorPanel.getMonitorState(metaObj)
            return mapMark.getStateImage('product.gif', st)
        else:
            return ic_bmp.getUserBitmap('product.gif', 'plan')

    def getPic2_mVidProd(self, metaObj):
        """
        Атрибут <pic2> на узлах mVidProd.
        """
        # return lib.GetUserBitmap('product.gif', 'plan')
        return self.getPic_mVidProd(metaObj)

    def getPic_mReg(self, metaObj):
        """
        Атрибут <pic> на узлах mReg.
        """
        data = self.GetUserData()
        if data and data['mode'] == 'monitoring':
            st = IStdIndicatorPanel.getMonitorState(metaObj)
            return mapMark.getStateImage('region.gif', st)
        else:
            return ic_bmp.getUserBitmap('region.gif', 'plan')

    def getPic2_mReg(self, metaObj):
        """
        Атрибут <pic2> на узлах mReg.
        """
        # return lib.GetUserBitmap('region.gif', 'plan')
        return self.getPic_mReg(metaObj)

    def getPic_mMenager(self, metaObj):
        """
        Атрибут <pic> на узлах mMenager.
        """
        data = self.GetUserData()
        if data and data.has_key('mode') and data['mode'] == 'monitoring':
            st = IStdIndicatorPanel.getMonitorState(metaObj)
            return mapMark.getStateImage('human.gif', st)
        else:
            return ic_bmp.getUserBitmap('human.gif', 'plan')
        
    def getPic2_mMenager(self, metaObj):
        """
        Атрибут <pic2> на узлах mMenager.
        """
        # return lib.GetUserBitmap('human.gif', 'plan')
        return self.getPic_mMenager(metaObj)

    def can_containFuncmMonth(self, metatype):
        """
        Функция обрабатывает событие <?>.
        """
#        data = self.GetUserData()
#
#        #   Определяем идентификатор текущей модификации плана
#        if data and data.has_key('browserInterface'):
#            modif_plan_id = data['browserInterface'].getModifPlanId()
#        else:
#            modif_plan_id = None
        if self.planMenager:
            modif_plan_id = self.planMenager.getModifPlanId()
        else:
            modif_plan_id = None

        if modif_plan_id in (None, '__base__') and metatype in basePlanDict:
            # print '<base plan>:', basePlanDict[metatype]
            return basePlanDict[metatype]
        elif modif_plan_id:
            lst = self.planMenager.getCanContainLst(modif_plan_id, metatype)
            # lst = brws.getCanContainLst(modif_plan_id, metatype)
            # print '<modif plan id=%s>: %s' % (modif_plan_id, str(lst))
            return lst
#        else:
#            #print '<> ********** <> can_containFuncmMonth', "['mVidProd']"
#            return ['mVidProd']
        
    ###END EVENT BLOCK

    def GetUserData(self):
        """
        Возвращает пользоваетельские данные.
        """
        return self._userData
    
    def SetUserData(self, data):
        """
        Привязывает пользовательские данные к браузеру.
        """
        self._userData = data
        
    def setPlanMenager(self, menager):
        """
        Устанавливает менеджер планов.
        """
        self.planMenager = menager
        
    def setMetaplanById(self, id=None):
        """
        Возвращает указатель на базовый либо модифицированный план.
        
        @rtype: C{ic.components.user.ic_metatree_wrp.icMetaTree}
        @return: Возвращает указатель на базовый план.
        """
        if self.planMenager:
            return self.planMenager.setMetaplanById(id)
#        if self._baseStorageName:
#            if id in (None, '__base__'):
#                storage_name = self._baseStorageName
#            else:
#                storage_name = self._baseStorageName+'_'+id
#
#            metatree = self.getObject()
#            object_storage = objstore.CreateObjectStorageByDir(storage_name)
#            metatree.setStorage(object_storage)
#            return metatree


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
