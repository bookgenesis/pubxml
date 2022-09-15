"""
The following XML namespaces are commonly used in publishing projects.
"""


def namespaces(prefixes):
    """
    Return a dict of namespaces with the given prefixes
    """
    return {ns: url for ns, url in NS.items() if ns in prefixes}


NS = {
    # XML
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    # XHTML, EPUB, etc.
    "html": "http://www.w3.org/1999/xhtml",
    "opf": "http://www.idpf.org/2007/opf",
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "epub": "http://www.idpf.org/2007/ops",
    "ncx": "http://www.daisy.org/z3986/2005/ncx/",
    # Dublin Core etc.
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "dcmitype": "http://purl.org/dc/dcmitype/",
    # MathML and DocBook
    "m": "http://www.w3.org/1998/Math/MathML",
    "db": "http://docbook.org/ns/docbook",
    # InDesign
    "aid": "http://ns.adobe.com/AdobeInDesign/4.0/",
    "aid5": "http://ns.adobe.com/AdobeInDesign/5.0/",
    # Microsoft
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    # RelaxNG
    "a": "http://relaxng.org/ns/compatibility/annotations/1.0",
    "r": "http://relaxng.org/ns/structure/1.0",
    # Schematron
    "sch": "http://purl.oclc.org/dsdl/schematron",
    # Publishing XML
    "pub": "http://publishingxml.org/ns",
}
