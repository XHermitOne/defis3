#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import wx
import wx.lib.delayedresult as delayedresult
import thread

# Version
__version__ = (0, 0, 0, 2)


class DelayedFunction(object):
    """
    This demos simplistic use of delayedresult module.
    """
    
    def __init__(self, process_func, result_func, *args, **kwargs):
        self.process_func = process_func
        self.result_func = result_func
        self.args = args
        self.sessionID = 0
        self.abortEvent = delayedresult.AbortEvent()

    def abort(self, event):
        """
        Only needed because in demo, closing the window does not kill the
        app, so worker thread continues and sends result to dead frame; normally
        your app would exit so this would not happen.
        """
        self.abortEvent.set()
                    
    def start(self): 
        """
        Compute result in separate thread, doesn't affect GUI response.
        """
        self.abortEvent.clear()
        delayedresult.startWorker(self.result, self.process)
                        
    def process(self):
        """
        Pretend to be a complex worker function or something that takes
        long time to run due to network access etc. GUI will freeze if this 
        method is not called in separate thread.
        """
        self.process_func(*self.args)
        
    def result(self, delayedResult):
        try:
            # result = delayedResult.get()
            self.result_func(*self.args)
        except Exception as exc:
            print(u'Result for sessionID %s raised exception: %s' % (self.sessionID, exc))
