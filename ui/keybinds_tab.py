from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton,
                             QLabel, QScrollArea, QFrame, QButtonGroup, QPushButton, QCheckBox,QGridLayout,
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox, QColorDialog,
                             QListWidget, QListWidgetItem, QMenu, QMessageBox, QPlainTextEdit, QSplitter,
                             QDialog, QDialogButtonBox,QInputDialog, QFormLayout, QLabel, QKeySequenceEdit
                             )
import sys, subprocess

from PyQt6.QtCore import Qt, QTimer, QProcess
from PyQt6.QtGui import QFont, QColor, QAction, QCursor, QShortcut, QKeySequence

from pathlib import Path
import os, re, sys, subprocess, shutil

# Are we on LXQt or not?
current_desktop = os.environ.get('XDG_CURRENT_DESKTOP', '')
desktop_list = [item.strip() for item in current_desktop.split(':')]

class KeyBindsTab(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Get the config file path
        config_file = get_keybind_config_path()

        file_editor = KeybindsFileEditor(config_file)
        layout.addWidget(file_editor)

        self.setWidget(widget)
        self.setWidgetResizable(True)

class KeybindsFileEditor(QWidget):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.lines = []
        self.initUI()
        self.load_file()

        # Get niri actions:
        completed = subprocess.run(
            ["niri", "msg", "action"],
            stderr=subprocess.PIPE,
            text=True
        )

        lines = completed.stderr.splitlines()
        lines = lines[5:]
        lines = lines[::2]
        lines = [line[2:] for line in lines]
        actions = lines[:-3]
        self.niri_actions = sorted(actions)

    def initUI(self):
        layout = QVBoxLayout(self)

        self.label = QLabel()
        self.label.setText(
        self.tr("Editing %1").replace("%1", str(self.filename))
        )
        font = QFont()
        font.setItalic(True)
        self.label.setFont(font)
        layout.addWidget(self.label)

        # Create a splitter for horizontal division
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Top panel: Filter and List
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel(self.tr("Filter:")))

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText(self.tr("Type to filter..."))
        self.filter_input.textChanged.connect(self.filter_lines)
        self.filter_input.setClearButtonEnabled(True)
        shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        shortcut.activated.connect(self.filter_input.setFocus)

        filter_layout.addWidget(self.filter_input)

        self.filter_count = QLabel("")
        filter_layout.addWidget(self.filter_count)

        top_layout.addLayout(filter_layout)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        font = QFont("Monospace")
        self.list_widget.setFont(font)

        top_layout.addWidget(self.list_widget)

        splitter.addWidget(top_panel)

        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)

        # Shortcut editor
        self.text_edit = QPlainTextEdit()
        self.text_edit.setMaximumHeight(80)
        font = QFont("Monospace")
        self.text_edit.setFont(font)
        self.text_edit.setPlaceholderText(self.tr("Select a line to edit here"))

        bottom_layout.addWidget(self.text_edit)

        # Button layouts
        button_layout = QHBoxLayout()
        add_button_layout = QHBoxLayout()

        self.save_btn = QPushButton(self.tr("Save edit"))
        self.save_btn.setToolTip("Ctrl+S")
        self.save_btn.clicked.connect(self.save_line)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self.save_btn.click)

        self.remove_btn = QPushButton(self.tr("Remove this line"))
        self.remove_btn.setToolTip("Canc")
        self.remove_btn.clicked.connect(self.delete_line)
        self.remove_btn.setEnabled(False)
        button_layout.addWidget(self.remove_btn)
        button_layout.addStretch()
        shortcut = QShortcut(QKeySequence("Canc"), self)
        shortcut.activated.connect(self.remove_btn.click)

        self.move_up_btn = QPushButton(self.tr("Move up"))
        self.move_up_btn.clicked.connect(self.delete_line)
        self.move_up_btn.setEnabled(False)
        #button_layout.addWidget(self.move_up_btn)

        self.move_down_btn = QPushButton(self.tr("Move down"))
        self.move_down_btn.clicked.connect(self.delete_line)
        self.move_down_btn.setEnabled(False)
        #button_layout.addWidget(self.move_down_btn)

        self.trigger_label = QLabel(self.tr("Trigger:"))
        self.trigger_label.setEnabled(False)
        add_button_layout.addWidget(self.trigger_label)
        self.add_cmd_btn = QPushButton(self.tr("Application"))
        self.add_cmd_btn.clicked.connect(self.add_application)
        self.add_cmd_btn.setEnabled(False)
        add_button_layout.addWidget(self.add_cmd_btn)

        self.add_cmd_sh_btn = QPushButton(self.tr("Shell command"))
        self.add_cmd_sh_btn.clicked.connect(self.add_cmd_sh)
        self.add_cmd_sh_btn.setEnabled(False)
        add_button_layout.addWidget(self.add_cmd_sh_btn)

        self.add_action_btn = QPushButton(self.tr("niri action"))
        self.add_action_btn.clicked.connect(self.add_niri_action)
        self.add_action_btn.setEnabled(False)
        add_button_layout.addWidget(self.add_action_btn)
        add_button_layout.addStretch()

        self.add_comment_btn = QPushButton(self.tr("Insert custom line"))
        self.add_comment_btn.setToolTip("Ins")
        self.add_comment_btn.clicked.connect(self.add_comment)
        self.add_comment_btn.setEnabled(False)
        button_layout.addWidget(self.add_comment_btn)
        shortcut = QShortcut(QKeySequence("Ins"), self)
        shortcut.activated.connect(self.add_comment_btn.click)

        self.stored_key = ""
        self.xkbcommon_key = ""
        self.mod = ""
        self.mod5 = ""
        self.allow_locked = ""
        self.repeat_false = ""
        self.mousebind = ""

        keypress_layout = QFormLayout(self)
        self.label = QLabel(self.tr("Add a shortcut:"))
        self.key_edit = QKeySequenceEdit()
        self.key_edit.setToolTip(self.tr("'Super' (Meta) key is identical with 'Mod' by default.\n Select a line to insert the shortcut otherwise it will be added at the bottom.\nThe shortcut field doesn’t detect AltGr, use the checkbox instead.\nIf niri shows an error validate 'keybinds.kdl' in the next tab."))
        self.key_edit.setClearButtonEnabled(True)
        self.key_edit.setMaximumSequenceLength(1)
        self.key_edit.keySequenceChanged.connect(self.on_changed)
        keypress_layout.addRow(self.label, self.key_edit)

        options_layout = QHBoxLayout()
        self.mod_checkbox = QCheckBox(self.tr('Add "Mod"'))
        self.mod_checkbox.setEnabled(False)
        self.mod_checkbox.toggled.connect(self.on_toggled_mod)
        self.mod5_checkbox = QCheckBox(self.tr('Add "AltGr"'))
        self.mod5_checkbox.setEnabled(False)
        self.mod5_checkbox.toggled.connect(self.on_toggled_mod5)

        self.repeat_false_checkbox = QCheckBox(self.tr('No repeat'))
        self.repeat_false_checkbox.setToolTip(self.tr("Do not repeat the action. Repeating is default"))
        self.repeat_false_checkbox.setEnabled(False)
        self.repeat_false_checkbox.toggled.connect(self.on_toggled_repeat)
        self.allow_locked_checkbox = QCheckBox(self.tr('Allow when locked'))
        self.allow_locked_checkbox.setToolTip(self.tr("Allow execution when screen is locked"))
        self.allow_locked_checkbox.setEnabled(False)
        self.allow_locked_checkbox.toggled.connect(self.on_toggled_locked)

        options_layout.addWidget(self.mod_checkbox)
        options_layout.addWidget(self.mod5_checkbox)
        options_layout.addWidget(self.repeat_false_checkbox)
        options_layout.addWidget(self.allow_locked_checkbox)
        options_layout.addStretch()

        mousebinds_layout =QHBoxLayout()
        self.overlay_checkbox = QCheckBox(self.tr("No overlay"))
        self.overlay_checkbox.setToolTip(self.tr("Do not show in the hotkey overlay"))
        self.mousebinds_checkbox = QCheckBox(self.tr("Add mousebind:"))
        self.mousebinds_combobox = QComboBox()
        self.mousebinds_combobox.addItems(["MouseLeft", "MouseRight" ,"MouseMiddle","MouseForward", "MouseBack","WheelScrollDown","WheelScrollUp", "WheelScrollRight","WheelScrollLeft","TouchpadScrollDown","TouchpadScrollUp"])
        self.mousebinds_checkbox.setChecked(False)
        self.mousebinds_combobox.setEnabled(False)

        self.mousebinds_checkbox.toggled.connect(self.on_mousebinds)
        self.mousebinds_checkbox.toggled.connect(self.on_mousebind_checked)
        self.mousebinds_checkbox.toggled.connect(self.mousebinds_combobox.setEnabled)
        self.mousebinds_combobox.setEnabled(self.mousebinds_checkbox.isChecked())

        self.mod_checkbox.setChecked(self.mousebinds_checkbox.isChecked())
        self.mod_checkbox.setEnabled(self.mousebinds_checkbox.isChecked())
        self.mousebinds_checkbox.toggled.connect(self.mod_checkbox.setChecked)
        self.mousebinds_combobox.currentTextChanged.connect(self.on_mousebind_changed)

        #mousebinds_layout.addWidget(self.overlay_checkbox)
        mousebinds_layout.addWidget(self.mousebinds_checkbox)
        mousebinds_layout.addWidget(self.mousebinds_combobox)
        mousebinds_layout.addSpacing(20)
        mousebinds_layout.addStretch()

        bottom_layout.addLayout(button_layout)
        bottom_layout.addSpacing(15)
        bottom_layout.addLayout(keypress_layout)
        bottom_layout.addLayout(options_layout)
        bottom_layout.addLayout(mousebinds_layout)
        bottom_layout.addSpacing(10)
        bottom_layout.addLayout(add_button_layout)

        # Status label
        self.status_label = QLabel()
        bottom_layout.addWidget(self.status_label)
        font = QFont()
        font.setItalic(True)
        self.status_label.setFont(font)

        # Add bottom panel to splitter
        splitter.addWidget(bottom_panel)

        # Set initial splitter sizes
        splitter.setSizes([400, 150])

        # Add splitter to layout
        layout.addWidget(splitter)

    def showEvent(self, event):
        super().showEvent(event)
        self.filter_input.setFocus()

    def load_file(self):
        """Load file content into list widget, create if empty"""
        try:
            # Check if file exists and is empty
            if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
                # Create initial structure
                with open(self.filename, 'w') as file:
                    file.write("// keybinds managed by niri-settings. Consider moving existing binds here.\nbinds {\n}\n")
                self.status_label.setText(self.tr("Created new keybinds file"))

            # Read file
            with open(self.filename, 'r') as file:
                self.lines = file.readlines()

            self.update_list_display()
            self.status_label.setText(
            self.tr("Loaded %1 lines").replace("%1", str(len(self.lines)))
            )

        except Exception as e:
            self.status_label.setText(f"Error loading file: {str(e)}")

    def filter_lines(self):
        filter_text = self.filter_input.text().lower()

        if not filter_text:
            self.update_list_display()
            return

        self.list_widget.clear()
        filtered_count = 0

        for i, line in enumerate(self.lines):
            line_text = line.rstrip('\n').lower()
            if filter_text in line_text:
                display_text = self.lines[i].rstrip('\n')
                self.list_widget.addItem(display_text)
                filtered_count += 1
        self.filter_count.setText(
        self.tr("%1 matching").replace("%1", str(filtered_count))
        )

    def update_list_display(self):
        self.list_widget.clear()
        for line in self.lines:
            display_text = line.rstrip('\n')
            self.list_widget.addItem(display_text)
        self.filter_count.setText("")

    def on_item_clicked(self, item):
        # safeguards for brackets: no deleting, no adding after closing bracket
        second_item = self.list_widget.item(1)
        second_item.setFlags(second_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        second_item.setFlags(second_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
        last_item = self.list_widget.item(self.list_widget.count() - 1)
        last_item.setFlags(last_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        last_item.setFlags(last_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
        row = self.list_widget.row(item)
        if row == self.list_widget.count() - 1:
            return

        # If filtered, find the actual index in original lines
        if self.filter_input.text():
            filter_text = self.filter_input.text().lower()
            filtered_indices = []
            for i, line in enumerate(self.lines):
                if filter_text in line.lower():
                    filtered_indices.append(i)

            if row < len(filtered_indices):
                self.selected_index = filtered_indices[row]
            else:
                self.selected_index = row
        else:
            self.selected_index = row

        self.original_text = self.lines[self.selected_index].rstrip('\n')
        self.text_edit.setPlainText(self.original_text)

        self.save_btn.setEnabled(False)  # disabled until content actually changes
        self.text_edit.textChanged.connect(self.on_text_changed)

        self.add_comment_btn.setEnabled(True)
        self.remove_btn.setEnabled(True)
        self.status_label.setText(
        self.tr("Editing line %1").replace("%1", str(self.selected_index + 1))
        )

    def save_line(self):
        if hasattr(self, 'selected_index'):
            new_text = self.text_edit.toPlainText()
            self.lines[self.selected_index] = new_text + '\n'

            try:
                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                # Update the list display
                if self.filter_input.text():
                    self.filter_lines()
                else:
                    display_text = new_text
                    self.list_widget.item(self.selected_index).setText(display_text)

                self.status_label.setText(
                self.tr("Saved line %1").replace("%1", str(self.selected_index + 1))
                )

                self.text_edit.clear()
                self.save_btn.setEnabled(False)

            except Exception as e:
                self.status_label.setText(
                self.tr("Error saving file: %1").replace("%1", str(e))
                )

    def delete_line(self):
        if hasattr(self, 'selected_index'):
            try:
                # Remove from the internal list
                del self.lines[self.selected_index]

                # Rewrite file
                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                self.list_widget.takeItem(self.selected_index)
                self.status_label.setText(
                self.tr("Line %1 deleted").replace("%1", str(self.selected_index + 1))
                )

                self.text_edit.clear()

                self.filter_input.text()
                self.filter_lines()
                self.list_widget.setCurrentRow(self.selected_index)

                # Reapply filter if needed
                if self.filter_input.text():
                    self.filter_lines()

            except Exception as e:
                self.status_label.setText(
                self.tr("Error deleting line %1").replace("%1", str(e))
                )

    def add_application(self):
        new_line, ok = QInputDialog.getText(
            self,
            "Add Command",
            "Add a single command without arguments\nExample: firefox" ,
            QLineEdit.EchoMode.Normal,
            ""
        )

        if ok and new_line:
            if 'LXQt' in desktop_list:
                command = f'spawn-sh "lxqt-qdbus run {new_line}"'
                new_line = f"    {self.mod}{self.mod5}{self.mousebind}{self.xkbcommon_key}{self.allow_locked} {self.repeat_false} {{ {command} ; }}\n"
            else:
                command = f'spawn "{new_line}"'
                new_line = f"    {self.mod}{self.mod5}{self.mousebind}{self.xkbcommon_key}{self.allow_locked}{self.repeat_false} {{ {command} ; }}\n"

            try:
                if not hasattr(self, 'selected_index'):
                    self.selected_index = len(self.lines) - 1
                else:
                    self.selected_index = self.selected_index + 1

                self.lines.insert(self.selected_index, new_line)

                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                self.filter_input.text()
                self.filter_lines()
                self.list_widget.setCurrentRow(self.selected_index)
                self.reset_add_keybind()
                self.status_label.setText(
                self.tr("Added new shortcut at line %1").replace("%1", str(self.selected_index + 1))
                )

            except Exception as e:
                self.status_label.setText(
                self.tr("Error adding shortcut: %1").replace("%1", str(e))
                )

    def add_cmd_sh(self):
        new_command, ok = QInputDialog.getText(
            self,
            "Add Command",
            "Add a shell command with arguments\n\nExamples: firefox -p myprofile\ncopy show\n",
            QLineEdit.EchoMode.Normal,
            ""
        )

        if ok and new_command:
            command = f'spawn-sh "{new_command}"'
            new_line = f"    {self.mod}{self.mod5}{self.mousebind}{self.xkbcommon_key}{self.allow_locked}{self.repeat_false} {{ {command} ; }}\n"

            try:
                if not hasattr(self, 'selected_index'):
                    self.selected_index = len(self.lines) - 1
                else:
                    self.selected_index = self.selected_index + 1

                self.lines.insert(self.selected_index, new_line)

                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                self.filter_input.text()
                self.filter_lines()
                self.list_widget.setCurrentRow(self.selected_index)
                self.reset_add_keybind()
                self.status_label.setText(
                    self.tr("Added new shortcut at line %1").replace("%1", str(self.selected_index + 1))
                )

            except Exception as e:
                self.status_label.setText(
                self.tr("Error adding shortcut: %1").replace("%1", str(e))
                )

    def add_comment(self): # now: add custom line
        if hasattr(self, 'selected_index'):
            comment, ok = QInputDialog.getText(
                self,
                "Add a custom line",
                "Add a comment, 'e.g. // my comment', an empty line or else:",
                QLineEdit.EchoMode.Normal,
                ""
            )

            if ok:
                comment_to_add = f"    {comment}\n"
                self.selected_index = self.selected_index + 1
                self.lines.insert(self.selected_index, comment_to_add)

                try:
                    with open(self.filename, 'w') as file:
                        file.writelines(self.lines)

                    self.filter_input.text()
                    self.filter_lines()
                    self.save_btn.setEnabled(False)
                    self.remove_btn.setEnabled(False)
                    self.text_edit.clear()
                    self.status_label.setText(
                    self.tr("Custom line saved at line %1").replace("%1", str(self.selected_index+1))
                    )

                except Exception as e:
                    self.status_label.setText(
                    self.tr("Error saving custom line: %1").replace("%1", str(e))
                    )

    def add_niri_action(self):
        actions = self.niri_actions
        action, ok = QInputDialog.getItem(
            self,
            "Add niri action",
            "Select a niri action:",
            actions,
            0,
            editable=True
        )

        if ok and action:
            new_line = f"    {self.mod}{self.mod5}{self.mousebind}{self.xkbcommon_key}{self.allow_locked} {self.repeat_false}{{ {action}; }}\n"

            try:
                if not hasattr(self, 'selected_index'):
                    self.selected_index = len(self.lines) - 1
                else:
                    self.selected_index = self.selected_index + 1

                self.lines.insert(self.selected_index, new_line)

                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                self.filter_input.text()
                self.filter_lines()
                self.list_widget.setCurrentRow(self.selected_index)
                self.reset_add_keybind()
                self.status_label.setText(
                self.tr("Added new shortcut at line %1").replace("%1", str(self.selected_index + 1))
                )

            except Exception as e:
                self.status_label.setText(
                self.tr("Error adding shortcut: %1").replace("%1", str(e))
                )

    def on_text_changed(self):
        current = self.text_edit.toPlainText()
        self.save_btn.setEnabled(current != self.original_text)

    def reset_add_keybind(self):
        self.key_edit.clear()
        self.xkbcommon_key = ""
        self.add_cmd_btn.setEnabled(False)
        self.add_cmd_sh_btn.setEnabled(False)
        self.add_action_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.remove_btn.setEnabled(False)
        self.mod_checkbox.setEnabled(False)
        self.mod5_checkbox.setEnabled(False)
        self.allow_locked_checkbox.setEnabled(False)
        self.repeat_false_checkbox.setEnabled(False)
        self.mod_checkbox.setChecked(False)
        self.mod5_checkbox.setChecked(False)
        self.allow_locked_checkbox.setChecked(False)
        self.repeat_false_checkbox.setChecked(False)
        self.mousebinds_checkbox.setChecked(False)
        self.mousebinds_checkbox.setEnabled(True)
        self.mousebinds_checkbox.setChecked(False)

    def on_mousebind_checked(self):
        self.stored_key = ""
        self.trigger_label.setEnabled(True)
        self.add_cmd_btn.setEnabled(True)
        self.add_cmd_sh_btn.setEnabled(True)
        self.add_action_btn.setEnabled(True)
        self.mod_checkbox.setEnabled(True)
        self.mod5_checkbox.setEnabled(True)

    def on_changed(self, seq):
        if seq.isEmpty():
            self.stored_key = ""
            self.trigger_label.setEnabled(False)
            self.add_cmd_btn.setEnabled(False)
            self.add_cmd_sh_btn.setEnabled(False)
            self.add_action_btn.setEnabled(False)
            self.mousebinds_checkbox.setEnabled(True)
            self.mod_checkbox.setEnabled(False)
            self.mod5_checkbox.setEnabled(False)
            self.allow_locked_checkbox.setEnabled(False)
            self.repeat_false_checkbox.setEnabled(False)
        else:
            self.stored_key = seq.toString()
            self.trigger_label.setEnabled(True)
            self.add_cmd_btn.setEnabled(True)
            self.add_cmd_sh_btn.setEnabled(True)
            self.add_action_btn.setEnabled(True)
            self.mod_checkbox.setEnabled(True)
            self.mod5_checkbox.setEnabled(True)
            self.allow_locked_checkbox.setEnabled(True)
            self.repeat_false_checkbox.setEnabled(True)
            self.mousebinds_checkbox.setEnabled(False)
            self.mousebinds_checkbox.setChecked(False)
            self.text_edit.clear()
            self.save_btn.setEnabled(False)

        if self.stored_key:
            conversion = self.stored_key
            conversion = conversion.replace("Meta", "Super")
            conversion = conversion.replace("Esc", "escape")
            conversion = conversion.replace("-", "minus")
            conversion = conversion.replace("=", "equal")
            conversion = conversion.replace("[", "bracketleft")
            conversion = conversion.replace("]", "bracketright")
            conversion = conversion.replace("{", "braceleft")
            conversion = conversion.replace("}", "braceright")
            conversion = conversion.replace(";", "semicolon")
            conversion = conversion.replace(":", "colon")
            conversion = conversion.replace("'", "apostrophe")
            conversion = conversion.replace('"', "quotedbl")
            conversion = conversion.replace(",", "comma")
            conversion = conversion.replace(".", "period")
            conversion = conversion.replace("<", "less")
            conversion = conversion.replace(">", "greater")
            conversion = conversion.replace("/", "slash")
            conversion = conversion.replace("?", "question")
            conversion = conversion.replace("\\", "backslash")
            conversion = conversion.replace("|", "bar")
            conversion = conversion.replace("`", "grave")
            conversion = conversion.replace("~", "asciitilde")
            conversion = conversion.replace("!", "exclam")
            conversion = conversion.replace("@", "at")
            conversion = conversion.replace("#", "numbersign")
            conversion = conversion.replace("$", "dollar")
            conversion = conversion.replace("%", "percent")
            conversion = conversion.replace("^", "asciicircum")
            conversion = conversion.replace("&", "ampersand")
            conversion = conversion.replace("*", "asterisk")
            conversion = conversion.replace("(", "parenleft")
            conversion = conversion.replace(")", "parenright")
            conversion = conversion.replace("_", "underscore")
            conversion = conversion.replace("++", "+plus") # otherwise breaks all others...

            self.xkbcommon_key = conversion

    def on_toggled_mod(self, checked):
        if checked:
            self.mod = "Mod+"
        else:
            self.mod = ""

    def on_toggled_mod5(self, checked):
        if checked:
            self.mod5 = "Mod5+"
        else:
            self.mod5 = ""

    def on_toggled_locked(self, checked):
        if checked:
            self.allow_locked = " allow-when-locked=true"
        else:
            self.allow_locked = ""

    def on_toggled_repeat(self, checked):
        if checked:
            self.repeat_false = " repeat=false"
        else:
            self.repeat_false = ""

    def on_mousebinds(self, checked):
        if checked:
            self.on_mousebind_changed(self.mousebinds_combobox.currentText())
        else:
            self.mousebind = ""

    def on_mousebind_changed(self, text):
        if self.mousebinds_checkbox.isChecked():
            mousebind = self.mousebinds_combobox.currentText()
            if  "Mouse" not in mousebind:
                self.mousebind = f"{mousebind} cooldown-ms=150"
            else:
                self.mousebind = f"{mousebind}"
        else:
            self.mousebind = ""

def get_keybind_config_path():
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        # Ensure the directory exists
        config_dir = os.path.dirname(config_path)
        if config_dir:  # Only create if path has a directory component
            os.makedirs(config_dir, exist_ok=True)
        return config_path
    else:
        if 'LXQt' in desktop_list:
            default_path = os.path.join(
                os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
                'lxqt', 'wayland', 'niri', 'keybinds.kdl'
            )
        else:
            default_path = os.path.join(
                os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
                'niri', 'keybinds.kdl'
            )
        # Ensure the directory exists
        config_dir = os.path.dirname(default_path)
        os.makedirs(config_dir, exist_ok=True)
        return default_path
