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

from configobj import ConfigObj

from utils import get_home_dir


def get_config_dir():
    if not os.path.exists('%s/.config/' % get_home_dir() ):
        os.makedirs( '%s/.config/' % get_home_dir() )
    if not os.path.exists('%s/.config/mypyapp' % get_home_dir() ):
        os.makedirs( '%s/.config/mypyapp' % get_home_dir() )
    return '%s/.config/mypyapp' % get_home_dir()
    

class UserConfig(ConfigObj, object):
    
    def __init__(self, name, default=None, **kwargs):
        self.name = name
        
        filename = '%s/%s.ini' % ( get_config_dir() , self.name)
        
        if not os.path.exists(filename) and default is not None:
            config = default
            super(UserConfig, self).__init__(config, **kwargs)
            self.write(open(filename, 'w'))
        else:
            super(UserConfig, self).__init__(filename, **kwargs)

INSTALLED_APP = []
