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

class Alldebrid(base.Decrypter):
    #~ name = 'Alldebrid'
    
    #~ def do(self, links):
        #~ return self.links(links)
    #~ 
    #~ def __init__(self, user, passwd):
        #~ self.load(user, passwd)
    
    def decrypt(self, urls):
        pass
        
    #~ def load(self,user, passwd):
        #~ self.user = user
        #~ self.passwd = passwd
        #~ self.browser = mechanize.Browser()
        #~ self.connect()
        #~ 
    #~ def connect(self):
        #~ """ Connect to the website """
        #~ self.browser.open("http://www.alldebrid.com")
        #~ for form in self.browser.forms():
            #~ self.browser.form = form
            #~ break
        #~ self.browser.form.find_control(name="pseudo").value = self.user
        #~ self.browser.form.find_control(name="password").value = self.passwd 
        #~ self.browser.submit()
        #~ 
    #~ def isconnect(self):
        #~ """ Return True or False """
        #~ pass
        #~ 
    #~ def link(self, link):
        #~ """ prend un lien et retourne un lien debrider """
        #~ self.browser.open("http://www.alldebrid.com/service.php?link="+urllib.quote(link)+"&nb=0")
        #~ rep = self.browser.response().get_data()
        #~ if  rep[0] == '0':
            #~ urls = re.findall(r'href=[\'"]?([^\'" >]+)', rep)
            #~ return urls[0]
        #~ else:
            #~ return False
            #~ 
    #~ def links(self, links):
        #~ """ prend une liste et retoure une liste """
        #~ return [self.link(url) for url in links]
    
    
