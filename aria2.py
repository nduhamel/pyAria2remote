# -*- coding: utf-8 -*-
#!/usr/bin/python
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
import logging
import sys
import pprint

from utils import sizeof_fmt, simple_eta, achievepercent, ReadOnlyDict


class AriaDownload(ReadOnlyDict):
    def __init__(self, ariaControler, gid):
        ReadOnlyDict.__init__(self)
        
        assert isinstance(ariaControler, AriaControler)
        assert isinstance(gid, int) or isinstance(gid, str)
        self.aria2 = ariaControler
        self.gid = str(gid)
    
    def __enter__(self):  self._updateStatus()
    def __exit__(self, exc_type, exc_value, traceback): pass
    
    def _updateStatus(self):
        rep = self.aria2.do_tellStatus(self)
        self.update(rep)
    

class AriaControler:
        
    def __init__(self, server=None, port=None):
        self.connection = xmlrpclib.ServerProxy("http://localhost:6800/rpc")
        self.logger = logging.getLogger()

    def _do_cmd(self, cmd, *args):
        '''real xmlrpc command.'''
        server = self.connection
        try:
            fn = getattr(server, cmd)
            result = fn(*args)
            ppresult = pprint.pformat(result, 1)
            self.logger.debug("Call: "+ cmd )
            self.logger.debug("Response:\n "+ ppresult)
            return result
        except (xmlrpclib.Fault, xmlrpclib.ProtocolError):
            self.logger.error( '%s: %s' % (cmd, sys.exc_info()[1]) )

    ##############
    ### Repl cmd
    def do_addUri(self, uris):
        """ aria2.addUri return gid """
        rep = self._do_cmd("aria2.addUri", [uris])      
        return AriaDownload(self,int(rep))
    
    def do_pauseAll(self):
        """Return OK on success """
        #~ rep = self.connection.aria2.pauseAll()
        rep = self._do_cmd("aria2.pauseAll")
        return rep
            
    def do_unpauseAll(self):
        """Return OK on success """
        rep = self._do_cmd("aria2.unpauseAll")
        return rep
    
    def do_purgeDownloadResult(self):
        """Return OK on success """
        rep = self._do_cmd("aria2.purgeDownloadResult")
        return rep

    def do_tellActive(self):
        """ aria2.tellActive return a list of download """
        rep = self._do_cmd("aria2.tellActive")
        dls = []
        for download in rep:
            dls.append(AriaDownload(self,int(download["gid"])))
        return dls
        
    def do_tellWaiting(self,offset=0, num=10):
        """ aria2.tellWaiting return a list of download """
        rep = self._do_cmd("aria2.tellWaiting", offset, num)
        dls = []
        for download in rep:
            dls.append(AriaDownload(self,int(download["gid"])))
        return dls
        
    def do_tellStopped(self, offset=0, num=10):
        """ aria2.tellStopped return a list of download """
        rep = self._do_cmd("aria2.tellStopped", offset, num)        
        dls = []
        for download in rep:
            dls.append(AriaDownload(self,int(download["gid"])))
        return dls

    def do_remove(self,gid):
        """ Return the removed download's gid """
        rep = self._do_cmd("aria2.remove", gid)
        return rep
        
    def do_pause(self, gid):
        """ Return the removed download's gid """
        rep = self._do_cmd("aria2.pause", gid)
        return rep
        
    def do_unpause(self, gid):
        """ Return the removed download's gid """
        rep = self._do_cmd("aria2.unpause", gid)
        return rep
            
    def do_tellStatus(self, gid):
        assert isinstance(gid, str) or isinstance(gid, AriaDownload)
        if isinstance(gid, AriaDownload):
            gid = gid.gid
            rep = self._do_cmd("aria2.tellStatus", gid)
        else:
            rep = self._do_cmd("aria2.tellStatus", gid)
            rep = AriaDownload(self,rep["gid"])
        return rep
