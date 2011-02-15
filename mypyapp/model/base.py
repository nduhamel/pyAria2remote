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
from mypyapp.model.exception import DuplicatePropertyError, BadValueError, DerivedPropertyError


def _initialize_properties(model_class, name, bases, dct):
  """Initialize Property attributes for Model-class.

  Args:
    model_class: Model class to initialize properties for.
  """
  model_class._properties = {}


  defined = set()
  #spr the base cls handling

  for attr_name in dct.keys():
    attr = dct[attr_name]
    if isinstance(attr, Property):
      if attr_name in defined:
        raise DuplicatePropertyError('Duplicate property: %s' % attr_name)
      defined.add(attr_name)
      model_class._properties[attr_name] = attr
      attr.__property_config__(model_class, attr_name)

  model_class._all_properties = frozenset(
      prop.name for name, prop in model_class._properties.items())

class PropertiedClass(type):
  """Meta-class for initializing Model classes properties.

  Used for initializing Properties defined in the context of a model.
  By using a meta-class much of the configuration of a Property
  descriptor becomes implicit.  By using this meta-class, descriptors
  that are of class Model are notified about which class they
  belong to and what attribute they are associated with and can
  do appropriate initialization via __property_config__.

  Duplicate properties are not permitted.
  """

  def __init__(cls, name, bases, dct):
    super(PropertiedClass, cls).__init__(name, bases, dct)

    _initialize_properties(cls, name, bases, dct)

class Property(object):
    """ Property data descriptor """
    
    def __init__(self, 
                 name=None,
                 validator=None,
                 required=False):
        
        self.name = name
        self.validator = validator
        self.required = required
    
    def __property_config__(self, model_class, property_name):
        """Configure property, connecting it to its model.

        Configure the property so that it knows its property name and what class
        it belongs to.

        Args:
        model_class: Model class which Property will belong to.
        property_name: Name of property within Model instance to store property
        values in.  By default this will be the property name preceded by
        an underscore, but may change for different subclasses.
        """
        self.model_class = model_class
        if self.name is None:
            self.name = property_name

    def __get__(self, model_instance, model_class):
        """Returns the value for this property on the given model instance.

        See http://docs.python.org/ref/descriptors.html for a description of
        the arguments to this class and what they mean."""
        if model_instance is None:
            return self

        try:
            return getattr(model_instance, self._attr_name())
        except AttributeError:
            return None

    def __set__(self, model_instance, value):
        """Sets the value for this property on the given model instance."""
        value = self.validate(value)
        setattr(model_instance, self._attr_name(), value)
    
    def _attr_name(self):
        """Attribute name we use for this property in model instances.

        DO NOT USE THIS METHOD.
        """
        return '_' + self.name
    def empty(self, value):
        """Determine if value is empty in the context of this property.

        For most kinds, this is equivalent to "not value", but for kinds like
        bool, the test is more subtle, so subclasses can override this method
        if necessary.

        Args:
            value: Value to validate against this Property.

        Returns:
            True if this value is considered empty in the context of this Property
            type, otherwise False.
        """
        return not value

    def validate(self, value):
        """Assert that provided value is compatible with this property.

        Args:
        value: Value to validate against this Property.

        Returns:
        A valid value, either the input unchanged or adapted to the
        required type.

        Raises:
        BadValueError if the value is not appropriate for this
        property in any way.
        """
        if self.empty(value):
            if self.required:
                raise BadValueError('Property %s is required' % self.name)
        #removed choice handler
        if self.validator is not None:
            self.validator(value)
        return value
    
    def get_informal_string(self,model_instance):
        return self.__get__(model_instance, model_instance.__class__)

class ComputedProperty(Property):
    """Property used for creating properties derived from other values.

    Certain attributes should never be set by users but automatically
    calculated at run-time from other values of the same entity.  These
    values are implemented as persistent properties because they provide
    useful search keys.

    Example:

    import string

    class Person(Model):

      name = StringProperty(required=True)

      @db.ComputedProperty
      def lower_case_name(self):
        return self.name.lower()

    # Find all people regardless of case used in name.
    Person.gql('WHERE lower_case_name=:1' % name_to_search_for.lower())
    """

    def __init__(self, value_function):
        """Constructor.

        Args:
            value_function: Callable f(model_instance) -> value used to derive
            persistent property value for storage in datastore.
            indexed: Whether or not the attribute should be indexed.
        """
        super(ComputedProperty, self).__init__()
        self.__value_function = value_function

    def __set__(self, *args):
        """Disallow setting this value.

        Raises:
        DerivedPropertyError when developer attempts to set attribute manually.
        Model knows to ignore this exception when getting from datastore.
        """
        raise DerivedPropertyError(
            'Computed property %s cannot be set.' % self.name)

    def __get__(self, model_instance, model_class):
        """Derive property value.

        Args:
            model_instance: Instance to derive property for in bound method case,
                else None.
            model_class: Model class associated with this property descriptor.

        Returns:
            Result of calling self.__value_funcion as provided by property
            constructor.
        """
        if model_instance is None:
            return self
        return self.__value_function(model_instance)

class Model(object):
    __metaclass__ = PropertiedClass  
    
    @classmethod
    def properties(cls):
        """Returns a dictionary of all the properties defined for this model."""
        return dict(cls._properties)
            
    def __getitem__(self, key):
        if key in self.properties().keys():
            return self.properties()[key].get_informal_string(self)
        else:
            raise KeyError
            
