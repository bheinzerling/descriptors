from __future__ import print_function, unicode_literals, division

import unittest
import os
from itertools import product

from descriptors import Descriptor, Validated
from descriptors import _all_descriptors
globals().update(_all_descriptors)


class DescriptorTest(unittest.TestCase):

    def set_assert(self, obj, val, attr="f"):
        """Assert a valid assignment works."""
        setattr(obj, attr, val)
        self.assertEqual(getattr(obj, attr), val)

    def try_set(self, obj, value, attr="f"):
        """Assert an invalid assignment fails."""
        with self.assertRaises(ValueError):
            setattr(obj, attr, value)

    def test_and_with_non_descriptor(self):
        with self.assertRaises(TypeError):
            class A(Validated):
                f = Str() & set()

            A()

    def test_and(self):
        class A(Validated):
            f = Str() & ExistingPath()

        a = A()
        p = os.getcwd()
        self.set_assert(a, p)
        self.try_set(a, 1)
        self.try_set(a, "544gal5j455rij6706oh56")

    def test_or_with_non_descriptor(self):
        with self.assertRaises(TypeError):
            class A(Validated):
                f = List() | list([None, 7])

            A()

    def test_or(self):
        class B(Validated):
            f = Tuple() | List()

        a = B()
        self.set_assert(a, [1, 2])
        self.set_assert(a, (1, 2))
        self.set_assert(a, [1, 7, 11, 41])
        self.try_set(a, "This is not a string.")

    def test_all_binary_compositions(self):
        """Test AND and OR composition of all pairwise combinations
        of Descriptor instances.

        """
        builtin_descs = [
            "Bool()", "Complex()", "Dict()", "Float()", "Frozenset()", "Int()",
            "List()", "Set()", "Str()", "Tuple()"]
        range_descs = [
            "GreaterThan(7)", "GreaterThanOrEqual(5)", "InRange(-1, 1)",
            "LessThan(9)", "LessThanOrEqual(-4)", "Negative()", "NotZero()",
            "Positive()", "SemiNegative()", "SemiPositive()"]
        misc_descs = [
            "Apply(str.lower)", "Callable()", "EitherOr('g')",
            "ExistingPath()", "ForceNumeric()", "HasAttr('write')",
            "In(set(['a', 'b', 'c']))", "Length(10)", "MadePath()",
            "MaxLength(6)", "MinLength(2)", "NotNone()", "NotRegexMatch('^a')",
            "NotSatisfies(lambda x: x % 2)", "RegexMatch('a*')",
            "Satisfies(lambda x: x % 2)"]

        descs = builtin_descs + range_descs + misc_descs
        for desc1, desc2 in product(descs, descs):
            cls_code = """class A(Validated):
    f = {desc1} & {desc2}
    g = {desc1} | {desc2}
    h = ({desc1} | ({desc1} & {desc2} & {desc2})) & {desc2}

a = A()
""".format(desc1=desc1, desc2=desc2)
            exec(cls_code, globals())
        for attr in ("f g h".split()):
            self.assertTrue(isinstance(a.__class__.__dict__[attr], Descriptor))
            self.assertEqual(a.__class__.__dict__[attr].name, attr)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
