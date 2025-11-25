import re
from .base_parser import BaseParser

class TouchpadParser(BaseParser):
    """Parser for touchpad configuration"""
    
    def save_config(self, tab):
        """Save touchpad configuration"""
        content = '    \n'
        content += '    touchpad {\n'
        
        if tab.tap_checkbox.isChecked():
            content += '        tap\n'
        else:
            content += '        // tap\n'
            
        if tab.dwt_checkbox.isChecked():
            content += '        dwt\n'
        else:
            content += '        // dwt\n'
            
        if tab.natural_scroll_checkbox.isChecked():
            content += '        natural-scroll\n'
        else:
            content += '        // natural-scroll\n'
            
        if tab.drag_lock_checkbox.isChecked():
            content += '        drag-lock\n'
        else:
            content += '        // drag-lock\n'
            
        if tab.disable_external_mouse_checkbox.isChecked():
            content += '        disabled-on-external-mouse\n'
        else:
            content += '        // disabled-on-external-mouse\n'
            
        if tab.left_handed_checkbox.isChecked():
            content += '        left-handed\n'
        else:
            content += '        // left-handed\n'
        
        # Scroll method
        if tab.no_scroll_radio.isChecked():
            content += '        scroll-method "no-scroll"\n'
        elif tab.two_finger_radio.isChecked():
            content += '        scroll-method "two-finger"\n'
        elif tab.edge_radio.isChecked():
            content += '        scroll-method "edge"\n'
        elif tab.button_radio.isChecked():
            content += '        scroll-method "on-button-down"\n'
        
        # Always write these settings
        content += f'        accel-speed {tab.accel_speed_spinbox.value()}\n'
        content += f'        accel-profile "{tab.accel_profile_combobox.currentText()}"\n'
        content += f'        scroll-factor {tab.scroll_factor_spinbox.value()}\n'
        
        content += '    }\n'
        
        self.write_to_file(content, 'a')
    
    def load_config(self, tab, content):
        """Load touchpad configuration from content"""
        # Checkboxes
        tab.tap_checkbox.setChecked(
            self.is_setting_enabled(content, 'tap')
        )
        tab.dwt_checkbox.setChecked(
            self.is_setting_enabled(content, 'dwt')
        )
        tab.natural_scroll_checkbox.setChecked(
            self.is_setting_enabled(content, 'natural-scroll')
        )
        tab.drag_lock_checkbox.setChecked(
            self.is_setting_enabled(content, 'drag-lock')
        )
        tab.disable_external_mouse_checkbox.setChecked(
            self.is_setting_enabled(content, 'disabled-on-external-mouse')
        )
        tab.left_handed_checkbox.setChecked(
            self.is_setting_enabled(content, 'left-handed')
        )
        
        # Parse touchpad specific settings
        try:
            touchpad_match = re.search(r'touchpad\s*\{([^}]+)\}', content)
            if touchpad_match:
                touchpad_content = touchpad_match.group(1)
                
                # Parse acceleration speed
                speed_match = re.search(r'accel-speed\s+(-?[\d.]+)', touchpad_content)
                if speed_match:
                    tab.accel_speed_spinbox.setValue(float(speed_match.group(1)))
                
                # Parse acceleration profile
                profile_match = re.search(r'accel-profile\s+"([^"]+)"', touchpad_content)
                if profile_match:
                    profile_value = profile_match.group(1)
                    index = tab.accel_profile_combobox.findText(profile_value)
                    if index >= 0:
                        tab.accel_profile_combobox.setCurrentIndex(index)
                
                # Scroll factor
                scroll_match = re.search(r'scroll-factor\s+([\d.]+)', touchpad_content)
                if scroll_match:
                    tab.scroll_factor_spinbox.setValue(float(scroll_match.group(1)))
        except Exception as e:
            print(f"Error parsing touchpad settings: {e}")
        
        # Parse scroll method
        scroll_method = self.get_setting_value(content, r'scroll-method\s+"([^"]+)"')
        if scroll_method:
            if scroll_method == "no-scroll":
                tab.no_scroll_radio.setChecked(True)
            elif scroll_method == "two-finger":
                tab.two_finger_radio.setChecked(True)
            elif scroll_method == "edge":
                tab.edge_radio.setChecked(True)
            elif scroll_method == "on-button-down":
                tab.button_radio.setChecked(True)