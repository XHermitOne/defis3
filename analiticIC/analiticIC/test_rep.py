#!/usr/bin/env python3
#  -*- coding: cp1251 -*-
"""
������ ���������� �������.
�����(�): 
"""

# ������
__version__ = (0, 0, 0, 1)

#--- �������
import wx
from ic.dlg import ic_dlg

def getSQLTest():
    """
    ����������� SQL ������� ��� ��������� ������.
    """
    print 'getSQLTest'
    if ic_dlg.icAskDlg('������','?')==wx.YES:
        return 'SQL SELECT * FROM nsi_list'
    else:
        return 'SQL SELECT * FROM nsi_std'
