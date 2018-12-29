# AudioBPot

AudioBPot your personal "Audio Book Podcast Feed Creator Robot"

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
  * taglib 0.3.6+dfsg-2build7
  * pytz 2018.5
  * lxml 4.2.5

## Media file preparation

Move all files to a 'media' subdirectory. The files modification time is used
as their publication time in the podcast feed. As podcast players use the
publication time to sort the podcast feed, make sure the modification time is
set to your needs. If the files where just ripped, the files should be in
correct order.

If you need to recreate the modification order, one simple method is, to use filenames that sort in the wanted order and re-touch the files.

```bash
a=100
for file in $(echo *.mp3 | sort)
do
	touch -d "$a hours ago" $file
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
