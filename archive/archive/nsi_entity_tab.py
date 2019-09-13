#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis3/archive/archive/nsi_entity.tab>
File            </mnt/defis/defis3/archive/archive/nsi_entity_tab.py>
Description     <Resource module>
"""

from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/nsi_entity.tab

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 1, 1)

# Коды начиная с 00090 взяты из справочника БАЛАНСА <TYP=257>
DEFAULT_TAB_DATA = (dict(cod='00', name=u'Аян. Головное предприятие'),
                    dict(cod='00001', name=u'Аян. Бухгалтерия'),
                    dict(cod='00002', name=u'Аян. Сбыт'),
                    dict(cod='00003', name=u'Аян. ОМТС'),
                    dict(cod='00004', name=u'Аян. Кадры'),
                    dict(cod='00005', name=u'Аян. Плановый отдел'),
                    dict(cod='00006', name=u'Аян. Цех тары и готовой продукции (Экспедиция)'),
                    dict(cod='00007', name=u'Аян. Маркетинг'),
                    dict(cod='00008', name=u'Аян. Информационный отдел'),
                    dict(cod='00009', name=u'Аян. Юридический отдел'),
                    dict(cod='00010', name=u'Аян. Отдел охраны труда'),
                    dict(cod='00020', name=u'Аян. Отдел экологии'),
                    dict(cod='00030', name=u'Аян. Производственно-технический отдел'),
                    dict(cod='00090', name=u'Аян. Здравпункт'),
                    dict(cod='00110', name=u'Аян. Столовая'),
                    dict(cod='00120', name=u'Аян. Служба безопасности'),
                    dict(cod='00130', name=u'Аян. Транспортный цех'),
                    dict(cod='00140', name=u'Аян. Цех РСУ'),
                    dict(cod='00150', name=u'Аян. Административно-хозяйственный отдел'),
                    dict(cod='00160', name=u'Аян. КИПиА'),
                    dict(cod='00180', name=u'Аян. Лаборатория'),
                    dict(cod='00190', name=u'Аян. РМЦ'),
                    dict(cod='00200', name=u'Аян. Отдел ОГЭ'),
                    dict(cod='00210', name=u'Аян. Бродильно лагерный цех'),
                    dict(cod='00220', name=u'Аян. Варочно-подработачный цех'),
                    dict(cod='00260', name=u'Аян. Цех розлива'),
                    dict(cod='00330', name=u'Аян. Компрессорный цех'),
                    dict(cod='00380', name=u'Аян. Цех розлива минеральной воды'),
                    dict(cod='00390', name=u'Аян. Комплексная бригада слесарей'),

                    dict(cod='01', name=u'Хан-куль'),
                    dict(cod='01001', name=u'Хан-куль. Бухгалтерия'),

                    dict(cod='10', name=u'Аян. АУП'),
                    dict(cod='10010', name=u'Аян. Генеральный директор'),
                    dict(cod='10011', name=u'Аян. Главный инженер'),
                    dict(cod='10012', name=u'Аян. Главный технолог'),
                    dict(cod='10013', name=u'Аян. Главный бухгалтер'),
                    dict(cod='10014', name=u'Аян. Главный энергетик'),
                    dict(cod='10015', name=u'Аян. Начальник ПТО'),
                    dict(cod='10016', name=u'Аян. Начальник штаба ГО'),
                    dict(cod='10019', name=u'Аян. Секретарь-референт'),
                    )


class icNSIEntityTabManager(icmanagerinterface.icWidgetManager):

    def onInit(self, event):
        pass

    def set_default_data(self):
        """
        Установка значений справочника по умолчанию.
        """
        tab = self.get_object()

        # Очистить таблицу
        tab.clear()

        for record in DEFAULT_TAB_DATA:
            record['type'] = 'nsi_entity'
            tab.add(**record)

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icNSIEntityTabManager
