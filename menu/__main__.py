import pkgutil

PLUGIN_PACKAGE_PREFIX = 'menu_plugin_'

def find_plugins():
  plugin_list = []
  for p in pkgutil.iter_modules():
    if p.name.startswith(PLUGIN_PACKAGE_PREFIX):
      plugin_list.append(p.name)
  return plugin_list

def main():
  print('Found following plugins:')
  plugins = find_plugins()
  for plugin in plugins:
    print(f'\t{plugin}')

if __name__ == '__main__':
  main()
