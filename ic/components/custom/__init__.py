#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет содержит стандартные компоненты.
"""

__version__ = (1, 0, 0, 3)


def icGetModulDict(dct):
    """
    Возвращает словарь модулей системных компонентов.
    """
    #   Словарь модулей системных компонентов
    from . import icnotebook
    from . import icheadergrid
    from . import icheadcell
    from . import ictoolbar
    
    from . import icbutton
    # import ictoggleimagebutton
    from . import icimagebutton
    from . import icgradientbutton
    from . import iccheckbox
    from . import icchoice
    from . import iccombobox
    from . import icgauge
    from . import icradiogroup
    from . import icspinner
    from . import icchecklistbox
    from . import icstaticbox
    from . import icstaticline
    from . import icsplitter
    from . import icstaticbitmap
    from . import icstatictext
    
    dct[icnotebook.ic_class_spc['type']] = icnotebook
    dct[icheadergrid.ic_class_spc['type']] = icheadergrid
    dct[icheadcell.ic_class_spc['type']] = icheadcell
    dct[ictoolbar.ic_class_spc['type']] = ictoolbar
    
    dct[icbutton.ic_class_spc['type']] = icbutton
    # dct[ictoggleimagebutton.ic_class_spc['type']] = ictoggleimagebutton
    dct[icimagebutton.ic_class_spc['type']] = icimagebutton
    dct[icgradientbutton.ic_class_spc['type']] = icgradientbutton
    dct[iccheckbox.ic_class_spc['type']] = iccheckbox
    dct[icchoice.ic_class_spc['type']] = icchoice
    dct[iccombobox.ic_class_spc['type']] = iccombobox
    dct[icgauge.ic_class_spc['type']] = icgauge
    dct[icradiogroup.ic_class_spc['type']] = icradiogroup
    dct[icspinner.ic_class_spc['type']] = icspinner
    dct[icchecklistbox.ic_class_spc['type']] = icchecklistbox
    dct[icstaticbox.ic_class_spc['type']] = icstaticbox
    dct[icstaticline.ic_class_spc['type']] = icstaticline
    dct[icsplitter.ic_class_spc['type']] = icsplitter
    dct[icstaticbitmap.ic_class_spc['type']] = icstaticbitmap
    dct[icstatictext.ic_class_spc['type']] = icstatictext
    return dct

