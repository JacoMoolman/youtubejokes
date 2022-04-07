import httplib2
import os
import random
import sys
import time

from dateutil.rrule import rrule, WEEKLY, MO

from os import walk
import shutil


from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

# global YvidId

httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "E:\\Projects\\Jokes\\client_secrets.json"

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
   %s
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

inputdir="E:\\Projects\\JOKES\\finjokes"
outputdir="E:\\Projects\\JOKES\\donefinjokes"

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_UPLOAD_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
  tags = None
  if options.keywords:
    tags = options.keywords.split(",")

  body=dict(
    snippet=dict(
      title=options.title,
      description=options.description,
      tags=tags,
      categoryId=options.category
    ),
    status=dict(
      privacyStatus=options.privacyStatus
    )
  )


  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
  )

  resumable_upload(insert_request)

def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print( "Video id '%s' was successfully uploaded." % response['id'])
          print("Uploaded")
          global YvidId
          YvidId=response['id']
          print("YvidId inside:",YvidId)
          
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print( "Sleeping %f seconds and then retrying...") % sleep_seconds
      time.sleep(sleep_seconds)


def upload_video_to_youtube(filename,videotitle,videodesc,videokeyw):

  args = argparser.parse_args()

  args.file=filename
  args.title=videotitle
  args.description=videodesc
  args.keywords=videokeyw
  args.privacyStatus="private"
  args.category="23"
  args.publishAt="2022-04-06T00:00:00.000Z"
  

  youtube = get_authenticated_service(args)
  try:
    initialize_upload(youtube, args)
  except HttpError as e:
    print( "An HTTP error %d occurred:\n%s") % (e.resp.status, e.content)


def showmonday():
  for date in rrule(WEEKLY, byweekday=MO, count=400):
    print(date)

filenames = next(walk(inputdir), (None, None, []))[2]  # [] if no file



for file in filenames:
    fullfile=inputdir+"\\"+file
    print(fullfile)
    file=file.replace(".mp4","")
    print(file)
    upload_video_to_youtube(
    fullfile,
    file,
    file,"funny,joke,short,dad,jokes")
    print("----------------->Moving done",fullfile)
    shutil.move(fullfile, outputdir)
    input("Press Enter to continue...")



print("YvidId outside:",YvidId)

