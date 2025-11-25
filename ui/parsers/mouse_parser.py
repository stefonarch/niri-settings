import re
from .base_parser import BaseParser

class MouseParser(BaseParser):
    """Parser for mouse configuration"""
    
    def save_config(self, tab):
        """Save mouse configuration"""
        content = '    \n'
        content += '    mouse {\n'
        
        if tab.natural_scroll_checkbox.isChecked():
            content += '        natural-scroll\n'
        else:
            content += '        // natural-scroll\n'
            
        if tab.left_handed_checkbox.isChecked():
            content += '        left-handed\n'
        else:
            content += '        // left-handed\n'
            
        if tab.middle_emulation_checkbox.isChecked():
            content += '        middle-emulation\n'
        else:
            content += '        // middle-emulation\n'
        
        # Always write these settings
        content += f'        accel-speed {tab.accel_speed_spinbox.value()}\n'
        content += f'        accel-profile "{tab.accel_profile_combobox.currentText()}"\n'
        content += f'        scroll-factor {tab.scroll_factor_spinbox.value()}\n'
        
        content += '    }\n'
        
        self.write_to_file(content, 'a')
    
    def load_config(self, tab, content):
        """Load mouse configuration from content"""
        try:
            mouse_match = re.search(r'mouse\s*\{([^}]+)\}', content)
            if mouse_match:
                mouse_content = mouse_match.group(1)
                
                # Checkboxes within mouse block
                tab.natural_scroll_checkbox.setChecked(
                    'natural-scroll' in mouse_content and '// natural-scroll' not in mouse_content
                )
                tab.left_handed_checkbox.setChecked(
                    'left-handed' in mouse_content and '// left-handed' not in mouse_content
                )
                tab.middle_emulation_checkbox.setChecked(
                    'middle-emulation' in mouse_content and '// middle-emulation' not in mouse_content
                )
                
                # Mouse acceleration speed
                speed_match = re.search(r'accel-speed\s+(-?[\d.]+)', mouse_content)
                if speed_match:
                    tab.accel_speed_spinbox.setValue(float(speed_match.group(1)))
                
                # Mouse acceleration profile
                profile_match = re.search(r'accel-profile\s+"([^"]+)"', mouse_content)
                if profile_match:
                    profile_value = profile_match.group(1)
                    index = tab.accel_profile_combobox.findText(profile_value)
                    if index >= 0:
                        tab.accel_profile_combobox.setCurrentIndex(index)
                
                # Scroll factor
                scroll_match = re.search(r'scroll-factor\s+([\d.]+)', mouse_content)
                if scroll_match:
                    tab.scroll_factor_spinbox.setValue(float(scroll_match.group(1)))
        except Exception as e:
            print(f"Error parsing mouse settings: {e}")