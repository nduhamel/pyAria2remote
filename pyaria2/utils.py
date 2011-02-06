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

from threading import Lock

class stdoutLock(object):
    """ Make a function thread safe for a global ressource like stdout"""
    lock = Lock()
 
    def __call__(self, f):
        def lockedfunc(*args, **kwargs):
            with self.lock:
                try:
                    return f(*args, **kwargs)
                except Exception, e:
                    raise
        return lockedfunc


class LimitedSizeList(list):
    __slots__ = ['size']
    
    def __init__(self, itr=[], size=0):
        self.size = size
        if self.size:
            l = list(itr)
            while len(l) > self.size:
                l.pop(0)
            itr = l
        list.__init__(self, itr)
    
    def append(self, item):
        if self.size and len(self) >= self.size:
            list.pop(self,0)
        list.append(self, item)
    
    def extend(self, itr):
        l = list(itr)
        self.size = self.size + len(l)
        list.extend(self,l)
    
    def downsize(self, howmuch = 1):
        if not self.size or self.size == 1: raise ValueError
        self.size = self.size - howmuch
        while len(self) > self.size:
            list.pop(self,0)


import re

URL_RE = ( re.compile("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?/[-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]*[^]'\\.}>\\),\\\"]"),
           re.compile("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?"),
           )
        
def isUrl(str):
    if any(regexp.match(str) for regexp in URL_RE):
        return True

import urllib
def tagetUrlIsText(url):
    u = urllib.urlopen(url)
    content_type = u.info().getheader("Content-Type")
    if "text" in content_type: return True
    return False


def time_string(seconds):
    """Return a human-friendly string representing a time duration.

    Examples:
    >>> time_string(12345)
    '3h26m'

    >>> time_string(61)
    '1m1s'

    >>> time_string(0)
    '0s'
    """
    if seconds < 0:
	return "--"
    units = [(60*60*24, "d"), (60*60, "h"), (60, "m"), (1, "s")]
    parts = []
    for i in range(len(units)):
	unit = units[i]
	if seconds >= unit[0]:
	    break

    if i < len(units) - 1:
	# Round to the smallest unit that will be displayed.
	seconds = units[i+1][0] * round(float(seconds) / units[i+1][0])
	n = int(seconds / unit[0])
	parts.append("%d%s" % (n, unit[1]))
	seconds -= n * unit[0]
	unit = units[i+1]
    n = round(seconds / unit[0])
    parts.append("%d%s" % (n, unit[1]))

    return "".join(parts)

def simple_eta(size, speed):
    if speed == 0:
        return -1
    return size/speed

def percent(val, total):
    val = float(val)
    total = float(total)
    if total == 0:
        return 0
    return (val*100/total)
    
def sizeof_humanreadable(num):
    num = float(num)
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

import optparse
make_option = optparse.make_option

def option(option_list, arg_desc="arg"):
    
    if not isinstance(option_list, list):
        option_list = [option_list]
    
    def option_setup(func):
        parser = optparse.OptionParser(option_list=option_list)
        parser.set_usage("%s [options] %s" % (func.__name__, arg_desc))
        parser._func = func
        def new_func(instance, arg):
            try:
                opts, newArgList = parser.parse_args(arg.split())
 

            except (optparse.OptionValueError, optparse.BadOptionError,
                    optparse.OptionError, optparse.AmbiguousOptionError,
                    optparse.OptionConflictError), e:
                print (e)
                parser.print_help()
                return

            result = func(instance,newArgList,opts)                          
            return result
        if not func.__doc__: func.__doc__ = ''
        new_func.__doc__ = '%s\n%s' % (func.__doc__, parser.format_help())
        return new_func
    return option_setup
