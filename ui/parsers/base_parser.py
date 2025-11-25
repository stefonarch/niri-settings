import re
from abc import ABC, abstractmethod

class BaseParser(ABC):
    """Base class for all configuration parsers"""
    
    def __init__(self, config_path):
        self.config_path = config_path
    
    @abstractmethod
    def save_config(self, tab):
        """Save configuration for this tab"""
        pass
    
    @abstractmethod
    def load_config(self, tab, content):
        """Load configuration for this tab from content"""
        pass
    
    def read_file_content(self):
        """Read the entire config file content"""
        try:
            with open(self.config_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""
    
    def write_to_file(self, content, mode='w'):
        """Write content to config file"""
        with open(self.config_path, mode) as f:
            f.write(content)
    
    def is_setting_enabled(self, content, setting_name):
        """Check if a setting is enabled (not commented out)"""
        return setting_name in content and f'// {setting_name}' not in content
    
    def get_setting_value(self, content, setting_pattern):
        """Extract setting value using regex pattern"""
        match = re.search(setting_pattern, content)
        return match.group(1) if match else None