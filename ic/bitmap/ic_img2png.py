#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from ic.imglib import common

def img2png_tmp():
    app = wx.PySimpleApp()
    common.img_init()
    for img_name in dir(common):
        if not isinstance(common.__dict__[img_name], dict) and \
           not isinstance(common.__dict__[img_name], str) and \
           not isinstance(common.__dict__[img_name], tuple) and \
           common.__dict__[img_name] is not None and \
           not isinstance(common.__dict__[img_name], list):
            if type(common.__dict__[img_name]).__name__ == 'Bitmap':
                img_file_name = './tmp/' + img_name + '.png'
                img = common.__dict__[img_name].ConvertToImage()
                img.SaveFile(img_file_name, wx.BITMAP_TYPE_PNG)
    
if __name__ == '__main__':
    img2png_tmp()
