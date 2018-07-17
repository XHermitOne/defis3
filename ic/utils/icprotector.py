#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Реализация защищенных методов и атрибутов.
"""

def readonly(value):
    return property(lambda self: value)

def protect(f):
    """ 
    Decorator used to assign the attribute __protect__ to methods.
    """
    f.__protected__ = True
    return f

class Protected(object):
    """  
    Base class of all classes that want to hide protected attributes from
    public access.
    """

    def __new__(cls, *args, **kwd):
        obj = object.__new__(cls)        
        cls.__init__(obj, *args, **kwd)
                                
        def __getattr__(self, name):            
            attr = getattr(obj, name)
            if hasattr(attr, "__protected__"):
                raise AttributeError, "Attribute %s is not public." % name
            elif hasattr(cls, "__protected__"):
                if name in cls.__protected__:
                    raise AttributeError, "Attribute %s is not public." % name
            return attr
        
        def __setattr__(self, name, value):
            attr = getattr(self, name)
            print('__setattr__:', attr)                 
            cls.__setattr__(self, name, value)    

        # Magic methods defined by cls must be copied to Proxy.
        # Delegation using __getattr__ is not possible.

        def is_own_magic(cls, name, without=[]):
            return name not in without and name.startswith("__") and name.endswith("__")

        Proxy = type("Protected(%s)" % cls.__name__,(),{})   

        for name in dir(cls):
            if is_own_magic(cls,name, without=dir(Proxy)):
                try:
                    setattr(Proxy, name, getattr(obj,name))
                except TypeError:
                    pass
        
        Proxy.__getattr__ = __getattr__
        Proxy.__setattr__ = __setattr__
        return Proxy()

