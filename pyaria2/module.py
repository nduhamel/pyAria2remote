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
#~ from .utils import LimitedSizeList

class ModuleMount(type):
    """ The metaclass that enable auto-register module """
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'modules'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.modules = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.modules.append(cls)
            

class MountPoint(object):
    """ Just for issubclass test """
    pass

class ModuleReq(object):
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

class ModuleLoader(object):
    def __init__(self, mount):
        self.mount = mount
        #~ self.cache = LimitedSizeList(size=5)
        
        #init modules
        self.modules = [p() for p in self.mount.modules]
        #launch modules
        for p in self.modules:
            p.start()
    
    def request(self, req):
                
        req = ModuleReq(req)
        
        for mod in self.modules:
            mod.jobQueue.put(req.start())
        
        return req
        #~ request = ModuleReq(req)
        #~ if request in self.cache:
            #~ print "Already cached"
            #~ return "cached"
        #~ else:
            #~ self.cache.append(request)
            #~ 
        #~ for mod in self.modules:
            #~ mod.jobQueue.put(req)
            #~ mod.jobQueue.join()
            #~ 
        #~ res = []
        #~ for mod in self.modules:
            #~ res.append(mod.resultsQueue.get())
        #~ return res
    
