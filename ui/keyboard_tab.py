from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton,
                             QLabel, QFrame, QButtonGroup, QPushButton, QCheckBox,
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox)
from PyQt6.QtCore import Qt

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
