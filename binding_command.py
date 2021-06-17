import platform
import os
import json

import sublime
import sublime_plugin

if platform.python_version() == '3.3.6':
  from importlib.machinery import SourceFileLoader

  def run_module(module_name, user_bindings, **kwargs):
    user_module = SourceFileLoader(module_name, user_bindings).load_module()
    user_module.keybinding(kwargs.get('key'), command=kwargs.get('command'))

else:
  import importlib.util

  def run_module(module_name, user_bindings, **kwargs):
    spec = importlib.util.spec_from_file_location(module_name, user_bindings)
    user_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_module)

    user_module.keybinding(kwargs.get('key'), command=kwargs.get('command'))


class SpkKeyBinding(sublime_plugin.ApplicationCommand):
  def __init__(self):
    self.path = '$packages/User/SublimeProKeyBindings/keybindings.py'
    self.dest = '$packages/User/SublimeProKeyBindings/Default ($platform).sublime-keymap'

    self.module = 'spk_user_bindings'

  def run(self, **kwargs):
    self.bindings = []

    user_bindings = format(kwargs.get('bindings', self.path))
    dest = format(kwargs.get('destination', self.dest))

    if not os.path.isfile(user_bindings):
      sublime.error_message("Couldn't find %s\n\nMake sure the file exists." % user_bindings)
      return

    try:
      run_module(self.module, user_bindings, key=self.key, command=self.command)
    except Exception as err:
      sublime.error_message("Something went wrong.\nCheck out sublime console to see more information")
      raise err

    if len(self.bindings) == 0:
      sublime.error_message("Couldn't find any key bindings")
      return

    with open(dest, 'w') as file:
      json.dump(self.bindings, file, indent=2)
      sublime.message_dialog("Key bindings updated")

  def key(self, keys, command, *context, **args):
    if not isinstance(keys, list) or len(keys) < 1:
      raise Exception("The first argument needs to be an array of keys")

    if not isinstance(command, (str, list)) or len(keys) < 1:
      raise Exception("The command needs to be a string or an array")

    data = {}

    data['keys'] = keys

    if isinstance(command, list):
      data['command'] = 'spk_multi_cmd'
      data['args'] = {"commands": command}
    else:
      data['command'] = command
      if len(args) > 0:
        data['args'] = self.set_args(args)

    if len(context) > 0:
      data['context'] = self.context(context)

    self.bindings.append(data)

  def set_args(self, args):
    data = {}
    for arg in args:
      data[arg] = args.get(arg)

    return data

  def context(self, args):
    res = []
    for a in args:
      if isinstance(a, list):
        res.extend(a)
      else:
        res.append(a)

    return res

  def command(self, name, **kwargs):
    data = {}
    data['command'] = name

    if len(kwargs) > 0:
      data['args'] = {}

      for k in kwargs:
        data['args'][k] = kwargs.get(k)

    return data


class SpkMultiCmd(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    commands = kwargs.get('commands', [])

    if len(commands) == 0:
      return

    for cmd in commands:
      name = cmd.get('command', "")
      args = cmd.get('args', None)

      if len(name) < 1:
        return

      if args is None:
        self.view.run_command(name)
      else:
        self.view.run_command(name, args)

def format(string):
  return sublime.expand_variables(string, sublime.active_window().extract_variables())

