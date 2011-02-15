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
from mypyapp.model.base import Property
from mypyapp.model.exception import BadValueError

from mypyapp.utils import sizeof_humanreadable

"""
StringProperty   can be multi- or single-line

IntegerProperty
FloatProperty

StorageSizesProperty
"""

class StringProperty(Property):
    """A textual property, which can be multi- or single-line."""

    def __init__(self, verbose_name=None, multiline=False, **kwds):
	    """Construct string property.

	    Args:
	        verbose_name: Verbose name is always first parameter.
	        multi-line: Carriage returns permitted in property.
	    """
	    super(StringProperty, self).__init__(verbose_name, **kwds)
	    self.multiline = multiline

    def validate(self, value):
	    """Validate string property.

	    Returns:
	        A valid value.

	    Raises:
	        BadValueError if property is not multi-line but value is.
	    """
	    value = super(StringProperty, self).validate(value)
	    if value is not None and not isinstance(value, basestring):
	        raise BadValueError(
		        'Property %s must be a str or unicode instance, not a %s'
                % (self.name, type(value).__name__))
	    if not self.multiline and value and value.find('\n') != -1:
	        raise BadValueError('Property %s is not multi-line' % self.name)
	    return value

    data_type = basestring

########################################################################
##
##           Numeric
##
########################################################################

class IntegerProperty(Property):
    """An integer property."""

    def validate(self, value):
        """Validate integer property.

        Returns:
            A valid value.

        Raises:
            BadValueError if value is not an integer or long instance.
        """
        value = super(IntegerProperty, self).validate(value)
        if value is None:
            return value
        if not isinstance(value, (int, long)) or isinstance(value, bool):
            raise BadValueError('Property %s must be an int or long, not a %s'
                          % (self.name, type(value).__name__))
        if value < -0x8000000000000000 or value > 0x7fffffffffffffff:
            raise BadValueError('Property %s must fit in 64 bits' % self.name)
        return value

    data_type = int

    def empty(self, value):
        """Is integer property empty.

        0 is not an empty value.

        Returns:
          True if value is None, else False.
        """
        return value is None

class FloatProperty(Property):
    """A float property."""

    def validate(self, value):
        """Validate float.

        Returns:
            A valid value.

        Raises:
            BadValueError if property is not instance of 'float'.
        """
        value = super(FloatProperty, self).validate(value)
        if value is not None and not isinstance(value, float):
            raise BadValueError('Property %s must be a float' % self.name)
        return value

    data_type = float

    def empty(self, value):
        """Is float property empty.

        0.0 is not an empty value.

        Returns:
            True if value is None, else False.
        """
        return value is None
        
########################################################################
##
##           Special
##
########################################################################

class StorageSizesProperty(Property):
    """ Storage size property """
    
    def validate(self, value):
        """Validate Storage size.

        Returns:
            A valid value as a float.

        Raises:
            BadValueError if property is not instance of 'float' or 'int'.
        """
        value = super(StorageSizesProperty, self).validate(value)
        if value is not None and not isinstance(value, float) and  not isinstance(value, int) :
            raise BadValueError('Property %s must be a float or an int' % self.name)
        return float(value)
    
    data_type = float
    
    def empty(self, value):
        """Is float property empty.

        0.0 is not an empty value.

        Returns:
            True if value is None, else False.
        """
        return value is None
        
    def get_informal_string(self,model_instance):
        value = self.__get__(model_instance, model_instance.__class__)
        return sizeof_humanreadable(value)
