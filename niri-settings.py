#!/usr/bin/env python3

import sys
import os
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QRadioButton, QLabel, QFrame,
                             QButtonGroup, QPushButton, QCheckBox, QDoubleSpinBox,
                             QComboBox, QTabWidget, QSpinBox, QLineEdit, QGroupBox, QColorDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QColor

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
            'lxqt', 'wayland', 'niri', 'input.kdl'
        )
        # Ensure the directory exists
        config_dir = os.path.dirname(default_path)
        os.makedirs(config_dir, exist_ok=True)
        return default_path

class AppearanceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    # Add the methods to your class
    def choose_active_color(self):
        """Open color dialog to choose active focus ring color"""
        color = QColorDialog.getColor(QColor(self.current_color), self, self.tr("Choose Focus Ring Color"))
        if color.isValid():
            self.current_color = color.name()
            self.update_color_button()

    def update_color_button(self):
        """Update color button background to show current color"""
        self.color_button.setStyleSheet(f"background-color: {self.current_color}; border: 1px solid gray;")


    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 10, 20, 20)

        # Appearance configuration section
        appearance_frame = QFrame()
        appearance_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        appearance_layout = QVBoxLayout(appearance_frame)

        # Appearance checkboxes
        self.csd_checkbox = QCheckBox(self.tr('Use client side decorations'))


       # Gaps
        gaps_layout = QHBoxLayout()
        gaps_label = QLabel(self.tr('Gaps:'))
        self.gaps_spinbox = QDoubleSpinBox()
        self.gaps_spinbox.setRange(0,30)
        self.gaps_spinbox.setSingleStep(1)
        self.gaps_spinbox.setValue(8)
        self.gaps_spinbox.setDecimals(1)

        gaps_layout.addWidget(gaps_label)
        gaps_layout.addWidget(self.gaps_spinbox)
        gaps_layout.addStretch()
        appearance_layout.addLayout(gaps_layout)

        # Overwiew
        gaps_layout = QHBoxLayout()
        gaps_label = QLabel(self.tr('Gaps:'))
        self.gaps_spinbox = QDoubleSpinBox()
        self.gaps_spinbox.setRange(0,30)
        self.gaps_spinbox.setSingleStep(1)
        self.gaps_spinbox.setValue(8)
        self.gaps_spinbox.setDecimals(1)

        gaps_layout.addStretch()
        appearance_layout.addLayout(gaps_layout)

                # Overwiew
        overview_layout = QHBoxLayout()
        overview_label = QLabel(self.tr('Overview zoom:'))
        self.overview_spinbox = QDoubleSpinBox()
        self.overview_spinbox.setRange(0.1,1.0)
        self.overview_spinbox.setSingleStep(0.05)
        self.overview_spinbox.setValue(0.4)
        self.overview_spinbox.setDecimals(2)

        overview_layout.addWidget(overview_label)
        overview_layout.addWidget(self.overview_spinbox)
        overview_layout.addStretch()
        appearance_layout.addLayout(overview_layout)


        # Focus Ring
        focus_group = QGroupBox(self.tr("Focus ring"))
        focus_layout = QVBoxLayout(focus_group)

        # Enabled checkbox
        self.focus_ring_enabled = QCheckBox(self.tr('Enabled'))
        self.focus_ring_enabled.setChecked(True)
        focus_layout.addWidget(self.focus_ring_enabled)

        # Border width
        border_layout = QHBoxLayout()
        border_label = QLabel(self.tr('Width:'))
        self.border_spinbox = QSpinBox()
        self.border_spinbox.setRange(0, 10)
        self.border_spinbox.setValue(2)
        border_layout.addWidget(border_label)
        border_layout.addWidget(self.border_spinbox)
        border_layout.addStretch()
        focus_layout.addLayout(border_layout)

        # Active color selector
        color_layout = QHBoxLayout()
        color_label = QLabel(self.tr('Color:'))
        self.color_button = QPushButton()
        self.color_button.setFixedSize(60, 25)
        self.color_button.clicked.connect(self.choose_active_color)
        self.current_color = "#3584e4"  # Default color
        self.update_color_button()
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        color_layout.addStretch()
        focus_layout.addLayout(color_layout)

        # Border
        border_group = QGroupBox(self.tr("Border"))
        borderb_layout = QVBoxLayout(border_group)

        # Enabled checkbox
        self.borderb_enabled = QCheckBox(self.tr('Enabled'))
        self.borderb_enabled.setChecked(True)
        borderb_layout.addWidget(self.borderb_enabled)

        # Border's border width
        border2_layout = QHBoxLayout()
        border2_label = QLabel(self.tr('Width:'))
        self.border2_spinbox = QSpinBox()
        self.border2_spinbox.setRange(0, 10)
        self.border2_spinbox.setValue(2)
        border2_layout.addWidget(border2_label)
        border2_layout.addWidget(self.border2_spinbox)
        border2_layout.addStretch()
        borderb_layout.addLayout(border2_layout)

        # Active border color selector
        bordercolor_layout = QHBoxLayout()
        bordercolor_label = QLabel(self.tr('Color:'))
        self.bordercolor_button = QPushButton()
        self.bordercolor_button.setFixedSize(60, 25)
        self.bordercolor_button.clicked.connect(self.choose_active_color)
        self.current_bordercolor = "#3584e4"  # Default color
        self.update_color_button()
        bordercolor_layout.addWidget(bordercolor_label)
        bordercolor_layout.addWidget(self.bordercolor_button)
        bordercolor_layout.addStretch()
        borderb_layout.addLayout(bordercolor_layout)

        appearance_layout.addWidget(self.csd_checkbox)

        layout.addWidget(appearance_frame)
        layout.addWidget(focus_group)
        layout.addWidget(border_group)
        layout.addStretch()


class BehaviorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 10, 20, 20)

        # Behavior configuration section
        behavior_frame = QFrame()
        behavior_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        behavior_layout = QVBoxLayout(behavior_frame)

        # Behavior checkboxes
        self.hotkey_overlay_checkbox = QCheckBox(self.tr('Show shortcuts at login'))
        self.warp_mouse_to_focus_checkbox = QCheckBox(self.tr('Warp mouse to focus'))
        self.focus_follows_mouse_checkbox = QCheckBox(self.tr('Focus follows mouse'))
        self.focus_request_checkbox = QCheckBox(self.tr('Always focus windows on request'))
        self.disable_power_key_checkbox = QCheckBox(self.tr('Disable power key handling'))
        self.workspace_auto_back_forth_checkbox = QCheckBox(self.tr('Workspace auto back and forth'))
        self.hot_corners_checkbox = QCheckBox(self.tr('Disable hot corners'))
        self.hide_while_typing_checkbox = QCheckBox(self.tr('Hide cursor while typing'))

        behavior_layout.addWidget(self.hotkey_overlay_checkbox)
        behavior_layout.addWidget(self.focus_request_checkbox)
        behavior_layout.addWidget(self.disable_power_key_checkbox)
        behavior_layout.addWidget(self.workspace_auto_back_forth_checkbox)
        behavior_layout.addWidget(self.hot_corners_checkbox)

        # Mod key
        behavior_layout.addSpacing(10)
        mod_key_label = QLabel(self.tr('Mod Key:'))
        behavior_layout.addWidget(mod_key_label)

        self.mod_key_group = QButtonGroup(self)
        self.super_radio = QRadioButton(self.tr('Super'))
        self.alt_radio = QRadioButton(self.tr('Alt'))
        self.ctrl_radio = QRadioButton(self.tr('Ctrl'))
        self.super_radio.setChecked(True)

        self.mod_key_group.addButton(self.super_radio)
        self.mod_key_group.addButton(self.alt_radio)
        self.mod_key_group.addButton(self.ctrl_radio)

        mod_key_radio_layout = QHBoxLayout()
        mod_key_radio_layout.addWidget(self.super_radio)
        mod_key_radio_layout.addWidget(self.alt_radio)
        mod_key_radio_layout.addWidget(self.ctrl_radio)
        mod_key_radio_layout.addStretch()

        behavior_layout.addLayout(mod_key_radio_layout)

        # screenshot_path
        screenshot_path_layout = QHBoxLayout()
        behavior_layout.addSpacing(10)
        screenshot_path_label = QLabel(self.tr('Screenshots:'))
        self.screenshot_path_edit = QLineEdit()
        self.screenshot_path_edit.setPlaceholderText("~/Pictures/Screenshot %Y-%m-%d %H-%M-%S.png")
        self.screenshot_path_edit.setMinimumWidth(400)
        self.screenshot_path_edit.setClearButtonEnabled(True)

        screenshot_path_layout.addWidget(screenshot_path_label)
        screenshot_path_layout.addSpacing(34)
        screenshot_path_layout.addWidget(self.screenshot_path_edit)
        screenshot_path_layout.addStretch()
        behavior_layout.addLayout(screenshot_path_layout)

        # Cursor
        cursor_group = QGroupBox(self.tr("Cursor"))
        cursor_layout = QVBoxLayout(cursor_group)
        self.inactive_enable_checkbox = QCheckBox(self.tr("Enable"))

        # inactive block
        inactive_layout = QHBoxLayout()
        inactive_label = QLabel(self.tr('hiding after inactive for:'))
        self.inactive_spinbox = QSpinBox()
        self.inactive_spinbox.setRange(500, 99999)
        self.inactive_spinbox.setValue(3000)
        self.inactive_spinbox.setSingleStep(250)


        inactive_layout.addWidget(self.inactive_enable_checkbox)
        inactive_layout.addWidget(inactive_label)
        inactive_layout.addWidget(self.inactive_spinbox)
        inactive_layout.addStretch()
        self.inactive_enable_checkbox.toggled.connect(
        self.inactive_spinbox.setEnabled
        )


        cursor_layout.addWidget(self.focus_follows_mouse_checkbox)
        cursor_layout.addWidget(self.warp_mouse_to_focus_checkbox)
        cursor_layout.addWidget(self.hide_while_typing_checkbox)
        cursor_layout.addLayout(inactive_layout)


        layout.addWidget(behavior_frame)
        layout.addWidget(cursor_group)

        layout.addStretch()




class TouchpadTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 10, 20, 20)

        # Touchpad configuration section
        touchpad_frame = QFrame()
        touchpad_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        touchpad_layout = QVBoxLayout(touchpad_frame)

        # Touchpad checkboxes
        self.tap_checkbox = QCheckBox(self.tr('Tap to click'))
        self.natural_scroll_checkbox = QCheckBox(self.tr('Natural scroll'))
        self.drag_lock_checkbox = QCheckBox(self.tr('Drag lock'))
        self.disable_external_mouse_checkbox = QCheckBox(self.tr('Disable when external mouse connected'))
        self.dwt_checkbox = QCheckBox(self.tr('Disable while typing'))
        self.left_handed_checkbox = QCheckBox(self.tr('Left handed'))

        touchpad_layout.addWidget(self.tap_checkbox)
        touchpad_layout.addWidget(self.natural_scroll_checkbox)
        touchpad_layout.addWidget(self.drag_lock_checkbox)
        touchpad_layout.addWidget(self.disable_external_mouse_checkbox)
        touchpad_layout.addWidget(self.dwt_checkbox)
        touchpad_layout.addWidget(self.left_handed_checkbox)

        # Scroll method selection
        touchpad_layout.addSpacing(10)
        scroll_label = QLabel(self.tr('Scroll method:'))
        scroll_label.setContentsMargins(0, 10, 0, 0)
        touchpad_layout.addWidget(scroll_label)

        self.scroll_group = QButtonGroup(self)
        self.no_scroll_radio = QRadioButton(self.tr('No scroll'))
        self.two_finger_radio = QRadioButton(self.tr('Two finger'))
        self.edge_radio = QRadioButton(self.tr('Edge'))
        self.button_radio = QRadioButton(self.tr('Button'))

        self.scroll_group.addButton(self.no_scroll_radio)
        self.scroll_group.addButton(self.two_finger_radio)
        self.scroll_group.addButton(self.edge_radio)
        self.scroll_group.addButton(self.button_radio)
        self.two_finger_radio.setChecked(True)

        touchpad_layout.addWidget(self.no_scroll_radio)
        touchpad_layout.addWidget(self.two_finger_radio)
        touchpad_layout.addWidget(self.edge_radio)
        touchpad_layout.addWidget(self.button_radio)

        # Acceleration speed
        accel_speed_layout = QHBoxLayout()
        accel_speed_label = QLabel(self.tr('Acceleration speed:'))
        self.accel_speed_spinbox = QDoubleSpinBox()
        self.accel_speed_spinbox.setRange(-1.0, 1.0)
        self.accel_speed_spinbox.setSingleStep(0.1)
        self.accel_speed_spinbox.setValue(0.2)
        self.accel_speed_spinbox.setDecimals(1)

        accel_speed_layout.addWidget(accel_speed_label)
        accel_speed_layout.addWidget(self.accel_speed_spinbox)
        accel_speed_layout.addStretch()
        touchpad_layout.addLayout(accel_speed_layout)

        # Acceleration profile
        accel_profile_layout = QHBoxLayout()
        accel_profile_label = QLabel(self.tr('Acceleration profile:'))
        self.accel_profile_combobox = QComboBox()
        self.accel_profile_combobox.addItems(["adaptive", "flat"])

        accel_profile_layout.addWidget(accel_profile_label)
        accel_profile_layout.addWidget(self.accel_profile_combobox)
        accel_profile_layout.addStretch()
        touchpad_layout.addLayout(accel_profile_layout)

        # Scroll factor
        scroll_factor_layout = QHBoxLayout()
        scroll_factor_label = QLabel(self.tr('Scroll factor:'))
        self.scroll_factor_spinbox = QDoubleSpinBox()
        self.scroll_factor_spinbox.setRange(0.1, 3.0)
        self.scroll_factor_spinbox.setSingleStep(0.1)
        self.scroll_factor_spinbox.setValue(1.0)
        self.scroll_factor_spinbox.setDecimals(1)

        scroll_factor_layout.addWidget(scroll_factor_label)
        scroll_factor_layout.addWidget(self.scroll_factor_spinbox)
        scroll_factor_layout.addStretch()
        touchpad_layout.addLayout(scroll_factor_layout)

        layout.addWidget(touchpad_frame)
        layout.addStretch()

        # Tab button_map method selection
        touchpad_layout.addSpacing(10)
        button_map_label = QLabel(self.tr('Tap Button Map:'))
        button_map_label.setContentsMargins(0, 10, 0, 0)
        touchpad_layout.addWidget(button_map_label)

        self.button_map_group = QButtonGroup(self)
        self.lmr_radio = QRadioButton(self.tr('left-middle-right'))
        self.lrm_radio = QRadioButton(self.tr('left-right-middle'))


        self.button_map_group.addButton(self.lmr_radio)
        self.button_map_group.addButton(self.lrm_radio)

        self.lmr_radio.setChecked(True)

        touchpad_layout.addWidget(self.lmr_radio)
        touchpad_layout.addWidget(self.lrm_radio)

class MouseTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 10, 20, 20)

        # Mouse configuration section
        mouse_frame = QFrame()
        mouse_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        mouse_layout = QVBoxLayout(mouse_frame)

        # Mouse checkboxes
        self.natural_scroll_checkbox = QCheckBox(self.tr('Natural scroll'))
        self.left_handed_checkbox = QCheckBox(self.tr('Left handed'))
        self.middle_emulation_checkbox = QCheckBox(self.tr('Middle button emulation'))

        mouse_layout.addWidget(self.natural_scroll_checkbox)
        mouse_layout.addWidget(self.left_handed_checkbox)
        mouse_layout.addWidget(self.middle_emulation_checkbox)

        # Acceleration speed
        accel_speed_layout = QHBoxLayout()
        accel_speed_label = QLabel(self.tr('Acceleration speed:'))
        self.accel_speed_spinbox = QDoubleSpinBox()
        self.accel_speed_spinbox.setRange(-1.0, 1.0)
        self.accel_speed_spinbox.setSingleStep(0.1)
        self.accel_speed_spinbox.setValue(0.2)
        self.accel_speed_spinbox.setDecimals(1)

        accel_speed_layout.addWidget(accel_speed_label)
        accel_speed_layout.addWidget(self.accel_speed_spinbox)
        accel_speed_layout.addStretch()
        mouse_layout.addLayout(accel_speed_layout)

        # Acceleration profile
        accel_profile_layout = QHBoxLayout()
        accel_profile_label = QLabel(self.tr('Acceleration profile:'))
        self.accel_profile_combobox = QComboBox()
        self.accel_profile_combobox.addItems(["adaptive","flat"])

        accel_profile_layout.addWidget(accel_profile_label)
        accel_profile_layout.addWidget(self.accel_profile_combobox)
        accel_profile_layout.addStretch()
        mouse_layout.addLayout(accel_profile_layout)

        # Scroll factor
        scroll_factor_layout = QHBoxLayout()
        scroll_factor_label = QLabel(self.tr('Scroll factor:'))
        self.scroll_factor_spinbox = QDoubleSpinBox()
        self.scroll_factor_spinbox.setRange(0.1, 3.0)
        self.scroll_factor_spinbox.setSingleStep(0.1)
        self.scroll_factor_spinbox.setValue(1.0)
        self.scroll_factor_spinbox.setDecimals(1)

        scroll_factor_layout.addWidget(scroll_factor_label)
        scroll_factor_layout.addWidget(self.scroll_factor_spinbox)
        scroll_factor_layout.addStretch()
        mouse_layout.addLayout(scroll_factor_layout)

        layout.addWidget(mouse_frame)
        layout.addStretch()


class KeyboardTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 10, 20, 20)

        # Keyboard configuration section
        keyboard_frame = QFrame()
        keyboard_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        keyboard_layout = QVBoxLayout(keyboard_frame)

        # Numlock checkbox
        self.numlock_checkbox = QCheckBox(self.tr('Enable num lock at startup'))
        keyboard_layout.addWidget(self.numlock_checkbox)

        # Track layout
        track_layout_layout = QHBoxLayout()
        track_layout_label = QLabel(self.tr('Track keyboard layout:'))
        self.track_layout_combobox = QComboBox()
        self.track_layout_combobox.addItems(["window", "global"])

        track_layout_layout.addWidget(track_layout_label)
        track_layout_layout.addWidget(self.track_layout_combobox)
        track_layout_layout.addStretch()
        keyboard_layout.addLayout(track_layout_layout)

        # XKB Settings Group
        xkb_group = QGroupBox(self.tr("XKB Settings"))
        xkb_layout = QVBoxLayout(xkb_group)

        # Layout
        layout_layout = QHBoxLayout()
        layout_label = QLabel(self.tr('Layout:'))
        self.layout_edit = QLineEdit()
        self.layout_edit.setPlaceholderText("e.g. us,ru,de")
        self.layout_edit.setMaximumWidth(120)
        self.layout_edit.setClearButtonEnabled(True)

        layout_layout.addWidget(layout_label)
        layout_layout.addSpacing(5)
        layout_layout.addWidget(self.layout_edit)
        layout_layout.addStretch()
        layout_layout.addSpacing(10)
        xkb_layout.addLayout(layout_layout)

        # Variant
        variant_layout = QHBoxLayout()
        variant_label = QLabel(self.tr('Variant:'))
        self.variant_edit = QLineEdit()
        self.variant_edit.setPlaceholderText("e.g., colemak_dh_ortho")
        self.variant_edit.setMinimumWidth(300)
        self.variant_edit.setClearButtonEnabled(True)

        variant_layout.addWidget(variant_label)
        variant_layout.addSpacing(5)
        variant_layout.addWidget(self.variant_edit)
        variant_layout.addStretch()
        xkb_layout.addLayout(variant_layout)

        # Options
        options_layout = QHBoxLayout()
        options_label = QLabel(self.tr('Options:'))
        self.options_edit = QLineEdit()
        self.options_edit.setText("grp:alt_shift_toggle,compose:rctrl")
        self.options_edit.setMinimumWidth(400)
        self.options_edit.setClearButtonEnabled(True)

        options_layout.addWidget(options_label)
        options_layout.addWidget(self.options_edit)
        options_layout.addStretch()
        xkb_layout.addLayout(options_layout)

        # Model
        model_layout = QHBoxLayout()
        model_label = QLabel(self.tr('Model:'))
        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText("e.g., pc_105")
        self.model_edit.setMinimumWidth(200)
        self.model_edit.setClearButtonEnabled(True)

        model_layout.addWidget(model_label)
        model_layout.addSpacing(14)
        model_layout.addWidget(self.model_edit)
        model_layout.addStretch()
        xkb_layout.addLayout(model_layout)

        # file
        file_layout = QHBoxLayout()
        file_label = QLabel(self.tr('File:'))
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("e.g., ~/.config/keymap.xkb")
        self.file_edit.setMinimumWidth(400)
        self.file_edit.setClearButtonEnabled(True)

        file_layout.addWidget(file_label)
        file_layout.addSpacing(34)
        file_layout.addWidget(self.file_edit)
        file_layout.addStretch()
        xkb_layout.addLayout(file_layout)

        keyboard_layout.addWidget(xkb_group)

        # Repeat settings
        repeat_group = QGroupBox(self.tr("Repeat Settings"))
        repeat_layout = QVBoxLayout(repeat_group)

        # Repeat delay
        repeat_delay_layout = QHBoxLayout()
        repeat_delay_label = QLabel(self.tr('Repeat delay:'))
        self.repeat_delay_spinbox = QSpinBox()
        self.repeat_delay_spinbox.setRange(100, 2000)
        self.repeat_delay_spinbox.setSingleStep(100)
        self.repeat_delay_spinbox.setValue(600)
        self.repeat_delay_spinbox.setSuffix(' ms')

        repeat_delay_layout.addWidget(repeat_delay_label)
        repeat_delay_layout.addWidget(self.repeat_delay_spinbox)
        repeat_delay_layout.addStretch()
        repeat_layout.addLayout(repeat_delay_layout)

        # Repeat rate
        repeat_rate_layout = QHBoxLayout()
        repeat_rate_label = QLabel(self.tr('Repeat rate:'))
        self.repeat_rate_spinbox = QSpinBox()
        self.repeat_rate_spinbox.setRange(1, 100)
        self.repeat_rate_spinbox.setValue(25)

        repeat_rate_layout.addWidget(repeat_rate_label)
        repeat_rate_layout.addWidget(self.repeat_rate_spinbox)
        repeat_rate_layout.addStretch()
        repeat_layout.addLayout(repeat_rate_layout)

        keyboard_layout.addWidget(repeat_group)

        layout.addWidget(keyboard_frame)
        layout.addStretch()

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_path = get_config_path()
        self.init_ui()
        self.load_settings()

    def open_wiki(self):
        import webbrowser
        wiki_url = "https://yalter.github.io/niri/Configuration%3A-Input"
        webbrowser.open(wiki_url)

    def init_ui(self):
        self.setWindowTitle('Niri Settings')
        self.setFixedSize(600, 750)

  # Try to use system theme icon first, fallback to Qt standard icon
        icon = QIcon.fromTheme("preferences-desktop-peripherals")
        if icon.isNull():
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        self.setWindowIcon(icon)


        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Create tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.appearance_tab = AppearanceTab(self)
        self.behavior_tab = BehaviorTab(self)
        self.touchpad_tab = TouchpadTab(self)
        self.mouse_tab = MouseTab(self)
        self.keyboard_tab = KeyboardTab(self)

        self.tabs.addTab(self.appearance_tab, self.tr("Appearance"))
        self.tabs.addTab(self.behavior_tab, self.tr("Behavior"))
        self.tabs.addTab(self.touchpad_tab, self.tr("Touchpad"))
        self.tabs.addTab(self.mouse_tab, self.tr("Mouse"))
        self.tabs.addTab(self.keyboard_tab, self.tr("Keyboard"))

        main_layout.addWidget(self.tabs)

        # Button layout
        button_layout = QHBoxLayout()

        wiki_btn = QPushButton(self.tr('Wiki'))
        wiki_btn.setFixedSize(80, 35)
        wiki_btn.clicked.connect(self.open_wiki)

        apply_btn = QPushButton(self.tr('Apply'))
        apply_btn.setFixedSize(120, 35)
        apply_btn.clicked.connect(self.apply_settings)

        close_btn = QPushButton(self.tr('Close'))
        close_btn.setFixedSize(120, 35)
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(wiki_btn)
        button_layout.addStretch()
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(close_btn)

        main_layout.addLayout(button_layout)

    def apply_settings(self):
        """Save settings to input.kdl in KDL format"""
        self.save_behavior_config()
        self.save_touchpad_config()
        self.save_mouse_config()
        self.save_keyboard_config()
        print(f"Settings applied to {self.config_path}.")

    def save_behavior_config(self):
        """Save behavior configuration to input.kdl in KDL format"""
        with open(self.config_path, 'w') as f:
            f.write('// Generated by niri-settings - Edits will be overwritten!\n\n')
            f.write('input {\n')
            if self.behavior_tab.warp_mouse_to_focus_checkbox.isChecked():
                f.write('    warp-mouse-to-focus\n')
            else:
                f.write('    // warp-mouse-to-focus\n')
            if self.behavior_tab.focus_follows_mouse_checkbox.isChecked():
                f.write('    focus-follows-mouse\n')
            else:
                f.write('    // focus-follows-mouse\n')
            if self.behavior_tab.disable_power_key_checkbox.isChecked():
                f.write('    disable-power-key-handling\n')
            else:
                f.write('    // disable-power-key-handling\n')
            if self.behavior_tab.workspace_auto_back_forth_checkbox.isChecked():
                f.write('    workspace-auto-back-and-forth\n')
            else:
                f.write('    // workspace-auto-back-and-forth\n')
            if self.behavior_tab.super_radio.isChecked():
                f.write('    mod-key "Super"\n')
            elif self.behavior_tab.alt_radio.isChecked():
                f.write('    mod-key "Alt"\n')
            elif self.behavior_tab.ctrl_radio.isChecked():
                f.write('    mod-key "Ctrl"\n')

    def save_touchpad_config(self):
        try:
            with open(self.config_path, 'a') as f:  # Append to the file
                f.write('    \n')
                f.write('    touchpad {\n')

                if self.touchpad_tab.tap_checkbox.isChecked():
                    f.write('        tap\n')
                else:
                    f.write('        // tap\n')
                if self.touchpad_tab.dwt_checkbox.isChecked():
                    f.write('        dwt\n')
                else:
                    f.write('        // dwt\n')
                if self.touchpad_tab.natural_scroll_checkbox.isChecked():
                    f.write('        natural-scroll\n')
                else:
                    f.write('        // natural-scroll\n')
                if self.touchpad_tab.drag_lock_checkbox.isChecked():
                    f.write('        drag-lock\n')
                else:
                    f.write('        // drag-lock\n')
                if self.touchpad_tab.disable_external_mouse_checkbox.isChecked():
                    f.write('        disabled-on-external-mouse\n')
                else:
                    f.write('        // disabled-on-external-mouse\n')
                if self.touchpad_tab.left_handed_checkbox.isChecked():
                    f.write('        left-handed\n')
                else:
                    f.write('        // left-handed\n')

                if self.touchpad_tab.no_scroll_radio.isChecked():
                    f.write('        scroll-method "no-scroll"\n')
                elif self.touchpad_tab.two_finger_radio.isChecked():
                    f.write('        scroll-method "two-finger"\n')
                elif self.touchpad_tab.edge_radio.isChecked():
                    f.write('        scroll-method "edge"\n')
                elif self.touchpad_tab.button_radio.isChecked():
                    f.write('        scroll-method "on-button-down"\n')

                # Always write those settings
                f.write(f'        accel-speed {self.touchpad_tab.accel_speed_spinbox.value()}\n')
                f.write(f'        accel-profile "{self.touchpad_tab.accel_profile_combobox.currentText()}"\n')
                f.write(f'        scroll-factor {self.touchpad_tab.scroll_factor_spinbox.value()}\n')
                f.write('    }\n')

        except Exception as e:
            print(f"Error saving touchpad configuration: {e}")

    def save_mouse_config(self):
        try:
            with open(self.config_path, 'a') as f:  # Append to the file
                f.write('    \n')
                f.write('    mouse {\n')
                if self.mouse_tab.natural_scroll_checkbox.isChecked():
                    f.write('        natural-scroll\n')
                else:
                    f.write('        // natural-scroll\n')
                if self.mouse_tab.left_handed_checkbox.isChecked():
                    f.write('        left-handed\n')
                else:
                    f.write('        // left-handed\n')
                if self.mouse_tab.middle_emulation_checkbox.isChecked():
                    f.write('        middle-emulation\n')
                else:
                    f.write('        // middle-emulation\n')

                # Always write those settings
                f.write(f'        accel-speed {self.mouse_tab.accel_speed_spinbox.value()}\n')
                f.write(f'        accel-profile "{self.mouse_tab.accel_profile_combobox.currentText()}"\n')
                f.write(f'        scroll-factor {self.mouse_tab.scroll_factor_spinbox.value()}\n')

                f.write('    }\n')

        except Exception as e:
            print(f"Error saving mouse configuration: {e}")

    def save_keyboard_config(self):
        """Save keyboard configuration to input.kdl in KDL format"""
        with open(self.config_path, 'a') as f:  # Append to the file
            f.write('    \n')
            f.write('    keyboard {\n')
            f.write(f'        track-layout "{self.keyboard_tab.track_layout_combobox.currentText()}"\n')
            if self.keyboard_tab.numlock_checkbox.isChecked():
                f.write('        numlock\n')
            else:
                f.write('        // numlock\n')
            f.write('        xkb {\n')
            f.write(f'           layout "{self.keyboard_tab.layout_edit.text()}"\n')
            f.write(f'           variant "{self.keyboard_tab.variant_edit.text()}"\n')
            f.write(f'           options "{self.keyboard_tab.options_edit.text()}"\n')
            f.write(f'           model "{self.keyboard_tab.model_edit.text()}"\n')
            f.write(f'           file "{self.keyboard_tab.file_edit.text()}"\n')
            f.write('        }\n')

            f.write(f'        repeat-delay {self.keyboard_tab.repeat_delay_spinbox.value()}\n')
            f.write(f'        repeat-rate {self.keyboard_tab.repeat_rate_spinbox.value()}\n')

            f.write('    }\n')
            f.write('}\n\n')

            # Behavior Tab: Hot Key Overlay
            f.write('hotkey-overlay {\n    hide-not-bound\n')
            if self.behavior_tab.hotkey_overlay_checkbox.isChecked():
                f.write('    // skip-at-startup\n')
            else:
                f.write('    skip-at-startup\n')
            f.write('    }\n\n')

            # Gestures
            f.write('gestures {\n')
            f.write('    hot-corners {\n')
            if self.behavior_tab.hot_corners_checkbox.isChecked():
                f.write('        off\n')
            else:
                f.write('        // off\n')
            f.write('    }\n}\n\n')

            # Debug
            f.write('debug {\n')
            if self.behavior_tab.focus_request_checkbox.isChecked():
                f.write('    honor-xdg-activation-with-invalid-serial \n')
            else:
                    f.write('    // honor-xdg-activation-with-invalid-serial \n')
            f.write('}\n')

            # Cursor
            f.write('cursor {\n')
            if self.behavior_tab.hide_while_typing_checkbox.isChecked():
                f.write('    hide-when-typing \n')
            else:
                f.write('    // hide-when-typing \n')
            if self.behavior_tab.inactive_enable_checkbox.isChecked():
                f.write(f'    hide-after-inactive-ms {self.behavior_tab.inactive_spinbox.value()}\n')
            else:
                f.write('    // hide-after-inactive-ms {self.behavior_tab.inactive_spinbox.value()}\n')

            f.write('}\n')

            # Screenshot path
            path = self.behavior_tab.screenshot_path_edit.text()
            if path:
                f.write(f'\nscreenshot-path "{path}"\n')

    def load_settings(self):
        """Load existing settings from input.kdl"""
        import re

        try:
            with open(self.config_path, 'r') as f:
                content = f.read()

            # Parse behavior settings
            self.behavior_tab.warp_mouse_to_focus_checkbox.setChecked(
                '// warp-mouse-to-focus' not in content
            )
            self.behavior_tab.focus_follows_mouse_checkbox.setChecked(
                '// focus-follows-mouse' not in content
            )
            self.behavior_tab.disable_power_key_checkbox.setChecked(
                '// disable-power-key-handling' not in content
            )
            self.behavior_tab.workspace_auto_back_forth_checkbox.setChecked(
                '// workspace-auto-back-and-forth' not in content
            )

            self.behavior_tab.hotkey_overlay_checkbox.setChecked(
                '// skip-at-startup' in content
            )

            self.behavior_tab.focus_request_checkbox.setChecked(
                '// honor-xdg-activation-with-invalid-serial ' not in content
            )

            self.behavior_tab.hide_while_typing_checkbox.setChecked(
                '// hide-when-typing ' not in content
            )
            self.behavior_tab.inactive_enable_checkbox.setChecked(
                '// hide-after-inactive-ms' not in content
            )

            value = re.search(r'hide-after-inactive-ms\s+(\d+)', content)
            if value:
                self.behavior_tab.inactive_spinbox.setValue(int(value.group(1)))

            match = re.search(r'gestures\s*\{\s*hot-corners\s*\{[^}]*//[^}]*\}\s*\}', content)
            if match:
                self.behavior_tab.hot_corners_checkbox.setChecked(False)
            else:
                self.behavior_tab.hot_corners_checkbox.setChecked(True)

            path = re.search(r'screenshot-path\s+"([^"]+)"', content)
            if path:
                self.behavior_tab.screenshot_path_edit.setText(path.group(1))

            # Parse mod key with radio buttons
            try:
                match = re.search(r'mod-key\s+"([^"]+)"', content)
                if match:
                    mod_key = match.group(1)
                    if mod_key == "Super":
                        self.behavior_tab.super_radio.setChecked(True)
                    elif mod_key == "Alt":
                        self.behavior_tab.alt_radio.setChecked(True)
                    elif mod_key == "Ctrl":
                        self.behavior_tab.ctrl_radio.setChecked(True)
            except Exception as e:
                print(f"Error parsing mod-key: {e}")

            # Touchpad settings
            self.touchpad_tab.tap_checkbox.setChecked(
                'tap' in content and '// tap' not in content
            )
            self.touchpad_tab.dwt_checkbox.setChecked(
                'dwt' in content and '// dwt' not in content
            )
            self.touchpad_tab.natural_scroll_checkbox.setChecked(
                'natural-scroll' in content and '// natural-scroll' not in content
            )
            self.touchpad_tab.drag_lock_checkbox.setChecked(
                'drag-lock' in content and '// drag-lock' not in content
            )
            self.touchpad_tab.disable_external_mouse_checkbox.setChecked(
                'disabled-on-external-mouse' in content and '// disabled-on-external-mouse' not in content
            )
            self.touchpad_tab.left_handed_checkbox.setChecked(
                'left-handed' in content and '// left-handed' not in content
            )
            try:
                # Touchpad acceleration speed and profile
                touchpad_match = re.search(r'touchpad\s*\{([^}]+)\}', content)
                if touchpad_match:
                    touchpad_content = touchpad_match.group(1)

                    # Parse acceleration speed
                    speed_match = re.search(r'accel-speed\s+(-?[\d.]+)', touchpad_content)
                    if speed_match:
                        self.touchpad_tab.accel_speed_spinbox.setValue(float(speed_match.group(1)))

                    # Parse acceleration profile
                    profile_match = re.search(r'accel-profile\s+"([^"]+)"', touchpad_content)
                    if profile_match:
                        profile_value = profile_match.group(1)
                        # Assuming you have a QComboBox for accel profile
                        index = self.touchpad_tab.accel_profile_combobox.findText(profile_value)
                        if index >= 0:
                            self.touchpad_tab.accel_profile_combobox.setCurrentIndex(index)

                    # Scroll factor
                    scroll_match = re.search(r'scroll-factor\s+([\d.]+)', touchpad_content)
                    if scroll_match:
                        self.touchpad_tab.scroll_factor_spinbox.setValue(float(scroll_match.group(1)))
            except:
                pass

                # Parse scroll method with radio buttons
            match = re.search(r'scroll-method\s+"([^"]+)"', content)
            if match:
                scroll_method = match.group(1)
                if scroll_method == "no-scroll":
                    self.touchpad_tab.no_scroll_radio.setChecked(True)
                elif scroll_method == "two-finger":
                    self.touchpad_tab.two_finger_radio.setChecked(True)
                elif scroll_method == "edge":
                    self.touchpad_tab.edge_radio.setChecked(True)
                elif scroll_method == "on-button-down":
                    self.touchpad_tab.button_radio.setChecked(True)

            # Mouse settings
            try:
                mouse_match = re.search(r'mouse\s*\{([^}]+)\}', content)
                if mouse_match:
                    mouse_content = mouse_match.group(1)

                    # Checkboxes within mouse block
                    self.mouse_tab.natural_scroll_checkbox.setChecked(
                        'natural-scroll' in mouse_content and '// natural-scroll' not in mouse_content
                    )
                    self.mouse_tab.left_handed_checkbox.setChecked(
                        'left-handed' in mouse_content and '// left-handed' not in mouse_content
                    )
                    self.mouse_tab.middle_emulation_checkbox.setChecked(
                        'middle-emulation' in mouse_content and '// middle-emulation' not in mouse_content
                    )

                    # Mouse acceleration speed
                    speed_match = re.search(r'accel-speed\s+(-?[\d.]+)', mouse_content)
                    if speed_match:
                        self.mouse_tab.accel_speed_spinbox.setValue(float(speed_match.group(1)))

                    # Mouse acceleration profile
                    profile_match = re.search(r'accel-profile\s+"([^"]+)"', mouse_content)
                    if profile_match:
                        profile_value = profile_match.group(1)
                        index = self.mouse_tab.accel_profile_combobox.findText(profile_value)
                        if index >= 0:
                            self.mouse_tab.accel_profile_combobox.setCurrentIndex(index)

                    # Scroll factor
                    scroll_match = re.search(r'scroll-factor\s+([\d.]+)', mouse_content)
                    if scroll_match:
                        self.mouse_tab.scroll_factor_spinbox.setValue(float(scroll_match.group(1)))
            except:
                pass

            # Keyboard settings
            self.keyboard_tab.numlock_checkbox.setChecked(
                'numlock' in content and '// numlock' not in content
            )

            match = re.search(r'repeat-delay\s+(\d+)', content)
            if match:
                self.keyboard_tab.repeat_delay_spinbox.setValue(int(match.group(1)))

            match = re.search(r'repeat-rate\s+(\d+)', content)
            if match:
                self.keyboard_tab.repeat_rate_spinbox.setValue(int(match.group(1)))

            # Track layout
            match = re.search(r'track-layout\s+"([^"]+)"', content)
            if match:
                track_layout = match.group(1)
                index = self.keyboard_tab.track_layout_combobox.findText(track_layout)
                if index >= 0:
                        self.keyboard_tab.track_layout_combobox.setCurrentIndex(index)

            try:
                # XKB layout
                xkb_match = re.search(r'xkb\s*{.*?layout\s+"([^"]+)"', content, re.DOTALL)
                if xkb_match:
                    self.keyboard_tab.layout_edit.setText(xkb_match.group(1))
            except:
                pass

            try:
                # XKB Variant
                variant_match = re.search(r'xkb\s*{.*?variant\s+"([^"]+)"', content, re.DOTALL)
                if variant_match:
                    self.keyboard_tab.variant_edit.setText(variant_match.group(1))
            except:
                pass

            try:
                # XKB options
                options_match = re.search(r'xkb\s*{.*?options\s+"([^"]+)"', content, re.DOTALL)
                if options_match:
                    self.keyboard_tab.options_edit.setText(options_match.group(1))
            except:
                pass

            try:
                # XKB model
                model_match = re.search(r'xkb\s*{.*?model\s+"([^"]+)"', content, re.DOTALL)
                if model_match:
                    self.keyboard_tab.model_edit.setText(model_match.group(1))
            except:
                pass

            try:
                # XKB file
                file_match = re.search(r'xkb\s*{.*?file\s+"([^"]+)"', content, re.DOTALL)
                if file_match:
                    self.keyboard_tab.file_edit.setText(file_match.group(1))
            except:
                pass
        except FileNotFoundError:
            # If file doesn't exist, use defaults
            print(f"No existing config file found at {self.config_path}, using defaults")
        except Exception as e:
            print(f"Error loading configuration: {e}")

def main():
    app = QApplication(sys.argv)
    app.setDesktopFileName("niri-settings")

    # Setup translator with XDG_DATA_DIRS lookup
    locale = QLocale.system().name()  # e.g., "it_IT"
    language_only = locale.split('_')[0]  # e.g., "it"

    translator = QTranslator()
    translation_loaded = False

    # Get XDG_DATA_DIRS from environment
    xdg_data_dirs = os.environ.get('XDG_DATA_DIRS')
    data_dirs = xdg_data_dirs.split(':')

    # Try both full locale and language-only versions
    locale_variants = [locale, language_only]

    for locale_var in locale_variants:
        for data_dir in data_dirs:
            trans_path = os.path.join(data_dir, "niri-settings", "translations", f"niri_settings_{locale_var}.qm")
            if os.path.exists(trans_path) and translator.load(trans_path):
                app.installTranslator(translator)
                print(f"Loaded translation: {trans_path}")
                translation_loaded = True
                break
        if translation_loaded:
            break

    # Fallback to system Qt translations if our translation wasn't found
    if not translation_loaded:
        qt_translator = QTranslator()
        qt_translations_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if qt_translator.load(f"qt_{language_only}", qt_translations_path):
            app.installTranslator(qt_translator)
            print(f"Loaded Qt system translation for {language_only}")

    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
