#!/usr/bin/env python3
import pkgutil
import importlib
import argcomplete
import argparse
import sys

from menu.logger import Logger

log = Logger('menu').main_logger
log.debug(f'Logger instantiated')

from menu.hook import Hook
from menu.plugin import Plugin, Plugins

PLUGIN_PACKAGE_PREFIX = 'menu_plugin_'

class Menu:

  logging_levels = ['FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

  def __init__(self):
    self.create_ui()
    self.plugins = Plugins()

  def setLogLevel(self, argv):
    idx = -1
    try:
      idx = argv.index('-v')
    except ValueError:
      pass
    try:
      idx = argv.index('--verbose')
    except ValueError:
      pass
    if idx != -1:
      try:
        log.setLevel(argv[idx+1])
      except IndexError:
        pass

  def main(self, argv):
    self.setLogLevel(argv)
    self.register_plugins()

    return self.execute(argv[1:], self.parser, self.subparsers)

  def register_plugins(self):
    for p in pkgutil.iter_modules():
      if p.name.startswith(PLUGIN_PACKAGE_PREFIX):
        self.register_plugin(p.name)

  def register_plugin(self, plugin_name):
    log.debug(f'Registering plugin {plugin_name}')
    try:
      plugin_module = importlib.import_module(f'{plugin_name}.plugin')
      hook = Hook(self.subparsers)
      log.debug(f'Hook created: {hook}')
      plugin_obj = plugin_module.init(self.plugins)
      plugin_obj.register(hook)
    except ModuleNotFoundError:
      log.error(f'Plugin {plugin_name} is broken Skipping')

  def create_ui(self):
    self.parser = argparse.ArgumentParser(description='Menu', prog='m')
    self.subparsers = self.parser.add_subparsers(required=True)

    # add global arguments
    self.parser.add_argument('-v', '--verbosity', metavar='LEVEL', default='INFO',
        help='Set verbosity to LEVEL', choices=self.logging_levels)

  def execute(self, argv, parser, subparsers):
    argcomplete.autocomplete(parser)
    log.debug('Argcomplete completion got called')
    if len(argv) == 0:
      parser.print_usage()
      return 255
    args = parser.parse_args(argv)

    # consume global arguments
    log.setLevel(args.verbosity)

    return args.func(args)


def main():
  Menu().main(sys.argv)

if __name__ == '__main__':
  sys.exit(main())
