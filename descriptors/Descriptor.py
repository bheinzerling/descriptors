# descriptors.Descriptor
#
# Implements the Descriptor class from which all the descriptors
# in the descriptors package inherit.

from __future__ import print_function, unicode_literals, division

import sys


def with_metaclass(meta, *bases):
    """Armin Ronacher's version of six.with_metaclass.
    http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/

    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass(str("temporary_class"), None, {})


class DescriptorMeta(type):
    """The sole purpose of this metaclass is to automatically append a
    call to Descriptor.__set__() to the __set__() method of derived
    classes, so we don't have to manually do that for every Descriptor
    we create. This can be disabled by creating a "no_autoset" class
    attribute in the derived class.

    """
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super(DescriptorMeta, cls).__new__(
            cls, clsname, bases, clsdict)
        if "no_autoset" in clsdict:
            return clsobj
        if hasattr(clsobj, "__set__"):
            setter = getattr(clsobj, "__set__")
            new_setter = cls.add_super__set__(clsobj, setter)
            setattr(clsobj, "__set__", new_setter)
        return clsobj

    def add_super__set__(clsobj, func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            next_cls = clsobj.__mro__[1]
            if hasattr(next_cls, "__set__"):
                super_setter = getattr(next_cls, "__set__")
                super_setter(*args, **kwargs)
        return wrapper


class Descriptor(with_metaclass(DescriptorMeta, object)):
    """The Descriptor base class from which all other descriptors
    inherit.

    """
    def __init__(self):
        self.field_type = self.__class__.__name__

    def __set__(self, instance, value, name=None):
        if name is None:
            name = self.name
        else:  # __set__ was originally called by a composed descriptor
            self.name = name
        instance.__dict__[name] = value

    def __get__(self, instance, cls):
        try:
            return instance.__dict__[self.name]
        except KeyError:
            raise AttributeError

    def __delete__(self, instance):
        del instance.__dict__[self.name]

    def __repr__(self):
        return "<Descriptor: {} at {}>".format(self.field_type, hex(id(self)))

    def err_msg(self, instance, value):
        """Return an error message for use in exceptions thrown by
        subclasses.

        """
        if not hasattr(self, "name"):
            # err_msg will be called by the composed descriptor
            return ""
        return (
            "Attempted to set the {f_type} attribute {inst}.{attr} to the "
            "{val_type} value {val}, which does not satisfy the condition "
            "{f_type}.".format(
                f_type=self.field_type,
                inst=instance.__class__.__name__,
                attr=self.name,
                val_type=value.__class__.__name__,
                val=value))

    @staticmethod
    def assert_descriptor(obj):
        """Assert that obj is a Descriptor instance."""
        if not isinstance(obj, Descriptor):
            raise TypeError(
                "Cannot combine with a non-Descriptor instance.")

    @staticmethod
    def __create_new(field_type, set_func):
        clsdict = {"__set__": set_func, "no_autoset": True}
        new_desc = type(str(field_type), (Descriptor, ), clsdict)()
        new_desc.field_type = field_type
        return new_desc

    def __and__(self, other):
        """Create a conjunction of this descriptor and another
        descriptor.

        """
        Descriptor.assert_descriptor(other)
        setter1 = self.__class__.__set__
        setter2 = other.__class__.__set__

        def new_set(new_self, instance, value, name=None):
            if name:
                new_self.name = name
            try:
                setter1(self, instance, value, name=new_self.name)
                value = getattr(instance, new_self.name)
                setter2(other, instance, value, name=new_self.name)
                value = getattr(instance, new_self.name)
                super(new_self.__class__, new_self).__set__(
                    instance, value, name)
            except ValueError:
                raise ValueError(new_self.err_msg(instance, value))

        new_field_type = self.field_type + "_AND_" + other.field_type
        new_desc = Descriptor.__create_new(new_field_type, new_set)
        return new_desc

    def __or__(self, other):
        """Create a disjunction of this descriptor and another
        descriptor.

        """
        Descriptor.assert_descriptor(other)
        setter1 = self.__class__.__set__
        setter2 = other.__class__.__set__

        def new_set(new_self, instance, value, name=None):
            if name:
                new_self.name = name
            exceptions = 0
            for setter, caller in zip((setter1, setter2), (self, other)):
                try:
                    setter(caller, instance, value, name=new_self.name)
                    return  # one descriptor satisfied
                except ValueError as e:  # Descriptors throw ValueErrors
                    if Descriptor.exc_thrown_by_descriptor():
                        exceptions += 1
                    else:
                        raise e
            if exceptions >= 2:
                raise ValueError(new_self.err_msg(instance, value))

        new_field_type = self.field_type + "_OR_" + other.field_type
        new_desc = Descriptor.__create_new(new_field_type, new_set)
        return new_desc

    @staticmethod
    def exc_thrown_by_descriptor():
        """Return True if the last exception was thrown by a
        Descriptor instance.

        """
        traceback = sys.exc_info()[2]
        tb_locals = traceback.tb_frame.f_locals
        # relying on naming convention to get the object that threw
        # the exception
        if "self" in tb_locals:
            if not isinstance(tb_locals["self"], Descriptor):
                return False
            return True
        return False
