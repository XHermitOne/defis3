#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
from ic.utils import filefunc
from ic.bitmap import icimglib


def img2gif_tmp():
    app = wx.PySimpleApp()
    img_lib = icimglib.icImgLibResource()
    img_lib.createNewImgLib()
    png_files = filefunc.getFilenamesByExt('./tmp/', '.png')
    for png_file in png_files:
        img_lib.addImg(png_file)
    img_lib.saveImgLib('new_img_lib.py')


if __name__ == '__main__':
    img2gif_tmp()
