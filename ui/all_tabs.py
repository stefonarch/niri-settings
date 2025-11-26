from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton,
                             QLabel, QFrame, QButtonGroup, QPushButton, QCheckBox,
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox, QColorDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class AppearanceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_color = "#7fc8ff"  # Default focus ring color
        self.current_bordercolor = "#ffc87f"  # Default border color
        self.init_ui()

    def choose_active_color(self):
        """Open color dialog to choose active focus ring color"""
        color = QColorDialog.getColor(QColor(self.current_color), self, self.tr("Choose Focus Ring Color"))
        if color.isValid():
            self.current_color = color.name()
            self.update_color_button()

    def update_color_button(self):
        """Update color button background to show current color"""
        self.color_button.setStyleSheet(f"background-color: {self.current_color}; border: 1px solid gray;")

    def choose_border_color(self):
        """Open color dialog to choose border color"""
        color = QColorDialog.getColor(QColor(self.current_bordercolor), self, self.tr("Choose Border Color"))
        if color.isValid():
            self.current_bordercolor = color.name()
            self.update_border_color_button()

    def update_border_color_button(self):
        """Update border color button background to show current color"""
        self.border_color_button.setStyleSheet(f"background-color: {self.current_bordercolor}; border: 1px solid gray;")

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
        appearance_layout.addWidget(self.csd_checkbox)

        # Overview
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

        self.shadows_checkbox = QCheckBox(self.tr('Enable shadows'))
        self.shadows_checkbox.setChecked(True)
        appearance_layout.addWidget(self.shadows_checkbox)

        # Animations
        animations_layout = QHBoxLayout()
        slowdown_label = QLabel(self.tr('Slowdown:'))

        self.animations_enable_checkbox = QCheckBox(self.tr('Enable Animations'))
        self.animations_enable_checkbox.setChecked(True)

        self.animations_spinbox = QDoubleSpinBox()
        self.animations_spinbox.setRange(0.1, 5.0)
        self.animations_spinbox.setSingleStep(0.1)
        self.animations_spinbox.setValue(1)
        self.animations_spinbox.setDecimals(1)

        self.animations_enable_checkbox.toggled.connect(self.animations_spinbox.setEnabled)
        self.animations_enable_checkbox.toggled.connect(slowdown_label.setEnabled)
        slowdown_label.setEnabled(self.animations_enable_checkbox.isChecked())

        animations_layout.addWidget(self.animations_enable_checkbox)
        animations_layout.addWidget(slowdown_label)
        animations_layout.addWidget(self.animations_spinbox)
        animations_layout.addStretch()
        appearance_layout.addLayout(animations_layout)
        appearance_layout.addSpacing(10)

        # Focus/border ring
        focus_ring_layout = QHBoxLayout()
        self.focus_ring_enable_checkbox = QCheckBox(self.tr('Enable borders'))
        self.focus_ring_enable_checkbox.setChecked(True)

        focus_ring_layout.addWidget(self.focus_ring_enable_checkbox)
        focus_ring_layout.addStretch()
        appearance_layout.addLayout(focus_ring_layout)

        # Create a container for the indented content
        indented_widget = QWidget()
        indented_layout = QVBoxLayout(indented_widget)
        indented_layout.setContentsMargins(25, 0, 0, 0)
        indented_layout.setSpacing(0)

        # Color and width
        color_width_layout = QHBoxLayout()

        color_label = QLabel(self.tr('Active color: '))
        self.color_button = QPushButton()
        self.color_button.setFixedSize(60, 25)
        self.color_button.clicked.connect(self.choose_active_color)
        self.update_color_button()

        width_label = QLabel(self.tr('Width:'))
        self.focus_ring_spinbox = QSpinBox()
        self.focus_ring_spinbox.setRange(1,9)
        self.focus_ring_spinbox.setSingleStep(1)
        self.focus_ring_spinbox.setValue(4)
        self.focus_ring_spinbox.setSuffix(' px')

        color_width_layout.addWidget(color_label)
        color_width_layout.addWidget(self.color_button)
        color_width_layout.addSpacing(20)  # Add some spacing between color and width
        color_width_layout.addWidget(width_label)
        color_width_layout.addWidget(self.focus_ring_spinbox)
        color_width_layout.addStretch()
        indented_layout.addLayout(color_width_layout)

        # Inactive color and width
        inactive_color_width_layout = QHBoxLayout()

        inactive_color_label = QLabel(self.tr('Inactive color: '))
        self.inactive_color_button = QPushButton()
        self.inactive_color_button.setFixedSize(60, 25)
        #self.inactive_color_button.clicked.connect(self.choose_active_inactive_color)
        #self.update_inactive_color_button()

        inactive_width_label = QLabel(self.tr('Inactive width:'))
        self.inactive_width_spinbox = QSpinBox()
        self.inactive_width_spinbox.setRange(1,9)
        self.inactive_width_spinbox.setSingleStep(1)
        self.inactive_width_spinbox.setValue(4)
        self.inactive_width_spinbox.setSuffix(' px')

        inactive_color_width_layout.addWidget(inactive_color_label)
        inactive_color_width_layout.addWidget(self.inactive_color_button)
        inactive_color_width_layout.addSpacing(20)  # Add some spacing between inactive_color and width
        inactive_color_width_layout.addWidget(inactive_width_label)
        inactive_color_width_layout.addWidget(self.inactive_width_spinbox)
        inactive_color_width_layout.addStretch()
        indented_layout.addLayout(inactive_color_width_layout)

        # Apply to
        apply_layout = QHBoxLayout()
        select_label = QLabel(self.tr('Apply to:'))

        self.focus_radio = QRadioButton(self.tr('Focus ring '))
        self.border_radio = QRadioButton(self.tr('Border'))
        self.focus_radio.setChecked(True)

        apply_layout.addWidget(select_label)
        apply_layout.addSpacing(20)
        apply_layout.addWidget(self.focus_radio)
        apply_layout.addWidget(self.border_radio)
        apply_layout.addStretch()
        indented_layout.addLayout(apply_layout)

        # Add the indented widget to the main appearance layout
        appearance_layout.addWidget(indented_widget)

        # Connect enable/disable states for all dependent widgets
        self.focus_ring_enable_checkbox.toggled.connect(self.focus_ring_spinbox.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.inactive_width_spinbox.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(width_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(inactive_width_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.color_button.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(color_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(inactive_color_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(select_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.focus_radio.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.border_radio.setEnabled)

        # Set initial states
        width_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.color_button.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        color_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        select_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.focus_radio.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.border_radio.setEnabled(self.focus_ring_enable_checkbox.isChecked())

        # Margins
        margins_group = QGroupBox(self.tr("Margins"))
        margins_layout = QVBoxLayout(margins_group)
        margins_layout.setContentsMargins(30, 10, 20, 20)

        # Gaps
        gaps_layout = QHBoxLayout()
        gaps_label = QLabel(self.tr('Gaps:'))
        self.gaps_spinbox = QSpinBox()
        self.gaps_spinbox.setRange(0,50)
        self.gaps_spinbox.setSingleStep(1)
        self.gaps_spinbox.setValue(8)
        self.gaps_spinbox.setSuffix(' px')

        gaps_layout.addWidget(gaps_label)
        gaps_layout.addWidget(self.gaps_spinbox)
        gaps_layout.addStretch()
        margins_layout.addLayout(gaps_layout)

        layout.addWidget(appearance_frame)
        layout.addWidget(margins_group)

        # Struts (two rows)
        struts_row1 = QHBoxLayout()
        struts_row2 = QHBoxLayout()

        # Left
        left_label = QLabel(self.tr("Left:"))
        self.struts_left_spin = QSpinBox()
        self.struts_left_spin.setRange(0, 100)
        self.struts_left_spin.setValue(0)
        self.struts_left_spin.setSuffix(' px')

        right_label = QLabel(self.tr("Right:"))
        self.struts_right_spin = QSpinBox()
        self.struts_right_spin.setRange(0, 100)
        self.struts_right_spin.setValue(0)
        self.struts_right_spin.setSuffix(' px')

        top_label = QLabel(self.tr("Top:"))
        self.struts_top_spin = QSpinBox()
        self.struts_top_spin.setRange(0, 100)
        self.struts_top_spin.setValue(0)
        self.struts_top_spin.setSuffix(' px')

        bottom_label = QLabel(self.tr("Bottom:"))
        self.struts_bottom_spin = QSpinBox()
        self.struts_bottom_spin.setRange(0, 100)
        self.struts_bottom_spin.setValue(0)
        self.struts_bottom_spin.setSuffix(' px')

        struts_row1.addWidget(left_label)
        struts_row1.addWidget(self.struts_left_spin)
        struts_row1.addWidget(right_label)
        struts_row1.addWidget(self.struts_right_spin)
        struts_row1.addStretch()

        struts_row2.addWidget(top_label)
        struts_row2.addWidget(self.struts_top_spin)
        struts_row2.addWidget(bottom_label)
        struts_row2.addWidget(self.struts_bottom_spin)
        struts_row2.addStretch()

        struts_title = QLabel(self.tr("Struts:"))
        margins_layout.addSpacing(10)
        margins_layout.addWidget(struts_title)

        margins_layout.addLayout(struts_row1)
        margins_layout.addLayout(struts_row2)

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
        self.hotkey_overlay_checkbox = QCheckBox(self.tr('Show hotkeys at login'))
        self.hotkey_overlay_checkbox.setChecked(True)
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
        self.inactive_spinbox.setRange(500, 20000)
        self.inactive_spinbox.setValue(3000)
        self.inactive_spinbox.setSingleStep(250)
        self.inactive_spinbox.setSuffix(' ms')

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
        self.numlock_checkbox.setChecked(True)
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
        self.options_edit.setPlaceholderText("grp:alt_shift_toggle,compose:rctrl")
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
        self.tap_checkbox.setChecked(True)
        self.natural_scroll_checkbox = QCheckBox(self.tr('Natural scroll'))
        self.natural_scroll_checkbox.setChecked(True)
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

        # Button_map method selection
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

        layout.addWidget(touchpad_frame)
        layout.addStretch()
