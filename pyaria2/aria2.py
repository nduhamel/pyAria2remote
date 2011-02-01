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
import sys
import xmlrpclib

from .objects import AriaDownload
from .formater import Formaters, ConsolFormater
from .utils import option, make_option
from .utils import isUrl, tagetUrlIsText

from linkdecrypter import Decrypter

from .controler import Controler

class AriaControler(Controler):
    """
    _conf autoloaded by MetaConfig with CONFIG as section param
    """
    
    CONFIG = "AriaControler"
    
    prompt = "Aria> "
    verbose = True
    formaters = Formaters(ConsolFormater)
    
    def preloop(self):
        """Hook method executed once when the cmdloop() method is called."""
        self.stdout = sys.stdout
        serv_url = "http://%s:%s/rpc" % (self._conf['server'], self._conf['port'])
        self.connection = xmlrpclib.ServerProxy(serv_url)
        
        #~ if self._conf['clipboard']:
            #~ self.pfeedback("* Load clipboard watcher")
            #~ from clipboard import ClipboardWatcher
            #~ ClipboardWatcher.set_onClip(self.onclip)
        
        #Test linkdecrypter
        print Decrypter().modules
    
    def onclip(self, txt):
        pass
    
    def do_clip(self, args):
        self.poutput(args)
    
    def _xmlrpc(self, cmd, *args):
        '''real xmlrpc command'''
        server = self.connection
        fn = getattr(server, cmd)
        return fn(*args)
    
    def do_quit(self, *args):
        import threading
        for thread in threading.enumerate():
            try:
                thread.cancel()
            except AttributeError:
                pass
        return False
    do_q = do_quit
    
    def do_addurls(self, arg):
        """Download urls.  addurls url [ulr,]"""
        args = arg.split()
        
        #Validate url
        do = lambda i: isUrl(i) or self.pfeedback(str(i) + " is not a valid url")
        urls = [i for i in args if do(i) ]
        
        if not urls:
            self.pfeedback("No url provided")
            return None
        #Check content-type for require decrypter
        #In progress
        for url in urls:
            if tagetUrlIsText(url):
                question = "The url (%s) point to an HTML document\nIs it expected ?" % url
                choice = self.select( (('dl',"download"), ('decrypt',"decrypt"), ('c',"cancel") ),prompt=question)
                if choice == 'c' : return None
                if choice == 'decrypt': pass

        
        options = {'max-connection-per-server':'2'}
        started = [ self._xmlrpc("aria2.addUri", [url], options) for url in urls]
        
        return started

    @option(make_option("-d", "--download", action="store", type="string", dest="gid"))
    def do_url(self, arg, opts):
        
        if not opts.gid:
            self.pfeedback("You must set the download id with -d")
            return None
            
        if not arg:
            #list url
            return self._xmlrpc("aria2.getUris", opts.gid)
        else:
            #add url
            pass
        return True
    
    def do_tellactive(self, arg):
        ''' Return list of active downloads '''
        if arg: self.pfeedback("no arg require")
        rep = self._xmlrpc("aria2.tellActive")
        return map(AriaDownload, rep)
    
    def do_tellwaiting(self, arg):
        """ Return list of waiting downloads """
        if arg: self.pfeedback("no arg require")
        rep = self._xmlrpc("aria2.tellWaiting", 0, 10)
        return map(AriaDownload, rep)
        
    def do_tellstopped(self, arg):
        """ Return list of stoped downloads """
        if arg: self.pfeedback("no arg require")
        rep = self._xmlrpc("aria2.tellStopped", 0, 10)
        return map(AriaDownload, rep)
    
    def do_option(self, arg):
        rep = self._xmlrpc("aria2.getGlobalOption")
        return rep
        
    def do_purge(self, arg):
        """ purges completed/error/removed downloads to free memory """
        rep = self._xmlrpc("aria2.purgeDownloadResult")
        return rep
    
    
    def postcmd(self, out, line):
        if out == False: return True # Quit
        if out == None: return False # Error
        if out == [] : return False  # No result
        
        if type(out) == type([]):
            for item in out:
                self.poutput( self.formaters.format(item) )
            return False
        
        self.poutput( self.formaters.format(out) )
        
        return False                 # Continue
