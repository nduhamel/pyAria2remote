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
import copy

from blinker import signal

from mypyapp.log import debug, error

class Target(object):
    def __init__(self, url):
        self._url = url
        self._decrypted_by = []
        self._sources = []
    
    def add_download_link(self, link, decrypter):
        self._sources.append(link)
        self._decrypted_by.append(decrypter)
    
    def already_decrypt(self, decrypter):
        return decrypter in self._decrypted_by
        
    @property
    def sources(self):
        return copy.copy(self._sources)
    
    @property
    def link(self):
        return self._url

class Request(object):
    def __init__(self, original_link):
        self._original_link = original_link
        self._targets = [ Target(original_link) , ]
    
    def add_target(self, target_link):
        """ Some link can point to multiple target here add a target"""
        debug("Request %s: add target %s" % (self._original_link, target_link) )
        self._targets.append( Target(target_link) )
    
    def remove_target(self, link):
        for target in self._targets:
            if link == target.link:
                debug( "Request %s: remove target %s" % (self._original_link, link) )
                self._targets.remove(target)
        
    def get_undecrypt_targets(self, decrypter_filtre):
        for target in self._targets:
            if not target.already_decrypt(decrypter_filtre):
                yield target
        
    @property
    def targets(self):
        return self._targets
    
    @property
    def source(self):
        return self._original_link

    

class Decrypter(object):
    
    def __init__(self):
        self._requests = []
        self._decrypt_signal = signal('DECRYPT_request')

    def add(self, link):
        self._requests.append( Request(link) )
        debug("Decrypter: add link: %s" % link)
    
    def join(self):
        for req in self._requests:
            have_results = True
            while have_results:
                responses = self._decrypt_signal.send(req)
                have_results = [ rep for rep in responses if rep[1]]
                debug("Decrypter request: %s result %s" % (req.source,bool(have_results)) )
        return self._requests
