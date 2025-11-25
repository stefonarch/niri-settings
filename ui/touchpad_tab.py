from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton,
                             QLabel, QFrame, QButtonGroup, QPushButton, QCheckBox,
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox)
from PyQt6.QtCore import Qt

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
