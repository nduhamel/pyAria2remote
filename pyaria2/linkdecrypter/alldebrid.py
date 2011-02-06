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

import mechanize
import urllib
import re

import base
from ..config import getConfig

class Alldebrid(base.Decrypter):
   
    def __init__(self):
        super(Alldebrid, self).__init__()
        
    
    def load(self):
        #Load config
        self.conf = getConfig("alldebrid")
        #Load browser
        self.browser = mechanize.Browser()
        
        #Connect
        self.connect()
    
    def connect(self):
        self.browser.open("http://www.alldebrid.com")
        for form in self.browser.forms():
            self.browser.form = form
            break
        self.browser.form.find_control(name="pseudo").value = self.conf['user']
        self.browser.form.find_control(name="password").value = self.conf['password'] 
        self.browser.submit()

    def decrypt(self, url):
        if self.isconnect():
            self.browser.open("http://www.alldebrid.com/service.php?link="+urllib.quote(url)+"&nb=0")
            rep = self.browser.response().get_data()
            print rep
            if  rep[0] == '0':
                urls = re.findall(r'href=[\'"]?([^\'" >]+)', rep)
                return urls[0]
            else:
                print rep[0]
                print rep.split(":", 1)[1]
                return False
                
    def isconnect(self):
        return True
    
    
