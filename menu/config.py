"""Configuration object

Its purpose is to provide subobjects for plugins, keeping separate
configuration for each plugin, while still allowing orderly reads from other
plugins."""
class Config:

  def __init__(self, root):
    self.location = root
