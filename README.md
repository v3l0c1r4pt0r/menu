# menu

Template for having plugin architecture in Python

## Installation

1. In project directory type: `poetry build`
2. This creates package in `dist/` directory
3. Install it with `pip install dist/menu*.tar.gz`
4. Optionally do the same in [demo
plugin](https://github.com/v3l0c1r4pt0r/menu-plugin-demo) project

## Plugin interface

1. Each plugin must provide package `menu_plugin_$pluginname` in order to be
detected by menu (use poetry to have that one out of the box)
2. In this default package there must be at least one module called `plugin.py`
3. This module must provide register function with one argument - hook
4. This hook provides certain capabilities described separately
5. Plugins can get access to logging facility of main menu by importing
`menu.logger.Logger`, then getting its own child logger with:
`Logger.get(__name__)`, where `__name__` part is crucial to stay this way

### Hook capabilities

#### Access to subparsers

Each plugin can get access to subparsers of main argparse object. It can be used
to register its own command. Proper way of interaction is also to register a
function that will be executed if user chooses to execute the command.

Example:
```
def execute(args):
  print(args)

parser = hook.subparsers.add_parser('command', help='Some command')
parser.set_defaults(func=execute)
```

In this example, once user executes the following: `m command`, he will be
presented with all the arguments he passed as internal argparse object.

## argcomplete

Menu has integration with argcomplete. This allows effortless completion to be
installed in user's shell of choice. It does not require any additional code to
provide pretty good completion.

It must be however installed with:
1. Executing `activate-global-python-argcomplete --user` once after installing
argcomplete
2. Adding `eval "$(register-python-argcomplete m)"` to shell's rc file, like
`.bashrc`.
