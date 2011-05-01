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
from blinker import signal

import configobj

from mypyapp.console import ConsoleApp, command, option, make_option
from mypyapp.completer import FilePathCompleter
from mypyapp.templates import render
from mypyapp.config import UserConfig
import mypyapp.log

from .aria2interface import Aria2Interface
from .decrypter import Decrypter
from .utils import isUrl, tagetUrlIsText, sort
from .model import AriaDownload

mypyapp.log.init(mypyapp.log.DEBUG)

CONF = {'aria2remote':{
                            'server': '127.0.0.1',
                            'port'  : '6800',
                            'plugins' : ['fileservefolder','filesonicfolder'],
                        }
}


class Aria2console(ConsoleApp):
    
    CONFIG = "Aria2console"   
    prompt = "\x1b[1m\x1b[35mAria>\x1b[0m "

    def load(self):
        self.config = UserConfig("aria2remote", default=CONF)
        
        self.aria2interface = \
             Aria2Interface(self.config['aria2remote']['server'], \
                            self.config['aria2remote']['port'])
                            
        self.decrypter = Decrypter()

        
        #Load plugin:
        if "plugins" in self.config['aria2remote'].keys():
            loaded = []
            for plugin in self.config['aria2remote']['plugins']:
                package_name = 'pyaria2.plugins.%s' % plugin
                loaded.append( __import__(package_name, fromlist=[plugin,]) )
            
            plugins = []
            for plugin in loaded:
                cls = getattr(plugin, plugin.__PLUGIN__)
                obj = cls(self.config)
                plugins.append(obj)
            self.plugins = plugins
        else:
            self.plugins = []
        
    @command('add')
    @option([make_option("-f", "--file", action="store", type="string", dest="filename", completer=FilePathCompleter),
             make_option("-d", action="store_true", dest="decrypt"),])
    def addurls(self, args, opts):
        """Download urls.  
        add url [ulr,]
        add -f linksfile"""
        
        links = args
        
        # Extend links with links from file
        if opts.filename: 
            with open(opts.filename, 'r') as f:
                #One link per line and filter empty line
                l = [line.strip('\n') for line in f.readlines() if line.strip('\n ')]
                links.extend(l)
        
        #Check links        
        links , badlinks = sort(isUrl,links)
        
        for link in badlinks:
            mypyapp.log.error("Error '%s' is not a valid url " % link)
            self.pfeedback( "Error '%s' is not a valid url " % link)
        
        #Case where there is no (valid) link
        if not links:
            mypyapp.log.error("No valid url provided. Abord.")
            self.pfeedback("No valid url provided. Abord.")
            return False
        
        #Check if url don't point to a text/html file
        need_decrypt , links = sort(tagetUrlIsText, links)
        
        #Ask for decrypt link
        to_decrypt = []
        for link in need_decrypt:
            if not opts.decrypt:
                question = "The url (%s) point to an HTML document\nIs it expected ?" % link
                choice = self.select( ( (1,"cancel"), (2,"download"), (3,"decrypt") ),prompt=question)
                if choice == 1 : continue
                if choice == 2 : links.append(link)
                if choice == 3 : to_decrypt.append(link)
            else: 
                to_decrypt.append(link)
        
        options = {'max-connection-per-server':'2'}
        started = [ self.aria2interface.adduri([link], options) for link in links]

        for i in to_decrypt:
            self.decrypter.add(i)
        
        
        for request in self.decrypter.join():
            for target in request.targets:
                if target.sources:
                    mypyapp.log.debug( "%s : decrypted" % target.link )
                    self.aria2interface.adduri( target.sources , options)
                else:
                    mypyapp.log.error( "%s : can't be decrypted" % target.link )
        
        return False
    
    @command()
    def status(self, args):
        args = args.split()
        if not args:
            mypyapp.log.error( "You must specify a download id" )
            self.pfeedback( "You must specify a download id" )
            return False
        
        if len(args) > 1:
            mypyapp.log.error( "You must specify only one download id" )
            self.pfeedback( "You must specify only one download id" )
            return False
            
        objs = self.aria2interface.tellstatus(args[0])
        self.poutput( render('/downloadList.tmplc', objs=[objs]) )
        
        return False
        
    
    ####################################################################
    ## Final
    @command()
    @option([make_option("-i", "--id", action="store", type="string", dest="gid"),
            ])
    def pause(self, args, opts):
        if opts.gid:
            rep = self.aria2interface.pause(opts.gid)
            self.poutput(str(rep))
        else:
            self.poutput( 'You must specify a download id with option -i' )
    
    @command()
    def pauseall(self, args):
        if self.aria2interface.pauseall():
            self.poutput( 'All downloads paused' )
        else:
            self.poutput( 'Unknow error')
        return False
    
    @command()
    @option([make_option("-i", "--id", action="store", type="string", dest="gid"),
            ])
    def unpause(self, args, opts):
        if opts.gid:
            rep = self.aria2interface.unpause(opts.gid)
            self.poutput(str(rep))
        else:
            self.poutput( 'You must specify a download id with option -i' )
    
    @command()
    def unpauseall(self, args):
        if self.aria2interface.unpauseall():
            self.poutput( 'All downloads unpaused' )
        else:
            self.poutput( 'Unknow error')
        return False
    
    @command()
    @option([make_option("-i", "--id", action="store", type="string", dest="gid"),
            ])
    def remove(self, args, opts):
        if opts.gid:
            rep = self.aria2interface.remove(opts.gid)
            self.poutput(str(rep))
        else:
            self.poutput( 'You must specify a download id with option -i' )
    
        
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
    
    @command()
    def option(self, arg):
        rep = self.aria2interface.getglobaloption()
        self.poutput( render('/options.tmplc', objs=rep) )
        return False
    
    @command('q', 'quit', 'bye')
    def quit(self, *ignored): return True
