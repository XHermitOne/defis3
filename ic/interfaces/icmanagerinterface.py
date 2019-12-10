#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Базовый класс управления программными объектами.
"""

import wx

from ic.log import log


__version__ = (0, 1, 1, 1)


class icManagerInterface(object):
    """
    Класс управления компонентом.
    """
    def __init__(self):
        """
        Конструктор. Без параметров.
        """
        # Объект управления
        self.obj = None
        # self.Init()
        wx.CallAfter(self.PostInit)

    def set_object(self, obj):
        """
        Управляемый менеджером объект.
        """
        self.obj = obj

    def get_object(self):
        """
        Управляемый менеджером объект.
        """
        if self.obj is None:
            log.warning(u'Не определен управляемый объект для менеджера <%s>' % self.__class__.__name__)
        return self.obj

    def GetObject(self, name):
        """
        Доступ к объекту контекста.
        """
        return self.obj.GetObject(name)

    def Init(self):
        """
        Функция инициализации.
        """
        pass

    def PostInit(self):
        """
        Функция отрабатывает после создания объекта и всех дочерних элементов.
        """
        pass

    def get_metadata(self):
        return self.context['metadata']

    metadata = property(get_metadata)

    def get_context(self):
        return self.obj.context

    context = property(get_context)

    def bform(self, name, parent, subsys='THIS'):
        """
        """
        bname = '_%s' % name
        if getattr(self, bname, None):
            return getattr(self, bname)
        else:
            sub = getattr(self.metadata, subsys)
            frm = getattr(sub.frm, name).create(parent=parent)
            setattr(self, bname, frm)
        return frm


class icWidgetManager(icManagerInterface):
    """
    Класс управления компонентами.
    """
    def __init__(self):
        icManagerInterface.__init__(self)
