# PyReditor - Advanced Python Regular Expresion Editor
#
# Copyright (c) 2008, 2009
# Primoz Cermelj <primoz.cermelj@gmail.com>
#
# This program is based on RegexEditor.plug-in.py plugin originated from
# Boa Constructor and is licensed under GPL.
# 
# See LICENSE.TXT for license terms.
#----------------------------------------------------------------------------
"""
This module implements basic saving of the .cfg file as well as of RE and/or
text (string) for the PyReditor program.
"""

from configobj import ConfigObj
from validate import Validator
from .commons import RE_FLAGS
import re
import os

_FLAGS = dict([(it[0], 0) for it in RE_FLAGS.items()])


class Settings:
    """Reading, saving,... of settings for an application."""
    def __init__(self, fname, defkeys=None, autoload=True):
        self._fname = fname
        self._defkeys = defkeys
        # a ConfigObj instance
        self._keys = ConfigObj(self._fname, configspec=defkeys, raise_errors=True,
                               create_empty=False, write_empty_values=True,
                               stringify=True)
        if autoload:
            self.load()
            
    def has_section(self, section):
        if section in self._keys:
            if isinstance(self._keys[section], dict):
                return True
        return False
    
    def has_key(self, section, key):
        res = False
        if section in self._keys:
            try:
                return not isinstance(self._keys[section][key], dict)
            except:
                pass
        return res
    
    def get(self, section, key, defvalue=None, t='s'):
        """If defvalue is None, the key must exist or an error will be
        raised. Types supported:
            s - string (default)
            f - float
            i - integer
        """
        if defvalue != None:
            if not self.has_key(section, key):
                val = defvalue
            else:
                val = self._keys[section][key]
        else:
            val = self._keys[section][key]
        if t.lower() == 'f': val = float(val)
        elif t.lower() == 'i': val = int(val)
        return val
    
    def getkeys(self, section):
        return self._keys[section].dict()
    
    def getallkeys(self):
        return self._keys.dict()
    
    def getsecnames(self):
        return self._keys.dict().keys()
    
    def getkeynames(self, section):
        return self._keys[section].dict().keys()
    
    def set(self, section, key=None, value=''):
        """If the key does not exist, it adds it."""
        if key != None:
            self._keys[section].update({key: value})
        else:
            self._keys[section] = {}
            
    def update(self, opts):
        """Updates the options dictionary opts representing all the options
        in general.
        """
        self._keys.update(opts)
        
    def save(self):
        self._write()
    
    def load(self):
        """Loads/reloads the inifile."""
        self._read()
        
    def exists(self):
        return os.path.exists(self._fname)
    
    def _read(self):
        # Reads contents into self._keys
#        if not self.exists():
#            raise SettException('Settings file %s does not exist' % self._fname)
        ex_keys = self._keys.dict()
        self._keys.reload()
        self._keys.merge(ex_keys)
        if self._defkeys != None:
            validator = Validator()
            test = self._keys.validate(validator, copy=False)
        
    def _write(self):
        # Write self._keys
        validator = Validator()
        # Use copy below in order to force not to set defaults for missing keys
        # and enabling writing of such keys. But, copy=True removes comments.
        if self._defkeys != None:
            test = self._keys.validate(validator, copy=False)
        self._keys.indent_type = ''
        self._keys.write()
        
        
class ProjFile(Settings):
    """Simple "project" management class to load/save a project file. The
    classical "CFG syntax" (aka INI files) is used for this.
    
    The project can be saved (and read of course) in an ASCII file with either:
        1. [re] section, "re" key and some additional (non-mandatory) keys, and
           with an optional [text] section with the "text" key, or
        2. as a simple ASCII file where the whole contents is assumed being
           a re.
           
    When saving, the first option is always used, while for loading the second
    option is accepted as well.
    """
    def __init__(self, fname):
        Settings.__init__(self, fname, defkeys=None, autoload=False)
    
    def load(self):
        """Loads the contents of the project file and returns:
            (re, reflags, text).

        If reflags are not available, they will be set to 0 (default). If text
        is not available or empty, None will be returned.
        """
        # No merging as in the parent class Settings
        self._keys.reload()
        reflags = _FLAGS.copy()     # default reflags
        action = 0
        text = None                 # default text
        re = None
        if self.has_section('re'):
            re = self.get('re', 're', defvalue='', t='s')
            for flag in reflags:
                reflags[flag] = self.get('re', flag, defvalue=0, t='i')
            action = self.get('re', 'action', defvalue=0, t='i')
            if action < 0 or action > 2:
                action = 0
        else:
            re = self._raw_read()
        if self.has_section('text'):
            text = self.get('text', 'text', defvalue='', t='s')
        if text == '':
            text = None
        return (re, reflags, text, action)
            
    def save(self, re, reflags=None, text=None, action=0):
        self._keys.clear()
        self._keys['re'] = {}
        self._keys['text'] = {}
        self._keys['re']['re'] = str(re)
        if reflags != None:
            for flag in reflags:
                self.set('re', flag, int(reflags[flag]))
        self.set('re', 'action', action)
        if text != None:
            self.set('text', 'text', text)
        Settings.save(self)
        
    def _raw_read(self):
        data = None
        try:
            fh = open(self._fname, 'r')
            data = fh.read()
            fh.close()
        except:
            raise Exception('Error reading %s' % self._fname)
        return data


class Templates(Settings):
    """Simple "templates" management class to load templates."""
    def __init__(self, fname):
        Settings.__init__(self, fname, defkeys=None, autoload=False)
    
    def load(self):
        """Loads all the templates and returns a dictionary of items - the
        same shape as the M_ITMES has. Optional icon is a string used to
        "add" icons to the menu items. \t string will be converted to a tab
        character.
        """
        # Loads a file with re templates and returns a dictionary of template
        # items in the form the insertitems are given (see EditInsertMenu in
        # menus.py or M_ITEMS in commmons.py), i.e., in the form used in this
        # class to create "insert-like" menus.

        self._keys.reload()
        menu_items = {}
        
        patt = re.compile(r'\\t')
        
        # Get all the sections = sub-menus
        try:
            menus = self._keys.keys()
            for menu in menus:
                # Get icon name
                if 'icon' in self._keys[menu]:
                    icon = self.get(menu, 'icon', defvalue='', t='s')
                else:
                    icon = None
                if icon == '': icon = None
                # Get all the menu items (sub-sections)
                items = self._keys[menu].keys()
                items_d = {}
                k = 0
                for item in items:
                    if isinstance(self._keys[menu][item], dict):
                        # subsection found, read the keys
                        caption = self._keys[menu][item]['caption']
                        caption = re.sub(patt, '\t', caption)
                        template = self._keys[menu][item]['template']
                        id = '%s_%s_%d' % (menu, item, k)
                        k += 1
                        items_d.update({id: [caption, False, template, None]})
                d = {menu: [icon, items_d]}
                menu_items.update(d)
        except:
            menu_items = None

        return menu_items

