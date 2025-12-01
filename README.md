## niri-settings

> GUI in PyQt for configuring niri


https://github.com/user-attachments/assets/0d2b044e-59a8-4427-bf19-e672891bd53b



## Usage

Default niri configuration values are used everywhere.

The line to include `basicsettings.kdl"` at the bottom of the default configuration file (for LXQt: `~/.config/lxqt/wayland/lxqt-niri.kdl`, otherwise `~/.config/niri/config.kdl`) should be added automatically when applying the first changes. The "include" feature was added in niri version 25.11.

If no argument is given `$XDG_CONFIG_HOME/lxqt/wayland/niri/basicsettings.kdl` is used when running
under LXQt, otherwise `$XDG_CONFIG_HOME/niri/basicsettings.kdl` will be used. Edit `ui/conf_path.py`
to change those defaults.

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

* Get feedback and testing
* Improve parsing
* Show default niri config files if not running under LXQt
* Default column width settings
* Setup translations at https://translate.lxqt-project.org
* Submit to AUR.
