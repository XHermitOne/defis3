#!/usr/bin/env python
#  -*- coding: cp1251 -*-

# -----------------------------------------------------------------------------
# Name:       log_parser.py
# Purpose:    ������� ������� �����.
#
# Author:     <����������� �.�.>
#
# Created:     8.02.2006
# RCS-ID:
# Copyright:   (c) 2006 Infocentre
# Licence:     $licence:<your licence>$
# -----------------------------------------------------------------------------

"""
������� ������� ����������� �����.
"""
import os
import os.path

#   ������ ������ ��� �����
LogKeyList = ['EXCELNAME','ERROR','REPORT','WARNING']

#   ����������� ������ ����
LogBlockDiv = '==================================='

def getLineKey(line):
    """
    ���������� ���� ������.
    """
    line = line.rstrip()
    for key in LogKeyList:
        if line.startswith(key):
            return key

def stdLogToDict(fileName, bDel=False):
    """
    ������ ����:
        ========================================================
        WARRNING: ���������� C:\!\Ex �� ����������. ������� ��.
        ========================================================
        REPORT: ����������� ���������.
        ...
        
    ��� ������������� � ����������� ������� ->
        {'WARNING':'...',
          'REPORT':'...' ...}
        
    @type fileName: C{string}
    @param fileName: ������ �� ����� �����.
    @type bDel: C{bool}
    @param bDel: ������� �������� ����� ����� ����� ������.
    """
    d = {}
    if os.path.isfile(fileName):
        f = open(fileName)
        
        #   ��������� �� ��������
        txt = ''
        lastKey = None
        
        for line in f:
            key = getLineKey(line)
            
            if key:
                lastKey = key
                txt += ':'.join(line.split(':')[1:])
            elif lastKey and not line.startswith(LogBlockDiv):
                txt += line
                
            if lastKey and line.startswith(LogBlockDiv):
                d[lastKey] = txt
                txt = ''
                lastKey = None
    
        if lastKey:
            d[lastKey] = txt
    
        f.close()
        
        if bDel:
            os.remove(fileName)
    else:
        d['ERROR'] = '���� ����� %s �� ������.' % fileName
        
    return d
    
def test():
    #  ��������� stdLogToDict
    d = stdLogToDict('V:/pythonprj/icservice/dist/econvert.log')
    print(' .... LogDict:', d)
    
if __name__ == "__main__":
    test()