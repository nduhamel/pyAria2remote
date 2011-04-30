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
import re
import mechanize

from blinker import signal

from mypyapp.log import debug, error

from mypyapp.htmlparser import get_parser

__PLUGIN__ = 'Filesonicfolder'

URL_SCHEME = "http://www\.filesonic\.pl/folder/*"

class Filesonicfolder(object):
    def __init__(self, conf):
        self.Browser = mechanize.Browser()
        self.Browser.set_handle_robots(False)
        signal('DECRYPT_request').connect(self.check_url)
    
    def check_url(self, request):
        have_results = False
        for target in request.targets:
            if re.findall(URL_SCHEME, target.link):
                debug("Filesonicfolder: %s is a filesonic folder url" % target.link)
                have_results = True
                for res in self.process(target.link):
                    request.add_target( res )
                request.remove_target( target.link )
        return have_results
    
    def process(self, link):
        self.Browser.open(link)
        rep =self.Browser.response()
        
        parser = get_parser()()
        document = parser.parse(rep, 'utf-8')
        table = document.xpath("//div[@id='mainContent']//table")[0]
        links = []
        for a in table.xpath(".//td/a"):
            link = a.get("href")
            debug("Filesonicfolder: link found %s" % link)
            links.append( link )
        return links
