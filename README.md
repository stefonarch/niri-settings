## niri-settings

> GUI in PyQt for configuring niri


https://github.com/user-attachments/assets/cbd55c8f-163c-40a9-b882-86813ddd7c69


## Features

* Basic settings for appearance, behavior, mouse, touchpad and keyboard.
* Shortcut editor with filter and "Add new shortcut" dialog, including list of `niri msg action` commands.
* Display, edit, open and backup niri config files, including a configuration validator.
* Toolbox for showing infos about windows, outputs, layers and performing actions (pick color to clipboard,
kill selected window, detect xwayland windows).
* Detects if running under LXQt, otherwise default niri config path is used.


## Usage

Default niri configuration values are used everywhere, see `basicsettings.kdl` example file.

When running under LXQt `$XDG_CONFIG_HOME/lxqt/wayland/niri/` is used as configuration directory, otherwise `$XDG_CONFIG_HOME/niri/` will be used. Edit `ui/conf_path.py` to change those defaults. It will only write and `read basicsettings.kdl"` and `ḱeybinds.kdl` and not add any if already existing.

The lines to include `basicsettings.kdl"` and `ḱeybinds.kdl` at the end of the default configuration file will be added automatically only when applying the first changes. The "include" feature was added in niri version 25.11, so using this version or higher is mandatory.

Options in this file will override identical options coming _before_ and in the same way any file included _after_  will override identical niri-settings options. See [niri Documentation](https://yalter.github.io/niri/Configuration%3A-Include.html) for more details.
## Installation

#### Archlinux

An [AUR package](https://aur.archlinux.org/packages/niri-settings-git) is available:

```
yay -S niri-settings-git
```

### Dependencies:

#### Debian, derivatives
```apt
# apt -y install python3-pyqt6 qt6-wayland
```
#### Fedora
```
# dnf install python-pyqt6 qt6-wayland
```
#### openSuse
```
zypper install python-PyQt6 qt6-wayland

```
Installation as user (to `~/bin` → has to be in your `$PATH`) or systemwide:

```bash
git clone https://github.com/stefonarch/niri-settings /tmp/niri-settings
cd /tmp/niri-settings
chmod a+x install.sh
./install.sh

```
## Translations

Translations should be submitted using the [Weblate platform](https://translate.lxqt-project.org/projects/stefonarch/niri-settings/).

<a href="https://translate.lxqt-project.org/projects/stefonarch/niri-settings/">
<img src="https://translate.lxqt-project.org/widgets/stefonarch/-/niri-settings/multi-auto.svg" alt="Translation status" />
</a>

## Disclaimer

Scripts here may contain the following ingredients: LLM generated content, typos, bugs.
If you have an allergy, please be aware.

## Todo list

* Get feedback and testing.
* Improve parsing regex.
