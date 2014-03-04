# descriptors.docstrings
#
# Docstrings for the automatically generated Descriptor classes.

from __future__ import print_function, unicode_literals, division

from descriptors.builtin_types import builtins_camel

docstrings = {
    "Positive": """A descriptor that only allows setting strictly
    positive values, i.e. values > 0.""",
    "SemiPositive": """A descriptor that only allows setting
    semi-positve values, i.e. values >= 0.""",
    "Negative": """A descriptor that only allows setting strictly
    negative values, i.e. values < 0.""",
    "SemiNegative": """A descriptor that only allows setting
    semi-negative values, i.e. values <= 0.""",
    "NotZero": """A descriptor that only allows non-zero values.""",
    "GreaterThan": """A descriptor that only allows values greater than
    the specified value.

    Example:
        class A(Validated):
            f = GreaterThan(3)

        a = A()
        a.f = 7
        -> ok
        a.f = 2
        -> ValueError""",
    "GreaterThanOrEqual": """A descriptor that only allows values
    greater than or equal to the specified value.

    Example:
        class A(Validated):
            f = GreaterThanOrEqual(3)

        a = A()
        a.f = 3
        -> ok
        a.f = 2
        -> ValueError""",
    "LessThan": """A descriptor that only allows values smaller than
    the specified value.

    Example:
        class A(Validated):
            f = LessThan(3)

        a = A()
        a.f = 2
        -> ok
        a.f = 7
        -> ValueError""",
    "LessThanOrEqual": """A descriptor that only allows values
    smaller than or equal to the specified value.

    Example:
        class A(Validated):
            f = LessThanOrEqual(3)

        a = A()
        a.f = 3
        -> ok
        a.f = 6
        -> ValueError""",
    "InRange": """A descriptor that only allows values within the
    specified range.

    Example:
        class A(Validated):
            f = InRange(3, 8)

        a = A()
        a.f = 6
        -> ok
        a.f = 0
        -> ValueError""",
    "NotNone": """A descriptor that only allows values that are not
    None.""",
    "Callable": """A descriptor that only allows setting the described
    attribute to a callable object.

    Example:
        class A(Validated):
            process_func = Callable()

        a = A()
        a.process_func = str.lower
        -> ok
        a.process_func = "rm -rf /"
        -> ValueError""",
    "HasAttr": """A descriptor ensuring that the described attribute
    is set to an object that has the specified attribute.

    Example:
        class A(Validated):
            f = HasAttr("read")

        a = A()
        a.f = open("/tmp/some_file.txt")
        -> ok
        a.f = "/tmp/some_file.txt"
        -> ValueError""",
    "Satisfies": """A descriptor that only allows values that satisfy
    the specified function, i.e. applying the function to the value
    gives a True-y result.

    Example:
        class A(Validated):
            even_number = Satisfies(lambda x: x % 2 == 0)

        a = A()
        a.even_number = 2
        -> ok
        a.even_number = 7
        -> ValueError""",
    "NotSatisfies": """A descriptor that only allows values that do not
    satisfy the specified function, i.e. applying the function to the
    values gives a False-y result.

    Example:
        class A(Validated):
            odd_number = NotSatisfies(lambda x: x % 2 == 0)

        a = A()
        a.odd_number = 5
        -> ok
        a.odd_number = 4
        -> ValueError""",
    "Length": """A descriptor that only allows values that have the
    specified length.

    Example:
        class A(Validated):
            coords = Length(3)

        a = A()
        a.coords = (1, 2, 3)
        -> ok
        a.coords = (1, 2)
        -> ValueError""",

    "MinLength": """A descriptor that only allows values that have at
    least the specified length.

    Example:
        class A(Validated):
            elements = MinLength(2)

        a = A()
        a.elements = (1, 2, 3)
        -> ok
        a.elements = (1, )
        -> ValueError""",
    "MaxLength": """A descriptor that only allows values that have at
    most the specified length.

    Example:
        class A(Validated):
            players = MaxLength(2)

        a = A()
        a.players = ("Ann", "Bob")
        -> ok
        a.players = ("Ann", "Bob", "Charlie")
        -> ValueError""",
    "ExistingPath": """A descriptor that only allows strings that
    represent an existing path.

    Example:
        class A(Validated):
            input_dir = ExistingPath()

        a = A()
        a.input_dir = "/tmp"
        -> ok
        a.input_dir = None
        -> ValueError"""
    }

for b_str in builtins_camel:
    docstrings[b_str] = (
        "A descriptor that ensures the value being set is an "
        "instance of {}.".format(b_str.lower()))
