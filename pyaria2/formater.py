# -*- coding: utf-8 -*-
class FormaterMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'formaters'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.formaters = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.formaters.append(cls)


class MountPoint(object):
    pass          

class ConsolFormater(MountPoint):
    """
    Mount point for plugins which refer to actions that can be performed.
    Rename it !

    Plugins implementing this reference should provide the following attributes:
    The doc is essential adapt it !
    
    ========  ========================================================
    a class member : obj   that point to the obj type that formate
    a class method : format(cls, obj) that return the formated obj
    ========  ========================================================
    """
    __metaclass__ = FormaterMount


class Formaters(object):
    def __init__(self, mount):
        assert issubclass(mount, MountPoint)
        self.mount = mount
    
    def format(self, obj):
        for f in self.mount.formaters:
            if isinstance(obj, f.obj):
                return f.format(obj)
        return str(obj)

