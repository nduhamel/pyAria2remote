# -*- coding: utf-8 -*-
# Copyright(C) 2010  Nicolas Duhamel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
from Queue import Queue, Empty
import time

class PluginMount(type):
    """ The metaclass that enable auto-register plugin """
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)
            

class PluginMountPoint(object):
    """ Just for issubclass test """
    pass

class PluginReq(object):
    """ Simple req object for store result """
    __slots__ = ('req', 'results', 'inprogress') 
    
    def __init__(self, req):
        
        self.req = req # The request
        
        self.results = [] # The result
        self.inprogress = 0 #how many process the obj
    
    def start(self):
        self.inprogress += 1
        return self
    
    def set_response(self, rep):
        self.results.append(rep)
    
    def task_done(self):
        self.inprogress -= 1
    
    def get(self):
        """ Return first result, raise Empty if no result pending"""
        if len(self.results) > 0:
            return self.results.pop(0)
        elif self.inprogress == 0 and  len(self.results) == 0:
            raise Empty
        #result pending wait for it:
        time.sleep(0.1)
        return self.get()
    
    def join(self):
        while self.inprogress > 0:
            time.sleep(0.1)
        return self.results
    
    def __eq__(self, other):
        try:
            return self.req == other.req
        except:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)


class PluginLoader(object):
    def __init__(self, mountpoint):
        self.mountpoint = mountpoint
        self.plugins = [p() for p in self.mountpoint.plugins]

        for p in self.plugins:
            p.start()
    
    def request(self, req):
                
        req = PluginReq(req)
        
        for p in self.plugins:
            p.jobQueue.put(req.start())
        
        return req


REGISTER_MOUNT_POINT = {}
LOADED_MOUNT_POINT = {}

def Plugins(mountpoint):
    """ Load a mount point """
    if mountpoint in LOADED_MOUNT_POINT.keys():
        return LOADED_MOUNT_POINT[mountpoint]
    else:
        if mountpoint in REGISTER_MOUNT_POINT.keys():
            pl = PluginLoader(REGISTER_MOUNT_POINT[mountpoint])
            LOADED_MOUNT_POINT[mountpoint] = pl
            return pl
        else:
            assert False

def PluginsRegister(package,name):
    """ Import a mount point """
    modname = package + '.' + name
    mod = __import__(modname, fromlist="dummy")
    for mountpoint in mod.__all__:
        REGISTER_MOUNT_POINT[mountpoint] = getattr(mod, mountpoint)    
