# ui/widgets.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, 
                             QLabel, QFrame, QButtonGroup, QPushButton, QCheckBox, 
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox,
                             QColorDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

# Add any custom widgets or shared UI components here
class ColorPickerButton(QPushButton):
    def __init__(self, color=QColor(255, 255, 255), parent=None):
        super().__init__(parent)
        self.color = color
        self.update_color_display()
        self.clicked.connect(self.pick_color)
    
    def update_color_display(self):
        self.setStyleSheet(f"background-color: {self.color.name()};")
    
    def pick_color(self):
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.update_color_display()