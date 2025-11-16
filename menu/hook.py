"""API between main module and plugins"""

"""Hook class

Its purpose is to be passsed to plugin and provide certain features"""
from pathlib import Path

class Hook:

  def __init__(self, subparsers):
    self.subparsers = subparsers
