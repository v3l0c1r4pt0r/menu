"""API between main module and plugins"""

"""Hook class

Its purpose is to be passsed to plugin and provide certain features"""
from pathlib import Path

from menu.config import Config

CONFIG_ROOT = Path("~").expanduser() / '.config' / 'menu'

class Hook:

  def __init__(self, subparsers):
    self.subparsers = subparsers
    self.config = Config(CONFIG_ROOT)
