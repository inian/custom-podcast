import urllib2
import os
import logging
import uuid

import feedparser
from FeedItem import FeedItem
from Feed import Feed
from pytube import YouTube
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def downloadFeed(url):
    response = urllib2.urlopen(url)
    html = response.read()
    with open('/tmp/podcast.xml', 'w') as f:
        f.write(html)


def initFeed(podcastFile):
    d = feedparser.parse(podcastFile)
    f = Feed(title=d.feed.title, link=d.feed.link, description=d.feed.subtitle)
    for entry in d.entries:
        print entry['links']
        fi = FeedItem(id=entry['id'], title=entry['title'], link=entry['links'][-1]['href'], mimeType=entry[
                      'links'][-1]['type'], length=entry['links'][-1]['length'], description=entry['summary'])
        f.addEntry(fi)
    return f


def downloadVideo(videoURL, filepath):
    yt = YouTube(videoURL)
    video = yt.filter('mp4')
    if type(video) == list:
        video = video[0]
    video.download(filepath, force_overwrite=True)
    return video.filename


def uploadToS3(filename, filepath):
    s3 = boto3.client('s3')
    s3.upload_file(filepath, "custom-podcasts", filename,
                   ExtraArgs={'ACL': 'public-read'})


def lambda_handler(event, context):
    # if event['httpMethod'] != 'POST':
    #     return

    # body = json.loads(event['body'])
    # youtubeURL = body['youtubeURL']
    # podcastURL = body['podcastURL']

    youtubeURL = event['youtubeURL']
    podcastURL = event['podcastURL']

    # get current podcast.xml
    logger.info(youtubeURL)
    logger.info(podcastURL)

    downloadFeed(podcastURL)
    f = initFeed('/tmp/podcast.xml')

    unique_name = str(uuid.uuid1())
    filename = unique_name + '.mp4'
    filepath = '/tmp/' + filename
    videoName = downloadVideo(youtubeURL, filepath)
    logger.info(videoName)
    uploadToS3(filename, filepath)

    logger.info("https://s3.amazonaws.com/custom-podcasts/" + filename)
    # extractAudio('/tmp/video.mp4')

    newFeedItem = FeedItem(id=unique_name, title=videoName, link="https://s3.amazonaws.com/custom-podcasts/" + filename,
                           mimeType='video/mp4', length=str(os.path.getsize(filepath)), description='Well what do you want me to say')
    f.addEntry(newFeedItem)

    # insert and generate new podcast.xml
    f.writeFeed('/tmp/podcast.xml')

    uploadToS3('podcast.xml', '/tmp/podcast.xml')

    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": os.path.getsize(filepath)
    }
    return response
