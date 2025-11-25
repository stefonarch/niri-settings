import re
from .base_parser import BaseParser

class KeyboardParser(BaseParser):
    """Parser for keyboard configuration"""
    
    def save_config(self, tab):
        """Save keyboard configuration"""
        content = '    \n'
        content += '    keyboard {\n'
        content += f'        track-layout "{tab.track_layout_combobox.currentText()}"\n'
        
        if tab.numlock_checkbox.isChecked():
            content += '        numlock\n'
        else:
            content += '        // numlock\n'
            
        content += '        xkb {\n'
        content += f'           layout "{tab.layout_edit.text()}"\n'
        content += f'           variant "{tab.variant_edit.text()}"\n'
        content += f'           options "{tab.options_edit.text()}"\n'
        content += f'           model "{tab.model_edit.text()}"\n'
        content += f'           file "{tab.file_edit.text()}"\n'
        content += '        }\n'
        
        content += f'        repeat-delay {tab.repeat_delay_spinbox.value()}\n'
        content += f'        repeat-rate {tab.repeat_rate_spinbox.value()}\n'
        content += '    }\n'
        
        self.write_to_file(content, 'a')
    
    def load_config(self, tab, content):
        """Load keyboard configuration from content"""
        # Numlock
        tab.numlock_checkbox.setChecked(
            self.is_setting_enabled(content, 'numlock')
        )
        
        # Repeat settings
        repeat_delay = self.get_setting_value(content, r'repeat-delay\s+(\d+)')
        if repeat_delay:
            tab.repeat_delay_spinbox.setValue(int(repeat_delay))
            
        repeat_rate = self.get_setting_value(content, r'repeat-rate\s+(\d+)')
        if repeat_rate:
            tab.repeat_rate_spinbox.setValue(int(repeat_rate))
        
        # Track layout
        track_layout = self.get_setting_value(content, r'track-layout\s+"([^"]+)"')
        if track_layout:
            index = tab.track_layout_combobox.findText(track_layout)
            if index >= 0:
                tab.track_layout_combobox.setCurrentIndex(index)
        
        # XKB settings
        try:
            # Layout
            layout = self.get_setting_value(content, r'xkb\s*{.*?layout\s+"([^"]+)"', re.DOTALL)
            if layout:
                tab.layout_edit.setText(layout)
        except:
            pass
        
        try:
            # Variant
            variant = self.get_setting_value(content, r'xkb\s*{.*?variant\s+"([^"]+)"', re.DOTALL)
            if variant:
                tab.variant_edit.setText(variant)
        except:
            pass
        
        try:
            # Options
            options = self.get_setting_value(content, r'xkb\s*{.*?options\s+"([^"]+)"', re.DOTALL)
            if options:
                tab.options_edit.setText(options)
        except:
            pass
        
        try:
            # Model
            model = self.get_setting_value(content, r'xkb\s*{.*?model\s+"([^"]+)"', re.DOTALL)
            if model:
                tab.model_edit.setText(model)
        except:
            pass
        
        try:
            # File
            file = self.get_setting_value(content, r'xkb\s*{.*?file\s+"([^"]+)"', re.DOTALL)
            if file:
                tab.file_edit.setText(file)
        except:
            pass