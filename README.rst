decriptors - a package for easy input validation
=================================================

**tl;dr:** A collection of descriptors for easily validating attributes like so:

::

    from descriptors import Validated, ExistingPath, MadePath

    class BatchProcessor(Validated):
        input_dir = ExistingPath()
        output_dir = MadePath()

        def process(self, input_dir, output_dir):
            self.input_dir = input_dir  # error if input_dir doesn't exist
            self.output_dir = output_dir  # output_dir automatically created


Contents
--------

`Usage Examples`_

`Reference`_

`Why use descriptors?`_

`Caveats`_

`Installation`_

`Credit`_

.. _`Usage Examples`:

Usage examples
**************

Validation of builtin types:

::

    from descriptors import Validated, Str, Dict, Int

    class A(Validated):
        some_str = Str()
        some_dict = Dict()
        some_int = Int()

    a = A()
    a.some_str = "test"  # ok
    a.some_str = 7  # ValueError
    a.some_dict = {"two": "dos"}  #ok
    a.some_int = "test"  # ValueError

Validation of numeric ranges:

::

    from descriptors import Validated, GreaterThan, InRange, NotZero

    class A(Validated):
        many = GreaterThan(2)
        num_players = InRange(1, 4)
        divisor = NotZero()

    a = A()
    a.many = 2  # ValueError
    a.num_players = 3  # ok
    a.divisor = 0  # ValueError

Some more examples:

::

    import os
    from descriptors import (
        Validated, ExistingPath, Apply, Length, NotNone, RegexMatch, Satisfies)

    class A(Validated):
        abs_path = ExistingPath() & Apply(os.path.abspath)
        triple = Length(3)
        something = NotNone()
        only_a = RegexMatch("^a+$")
        lower_str = Apply(str.lower)
        even = Satisfies(lambda x: x % 2 == 0)

    a = A()
    os.chdir("/home/username")
    a.abs_path = ".."  # a.abs_path = "/home"
    a.triple = [1, 2, 3]  # ok
    a.something = None  # ValueError
    a.only_a = "aaaab"  # ValueError
    a.lower_str = "sOmE StrIng"  # a.lower == "some string"
    a.even = 1  # ValueError

Descriptors can be composed using the bitwise AND and OR operators (i.e. & and \|):

::

    from descriptors import (
        Validated, Int, Satisfies, HasAttr, GreaterThan, LessThan)

    class A(Validated):
        an_even_int = Int() & Satisfies(lambda x: x % 2 == 0)
        a_finite_set = HasAttr("__contains__") & HasAttr("__len__")
        no_single_digits = Int() & (GreaterThan(9) | LessThan(-9))

    a = A()
    a.an_even_int = 2.0  # ValueError
    a.a_finite_set = [1, 2, 3]  # ok
    a.no_single_digits = 7  # ValueError

Inheriting from Validated means that class attributes with an assigned Descriptor
will be validated, but nothing else. Other class attributes behave as usual, and assigning a Descriptor
to an instance variable will not have the desired effect:

::

    from descriptors import Validated, HasAttr

    class A(Validated):
        f = HasAttr("read")  # assigning to class attribute
        g = 0  # normal class attribute, not validated

        def __init__(self):
            self.h = HasAttr("read")  # h not validated, you can assign anything

    a = A()
    a.f = 7  # ValueError
    a.h = 7  # assigns 7, no ValueError

.. _`Reference`:

Reference
*********

A complete list of all descriptors provided can be found `here <reference.rst>`_.

.. _`Why use descriptors?`:

Why use descriptors?
********************

If you have ever written a program that takes user input, you have probably written code to make sure that user input is what your program expects it to be. For example, say you're writing a tool to batch-process files in an input directory and save them to an output directory. You'll want to verify that input_dir exists and show the user a non-cryptic error message if it doesn't. You'll also want to make sure output_dir exists or can be created, so the program doesn't process files for possibly hours just to fail saving the results because output_dir contains an invalid character:


::

    class BatchProcessor(object):
        def process(self, input_dir, output_dir):
            if os.path.exists(input_dir)
                self.input_dir = input_dir
            else:
                self.some_error_msg()
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(outputdir)
                    self.output_dir = output_dir
                except OSError:
                    self.another_error_msg()

This is tedious to write and maintain, and doesn't prevent setting invalid values somewhere else in the program. A better approach is using properties:

::

    class BatchProcessor(object):
        @property
        def input_dir(self):
            return self._input_dir
        
        @input_dir.setter:
        def input_dir(self, val):
            if os.path.exists(val)
                self._input_dir = val
            else:
                self.some_error_msg()
        
        # output_dir property left as an exercise for the reader

Properties make your intentions much clearer and prevent setting invalid values, but now there are getters and setters all over the place. Also, reusing properties from one class in another isn't exactly convenient. A much better solution is using `descriptors <http://docs.python.org/2/howto/descriptor.html>`_. A descriptor is an object that hooks into attribute access by implementing any of the following methods: `__get__`, `__set__`, `__delete__`. By assigning a descriptor to a class attribute, that descriptor's `__get__`, `__set__`, or `__delete__` method will be invoked when the attribute is retrieved, set, or deleted. With descriptors, our example program looks like this:

::

    from descriptors import Validated, ExistingPath, MadePath

    class BatchProcessor(Validated):
        input_dir = ExistingPath()
        output_dir = MadePath()

        def process(self, input_dir, output_dir):
            self.input_dir = input_dir
            self.output_dir = output_dir

As the name suggests, `ExistingPath` only allows existing paths to be set; it will raise an exception otherwise. `MadePath` will create the path, if necessary, and raise an exception if the path cannot be created. By inheriting from `Validated`, class attributes will automatically be bound to their descriptor.

(The last sentence is completely false, but the actual reason for inheriting from Validated is a bit more complicated.)


.. _`Caveats`:

Handle with care
****************

The purpose of this package is to conveniently validate input data. This convenience comes at the price of performance. While the performance hit is completely negligible for most reasonable use cases (e.g., setting a couple of parameters before running the main part of your program), using descriptors in a long-running, CPU-intensive loop, or some other heavy-duty part of your program will likely cause a significant drop in performance.

Descriptors are not a static type system. Do a couple of sanity checks so users don't have to deal with error messages from deep down your program, where the actual failure would occur otherwise. It's probably not a good idea to go overboard by using descriptors on every single attribute or being overly restrictive with what values you allow.


.. _`Installation`:

Installation
************

This package has been tested on Python 2.7 and Python 3.3.

Installation using pip (depending on your system you might have to run this as root):

::

    pip install descriptors

Uninstall:

::

    pip uninstall descriptors

Installation without pip:
^^^^^^^^^^^^^^^^^^^^^^^^^

Download the latest zip archive of this package from pypi:

`pypi.python.org/pypi/descriptors/ <pypi.python.org/pypi/descriptors/>`_

Extract the archive, navigate to the extracted folder and run:

::

    python setup.py install

Other validation options
************************

If descriptors is not what you're looking for, check out these projects:

- `jsonschema <https://github.com/Julian/jsonschema>`_
- `Schema <https://github.com/halst/schema>`_
- `voluptuous <https://pypi.python.org/pypi/voluptuous/>`_
- `wheezy.validation <http://pythonhosted.org/wheezy.validation/>`_

.. _`Credit`:

Credit
******

This package is inspired by (read: shamelessly stolen from) `David Beazley <http://www.dabeaz.com/>`_'s excellent tutorial on Python 3 metaprogramming (`video <https://www.youtube.com/watch?v=sPiWg5jSoZI>`_, `slides and code <http://www.dabeaz.com/py3meta/>`_).
