# descriptors.generate_doc
#
# Compile descriptor docstrings into a single document.

from __future__ import print_function, unicode_literals, division

import re

from descriptors import _all_descriptors
from descriptors.massproduced import range_funcs
from descriptors.builtin_types import builtins_camel

title = "Descriptors"
header = title + "\n" + "="*len(title)
abstract = """A collection of descriptors for validating class
attributes. This is a list of all descriptors the package contains."""


def make_link(name):
    return '<a href="#{name}">{name}</a>'.format(name=name)


def add_id(name):
    return '<a id="{name}">{name}</a>'.format(name=name)


def make_rst_link(name):
    return ".. _{name}:\n\n{name}".format(name=name)


def remove_non_code_indent(docstring):
    m = re.match("(.+)Example:(.+)", docstring, flags=re.DOTALL)
    if m:
        doc = m.group(1)
        code = m.group(2)
        doc = re.sub("\n +", "\n", doc)
        return doc + "Example:" + code
    doc = docstring
    doc = re.sub("\n +", "\n", doc)
    return doc


def add_code_mark(docstring):
    return re.sub(
        "(.+)Example:(.+)", r"\1Example:\n\n::\n\n\2",
        docstring, flags=re.DOTALL)


def add_pre_tag(docstring):
    if docstring is None:
        return docstring
    return re.sub(
        "(.+)Example:(.+)", r"\1Example:<pre>\2</pre>",
        docstring, flags=re.DOTALL)

ranges_camel = [name for name, _, _ in range_funcs]
misc_camel = (
    set([name for name, _ in _all_descriptors]) -
    set(ranges_camel) - set(builtins_camel))

category2descs = list(zip(
    ("Builtin types", "Numeric ranges", "Misc"),
    (builtins_camel, ranges_camel, misc_camel)))

toc_rst = "\n\n".join(
    "{cat}\n{line}\n{descs}".format(
        cat=category,
        line="-"*len(category),
        descs=", ".join([n + "_" for n in sorted(desc_names)]))
    for category, desc_names in category2descs)

desc_docs_rst = "\n".join([
    "{name}\n{line}\n\n{docstr}\n\n".format(
        name=make_rst_link(cls_name),
        line="-"*len(cls_name),
        docstr=remove_non_code_indent(add_code_mark(cls.__doc__)))
    for cls_name, cls in sorted(_all_descriptors, key=lambda d: d[0])])

rst = "\n\n".join((header, abstract, toc_rst, desc_docs_rst))

with open("reference.rst", "w") as f:
    f.write(rst)
