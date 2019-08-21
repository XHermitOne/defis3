#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс управления MS Agent.
"""
 
# --- Подключение библиотек ---
try:
    import win32com.client
except ImportError:
    print('ImportError pywin32')
    
from ic.log import log

from ic.components import icwidget

# --- Константы ---
CHARACTERS = ['default', 'Merlin']

# --- Спецификации ---
SPC_IC_MSAGENT = {'type': 'MSAgent',
                  'name': 'default',
                  'description': '',    # Описание
                  'character': 'default',   # Персонаж
                  '__parent__': icwidget.SPC_IC_SIMPLE,
                  }


# --- Классы ---
class icMSAgentControl(object):
    """
    Класс управления MS Agent.
    """
    _agent = None   # Объект агента
    
    def __init__(self, spc):
        """
        Конструктор.
        """
        self._character = spc['character']  # Персонаж
        
    def connect(self):
        """
        Соединение с объектом.
        """
        try:
            self._agent = win32com.client.Dispatch('Agent.Control.2')
        except:
            log.fatal(u'В системе не установлен MSAgent')
            self._agent = None
        if self._agent:
            self._agent.Connected = True    # Подключиться к объекту
            # Установить персонажа
            self.setCharacter(self._character)
    
    def disconnect(self):
        """
        Разорвать соединение с объектом.
        """
        self._agent=None
        
    def setCharacter(self, character=None):
        """
        Установить персонажа.
        """
        if character is None and self._character is None:
            self_character ='default'
        if character:
            self._character = character
        
    def loadCharacter(self, character=None):
        """
        Загрузить персонажа.
        """
        self.setCharacter(character)
        
        if self._agent:
            if self._character.lower() == 'default':
                self._agent.Characters.Load()
        
            else:
                self._agent.Characters.Load(self._character, self._character.lower()+'.acs')

    def showCharacter(self, character=None):
        """
        Показать.
        """
        self.setCharacter(character)
        
        if self._agent:
            return self._agent.Characters(self._character).Show()
        return None

    def getCharacter(self, character=None):
        """
        Объект персонажа.
        """
        self.setCharacter(character)
        if self._agent:
            return self._agent.Characters(self._character)
        return None
