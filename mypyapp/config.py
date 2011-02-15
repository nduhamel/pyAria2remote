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
import os

from lib.configobj import ConfigObj

INSTALLED_APP = []

def _getConfObj():
    return ConfigObj("".join((os.path.basename(sys.argv[0]).split('.')[0],'.conf')))

class ConfWrapper(object):
    
    def __init__(self, confobj):
        self.confobj = confobj
        
    def __getitem__(self, key):
        try:
            return self.confobj.__getitem__(key)
        except KeyError:
            return None
            
    def debug(self):
        print self.confobj
        


def getConfig(name):
    config = _getConfObj()
    section = config[name]
    return ConfWrapper(section)


class LoadConfig(object):
    """ Add a _conf attr with the conf object """
    
    def __init__(self):
        if hasattr(self, 'CONFIG'):
            self._conf = getConfig(self.CONFIG)            
