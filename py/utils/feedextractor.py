import logging
import os
import sys

from lxml import etree
import datetime


class FeedExtractor():
    """Extract overview information from podcast feed"""

    def __init__(self, path):
        """extract information from RSS podcast feed

        Parameters
        ----------
        path : str
            podcast feed xml file
        """
        self.name = "FeedExtractor"
        self.log = logging.getLogger(__name__ + "." + self.name)
        self.log.debug("Initialising new FeedExtractor")

        self.is_podcast = False

        self.path = path
        if not os.path.isfile(self.path):
            self.log.error(str(self.path) +
                           " is not a valid file!")
            return

        self.xml = None
        try:
            parser = etree.XMLParser(
                    ns_clean=True,
                    huge_tree=True,
                    recover=True)
            self.xml = etree.parse(self.path, parser)
        except Exception as e:
            self.log.exception("Failed to parse given file!")
            return

        self.title = None
        for t in self.xml.xpath('//rss/channel/title'):
            self.title = str(t.text)
        self.log.debug("Title: " + self.title)

        self.description = None
        for d in self.xml.xpath('//rss/channel/description'):
            self.description = str(d.text)
        self.log.debug("Description: " + self.description)

        self.link = None
        for l in self.xml.xpath('//rss/channel/link'):
            self.link = str(l.text)
        self.log.debug("Link: " + self.link)

        self.feed = None
        for f in self.xml.xpath('//rss/channel/atom:link/@href',
                                namespaces={
                                    'atom': 'http://www.w3.org/2005/Atom', }):
            self.feed = str(f)
        self.log.debug("Feed: " + self.feed)

        self.image = None
        for i in self.xml.xpath('//rss/channel/itunes:image/@href',
                                namespaces={
                                    'itunes':
                                    'http://www.itunes.com/dtds/podca' +
                                    'st-1.0.dtd', }):
            self.image = str(i)
        self.log.debug("Image: " + self.image)

        self.duration = datetime.timedelta(seconds=0)
        self.mediacount = 0
        for d in self.xml.xpath('//rss/channel/item/itunes:duration',
                                namespaces={
                                    'itunes':
                                    'http://www.itunes.com/dtds/podcast' +
                                    '-1.0.dtd', }):
            self.mediacount += 1
            td = d.text.split(':')
            if len(td) == 1:
                self.duration += datetime.timedelta(
                        seconds=int(td[0]))
            if len(td) == 2:
                self.duration += datetime.timedelta(
                        minutes=int(td[0]), seconds=int(td[1]))
            if len(td) == 3:
                self.duration += datetime.timedelta(
                        hours=int(td[0]),
                        minutes=int(td[1]),
                        seconds=int(td[2]))
        self.log.debug("Duration: " + str(self.duration))
        self.log.debug("Media files: " + str(self.mediacount))

        self.is_podcast = True

    def xml_element(self):
        if not self.is_podcast:
            self.log.error("Not a valid podcast overview!")
            return None
        pod = etree.Element('podcast')
        doc = etree.ElementTree(pod)
        if self.title:
            etree.SubElement(pod, 'title').text = str(self.title)
        if self.description:
            etree.SubElement(pod, 'description').text = str(self.description)
        if self.link:
            etree.SubElement(pod, 'link').text = str(self.link)
        if self.feed:
            etree.SubElement(pod, 'feed').text = str(self.feed)
        if self.image:
            etree.SubElement(pod, 'image').text =str(self.image)
        etree.SubElement(pod, 'duration').text = str(self.duration)
        etree.SubElement(pod, 'mediaelements').text = str(self.mediacount)
        xml = etree.tostring(doc, pretty_print=True)
        self.log.debug("XML overview: " + str(xml))
        return pod


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger("main")
    log.debug("argv " + str(sys.argv))
    fe = FeedExtractor(sys.argv[1])
