from menu.logger import Logger

log = Logger.get(__name__)

"""Configuration object"""
class Config:

  def __init__(self, root, name):
    self.location = root
    self.name = name

  """Get config object for plugin"""
  def get(self):
    log.debug(f'Getting config for {self.name}')
    return None
