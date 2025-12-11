from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton,
                             QLabel, QScrollArea, QFrame, QButtonGroup, QPushButton, QCheckBox,QGridLayout,
                             QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit, QGroupBox, QColorDialog,
                             QListWidget, QListWidgetItem, QMenu, QMessageBox, QPlainTextEdit, QSplitter,
                             QDialog, QDialogButtonBox,QInputDialog, QFormLayout, QLabel, QKeySequenceEdit
                             )
import sys

from PyQt6.QtCore import Qt, QTimer, QProcess
from PyQt6.QtGui import QFont, QColor, QAction, QCursor

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

        # Create the file editor widget
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

    def initUI(self):
        layout = QVBoxLayout(self)

        # Label
        self.label = QLabel(f"Editing: {self.filename}")
        layout.addWidget(self.label)

        # Create a splitter for horizontal division
        splitter = QSplitter(Qt.Orientation.Vertical)

        # TOP PANEL: Filter and List
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel(self.tr("Filter:")))

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText(self.tr("Type to filter..."))
        self.filter_input.textChanged.connect(self.filter_lines)
        self.filter_input.setClearButtonEnabled(True)
        self.filter_input.setClearButtonEnabled(True)

        filter_layout.addWidget(self.filter_input)

        self.filter_count = QLabel("")
        filter_layout.addWidget(self.filter_count)

        top_layout.addLayout(filter_layout)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        top_layout.addWidget(self.list_widget)

        # Add top panel to splitter
        splitter.addWidget(top_panel)

        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)

        # Edit area label
        edit_label = QLabel(self.tr("Edit selected shortcut:"))
        bottom_layout.addWidget(edit_label)

        # Text editor
        self.text_edit = QPlainTextEdit()
        self.text_edit.setMaximumHeight(80)
        bottom_layout.addWidget(self.text_edit)

        # Button layouts
        button_layout = QHBoxLayout()
        add_button_layout = QHBoxLayout()

        self.save_btn = QPushButton(self.tr("Save edit"))
        self.save_btn.clicked.connect(self.save_line)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

        self.remove_btn = QPushButton(self.tr("Remove this line"))
        self.remove_btn.clicked.connect(self.delete_line)
        self.remove_btn.setEnabled(False)
        button_layout.addWidget(self.remove_btn)
        button_layout.addStretch()

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

        self.add_comment_btn = QPushButton(self.tr("Insert comment"))
        self.add_comment_btn.clicked.connect(self.add_comment)
        self.add_comment_btn.setEnabled(False)
        button_layout.addWidget(self.add_comment_btn)

        self.stored_key = ""
        self.xkbcommon_key = ""
        self.mod = ""
        self.mod5 = ""
        self.allow_locked = ""
        self.repeat_false = ""

        keypress_layout = QFormLayout(self)
        self.label = QLabel(self.tr("Add a shortcut:"))
        self.key_edit = QKeySequenceEdit()
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
        self.repeat_false_checkbox = QCheckBox(self.tr('No repeating'))
        self.repeat_false_checkbox.setEnabled(False)
        self.repeat_false_checkbox.toggled.connect(self.on_toggled_repeat)
        self.allow_locked_checkbox = QCheckBox(self.tr('Allow when locked'))
        self.allow_locked_checkbox.setEnabled(False)
        self.allow_locked_checkbox.toggled.connect(self.on_toggled_locked)

        options_layout.addWidget(self.mod_checkbox)
        options_layout.addWidget(self.mod5_checkbox)
        options_layout.addWidget(self.repeat_false_checkbox)
        options_layout.addWidget(self.allow_locked_checkbox)
        options_layout.addStretch()

        bottom_layout.addLayout(button_layout)
        bottom_layout.addSpacing(15)
        # Notes
        self.notes_label = QLabel(self.tr("Note: The input doesn't read 'Meta' and 'ALtGr' keys, use the checkboxes instead.\nIf niri shows an error validate 'keybinds.kdl' in the next tab."))
        #self.notes_label.setEnabled(False)
        bottom_layout.addWidget(self.notes_label)
        bottom_layout.addLayout(keypress_layout)
        bottom_layout.addLayout(options_layout)
        bottom_layout.addLayout(add_button_layout)

        # Status label
        self.status_label = QLabel(self.tr("Select a keybind line to edit"))
        bottom_layout.addWidget(self.status_label)

        # Add bottom panel to splitter
        splitter.addWidget(bottom_panel)

        # Set initial splitter sizes (top 70%, bottom 30%)
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
            self.status_label.setText(f"Loaded {len(self.lines)} lines")

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

        self.filter_count.setText(f"({filtered_count} matching)")

    def update_list_display(self):
        self.list_widget.clear()
        for line in self.lines:
            display_text = line.rstrip('\n')
            self.list_widget.addItem(display_text)
        self.filter_count.setText("")

    def on_item_clicked(self, item):
        row = self.list_widget.row(item)

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
        self.status_label.setText(f"Editing line {self.selected_index + 1}")

    def save_line(self):
        if hasattr(self, 'selected_index'):
            new_text = self.text_edit.toPlainText()
            self.lines[self.selected_index] = new_text + '\n'

            # Write back to file
            try:
                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                # Update the list display
                if self.filter_input.text():
                    self.filter_lines()
                else:
                    display_text = new_text
                    self.list_widget.item(self.selected_index).setText(display_text)

                self.status_label.setText(f"Line {self.selected_index + 1} saved")
                self.text_edit.clear()
                self.save_btn.setEnabled(False)

            except Exception as e:
                self.status_label.setText(f"Error saving file: {str(e)}")

    def delete_line(self):
        if hasattr(self, 'selected_index'):
            try:
                # Remove from the internal list
                del self.lines[self.selected_index]

                # Rewrite file
                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                # Update UI
                self.list_widget.takeItem(self.selected_index)
                self.status_label.setText(f"Line {self.selected_index + 1} deleted")

                # Clear selection & editor
                self.selected_index = None #FIXME doesn't remove selection
                self.text_edit.clear()

                # Reapply filter if needed
                if self.filter_input.text():
                    self.filter_lines()

            except Exception as e:
                self.status_label.setText(f"Error deleting line: {str(e)}")

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
                new_line = f"    {self.mod}{self.mod5}{self.xkbcommon_key} {self.allow_locked} {self.repeat_false} {{ {command} ; }}\n"
            else:
                command = f'spawn "{new_line}"'
                new_line = f"    {self.mod}{self.mod5}{self.xkbcommon_key} {self.allow_locked} {self.repeat_false} {{ {command} ; }}\n"

            try:
                # Find the last line (should be "}") #FIXME add at current index if there is
                last_line_index = len(self.lines) - 1

                # Insert before the last line
                self.lines.insert(last_line_index, new_line)

                # Write back to file
                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                # Update the list display
                self.update_list_display()

                # Select and scroll to the new line
                new_index = last_line_index  # Because we inserted before last line
                self.list_widget.setCurrentRow(new_index)
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
                self.status_label.setText(f"Added new application shortcut at line {new_index + 1}")

            except Exception as e:
                self.status_label.setText(f"Error adding application shortcut: {str(e)}")

    def add_cmd_sh(self):
        """Add a shell cmd before closing bracket"""
        new_line, ok = QInputDialog.getText(
            self,
            "Add Command",
            "Add a shell command with arguments\n\nExamples: firefox -p myprofile\ncopy show\n",
            QLineEdit.EchoMode.Normal,
            ""
        )

        if ok and new_line:
            command = f'spawn-sh "{new_line}"'
            new_line = f"    {self.mod}{self.mod5}{self.xkbcommon_key} {self.allow_locked} {self.repeat_false} {{ {command} ; }}\n"

            try:
                last_line_index = len(self.lines) - 1
                self.lines.insert(last_line_index, new_line)

                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                # Update the list display
                self.update_list_display()

                # Select and scroll to the new line
                new_index = last_line_index  # Because we inserted before last line
                self.list_widget.setCurrentRow(new_index)
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
                self.status_label.setText(f"Added new shell keybind at line {new_index + 1}")

            except Exception as e:
                self.status_label.setText(f"Error adding shell command: {str(e)}")

    def add_comment(self):
        if hasattr(self, 'selected_index'):
            comment, ok = QInputDialog.getText(
                self,
                "Add a comment",
                "Add a comment for this keybind:",
                QLineEdit.EchoMode.Normal,
                ""
            )

            if ok and comment:
                comment_to_add = f"    // {comment}\n"
                self.lines.insert(self.selected_index, comment_to_add)

                try:
                    with open(self.filename, 'w') as file:
                        file.writelines(self.lines)

                    #display_text = comment_to_add
                    self.filter_input.text()
                    self.filter_lines()
                    #self.filter_lines(comment)
                    #self.list_widget.item(self.selected_index).setText(display_text)
                    self.save_btn.setEnabled(False)
                    self.remove_btn.setEnabled(False)
                    self.status_label.setText(f"Comment saved at line {self.selected_index+1}")

                except Exception as e:
                    self.status_label.setText(f"Error saving file: {str(e)}")

    def add_niri_action(self):
        new_line, ok = QInputDialog.getText(
            self,
            "Add niri action",
            "Add a niri action\nExamples: consume-or-expel-window-right\ntoggle-overview\n\nSee `niri msg action` for all actions.",
            QLineEdit.EchoMode.Normal,
            ""
        )

        if ok and new_line:
            new_line = f"    {self.mod}{self.mod5}{self.xkbcommon_key} {self.allow_locked} {self.repeat_false}{{ {new_line}; }}\n"

            try:
                last_line_index = len(self.lines) - 1
                self.lines.insert(last_line_index, new_line)

                with open(self.filename, 'w') as file:
                    file.writelines(self.lines)

                self.update_list_display()

                new_index = last_line_index
                self.list_widget.setCurrentRow(new_index)
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
                self.status_label.setText(f"Added new niri action keybind at line {new_index + 1}")

            except Exception as e:
                self.status_label.setText(f"Error adding niri action: {str(e)}")

    def on_text_changed(self):
        current = self.text_edit.toPlainText()
        self.save_btn.setEnabled(current != self.original_text)


    def on_changed(self, seq):
        self.key_edit.setKeySequence(seq)
        self.stored_key = seq.toString()
        self.trigger_label.setEnabled(True)
        self.add_cmd_btn.setEnabled(True)
        self.add_cmd_sh_btn.setEnabled(True)
        self.add_action_btn.setEnabled(True)
        self.mod_checkbox.setEnabled(True)
        self.mod5_checkbox.setEnabled(True)
        self.allow_locked_checkbox.setEnabled(True)
        self.repeat_false_checkbox.setEnabled(True)
        #self.notes_label.setEnabled(True)

        if self.stored_key:
            conversion = self.stored_key
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
        #else:
        #    self.xkbcommon_key = ""
        #print(f"Qt: '{self.stored_key}' -> xkbcommon: '{self.xkbcommon_key}'")

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
            self.allow_locked = "allow-when-locked=true"
        else:
            self.allow_locked = ""

    def on_toggled_repeat(self, checked):
        if checked:
            self.repeat_false = "repeat=false"
        else:
            self.repeat_false = ""

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
