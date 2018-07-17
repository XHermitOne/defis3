#!/usr/bin/env python
#  -*- coding: utf-8 -*-
'''
Пакет прикладной системы АВТОМАТИЗАЦИИ БИЗНЕСС ПРОЦЕССОВ 
    или ОРГАНИЗАЦИИ ДЕЛОПРОИЗВОДСТВА.
    
    Основные понятия:
    =================
    БИЗНЕС-ОБЪЕКТ (WorkObj) - абстрактный регистрируемый объект.
    БИЗНЕС-ПРОЦЕСС (WorkFlow) - процесс делопроизводства, 
    отражающий изменение информации о неком бизнес-объекте во времени.
    ДОКУМЕНТ (Document) - информация, отражающая изменение состояния или
    информации о бизнес-объекте. Документ является управляющей структурой 
    бизнес процесса.
    СПЕЦИФИКАЦИЯ ДОКУМЕНТА (DocSpc) - табличная часть документа. В документе м.б.
    несколько спецификаций.
    ЗАДАЧА (WorkTask) - регистрируемый набор действий, направленных на 
    преобразование информации об бизнесс объекте. Задача состоит из операций и
    реализует транзакционный механизм управления выполнением операций.
    ОПЕРАЦИЯ (Operation) - одно логическое действие по изменению информации о
    бизнес-объекте. Выполнение операции автоматически регистрируется в системе.
    РЕГИСТРАТОР (WorkLog) - объект, регистрируемый выполнение задач и операций 
    в системе.
    РЕКВИЗИТ (Requisite) - информационный элемент документа, операции или 
    спецификации документа.
    СВЯЗАННЫЙ ОБЪЕКТ (LinkObj) - реквизит, который в качестве значения хранит
    указатель/ссылку на абстрактный файл, который не может быть помещен в БД.
    
    Объектная модель:
    =================
    где 
        1. -* : Отношение агрегирования
        2. ->, <-, ^, v : Отношение наследования
    
    +----------+
    |icWorkFlow|
    +----------+
        |
        |   +---------+
        +---*icWorkObj|
        |   +---------+
        |   
        |   +----------+
        +---*icDocument|<-----------------------+
        |   +----------+    +-------------------+
        |       |           v                   |
        |       |    +-----------+              |
        |       +----*icRequisite*--+           |           Класс icWorkBase является базовым 
        |       |    +------*----+  |       +----------+    абстрактным классом организации 
        |       |      |    |       |       |icWorkBase|    бизнесс процесса.
        |       |      v    +-----+ |       +----------+
        |       |    +---------+  | |           |
        |       +----*icLinkObj|  | |           |
        |       |    +---------+  | |           |
        |       |           +-----+ |           |
        |       |           |       |           |
        |       |    +--------+     |           |
        |       +----*icDocSpc|<----------------+
        |            +--------+     |            
        |                           |           
        |                           |           
        |    +----------+           |           
        +----*icWorkTask|   +-------+
             +----------+   |
                |           |
                |    +-----------+
                +----*icOperation|
                     +-----------+
    
@version: 0.001
'''

# Версия
__version__ = (0, 0, 0, 1)

