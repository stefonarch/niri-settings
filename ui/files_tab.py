from PyQt6.QtWidgets import (QApplication, QInputDialog, QWidget, QVBoxLayout, QHBoxLayout,QLabel, QScrollArea,
                             QPushButton, QCheckBox,QListWidget, QListWidgetItem, QMenu, QMessageBox,
                             QPlainTextEdit, QStyle, QSplitter
                             )
from PyQt6.QtCore import Qt, QTimer, QProcess, QFile,QRegularExpression
from PyQt6.QtGui import QFont, QAction, QShortcut, QKeySequence, QPalette, QColor,QSyntaxHighlighter,                                                 QTextCharFormat

from pathlib import Path
import os, re, sys, subprocess, shutil
from .kdl_highlighter import KdlHighlighter

class FilesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_kdl_files()
        self.kdl_highlighter = KdlHighlighter(
            self.terminal.document()
        )

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel(self.tr("Configuration Files"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Create a splitter
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Top panel (list and buttons)
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)

        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        top_layout.addWidget(self.list_widget)

        self.home = os.path.expanduser("~")

        button_layout = QHBoxLayout()

        self.save_btn = QPushButton(self.tr("Save"))
        self.save_btn.setToolTip("Ctrl+S")
        self.save_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.save_btn.clicked.connect(self.save_selected)
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self.save_btn.click)
        self.save_btn.setEnabled(False)

        self.validate_btn = QPushButton(self.tr("Validate"))
        self.validate_btn.setToolTip("Ctrl+V")
        self.validate_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning))
        self.validate_btn.clicked.connect(self.validate_selected)
        shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        shortcut.activated.connect(self.validate_btn.click)
        self.validate_btn.setEnabled(False)

        self.backup_btn = QPushButton(self.tr("Backup"))
        self.backup_btn.setToolTip("Ctrl+B")
        self.backup_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileLinkIcon))
        self.backup_btn.clicked.connect(self.backup_selected)
        shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        shortcut.activated.connect(self.backup_btn.click)
        self.backup_btn.setEnabled(False)

        self.refresh_btn = QPushButton(self.tr("Refresh"))
        self.refresh_btn.setToolTip("Ctrl+R, update file list")
        self.refresh_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.refresh_btn.clicked.connect(self.refresh_files)
        shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        shortcut.activated.connect(self.refresh_btn.click)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.backup_btn)
        button_layout.addWidget(self.validate_btn)
        button_layout.addWidget(self.refresh_btn)

        button_layout.addStretch()

        self.exclude_backups_checkbox = QCheckBox(self.tr('Hide backups'))
        button_layout.addWidget(self.exclude_backups_checkbox)
        self.exclude_backups_checkbox.toggled.connect(self.refresh_files)

        top_layout.addLayout(button_layout)

        splitter.addWidget(top_panel)

        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)

        self.terminal = QPlainTextEdit()
        font = QFont("Monospace")
        self.terminal.setFont(font)
        self.terminal.setPlaceholderText(self.tr("Click file to edit here\nDouble click to open in text editor\nRight click for other options"))
        self.terminal.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.terminal.setReadOnly(True)

        KdlHighlighter(self.terminal.document())
        bottom_layout.addWidget(self.terminal)

        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Add bottom panel to splitter
        splitter.addWidget(bottom_panel)
        splitter.setSizes([200, 400])

        # Add splitter to layout
        layout.addWidget(splitter)

        pass

    def load_kdl_files(self):
        """Load and display all .kdl* files from the configuration directory."""
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

        self.base_path = base_path# simplify

        if not base_path.exists():  # is that needed?
            self.show_error(self.tr("Directory does not exist:\n{base_path}"))
            return

        if self.exclude_backups_checkbox.isChecked():
            kdl_files = list(base_path.rglob('*.kdl'))
        else:
            kdl_files = list(base_path.rglob('*.kdl*'))

        if not kdl_files:
            self.show_info(self.tr(f"No .kdl files found in:\n{base_path}"))
            return

        for file_path in sorted(kdl_files):
            try:
                rel_path = file_path.relative_to(base_path)
                display_text = str(rel_path)
            except ValueError:
                display_text = str(file_path)

            tooltip_path = str(file_path).replace(self.home, "~", 1)
            item = QListWidgetItem(display_text)
            item.setToolTip(str(tooltip_path))
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
        self.validate_btn.setEnabled(True)
        self.backup_btn.setEnabled(True)
        self.terminal.setReadOnly(False)
        current_item = self.list_widget.currentItem()

        file_path = current_item.data(Qt.ItemDataRole.UserRole)

        self.text = Path(file_path).read_text(encoding="utf-8")
        self.terminal.setPlainText(self.text)
        self.save_btn.setEnabled(False)  # disabled until content actually changes
        self.terminal.textChanged.connect(self.on_text_changed)

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
        open_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        open_action.triggered.connect(lambda: self.open_with_xdg(file_path))
        menu.addAction(open_action)

        show_in_folder_action = QAction(self.tr("Show in file manager"), self)
        show_in_folder_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        show_in_folder_action.triggered.connect(
            lambda: subprocess.Popen(['xdg-open', os.path.dirname(file_path)])
        )
        menu.addAction(show_in_folder_action)

        copy_path_action = QAction(self.tr("Copy path to clipboard"), self)
        copy_path_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileLinkIcon))
        copy_path_action.triggered.connect(
            lambda: QApplication.clipboard().setText(file_path)
        )
        menu.addAction(copy_path_action)

        new_file_action = QAction(self.tr("Create new file here"), self)
        new_file_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        new_file_action.triggered.connect(self.new_file)
        menu.addAction(new_file_action)

        restore_action = QAction(self.tr("Restore from backup"), self)
        restore_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        restore_action.triggered.connect(self.restore_from_backup)
        menu.addAction(restore_action)

        trash_action = QAction(self.tr("Move to trash"), self)
        trash_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        trash_action.triggered.connect(self.move_to_trash)
        menu.addAction(trash_action)

        self.to_trash = file_path

        menu.exec(self.list_widget.mapToGlobal(position))

    def new_file(self):
        name, ok = QInputDialog.getText(
            self,
            "New File",
            "File name:"
        )

        if not ok:
            return

        name = str(name).strip()
        if not name:
            return

        if not name.endswith(".kdl"):
            name += ".kdl"

        current_item = self.list_widget.currentItem()
        file_path = current_item.data(Qt.ItemDataRole.UserRole)
        dir = Path(file_path).parent
        path = dir / name

        try:
            path.touch(exist_ok=False)
        except FileExistsError:
            QMessageBox.warning(
                self,
                "Error",
                f"The file '{name}' already exists."
            )
            return
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not create file:\n{e}"
            )
            return

        with open(path, 'a', encoding='utf-8') as f:
                f.write('// Added by niri-settings\n')

        file = str(path).replace(self.home, "~", 1)
        self.terminal.setPlainText(f"File {file} created.\nIt needs to be included in the main configuration file.")
        self.refresh_files()

    def restore_from_backup(self):
        current_item = self.list_widget.currentItem()
        file_path = current_item.data(Qt.ItemDataRole.UserRole)

        if file_path.endswith(".kdl~"):
            self.show_info(self.tr("Selected a backup file!"))
            return False

        backup_path = file_path + "~"
        ok = QMessageBox.question(
            self,
            self.tr("Confirm"),
            self.tr("Overwrite this file with its backup?"),
        ) == QMessageBox.StandardButton.Yes

        if not ok:
            return

        try:
            if QFile.exists(file_path):
                if not QFile.remove(file_path):
                    raise RuntimeError("Could not remove existing file")

                if not QFile.copy(backup_path, file_path):
                    raise RuntimeError("Could not copy backup file")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not restore from backup: \n{e}"
            )
            return

        info_path = str(file_path).replace(self.home, "~", 1)
        self.terminal.setPlainText(f"File {info_path} restored from backup")
        self.refresh_files()
        QTimer.singleShot(2500, self.clear_terminal)

    def move_to_trash(self):
        reply = QMessageBox.question(
            self,
            self.tr("Confirm"),
            self.tr("Move file to trash?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            QFile.moveToTrash(self.to_trash)
            self.refresh_files()
            self.clear_terminal()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Information", message)

    def refresh_files(self):
        self.list_widget.clear()
        self.load_kdl_files()
        self.save_btn.setEnabled(False)
        self.validate_btn.setEnabled(False)
        self.backup_btn.setEnabled(False)

    def on_text_changed(self):
          self.save_btn.setEnabled(self.terminal.toPlainText() != self.text)

    def clear_terminal(self):
       # self.terminal.textChanged.disconnect(self.on_text_changed)
        self.terminal.blockSignals(True)
        self.terminal.clear()
        self.terminal.blockSignals(False)
       # self.terminal.textChanged.connect(self.on_text_changed)

    def save_selected(self):
        current_item = self.list_widget.currentItem()
        file_path = current_item.data(Qt.ItemDataRole.UserRole)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.terminal.toPlainText())
        save_path = str(file_path).replace(self.home, "~", 1)
        self.terminal.setPlainText(f"File {save_path} saved")
        self.terminal.setReadOnly(True)
        self.refresh_files()
        QTimer.singleShot(2500, self.clear_terminal)

    def backup_selected(self):
        current_item = self.list_widget.currentItem()
        file_path = current_item.data(Qt.ItemDataRole.UserRole)

        try:
            if not os.path.exists(file_path):
                self.show_info(self.tr(f"File not found: {file_path}"))
                return False

            backup_path = f"{file_path}~"
            shutil.copy2(file_path, backup_path)

            info_path = str(backup_path).replace(self.home, "~", 1)
            self.terminal.setPlainText(f"Backup saved as {info_path}")
            self.refresh_files()
            QTimer.singleShot(2500, self.clear_terminal)

            return True

        except PermissionError:
            self.show_info(self.tr("Permission denied. Cannot create backup."))
            return False
        except Exception as e:
            self.show_info(self.tr(f"Backup failed: {str(e)}"))
            return False

    ansi_escape = re.compile(r'\x1b\[[0-9;]*m') # clean "file is valid" output
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

        info_path = str(file_path).replace(self.home, "~", 1)
        self.terminal.clear()
        self.terminal.appendPlainText(f"$ niri validate -c {info_path}\n")

        self.proc.start()
