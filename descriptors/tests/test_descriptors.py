from __future__ import print_function, unicode_literals, division

import unittest
import os
import string
from itertools import product
from tempfile import mkdtemp

from descriptors import Validated, _all_descriptors
from descriptors.builtin_types import builtins, builtins_camel
globals().update(_all_descriptors)


def make_obj(val=None, clsdict=None):
    """Create a dummy object for testing descriptors."""
    clsdict = {"f": val} if clsdict is None else clsdict
    return type(str("A"), (Validated, ), clsdict)()


def desc_cls(obj, attr="f"):
    """Return the class of the Descriptor associated with obj.attr."""
    return obj.__class__.__dict__[attr].__class__


class DescriptorsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # sets for keeping track if all descriptors have been tested
        desc_classes = [c for _, c in _all_descriptors]
        cls.valid_to_do = set(desc_classes)
        cls.invalid_to_do = set(desc_classes)

    def set_assert(self, obj, val, attr="f"):
        """Assert a valid assignment works and do bookkeeping."""
        setattr(obj, attr, val)
        self.assertEqual(getattr(obj, attr), val)
        self.valid_to_do.discard(desc_cls(obj, attr))

    def try_set(self, obj, value, attr="f"):
        """Assert an invalid assignment fails and do bookkeeping."""
        with self.assertRaises(ValueError):
            setattr(obj, attr, value)
        self.invalid_to_do.discard(desc_cls(obj, attr))

    def test_ranges(self):
        """Test valid and invalid assignments for range descriptors."""
        descs = (
            Positive(), SemiPositive(), Negative(), SemiNegative(),
            NotZero(), GreaterThan(7), GreaterThanOrEqual(-12),
            LessThan(-111), LessThanOrEqual(1), InRange(-1000, 2000))
        fields = [d.__class__.__name__.lower() for d in descs]
        clsdict = dict(zip(fields, descs))
        a = make_obj(clsdict=clsdict)
        valids = (7, 0, -17, -0.0, 0.1, 8, -12, -111.0001, 0, 1400)
        invalids = (-7, -0.1, 17, 0.1, 0, 6.7, -100, 111, 1.1, -2222)
        for field, valid, invalid in zip(fields, valids, invalids):
            self.set_assert(a, valid, field)
            self.try_set(a, invalid, field)

    def test_builtin_types(self):
        """Test all valid and invalid assignment combinations for the
        builtin types descriptors.

        """
        z = list(zip(builtins, builtins_camel))
        for (field_cls, field_type), (val_cls, _) in product(z, z):
            desc_cls = globals()[field_type] 
            a = make_obj(desc_cls())
            try:
                val = val_cls(7)
            except TypeError:
                if isinstance(val_cls(), dict):
                    val = {"k": 2}
                else:
                    val = val_cls([7])
            # "or" to account for bool values being instances of int
            if val_cls == field_cls or isinstance(val_cls(), field_cls):
                self.set_assert(a, val_cls())
                self.set_assert(a, val)
            else:
                self.try_set(a, val_cls())
                self.try_set(a, val)

    def test_misc_and_some_handmade_types(self):
        misc_tests = [
            (NotNone(), object(), None),
            (Callable(), lambda x: x < x, "not_callable"),
            (HasAttr("__contains__"), set([1, 2, 3]), True),
            (Satisfies(lambda x: x % 2 == 0), 1234, 12345),
            (NotSatisfies(lambda x: x % 2 == 0), 12345, 1234),
            (Length(4), set(range(4)), [1, 2]),
            (Length(0), [], "asdf"),
            (MinLength(3), "asd", "ab"),
            (MaxLength(2), "as", (1, 2, 3)),
            (ExistingPath(), os.path.expanduser("~"), "abae454gas3")]
        some_handmade_tests = [
            (In(set(["a", "b", "c"])), "b", "d"),
            (In("xyz"), "z", True),
            (In(dict(zip([1, 2, 3], "abc"))), 1, "a"),
            (In(string.ascii_uppercase), "R", "|"),
            (RegexMatch("aa+"), "baaaab", "abc"),
            (RegexMatch("[0|1]+1$"), "01010101", "10101000"),
            (NotRegexMatch("^a(xyz+)b$"), "axyzzz", "axyzzb"),
            (NotRegexMatch("^a"), "ba", "ab")]
        for desc, valid_val, invalid_val in misc_tests + some_handmade_tests:
            a = make_obj(desc)
            self.set_assert(a, valid_val)
            self.try_set(a, invalid_val)

    def test_in_no_membership(self):
        for val in (7, True, None, complex(8, 2)):
            with self.assertRaises(TypeError):
                make_obj(In(val))

    def test_apply(self):
        a = make_obj(Apply(str.lower))
        a.f = s = str("SomE StRinG")
        self.assertEqual(a.f, str(s).lower())
        a = make_obj(Apply(str.strip))
        a.f = s = str("\n\tabc\r")
        self.assertEqual(a.f, str(s).strip())
        a = make_obj(Apply(set))
        a.f = l = [True, False, 1, 2, (7, 8)]
        self.assertEqual(a.f, set(l))
        with self.assertRaises(TypeError):
            make_obj(Apply(print()))
        self.valid_to_do.discard(desc_cls(a))
        self.invalid_to_do.discard(desc_cls(a))

    def test_apply_composition(self):
        a = make_obj(Str() & Apply(str.lower))
        a.f = s = str("SomE StRing")
        self.assertEqual(a.f, str(s).lower())
        a = make_obj(Apply(str.lower) & Str())
        a.f = s = str("OtheR StRing")
        self.assertEqual(a.f, str(s).lower())
        a = make_obj(Str() | Apply(str.lower))
        a.f = s = str("SomE StRing")
        self.assertEqual(a.f, str(s))
        a = make_obj(Apply(str.upper) | Apply(str.lower))
        a.f = s = str("SomE StRing")
        self.assertEqual(a.f, str(s).upper())

    def test_made_path(self):
        a = make_obj(MadePath())
        t = mkdtemp()
        d = os.path.join(t, "mnbv")
        a.f = d
        self.assertTrue(os.path.exists(d))
        self.valid_to_do.discard(desc_cls(a))
        with self.assertRaises(TypeError):
            a.f = ["asdf"]
        with self.assertRaises(OSError):
            a.f = ""
        self.invalid_to_do.discard(desc_cls(a))

    def test_force_numeric(self):
        a = make_obj(ForceNumeric())
        a.f = 7
        self.assertTrue(isinstance(a.f, int) and a.f == 7)
        a.f = -7.0
        self.assertTrue(isinstance(a.f, float) and a.f == -7.0)
        a.f = "-13.123"
        self.assertTrue(isinstance(a.f, float) and a.f == -13.123)
        self.valid_to_do.discard(desc_cls(a))
        self.try_set(a, (0, 0))
        self.try_set(a, "seven")
        self.try_set(a, None)

    def test_force_numeric_composition(self):
        a = make_obj(ForceNumeric() & LessThan(8))
        a.f = "7"
        self.assertTrue(isinstance(a.f, int) and a.f == 7)
        with self.assertRaises(Exception):
            a = make_obj(LessThan(8) & ForceNumeric())
            a.f = "7"
        a = make_obj(ForceNumeric() | LessThan(3))
        a.f = "7"
        self.assertTrue(isinstance(a.f, int) and a.f == 7)

    def test_either_or(self):
        clsdict = {"f": EitherOr("g"), "g": EitherOr("f")}
        a = make_obj(clsdict=clsdict)
        a.f = a.g = None
        self.assertTrue(a.f is None and a.g is None)
        a.g = True
        self.assertTrue(a.g and not a.f)
        self.try_set(a, True, attr="f")
        a.f = a.g = None
        a.f = "s"
        self.assertTrue(a.f == "s" and a.g is None)
        self.try_set(a, 9, attr="g")
        self.valid_to_do.discard(desc_cls(a))
        self.invalid_to_do.discard(desc_cls(a))

    def test_delete(self):
        a = make_obj(Str())
        a.f = str("test")
        self.assertTrue(hasattr(a, "f"))
        del(a.f)
        self.assertFalse(hasattr(a, "f"))

    def test_repr(self):
        a = make_obj(MadePath())
        self.assertTrue(
            repr(a.__class__.__dict__["f"]).startswith(
                "<Descriptor: MadePath at"))


    @classmethod
    def tearDownClass(cls):
        assert len(cls.valid_to_do) == 0, cls.valid_to_do
        assert len(cls.invalid_to_do) == 0, cls.invalid_to_do


def main():
    unittest.main()

if __name__ == "__main__":
    main()
