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
Some common constants, functions and classes for PyReditor.
"""

import os
import sys
import wx
import wx.stc
import re


SET_FILE = 'pyreditor.cfg'      # settings file
TEMP_FILE = 'templates.cfg'     # templates file
TITLE = 'PyReditor'             # main frame's title

#---------------------------------------
# Default settings options
#---------------------------------------
SETT_KEYS = {'options':
                {'newline': 'integer(default=1)',
                 'savetext': 'integer(default=1)',
                 'lines_text': 'integer(default=1)',
                 'lines_re': 'integer(default=0)',
                 'autoindent': 'integer(default=0)'},
             'general':
                {'x': 'integer(default=100)',
                 'y': 'integer(default=100)',
                 'maxgroups': 'integer(default=50)',
                 'w': 'integer',
                 'h': 'integer',
                 'sp1': 'integer',
                 'sp2': 'integer',
                 'zoom_re': 'integer(-10, 20, default=0)',
                 'zoom_text': 'integer(-10, 20, default=0)',}
            }

#---------------------------------------
# Menu items for insertions (sub menus):
#     {submenu_name:[icon, {
#         item_name: [text, embrace_selection, insertion, (startsel, sellen)]
#      ...
#        }]
#      ...
#     }
# Use None for (startsel, sellen) if not applicable. When embrace_selection
# is True, the insertion must include %s as well! If icon is None, it will
# not be used.
#
# In TEMP_FILE there are some templates saved which will, essentially,
# be read in and used as additional submenus. Therefore, they will behave
# exactly the same as these, insert submenus/menu items.
#---------------------------------------
M_ITEMS = {'Groups': ['group.png', {
                'group_named': ['(?P<name>...)\tNamed group', True, r'(?P<name>%s)', (4, 4)],
                'group_unnamed':['(...)\tUnnamed group', True, r'(%s)', None],
                'group_non': ['(?:...)\tNon-grouping', True, r'(?:%s)', None],
                'group_set': ['[]\tAny char', True, r'[%s]', (1, 0)],
                'group_setbut': ['[^]\tAny char but', True, r'[^%s]', (2, 0)],
                'group_ilmsux': ['(?iLmsux)\tEmpty (flag set only)', True, r'(?iLmsux%s)', (2, 6)],
                'group_comment': ['(?#...)\tComment (ignored)', True, r'(?#%s)', None],
                'group_range': ['[x-y]\tAny in range', False, r'[x-y]', (1, 3)], 
            }],
            'Repeat': ['repeat.png', {
                'op_*': ['*\tRepeat 0 or more', False, r'*', None],
                'op_*?': ['*?\tRepeat 0 or more (non-greedy)', False, r'*?', None],
                'op_rep1': ['{m}\tRepeat m times', False, r'{m}', (1, 1)],
                'op_rep2': ['{m,}\tRepeat m times or more', False, r'{m,}', (1, 1)],
                'op_rep3': ['{,n}\tRepeat up to n times', False, r'{,n}', (2, 1)],
                'op_rep4': ['{m,n}\tRepeat m to n times', False, r'{m,n}', (1, 1)],
                'op_rep5': ['{m,n}?\tRepeat m to n times (non-greedy)', False, r'{m,n}?', (1, 1)],
                'op_+': ['+\tRepeat 1 or more', False, r'+', None],
                'op_+?': ['+?\tRepeat 1 or more (non-greedy)', False, r'+?', None],
                'op_?': ['?\tRepeat 0 or 1', False, r'?', None],
                'op_??': ['??\tRepeat 0 or 1 (non-greedy)', False, r'??', None],
            }],
            'Conditions': [r'cond.png', {
                'c_ifnext': ['(?=...)\tIF next', True, r'(?=%s)', None],
                'c_ifnotnext': ['(?!...)\tIF NOT next', True, r'(?!%s)', None],
                'c_ifprev': ['(?<=...)\tIF previous', True, r'(?<=%s)', None],
                'c_ifnotprev': ['(?<!...)\tIF NOT previous', True, r'(?<!%s)', None],
                'c_ifpatt': ['(?(id/name)Y|N)\tYES/NO', True, r'(?(id/name)%s)', (3, 7)],
            }],
            'Other': [r'other.png', {
                'op_.': ['.\tMatches any character', False, r'.', None],
                'op_^': ['^\tMatches start of string', False, r'^', None],
                'op_$': ['$\tMatches end of string', False, r'$', None],
                'op_group1': ['\\number\tMathces group #n', False, r'\1', (1,1)],
                'op_group2': ['(?P=name)\tMatches text from group', False, r'(?P=name)', (4, 4)],
                'op_or': ['|\tOR', False, r'|', None],
            }],
            'Special': [r'special.png', {
                'special_00_backs': ['\\\\\tBackslash', False, r'\\', None],
                'special_01_octal': ['\\xxx\tOctal escape', False, r'\000', (1, 3)],
                'special_02_x': ['\\xhh\tHex value', False, r'\x00', (2, 2)],
                'special_03_A': ['\\A\tString start', False, r'\A', None],
                'special_04_a': ['\\a\tBell', False, r'\a', None],
                'special_05_b': ['\\b\tEmpty string (end/start)', False, r'\b', None],
                'special_06_B': ['\\B\tEmpty string', False, r'\B', None],
                'special_07_d': ['\\d\tDecimal digit', False, r'\d', None],
                'special_08_D': ['\\D\tNon-digit', False, r'\D', None],
                'special_09_f': ['\\f\tFormfeed', False, r'\f', None],
                'special_10_n': ['\\n\tNew line', False, r'\n', None],
                'special_11_r': ['\\r\tCarriage Return', False, r'\r', None],
                'special_12_s': ['\\s\tAny white space', False, r'\s', None],
                'special_13_S': ['\\S\tNon-white space', False, r'\S', None],
                'special_14_t': ['\\t\tHorizontal tab', False, r'\t', None],
                'special_15_v': ['\\v\tVertical tab', False, r'\v', None],
                'special_16_w': ['\\w\tAlphanumeric', False, r'\w', None],
                'special_17_W': ['\\W\tNon-alphanumeric', False, r'\W', None],
                'special_18_Z': ['\\Z\tEnd of string only', False, r'\Z', None],
            }]}

#---------------------------------
# 2 colors to display matches in the list and in the editor
#---------------------------------
YELLOW1 = wx.Colour(255, 128, 0)        # "yellow" in the text editor
GREEN1 = wx.Colour(0, 200, 0)           # "green" in the text editor
YELLOW2 = wx.Colour(255, 240, 225)      # "yellow" in the list
GREEN2 = wx.Colour(225, 248, 225)       # "green" in the list

#---------------------------------
# All the re flags that can be set
#---------------------------------
RE_FLAGS = {
    'IGNORECASE':   re.IGNORECASE,
    'LOCALE':       re.LOCALE,
    'MULTILINE':    re.MULTILINE,
    'DOTALL':       re.DOTALL,
    'UNICODE':      re.UNICODE,
    'VERBOSE':      re.VERBOSE
    }

#---------------------------------
# All the custom style ids that can be used for the custom lexer
#---------------------------------
CUSTOM_STYLE_IDS = [\
    wx.stc.STC_P_CLASSNAME,
    wx.stc.STC_P_DECORATOR,
    wx.stc.STC_P_OPERATOR,
    wx.stc.STC_P_NUMBER,
    wx.stc.STC_P_IDENTIFIER,
    wx.stc.STC_P_WORD,
    wx.stc.STC_P_WORD2,
    wx.stc.STC_P_STRING,
    wx.stc.STC_P_COMMENTLINE,
    wx.stc.STC_P_TRIPLE,
    wx.stc.STC_P_DEFNAME
    ]

#---------------------------------
# All the lexers available (all but 'container' which is a custom one that
# needs further implementation).
# Note: hypertext this is for HTML
# Note: 'null', 'automatic' and 'container' are added here and are not supported by
# SetLexerlanguage, instead, SetLexer command needs to be used for them.
#---------------------------------
LEXERS = ['ada', 'ave', 'baan', 'bullant', 'conf', 'cpp', 'tcl', 'nncrontab',
          'eiffel', 'eiffelkw', 'hypertext', 'xml', 'asp', 'php', 'lisp', 'lua',
          'matlab', 'batch', 'diff', 'props', 'makefile', 'errorlist', 'latex',
          'pascal', 'perl', 'python', 'ruby', 'sql', 'vb', 'vbscript',
          'null', 'automatic']

#---------------------------------
# Here, we add the 'container' lexer as well - custom lexer.
#---------------------------------
LEXERS_ALL = ['container'] 
LEXERS_ALL.extend(LEXERS)

#---------------------------------
# Default style
#---------------------------------
STYLE_DEFAULT ={\
     'default':     'face:Courier new,size:10',           # default fonts
     'linenumber':  'back:#C0C0C0,face:Helvetica,size:8', # line numbers
     'controlchar': 'face:new century schoolbook',        # ?
     'bracelight':  'fore:#0000CE,back:#00F400,bold',     # if brace matched
     'bracebad':    'fore:#0000CE,back:#F30000,bold',     # if brace not matched
     }

#---------------------------------
# Custom lexers. The syntax is:
#     [token_name, re_pattern, style]
# If style is None it will be ignored.
# Each token will be a separate RE group and all the groups will be concatenated
# using the OR (|) into the final RE for matching and finally, for "coloring".
# The order below IS therefore important - the order of priority.
#---------------------------------
LEXER_RE =[\
    ['group',
         r'(?:\\[1-9]\d?(?!\d))|(?:(?:\((?:(?:\?<!)|(?:\?<=)|(?:\?=)|(?:\?[:!#])|(?:\?P\<\w+\>)|(?:\?P\=\w+)|(?:\?\(\w+\))|(?:\?[iLmsux]{1,6}(?=\W))?)))|(?:\))',
         r"fore:#0000F3,back:#FFFFFF,bold"],
    ['braces',
        r'(?:[\[\]\{\}])',
        r"fore:#D81CD8,back:#FFFFFF,bold"],
    ['keyword',
        r'(?:\\(?:(?:\d{3})|(?:x[a-fA-F\d]{2})|(?:[aAbBdDsSwWZntrvxf])))|(?:\\\\)',
        r"fore:#FF8306,back:#FFFFFF,bold"],
    ['plain',   # to eliminate operators matching when there is \ in front of it
        r'\\[*+$^.|\?\(\)\[\]\{\}\<\>]',
        None],  # None => no coloring => default
    ['operator',
        r'(?:[*+$^.|])|(?:(?<![\(])\?)',
        r"fore:#CE0000,back:#FFFFFF,bold"]
    ]

# Lexer for the template editor
LEXER_TMPL_EDIT =[\
    ['comment',
         r'(?:#.*)',
         r"fore:#00953C,back:#FFFFFF"],
    ['section',
         r'(?:\s*\[\w+\]\s)',
         r"fore:#800080,back:#FFFFFF,bold"],
    ['subsection',
         r'(?:\s*\[\[\w+\]\]\s)',
         r"fore:#7B7BFF,back:#FFFFFF,bold"],
    ['key',
         r'(?:\s*\w+\s*\=)',
         r"fore:#000000,back:#FFFFFF,bold"],
    ['template',
         r'(?:\s*template\s*\=)',
         r"fore:#000000,back:#FFFFFF,bold"]
    ]
# ...and add the LEXER_RE as well
LEXER_TMPL_EDIT.extend(LEXER_RE)

#---------------------------------
# A list for auto-completion tokens; not used at the moment
#---------------------------------
AC_TOKENS = {r'\\': 'backspace', r'\s': 'space', r'\S': 'anything but space',
             r'{m}': 'exactly m repetitions',
             r'{m,n}': 'at least m and at most n repetitions',
             r'(?P<name>)': 'named group', r'(?:)': 'unnamed group'}

AC_TOKENS = {r'\s': 'asdfasdf', r'{m}': 'ssdfdsf', r'*': 'dfd'}



def set_png(path, pngfile):
    fld = os.path.join(path, r'Images')
    #fld = os.path.normpath(fld)
    return wx.Bitmap(os.path.join(fld, pngfile), wx.BITMAP_TYPE_PNG)


def setpath(path=None):
    if path is None:
        return os.path.split(sys.argv[0])[0]
    else:
        return path
    
    
def add_menu_item(menu, id, text, icon=None):
    """Adds a menu icon to the menu. If the icon does not exist, it simply
    ignores this.
    """
    mitem = wx.MenuItem(menu, id=id, text=text)
    try: mitem.SetBitmap(set_png(icon))
    except: pass
    menu.AppendItem(mitem)
    
    
def dlg(parent, msg, title=''):
    """Raises a dlg with the msg message and returns 1 on OK, 0 on No and -1
    on Cancel.
    """
    dlg = wx.MessageDialog(parent, msg, caption=title,
                           style=wx.ICON_QUESTION|wx.YES_NO|wx.CANCEL)
    res = dlg.ShowModal()
    if res == wx.ID_YES: return 1
    elif res == wx.ID_NO: return 0
    else: return -1


def errdlg(parent, msg):
    """Raises a dlg with the msg message and returns 1 on OK, 0 on No and -1
    on Cancel.
    """
    dlg = wx.MessageDialog(parent, msg, caption='Error',
                           style=wx.ICON_ERROR|wx.OK)
    res = dlg.ShowModal()
     
