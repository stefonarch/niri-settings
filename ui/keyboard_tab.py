from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget,
                             QLabel, QFrame, QPushButton, QCheckBox, QDialog,QTreeWidget, QTreeWidgetItem,
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox
                             )
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from pathlib import Path

class KeyboardTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

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
        self.track_layout_combobox.addItems([self.tr("window"),self.tr("global")])

        track_layout_layout.addWidget(track_layout_label)
        track_layout_layout.addWidget(self.track_layout_combobox)
        track_layout_layout.addStretch()
        keyboard_layout.addLayout(track_layout_layout)

        # XKB Settings Group
        xkb_group = QGroupBox(self.tr("Keyboard Layout"))
        xkb_layout = QVBoxLayout(xkb_group)

        # Get layout list:
        try:
            with open("/usr/share/X11/xkb/rules/evdev.lst") as f:
                self.evdev_lines = [line.rstrip() for line in f]

                layouts = []
                in_layouts = False
                for line in self.evdev_lines:

                    if line.startswith("! layout"):
                        in_layouts = True
                        continue

                    if in_layouts:
                        if line.startswith("!"):
                            break
                        line = line.strip()
                        if line:
                            layouts.append(line)

            layouts.sort()
            self.xkb_layouts = layouts

            # Get xkb variants:
            variants = []
            in_variants = False
            for line in self.evdev_lines:

                if line.startswith("! variant"):
                    in_variants = True
                    continue

                if in_variants:
                    if line.startswith("!"):
                        break  # next section
                    if line.strip():
                        variants.append(line.split()[0])

            variants = sorted(set(variants))
            variants.insert(0, "")
            self.xkb_variants = variants

        # Get xkb models:
            models = []
            in_models = False
            for line in self.evdev_lines:

                if line.startswith("! model"):
                    in_models = True
                    continue

                if in_models:
                    if line.startswith("!"):
                        break  # next section
                    if line.strip():
                        models.append(line.split()[0])

            models.sort()
            models.insert(0, "")
            self.xkb_models = models

        except FileNotFoundError:
            print("File /usr/share/X11/xkb/rules/evdev.lst not found")
            pass

        # Layout
        layout_layout = QHBoxLayout()
        layout_label = QLabel(self.tr('Layout:'))
        self.layout_edit = QLineEdit()
        self.layout_edit.setPlaceholderText("e.g. us,ru,de")
        self.layout_edit.setFixedWidth(200)
        self.layout_edit.setClearButtonEnabled(True)

        self.list_combobox = QComboBox()
        self.list_combobox.setPlaceholderText(self.tr("Select a layout to add"))

        self.list_combobox.currentIndexChanged.connect(self.on_select)
        if hasattr(self, 'xkb_layouts') and self.xkb_layouts:
            self.list_combobox.addItems(self.xkb_layouts)

        layout_layout.addWidget(layout_label)
        layout_layout.addWidget(self.layout_edit)
        layout_layout.addWidget(self.list_combobox)
        layout_layout.addStretch()
        xkb_layout.addLayout(layout_layout)

        # Variant
        variant_layout = QHBoxLayout()
        variant_label = QLabel(self.tr('Variant:'))
        self.variant_combobox = QComboBox()
        self.variant_combobox.setEditable(True)

        if hasattr(self, 'xkb_variants') and self.xkb_variants:
            self.variant_combobox.addItems(self.xkb_variants)

        variant_layout.addWidget(variant_label)
        variant_layout.addWidget(self.variant_combobox)
        variant_layout.addStretch()
        xkb_layout.addLayout(variant_layout)

        # Options
        options_layout = QHBoxLayout()
        options_label = QLabel(self.tr('Options:'))
        self.options_edit = QLineEdit()
        self.options_edit.setClearButtonEnabled(True)

        self.show_options_btn = QPushButton(self.tr("Options (double click to add)"))
        self.show_options_btn.clicked.connect(self.show_options)

        options_layout.addWidget(options_label)
        options_layout.addWidget(self.options_edit)
        options_layout.addWidget(self.show_options_btn)
        options_layout.addStretch()
        xkb_layout.addLayout(options_layout)

        # Model
        model_layout = QHBoxLayout()
        model_label = QLabel(self.tr('Model:'))
        self.model_combobox = QComboBox()
        self.model_combobox.setEditable(True)

        if hasattr(self, 'xkb_models') and self.xkb_models:
            self.model_combobox.addItems(self.xkb_models)

        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combobox)
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

    def on_select(self, index):
        layouts = self.list_combobox.itemText(index)
        layout = layouts.split()[0]
        current = self.layout_edit.text()
        if current:
            self.layout_edit.setText(f"{current},{layout}")
        else:
            self.layout_edit.setText(layout)

    def show_options(self):
        grp_options = []
        in_options = False
        for line in self.evdev_lines:

            if line.startswith("! option"):
                in_options = True
                continue

            if in_options:
                if line.startswith("!"):
                    break
                line = line.strip()
                grp_options.append(line)

        # Modal dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("XKB Group Options")
        dialog.resize(900, 500)

        layout = QVBoxLayout(dialog)

        tree = QTreeWidget()
        tree.setColumnCount(2)
        tree.itemDoubleClicked.connect(self.on_item_double_clicked)

        tree.setHeaderLabels(["Key", "Description"])

        font_bold = QFont()
        font_bold.setBold(True)

        for line in grp_options:
            parts = line.split(None, 1)
            key = parts[0]
            desc = parts[1] if len(parts) > 1 else ""
            display_key = f"    {key}" if ":" not in key else key
            item = QTreeWidgetItem([display_key, desc])
            if ":" not in key:
                item.setFont(0, font_bold)
                item.setFont(1, font_bold)
            tree.addTopLevelItem(item)
            tree.resizeColumnToContents(0)
            tree.resizeColumnToContents(1)

        layout.addWidget(tree)

        btn_layout = QHBoxLayout()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)
        dialog.exec()

    # Insert first column into QLineEdit on double click
    def on_item_double_clicked(self, item, column):
        key = item.text(0)
        current = self.options_edit.text()
        if current:
            self.options_edit.setText(f"{current}, {key}")
        else:
            self.options_edit.setText(key)
