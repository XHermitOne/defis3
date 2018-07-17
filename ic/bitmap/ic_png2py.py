#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from ic.utils import ic_file
from ic.bitmap import icimglib


def img2gif_tmp():
    app = wx.PySimpleApp()
    img_lib = icimglib.icImgLibResource()
    img_lib.createNewImgLib()
    png_files = ic_file.GetFilesByExt('./tmp/', '.png')
    for png_file in png_files:
        img_lib.addImg(png_file)
    img_lib.saveImgLib('new_img_lib.py')
    
if __name__ == '__main__':
    img2gif_tmp()
