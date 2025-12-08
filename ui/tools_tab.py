from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,QLabel, QPushButton,
                             QGroupBox,QMessageBox, QPlainTextEdit)
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QFont

import subprocess

class ToolsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Toolbox")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        button_group = QGroupBox(self.tr("Lists"))
        button_layout = QHBoxLayout(button_group)

        List_label = QLabel(self.tr(':'))
        windows_btn = QPushButton(self.tr("Windows"))
        windows_btn.clicked.connect(self.list_windows)
        button_layout.addWidget(windows_btn)

        workspaces_btn = QPushButton(self.tr("Workspaces"))
        workspaces_btn.clicked.connect(self.list_workspaces)
        button_layout.addWidget(workspaces_btn)

        layers_btn = QPushButton(self.tr("Layers"))
        layers_btn.clicked.connect(self.list_layers)
        button_layout.addWidget(layers_btn)

        outputs_btn = QPushButton(self.tr("Monitors"))
        outputs_btn.clicked.connect(self.list_outputs)
        button_layout.addWidget(outputs_btn)

        xwayland_btn = QPushButton(self.tr("Xwayland windows"))
        xwayland_btn.clicked.connect(self.list_xwayland)
        button_layout.addWidget(xwayland_btn)

        button_layout.addStretch()

        # Info
        button_info_group = QGroupBox(self.tr("Information"))
        button_layout = QHBoxLayout(button_info_group)

        focused_window_btn = QPushButton(self.tr("Window"))
        focused_window_btn.clicked.connect(self.list_focused_window)
        button_layout.addWidget(focused_window_btn)

        focused_monitor_btn = QPushButton(self.tr("Monitor"))
        focused_monitor_btn.clicked.connect(self.list_focused_monitor)
        button_layout.addWidget(focused_monitor_btn)

        show_version_btn = QPushButton(self.tr("niri version"))
        show_version_btn.clicked.connect(self.show_version)
        button_layout.addWidget(show_version_btn)

        process_tree_btn = QPushButton(self.tr("Processes"))
        process_tree_btn.clicked.connect(self.process_tree)
        button_layout.addWidget(process_tree_btn)

        event_stream_btn = QPushButton(self.tr("Event Stream"))
        event_stream_btn.clicked.connect(self.event_stream_selected)
        button_layout.addWidget(event_stream_btn)
        button_layout.addStretch()

        # Actions
        button_actions_group = QGroupBox(self.tr("Actions"))
        button_layout = QHBoxLayout(button_actions_group)

        kill_window_btn = QPushButton(self.tr("Kill a window"))
        kill_window_btn.clicked.connect(self.kill_window)
        button_layout.addWidget(kill_window_btn)

        pick_color_btn = QPushButton(self.tr("Pick color"))
        pick_color_btn.clicked.connect(self.pick_color)
        button_layout.addWidget(pick_color_btn)

        to_do_btn = QPushButton(self.tr("New action"))
        #to_do_btn.clicked.connect(self.to_do_selected)
        #button_layout.addWidget(to_do_btn)
        button_layout.addStretch()

        layout.addWidget(button_group)
        layout.addWidget(button_info_group)
        layout.addWidget(button_actions_group)
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        font = QFont("Monospace")
        self.terminal.setFont(font)

        layout.addWidget(self.terminal)

    def run_proc(self, program, args):
        proc = QProcess(self)
        proc.setProgram(program)
        proc.setArguments(args)

        proc.readyReadStandardOutput.connect(
            lambda: self.terminal.appendPlainText(
                bytes(proc.readAllStandardOutput()).decode()
            )
        )

        self.terminal.clear()
        proc.start()
        return proc

    def event_stream_selected(self):
        self.proc = self.run_proc("niri", ["msg", "event-stream"])

    def list_windows(self):
        self.proc = self.run_proc("niri", ["msg", "windows"])


    def list_workspaces(self):
        self.proc = self.run_proc("niri", ["msg", "workspaces"])

    def list_layers(self):
        self.proc = self.run_proc("niri", ["msg", "layers"])
        self.proc.setProgram("niri")

    def list_outputs(self):
        self.proc = self.run_proc("niri", ["msg", "outputs"])

    def list_xwayland(self):
        self.proc = self.run_proc("sh", ["-c","xlsclients -a | awk '{print $2}'"])

    def list_focused_window(self):
        self.proc = self.run_proc("niri", ["msg", "pick-window"])

    def list_focused_monitor(self):
        self.proc = self.run_proc("niri", ["msg", "focused-output"])

    def show_version(self):
        self.proc = self.run_proc("niri", ["msg", "version"])

    def process_tree(self):
        self.proc = self.run_proc("sh", ["-c","ps f"])

    def pick_color(self):
        #self.proc = self.run_proc("niri", ["msg", "pick-color"])
        self.proc = self.run_proc("sh",["-c","niri msg pick-color |grep Hex | cut -c 6-|wl-copy -t text/plain && notify-send -a 'niri' -t 2000 -i 'niri-settings' 'Color copied to clipboard'"])

    def kill_window(self):
        self.pick_proc = QProcess(self)
        self.pick_proc.setProgram("niri")
        self.pick_proc.setArguments(["msg", "pick-window"])

        self.pick_proc.finished.connect(self._pick_finished)
        self.pick_proc.start()

    def _pick_finished(self, exitCode, exitStatus):
        out = bytes(self.pick_proc.readAllStandardOutput()).decode()

        pid = None
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("PID:"):
                pid = line.split(":")[1].strip()
                break

        if not pid:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Not a window but maybe a layer surface?"))
            return

        reply = QMessageBox.question(
            self,
            self.tr("Confirm"),
            self.tr("Are you sure to kill this window\nwith PID {}?").format(pid),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.run_proc("kill", ["-9", pid])
