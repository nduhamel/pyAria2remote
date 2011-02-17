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
import mypyapp.config
import logging

class ControlerType(type):
    def __init__(cls, name, bases, attrs):

        if cls.__module__.split('.')[0] != 'mypyapp':
            mypyapp.config.INSTALLED_APP.append( cls.__module__ )
            
            log_file = '/tmp/' + cls.__module__.split('.')[0] + '.log'
            logging.basicConfig(filename=log_file,level=logging.DEBUG)
            
            logger = logging.getLogger(name)
            setattr(cls, 'logger', logger)
        
        for key, val in attrs.iteritems():
            commands = getattr(val, 'command', None)
            if commands:
                for cmd in commands:
                    cmd = "do_%s" % cmd
                    setattr(cls, cmd, val)
