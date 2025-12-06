## niri-settings

> GUI in PyQt for configuring niri


https://github.com/user-attachments/assets/0d2b044e-59a8-4427-bf19-e672891bd53b



## Usage

Default niri configuration values are used everywhere, see `basicsettings.kdl` example file.

The line to include `basicsettings.kdl"` at the bottom of the default configuration file (for LXQt: `~/.config/lxqt/wayland/lxqt-niri.kdl`, otherwise `~/.config/niri/config.kdl`) should be added automatically when applying the first changes. The "include" feature was added in niri version 25.11, so using this version or above is mandatory.

If no argument is given `$XDG_CONFIG_HOME/lxqt/wayland/niri/basicsettings.kdl` is used when running
under LXQt, otherwise `$XDG_CONFIG_HOME/niri/basicsettings.kdl` will be used. Edit `ui/conf_path.py`
to change those defaults.

## Installation

### Arch, derivatives

Install `pyqt6` and  package:
```
# pacman -S python-pyqt6 qt6-wayland

```

### Debian, derivatives
```apt
# apt -y install python3-pyqt6 qt6-wayland
```
### Fedora
```
# dnf install python-pyqt6 qt6-wayland
```

### openSuse
```
zypper install python-PyQt6 qt6-wayland
```

Manual local installation as user:

```bash
git clone https://github.com/stefonarch/niri-settings
cd niri-settings
mkdir -p ~/.local/share/niri-settings/  ~/.local/share/applications
cp niri-settings.desktop ~/.local/share/applications/
cp -a translations/ ~/.local/share/niri-settings/
mkdir -p ~/.local/share/icons/hicolor/scalable/apps/
cp niri-settings.svg ~/.local/share/icons/hicolor/scalable/apps/niri-settings.svg

```
Run `./niri-settings-local` from a terminal inside the folder or customize `~/.local/share/applications/niri-settings.desktop` to match the path to `niri-settings/niri-settings.py`.

### Archlinux

An [AUR package](https://aur.archlinux.org/packages/niri-settings) is available.

```
yay -S niri-settings
```

## Shortcut editor

![screenshot of the niri shortcut editor](editor.png)

By default `keybinds.kdl` is used, again in relative paths both for LXQt and pure niri. It will be created and
added to the default configuration when applying changes with the "Apply" button. Existing shortcuts can be moved there. Backup your files.

## Translations

Translations should be submitted using the [Weblate platform](https://translate.lxqt-project.org/projects/stefonarch/niri-settings/).

<a href="https://translate.lxqt-project.org/projects/stefonarch/niri-settings/">
<img src="https://translate.lxqt-project.org/widgets/stefonarch/-/niri-settings/multi-auto.svg" alt="Translation status" />
</a>

## Disclaimer

Scripts here may contain the following ingredients: LLM generated content, typos, bugs.
If you have an allergy, please be aware.

## Todo list

* Get feedback and testing
* Improve parsing regex
* Add install script for local install
* Add Default column width settings, corner rounding yes|no, else ?
* Add new shortcut at position instead at the end

