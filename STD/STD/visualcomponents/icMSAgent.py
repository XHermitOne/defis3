#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Класс управления MS Agent.
"""
 
#--- Подключение библиотек ---
try:
    import win32com.client
except ImportError:
    print('ImportError pywin32')
    
from ic.log import ic_log

from ic.components import icwidget

#--- Константы ---
CHARACTERS=['default','Merlin']

#--- Спецификации ---
SPC_IC_MSAGENT={
    'type': 'MSAgent',
    'name': 'default',
    'description':'',    #Описание
    'character':'default', #Персонаж
    '__parent__':icwidget.SPC_IC_SIMPLE,
    }
#--- Функции ---

#--- Классы ---
class icMSAgentControl:
    """
    Класс управления MS Agent.
    """
    _agent=None #Объект агента
    
    def __init__(self,Spc_):
        """
        Конструктор.
        """
        self._character=Spc_['character'] #Персонаж
        
    def connect(self):
        """
        Соединение с объектом.
        """
        try:
            self._agent=win32com.client.Dispatch('Agent.Control.2')
        except:
            ic_log.icLogErr(u'В системе не установлен MSAgent')
            self._agent=None
        if self._agent:
            self._agent.Connected=True #Подключиться к объекту
            #Установить персонажа
            self.setCharacter(self._character)
    
    def disconnect(self):
        """
        Разорвать соединение с объектом.
        """
        self._agent=None
        
    def setCharacter(self,Character_=None):
        """
        Установить персонажа.
        """
        if Character_ is None and self._character is None:
            self_character='default'
        if Character_:
            self._character=Character_
        
    def loadCharacter(self,Character_=None):
        """
        Загрузить персонажа.
        """
        self.setCharacter(Character_)
        
        if self._agent:
            if self._character.lower()=='default':
                self._agent.Characters.Load()
        
            else:
                self._agent.Characters.Load(self._character,self._character.lower()+'.acs')

    def showCharacter(self,Character_=None):
        """
        Показать.
        """
        self.setCharacter(Character_)
        
        if self._agent:
            return self._agent.Characters(self._character).Show()
        return None

    def getCharacter(self,Character_=None):
        """
        Объект персонажа.
        """
        self.setCharacter(Character_)
        if self._agent:
            return self._agent.Characters(self._character)
        return None