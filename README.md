# AudioBPot

AudioBPot your personal "Audio Book Podcast Feed Creator Robot"

Sick of listening to audio books in your local mp3 player when podcast players
are so good at remembering the position you stopped playing? This python script
creates a static podcast feed to be served locally in your WiFi by any
available web server in your local network.

## python package requirements

python version and modules used during development of the application

* Python 3.6.7
  * os
  * sys
  * logging
  * argparse
  * datetime
  * configparser
  * distutils.util
  * podgen 1.0.0
  * pytz 2018.5
  * lxml 4.2.5

## Media file preparation

Move all files to a 'media' subdirectory. The files modification time is used
as their publication time in the podcast feed. As podcast players use the
publication time to sort the podcast feed, make sure the modification time is
set to your needs. If the files where just ripped, the files should be in
correct order.

If you need to recreate the modification order, one simple method is, to use filenames that sort in the wanted order and re-touch the files.

While at it, remove spaces from filenames.

```bash
for file in *.mp3
do
	mv "$file" $(echo "$file" | sed 's/ /_/g')
done

let a=1000
for file in $(echo *.mp3 | sort)
do
	touch -d "$a hours ago" "$file"
	let a=$a-1
done
```

## podcast icon / cover image

Prepare a cover image and place it in the podcast folder. 200px x 200px seems
to be a reasonable size.

## podcast initialization file

create a file named 'podcast.ini' by default and fill it accordingly:

```ini
[podcast]

name = Name of your audio book
explicit = False # (or True if you like)
description = Short description of the podcast
image = podcast_image_filename.jpeg
```

## command line options

The --directory option is always required. The --server option is always
required when creating a podcast, can be omitted when only creating the
overview page.

```
usage: audiobpot.py [-h] [-c] [-p] [-o] [-d DIRECTORY] [--protocol PROTOCOL]
                    [-s SERVER] [-r PODCASTROOT] [-m MEDIASUBDIR] [-i INIFILE]
                    [--rssxslt RSSXSLT] [--overviewxslt OVERVIEWXSLT]
                    [--indexfile INDEXFILE] [-v]

Create static podcasts from audio book audio files (see README.md for detailed
information)

optional arguments:
  -h, --help            show this help message and exit
  -c, --collection      (re-)create podcast collection creation (all sub-
                        directories visited)
  -p, --podcast         create a single static podcast
  -o, --overview        create overview index file of collection
  -d DIRECTORY, --directory DIRECTORY
                        path of directory
  --protocol PROTOCOL   data transfer protocol (default http)
  -s SERVER, --server SERVER
                        server name or ip
  -r PODCASTROOT, --podcastroot PODCASTROOT
                        server root directory (default '')
  -m MEDIASUBDIR, --mediadir MEDIASUBDIR
                        subdir for media files in podcast directory (default
                        media)
  -i INIFILE, --inifile INIFILE
                        ini file in podcast directory (default podcast.ini)
  --rssxslt RSSXSLT     xslt to create podcast website from rss feed (default
                        xslt/rss.xslt)
  --overviewxslt OVERVIEWXSLT
                        xslt to create podcast overview website from rss feeds
                        (default xslt/overview.xslt)
  --indexfile INDEXFILE
                        html indexfile filename (default index.html)
  -v, --verbose         create verbose debugging output

2018, Robert Schneider

```
