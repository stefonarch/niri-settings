from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, 
                             QLabel, QFrame, QButtonGroup, QPushButton, QCheckBox, 
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox)
from PyQt6.QtCore import Qt

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