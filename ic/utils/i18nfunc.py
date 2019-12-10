#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Dependancies
import os
import wx
from wx.lib import langlistctrl as langlist
import wx.adv
import glob
from . import resource


__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_i18n.py 50147 2007-11-22 07:44:22Z CJP $'
__revision__ = '$Revision: 50147 $'
__version__ = (0, 1, 1, 1)

# ----------------------------------------------------------------------------
# Global Variables
OPT_NO_OP = 0
OPT_DESCRIPT = 1
LANG_DIR = resource.icGetICPath()+os.sep+'locale'
PROG_NAME = 'restree'
# ----------------------------------------------------------------------------


# ---- Helper Functions used by the classes in this module ----
def GetAvailLocales():
    """
    Gets a list of the available locales that have been installed
    for the editor. Returning a list of strings that represent the 
    canonical names of each language.
    :return: list of all available local/languages available

    """
    avail_loc = list()
    loc = glob.glob(os.path.join(LANG_DIR, '*'))
    for path in loc:
        the_path = os.path.join(path, 'LC_MESSAGES', PROG_NAME + '.mo')
        if os.path.exists(the_path):
            avail_loc.append(os.path.basename(path))
    return avail_loc


def GetLocaleDict(loc_list, opt=OPT_NO_OP):
    """Takes a list of cannonical locale names and by default returns a 
    dictionary of available language values using the canonical name as 
    the key. Supplying the Option OPT_DESCRIPT will return a dictionary
    of language id's with languages description as the key.
    :param loc_list: list of locals
    @keyword opt: option for configuring return data
    :return: dict of locales mapped to wx.LANGUAGE_*** values

    """
    lang_dict = dict()
    for lang in [x for x in dir(wx) if x.startswith('LANGUAGE')]:
        loc_i = wx.Locale(wx.LANGUAGE_DEFAULT).\
                          GetLanguageInfo(getattr(wx, lang))
        if loc_i:
            if loc_i.CanonicalName in loc_list:
                if opt == OPT_DESCRIPT:
                    lang_dict[loc_i.Description] = getattr(wx, lang)
                else:
                    lang_dict[loc_i.CanonicalName] = getattr(wx, lang)
    return lang_dict


def GetLangId(lang_n):
    """Gets the ID of a language from the description string. If the 
    language cannot be found the function simply returns the default language
    :param lang_n: Canonical name of a language
    :return: wx.LANGUAGE_*** id of language
    
    """
    lang_desc = GetLocaleDict(GetAvailLocales(), OPT_DESCRIPT)
    return lang_desc.get(lang_n, wx.LANGUAGE_DEFAULT)


# ---- Language List Combo Box----
class LangListCombo(wx.adv.BitmapComboBox):
    """
    Combines a langlist and a BitmapComboBox
    """
    def __init__(self, parent, id_, default=None):
        """
        Creates a combobox with a list of all translations for the
        editor as well as displaying the countries flag next to the item
        in the list.

        :param default: The default item to show in the combo box
        """
        lang_ids = GetLocaleDict(GetAvailLocales()).values()
        lang_items = langlist.CreateLanguagesResourceLists(langlist.LC_ONLY,
                                                           lang_ids)
        wx.adv.BitmapComboBox.__init__(self, parent, id_,
                                       size=wx.Size(250, 26),
                                       style=wx.CB_READONLY)
        for lang_d in lang_items[1]:
            bit_m = lang_items[0].GetBitmap(lang_items[1].index(lang_d))
            self.Append(lang_d, bit_m)

        if default:
            self.SetValue(default)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.PySimpleApp(False)
    # Print a list of Cannonical names usefull for seeing what codes to
    # use when naming po files
    for lang in [x for x in dir(wx) if x.startswith('LANGUAGE')]:
            loc_i = wx.Locale(wx.LANGUAGE_DEFAULT).\
                              GetLanguageInfo(getattr(wx, lang))
            if loc_i:
                print(loc_i.CanonicalName)
