#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Мастер создания пользовательского компонента.
"""

import wx

from ic.log import log

try:
    from . import create_component_wizard_proto
except ImportError:
    import create_component_wizard_proto


class icCreateComponentWizard(create_component_wizard_proto.icCreateComponentWizardProto):
    """
    Мастер создания пользовательского компонента.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        :param args:
        :param kwargs:
        """
        create_component_wizard_proto.icCreateComponentWizardProto.__init__(self, *args, **kwargs)


def show_create_component_wizard(parent=None):
    """
    Функция отображения мастера создания компонента.

    :param parent: Родительское окно для визарда.
    :return:
    """
    try:
        if parent is None:
            parent = wx.GetApp().GetTopWindow()
        wizard = icCreateComponentWizard(parent=parent)
        wizard.RunWizard(wizard.base_wizPage)
    except:
        log.fatal(u'Ошибка мастера создания компонента')


def test():
    """
    Функция тестирования.

    :return:
    """
    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None)
    show_create_component_wizard(parent=frame)
    app.MainLoop()


if __name__ == '__main__':
    test()
