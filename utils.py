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

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def simple_eta(size, speed):
    if speed == 0:
        return 0
    return size/speed

def achievepercent(total, completed):
    if total == 0:
        return 0
    return (completed*100/total)



import UserDict

class ReadOnlyDict(UserDict.IterableUserDict):
    def __setitem__(self, key, item): raise TypeError
    def __delitem__(self, key): raise TypeError
    def clear(self): raise TypeError
    def pop(self, key, *args): raise TypeError
    def popitem(self): raise TypeError
    
    def update(self, dict=None):
        if dict is None:
            pass
        elif isinstance(dict, UserDict.UserDict):
            self.data = dict.data
        elif isinstance(dict, type({})):
            self.data = dict
        else:
            raise TypeError
