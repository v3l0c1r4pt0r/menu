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
  OFF = 0
  BOLD = 1


class Color(Enum):
  RED = 31
  GREEN = 32
  YELLOW = 33
  BLUE = 34
  MAGENTA = 35
  CYAN = 36
  DARK_GREY = 90
  LIGHT_RED = 91
  LIGHT_GREEN = 92
  LIGHT_YELLOW = 93
  LIGHT_BLUE = 94
  LIGHT_MAGENTA = 95
  LIGHT_CYAN = 96


class ColoringFormatter(logging.Formatter):

  fmt = '{start}%(levelname)s/%(name)s [%(asctime)s]: %(message)s{stop}'
  FORMATS = {
    logging.FATAL: fmt.format(start=Format(Style.BOLD, Color.RED),
        stop=Format(Style.OFF)),
    logging.ERROR: fmt.format(start=Format(color=Color.LIGHT_RED),
        stop=Format(Style.OFF)),
    logging.WARNING: fmt.format(start=Format(color=Color.LIGHT_YELLOW),
        stop=Format(Style.OFF)),
    logging.DEBUG: fmt.format(start=Format(color=Color.DARK_GREY),
        stop=Format(Style.OFF)),
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
    self.main_logger.setLevel(logging.INFO)

    # create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # set console handler's formatter to coloring
    handler.setFormatter(ColoringFormatter())
    self.main_logger.addHandler(handler)

  def get(module):
    module = module.replace('menu_plugin_', 'plugin.')
    return Logger.logger.main_logger.getChild(module)
