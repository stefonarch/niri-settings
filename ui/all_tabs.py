from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton,
                             QLabel, QScrollArea, QFrame, QButtonGroup, QPushButton, QCheckBox,QGridLayout,
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox, QColorDialog,
                             QListWidget, QListWidgetItem, QMenu, QMessageBox, QPlainTextEdit)
from PyQt6.QtCore import Qt, QTimer, QProcess
from PyQt6.QtGui import QFont, QColor, QAction, QCursor

from pathlib import Path
import os, re, sys, subprocess, shutil

class AppearanceTab(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_color = "#7fc8ff"  # Default focus ring/border color
        self.current_inactive_color = "#505050"  # Default inactive color
        self.current_hint_color = "#ffc87f"
        self.init_ui()

    def choose_active_color(self):
        color = QColorDialog.getColor(QColor(self.current_color), self, self.tr("Choose Color"))
        if color.isValid():
            self.current_color = color.name()
            self.update_color_button()

    def update_color_button(self):
        self.color_button.setStyleSheet(f"background-color: {self.current_color}; border: 1px solid gray;")

    def choose_inactive_color(self):
        color = QColorDialog.getColor(QColor(self.current_inactive_color), self, self.tr("Choose Incactive Color"))
        if color.isValid():
            self.current_inactive_color = color.name()
            self.update_inactive_color_button()

    def update_inactive_color_button(self):
        self.inactive_color_button.setStyleSheet(f"background-color: {self.current_inactive_color}; border: 1px solid gray;")


    def choose_hint_color(self):
        color = QColorDialog.getColor(QColor(self.current_hint_color), self, self.tr("Choose Insert Hint Color"))
        if color.isValid():
            self.current_hint_color = color.name()
            self.update_hint_color_button()

    def update_hint_color_button(self):
        self.hint_color_button.setStyleSheet(f"background-color: {self.current_hint_color}; border: 1px solid gray;")

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Appearance configuration section
        appearance_frame = QFrame()
        appearance_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        appearance_layout = QVBoxLayout(appearance_frame)

        self.csd_checkbox = QCheckBox(self.tr('Use client side decorations'))
        appearance_layout.addWidget(self.csd_checkbox)
        self.csd_checkbox.setChecked(True)

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

        self.animations_enable_checkbox = QCheckBox(self.tr('Enable Animations'))
        self.animations_enable_checkbox.setChecked(True)
        animations_layout = QHBoxLayout()
        slowdown_label = QLabel(self.tr('Slowdown:'))

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

        # Focus ring or border
        focus_ring_layout = QHBoxLayout()
        self.focus_ring_enable_checkbox = QCheckBox(self.tr('Enable focus-ring or border'))
        self.focus_ring_enable_checkbox.setChecked(True)

        focus_ring_layout.addWidget(self.focus_ring_enable_checkbox)
        focus_ring_layout.addStretch()
        appearance_layout.addLayout(focus_ring_layout)

        # Create a container for the indented content
        indented_widget = QWidget()
        indented_layout = QVBoxLayout(indented_widget)
        indented_layout.setContentsMargins(25, 0, 0, 0)

        # Color and inactive color on first line
        colors_layout = QHBoxLayout()

        color_label = QLabel(self.tr('Active color: '))
        self.color_button = QPushButton()
        self.color_button.clicked.connect(self.choose_active_color)
        self.update_color_button()

        inactive_color_label = QLabel(self.tr('Inactive color: '))
        self.inactive_color_button = QPushButton()
        self.inactive_color_button.clicked.connect(self.choose_inactive_color)
        self.update_inactive_color_button()

        colors_layout.addWidget(color_label)
        colors_layout.addWidget(self.color_button)
        colors_layout.addSpacing(25)
        colors_layout.addWidget(inactive_color_label)
        colors_layout.addWidget(self.inactive_color_button)
        colors_layout.addStretch()
        indented_layout.addLayout(colors_layout)

        # Width on second line
        width_layout = QHBoxLayout()
        width_label = QLabel(self.tr('Width:'))
        self.focus_ring_spinbox = QSpinBox()
        self.focus_ring_spinbox.setRange(1,9)
        self.focus_ring_spinbox.setSingleStep(1)
        self.focus_ring_spinbox.setValue(4)
        self.focus_ring_spinbox.setSuffix(' px')

        width_layout.addWidget(width_label)
        width_layout.addWidget(self.focus_ring_spinbox)
        width_layout.addStretch()
        indented_layout.addLayout(width_layout)
        #indented_layout.addSpacing(10)

        # Add the indented widget to the main appearance layout
        appearance_layout.addWidget(indented_widget)

        # Apply to
        apply_layout = QHBoxLayout()
        select_label = QLabel(self.tr('Apply as:'))

        self.focus_radio = QRadioButton(self.tr('Focus ring '))
        self.border_radio = QRadioButton(self.tr('Border'))
        self.focus_radio.setChecked(True)

        apply_layout.addWidget(select_label)
        apply_layout.addSpacing(15)
        apply_layout.addWidget(self.focus_radio)
        apply_layout.addWidget(self.border_radio)
        apply_layout.addStretch()
        indented_layout.addLayout(apply_layout)

        # Add the indented widget to the main appearance layout
        appearance_layout.addWidget(indented_widget)

        # Connect enable/disable states for all dependent widgets
        self.focus_ring_enable_checkbox.toggled.connect(self.focus_ring_spinbox.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(width_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.color_button.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.inactive_color_button.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(color_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(inactive_color_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(select_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.focus_radio.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.border_radio.setEnabled)

        # Set initial states
        width_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.color_button.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.inactive_color_button.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        color_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        select_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.focus_radio.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.border_radio.setEnabled(self.focus_ring_enable_checkbox.isChecked())

        hint_color_layout = QHBoxLayout()

        self.hint_enable_checkbox = QCheckBox(self.tr('Enable insert hint'))
        self.hint_enable_checkbox.setChecked(True)

        hint_color_label = QLabel(self.tr('Color: '))
        self.hint_color_button = QPushButton()
        self.hint_color_button.clicked.connect(self.choose_hint_color)
        self.update_hint_color_button()
        hint_color_layout.addWidget(self.hint_enable_checkbox)
        hint_color_layout.addSpacing(25)
        hint_color_layout.addWidget(hint_color_label)

        hint_color_layout.addWidget(self.hint_color_button)
        hint_color_layout.addStretch()

        self.hint_enable_checkbox.toggled.connect(self.hint_color_button.setEnabled)
        self.hint_enable_checkbox.toggled.connect(hint_color_label.setEnabled)
        hint_color_label.setEnabled(self.hint_enable_checkbox.isChecked())
        self.hint_color_button.setEnabled(self.hint_enable_checkbox.isChecked())#same

        appearance_layout.addLayout(hint_color_layout)

        # Margins Group
        margins_group = QGroupBox(self.tr("Margins"))
        margins_layout = QVBoxLayout(margins_group)

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
        layout.addSpacing(10)

        # Struts (two rows)
        struts_row1 = QHBoxLayout()
        struts_row2 = QHBoxLayout()

        # Left
        left_label = QLabel(self.tr("Left:"))
        self.struts_left_spin = QSpinBox()
        self.struts_left_spin.setRange(-100, 100)
        self.struts_left_spin.setValue(0)
        self.struts_left_spin.setSuffix(' px')

        right_label = QLabel(self.tr("Right:"))
        self.struts_right_spin = QSpinBox()
        self.struts_right_spin.setRange(-100, 100)
        self.struts_right_spin.setValue(0)
        self.struts_right_spin.setSuffix(' px')

        top_label = QLabel(self.tr("Top:"))
        self.struts_top_spin = QSpinBox()
        self.struts_top_spin.setRange(-100, 100)
        self.struts_top_spin.setValue(0)
        self.struts_top_spin.setSuffix(' px')

        bottom_label = QLabel(self.tr("Bottom:"))
        self.struts_bottom_spin = QSpinBox()
        self.struts_bottom_spin.setRange(-100, 100)
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
        margins_layout.addWidget(struts_title)

        margins_layout.addLayout(struts_row1)
        margins_layout.addLayout(struts_row2)

        # Tab Indicator
        tab_group = QGroupBox(self.tr("Tab Indicator"))
        tab_layout = QVBoxLayout(tab_group)

        layout.addWidget(tab_group)

        hide_place_layout = QHBoxLayout()
        self.hide_indicator_checkbox = QCheckBox(self.tr('Hide when single tab'))
        self.hide_indicator_checkbox.setChecked(True)
        hide_place_layout.addWidget(self.hide_indicator_checkbox)
        self.place_within_checkbox = QCheckBox(self.tr('Place within column'))
        self.place_within_checkbox.setChecked(True)
        hide_place_layout.addWidget(self.place_within_checkbox)
        tab_layout.addLayout(hide_place_layout)

        corner_radius_layout = QHBoxLayout()
        corner_radius_label = QLabel(self.tr('Corner radius:'))
        self.corner_radius_spinbox = QSpinBox()
        self.corner_radius_spinbox.setRange(0,20)
        self.corner_radius_spinbox.setSingleStep(1)
        self.corner_radius_spinbox.setValue(4)
        self.corner_radius_spinbox.setSuffix(' px')
        corner_radius_layout.addWidget(corner_radius_label)
        corner_radius_layout.addWidget(self.corner_radius_spinbox)
        corner_radius_layout.addStretch()
        tab_layout.addLayout(corner_radius_layout)

        # Tab Width and Length
        tab_width_layout = QHBoxLayout()
        tab_width_label = QLabel(self.tr('Width:'))
        self.tab_width_spinbox = QSpinBox()
        self.tab_width_spinbox.setRange(0,50)
        self.tab_width_spinbox.setSingleStep(1)
        self.tab_width_spinbox.setValue(4)
        self.tab_width_spinbox.setSuffix(' px')

        length_label = QLabel(self.tr('Length:'))
        self.length_spinbox = QDoubleSpinBox()
        self.length_spinbox.setRange(0,1)
        self.length_spinbox.setSingleStep(0.05)
        self.length_spinbox.setValue(1)

        tab_width_layout.addWidget(tab_width_label)
        tab_width_layout.addWidget(self.tab_width_spinbox)
        tab_width_layout.addSpacing(10)
        tab_width_layout.addWidget(length_label)
        tab_width_layout.addSpacing(10)
        tab_width_layout.addWidget(self.length_spinbox)
        tab_width_layout.addStretch()
        tab_layout.addLayout(tab_width_layout)

        # Tab Gaps
        tab_gaps_layout = QHBoxLayout()
        tab_gaps_label = QLabel(self.tr('Gap:'))
        self.tab_gap_spinbox = QSpinBox()
        self.tab_gap_spinbox.setRange(0,99)
        self.tab_gap_spinbox.setSingleStep(1)
        self.tab_gap_spinbox.setValue(4)
        self.tab_gap_spinbox.setSuffix(' px')

        gap_between_label = QLabel(self.tr('Gap between:'))
        self.gap_between_spinbox = QSpinBox()
        self.gap_between_spinbox.setRange(0,99)
        self.gap_between_spinbox.setSingleStep(1)
        self.gap_between_spinbox.setValue(2)
        self.gap_between_spinbox.setSuffix(' px')

        tab_gaps_layout.addWidget(tab_gaps_label)
        tab_gaps_layout.addWidget(self.tab_gap_spinbox)
        tab_gaps_layout.addSpacing(10)
        tab_gaps_layout.addWidget(gap_between_label)
        tab_gaps_layout.addSpacing(10)
        tab_gaps_layout.addWidget(self.gap_between_spinbox)
        tab_gaps_layout.addStretch()
        tab_layout.addLayout(tab_gaps_layout)

        # Position
        tab_position_label = QLabel(self.tr('Position:'))

        self.left_radio = QRadioButton(self.tr('left'))
        self.top_radio = QRadioButton(self.tr('top'))
        self.right_radio = QRadioButton(self.tr('right'))
        self.bottom_radio = QRadioButton(self.tr('bottom'))
        self.left_radio.setChecked(True)

        tab_position_radio_layout = QHBoxLayout()
        tab_position_radio_layout.addWidget(tab_position_label)
        tab_position_radio_layout.addSpacing(10)
        tab_position_radio_layout.addWidget(self.left_radio)
        tab_position_radio_layout.addWidget(self.top_radio)
        tab_position_radio_layout.addWidget(self.right_radio)
        tab_position_radio_layout.addWidget(self.bottom_radio)
        tab_position_radio_layout.addStretch()
        tab_layout.addLayout(tab_position_radio_layout)

        layout.addStretch()

        self.setWidget(widget)

class BehaviorTab(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

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
        self.always_center_single_checkbox = QCheckBox(self.tr('Always center single column'))
        self.disable_power_key_checkbox = QCheckBox(self.tr('Disable power key handling'))
        self.workspace_auto_back_forth_checkbox = QCheckBox(self.tr('Workspace auto back and forth'))
        self.hot_corners_checkbox = QCheckBox(self.tr('Disable hot corners'))
        self.hide_while_typing_checkbox = QCheckBox(self.tr('Hide cursor while typing'))

        behavior_layout.addWidget(self.hotkey_overlay_checkbox)
        behavior_layout.addWidget(self.focus_request_checkbox)

        # Column group
        column_group = QGroupBox(self.tr('Columns'))
        column_layout =QVBoxLayout(column_group)

        # Default column layout
        default_column_display_layout = QHBoxLayout()
        column_layout_label = QLabel(self.tr('Default layout:'))

        column_display_btngroup = QButtonGroup(self) # keep radio button independent

        self.tabbed_radio = QRadioButton(self.tr('Tabbed'))
        self.normal_radio = QRadioButton(self.tr('Normal'))
        self.tabbed_radio.setChecked(True)
        column_display_btngroup.addButton(self.tabbed_radio)
        column_display_btngroup.addButton(self.normal_radio)

        default_column_display_layout.addWidget(column_layout_label)
        default_column_display_layout.addWidget(self.tabbed_radio)
        default_column_display_layout.addSpacing(15)
        default_column_display_layout.addWidget(self.normal_radio)
        default_column_display_layout.addStretch()

        # Default column width
        column_width_label = QLabel(self.tr("Default width:"))

        proportion_layout = QHBoxLayout()
        width_layout = QHBoxLayout()
        app_decide_layout = QHBoxLayout()

        self.column_proportion_radio = QRadioButton(self.tr('Proportion:'))
        self.column_width_radio = QRadioButton(self.tr('Fixed width:'))
        self.app_decide_radio = QRadioButton(self.tr('Applications may decide'))

        self.column_width_spinbox = QSpinBox()
        self.column_width_spinbox.setRange(100, 4000)
        self.column_width_spinbox.setValue(500)
        self.column_width_spinbox.setSingleStep(100)
        self.column_width_spinbox.setSuffix(" px ")
        self.column_width_spinbox.setEnabled(False)
        self.column_width_radio.toggled.connect(self.column_width_spinbox.setEnabled)
        self.column_width_spinbox.setEnabled(self.column_width_radio.isChecked())

        self.column_proportion_spinbox = QDoubleSpinBox()
        self.column_proportion_spinbox.setRange(0.1, 1.0)
        self.column_proportion_spinbox.setValue(0.5)
        self.column_proportion_spinbox.setSingleStep(0.05)
        self.column_proportion_spinbox.setEnabled(False)
        self.column_proportion_radio.toggled.connect(self.column_proportion_spinbox.setEnabled)
        self.column_width_spinbox.setEnabled(self.column_width_radio.isChecked())

        proportion_layout.addSpacing(20)
        proportion_layout.addWidget(self.column_proportion_radio)
        proportion_layout.addWidget(self.column_proportion_spinbox)
        proportion_layout.addStretch()

        width_layout.addSpacing(20)
        width_layout.addWidget(self.column_width_radio)
        width_layout.addWidget(self.column_width_spinbox)
        width_layout.addStretch()

        app_decide_layout.addSpacing(20)
        app_decide_layout.addWidget(self.app_decide_radio)

        # Center focused column
        center_focused_label = QLabel(self.tr("Center focused column:"))
        center_focused_layout = QHBoxLayout()
        center_focused_btns = QButtonGroup(self)

        self.column_never_radio = QRadioButton(self.tr('never'))
        self.column_never_radio.setChecked(True)
        self.column_always_radio = QRadioButton(self.tr('always'))
        self.column_on_overflow_radio = QRadioButton(self.tr('on overflow'))

        center_focused_btns.addButton(self.column_never_radio)
        center_focused_btns.addButton(self.column_always_radio)
        center_focused_btns.addButton(self.column_on_overflow_radio)

        center_focused_layout.addSpacing(20)
        center_focused_layout.addWidget(self.column_never_radio)
        center_focused_layout.addWidget(self.column_always_radio)
        center_focused_layout.addWidget(self.column_on_overflow_radio)
        center_focused_layout.addStretch()

        column_layout.addLayout(default_column_display_layout)
        column_layout.addWidget(column_width_label)
        column_layout.addLayout(proportion_layout)
        column_layout.addLayout(width_layout)
        column_layout.addLayout(app_decide_layout)
        column_layout.addSpacing(10)
        column_layout.addWidget(center_focused_label)
        column_layout.addLayout(center_focused_layout)
        column_layout.addWidget(self.always_center_single_checkbox)

        behavior_layout.addWidget(column_group)
        behavior_layout.addWidget(self.disable_power_key_checkbox)
        behavior_layout.addWidget(self.workspace_auto_back_forth_checkbox)
        behavior_layout.addWidget(self.hot_corners_checkbox)

        # Mod key
        behavior_layout.addSpacing(10)
        mod_key_label = QLabel(self.tr('Mod Key:'))

        self.super_radio = QRadioButton(self.tr('Super'))
        self.alt_radio = QRadioButton(self.tr('Alt'))
        self.ctrl_radio = QRadioButton(self.tr('Ctrl'))
        self.super_radio.setChecked(True)

        mod_key_radio_layout = QHBoxLayout()
        mod_key_radio_label = QLabel(self.tr('Mod Key:'))
        mod_key_radio_layout.addWidget(mod_key_label)
        mod_key_radio_layout.addSpacing(15)
        mod_key_radio_layout.addWidget(self.super_radio)
        mod_key_radio_layout.addWidget(self.alt_radio)
        mod_key_radio_layout.addWidget(self.ctrl_radio)
        mod_key_radio_layout.addStretch()

        behavior_layout.addLayout(mod_key_radio_layout)

        # screenshot_path
        screenshot_path_layout = QHBoxLayout()
        screenshot_path_label = QLabel(self.tr('Screenshots:'))
        self.screenshot_path_edit = QLineEdit()
        self.screenshot_path_edit.setPlaceholderText("~/Pictures/Screenshot %Y-%m-%d %H-%M-%S.png")
        self.screenshot_path_edit.setMinimumWidth(400)
        self.screenshot_path_edit.setClearButtonEnabled(True)

        screenshot_path_layout.addWidget(screenshot_path_label)
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
        self.inactive_enable_checkbox.toggled.connect(self.inactive_spinbox.setEnabled)
        self.inactive_enable_checkbox.toggled.connect(inactive_label.setEnabled)
        inactive_label.setEnabled(self.inactive_enable_checkbox.isChecked())
        self.inactive_spinbox.setEnabled(self.inactive_enable_checkbox.isChecked())

        cursor_layout.addWidget(self.focus_follows_mouse_checkbox)
        cursor_layout.addWidget(self.warp_mouse_to_focus_checkbox)
        cursor_layout.addWidget(self.hide_while_typing_checkbox)
        cursor_layout.addLayout(inactive_layout)

        layout.addWidget(behavior_frame)
        layout.addWidget(cursor_group)
        layout.addStretch()

        self.setWidget(widget)

class TouchpadTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

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

        scroll_groupbox = QGroupBox(self.tr('Scroll method'))
        scroll_groupbox_layout = QGridLayout(scroll_groupbox)
        scroll_groupbox.setFixedWidth(500)

        scroll_groupbox_layout.addWidget(self.no_scroll_radio, 0, 0)   # row 0, col 0
        scroll_groupbox_layout.addWidget(self.two_finger_radio, 0, 1)  # row 0, col 1
        scroll_groupbox_layout.rowStretch(0)
        scroll_groupbox_layout.addWidget(self.edge_radio, 1, 0)        # row 1, col 0
        scroll_groupbox_layout.addWidget(self.button_radio, 1, 1)
        scroll_groupbox_layout.rowStretch(1)     # row 1, col 1
        touchpad_layout.addWidget(scroll_groupbox)

        # Acceleration speed
        accel_speed_layout = QHBoxLayout()
        accel_speed_label = QLabel(self.tr('Acceleration speed:'))
        self.accel_speed_spinbox = QDoubleSpinBox()
        self.accel_speed_spinbox.setRange(-1.0, 1.0)
        self.accel_speed_spinbox.setSingleStep(0.05)
        self.accel_speed_spinbox.setValue(0.2)
        self.accel_speed_spinbox.setDecimals(2)

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
        self.scroll_factor_spinbox.setRange(0.1, 5.0)
        self.scroll_factor_spinbox.setSingleStep(0.1)
        self.scroll_factor_spinbox.setValue(1.0)
        self.scroll_factor_spinbox.setDecimals(1)

        scroll_factor_layout.addWidget(scroll_factor_label)
        scroll_factor_layout.addWidget(self.scroll_factor_spinbox)
        scroll_factor_layout.addStretch()
        touchpad_layout.addLayout(scroll_factor_layout)

        # Button_map method selection
        button_map_label = QLabel(self.tr('Tap Button Map:'))
        touchpad_layout.addWidget(button_map_label)


        self.lmr_radio = QRadioButton(self.tr('left-middle-right'))
        self.lrm_radio = QRadioButton(self.tr('left-right-middle'))


        self.lmr_radio.setChecked(True)

        touchpad_layout.addWidget(self.lmr_radio)
        touchpad_layout.addWidget(self.lrm_radio)

        layout.addWidget(touchpad_frame)
        layout.addStretch()

class MouseTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        #layout.setSpacing(20)
        #layout.setContentsMargins(20, 10, 20, 20)

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
        self.accel_speed_spinbox.setSingleStep(0.05)
        self.accel_speed_spinbox.setValue(0.2)
        self.accel_speed_spinbox.setDecimals(2)

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
        self.scroll_factor_spinbox.setRange(0.1, 5.0)
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
        xkb_group = QGroupBox(self.tr("Keyboard Layout"))
        xkb_layout = QVBoxLayout(xkb_group)

        # Layout
        layout_layout = QHBoxLayout()
        layout_label = QLabel(self.tr('Layout:'))
        self.layout_edit = QLineEdit()
        self.layout_edit.setPlaceholderText("e.g. us,ru,de")
        self.layout_edit.setMaximumWidth(120)
        self.layout_edit.setClearButtonEnabled(True)

        layout_layout.addWidget(layout_label)
        #layout_layout.addSpacing(5)
        layout_layout.addWidget(self.layout_edit)
        layout_layout.addStretch()
        #layout_layout.addSpacing(10)
        xkb_layout.addLayout(layout_layout)

        # Variant
        variant_layout = QHBoxLayout()
        variant_label = QLabel(self.tr('Variant:'))
        self.variant_edit = QLineEdit()
        self.variant_edit.setPlaceholderText("e.g., colemak_dh_ortho")
        self.variant_edit.setMinimumWidth(300)
        self.variant_edit.setClearButtonEnabled(True)

        variant_layout.addWidget(variant_label)
        #variant_layout.addSpacing(5)
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
        #model_layout.addSpacing(14)
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
        #file_layout.addSpacing(34)
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

class FilesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_kdl_files()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel(self.tr("KDL Files in Configuration"))#specific title?
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()

        refresh_btn = QPushButton(self.tr("Refresh"))
        refresh_btn.clicked.connect(self.refresh_files)
        button_layout.addWidget(refresh_btn)

        open_btn = QPushButton(self.tr("Open"))
        open_btn.clicked.connect(self.open_selected)
        button_layout.addWidget(open_btn)

        validate_btn = QPushButton(self.tr("Validate file"))
        validate_btn.clicked.connect(self.validate_selected)

        backup_btn = QPushButton(self.tr("Backup file"))
        backup_btn.clicked.connect(self.backup_selected)
        button_layout.addWidget(backup_btn)

        button_layout.addWidget(validate_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)

        layout.addWidget(self.terminal)

        # Connect signals
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

    def load_kdl_files(self):
        """Load and display all .kdl files from the configuration directory."""
        # Get XDG_CONFIG_HOME or use default
        current_desktop = os.environ.get('XDG_CURRENT_DESKTOP', '')
        desktop_list = [item.strip() for item in current_desktop.split(':')]
        xdg_config_home = os.getenv('XDG_CONFIG_HOME')

        if not xdg_config_home:
            xdg_config_home = Path.home() / '.config'

        if 'LXQt' in desktop_list:
            base_path = Path(xdg_config_home) / 'lxqt' / 'wayland'
        else:
            base_path = Path(xdg_config_home) / 'niri'

        if not base_path.exists():  #needed?
            self.show_error(self.tr("Directory does not exist:\n{base_path}"))
            return

        # Find all .kdl files recursively
        kdl_files = list(base_path.rglob('*.kdl*'))

        if not kdl_files:
            self.show_info(self.tr(f"No .kdl files found in:\n{base_path}"))
            return

        for file_path in sorted(kdl_files):
            # Get relative path from base directory for cleaner display
            try:
                rel_path = file_path.relative_to(base_path)
                display_text = str(rel_path)
            except ValueError:
                display_text = str(file_path)

            # Create list item with full path as tooltip
            item = QListWidgetItem(display_text)
            item.setToolTip(str(file_path))
            item.setData(Qt.ItemDataRole.UserRole, str(file_path))  # Store full path
            self.list_widget.addItem(item)

    def open_with_xdg(self, file_path):
        try:
            subprocess.Popen(['xdg-open', file_path])
            return True
        except FileNotFoundError:
            self.show_error(self.tr("xdg-open not found. Make sure it's installed and in your PATH."))
            return False
        except Exception as e:
            self.show_error(self.tr(f"Failed to open file:\n{str(e)}"))
            return False

    def on_item_clicked(self, item):
        file_path = item.data(Qt.ItemDataRole.UserRole)

    def on_item_double_clicked(self, item):
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.open_with_xdg(file_path)

    def show_context_menu(self, position):
        item = self.list_widget.itemAt(position)
        if not item:
            return

        file_path = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu()

        open_action = QAction(self.tr("Open"), self)
        open_action.triggered.connect(lambda: self.open_with_xdg(file_path))
        menu.addAction(open_action)

        show_in_folder_action = QAction(self.tr("Show in file manager"), self)
        show_in_folder_action.triggered.connect(
            lambda: subprocess.Popen(['xdg-open', os.path.dirname(file_path)])
        )
        menu.addAction(show_in_folder_action)

        copy_path_action = QAction(self.tr("Copy path to clipboard"), self)
        copy_path_action.triggered.connect(
            lambda: QApplication.clipboard().setText(file_path)
        )
        menu.addAction(copy_path_action)

        menu.exec(self.list_widget.mapToGlobal(position))

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Information", message)

    def refresh_files(self):
        self.list_widget.clear()
        self.load_kdl_files()

    def open_selected(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            file_path = current_item.data(Qt.ItemDataRole.UserRole)
            self.open_with_xdg(file_path)
        else:
            self.show_info(self.tr("No file selected."))

    def backup_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                self.show_info(self.tr(f"File not found: {file_path}"))
                return False

            backup_path = f"{file_path}~"
            shutil.copy2(file_path, backup_path)

            self.refresh_files()
            return True

        except PermissionError:
            self.show_info(self.tr("Permission denied. Cannot create backup."))
            return False
        except Exception as e:
            self.show_info(self.tr(f"Backup failed: {str(e)}"))
            return False

    def backup_selected(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            file_path = current_item.data(Qt.ItemDataRole.UserRole)
            self.backup_file(file_path)
        else:
            self.show_info(self.tr("No file selected."))

    ansi_escape = re.compile(r'\x1b\[[0-9;]*m') # needed to clean "file is valid" output
    def clean_ansi(self, text: str) -> str:
        return self.ansi_escape.sub('', text)

    def validate_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            self.show_info("No file selected.")
            return

        file_path = item.data(Qt.ItemDataRole.UserRole)

        self.proc = QProcess(self)
        self.proc.setProgram("niri")
        self.proc.setArguments(["validate", "-c", file_path])

        self.proc.readyReadStandardOutput.connect(
            lambda: self.terminal.appendPlainText(
                self.clean_ansi(bytes(self.proc.readAllStandardOutput()).decode())
            )
        )

        self.proc.readyReadStandardError.connect(
            lambda: self.terminal.appendPlainText(
                self.clean_ansi(bytes(self.proc.readAllStandardError()).decode())
            )
        )

        self.terminal.clear()
        self.terminal.appendPlainText(f"$ niri validate -c {file_path}\n")

        self.proc.start()
