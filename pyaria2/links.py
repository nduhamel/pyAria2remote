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

class Request(object):
    
    def __init__(self, original_link):
        self.request_url = original_link
    
    def __repr__(self):
        return self.request_url

    def append_target(self, link):
        pass

class Source(object):
    """ Handle a source link """
    url = None

class FinalTarget(object):
    pass
    
