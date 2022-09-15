"""
Constructors et al for the <pub:*> namespace.
"""
from lxml import etree
import pubxml


NS = {
    prefix: uri
    for prefix, uri in pubxml.NS.items()
    if prefix in pubxml.namespaces(["html", "pub", "m", "epub", "opf"])
}
Builder = pubxml.Builder(NS, default=NS["html"])


def Document(filepath=None, metadata=None, body=None):
    HTML = pubxml.Builder.one(NS['html'])
    PUB = pubxml.Builder.one(NS['pub'])
    OPF = pubxml.Builder.one(NS['opf'])
    return pubxml.XML(
        tree=etree.ElementTree(
            PUB.document(
                "\n",
                metadata if metadata is not None else OPF.metadata("\n\t"),
                "\n",
                body if body is not None else HTML.body("\n", tail="\n"),
            )
        ),
        namespaces=NS,
        filepath=filepath,
    )
