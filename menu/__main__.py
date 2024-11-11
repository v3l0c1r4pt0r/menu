import pkgutil
import importlib

from menu.logger import Logger

PLUGIN_PACKAGE_PREFIX = 'menu_plugin_'

logger = Logger(__name__).main_logger
logger.debug(f'Logger instantiated')

def find_plugins():
  plugin_list = []
  for p in pkgutil.iter_modules():
    if p.name.startswith(PLUGIN_PACKAGE_PREFIX):
      plugin_list.append(p.name)
  return plugin_list

def register_plugin(plugin_name):
  try:
    plugin = importlib.import_module(f'{plugin_name}.plugin')
  except ModuleNotFoundError:
    print(f'Plugin {plugin_name} is broken')
  plugin.register()

def main():
  print('Found following plugins:')
  plugins = find_plugins()
  for plugin in plugins:
    print(f'\t{plugin}')
    register_plugin(plugin)
  logger.fatal('Not implemented')

if __name__ == '__main__':
  main()
