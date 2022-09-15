"""
An XML Document.
"""
from dataclasses import dataclass, field
from io import BytesIO, IOBase
from pathlib import Path

from lxml import etree


@dataclass
class XML:
    tree: etree._ElementTree
    filepath: Path = None
    namespaces: dict = field(default_factory=dict)

    def __post_init__(self):
        # if isinstance(self.tree, etree._Element):
        #     self.tree = etree.ElementTree(self.tree)
        if not self.namespaces:
            self.namespaces = {**self.root.nsmap}

    @property
    def root(self):
        return self.tree.getroot()

    @property
    def info(self):
        return self.tree.docinfo

    # Queries

    def xpath(self, node, path, namespaces=None, extensions=None, **params):
        return node.xpath(
            path,
            namespaces={
                k: v
                for k, v in (namespaces or self.namespaces or node.nsmap).items()
                if k is not None
            },
            extensions=extensions,
            **params,
        )

    def find(self, node, path, namespaces=None, extensions=None, **params):
        results = self.xpath(
            node,
            path,
            namespaces=namespaces,
            extensions=extensions,
            **params,
        )
        return next(iter(results), None)

    # Input

    @classmethod
    def load(cls, filepath: Path, namespaces=None):
        return cls(
            filepath=filepath,
            tree=etree.parse(
                filepath,
                base_url=f"file://{filepath}",
            ),
            namespaces=namespaces,
        )

    @classmethod
    def frombytes(cls, xml: bytes, filepath: Path = None, namespaces=None):
        return cls(
            filepath=filepath,
            tree=etree.parse(
                BytesIO(xml),
                base_url=f"file://{filepath}" if filepath else None,
            ),
            namespaces=namespaces,
        )

    @classmethod
    def fromstring(cls, xml: str, filepath: Path = None, namespaces=None):
        return cls.frombytes(
            xml.encode("UTF-8"), filepath=filepath, namespaces=namespaces
        )

    # Output

    def __str__(self):
        return etree.tounicode(self.tree.getroot())

    def text(self):
        return etree.tounicode(self.tree.getroot(), method="text")

    def canonicalize(self) -> bytes:
        bytestream = BytesIO()
        self.tree.write_c14n(bytestream)
        return bytestream.getvalue()

    def write(self, file=None):
        """
        Write the XML to the given file (defaults to the XML.filepath) as
        canonicalized bytes. (Canonicalization ensures that the output for the same XML
        is always the same -- for example, attributes will always occur in the same
        order -- which makes comparing different versions much more productive.)

        * If file is a string or Path, write to that filesystem location.
        * If file is a file-like object, write to that file.
        """
        if file is None:
            file = self.filepath

        assert isinstance(
            file, (str, Path, IOBase)
        ), f"file={file} ({type(file)}), which is not writeable."

        output = b"<?xml version='1.0' encoding='UTF-8'?>\n" + self.canonicalize()
        if isinstance(file, IOBase):
            file.write(output)
        else:
            with open(file, "wb") as f:
                f.write(output)
