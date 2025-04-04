# xwkh (x-wayland keybindings helper)
A keybindings helper. Powered by AI.

## Based on [this script](https://github.com/JaKooLit/Hyprland-Dots/blob/main/config/hypr/scripts/KeyHints.sh) by [JaKooLit](https://github.com/JaKooLit). Converted to Python using GPT O4 mini (Merlin).

# Feature
- small package
- uses JSON to configure keybinds to display
- easy to configure the application

# Use
Download and run the binary. Press `esc` to quit.

You must put the .json file and the .ini file in the same directory as the binary. There are example files on the archive (config + my hyprland keybindings)

# Launch options
## Attention: please list all the keybindings file (.json) on the config file before launching.
Run `xwkh -0` for the first config file of the list, then -1 for the second and so on. It will use config number 0 as default, unless configured.


# Configure
The config file is straightfoward. You can modify the background color, font color, opacity and font (it's so straightfoward lol).

`json_files =` will list a list of keybindings files, separated by a comma. Put all of them in the same folder as the executable.

`default_json_file = ` will configure which file to use when there is no launch option. File number starts with 0.

# To-be-added
- transparency (it's still an issue)
- loading config files from `$HOME/.config/`
- loading config file from the Internet
- separating the two columns

# Credits/Thanks
- [JaKooLit](https://github.com/JaKooLit) for his bash script
- OpenAI for the model
- Merlin for the service
- me for testing and fixing bugs (yes, there are)
