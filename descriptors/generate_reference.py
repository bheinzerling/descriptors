# descriptors.generate_reference
#
# Compile descriptor docstrings into a single document.

from __future__ import print_function, unicode_literals, division

import re

from descriptors import _all_descriptors
from descriptors.massproduced import range_funcs
from descriptors.builtin_types import builtins_camel

title = "Descriptors"
header = title + "\n" + "="*len(title)
abstract = """This is a list of all descriptors the package contains."""


def make_rst_target(name):
    return ".. _{name}:\n\n{name}".format(name=name)


def remove_non_code_indent(doc):
    m = re.match("(.+)Example:(.+)", doc, flags=re.DOTALL)
    code = ""
    if m:
        doc = m.group(1)
        code = "Example:" + m.group(2)
    doc = re.sub("\n +", "\n", doc)
    return doc + code


def add_code_mark(doc):
    return re.sub(
        "(.+)Example:(.+)", r"\1Example:\n\n::\n\n\2", doc, flags=re.DOTALL)


ranges_camel = [name for name, _, _ in range_funcs]
all_camel = set(name for name, _ in _all_descriptors)
misc_camel = all_camel - set(ranges_camel) - set(builtins_camel)

category2descs = list(zip(
    ("Builtin types", "Numeric ranges", "Misc."),
    (builtins_camel, ranges_camel, misc_camel)))

toc = "\n\n".join(
    "{cat}\n{line}\n{descs}".format(
        cat=category,
        line="-"*len(category),
        descs=", ".join([n + "_" for n in sorted(desc_names)]))
    for category, desc_names in category2descs)

desc_docs = "\n".join([
    "{name}\n{line}\n\n{docstr}\n\n".format(
        name=make_rst_target(cls_name),
        line="-"*len(cls_name),
        docstr=remove_non_code_indent(add_code_mark(cls.__doc__)))
    for cls_name, cls in sorted(_all_descriptors, key=lambda d: d[0])])

rst = "\n\n".join((header, abstract, toc, desc_docs))

with open("../reference.rst", "w") as f:
    f.write(rst)
