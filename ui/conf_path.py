import sys
import os

def get_config_path():
    """Get the configuration file path from command line or use LXQt's default"""
    if len(sys.argv) > 1:
        # Use the path provided as command line argument
        config_path = sys.argv[1]
        # Ensure the directory exists
        config_dir = os.path.dirname(config_path)
        if config_dir:  # Only create if path has a directory component
            os.makedirs(config_dir, exist_ok=True)
        return config_path
    else:
        # Fallback to default LXQt path
        default_path = os.path.join(
            os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
            'lxqt', 'wayland', 'niri', 'basicsettings.kdl'
        )
        # Ensure the directory exists
        config_dir = os.path.dirname(default_path)
        os.makedirs(config_dir, exist_ok=True)
        return default_path
