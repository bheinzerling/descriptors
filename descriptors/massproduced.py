# descriptors.massproduced
#
# Generates Descriptor classes whose functionality can be
# implemented with a single function.

from __future__ import print_function, unicode_literals, division

import os

from descriptors import Descriptor
from descriptors.builtin_types import builtins_str, builtins_camel
from descriptors.docstrings import docstrings


range_funcs = [
    #(Descriptor name, function to satisfy, __init__ arg names)
    ("Positive", lambda x: x > 0, []),
    ("SemiPositive", lambda x: x >= 0, []),
    ("Negative", lambda x: x < 0, []),
    ("SemiNegative", lambda x: x <= 0, []),
    ("NotZero", lambda x: x != 0, []),
    ("GreaterThan", lambda x, a: x > a, ["threshold"]),
    ("GreaterThanOrEqual", lambda x, a: x >= a, ["threshold"]),
    ("LessThan", lambda x, a: x < a, ["threshold"]),
    ("LessThanOrEqual", lambda x, a: x <= a, ["threshold"]),
    ("InRange", lambda x, a, b: a <= x <= b, ["lower_bound", "upper_bound"])]

misc_funcs = [
    ("NotNone", lambda x: x is not None, []),
    ("Callable", lambda x: callable(x), []),
    ("HasAttr", lambda x, a: hasattr(x, a), ["attribute"]),
    ("Satisfies", lambda x, a: a(x), ["function"]),
    ("NotSatisfies", lambda x, a: not a(x), ["function"]),
    ("Length", lambda x, a: len(x) == a, ["length"]),
    ("MinLength", lambda x, a: len(x) >= a, ["min_length"]),
    ("MaxLength", lambda x, a: len(x) <= a, ["max_length"]),
    ("ExistingPath", lambda x: os.path.exists(x), [])]

# Turn the builtins tuple into a list like the other funcs lists
builtin_func_els = ", ".join([
    '("{name}", lambda obj: isinstance(obj, {ty}), [])'.format(
        name=b_camel,
        ty=b_str)
    for b_str, b_camel in zip(builtins_str, builtins_camel)])
list_code = "builtin_funcs = [{}]".format(builtin_func_els)
exec(list_code, locals())

funcs = builtin_funcs + range_funcs + misc_funcs


def create_init(attrs):
    """Create an __init__ method that sets all the attributes
    necessary for the function the Descriptor invokes to check the
    value.

    """
    args = ", ".join(attrs)
    vals = ", ".join(['getattr(self, "{}")'.format(attr) for attr in attrs])
    attr_lines = "\n    ".join(
        ["self.{attr} = {attr}".format(attr=attr) for attr in attrs])
    init_code = """def _init(self, {args}):
    super(self.__class__, self).__init__()
    {attr_lines}
    self.field_type += "({{}})".format(
        ", ".join([str(val) for val in [{vals}]]))
    """.format(args=args, attr_lines=attr_lines, vals=vals)
    exec(init_code, globals())
    return _init


def create_setter(func, attrs):
    """Create the __set__ method for the descriptor."""
    def _set(self, instance, value, name=None):
        args = [getattr(self, attr) for attr in attrs]
        if not func(value, *args):
            raise ValueError(self.err_msg(instance, value))
    return _set


def make_class(clsname, func, attrs):
    """Turn a funcs list element into a class object."""
    clsdict = {"__set__": create_setter(func, attrs)}
    if len(attrs) > 0:
        clsdict["__init__"] = create_init(attrs)
    clsobj = type(str(clsname), (Descriptor, ), clsdict)
    clsobj.__doc__ = docstrings.get(clsname)
    return clsobj


# create all descriptors classes from funcs and put them in this module
desc_dict = {
    name: make_class(name, func, attrs) for name, func, attrs in funcs}
globals().update(desc_dict)
