from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, 
                             QLabel, QFrame, QButtonGroup, QPushButton, QCheckBox, 
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox, QColorDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class AppearanceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_color = "#3584e4"  # Default color
        self.current_bordercolor = "#3584e4"  # Default border color
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
        self.bordercolor_button.setStyleSheet(f"background-color: {self.current_bordercolor}; border: 1px solid gray;")

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
        self.bordercolor_button.clicked.connect(self.choose_border_color)
        self.update_border_color_button()
        bordercolor_layout.addWidget(bordercolor_label)
        bordercolor_layout.addWidget(self.bordercolor_button)
        bordercolor_layout.addStretch()
        borderb_layout.addLayout(bordercolor_layout)

        layout.addWidget(appearance_frame)
        layout.addWidget(focus_group)
        layout.addWidget(border_group)
        layout.addStretch()