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
import os

def get_home_dir():
    """
    Return user home directory
    """
    try:
        path = os.path.expanduser('~')
    except:
        path = ''
    for env_var in ('HOME', 'USERPROFILE', 'TMP'):
        if os.path.isdir(path):
            break
        path = os.environ.get(env_var, '')
    if path:
        return path
    else:
        raise RuntimeError('Please define environment variable $HOME')



def sizeof_humanreadable(num):
    num = float(num)
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

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
