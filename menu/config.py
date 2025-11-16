from menu.logger import Logger

log = Logger.get(__name__)

"""Configuration object"""
class Config:

  def __init__(self, root, name):
    self.location = root
    self.name = name
    self.obj = None

  def load(self):
    log.debug(f'Reading config from {self.location / self.name}')
    return None

  """Get property from config"""
  def get(self, prop):
    log.debug(f'Getting property {prop} for {self.name}')
    return None

  def set(self, prop, value):
    log.debug(f'Attempted change to {prop} = {value}')

  def save(self):
    log.debug(f'Saving config for {self.name}')
