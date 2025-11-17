"""Plugin interface"""
from menu.logger import Logger

log = Logger.get(__name__)

from pathlib import Path

from menu.config import Config

CONFIG_ROOT = Path("~").expanduser() / '.config' / 'menu'


class PluginNotFoundError(Exception):

  def __init__(self, plugin):
    super().__init__(self, f'Plugin {plugin} not found')


class Plugin:

  def __init__(self, plugins):
    self.config = Config(CONFIG_ROOT, type(self).__name__)
    self.deps = []
    self.__plugins = plugins

  """Return plugin that was marked as dependency"""
  def depend(self, plugin):
    dependency = self.__plugins.find(plugin)
    self.deps.append(plugin)
    return plugin

  def __register(self, hook):
    name = self.register(hook)
    self.__plugins.register(name, self)

  """Register plugin into system

  This is where it can insert its interface into argparse"""
  def register(self, hook):
    raise NotImplementedError()

  """Execute plugin action

  This is where it can execute action requested by user"""
  def execute(self, args):
    raise NotImplementedError()


class Plugins:

  def __init__(self):
    self.plugins = {}

  def register(self, name, plugin):
    self.plugins[name] = plugin

  def find(self, plugin):
    if plugin in self.plugins:
      return self.plugins[plugin]
    else:
      raise PluginNotFoundError(plugin)
