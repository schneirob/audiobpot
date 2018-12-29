import logging
import os

import lxml.html
from lxml import etree

def xsltparse(xsltpath, xmlpath, resultpath):
    name = "xsltparse"
    log = logging.getLogger(__name__ + "." + name)

    if not os.path.isfile(xsltpath):
        log.error("xsltpath " + str(xsltpath) + " is not a valid file!")
        return
    if not os.path.isfile(xmlpath):
        log.error("xmlpath " + str(xmlpath) + " is not a valid file!")
        return

    try:
        xslt = etree.parse(xsltpath)
        trans = etree.XSLT(xslt)

        # https://lxml.de/parsing.html
        parser = etree.XMLParser(ns_clean=True, huge_tree=True, recover=True)
        source = etree.parse(xmlpath, parser)

        html = trans(source)
        html.write(resultpath)
    except Exception as e:
        log.exception("Failed to parse xml using xslt!")
        return

    log.debug("Parsed xml written to" + str(resultpath))
