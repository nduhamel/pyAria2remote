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
from mypyapp.console import ConsoleApp, command, option, make_option
from mypyapp.completer import FilePathCompleter
from mypyapp.plugins import Plugins, PluginsRegister
from mypyapp.templates import render

from .aria2interface import Aria2Interface
from .utils import isUrl, tagetUrlIsText
from .model import AriaDownload


class Aria2console(ConsoleApp):
    
    CONFIG = "Aria2console"   
    prompt = "Aria> "
        
    PluginsRegister(__package__, "linkdecrypter")
    
    def load(self): 
        self.aria2interface = Aria2Interface(self._conf['server'], self._conf['port'])
        
    @command('add')
    @option([make_option("-f", "--file", action="store", type="string", dest="filename", completer=FilePathCompleter),
            make_option("-d", action="store_true", dest="decrypt"),
            ])
    def addurls(self, args, opts):
        """Download urls.  addurls url [ulr,]"""
        
        #Import url from file 
        if opts.filename:
            with open(opts.filename, 'r') as f:
                args.extend( f.readlines() )
        
        
        #Validate url
        error_msg = "/!\ -->  '{0}' is not a valid url "
        do = lambda i: isUrl(i) or self.pfeedback(error_msg.format(i))
        urls = [i for i in args if do(i) ]
        
        #if no valid urls quit
        if not urls:
            self.pfeedback("No url provided")
            return False
        
        #Check content-type for require decrypter
        #Need user intervention
        final_urls = []
        
        for url in urls:
            if tagetUrlIsText(url) and not opts.decrypt:
                
                question = "The url (%s) point to an HTML document\nIs it expected ?" % url
                choice = self.select( ( ('c',"cancel"), ('dl',"download"), ('decrypt',"decrypt") ),prompt=question)
                if choice == 'c' : continue
                if choice == 'decrypt': 
                    rep = self._decrypt(url)
                    if rep: final_urls.append(rep)
                    else: self.pfeedback('%s can\'t be decrypt' % url)
                if choice == 'dl' : final_urls.append(url)
                
            elif tagetUrlIsText(url) and opts.decrypt:
                rep = self._decrypt(url)
                if rep: final_urls.append(rep)
                else: self.pfeedback('%s can\'t be decrypt' % url)
            else:
                final_urls.append(url)
                
        options = {'max-connection-per-server':'2'}
        started = [ self.aria2interface.adduri(url, options) for url in final_urls]
        for obj in started:
            self.poutput(obj)
        
        return False        
    
    
    @command()
    def decrypt(self, arg):
        rep = self._decrypt(arg)
        if rep:
            return self.do_add(rep)
        else:
            self.poutput("Error")
            return True
    
    def _decrypt(self, url):
        req = Plugins("Decrypter").request(url)
        try:
            return req.get()
            
        except:
            self.pfeedback( "No result")

    
    ####################################################################
    ## Final
    @command()
    def pauseall(self, args):
        if self.aria2interface.pauseall():
            self.poutput( 'All downloads paused' )
        else:
            self.poutput( 'Unknow error')
        return False
    
    @command()
    def unpauseall(self, args):
        if self.aria2interface.unpauseall():
            self.poutput( 'All downloads unpaused' )
        else:
            self.poutput( 'Unknow error')
        return False
        
    @command('active')
    def tellactive(self, arg):
        """ Return list of active downloads """
        if arg: self.pfeedback("no arg require")
        objs = self.aria2interface.tellactive()
        
        if not objs: 
            self.pfeedback( 'No active downloads' )
            return False
        
        self.poutput( render('/downloadList.tmplc', objs=objs) )
            
        return False
    
    @command('stopped')
    @option( [make_option("-s", "--start", action="store", type="int", dest="start", default=0),
              make_option("-n", "--num" , action='store', type='int', dest='num', default=10),
              ] )
    def tellstopped(self, args, opts):
        """ Return list of stoped downloads """
        if args: self.pfeedback("no arg require")

        objs = self.aria2interface.tellstopped(opts.start,opts.num) 
        
        if not objs: 
            self.pfeedback( 'No more stoped downloads' )
            return False
            
        self.poutput( render('/downloadList.tmplc', objs=objs) )
        
        if len(objs) < opts.num: return False 
        
        self.handle_inifite_results(self.tellstopped, '-s %s -n %s' %(opts.start+opts.num,opts.num ))
    
    @command('waiting')
    @option( [make_option("-s", "--start", action="store", type="int", dest="start", default=0),
              make_option("-n", "--num" , action='store', type='int', dest='num', default=10),
              ] )
    def tellwaiting(self, args, opts):
        """ Return list of waiting downloads """
        if args: self.pfeedback("no arg require")
        
        objs = self.aria2interface.tellwaiting(opts.start,opts.num) 
        
        if not objs: 
            self.pfeedback( 'No more waiting downloads' )
            return False

        self.poutput( render('/downloadList.tmplc', objs=objs) )
        
        if len(objs) < opts.num: return False 
        self.handle_inifite_results(self.tellwaiting, '-s %s -n %s' %(opts.start+opts.num,opts.num ))

    @command()
    def purge(self, arg):
        """ purges completed/error/removed downloads to free memory """
        if self.aria2interface.purge():
            self.poutput( 'Downloads purged' )
        else:
            self.poutput( 'Unknow error')
        return False
    
    @command('q', 'quit', 'bye')
    def quit(self, *ignored): return True
