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
import readline

class Formater:
    def __init__(self, obj):
        self.object = obj
    def pprint(self):
        print self.object


class REPL:
    def __init__(self):
        self.cmd = {}
        self.formater = {}
        
        self.cmd["help"] = self.print_cmd
    
    def completer(self, text, state):
        '''Readline auto completer.'''
        match = []
        line = readline.get_line_buffer().lstrip()
        parts = line.split()
        
        cmdkeys = self.cmd.keys()
        cmdkeys.extend(['quit', 'bye', 'exit'])
        for k in cmdkeys:
            if k.startswith(text):
                match.append(k+" ")
        if state < 0:
            return match
        if len(match) > state:
            return match[state]
        else:
            return None
            
    def interactive(self):
        '''Start interactive mode.'''
        readline.set_completer(self.completer)
        readline.parse_and_bind('tab: complete')

        while True:
            try:
                line = raw_input('> ')
                if not line: continue
            except EOFError:
                print
                break

            parts = line.strip().split()
            cmd = parts[0]
            cmd = cmd.lower()
            if cmd in set(['quit', 'bye', 'exit']):
                break
            self.do_cmd(parts)
            
    def do_cmd(self, parts):
        cmd = parts[0]
        args = parts[1:]
        if cmd in self.cmd:
            if args:
                rep = self.cmd[cmd](*args)
            else:
                rep = self.cmd[cmd]()
        else:
            print "Error cmd"
        if not isinstance(rep, list):
            rep =[rep]
            
        def wrapper(obj, formaters):
            for knowObj in formaters:
                if isinstance(obj, knowObj):
                    return self.formater[knowObj](obj).pprint()
            return Formater(obj).pprint()
        for obj in rep:
            wrapper(obj, self.formater)

    
    def register_obj(self, obj ):
        """ Register method obj as cmd
        method must start with do_
        arg are passed as dict
        """
        import re
        pattern = re.compile("^do_.*")
        for name in dir(obj):
            item = getattr(obj, name)
            if callable(item) and pattern.match(name):
                name = name.lower()[3:]
                self.cmd[name] = item
                
    def print_cmd(self):
        for cmd in self.cmd:
            print str(cmd)
            print self.cmd[cmd].__doc__
    
    def register_formater(self, objtype, formater):
        """ Register a console formater for an object type
        :param objtype classobject
        :param formater classobject inherited from Formater
        """
        assert issubclass(formater, Formater)
        self.formater[objtype] = formater
