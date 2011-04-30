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

from blinker import signal

from mypyapp.log import debug, error

__PLUGIN__ = 'Alldebrid'

class Alldebrid(object):

    def __init__(self, conf):
        
        if "alldebrid" not in conf:
            error("alldebrid config not in your config file !")
            return
        
        self.conf = conf.get("alldebrid")
        
        if "username" not in self.conf:
            error("Alldebrid: Please specify an username in your config file !")
            return
        
        self.username = self.conf["username"]
        
        if "password" not in self.conf:
            error("Alldebrid: Please specify a password in your config file !")
            return
            
        self.password = self.conf["password"]
        
        self.connected = False
        self.browser = mechanize.Browser()
        signal('DECRYPT_request').connect(self.handle_request)
    
    def connect(self):
        debug( "Alldebrid: connection" )
        self.browser.open("http://www.alldebrid.com")
        for form in self.browser.forms():
            self.browser.form = form
            break
        self.browser.form.find_control(name="pseudo").value = self.username
        self.browser.form.find_control(name="password").value = self.password 
        self.browser.submit()
        self.connected = True
    
    def handle_request(self, request):
        have_results = False
        for target in request.get_undecrypt_targets(self):
            r = self.decrypt(target.link)
            if r:
                have_results = True
                debug( "Alldebrid: link %s decrypted: %s" % (target, r) )
                target.add_download_link(r, self)
        return have_results
    
    
    def decrypt(self, url):
        if not self.isconnect():
            self.connect()
            
        self.browser.open("http://www.alldebrid.com/service.php?link="+urllib.quote(url)+"&nb=0")
        rep = self.browser.response().get_data()
        if  rep[0] == '0':
            urls = re.findall(r'href=[\'"]?([^\'" >]+)', rep)
            return urls[0]
        else:
            debug( "Alldebrid link: %s can't be decrypt:%s : %s" % ( url, rep[0] ,rep.split(":", 1)[1] ) )
            return False
                
    def isconnect(self):
        return self.connected
