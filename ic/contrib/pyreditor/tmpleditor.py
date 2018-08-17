#Boa:Frame:Frame1

# Template editor - a simple frame with an editor and save option to
# edit template file ("plain" cfg file).

import wx
from wx.lib.anchors import LayoutAnchors

from .editor import Editor
from .commons import STYLE_DEFAULT, set_png, dlg, errdlg, LEXER_TMPL_EDIT


[wxID_FRAME1, wxID_FRAME1TOOLBAR1, 
] = [wx.NewId() for _init_ctrls in range(2)]

_TITLE = r'Template Editor'


class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        if prnt != None:
            style = wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT
        else:
            style = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(509, 289), size=wx.Size(730, 644),
              style=style,
              title='Template editor')
        self.SetClientSize(wx.Size(712, 599))

        self.toolBar1 = wx.ToolBar(id=wxID_FRAME1TOOLBAR1, name='toolBar1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(712, 28),
              style=wx.TB_FLAT | wx.TB_HORIZONTAL)
        self.toolBar1.SetConstraints(LayoutAnchors(self.toolBar1, True, True, True, False))
        self.toolBar1.SetToolBitmapSize(wx.Size(22, 22))
        
        self.SetToolBar(self.toolBar1)
        
        self.editor = Editor(id=wx.NewId(), parent=self, enh_menu=False,
                           style=wx.TE_MULTILINE | wx.BORDER_THEME)
              
        self.editor.SetAutoLayout(True)
        self.editor.SetConstraints(LayoutAnchors(self.editor, True, True,
              True, True))

    def __init__(self, parent, tmpfile, path=None, onsave=None):
        # onsave is a parent's callback to be called on save and on close. Its
        # structure is:
        #    some_fun(event)
        self._init_ctrls(parent)
        
        # Some variables
        self._is_saved = True
        self._path = path
        self._tmpfile = tmpfile
        self._onsave = onsave
        
        # Set the editor
        self.editor.set_lexer(style=STYLE_DEFAULT, lexer='container',
                                lexer_style=LEXER_TMPL_EDIT)
        self.editor.set_braces()
        
        # Set the toolbar - add tools
        self.toolBar1.SetToolBitmapSize(wx.Size(22, 22))
        self._id = {'save': wx.NewId()}
        self.toolBar1.AddSeparator()
        self.toolBar1.DoAddTool(bitmap=set_png(path, r'filesave2.png'),
                                bmpDisabled=wx.NullBitmap, id=self._id['save'],
                                kind=wx.ITEM_NORMAL, label='Save', longHelp='Save',
                                shortHelp=u'Save')
        self.toolBar1.AddSeparator()
        self.toolBar1.Realize()
        
        # Callbacks
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.editor.Bind(wx.stc.EVT_STC_CHANGE, self.OnChange)
        self.toolBar1.Bind(wx.EVT_TOOL, self.OnSave, id=self._id['save'])
        
        self._refresh_editor()
        self._load()
        
    def _refresh_editor(self):
        if not self._is_saved:
            self.SetTitle('%s *' % _TITLE)
            self.toolBar1.EnableTool(self._id['save'], True)
        else:
            self.SetTitle(_TITLE)
            self.toolBar1.EnableTool(self._id['save'], False)
        
    def OnClose(self, event):
        res = 0
        if not self._is_saved:
            res = dlg(self, msg='Save templates before exiting?', title='Confirm')
            if res == 1:
                # OK => save
                self._save()
                res = 0
        if res != -1:
            if self._onsave != None:
                self._onsave(None)
            self.Destroy()
        
    def OnChange(self, event):
        self._is_saved = False
        self._refresh_editor()
        event.Skip()
        
    def OnSave(self, event):
        self._save()
    
    def _save(self):
        # Saves the templates
        try:
            self.editor.SaveFile(self._tmpfile)
            self._is_saved = True
            self._refresh_editor()
            if self._onsave != None:
                self._onsave(None)
        except:
            errdlg(self, 'Cannot save to %s' % self._tmpfile)
    
    def _load(self):
        # Loads the templates
        try:
            self.editor.LoadFile(self._tmpfile)
            self._is_saved = True
            self._refresh_editor()
        except:
            pass
        

def main():
    app = wx.PySimpleApp()
    frame = Frame1(None, r'templates.cfg', path=r'.')
    frame.Show()
    app.MainLoop()
    
    
if __name__ == '__main__':
    main()
