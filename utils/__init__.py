import os
import hashlib
import uuid

def make_safe(n: str):
  return n.lower().replace(' ', '_')

def make_md5(n: str):
  return hashlib.md5(n.encode()).hexdigest()

def make_uuid(name: str = ''):
  return name + str(uuid.uuid4()).replace('-', '')

def check_folder():
  required_folders = ['replays', 'beatmaps']

  if not os.path.isdir('data'):
    os.mkdir('data')

  for folder in required_folders:
    if not os.path.isdir(f'data/{folder}'):
      os.mkdir(f'data/{folder}')

