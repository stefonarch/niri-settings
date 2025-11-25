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

        # focus_ring
        focus_ring_layout = QHBoxLayout()
        focus_ring_label = QLabel(self.tr('Width:'))

        self.focus_ring_enable_checkbox = QCheckBox(self.tr('Focus ring'))
        self.focus_ring_enable_checkbox.setChecked(True)

        self.focus_ring_spinbox = QSpinBox()
        self.focus_ring_spinbox.setRange(1,9)
        self.focus_ring_spinbox.setSingleStep(1)
        self.focus_ring_spinbox.setValue(4)

        self.focus_ring_enable_checkbox.toggled.connect(self.focus_ring_spinbox.setEnabled)

        focus_ring_layout.addWidget(self.focus_ring_enable_checkbox)
        focus_ring_layout.addWidget(focus_ring_label)
        focus_ring_layout.addWidget(self.focus_ring_spinbox)
        focus_ring_layout.addStretch()
        appearance_layout.addSpacing(15)
        appearance_layout.addLayout(focus_ring_layout)

        color_layout = QHBoxLayout()
        color_label = QLabel(self.tr('Color:'))
        self.color_button = QPushButton()
        self.color_button.setFixedSize(60, 25)
        self.color_button.clicked.connect(self.choose_active_color)
        self.update_color_button()
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        color_layout.addStretch()
        self.focus_ring_enable_checkbox.toggled.connect(focus_ring_label.setEnabled)
        self.focus_ring_enable_checkbox.toggled.connect(self.color_button.setEnabled)

        # initial states
        focus_ring_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.color_button.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.focus_ring_enable_checkbox.toggled.connect(color_label.setEnabled)
        color_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())

        appearance_layout.addLayout(color_layout)

        # Border
        border_layout = QHBoxLayout()
        border_label = QLabel(self.tr('Width:'))

        self.border_enable_checkbox = QCheckBox(self.tr('Border'))
        self.border_enable_checkbox.setChecked(True)

        self.border_spinbox = QSpinBox()
        self.border_spinbox.setRange(1,9)
        self.border_spinbox.setSingleStep(1)
        self.border_spinbox.setValue(4)

        self.border_enable_checkbox.toggled.connect(self.border_spinbox.setEnabled)
        self.border_enable_checkbox.toggled.connect(border_label.setEnabled)
        border_label.setEnabled(self.border_enable_checkbox.isChecked())

        border_layout.addWidget(self.border_enable_checkbox)
        border_layout.addWidget(border_label)
        border_layout.addWidget(self.border_spinbox)
        border_layout.addStretch()
        appearance_layout.addSpacing(15)
        appearance_layout.addLayout(border_layout)

        border_color_layout = QHBoxLayout()
        border_color_label = QLabel(self.tr('Color:'))
        self.border_color_button = QPushButton()
        self.border_color_button.setFixedSize(60, 25)
        self.border_color_button.clicked.connect(self.choose_border_color)
        self.update_border_color_button()
        border_color_layout.addWidget(border_color_label)
        border_color_layout.addWidget(self.border_color_button)
        border_color_layout.addStretch()
        self.border_enable_checkbox.toggled.connect(border_color_label.setEnabled)
        self.border_enable_checkbox.toggled.connect(self.border_color_button.setEnabled)

        focus_ring_label.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.border_color_button.setEnabled(self.focus_ring_enable_checkbox.isChecked())
        self.focus_ring_enable_checkbox.toggled.connect(border_color_label.setEnabled)
        border_color_label.setEnabled(self.border_enable_checkbox.isChecked())

        appearance_layout.addLayout(border_color_layout)

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
        #self.gaps_spinbox.setDecimals(0)

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

        right_label = QLabel(self.tr("Right:"))
        self.struts_right_spin = QSpinBox()
        self.struts_right_spin.setRange(0, 100)
        self.struts_right_spin.setValue(0)

        top_label = QLabel(self.tr("Top:"))
        self.struts_top_spin = QSpinBox()
        self.struts_top_spin.setRange(0, 100)
        self.struts_top_spin.setValue(0)

        bottom_label = QLabel(self.tr("Bottom:"))
        self.struts_bottom_spin = QSpinBox()
        self.struts_bottom_spin.setRange(0, 100)
        self.struts_bottom_spin.setValue(0)

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

