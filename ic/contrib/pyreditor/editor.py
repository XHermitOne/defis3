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


import re
import sys
import os
import wx
import wx.stc
from wx.lib.anchors import LayoutAnchors
import string
from .commons import STYLE_DEFAULT, LEXERS_ALL, CUSTOM_STYLE_IDS, YELLOW1, GREEN1
from .commons import SET_FILE
from .menus import EditInsertMenu

        

class Editor(wx.stc.StyledTextCtrl):
    """Basic editor that implements brace matching, auto-completion and
    simple syntax coloring.
    """
    def __init__(self, enh_menu=False, **kwargs):
        """See set_lexer for lexer parameter; if 'container' (custom lexer)
        lexer_style needs to be specified as well.
        """
        wx.stc.StyledTextCtrl.__init__(self, **kwargs)
        
        # Lexer, lexer style and tokens (a list of all the tokens for the
        # custom lexer - in the order of priority) are set in set_lexer.
        self._style = None
        self._lexer = None
        self._lexer_style = None
        self._tokens = []           # token names
        self._name2styleid = None   # dict of tokens (names) and corresponding style ids    
        self._all_patts = None
        self._braces = None
        self._braces_patt = None
        self._ac_tokens = None      # auto-completion tokens as a dictionary of tokens with a description

        # Some other, internal vars
        self._popup = None  # enhanced popup menu - see enh_popup()
        self._do_autocomplete = True
        self._maxgroups = 20
        self._autoindent = False
        self._auto_complete_keys = range(33, 256) # The keys when autocompletion is invoked for
        
        # Event bindings. Important, self.OnUpdateUI should be "fired" when
        # the stc editor is being updated and not when the frame is being updated.
        # If not, the processor will work with 100% most of the time!
        self.Bind(wx.stc.EVT_STC_UPDATEUI, self.on_updateui)
        self.Bind(wx.stc.EVT_STC_STYLENEEDED, self.on_styleneeded)
        self.Bind(wx.EVT_KEY_UP, self.on_keyupevent)
        self.Bind(wx.EVT_KEY_DOWN, self.on_keyevent)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        self.Bind(wx.stc.EVT_STC_CHARADDED, self.on_charadded)
        
        # Some other initializations
        self.AutoCompSetSeparator(ord('@'))
        self.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER) # margin 0 for line numbers
        self.SetMarginWidth(1, 0)   # zero-width margin 1
        self.SetMarginWidth(2, 0)   # zero-width margin 2
        
    def set_maxgroups(self, maxgroups=20):
        self._maxgroups = maxgroups
        
    def enh_popup(self, insertitems=None, tempitems=None, on=True, path=None):
        """Turns the enhanced popup menu on/off."""
        if on == True:
            self._popup = EditInsertMenu(None, self, path, hasedit=True,
                                         insertitems=insertitems, tempitems=tempitems)
        else:
            self._popup = None
    
    def set_braces(self, braces=r'()[]{}<>'):
        # Braces patterns
        self._braces = braces
        patt = '[%s]' % string.join(['\\%s' % br for br in self._braces], '')
        self._braces_patt = re.compile(patt, re.IGNORECASE)
        # And a pattern to check \( and similar conditions that are not
        # to be matched.
        self._braces_patt2 = re.compile(r'%s\\*' % patt)
        
    def autoindent(self, on=False):
        self._autoindent = (on == True)
        
    def set_tokens(self, tokens):
        """Set the auto-completion tokens - a dictionary with tokens and their
        descriptions. Set tokens to None not to use them.
        """
        if tokens is None:
            self._ac_tokens = None
            self._autocomplete_on = False
            return
        if not(isinstance(tokens, dict)):
            raise Exception('tokens must be a dictionary')
        self._ac_tokens = tokens
        
    def insert_text(self, text, embrace_sel=True, sel=None):
        """Inserts a text code from _M_ITEMS according to name, position, etc.
        If embrace_sel is True, the text must hold %s where the selected
        (existing) text will be injected. sel can be a tuple of (selstart, sellen)
        to select the text after insertion - with respect to the cursor 
        start position  before the insertion.
        """
        (start, end) = self.GetSelection()
        old_text = self.GetSelectedText()
        if embrace_sel:
            self.ReplaceSelection(text % old_text)
        else:
            self.ReplaceSelection(text)
        if sel != None:
            self.SetSelection(start+sel[0], start+sel[0]+sel[1])
        
    def autocomplete(self, on=False):
        """Turn auto-completion on/off. To turn it on, auto-completion tokens
        must be set already - see set_tokens.
        """
        if not(self._ac_tokens is None):
            self._autocomplete_on = (on==True)
        else:
            self._autocomplete_on = False
        
    def linenums(self, show=False):
        """Show or hide the lines margin."""
        if show:
            self.SetMarginWidth(0, 15)
        else:
            self.SetMarginWidth(0, 0)

    def set_lexer(self, style=STYLE_DEFAULT, lexer='null', lexer_style=None):
        """Sets the lexer by giving a lexer string (see _LEXERS). 'null' is the
        default lexer (no lexer); for plain text. On the other hand, 'container'
        needs to be used for a custom lexer.
        """
        self._style = style
        self._lexer = lexer
        self._lexer_style = lexer_style
        
        # Default/common styles
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,     style['default'])
        self.StyleClearAll()
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,  style['linenumber'])
        self.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, style['controlchar'])
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,  style['bracelight'])
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,    style['bracebad'])
        
        # Select the lexer
        if not(lexer.lower() in LEXERS_ALL):
            raise Exception('%s is not a supported lexer' % lexer)
        if lexer.lower() == 'automatic':
            self.SetLexer(wx.stc.STC_LEX_AUTOMATIC)
        elif lexer.lower() == 'null':
            self.SetLexer(wx.stc.STC_LEX_NULL)
        elif lexer.lower() == 'container':
            # Custom lexing needs to be implemented - see the onstyleneeded
            # method.
            if not(isinstance(lexer_style, list)):
                raise Exception('Custom lexer must be given as a list of lists '\
                                'defining the lexer style')
            
            self.SetLexer(wx.stc.STC_LEX_CONTAINER)
            
            # Set the pattern for lexing.
            # The order below IS important!
            patts = [('(?P<%s>%s)') % (ls[0], ls[1]) for ls in lexer_style]
            self._all_patts = re.compile(string.join(patts, '|'))
            self._tokens = [n[0] for n in self._lexer_style]
            
            ls = self._lexer_style
            self._name2styleid = dict( [(ls[k][0], CUSTOM_STYLE_IDS[k]) for k in range(len(ls))] )
            
            # Some modified Python styles for our own "highlighter"
            ns = len(self._lexer_style)
            if ns > len(CUSTOM_STYLE_IDS):
                raise Exception('Max %d styles can be defined' % len(CUSTOM_STYLE_IDS))
            for k in range(ns):
                if self._lexer_style[k][2] != None:
                    self.StyleSetSpec(CUSTOM_STYLE_IDS[k], self._lexer_style[k][2])
        else:
            # One of the pre-defined lexers
            self.SetLexerLanguage(lexer.lower())
            
        # Set the indicators used to show the matching results in the "string"
        # editor
        try: self.IndicatorSetStyle(0, wx.stc.STC_INDIC_ROUNDBOX)
        except: pass
        self.IndicatorSetForeground(0, YELLOW1)
        try: self.IndicatorSetStyle(1, wx.stc.STC_INDIC_ROUNDBOX)
        except: pass
        self.IndicatorSetForeground(1, GREEN1)
        
    def on_updateui(self, event):
        """On editor's UI update. Brace matching is handled here."""
        # If there is a brace at this position and if it is, is there a
        # matching brace?
        if self._braces_patt is None:
            # No brace matching required
            return
        
        pos1 = self.GetCurrentPos()
        ch = chr(self.GetCharAt(pos1))
        res = re.match(self._braces_patt, ch)
        if not res:
            # Check one char back if there is one at the current line
            line_no = self.LineFromPosition(pos1)
            start = self.PositionFromLine(line_no)
            if pos1 > start:
                pos1 -= 1
                ch = chr(self.GetCharAt(pos1))
                res = re.match(self._braces_patt, ch)
        if res:
            # If there is a brace at pos1 or at pos1-1
            
            # Check if there are either none or even number of \ in front
            # of the brace - otherwise, no matching is to be performed
            s = self.GetText()[pos1::-1]
            res2 = re.match(self._braces_patt2, s)
            if divmod(len(res2.group()), 2)[1] == 0:
                # not OK
                self.BraceHighlight(wx.stc.STC_INVALID_POSITION, wx.stc.STC_INVALID_POSITION)
                event.Skip()
                return
            
            pos2 = self.BraceMatch(pos1)
            if pos2 != wx.stc.STC_INVALID_POSITION:
                # Matching brace?
                s = self.GetText()[pos2::-1]
                res2 = re.match(self._braces_patt2, s)
                if divmod(len(res2.group()), 2)[1] == 0:
                    # not OK
                    self.BraceBadLight(pos1)
                else:
                    # OK
                    if pos1 > pos2:
                        self.BraceHighlight(pos2, pos1)
                    else:
                        self.BraceHighlight(pos1, pos2)
            else:
                # No matching brace
                self.BraceBadLight(pos1)
        else:
            self.BraceBadLight(wx.stc.STC_INVALID_POSITION)
            self.BraceHighlight(wx.stc.STC_INVALID_POSITION, wx.stc.STC_INVALID_POSITION)

        # To process the key events by default handler as well...   
        event.Skip() 
        
    def on_styleneeded(self, event):
        """On style change - for the custom lexer."""
        # Get the first character that "needs styling", start
        # and the last one that "needs styling", end
        start = self.GetEndStyled()
        end = event.GetPosition()
        
        # Get the line # corresponding to start and then the first
        # position in that line
        line_no = self.LineFromPosition(start)
        start = self.PositionFromLine(line_no)
        
        # Get the text from the editor
        s = self.GetTextRange(start, end)
        
        # Apply the default styling to the selection
        self.StartStyling(start, 31)     
        self.SetStyling(end-start+1, wx.stc.STC_STYLE_DEFAULT)
        
        # Iterate over all the matches according to self.all_patts and
        # apply styling according to which group is being matched
        
        iter = re.finditer(self._all_patts, s)
        for it in iter:
            (s1, s2) = it.span()
            self.StartStyling(start+s1, 31)
            for n in self._tokens:
                if it.group(n):
                    self.SetStyling(s2-s1, self._name2styleid[n])
                    break
                
    def color_txtString(self, span):
        # Colors the matched text in the txtString edit component according
        # to span ((start, end)) positions. If span=None, no coloring will
        # be performed. This is to be called from the OnChange method.
        # Moreover, if span is a list of tuples, several regions will be
        # colored using alternating yellow/green colors.
        # Only self._maxgroups results will be shown.
        
        # Here we use the so-called INDICATOR styles to ADD some additional
        # styles to the (already styled) text. So, this is the way to preserve
        # any existing styling and add some additional "effects" - we add colored
        # boxes.
        
        self.StartStyling(0, wx.stc.STC_INDICS_MASK)
        self.SetStyling(self.GetTextLength(), wx.stc.STC_INDIC_HIDDEN)
        
        if span is not None:
            # "Match" color for the span region
            if isinstance(span, list):
                # Span is a list of tuples
                n = min(len(span), self._maxgroups)
                for k in range(0, n, 2):
                    # yellow background
                    start = span[k][0]
                    end = span[k][1]
                    self.StartStyling(start, wx.stc.STC_INDICS_MASK)
                    self.SetStyling(end-start, wx.stc.STC_INDIC0_MASK)
                for k in range(1, n, 2):
                    # green background
                    start = span[k][0]
                    end = span[k][1]
                    self.StartStyling(start, wx.stc.STC_INDICS_MASK)
                    self.SetStyling(end-start, wx.stc.STC_INDIC1_MASK)
            else:
                # span should be a tuple
                # yellow background
                start = span[0]
                end = span[1]
                self.StartStyling(start, wx.stc.STC_INDICS_MASK)
                self.SetStyling(end-start, wx.stc.STC_INDIC0_MASK)
                
    def on_charadded(self, event):
        """When a character is added. Auto indent,..."""
        key = event.GetKey()
        # Auto-indent?
        if key == wx.stc.STC_KEY_RETURN and self._autoindent:
            curr_ln_num = self.GetCurrentLine()     # the new line
            if curr_ln_num > 0:
                prevline = self.GetLine(curr_ln_num - 1)
                res = re.match(r'[ \t\f\v]+', prevline)
                if res:
                    self.AddText(res.group())
        event.Skip()

    def on_keyupevent(self, event):
        # Check if auto-completion is to be fired
        key = event.GetKeyCode()
        if self._do_autocomplete:
            # Is CTRL+SPCACE pressed?
            if key == 32 and event.ControlDown() and not self.AutoCompActive():
                # If shift is also pressed, show the call tip (if available)
                if event.ShiftDown():
                    self.CallTipCancel()
                    self.__show_call_tip()
                else:
                    # Forced autocompletion; also, use the full list of
                    # possibilities when no match is found
                    self.__show_auto_complete(allow_all=True)
            
            elif key in self._auto_complete_keys:
                # If a char is added, check for auto-completion
                exact = self.__show_auto_complete(allow_all=False)
                if exact:
                    # Hide the list and show the tip when an exact match is found
                    self.AutoCompCancel()
                    self.__show_call_tip()
            
        # To process the key events by default handler as well...   
        event.Skip()
        
    def on_keyevent(self, event):
        # When the auto complete is on, check what to do when something is
        # selected from the list (ENTER or TAB pressed).
        key = event.GetKeyCode()
        if self.AutoCompActive() and (key == wx.WXK_RETURN or key == wx.WXK_TAB):
                # If autocomplete is active and either RETURN or TAB are pressed
                # do the autocompletion and show the tip. This event is
                # handled here as it needs to be handled before the ENTER
                # or TAB key is up!
                self.AutoCompComplete()
                self.__show_call_tip(r'\s')
                return      # with this, this event WILL NOT be skipped!
        
        # To process the key events by default handler as well...   
        event.Skip()
        
    def on_rightdown(self, event):
        # On right mouse button shows the popup menu
        if not (self._popup is None):
            self.PopupMenu(self._popup)
        else:
            event.Skip()
        
    def __show_auto_complete(self, allow_all=False):
        # Shows the auto-complete list. This is a simple implementation
        # where all the tokens are displayed - to be selected
        # and inserted if one wishes. If inserted, any selected text will be
        # replaced by the insertion.
        pass
        if not(self._ac_tokens is None):
            tokens = self._ac_tokens.keys()
            tokens = string.join(tokens, '@')
            self.AutoCompShow(0, tokens)
        
    def __extract_token(self):
        # Extract a "token" from the current cursor position. Actually, it
        # extracts a "token" as found in _AC_TOKENS that is to be used for
        # auto completion and/or call tips.
#        (line, c_pos) = self.GetCurLine()
#        # Split into delimiter-token groups
#        res = re.finditer(self._sset.getpattdelims(), line[:c_pos])
#        res = [(r.span('token'), r.group('token')) for r in res]
        pass
    
    def __show_call_tip(self, token):
        # Shows a call tip according to the given token.
        try:
            pos = self.GetCurrentPos()
            desc = self._ac_tokens[token]
            self.CallTipShow(pos, desc)
        except:
            pass