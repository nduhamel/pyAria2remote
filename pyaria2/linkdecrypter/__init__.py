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
# Taken from Python 2.7 with permission from/by the original author.
import pkgutil
import inspect

from mypyapp.config import getConfig

from base import *

"""
Import all installed in conf plugins
"""

conf =  getConfig("Aria2console")


if type(conf['decrypter']) == type([]):    
    active_mod = map((lambda s: "%s.%s" % (__name__, s)), conf['decrypter'])
else:
    active_mod = "%s.%s" % (__name__,conf['decrypter'])

for importer, modname, ispkg in pkgutil.iter_modules(__path__,__name__+'.'):
    if modname == __name__+'.base': continue
    if modname in active_mod:
        __import__(modname, fromlist="dummy")

__all__ = ["Decrypter"]
