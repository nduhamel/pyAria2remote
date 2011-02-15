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
from mypyapp.model.base import Model, ComputedProperty
from mypyapp.model.property import StringProperty, IntegerProperty, StorageSizesProperty
from mypyapp.utils import time_string

class AriaDownload(Model):
    
    id             = IntegerProperty()
    filename        = StringProperty()
    totalLength     = StorageSizesProperty()
    completedLength = StorageSizesProperty()
    downloadSpeed   = StorageSizesProperty()
    connections     = IntegerProperty()
    
    @ComputedProperty
    def complete_percent(self):
        """Get the current complete percent."""
        if self.totalLength == 0:
            return '0%'
        return '{0:.2%}'.format(self.completedLength/self.totalLength)
    
    @ComputedProperty
    def eta(self):
        if self.downloadSpeed == 0:
            return -1
        return time_string((self.totalLength-self.completedLength)/self.downloadSpeed)
    
    def __init__(self, data):
        super(AriaDownload, self).__init__()
        self.populate_from_aria(data)
    
    def populate_from_aria(self, response):
        self.id              = int(response['gid'])
        self.filename        = response['files'][0]['path']
        self.totalLength     = int(response['totalLength'])
        self.completedLength = int(response['completedLength'])
        self.downloadSpeed   = int(response['downloadSpeed'])
        self.connections     = int(response['connections'])
