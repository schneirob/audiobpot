import logging
import os

from urllib.parse import quote as urlquote
from distutils.util import strtobool
from podgen import Podcast, Episode, Media
from datetime import datetime
import pytz

from utils.xslt import xsltparse
from utils.configread import ConfigRead
from utils.pathutils import get_files


class AudioBPot():
    """Create a podcast feed from directory with media files"""

    def __init__(self, path, **kwargs):
        """create podcast feed for path using configuration given in kwargs

        Parameters
        ----------
        path : str
            base directory for podcast
        **kwargs
            protocol : str
                http or https (defaults to http)
            server : str
                server name or ip
            podcastroot : str
                root for podcasts on the server (defaults to "")
            mediasubdir : str
                subdirectory where media files are stored (defaults to
                "media")
            inifile : str
                podcast configuration filename (defaults to podcast.ini)
            rssxslt : str
                xslt file to tranform rss feed into index.html
            indexfile : str
                filename of index file (defaults to index.html)
        """
        self.name = "AudioBPot"
        self.log = logging.getLogger(__name__ + "." + self.name)
        self.log.debug("Initialising new AudioBPot")

        self.is_podcast = False

        self.indexfile = "index.html"
        if "indexfile" in kwargs:
            self.protocol = kwargs["indexfile"]

        if "rssxslt" in kwargs:
            self.rssxslt = kwargs["rssxslt"]
            if not os.path.isfile(self.rssxslt):
                self.log.error(str(self.rssxslt) + " is not a file!")
                return
        else:
            self.log.error("No xslt for rss conversion defined!")
            return

        self.path = path
        if not os.path.isdir(self.path):
            self.log.error(str(self.path) +
                           " is not a valid directory (base directory)!")
            return

        self.protocol = "http"
        if "protocol" in kwargs:
            self.protocol = kwargs["protocol"]

        if "server" not in kwargs:
            log.error("No server defined!")
            return
        self.server = kwargs["server"]

        self.podcastroot = ""
        if "podcastroot" in kwargs:
            self.podcastroot = kwargs["podcastroot"]

        self.mediasubdir = "media"
        if "mediasubdir" in kwargs:
            self.mediasubdir = kwargs["mediasubdir"]
        self.mediasubdirbasename = self.mediasubdir
        self.mediasubdir = self.path + "/" + self.mediasubdir
        if not os.path.isdir(self.mediasubdir):
            self.log.error(str(self.mediasubdir) +
                           " is not a valid directory (mediasubdir)!")
            return
        self.log.debug("Media directory: " + self.mediasubdir)

        if self.podcastroot is "":
            self.baseurl = self.protocol + "://" + \
                           self.server
        else:
            self.baseurl = self.protocol + "://" + \
                           self.server + "/" + \
                           urlquote(self.podcastroot)
        self.log.debug("Base URL: " + str(self.baseurl))
        self.podcasturl = self.baseurl + "/" + \
            urlquote(os.path.basename(self.path))
        self.log.debug("Podcast URL: " + str(self.podcasturl))
        self.mediaurl = self.podcasturl + "/" + \
            urlquote(self.mediasubdirbasename)
        self.log.debug("Media URL: " + str(self.mediaurl))
        self.feedurl = self.podcasturl + "/" + \
            urlquote(os.path.basename(self.path)) + ".xml"
        self.log.debug("Feed URL: " + str(self.feedurl))
        self.feedpath = self.path + "/" + os.path.basename(self.path) + \
            ".xml"
        self.log.debug("Feed Path: " + str(self.feedpath))

        self.inifile = "podcast.ini"
        if "inifile" in kwargs:
            self.inifile = kwargs["inifile"]
        self.inifile = self.path + "/" + self.inifile
        if not os.path.isfile(self.inifile):
            self.log.error(str(self.inifile) +
                           " is not a valid file (podcast configuration)!")
            return

        self.config = ConfigRead(self.inifile)
        if self.config.is_config:
            if "podcast" in self.config._config:
                self.config = self.config._config['podcast']
            else:
                self.log.error(str(self.inifile) +
                               " is no valid podcast config!")
                return
        else:
            self.log.error("Failed to read configuration from " +
                           str(self.inifile))
            return
        self.log.debug("Podcast config: " + str(self.config))

        self.podcast_name = os.path.basename(self.path)
        if "name" in self.config:
            self.podcast_name = self.config["name"]
        self.log.debug("Podcast name: " + str(self.podcast_name))

        self.podcast_description = os.path.basename(self.path)
        if "description" in self.config:
            self.podcast_description = self.config["description"]
        self.log.debug("Podcast description: " + str(self.podcast_description))

        self.podcast_image = False
        if "image" in self.config:
            self.podcast_imagepath = self.path + "/" + self.config["image"]
            if not os.path.isfile(self.podcast_imagepath):
                self.log.warning(str(self.podcast_imagepath) +
                                 " is no valid file!")
            else:
                self.podcast_image = True
                self.podcast_imageurl = self.podcasturl + "/" + \
                    urlquote(self.config["image"])
                self.log.debug("Podcast image URL: " +
                               str(self.podcast_imageurl))

        self.podcast_explicit = True
        if "explicit" in self.config:
            self.podcast_explicit = bool(strtobool(self.config["explicit"]))
        self.log.debug("Podcast explicit: " + str(self.podcast_explicit))

        self.mediafiles = get_files(self.mediasubdir)
        self.mediafiles.sort()

        self.podcast = Podcast()
        self.podcast.name = self.podcast_name
        self.podcast.description = self.podcast_description
        self.podcast.website = self.podcasturl
        self.podcast.explicit = self.podcast_explicit
        if self.podcast_image:
            self.podcast.image = self.podcast_imageurl
        self.podcast.feed_url = self.feedurl

        count = 0
        for media in self.mediafiles:
            count += 1
            episode = self.podcast.add_episode()
            episode.title = os.path.splitext(os.path.basename(media))[0].encode(
                    encoding="ascii",errors="xmlcharrefreplace")
            episode.subtitle = os.path.splitext(os.path.basename(media))[0].encode(
                    encoding="ascii",errors="xmlcharrefreplace")
            episode.summary = (self.podcast_description +
                    "\n<br/>\n" + "media " + str(count) + "\n<br/>\n").encode(
                    encoding="ascii",errors="xmlcharrefreplace") + \
                             episode.title
            episode.publication_date = pytz.utc.localize(
                                            datetime.utcfromtimestamp(
                                                os.path.getmtime(
                                                    self.mediasubdir + "/" +
                                                    media)))
            episode.media = Media(self.mediaurl + "/" + urlquote(media),
                                  size=os.path.getsize(self.mediasubdir + "/" +
                                                       media))
            episode.media.populate_duration_from(self.mediasubdir + "/" +
                                                 media)
            self.log.debug(str(media) + " has duration " +
                           str(episode.media.duration) +
                           " and size " + str(episode.media.size))
        self.is_podcast = True

    def write_rss(self):
        if not self.is_podcast:
            self.log.error("Podcast creation failed. Cannot create RSS!")
            return
        self.podcast.rss_file(self.feedpath)
        self.log.debug("RSS feed created at " + str(self.feedpath))

    def write_html(self):
        if not self.is_podcast:
            self.log.error("Podcast creation failed. Cannot create html!")
            return
        xsltparse(
                self.rssxslt,
                self.feedpath,
                self.path + "/" + self.indexfile)
