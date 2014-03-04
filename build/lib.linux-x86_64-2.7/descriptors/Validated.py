# descriptors.Validated
#
# Implements the Validated metaclass, from which classes using
# attributes validated by a Descriptor should inherit.

from __future__ import print_function, unicode_literals, division

from collections import OrderedDict

from descriptors import Descriptor
from descriptors.utils.Prepareable import Prepareable


class Validated(Prepareable):
    """By inheriting from this metaclass, classes can conveniently use
    descriptors to create automatically validated attributes like
    this:

        class ExistingFile(Validated):
            path = ExistingPath()
            name = String()
            size = Integer()

    """

    def __prepare__(cls, bases, *args, **kwargs):
        return OrderedDict()

    def __new__(cls, *args, **kwargs):
        """Go through cls' class dict, collect all Descriptor instances,
        and then set the name attributes for those descriptors.

        """
        clsdict = dict(cls.__dict__)
        fields = [k for k, v in clsdict.items() if isinstance(v, Descriptor)]
        for name in fields:
            clsdict[name].name = name
        ty = type(cls.__name__, (object, ), clsdict)
        clsobj = ty(*args, **kwargs)
        clsobj.__init__(*args, **kwargs)
        return clsobj
