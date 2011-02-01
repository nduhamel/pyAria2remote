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
from ..module import ModuleMount, MountPoint

class Decrypter(MountPoint,object):
    """
    Mount point for decrypter plugins

    Decrypters implementing this reference should provide the following attributes:
    
    ========  ========================================================
    decrypt([url]) return [decrypted_url or False] raise an Error if not
                   available
    ========  ========================================================
    """
    __metaclass__ = ModuleMount
    


