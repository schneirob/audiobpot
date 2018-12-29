from utils.configread import ConfigRead
from utils.audiobpot import AudioBPot
from utils.feedextractor import FeedExtractor
import logging
from utils.pathutils import get_subdirs
from utils.xslt import xsltparse

from argparse import ArgumentParser
from lxml import etree
import sys
import os


def create_podcast(path, config):
    ap = AudioBPot(path, **config)
    ap.write_rss()
    ap.write_html()


def init():
    parser = ArgumentParser(
            description='Create static podcasts from audio book audio files' +
            " (see README.md for detailed information)",
            epilog='2018, Robert Schneider')
    parser.add_argument(
            "-c", "--collection", action="store_true",
            dest="collection", help="(re-)create podcast collection " +
            "creation (all sub-directories visited)", default=False)
    parser.add_argument(
            "-p", "--podcast", action="store_true",
            dest="podcast", help="create a single static podcast",
            default=False)
    parser.add_argument(
            "-o", "--overview", action="store_true",
            dest="overview", help="create overview index file of " +
            "collection", default=False)
    parser.add_argument(
            "-d", "--directory", action="store",
            dest="directory", help="path of directory", default=None)
    parser.add_argument(
            "--protocol", action="store",
            dest="protocol", help="data transfer protocol (default http)",
            default="http")
    parser.add_argument(
            "-s", "--server", action="store",
            dest="server", help="server name or ip", default=None)
    parser.add_argument(
            "-r", "--podcastroot", action="store",
            dest="podcastroot", help="server root directory (default '')",
            default="")
    parser.add_argument(
            "-m", "--mediadir", action="store",
            dest="mediasubdir", help="subdir for media files in podcast " +
            "directory (default media)", default="media")
    parser.add_argument(
            "-i", "--inifile", action="store",
            dest="inifile", help="ini file in podcast directory " +
            "(default podcast.ini)", default="podcast.ini")
    parser.add_argument(
            "--rssxslt", action="store", dest="rssxslt",
            help="xslt to create podcast website from rss feed " +
            "(default xslt/rss.xslt)", default="xslt/rss.xslt")
    parser.add_argument(
            "--overviewxslt", action="store", dest="overviewxslt",
            help="xslt to create podcast overview website from rss feeds " +
            "(default xslt/overview.xslt)", default="xslt/overview.xslt")
    parser.add_argument(
            "--indexfile", action="store", dest="indexfile",
            help="html indexfile filename (default index.html)",
            default="index.html")
    parser.add_argument(
            "-v", "--verbose", action="store_true", dest="verbose",
            help="create verbose debugging output", default=False)

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    # parse command line options
    o = parser.parse_args()

    # establish logging
    if o.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    log = logging.getLogger("podcast")
    log.debug("Running podcast generation")

    config = vars(o)
    log.debug("Options: " + str(config))

    # check command line options
    if o.collection and o.podcast:
        log.error("Target cannot be a collection and a podcast directory!")
        sys.exit(2)
    if o.overview and o.podcast:
        log.error("Target cannot be a collection to create overview " +
                  " and a podcast directory!")
        sys.exit(2)
    if not (o.collection or o.podcast or o.overview):
        log.error("What to do? Collection? Podcast? Overview?")
        sys.exit(2)
    if not o.directory:
        log.error("No directory specified!")
        sys.exit(2)
    if not os.path.isdir(o.directory):
        log.error("Given path " + str(o.directory) + " is not a valid " +
                  "directory!")
        sys.exit(2)

    if not o.server and (o.collection or o.podcast):
        log.error("No server specified! Required for valid podcast feed!")
        sys.exit(2)

    if o.collection:
        for d in get_subdirs(o.directory):
            create_podcast(o.directory + "/" + d, config)

    if o.podcast:
        create_podcast(o.directory, config)

    if o.overview:
        overview = etree.Element('podcastlist')
        for d in get_subdirs(o.directory):
            fe = FeedExtractor(o.directory + "/" + d + "/" + d + ".xml")
            overview.append(fe.xml_element())
        xml = etree.tostring(etree.ElementTree(overview),
                             pretty_print=True,
                             standalone=True)
        log.debug(xml)
        f = open(o.directory + "/overview.xml", 'w')
        f.write(xml.decode("utf-8"))
        f.close()
        xsltparse(
                o.overviewxslt,
                o.directory + "/overview.xml",
                o.directory + "/" + o.indexfile)


if __name__ == "__main__":
    init()
