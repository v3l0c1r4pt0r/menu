import pkgutil
import importlib
import argcomplete
import argparse
import sys

from menu.logger import Logger
from menu.hook import Hook

PLUGIN_PACKAGE_PREFIX = 'menu_plugin_'

log = Logger('menu').main_logger
log.debug(f'Logger instantiated')

class Menu:

  logging_levels = ['FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

  def __init__(self):
    self.create_ui()
    self.plugins = self.find_plugins()

  def main(self, argv):
    for plugin in self.plugins:
      log.debug(f'Processing plugin: {plugin}')
      self.register_plugin(plugin)

    return self.execute(argv[1:], self.parser, self.subparsers)

  def find_plugins(self):
    plugin_list = []
    for p in pkgutil.iter_modules():
      if p.name.startswith(PLUGIN_PACKAGE_PREFIX):
        plugin_list.append(p.name)
    return plugin_list

  def register_plugin(self, plugin_name):
    try:
      plugin = importlib.import_module(f'{plugin_name}.plugin')
      hook = Hook(self.subparsers)
      log.debug(f'Hook created: {hook}')
      plugin.register(hook)
    except ModuleNotFoundError:
      log.error(f'Plugin {plugin_name} is broken Skipping')

  def create_ui(self):
    self.parser = argparse.ArgumentParser(description='Menu', prog='m')
    self.subparsers = self.parser.add_subparsers(required=True)

    # add global arguments
    self.parser.add_argument('-v', '--verbosity', metavar='LEVEL', default='INFO',
        help='Set verbosity to LEVEL', choices=self.logging_levels)

  def execute(self, argv, parser, subparsers):
    if len(argv) == 0:
      parser.print_usage()
      return 255
    argcomplete.autocomplete(parser)
    args = parser.parse_args(argv)

    # consume global arguments
    log.setLevel(args.verbosity)

    return args.func(args)


def main():
  Menu().main(sys.argv)

if __name__ == '__main__':
  sys.exit(main())
