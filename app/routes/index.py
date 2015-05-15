from app import app
from pysnap import get_file_extension, Snapchat
from flask import request
import json
import shutil
import os
import sys
from glob import glob
from getpass import getpass
from zipfile import is_zipfile, ZipFile

from docopt import docopt

snapchat = Snapchat('secondwindsnaps', '2433fd63b5389757d0786ebf056a946e')

def process_snap(snap, s=snapchat, path='app/static/snap/', quiet=False):
    snap = snap['story']
    filename = '{0}.{1}'.format(snap['media_id'],
                                    get_file_extension(snap['media_type']))
    snap['filename'] = 'snap/' + filename
    snap['mediatext'] = False
    abspath = os.path.abspath(os.path.join(path, filename))
    if os.path.isdir(path + snap['id']):
      snap['mediatext'] = True
      snap['filename'] = 'snap/{}/media.mp4'.format(snap['id'])
      return snap
    if os.path.isfile(abspath):
      return snap
    data = s.get_blob(snap['id'])

    if data is None:
        return snap
    with open(abspath, 'wb') as f:
        f.write(data)
        if not quiet:
            print('Saved: {0}'.format(abspath))

    if is_zipfile(abspath):
        zipped_snap = ZipFile(abspath)
        unzip_dir = os.path.join(path, '{}'.format(snap['id']))
        zipped_snap.extractall(unzip_dir)
        if not quiet:
            print('Unzipped {0} to {1}'.format(filename, unzip_dir))
        for f in glob('{}{}/media*'.format(path, snap['id'])):
          os.rename(f, '{}{}/media.mp4'.format(path, snap['id']))
        for f in glob('{}{}/overlay*'.format(path, snap['id'])):
          os.rename(f, '{}{}/overlay.png'.format(path, snap['id']))
        snap['mediatext'] = True
        snap['filename'] = 'snap/{}/media.mp4'.format(snap['id'])

    return snap

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/snaps')
def getSnaps():
  snaps = stories = snapchat._request("all_updates", {
            'username': snapchat.username,
            'update_timestamp': 0
        }).json()['stories_response']['my_stories']
  snaps = map(process_snap, snaps)
  print snaps
  return json.dumps(snaps)

@app.route('/api/reject/', methods=['POST'])
def reject():
  snap = request.json
  snapchat.mark_viewed(snap['id'])
  if snap['mediatext']:
    os.remove('app/static/{}'.format(snap['filename']))
    shutil.rmtree('app/static/snap/{}'.format(snap['id']))
  else:
    os.remove('app/static/{}'.format(snap['filename']))
  return "Removed {}".format(snap['id'])

@app.route('/api/accept/', methods=['POST'])
def accept():
  snap = request.json
  snapchat.mark_viewed(snap['id'])
  if snap['mediatext']:
    snapchat.send_to_story(snapchat.upload('app/static/snap/{}.mp4'.format(snap['id'])))
  else:
    snapchat.send_to_story(snapchat.upload('app/static/{}'.format(snap['filename'])))
  return "Posted {} to story".format(snap['id'])

@app.route('/api/friends')
def getFriends():
  return json.dumps(snapchat.get_friends())

@app.route('/api/add/<name>')
def addFriend(name):
  snapchat.add_friend(name)
  return "Added {}".format(name)

@app.route('/api/remove/<name>')
def removeFriend(name):
  snapchat.delete_friend(name)
  return "Deleted {}".format(name)
