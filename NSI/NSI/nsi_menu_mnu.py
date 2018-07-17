#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource module <C:/defis/NSI/NSI/nsi_menu.mnu>.
"""
### RESOURCE_MODULE: C:/defis/NSI/NSI/nsi_menu.mnu
# -----------------------------------------------------------------------------
# Name:        C:/defis/NSI/NSI/nsi_menu_mnu.py
# Purpose:     Resource module.
#
# Author:      <...>
#
# Created:
# RCS-ID:      $Id: $
# Copyright:   (c)
# Licence:     <your licence>
# -----------------------------------------------------------------------------
### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0,0,0,1)

import ic

def show_hlp_sprav(*arg, **kwarg):
#    frm = ic.metadata.NSI.frm.test_nsi_form.create()
#    frm.Show()
    sprav_manager = ic.metadata.NSI.mtd.nsi_sprav.create()
    sprav = sprav_manager.getSpravByName('Registr')
    # Удаляем RU19
    pfx = 'RU19'
    print('deleting branch:%s ...' % pfx)
    sprav.getStorage().delRecByCod(pfx)
    print('delete branch:', pfx)
    addRec(sprav, pfx, {'name':u'Республика Хакасия'})
    print('add root cod:', pfx)
    for reg in range(1, 21):
        cod = '%s%04d09' % (pfx, reg)
        print('cod:', cod)
        addRec(sprav, cod, {'name':'name_%s' % cod})
        for cd in range(2000, 2010):
            cod = '%s%04d09%s' % (pfx, reg, cd)
            print('  ->cod:', cod)
            addRec(sprav, cod, {'name':'name_%s' % cod})
            for num in range(5000):
                cod = '%s%04d09%s%05d' % (pfx, reg, cd, num)
                print('    ->cod:', cod)
                addRec(sprav, cod, {'name':'name_%s' % cod})


def addRec(sprav, cod, RecDict_):
    RecDict_['cod']=cod
    result=sprav.getStorage().addRecDictDataTab(RecDict_)


def admin_sprav_sys(*arg, **kwarg):
    print('********* admin')
    sprav_manager = ic.metadata.NSI.mtd.nsi_sprav.create()
    sprav_manager.Admin()
   

def edit_sprav_menuitem():
    """
    Тестирование редактирования справочника.
    """
    sprav_manager = ic.metadata.NSI.mtd.nsi_sprav.create()
    sprav = sprav_manager.getSpravByName('NSITst')
    if sprav:
        from NSI.nsi_dlg import icspraveditdlg
        icspraveditdlg.edit_sprav_dlg(nsi_sprav=sprav)


def choice_sprav_menuitem():
    """
    Тестирование выбора кода справочника.
    """
    sprav_manager = ic.metadata.NSI.mtd.nsi_sprav.create()
    sprav = sprav_manager.getSpravByName('NSITst')
    if sprav:
        from NSI.nsi_dlg import icspravchoicetreedlg
        icspravchoicetreedlg.choice_sprav_dlg(nsi_sprav=sprav, fields=['s1', 's2', 'n1'])


def set_default_sprav_menuitem():
    """
    Заполнение справочника данными по умолчанию.
    """
    print('Start>>>')
    tab = ic.metadata.THIS.tab.nsi_data.create()
    tab.GetManager().set_default_data()
    
    