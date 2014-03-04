# descriptors.__init__
#
# Expose Descriptor, Validated, and all descriptors so they can be
# imported via "from descriptors import ..."

from __future__ import print_function, unicode_literals, division

from descriptors.Descriptor import Descriptor
from descriptors.Validated import Validated
import descriptors.handmade as hm
import descriptors.massproduced as mm

_all_descriptors = set([
    (obj_name, obj)
    for module in (hm, mm)
    for obj_name, obj in module.__dict__.items()
    if obj.__class__.__name__ == "DescriptorMeta"])

_all_descriptors.discard(("Descriptor", Descriptor))

globals().update(_all_descriptors)
