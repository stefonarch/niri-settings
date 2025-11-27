## niri-settings

> GUI in PyQt for configuring niri


https://github.com/user-attachments/assets/6b955a49-b09e-485c-ae79-6a2064a17fa4



## Usage

**Note**: A separated  `basicsettings.kdl` config file included at the end in the default `.kdl` file is needed.
Aka niri minimal version supported is 25.11.

Consider this beta software atm.


If no argument is given `$XDG_CONFIG_HOME/lxqt/wayland/niri/basicsettings.kdl` is used when running
under LXQt, otherwise `$XDG_CONFIG_HOME/niribasicsettings.kdl` will be used. Edit `ui/conf_path.py`
to change the defaults.

## Installation

Manual installation as user is recommended atm.

```
git clone https://github.com/stefonarch/niri-settings
mkdir -p ~/.local/share/niri-settings/
cp -a niri-settings/translations ~/.local/share/niri-settings/

```
Run `niri-settings` from terminal or customize the `.desktop` file.





