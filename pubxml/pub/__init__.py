from lxml import etree

import pubxml

NS = {
    prefix: uri
    for prefix, uri in pubxml.NS.items()
    if prefix in ["html", "pub", "m", "epub", "opf"]
}
Builder = pubxml.Builder(NS, default=NS["html"])


def Document(filepath=None):
    html = Builder.html
    pub = Builder.pub
    opf = Builder.opf
    return pubxml.XML(
        tree=etree.ElementTree(
            pub.document(
                "\n",
                opf.metadata("\n\t"),
                "\n",
                html.body("\n", tail="\n"),
            )
        ),
        namespaces=NS,
        filepath=filepath,
    )


def Documents(filepath=None):
    pub = Builder.pub
    return pubxml.XML(
        tree=etree.ElementTree(pub.documents("\n")), namespaces=NS, filepath=filepath
    )
