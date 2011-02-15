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
import cmd
import optparse
import functools

import os
import atexit
import readline
import sys

from .config import LoadConfig
from .bootstrap import ControlerType
from mypyapp.templates import load_template_dir

########################################################################
##  Command history
HISTORY_PATH = "".join((os.path.basename(sys.argv[0]).split('.')[0],'.history'))

if os.path.exists(HISTORY_PATH):
    readline.read_history_file(HISTORY_PATH)

def save_history(historyPath=HISTORY_PATH):
    import readline
    readline.write_history_file(historyPath)

atexit.register(save_history)
## END

def command(*arg):
    def deco(f):
        if arg:
            f.command = arg
        else:
            f.command = [f.__name__]
        return f
    return deco

def make_option(*args, **kwargs):
    """ Wrapper for optparse.Option which add a completer keyword """
    completer = kwargs.pop('completer', None)
    option =  optparse.Option(*args, **kwargs)
    option.completer = completer
    return option


def option(option_list, arg_desc="arg"):
    
    if not isinstance(option_list, list):
        option_list = [option_list]
        
    def option_setup(func):
        parser = optparse.OptionParser(option_list=option_list)
        parser.set_usage("%s [options] %s" % (func.__name__, arg_desc))
        #~ parser._func = func
        
        @functools.wraps(func)
        def new_func(instance, arg):
            try:
                opts, newArgList = parser.parse_args(arg.split())
 

            except (optparse.OptionValueError, optparse.BadOptionError,
                    optparse.OptionError, optparse.AmbiguousOptionError,
                    optparse.OptionConflictError), e:
                print (e)
                parser.print_help()
                return

            result = func(instance,newArgList,opts)                          
            return result
        if not func.__doc__: func.__doc__ = ''
        new_func.__doc__ = '%s\n%s' % (func.__doc__, parser.format_help())
        new_func._parser = parser
        return new_func
    return option_setup


class ConsoleApp(cmd.Cmd, LoadConfig, object):
    """ 
    Define:
        select(options, prompt='Your choice? ')
        poutput(msg)
        pfeedback(msg)
        
    
    Command return code:
        True quit app
        False continue
    """
    __metaclass__ =  ControlerType
    
    verbose = True
    
    def __init__(self):
        LoadConfig.__init__(self)
        cmd.Cmd.__init__(self)
        load_template_dir()
        
    def preloop(self):
        self.load()
    
    def load(self): pass
    
    def handle_inifite_results(self, callback, *args, **kwargs):
        self.stdout.write("---- PRESS ANY KEY OR Q -----")
        line = self.stdin.readline()
        if not len(line):
            line = 'EOF'
        else:
            line = line.rstrip('\r\n')
        if line == "q":
            return
        else:
            callback(*args, **kwargs)
    

    def select(self, options, prompt='Your choice? '):
        '''Presents a numbered menu to the user.  Modelled after
           the bash shell's SELECT.  Returns the item chosen.
           
           Argument ``options`` can be:

             | a single string -> will be split into one-word options
             | a list of strings -> will be offered as options
             | a list of tuples -> interpreted as (value, text), so 
                                   that the return value can differ from
                                   the text advertised to the user 
            
            The last option is the default option when you type enter'''
        if isinstance(options, basestring):
            options = zip(options.split(), options.split())
        fulloptions = []
        for opt in options:
            if isinstance(opt, basestring):
                fulloptions.append((opt, opt))
            else:
                try:
                    fulloptions.append((opt[0], opt[1]))
                except IndexError:
                    fulloptions.append((opt[0], opt[0]))
        self.poutput(prompt)
        for (idx, (value, text)) in enumerate(fulloptions):
            self.poutput('  %2d. %s\n' % (idx+1, text))
        self.poutput("Press ENTER for default: %s" % fulloptions[-1][1])
        while True:
            response = raw_input("Choice: ")
            try:
                response = int(response)
                result = fulloptions[response - 1][0]
                break
            except ValueError:
                if response == '':
                    result = fulloptions[-1][0]
                    break                
                continue# loop and ask again
        return result

    def poutput(self, msg):
        '''Convenient shortcut for self.stdout.write(); adds newline if necessary.'''
        if msg:
            msg = msg.encode('utf-8')
            self.stdout.write(msg)
            if msg[-1] != '\n':
                self.stdout.write('\n')
                
    def pfeedback(self, msg):
        if self.verbose:
            self.poutput(msg)
    
    
    def completedefault(self, text, line, begidx, endidx):
        
        args = line.split()
        cmd = args[0]
        cmd_func = getattr(self, "do_%s" % cmd)
        
        know_options = {}
        
        #Check if function had option parser:
        if hasattr(cmd_func, '_parser'):
            for option in cmd_func._parser.option_list:
                
                if hasattr(option, 'completer'):
                    optname = option._short_opts + option._long_opts
                    for name in optname:
                        know_options[name] = option.completer
        else: return []
        
        #1 cas il existe un blanc en fin de ligne donc nouvel arg
        if len(line) != len(line.strip()):
            previous = args[-1]
            if previous in know_options.keys():
                return know_options[previous]()
        #2 cas on est a la fin d'un mot en fin de ligne
        if endidx == len(line.strip()):
            if  args[-2] in know_options.keys():
                return know_options[args[-2]](args[-1])
        
        return []
