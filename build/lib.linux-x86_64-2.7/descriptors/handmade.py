# descriptors.handmade
#
# Implements Descriptor classes that cannot easily be implemented
# with only a single function.

from __future__ import print_function, unicode_literals, division

import os
import re
from numbers import Number

from descriptors import Descriptor
from descriptors.massproduced import create_init


class In(Descriptor):
    """A descriptor that only allows assigning a value if that value is
    a member of a set of given elements.

    Example:
        class A(Validated):
            mood = In(set(["bad", "go away", "Why me!?", ":-("]))

        a = A()
        a.mood = "awesome"
        -> ValueError

    """
    def __init__(self, valid_values):
        create_init(["valid_values"])(self, valid_values)
        if not hasattr(valid_values, "__contains__"):
            raise TypeError(
                "Attempted to create an In-Descriptor with an argument that "
                "doesn't support membership testing.")
        self.valid_values = valid_values

    def __set__(self, instance, value, name=None):
        try:
            if not value in self.valid_values:
                raise ValueError(self.err_msg(instance, value))
        except TypeError:  # raised e.g. when checking if non-str in str
            raise ValueError(self.err_msg(instance, value))


class RegexMatch(Descriptor):
    """A descriptor that ensures the described attribute is only set
    to a string that matches the supplied regular expression.

    """
    def __init__(self, regex):
        create_init(["regex"])(self, regex)
        self.pattern = re.compile(regex)

    def __set__(self, instance, value, name=None):
        if not self.pattern.search(value):
            raise ValueError(self.err_msg(instance, value))


class NotRegexMatch(Descriptor):
    """A descriptor that ensures the described attribute is only set
    to a string that does not match the supplied regular expression.

    """
    def __init__(self, regex):
        create_init(["regex"])(self, regex)
        self.pattern = re.compile(regex)

    def __set__(self, instance, value, name=None):
        if self.pattern.search(value):
            raise ValueError(self.err_msg(instance, value))


class Apply(Descriptor):
    """A descriptor that sets the described attribute to the result
    obtained from applying the supplied function to the value being
    set.

    Example:
        class A(Validated):
            f = Apply(str.lower)

        a = A()
        a.f = "SoMe stRInG"
        print(a.f)
        -> some string

    """
    no_autoset = True

    def __init__(self, func):
        create_init(["func"])(self, func)
        if not callable(func):
            raise TypeError(
                "Tried to create an Apply-Descriptor with a argument "
                "that is not callable.")
        self.func = func

    def __set__(self, instance, value, name=None):
        value = self.func(value)
        super(self.__class__, self).__set__(instance, value, name)


class ForceNumeric(Descriptor):
    """A descriptor that only allows numeric values, with "numeric"
    meaning that the value is
        a) an instance of a subclass of numbers.Number, or
        b) a string that can be converted to a float or int.
    In case a) the value will be passed through as is, in case b)
    the string will be converted to an int or a float, depending
    on the numeric value represented by the string.

    Example:
        class A(Validated):
            f = Numeric()

        a = A()
        a.f = 7.0
        -> ok

        a.f = "7"
        print(a.f)
        -> 7

        a.f = "7.0"
        print(a.f)
        -> 7.0

        a.f = (7, 0)
        -> ValueError

    """
    no_autoset = True

    def __set__(self, instance, value, name=None):
        if not isinstance(value, Number):
            try:
                value = self.try_convert(value)
            except ValueError:
                raise ValueError(self.err_msg(instance, value))
        super(self.__class__, self).__set__(instance, value, name)

    @staticmethod
    def try_convert(value):
        """Convert value to a numeric value or raise a ValueError
        if that isn't possible.

        """
        convertible = ForceNumeric.is_convertible(value)
        if not convertible or isinstance(value, bool):
            raise ValueError
        if isinstance(str(value), str):
            return ForceNumeric.str_to_num(value)
        return float(value)

    @staticmethod
    def is_convertible(value):
        """Return True if value can be converted to a float."""
        try:
            float(value)
            return True
        except ValueError:
            return False
        except TypeError:
            return False

    @staticmethod
    def str_to_num(str_value):
        """Convert str_value to an int or a float, depending on the
        numeric value represented by str_value.

        """
        str_value = str(str_value)
        try:
            return int(str_value)
        except ValueError:
            return float(str_value)


class MadePath(Descriptor):
    """A descriptor that creates the path represented by the passed
    string if that path doesn't exist already.

    """
    def __set__(self, instance, value, name=None):
        if not os.path.exists(value):
            try:
                os.makedirs(value)
            except OSError as e:
                if os.path.exists(value):
                    # path was created in the time since we checked
                    pass
                else:
                    raise e


class EitherOr(Descriptor):
    """A descriptor asserting that either the described attribute OR
    other_attr are True-y, but not both or neither. The descriptor
    is only active if both attributes are not None to allow
    re-setting values.
    If other_attr does not exist, it is assumed to be None.

    Example:
        class A(Validated):
            f1 = EitherOr("f2")
            f2 = EitherOr("f1")

        a = A()
        a.f1 = True
        a.f2 = True
        -> ValueError

    """
    def __init__(self, other_attr):
        create_init(["other_attr"])(self, other_attr)

    def __set__(self, instance, value, name=None):
        if self.other_attr in instance.__dict__:
            other_value = getattr(instance, self.other_attr)
        else:
            other_value = None
        if value is not None and other_value is not None:
            if bool(value) == bool(other_value):
                raise ValueError(self.err_msg(instance, value))
