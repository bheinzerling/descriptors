Descriptors
===========

This is a list of all descriptors the package contains.

Builtin types
-------------
Bool_, Complex_, Dict_, Float_, Frozenset_, Int_, List_, Set_, Str_, Tuple_

Numeric ranges
--------------
GreaterThan_, GreaterThanOrEqual_, InRange_, LessThan_, LessThanOrEqual_, Negative_, NotZero_, Positive_, SemiNegative_, SemiPositive_

Misc.
-----
Apply_, Callable_, EitherOr_, ExistingPath_, ForceNumeric_, HasAttr_, In_, Length_, MadePath_, MaxLength_, MinLength_, NotNone_, NotRegexMatch_, NotSatisfies_, RegexMatch_, Satisfies_

.. _Apply:

Apply
-----

A descriptor that sets the described attribute to the result
obtained from applying the supplied function to the value being
set.

Example:

.. code:: python


        class A(Validated):
            f = Apply(str.lower)

        a = A()
        a.f = "SoMe stRInG"
        print(a.f)
        -> some string

    


.. _Bool:

Bool
----

A descriptor that ensures the value being set is an instance of bool.


.. _Callable:

Callable
--------

A descriptor that only allows setting the described
attribute to a callable object.

Example:

.. code:: python


        class A(Validated):
            process_func = Callable()

        a = A()
        a.process_func = str.lower
        -> ok
        a.process_func = "rm -rf /"
        -> ValueError


.. _Complex:

Complex
-------

A descriptor that ensures the value being set is an instance of complex.


.. _Dict:

Dict
----

A descriptor that ensures the value being set is an instance of dict.


.. _EitherOr:

EitherOr
--------

A descriptor asserting that either the described attribute OR
other_attr are True-y, but not both or neither. The descriptor
is only active if both attributes are not None to allow
re-setting values.
If other_attr does not exist, it is assumed to be None.

Example:

.. code:: python


        class A(Validated):
            f1 = EitherOr("f2")
            f2 = EitherOr("f1")

        a = A()
        a.f1 = True
        a.f2 = True
        -> ValueError

    


.. _ExistingPath:

ExistingPath
------------

A descriptor that only allows strings that
represent an existing path.

Example:

.. code:: python


        class A(Validated):
            input_dir = ExistingPath()

        a = A()
        a.input_dir = "/tmp"
        -> ok
        a.input_dir = None
        -> ValueError


.. _Float:

Float
-----

A descriptor that ensures the value being set is an instance of float.


.. _ForceNumeric:

ForceNumeric
------------

A descriptor that only allows numeric values, with "numeric"
meaning that the value is
a) an instance of a subclass of numbers.Number, or
b) a string that can be converted to a float or int.
In case a) the value will be passed through as is, in case b)
the string will be converted to an int or a float, depending
on the numeric value represented by the string.

Example:

.. code:: python


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

    


.. _Frozenset:

Frozenset
---------

A descriptor that ensures the value being set is an instance of frozenset.


.. _GreaterThan:

GreaterThan
-----------

A descriptor that only allows values greater than
the specified value.

Example:

.. code:: python


        class A(Validated):
            f = GreaterThan(3)

        a = A()
        a.f = 7
        -> ok
        a.f = 2
        -> ValueError


.. _GreaterThanOrEqual:

GreaterThanOrEqual
------------------

A descriptor that only allows values
greater than or equal to the specified value.

Example:

.. code:: python


        class A(Validated):
            f = GreaterThanOrEqual(3)

        a = A()
        a.f = 3
        -> ok
        a.f = 2
        -> ValueError


.. _HasAttr:

HasAttr
-------

A descriptor ensuring that the described attribute
is set to an object that has the specified attribute.

Example:

.. code:: python


        class A(Validated):
            f = HasAttr("read")

        a = A()
        a.f = open("/tmp/some_file.txt")
        -> ok
        a.f = "/tmp/some_file.txt"
        -> ValueError


.. _In:

In
--

A descriptor that only allows assigning a value if that value is
a member of a set of given elements.

Example:

.. code:: python


        class A(Validated):
            mood = In(set(["bad", "go away", "Why me!?", ":-("]))

        a = A()
        a.mood = "awesome"
        -> ValueError

    


.. _InRange:

InRange
-------

A descriptor that only allows values within the
specified range.

Example:

.. code:: python


        class A(Validated):
            f = InRange(3, 8)

        a = A()
        a.f = 6
        -> ok
        a.f = 0
        -> ValueError


.. _Int:

Int
---

A descriptor that ensures the value being set is an instance of int.


.. _Length:

Length
------

A descriptor that only allows values that have the
specified length.

Example:

.. code:: python


        class A(Validated):
            coords = Length(3)

        a = A()
        a.coords = (1, 2, 3)
        -> ok
        a.coords = (1, 2)
        -> ValueError


.. _LessThan:

LessThan
--------

A descriptor that only allows values smaller than
the specified value.

Example:

.. code:: python


        class A(Validated):
            f = LessThan(3)

        a = A()
        a.f = 2
        -> ok
        a.f = 7
        -> ValueError


.. _LessThanOrEqual:

LessThanOrEqual
---------------

A descriptor that only allows values
smaller than or equal to the specified value.

Example:

.. code:: python


        class A(Validated):
            f = LessThanOrEqual(3)

        a = A()
        a.f = 3
        -> ok
        a.f = 6
        -> ValueError


.. _List:

List
----

A descriptor that ensures the value being set is an instance of list.


.. _MadePath:

MadePath
--------

A descriptor that creates the path represented by the passed
string if that path doesn't exist already.




.. _MaxLength:

MaxLength
---------

A descriptor that only allows values that have at
most the specified length.

Example:

.. code:: python


        class A(Validated):
            players = MaxLength(2)

        a = A()
        a.players = ("Ann", "Bob")
        -> ok
        a.players = ("Ann", "Bob", "Charlie")
        -> ValueError


.. _MinLength:

MinLength
---------

A descriptor that only allows values that have at
least the specified length.

Example:

.. code:: python


        class A(Validated):
            elements = MinLength(2)

        a = A()
        a.elements = (1, 2, 3)
        -> ok
        a.elements = (1, )
        -> ValueError


.. _Negative:

Negative
--------

A descriptor that only allows setting strictly
negative values, i.e. values < 0.


.. _NotNone:

NotNone
-------

A descriptor that only allows values that are not
None.


.. _NotRegexMatch:

NotRegexMatch
-------------

A descriptor that ensures the described attribute is only set
to a string that does not match the supplied regular expression.




.. _NotSatisfies:

NotSatisfies
------------

A descriptor that only allows values that do not
satisfy the specified function, i.e. applying the function to the
values gives a False-y result.

Example:

.. code:: python


        class A(Validated):
            odd_number = NotSatisfies(lambda x: x % 2 == 0)

        a = A()
        a.odd_number = 5
        -> ok
        a.odd_number = 4
        -> ValueError


.. _NotZero:

NotZero
-------

A descriptor that only allows non-zero values.


.. _Positive:

Positive
--------

A descriptor that only allows setting strictly
positive values, i.e. values > 0.


.. _RegexMatch:

RegexMatch
----------

A descriptor that ensures the described attribute is only set
to a string that matches the supplied regular expression.




.. _Satisfies:

Satisfies
---------

A descriptor that only allows values that satisfy
the specified function, i.e. applying the function to the value
gives a True-y result.

Example:

.. code:: python


        class A(Validated):
            even_number = Satisfies(lambda x: x % 2 == 0)

        a = A()
        a.even_number = 2
        -> ok
        a.even_number = 7
        -> ValueError


.. _SemiNegative:

SemiNegative
------------

A descriptor that only allows setting
semi-negative values, i.e. values <= 0.


.. _SemiPositive:

SemiPositive
------------

A descriptor that only allows setting
semi-positve values, i.e. values >= 0.


.. _Set:

Set
---

A descriptor that ensures the value being set is an instance of set.


.. _Str:

Str
---

A descriptor that ensures the value being set is an instance of str.


.. _Tuple:

Tuple
-----

A descriptor that ensures the value being set is an instance of tuple.

