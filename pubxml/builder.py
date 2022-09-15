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
    __makers: dict = field(default_factory=dict, init=False)
    default: str = None  # default namespace

    def __getattr__(self, key):
        return self.__makers[key]

    def __post_init__(self):
        if self.default is not None:
            # remember the default prefix
            default_prefix = next(
                (k for k, v in self.namespaces.items() if v == self.default), None
            )
            # rewrite namespaces so that the default has prefix of None (this is how
            # ElementMaker wants it.)
            self.namespaces = {
                None: self.default,
                **{k: v for k, v in self.namespaces.items() if v != self.default},
            }
        # map any default prefix to the default namespace's ElementMaker
        if default_prefix is not None:
            self.__makers[default_prefix] = ElementMaker(
                namespace=self.default, nsmap=self.namespaces
            )
        # map all the other prefixes to ElementMakers
        for prefix, uri in self.namespaces.items():
            self.__makers[prefix] = ElementMaker(namespace=uri, nsmap=self.namespaces)

    def __call__(self, name, *args, **kwargs):
        return self.__makers[None](name, *args, **kwargs)

    @classmethod
    def one(cls, namespace=None):
        """
        Create an ElementMaker with an optional single namespace that uses that
        namespace as the default.
        """
        if namespace is None:
            return cls()
        else:
            return cls({None: namespace}, default=namespace)


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
