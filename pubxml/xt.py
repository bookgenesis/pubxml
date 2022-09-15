import secrets
from collections import OrderedDict
from enum import Enum

from lxml import etree


class TestType(Enum):
    XPATH = "lxml.etree.XPath"
    FUNCTION = "function"

    @classmethod
    def select_for(C, test):
        if type(test) == etree.XPath:
            return C.XPATH
        elif isinstance(test, type(lambda: None)):
            return C.FUNCTION
        else:
            raise ValueError(f"Invalid test type: {type(test)}")


class RegisteredTransformer:
    def __init__(self, function=None, test=None, namespaces=None):
        self.function = function
        self.namespaces = namespaces or {}

        # if test is a string, make it an XPath test method on the given element.
        if isinstance(test, str):
            self.test = etree.XPath(f"self::{test}", namespaces=namespaces)
        elif isinstance(test, (etree.XPath, type(lambda: None))):
            self.test = test

        self.test_type = TestType.select_for(self.test)


class XT:
    """XML Transformations (XT)"""

    def __init__(self, namespaces=None):
        # a registered OrderedDict of transformers to select which transformation method
        # to apply
        self.transformers = OrderedDict()
        self.namespaces = namespaces

    def register(self, name=None, test=None, namespaces=None):
        """
        Decorator to register transformers that

        - match by test function (lambda) or by xpath (like xsl:apply-templates select)
        - can be called by name (like xsl:call-template name) -- just call the function.
        """

        def _registrar(function):
            nonlocal name
            # if a name is not given, assign a unique random one.
            if name is None:
                name = secrets.token_urlsafe(24)

            # register the transformer by name
            self.transformers[name] = RegisteredTransformer(
                function=function,
                test=test,
                namespaces=namespaces or self.namespaces,
            )

            # decorate
            def wrapper(self, *args, **params):
                return function(self, *args, **params)

            return wrapper

        # decorator
        return _registrar

    def transform_all(self, elements, **params):
        """
        Transform all the given elements and yield the results.
        """
        for element in elements:
            result = self.transform(element, **params)
            if result is not None:
                yield result

    def transform(self, element, **params):
        """
        Transform the given element with the first registered transformer that matches.
        Pass the element and params to the transformer and return the results, or None.
        """
        transformer = self.get_transformer(element, **params)
        if transformer is not None:
            return transformer.function(element, **params)

    def get_transformer(self, element, **params):
        """
        For the given element, select the transformer that will be applied.
        """
        for transformer in self.transformers.values():
            if bool(transformer.test(element, **params)) is True:
                return transformer
