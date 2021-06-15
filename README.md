# Sublime Text's Programatic Key Bindings

Use the full power of python to declare your key bindings.

Just imaging writing your bindings with this api:

```python
prefix_origami = "ctrl+w"

def keybinding(bind, **kwargs):
  command = kwargs.get('command')

  # Move between selections in overlay
  bind(["alt+k"], "move", overlay_visible, by="lines", forward=False)
  bind(["alt+j"], "move", overlay_visible, by="lines", forward=True)

  # Safe quit
  bind(["ctrl+q"], [command("close_workspace"), command("exit")])

  # Plugin: Origami
  bind([prefix_origami], "noop") # Disable the default behavior of ctrl+w
  bind([prefix_origami, "q"], "close")
  bind([prefix_origami], "c", "destroy_pane", direction="self")



# Contexts
overlay_visible = {
  "key": "overlay_visible",
  "operator": "equal",
  "operand": true
}
```

## Getting Started

### Installation
#### Recommended (for now, 'cause is not in Package control's repository)

Install `SublimeProKeyBindings` via Package Control.

1. Open the Command Palette via <kbd>Ctrl</kbd>/<kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>p</kbd>
2. Select *Package Control: Add Repository*
3. Copy the link of this repository on the input
4. Search for `SublimeProKeyBindings` and press <kbd>↲ Enter</kbd>

#### Manual

1. Clone or download this repository, (re)name the folder to `SublimeProKeyBindings` if necessary.
2. Move the folder inside your sublime `/Packages`. (*Preferences > Browse Packages...*)

## Usage

### Using the default command

This plugin only adds one command to sublime text:

```json
[
  {
    "caption": "Sublime Programatic Key Bindings - Compile Default",
    "command": "spk_key_binding",
    "args": {
      "bindings": "$packages/User/SublimeProKeyBindings/keybindings.py",
      "destination": "$packages/User/SublimeProKeyBindings/Default ($platform).sublime-keymap"
    }
  }
]
```

Make sure the file that `bindings` is pointing to exists and also that the `destination` can be created in the directory. In here `$packages` refers to the directory where your sublime text packages live.

Once you have created the file create a function called `keybinding`. This function will be called with two arguments. The first argument is the function gathers the data of your keybindings. The second is a helper function which should be used only when you need to bind multiple commands to a key. 

```python
def keybinding(bind, **kwargs):
  command = kwargs.get('command')

  # Your code...
```

After this function is executed a `.sublime-keymap` will be created in the directory `SublimeProKeyBindings` located in your "user folder". Sublime text will pick up any changes to that file and will reload your key bindings so the changes take effect (and you should be able to use then inmediately, reset sublime if you want to be sure).

That means, this plugin doesn't do anything at runtime. After the `.sublime-keymap` is created everything is in the hands of sublime's internal mechanism.

Anyway, once your ready, search the command `Sublime Programatic Key Bindings - Compile Default` in the command palette and run it.

### Create your own command

If you want to manage your primary keymap, the one in the root of your user folder, you need to create a new command.

First, create a file called `Default.sublime-commands`. In there you can your custom command.

```json
[
  {
    "caption": "Update root key bindings",
    "command": "spk_key_binding",
    "args": {
      "bindings": "$packages/User/keybindings.py",
      "destination": "$packages/User/Default.sublime-keymap"
    }
  }
]
```

Now your ready. Make sure `keybindings.py` exists and has the code you need. Search in the command palette `Update root key bindings`, run it and enjoy.

## Support

If you find this plugin useful and want to support my efforts, [buy me a coffee ☕](https://www.buymeacoffee.com/vonheikemen).

[![buy me a coffee](https://res.cloudinary.com/vonheikemen/image/upload/v1618466522/buy-me-coffee_ah0uzh.png)](https://www.buymeacoffee.com/vonheikemen)

