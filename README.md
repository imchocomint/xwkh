# xwkh (x-wayland keybindings helper)
A keybindings helper.

## Based on [this script](https://github.com/JaKooLit/Hyprland-Dots/blob/main/config/hypr/scripts/KeyHints.sh) by [JaKooLit](https://github.com/JaKooLit). Converted to Python using GPT O4 mini (Merlin). Fixes by me.


# Feature
- small package
- uses JSON to configure keybinds to display
- easy to configure the application

# Use
Download and run the binary. Press `esc` to quit.

You must put the .json files and the .ini file in `$HOME/.config/xwkh.` Otherwise it will be in the `config` folder in the same directory. Config and keyfiles will be loaded in `.config` first, then in the app directory.

# Launch options
## Attention: please list all the keybindings file (.json) on the config file before launching.
Run `xwkh -0` for the first config file of the list, then -1 for the second and so on. It will use config number 0 as default, unless configured.


# Configure
The config file is straightfoward. You can modify the background color, font color, opacity and font (it's so straightfoward lol).

`json_files =` will list a list of keybindings files, separated by a comma. Put all of them in the same folder as the executable.

`default_json_file = ` will configure which file to use when there is no launch option. File number starts with 0.

# To-be-added
- [ ] transparency (it's still an issue)
- [x] loading config files from `$HOME/.config/`
- [ ] loading config file from the Internet
- [x] separating the two columns

# Credits/Thanks
- [JaKooLit](https://github.com/JaKooLit) for his bash script
- OpenAI for the model
- Merlin for the service
- me for testing and fixing bugs (yes, there are)
