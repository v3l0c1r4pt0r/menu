import pkgutil
import importlib

from menu.logger import Logger

PLUGIN_PACKAGE_PREFIX = 'menu_plugin_'

log = Logger('menu').main_logger
log.debug(f'Logger instantiated')

def find_plugins():
  plugin_list = []
  for p in pkgutil.iter_modules():
    if p.name.startswith(PLUGIN_PACKAGE_PREFIX):
      plugin_list.append(p.name)
  return plugin_list

def register_plugin(plugin_name):
  try:
    plugin = importlib.import_module(f'{plugin_name}.plugin')
    plugin.register()
  except ModuleNotFoundError:
    log.error(f'Plugin {plugin_name} is broken Skipping')

def main():
  plugins = find_plugins()
  for plugin in plugins:
    log.debug(f'Processing plugin: {plugin}')
    register_plugin(plugin)
  log.fatal('Not implemented')
  log.error('Not implemented')
  log.warning('Not implemented')
  log.info('Not implemented')
  log.debug('Not implemented')

if __name__ == '__main__':
  main()
