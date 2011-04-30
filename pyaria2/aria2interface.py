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
import xmlrpclib

from .model import AriaDownload

class Aria2Interface(object):
    
    def __init__(self, server, port):
        
        serv_url = "http://%s:%s/rpc" % (server, port)
        self.connection = xmlrpclib.ServerProxy(serv_url)
    
    def request(self, cmd, *args):
        server = self.connection
        fn = getattr(server, cmd)
        rep = fn(*args)
        return rep
    
    def purge(self):
        """ purges completed/error/removed downloads to free memory """
        rep = self.request("aria2.purgeDownloadResult")
        if rep == 'OK': return True
        else: return False
    
    def tellactive(self):
        ''' Return list of active downloads '''
        rep = self.request("aria2.tellActive")
        return map(AriaDownload, rep)
    
    def tellstopped(self, start, num):
        rep = self.request("aria2.tellStopped", start, num)
        return map(AriaDownload, rep)  
    
    def tellwaiting(self, start, num):
        rep = self.request("aria2.tellWaiting", start, num)
        return map(AriaDownload, rep)

    def adduri(self, urls, options=None):
        if not isinstance(urls, list):
            urls = [urls]
        if options:
            rep = self.request("aria2.addUri", urls, options)
        else:
            rep = self.request("aria2.addUri", urls)
        
        return rep
    
    def pauseall(self):
        rep = self.request("aria2.pauseAll")
        if rep == 'OK': return True
        else: return False

    def unpauseall(self):
        rep = self.request("aria2.unpauseAll")
        if rep == 'OK': return True
        else: return False
    
    def unpause(self, gid):
        try:
            gid = self.request("aria2.unpause", gid)
            return gid
        except xmlrpclib.Fault, err:
            if "cannot be paused now" in err.faultString:
                return "Download can't be unpaused"
        
    def pause(self, gid):
        try:
            gid = self.request("aria2.pause", gid)
            return gid
        except xmlrpclib.Fault, err:
            if "cannot be paused now" in err.faultString:
                return "Download can't be paused"
    
    def remove(self, gid):
        gid = self.request("aria2.remove", gid)
        return gid
    
    def getglobaloption(self):
        rep = self.request("aria2.getGlobalOption")
        return rep
