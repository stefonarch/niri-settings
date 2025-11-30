import sys
import os

current_desktop = os.environ.get('XDG_CURRENT_DESKTOP', '')
desktop_list = [item.strip() for item in current_desktop.split(':')]

def get_config_path():
    """Get the configuration file path from command line, or use appropriate default"""
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        # Ensure the directory exists
        config_dir = os.path.dirname(config_path)
        if config_dir:  # Only create if path has a directory component
            os.makedirs(config_dir, exist_ok=True)
        return config_path
    else:
        if 'LXQt' in desktop_list:
            default_path = os.path.join(
                os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
                'lxqt', 'wayland', 'niri', 'basicsettings.kdl'
            )
        else:
            default_path = os.path.join(
                os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
                'niri', 'basicsettings.kdl'
            )
                    # Ensure the directory exists
        config_dir = os.path.dirname(default_path)
        os.makedirs(config_dir, exist_ok=True)
        return default_path

def get_niri_config_path():

        if 'LXQt' in desktop_list:
            default_niri_path = os.path.join(
                os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
                'lxqt', 'wayland','lxqt-niri.kdl'
            )
        else:
            default_niri_path = os.path.join(
                os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
                'niri', 'config.kdl'
            )
        config_dir = os.path.dirname(default_niri_path)
        os.makedirs(config_dir, exist_ok=True)
        return default_niri_path
