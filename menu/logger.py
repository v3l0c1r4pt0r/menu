import logging
from enum import Enum

class Format:

  def __init__(self, style=None, color=None):
    self.style = style
    self.color = color

  def __str__(self):
    stack = []
    if self.color is not None:
      stack.append(str(self.color.value))
    if self.style is not None:
      stack.append(str(self.style.value))
    seq_list = ';'.join(stack)
    return f'\033[{seq_list}m'


class Style(Enum):
  NORMAL = 0
  BOLD = 1
  WTF = 20


class Color(Enum):
  RED = 31
  LIGHT_RED = 91


class ColoringFormatter(logging.Formatter):

  fmt = '{start}%(levelname)s/%(name)s [%(asctime)s]: %(message)s{stop}'
  FORMATS = {
    logging.FATAL: fmt.format(start=Format(Style.BOLD, Color.RED),
        stop=Format(Style.NORMAL)),
    logging.NOTSET: fmt.format(start='', stop=''),
  }

  def format(self, record):
    if record.levelno in self.FORMATS:
      fmt = self.FORMATS[record.levelno]
    else:
      fmt = self.FORMATS[logging.NOTSET]
    formatter = logging.Formatter(fmt)
    return formatter.format(record)


class Logger:

  logger = None

  def __init__(self, appname):
    if type(self).logger is not None:
      raise Exception('Singleton reinitialization')
    else:
      type(self).logger = self

    # create main logger
    self.main_logger = logging.getLogger(appname)
    self.main_logger.setLevel(logging.DEBUG)

    # create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # set console handler's formatter to coloring
    handler.setFormatter(ColoringFormatter())
    self.main_logger.addHandler(handler)

  def get(module):
    return Logger.logger.main_logger.getLogger(module)
