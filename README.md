



## niri-settings

> GUI in Qt for configure niri


https://github.com/user-attachments/assets/13a54d1a-438a-4f7d-b1c6-76a9c5da6fc4





## Usage

**Note**: A separated  `basicsettings.kdl` config file included at the end in the default `.kdl` file is needed, which means niri minimal version 25.11.


If no argument is given `$XDG_CONFIG_HOME/lxqt/wayland/niri/basicsettings.kdl` is used, otherwise
`niri-settings /path/to/file.kdl` can be used. Edit `ui/conf_path.py` to change this default.

## Installation

Manual installation as user is recommended atm.

```
git clone https://github.com/stefonarch/niri-settings
mkdir -p ~/.local/share/niri-settings/
cp -a niri-settings/translations ~/.local/share/niri-settings/

```
Run `niri-settings` from terminal or customize the `.desktop` file.





