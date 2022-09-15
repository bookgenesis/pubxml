import logging
import types
from dataclasses import dataclass, field

import lxml.builder

LOG = logging.getLogger(__name__)


@dataclass
class Builder:
    """
    A Builder is a set of ElementMakers all bound to the same object.
    """

    namespaces: dict = field(default_factory=dict)
    makers: dict = field(default_factory=dict, init=False)
    default: str = None  # default namespace

    def __getattr__(self, key):
        return self.makers[key]

    def __post_init__(self):
        nsmap = {**self.namespaces}
        if self.default is not None:
            prefix = next((k for k, v in nsmap.items() if v == self.default), None)
            nsmap[None] = nsmap.pop(prefix)

        # map all the other prefixes to ElementMakers
        for prefix, uri in self.namespaces.items():
            self.makers[prefix] = ElementMaker(namespace=uri, nsmap=nsmap)

        # If there is no default ElementMaker, create one with no namespaces
        if None not in self.makers:
            self.makers[None] = ElementMaker()

    def __call__(self, name, *args, **kwargs):
        return self.makers[None](name, *args, **kwargs)

    @classmethod
    def one(cls, namespace=None):
        """
        Create an ElementMaker with an optional single namespace that uses that
        namespace as the default.
        """
        if namespace is None:
            B = cls().makers[None]
        else:
            B = cls({None: namespace}, default=namespace)

        return B.makers[None]


class ElementMaker(lxml.builder.ElementMaker):
    """
    An lxml ElementMaker with enhancements. As with lxml ElementMaker, "nodes" can be
    strings, dicts, or Elements.

    The following enhancements:

    - Nodes can also be lists / tuples / generators, in which case they are unpacked
      (flattened) into the element. (This is primarily useful for allowing XT
      transformer methods that take a single element to return a list.)
    - `tail` keyword can be defined in the element definition (saves a lot of trouble).
    - Attributes must be given as a mapping (dict, etc.) in children (= args), not as
      **kwargs - provide just one right way to add attributes to elements.
    """

    def __call__(self, tag, *nodes, tail=None):
        def gen_nodes(nodes):
            for node in nodes:
                if isinstance(node, (types.GeneratorType, list, tuple)):
                    for elem in gen_nodes(node):
                        yield elem
                elif node is not None:
                    yield node

        element = lxml.builder.ElementMaker.__call__(self, tag, *gen_nodes(nodes))
        element.tail = tail

        return element
