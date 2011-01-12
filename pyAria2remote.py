#!/usr/bin/python
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
import xmlrpclib
import logging
import sys

from repl import Formater, REPL
from utils import sizeof_fmt, simple_eta, achievepercent, ReadOnlyDict

from aria2 import AriaDownload, AriaControler

logger = logging.getLogger()
hdlr = logging.FileHandler('/tmp/pyaria2remote.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


class AriaDownloadFormater(Formater):
    
    def __init__(self, ariadownload):
        assert isinstance(ariadownload, AriaDownload)
        self.download = ariadownload
    
    def pprint(self):       
        print "-------------------------------------------"
        with self.download:
            data = self.download.data
            print "id: "+data["gid"]+"  "+data["files"][0]["path"] + "   " + str(sizeof_fmt(int(data["completedLength"]))) + "/" + \
                     str(sizeof_fmt(int(data["totalLength"])))
            print "Speed: " + sizeof_fmt(int(data["downloadSpeed"])) + "/s     "  + \
                 str(achievepercent(int(data["totalLength"]), int(data["completedLength"]))) + "%"
        print "-------------------------------------------"


if __name__ == '__main__':
    aria = AriaControler()
    app = REPL(configFile="pyaria2.conf")
    app.register_formater(AriaDownload, AriaDownloadFormater)
    app.register_obj(aria)
    app.interactive()
