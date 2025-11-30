## niri-settings

> GUI in PyQt for configuring niri


https://github.com/user-attachments/assets/6b955a49-b09e-485c-ae79-6a2064a17fa4



## Usage

Under LXQt a line `include "niri/basicsettings.kdl"` at the bottom of the default `~/.config/lxqt/wayland/lxqt-niri.kdl` file has to be added. The "include" feature was added in niri version 25.11.

If no argument is given `$XDG_CONFIG_HOME/lxqt/wayland/niri/basicsettings.kdl` is used when running
under LXQt, otherwise `$XDG_CONFIG_HOME/niribasicsettings.kdl` will be used. Edit `ui/conf_path.py`
to change the defaults in other environments.

## Installation

Manual installation as user:

```
git clone https://github.com/stefonarch/niri-settings
cd niri-settings
mkdir -p ~/.local/share/niri-settings/  ~/.local/share/applications
cp niri-settings.desktop ~/.local/share/applications/
cp -a translations/ ~/.local/share/niri-settings/
mkdir -p ~/.local/share/icons/hicolor/scalable/apps/
cp niri-settings.svg ~/.local/share/icons/hicolor/scalable/apps/niri-settings.svg


```
Run `./niri-settings` from terminal inside the folder or customize `~/.local/share/applications/niri-settings.desktop` to match the path to `niri-setttings/niri-settings.py`.

A `PKGBUILD` is added now.

## Todo list

* Add tab settings somewhere
* Add hint settings
* Default column width settings
* Submit to https://translate.lxqt-project.org after feedback
