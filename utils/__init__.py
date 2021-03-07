import os

def make_safe(n: str):
  return n.lower().replace(' ', '_')

def check_folder():
  required_folders = ['avatars', 'replays', 'beatmaps']

  if not os.path.isdir('data'):
    os.mkdir('data')

  for folder in required_folders:
    if not os.path.isdir(f'data/{folder}'):
      os.mkdir(f'data/{folder}')

