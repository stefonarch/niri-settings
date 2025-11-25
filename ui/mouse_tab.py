from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, 
                             QLabel, QFrame, QButtonGroup, QPushButton, QCheckBox, 
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox)
from PyQt6.QtCore import Qt

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