"""
An XML Document.
"""
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from lxml import etree


@dataclass
class XML:
    tree: etree._ElementTree
    filepath: Path = None

    @property
    def root(self):
        return self.tree.getroot()

    @property
    def info(self):
        return self.tree.docinfo

    # Queries

    @classmethod
    def xpath(cls, node, path, namespaces=None, extensions=None, **params):
        return node.xpath(
            path,
            namespaces=namespaces or node.nsmap,
            extensions=extensions,
            **params,
        )

    @classmethod
    def find(cls, node, path, namespaces=None, extensions=None, **params):
        results = cls.xpath(
            node,
            path,
            namespaces=namespaces,
            extensions=extensions,
            **params,
        )
        return next(iter(results), None)

    # Input

    @classmethod
    def load(cls, filepath: Path):
        return cls(
            filepath=filepath,
            tree=etree.parse(
                filepath,
                base_url=f"file://{filepath}",
            ),
        )

    @classmethod
    def frombytes(cls, xml: bytes, filepath: Path = None):
        return cls(
            filepath=filepath,
            tree=etree.parse(
                BytesIO(xml),
                base_url=f"file://{filepath}" if filepath else None,
            ),
        )

    @classmethod
    def fromstring(cls, xml: str, filepath: Path = None):
        return cls.frombytes(xml.encode("UTF-8"), filepath=filepath)

    # Output

    def __str__(self):
        return etree.tounicode(self.tree.getroot())

    def text(self):
        return etree.tounicode(self.tree.getroot(), method='text')

    def canonicalize(self) -> bytes:
        bytestream = BytesIO()
        self.tree.write_c14n(bytestream)
        return bytestream.getvalue()

    def write(self, output_path=None):
        if output_path is None:
            output_path = self.filepath

        with open(output_path, "wb") as f:
            f.write(b"<?xml version='1.0' encoding='UTF-8'?>\n" + self.canonicalize())
