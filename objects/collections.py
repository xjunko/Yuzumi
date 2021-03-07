import logging

import utils

class BaseCollection:
  name: str = 'BaseCollection'
  attrs: list = []

  def __init__(self):
    self.storage: list = []

  def __len__(self):
    return len(self.storage)

  def __iter__(self):
    return iter(self.storage)

  def __repr__(self):
    return f'<{self.name}|Items: {len(self)}>'

  def add(self, o: object):
    if o in self.storage:
      return logging.info(f"Already added {o} into {self.name}")


    self.storage.append(o)
    logging.info(f"Added {o} into {self.name}")

  def fix_attr(self, attr: str, val: str):
    """ yes """
    ...

  def get(self, **kwargs):
    for attr in self.attrs:
      if val := kwargs.get(attr, None):
        break
    else:
      raise Exception(f"Failed to get object from {self.name}: kwargs - {kwargs}")

    attr, val = self.fix_attr(attr, val)

    for x in self.storage:
      if getattr(x, attr) == val:
        return x


class PlayerList(BaseCollection):
  name = 'PlayerList'
  attrs = ['id', 'name']

  def fix_attr(self, attr: str, val: str):
    if attr == 'name':
      attr = 'name_safe'
      val = utils.make_safe(val)

    return attr, val




