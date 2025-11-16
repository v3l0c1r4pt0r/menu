import json

from menu.logger import Logger

log = Logger.get(__name__)

"""Configuration object"""
class Config:

  def __init__(self, root, name):
    self.location = root
    self.name = name
    self.obj = None

  def create(self, file):
    if not file.parent.exists():
      file.parent.mkdir(parents=True, exist_ok=True)
    # defaults:
    obj = {
      'property': 'value',
    }
    with open(file, 'w') as fp:
      json.dump(obj, fp)

  def load(self):
    file = self.location / f'{self.name}.json'
    log.debug(f'Reading config from {file}')
    if not file.exists():
      self.create(file)
    with open(file, 'r') as fp:
      self.obj = json.load(fp)
    self.filename = file

  """Get property from config"""
  def get(self, prop):
    log.debug(f'Getting property {prop} for {self.name}')
    if self.obj is None:
      self.load()
    return self.obj[prop]

  def set(self, prop, value):
    log.debug(f'Changed {prop} to {value}')
    if self.obj is None:
      self.load()
    self.obj[prop] = value

  def save(self):
    log.debug(f'Saving config for {self.name}')
    with open(self.filename, 'w') as fp:
      json.dump(self.obj, fp)
