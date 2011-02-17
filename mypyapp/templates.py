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
import mypyapp.config

from os.path import join, normcase, normpath, abspath, isabs, sep

# Define our own abspath function that can handle joining 
# unicode paths to a current working directory that has non-ASCII
# characters in it.  This isn't necessary on Windows since the 
# Windows version of abspath handles this correctly.  The Windows
# abspath also handles drive letters differently than the pure 
# Python implementation, so it's best not to replace it.
if os.name == 'nt':
    abspathu = abspath
else:
    def abspathu(path):
        """
        Version of os.path.abspath that uses the unicode representation
        of the current working directory, thus avoiding a UnicodeDecodeError
        in join when the cwd has non-ASCII characters.
        """
        if not isabs(path):
            path = join(os.getcwdu(), path)
        return normpath(path)

def safe_join(base, *paths):
    """
    Joins one or more path components to the base path component intelligently.
    Returns a normalized, absolute version of the final path.

    The final path must be located inside of the base path component (otherwise
    a ValueError is raised).
    """
    # We need to use normcase to ensure we don't false-negative on case
    # insensitive operating systems (like Windows).
    final_path = normcase(abspathu(join(base, *paths)))
    base_path = normcase(abspathu(base))
    base_path_len = len(base_path)
    # Ensure final_path starts with base_path and that the next character after
    # the final path is os.sep (or nothing, in which case final_path must be
    # equal to base_path).
    if not final_path.startswith(base_path) \
       or final_path[base_path_len:base_path_len+1] not in ('', sep):
        raise ValueError('The joined path (%s) is located outside of the base '
                         'path component (%s)' % (final_path, base_path))
    return final_path

class TemplateDoesNotExist(Exception):
    pass



from mako.template import Template
from mako.lookup import TemplateLookup

TEMPLATE_LOOKUP = None


def load_template_dir():
    global TEMPLATE_LOOKUP
    
    app_template_dirs = []
    for app in mypyapp.config.INSTALLED_APP:
        mod = __import__(app)
        template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
        if os.path.isdir(template_dir):
            app_template_dirs.append(template_dir)
    if app_template_dirs:
        app_template_dirs.append( os.path.join(os.path.dirname(__file__), 'default_templates') )
        TEMPLATE_LOOKUP = TemplateLookup(directories=app_template_dirs, module_directory='/tmp/mypyapp_mako_modules', output_encoding='utf-8', encoding_errors='replace')
    
def render(template_name, **data):
    mytemplate = TEMPLATE_LOOKUP.get_template(template_name)
    return mytemplate.render(**data)
