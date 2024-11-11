import pkgutil
import importlib
import argparse
import sys

from menu.logger import Logger
from menu.hook import Hook

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
    hook = Hook()
    log.debug(f'Hook created: {hook}')
    plugin.register(hook)
  except ModuleNotFoundError:
    log.error(f'Plugin {plugin_name} is broken Skipping')

def create_ui():
  parser = argparse.ArgumentParser(description='Menu', prog='m')
  subparsers = parser.add_subparsers(required=True)

  return parser, subparsers

def execute(argv, parser, subparsers):
  if len(argv) == 0:
    parser.print_usage()
    return 255
  args = parser.parse_args(argv)
  return args.func(args)

def main(argv):
  parser, subparsers = create_ui()

  plugins = find_plugins()
  for plugin in plugins:
    log.debug(f'Processing plugin: {plugin}')
    register_plugin(plugin)

  return execute(argv[1:], parser, subparsers)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
