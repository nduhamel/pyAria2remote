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

from lib.timer import RepeatTimer
from lib.pyperclip import getcb, setcb

from utils import stdoutLock

import sys

class ClipboardWatcher(object):
    
    @classmethod
    def set_onClip(cls, onClipFct):
        cls.onclip = onClipFct
        cls.timer = RepeatTimer(5, cls.check, 0)
        cls.timer.start()
    
    @classmethod
    def check(cls):
        pass

    @classmethod
    def onClip(cls, txt):
        cls.onclip(cls.onclip.__self__, txt)
