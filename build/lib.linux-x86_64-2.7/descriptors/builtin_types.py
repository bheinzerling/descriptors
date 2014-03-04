# descriptors.builtin_types
#
# Lists of some of Python's builtin types that are used for
# generating Descriptor classes and their docstrings.

from __future__ import print_function, unicode_literals, division


builtins = (bool, int, float, complex, str, list, dict, set, frozenset, tuple)
builtins_str = [ty().__class__.__name__ for ty in builtins]
upper_first = lambda s: s[0].upper() + s[1:]
builtins_camel = [upper_first(b_str) for b_str in builtins_str]
