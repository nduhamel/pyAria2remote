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
from mypyapp.plugins import PluginMountPoint, PluginMount

from threading import Thread
from Queue import Queue

class Decrypter(PluginMountPoint,Thread,object):
    """
    Mount point for decrypter plugins

    Decrypters implementing this reference should provide the following attributes:
    ========  ========================================================
    load()    initialisation method called when thread is started
    
    
    Decrypter already implement:
    ========  ========================================================
    jobQueue
    
    """
    __metaclass__ = PluginMount
    
    daemon = True
    
    def __init__(self):
        super(Decrypter, self).__init__()
        self.jobQueue = Queue()
    
    def run(self):
        self.load()
        while True:
            req = self.jobQueue.get()
            
            result = self.decrypt(req.req)
            if result: req.set_response(result)
            req.task_done()
            self.jobQueue.task_done()


