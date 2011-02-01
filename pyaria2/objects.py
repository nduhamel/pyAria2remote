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

from formater import Formaters, ConsolFormater
from utils import time_string, simple_eta, percent, sizeof_humanreadable

class AriaDownload():
    def __init__(self, data):
        self.__dict__.update(data)
    
    def __getitem__(self, key):
        return self.__dict__[key]
        

class FormaterAriaDownload(ConsolFormater):
    obj = AriaDownload
    
    @classmethod
    def format(cls, ariadownload):
        
        first_line = "id: %s  file: %s" % (ariadownload.gid, ariadownload.files[0]["path"])
        
        eta = simple_eta( int(ariadownload.totalLength) - int(ariadownload.completedLength), int(ariadownload.downloadSpeed) )
        
        
        second_line = "%s/s %.1f%%   %s/%s avec %s connexions dans: %s" % (sizeof_humanreadable(ariadownload.downloadSpeed),
                                    percent(int(ariadownload.completedLength), int(ariadownload.totalLength)),
                                    sizeof_humanreadable(ariadownload.completedLength), 
                                    sizeof_humanreadable(ariadownload.totalLength),
                                    ariadownload.connections,
                                    time_string(eta),
                                    )
                                    
        printable = first_line + '\n' + second_line
        return printable
