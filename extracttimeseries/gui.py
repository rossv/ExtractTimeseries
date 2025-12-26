#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Extractor GUI — v4 (Ported)
"""

from __future__ import annotations

import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PyQt5 import QtCore, QtGui, QtWidgets
from .help_ui import HelpDialog

VERSION = "4.0 (Ported)"

# --- MOCKED HELPERS from hh_tools ---
def apply_dark_palette(app):
    """
    Applies a modern dark theme to the PyQt5 application using a custom palette
    and a comprehensive Qt Style Sheet (QSS).
    """
    app.setStyle("Fusion")

    # 1. Customizable Palette
    dark_bg = QtGui.QColor(30, 30, 30)
    dark_panel = QtGui.QColor(45, 45, 45)
    text_color = QtGui.QColor(220, 220, 220)
    accent_color = QtGui.QColor(60, 140, 220)  # Soft blue
    accent_hover = QtGui.QColor(80, 160, 240)
    border_color = QtGui.QColor(60, 60, 60)
    
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, dark_bg)
    palette.setColor(QtGui.QPalette.WindowText, text_color)
    palette.setColor(QtGui.QPalette.Base, dark_panel)
    palette.setColor(QtGui.QPalette.AlternateBase, dark_bg)
    palette.setColor(QtGui.QPalette.ToolTipBase, dark_panel)
    palette.setColor(QtGui.QPalette.ToolTipText, text_color)
    palette.setColor(QtGui.QPalette.Text, text_color)
    palette.setColor(QtGui.QPalette.Button, dark_panel)
    palette.setColor(QtGui.QPalette.ButtonText, text_color)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Link, accent_color)
    palette.setColor(QtGui.QPalette.Highlight, accent_color)
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.white)
    app.setPalette(palette)

    # 2. Global Font
    # Using 'Segoe UI' as a standard nice font on Windows, fallback to sans-serif
    font = QtGui.QFont("Segoe UI", 9)
    app.setFont(font)

    # 3. Qt Style Sheet (QSS) for "Beautiful" Look
    qss = f"""
    QWidget {{
        color: {text_color.name()};
        font-family: 'Segoe UI', sans-serif;
        font-size: 9pt;
    }}
    
    /* Main Window & Backgrounds */
    QMainWindow, QDialog {{
        background-color: {dark_bg.name()};
    }}
    QGroupBox {{
        border: 1px solid {border_color.name()};
        border-radius: 6px;
        margin-top: 1.2em; /* leave space for the title */
        padding-top: 10px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        color: {accent_color.name()};
        font-weight: bold;
    }}
    
    /* Tabs */
    QTabWidget::pane {{
        border: 1px solid {border_color.name()};
        border-radius: 4px;
        background-color: {dark_panel.name()};
    }}
    QTabBar::tab {{
        background: {dark_bg.name()};
        border: 1px solid {border_color.name()};
        border-bottom-color: {border_color.name()};
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        padding: 8px 30px;
        min-width: 120px;
        margin-right: 2px;
        color: #888;
    }}
    QTabBar::tab:selected, QTabBar::tab:hover {{
        background: {dark_panel.name()};
        color: {text_color.name()};
        border-bottom-color: {dark_panel.name()}; /* Blend with pane */
    }}
    QTabBar::tab:selected {{
        border-top: 2px solid {accent_color.name()};
        font-weight: bold;
    }}

    /* Buttons */
    QPushButton {{
        background-color: {dark_panel.name()};
        border: 1px solid {border_color.name()};
        border-radius: 4px;
        padding: 5px 12px;
        color: {text_color.name()};
    }}
    QPushButton:hover {{
        background-color: #3d3d3d;
        border-color: {accent_color.name()};
    }}
    QPushButton:pressed {{
        background-color: {accent_color.name()};
        color: white;
    }}
    QPushButton:disabled {{
        background-color: #2a2a2a;
        color: #555;
        border-color: #333;
    }}

    /* Input Fields */
    QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: #252525;
        border: 1px solid {border_color.name()};
        border-radius: 4px;
        padding: 4px;
        selection-background-color: {accent_color.name()};
    }}
    QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus, QComboBox:focus {{
        border: 1px solid {accent_color.name()};
        background-color: #2a2a2a;
    }}
    
    /* Lists & Tables */
    QListWidget, QTableWidget, QTreeWidget {{
        background-color: #252525;
        border: 1px solid {border_color.name()};
        border-radius: 4px;
        alternate-background-color: #2a2a2a;
    }}
    QListWidget::item {{
        padding: 4px;
        border-radius: 3px;
    }}
    QListWidget::item:selected {{
        background-color: {accent_color.name()};
        color: white;
    }}
    QListWidget::item:hover:!selected {{
        background-color: #333;
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        border: none;
        background: {dark_bg.name()};
        width: 10px;
        margin: 0px 0px 0px 0px;
    }}
    QScrollBar::handle:vertical {{
        background: #555;
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {accent_color.name()};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        border: none;
        background: {dark_bg.name()};
        height: 10px;
        margin: 0px 0px 0px 0px;
    }}
    QScrollBar::handle:horizontal {{
        background: #555;
        min-width: 20px;
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {accent_color.name()};
    }}

    /* Progress Bar */
    QProgressBar {{
        border: 1px solid {border_color.name()};
        border-radius: 4px;
        text-align: center;
        background-color: #252525;
    }}
    QProgressBar::chunk {{
        background-color: {accent_color.name()};
        border-radius: 3px;
    }}

    /* Tooltips */
    QToolTip {{
        color: white;
        background-color: {accent_color.name()};
        border: 1px solid white;
        padding: 2px;
        border-radius: 3px;
    }}
    
    /* Splitter */
    QSplitter::handle {{
        background-color: {border_color.name()};
    }}
    """
    app.setStyleSheet(qss)


def show_help(topic, parent):
    if HelpDialog:
        dlg = HelpDialog(parent, version=VERSION)
        dlg.exec_()
    else:
        QtWidgets.QMessageBox.information(parent, "Help", f"Help topic: {topic}\n\n(help_ui.py not found)")

def completion_art():
    return "\n" + r"""
       __
      /  \
     |    |
   @_|____|_@
     |    |   Converted!
     \____/
    """ + "\n"

# --- IMPORTS FROM LOGIC.PY ---
from .logic import (
    combine_across_files,
    discover_ids,
    FilenameTemplateError,
    list_possible_params,
    output_subdir_name,
    plan_elements,
    process_elements,
    resolve_output_subdirs,
)

APP_ORG = "HH-Tools"
APP_NAME = "Timeseries Extractor"

# Use local icons or placeholder
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = Path(__file__).resolve().parent.parent

    return os.path.join(base_path, relative_path)

# Use local icons or placeholder
ICON_PATH = Path(resource_path(os.path.join("assets", "extract_timeseries.ico"))) 

TYPES = ["node", "link", "subcatchment", "system", "pollutant"]


@dataclass
class SelectionState:
    files: List[str] = field(default_factory=list)
    ids_by_type: Dict[str, List[str]] = field(
        default_factory=lambda: {t: [] for t in TYPES}
    )
    params_by_type: Dict[str, List[str]] = field(
        default_factory=lambda: {t: [] for t in TYPES}
    )
    include_regex: str = ""
    exclude_regex: str = ""
    use_all: bool = False
    union_mode: bool = True  # True=union across files, False=intersection
    # Units
    assume_units: Dict[str, str] = field(
        default_factory=lambda: {
            "flow": "cfs",
            "depth": "ft",
            "head": "ft",
            "velocity": "ft/s",
        }
    )
    to_units: Dict[str, str] = field(default_factory=dict)
    unit_overrides: Dict[str, str] = field(default_factory=dict)
    param_dimension: Dict[str, str] = field(default_factory=dict)
    # Output
    out_format: str = "tsf"
    combine_mode: str = "sep"  # "sep" | "com" | "across"
    output_dir: str = ""
    prefix: str = ""
    suffix: str = ""
    template: str = ""
    dat_template: str = ""
    tsf_template_sep: str = ""
    tsf_template_com: str = ""
    param_short: Dict[str, str] = field(default_factory=dict)
    label_map: Dict[str, str] = field(default_factory=dict)
    time_format: str = "%m/%d/%Y %H:%M"
    float_format: str = "%.6f"
    pptx_path: str = ""


class FileList(QtWidgets.QListWidget):
    filesChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(self.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragDropMode(self.DropOnly)
        self.setAlternatingRowColors(True)
        self.viewport().setAcceptDrops(True)
        self.setToolTip("Drop or add .out files to process")

    def add_files(self, paths: List[str]):
        existing = {self.item(i).text() for i in range(self.count())}
        added = False
        for p in paths:
            if p not in existing:
                it = QtWidgets.QListWidgetItem(p)
                it.setToolTip(p)
                self.addItem(it)
                added = True
        if added:
            # Notify only when new files were actually appended so downstream
            # auto-discovery logic runs once per real change.
            self.filesChanged.emit()

    def remove_selected(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))
        self.filesChanged.emit()

    def clear_files(self):
        self.clear()
        self.filesChanged.emit()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        paths = []
        for url in event.mimeData().urls():
            if url.isLocalFile():
                p = url.toLocalFile()
                if p.lower().endswith(".out"):
                    paths.append(p)
        if paths:
            self.add_files(paths)
        event.acceptProposedAction()


class SearchableList(QtWidgets.QWidget):
    def __init__(
        self, title: str, items: List[str] = None, checkable=True, parent=None
    ):
        super().__init__(parent)
        self.title = title
        self.checkable = checkable
        layout = QtWidgets.QVBoxLayout(self)
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText(f"Search {title}…")
        self.search.setClearButtonEnabled(True)
        self.search.setToolTip(f"Filter {title}")
        layout.addWidget(self.search)
        self.list = QtWidgets.QListWidget()
        self.list.setAlternatingRowColors(True)
        self.list.setUniformItemSizes(True)
        self.list.setToolTip(f"Select {title} to include")
        layout.addWidget(self.list)
        self.toolbar = QtWidgets.QHBoxLayout()
        if checkable:
            self.btn_all = QtWidgets.QPushButton("All")
            self.btn_all.setToolTip("Select all")
            self.btn_none = QtWidgets.QPushButton("None")
            self.btn_none.setToolTip("Select none")
            self.btn_invert = QtWidgets.QPushButton("Invert")
            self.btn_invert.setToolTip("Invert selection")
            for b in (self.btn_all, self.btn_none, self.btn_invert):
                self.toolbar.addWidget(b)
            # Small indeterminate progress bar shown during bulk operations
            self.progress = QtWidgets.QProgressBar()
            self.progress.setRange(0, 0)
            self.progress.setVisible(False)
            self.progress.setFixedHeight(self.btn_all.sizeHint().height())
            self.progress.setMaximumWidth(80)
            self.toolbar.addWidget(self.progress)
            self.btn_all.clicked.connect(self._check_all)
            self.btn_none.clicked.connect(self._check_none)
            self.btn_invert.clicked.connect(self._invert)
        self.toolbar.addStretch()
        layout.addLayout(self.toolbar)

        self.search.textChanged.connect(self._filter)

        if items:
            self.set_items(items)

    def set_items(self, items: List[str]):
        self.list.clear()
        for s in items:
            it = QtWidgets.QListWidgetItem(s)
            it.setToolTip(s)
            if self.checkable:
                it.setCheckState(QtCore.Qt.Unchecked)
            self.list.addItem(it)

    def selected(self) -> List[str]:
        if not self.checkable:
            return [
                self.list.item(i).text()
                for i in range(self.list.count())
                if not self.list.item(i).isHidden()
            ]
        out = []
        for i in range(self.list.count()):
            it = self.list.item(i)
            if it.checkState() == QtCore.Qt.Checked and not it.isHidden():
                out.append(it.text())
        return out

    def _filter(self, text: str):
        text = (text or "").strip().lower()
        for i in range(self.list.count()):
            it = self.list.item(i)
            it.setHidden(text not in it.text().lower())

    def _set_busy(self, busy: bool):
        if not self.checkable:
            return
        self.progress.setVisible(busy)
        for b in (self.btn_all, self.btn_none, self.btn_invert):
            b.setEnabled(not busy)
        QtWidgets.QApplication.processEvents()

    def _bulk_set(self, func):
        self._set_busy(True)
        self.list.setUpdatesEnabled(False)
        self.list.blockSignals(True)
        for i in range(self.list.count()):
            func(self.list.item(i))
        self.list.blockSignals(False)
        self.list.setUpdatesEnabled(True)
        # trigger downstream count updates once
        if self.list.count():
            self.list.itemChanged.emit(self.list.item(0))
        self._set_busy(False)

    def _check_all(self):
        self._bulk_set(lambda it: it.setCheckState(QtCore.Qt.Checked))

    def _check_none(self):
        self._bulk_set(lambda it: it.setCheckState(QtCore.Qt.Unchecked))

    def _invert(self):
        def toggle(it):
            it.setCheckState(
                QtCore.Qt.Unchecked
                if it.checkState() == QtCore.Qt.Checked
                else QtCore.Qt.Checked
            )

        self._bulk_set(toggle)


class DiscoverWorker(QtCore.QThread):
    progress = QtCore.pyqtSignal(int, int)
    finished = QtCore.pyqtSignal(dict)
    failed = QtCore.pyqtSignal(str)

    def __init__(self, files: List[str], inc: str, exc: str, union: bool, parent=None):
        super().__init__(parent)
        self.files = files
        self.inc_re = re.compile(inc) if inc else None
        self.exc_re = re.compile(exc) if exc else None
        self.union = union

    def run(self):
        try:
            per_file: Dict[str, Dict[str, List[str]]] = {}
            total = len(self.files) * len(TYPES)
            done = 0
            for f in self.files:
                per_file[f] = {}
                for t in TYPES:
                    ids = discover_ids(f, t)
                    flt = []
                    for i in ids:
                        if self.inc_re and not self.inc_re.search(i):
                            continue
                        if self.exc_re and self.exc_re.search(i):
                            continue
                        flt.append(i)
                    per_file[f][t] = flt
                    done += 1
                    self.progress.emit(done, total)
            result: Dict[str, List[str]] = {}
            for t in TYPES:
                if self.union:
                    result[t] = sorted({i for f in self.files for i in per_file[f][t]})
                else:
                    sets = [set(per_file[f][t]) for f in self.files]
                    result[t] = sorted(list(set.intersection(*sets))) if sets else []
            self.finished.emit(result)
        except Exception as e:
            self.failed.emit(f"{e.__class__.__name__}: {e}")


class Worker(QtCore.QThread):
    msg = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int, int, dict)  # done, total, ctx
    finished_ok = QtCore.pyqtSignal(list)  # written files
    failed = QtCore.pyqtSignal(str)

    def __init__(self, state: SelectionState, plan_only: bool, parent=None):
        super().__init__(parent)
        self.state = state
        self.plan_only = plan_only
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        try:
            written: List[str] = []
            planned: List[str] = []

            file_count = len(self.state.files)
            action_text = "Planning outputs" if self.plan_only else "Starting extraction"
            if file_count == 0:
                files_label = "no files"
            elif file_count == 1:
                files_label = "1 file"
            else:
                files_label = f"{file_count} files"
            self.msg.emit(f"{action_text} for {files_label}…")

            # Compute total series count for progress
            total = 0
            for f in self.state.files:
                for t in TYPES:
                    ids = self.state.ids_by_type.get(t, [])
                    params = self.state.params_by_type.get(t, [])
                    if t == "system" and ids:
                        ids = ["SYSTEM"]
                    total += (len(ids) or 0) * (len(params) or 0)
            total = max(total, 1)

            done_so_far = 0

            def cb(done, tot, ctx):
                nonlocal done_so_far
                done_so_far += 1
                self.progress.emit(done_so_far, total, ctx)
                if self._cancel:
                    raise RuntimeError("Canceled by user")

            subdir_map = resolve_output_subdirs(self.state.files, self.state.output_dir)

            for outfile in self.state.files:
                outdir_root = self.state.output_dir or os.path.dirname(outfile)
                subdir = subdir_map.get(outfile, output_subdir_name(outfile))
                file_label = Path(outfile).name or outfile
                per_file_action = "Planning" if self.plan_only else "Processing"
                self.msg.emit(f"{per_file_action} {file_label}…")

                if self.plan_only:
                    planned_for_file: List[str] = []
                    for t in TYPES:
                        ids = self.state.ids_by_type.get(t, [])
                        params = self.state.params_by_type.get(t, [])
                        if not ids or not params:
                            continue
                        planned_paths = plan_elements(
                            outfile,
                            t,
                            ids,
                            params,
                            self.state.out_format,
                            self.state.combine_mode,
                            outdir_root,
                            self.state.prefix,
                            self.state.suffix,
                            self.state.dat_template,
                            self.state.tsf_template_sep,
                            self.state.tsf_template_com,
                            self.state.param_short,
                            out_subdir=subdir,
                        )
                        planned += planned_paths
                        planned_for_file.extend(planned_paths)
                    if planned_for_file:
                        self.msg.emit(
                            f"Finished planning {file_label} ({len(planned_for_file)} planned outputs)"
                        )
                    else:
                        self.msg.emit(
                            f"Finished planning {file_label} (no matching selections)"
                        )
                else:
                    written_for_file: List[str] = []
                    failures_for_file: List[Tuple[str, str, str, str, str]] = []
                    for t in TYPES:
                        ids = self.state.ids_by_type.get(t, [])
                        params = self.state.params_by_type.get(t, [])
                        if not ids or not params:
                            continue
                        paths, failures = process_elements(
                            outfile,
                            t,
                            ids,
                            params,
                            self.state.out_format,
                            self.state.combine_mode,
                            outdir_root,
                            out_subdir=subdir,
                            time_format=self.state.time_format,
                            float_format=self.state.float_format,
                            prefix=self.state.prefix,
                            suffix=self.state.suffix,
                            dat_template=self.state.dat_template,
                            tsf_template_sep=self.state.tsf_template_sep,
                            tsf_template_com=self.state.tsf_template_com,
                            param_short=self.state.param_short,
                            label_map=self.state.label_map,
                            param_dimension=self.state.param_dimension,
                            assume_units=self.state.assume_units,
                            to_units=self.state.to_units,
                            unit_overrides=self.state.unit_overrides,
                            show_progress=False,
                            ppt=None,
                            progress_callback=cb,
                        )
                        written.extend(paths)
                        written_for_file.extend(paths)
                        failures_for_file.extend(failures)
                    count = len(written_for_file)
                    if count:
                        outputs_label = "file" if count == 1 else "files"
                        summary = f"Finished processing {file_label}: {count} {outputs_label}"
                    else:
                        summary = f"Finished processing {file_label}: no files written"
                    if failures_for_file:
                        failure_label = "failure" if len(failures_for_file) == 1 else "failures"
                        summary += f" ({len(failures_for_file)} {failure_label})"
                    self.msg.emit(summary)

            # Post-processing combine
            if not self.plan_only and self.state.combine_mode == "across" and written:
                self.msg.emit("Combining outputs across files…")
                combine_across_files(
                    written,
                    self.state.out_format,
                    (self.state.output_dir or os.getcwd()),
                )
                self.msg.emit("Finished combining outputs across files.")

            self.finished_ok.emit(planned if self.plan_only else written)
        except FilenameTemplateError as e:
            self.failed.emit(str(e))
        except Exception as e:
            import traceback

            with open("last_error.txt", "w", encoding="utf-8") as fh:
                fh.write(traceback.format_exc())
            self.failed.emit(f"{e.__class__.__name__}: {e}")


class ExtractorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setWindowTitle(APP_NAME)
        # self.setWindowIcon(QtGui.QIcon(str(ICON_DIR / "extract_timeseries.ico")))
        self.resize(1200, 560)
        self.settings = QtCore.QSettings(APP_ORG, APP_NAME)
        if geo := self.settings.value("geometry"):
            self.restoreGeometry(geo)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main = QtWidgets.QVBoxLayout(central)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        main.addWidget(splitter)

        # Top: controls (tabs per section)
        self.tabs = QtWidgets.QTabWidget()
        splitter.addWidget(self.tabs)
        splitter.setStretchFactor(0, 3)

        # Bottom: run + log
        bottom = QtWidgets.QWidget()
        b_layout = QtWidgets.QVBoxLayout(bottom)
        self.progress = QtWidgets.QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setToolTip("Progress of extraction")
        b_layout.addWidget(self.progress)
        hl = QtWidgets.QHBoxLayout()
        self.btn_run = QtWidgets.QPushButton("Run")
        self.btn_run.setToolTip("Run extraction")
        self.btn_preview = QtWidgets.QPushButton("Preview only")
        self.btn_preview.setToolTip("Show planned filenames without writing files")
        self.btn_open_dir = QtWidgets.QPushButton("Open folder")
        self.btn_open_dir.setToolTip("Open output directory")
        self.btn_help = QtWidgets.QPushButton("Help")
        self.btn_help.setToolTip("Show usage information")
        self.btn_help.clicked.connect(lambda: show_help("extract_timeseries", self))
        self.btn_cancel = QtWidgets.QPushButton("Cancel")
        self.btn_cancel.setToolTip("Cancel running task")
        self.btn_cancel.setEnabled(False)
        self.time_label = QtWidgets.QLabel()
        self.time_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        hl.addWidget(self.btn_run)
        hl.addWidget(self.btn_preview)
        hl.addWidget(self.btn_open_dir)
        hl.addWidget(self.btn_help)
        hl.addStretch()
        hl.addWidget(self.time_label)
        hl.addWidget(self.btn_cancel)
        b_layout.addLayout(hl)
        self.log = QtWidgets.QPlainTextEdit()
        self.log.setReadOnly(True)
        b_layout.addWidget(self.log, 1)
        splitter.addWidget(bottom)
        splitter.setStretchFactor(1, 1)

        # Runtime/ETA timer setup
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._update_time)
        self._start_time: Optional[float] = None
        self._progress_done = 0
        self._progress_total = 0

        # Section 1: Sources
        self.page_sources = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(self.page_sources)
        self.file_list = FileList()
        lay.addWidget(self.file_list, 1)
        hb = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("Add .out files")
        btn_add.setToolTip("Select SWMM .out files")
        btn_del = QtWidgets.QPushButton("Remove selected")
        btn_del.setToolTip("Remove highlighted files")
        btn_clear = QtWidgets.QPushButton("Clear")
        btn_clear.setToolTip("Clear file list")
        hb.addWidget(btn_add)
        hb.addWidget(btn_del)
        hb.addWidget(btn_clear)
        hb.addStretch()
        lay.addLayout(hb)
        btn_add.clicked.connect(self._choose_files)
        btn_del.clicked.connect(self.file_list.remove_selected)
        btn_clear.clicked.connect(self.file_list.clear_files)
        self.file_list.filesChanged.connect(lambda: self._start_discover_ids(auto=True))
        self.file_list.filesChanged.connect(self._detect_units)
        self.tabs.addTab(self.page_sources, "1) Sources")
        self.tabs.setTabToolTip(0, "Manage input .out files")

        # Section 2: IDs
        self.page_ids = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(self.page_ids)
        self.union_combo = QtWidgets.QComboBox()
        self.union_combo.addItems(["Union across files", "Intersection across files"])
        self.union_combo.setToolTip("How to combine IDs from multiple files")
        self.include_edit = QtWidgets.QLineEdit()
        self.include_edit.setPlaceholderText("Include regex (optional)")
        self.include_edit.setClearButtonEnabled(True)
        self.include_edit.setToolTip("Regular expression to include IDs")
        self.exclude_edit = QtWidgets.QLineEdit()
        self.exclude_edit.setPlaceholderText("Exclude regex (optional)")
        self.exclude_edit.setClearButtonEnabled(True)
        self.exclude_edit.setToolTip("Regular expression to exclude IDs")
        self.btn_discover = QtWidgets.QPushButton("Discover IDs")
        self.btn_discover.setToolTip("Scan files for IDs")
        self.btn_paste = QtWidgets.QPushButton("Paste IDs…")
        self.btn_paste.setToolTip("Paste newline-separated IDs from clipboard")
        self.discover_progress = QtWidgets.QProgressBar()
        self.discover_progress.setVisible(False)
        self.discover_progress.setTextVisible(False)
        grid.addWidget(QtWidgets.QLabel("Multi-file logic:"), 0, 0)
        grid.addWidget(self.union_combo, 0, 1)
        grid.addWidget(self.btn_discover, 0, 2)
        grid.addWidget(self.discover_progress, 0, 3)
        grid.addWidget(self.include_edit, 1, 0, 1, 2)
        grid.addWidget(self.exclude_edit, 1, 2, 1, 2)
        self.id_tabs = QtWidgets.QTabWidget()
        self.id_lists: Dict[str, SearchableList] = {}
        for i, t in enumerate(TYPES):
            w = SearchableList(f"{t} IDs")
            self.id_tabs.addTab(w, t.title())
            self.id_lists[t] = w
            w.list.itemChanged.connect(self._update_id_counts)
        grid.addWidget(self.id_tabs, 2, 0, 1, 4)
        grid.addWidget(self.btn_paste, 3, 0, 1, 1)
        self.id_count_label = QtWidgets.QLabel()
        grid.addWidget(self.id_count_label, 3, 1, 1, 3)
        grid.setRowStretch(2, 1)
        grid.setColumnStretch(3, 1)

        self.tabs.addTab(self.page_ids, "2) IDs")
        self.tabs.setTabToolTip(1, "Select specific elements (Nodes, Links, etc.)")

        # Set tooltips for ID sub-tabs
        id_tooltips = {
            "node": "Junctions, Outfalls, Dividers, Storage Units",
            "link": "Conduits, Pumps, Orifices, Weirs, Outlets",
            "subcatchment": "Subcatchment areas",
            "system": "System-wide variables (Rainfall, Runoff, etc.)",
            "pollutant": "Pollutant concentrations and loads"
        }
        for i, t in enumerate(TYPES):
            if t in id_tooltips:
                self.id_tabs.setTabToolTip(i, id_tooltips[t])

        # Section 3: Parameters
        self.page_params = QtWidgets.QWidget()
        gridp = QtWidgets.QGridLayout(self.page_params)
        self.param_tabs = QtWidgets.QTabWidget()
        self.param_lists: Dict[str, SearchableList] = {}
        for t in TYPES:
            w = SearchableList(f"{t} parameters")
            self.param_tabs.addTab(w, t.title())
            self.param_lists[t] = w
        gridp.addWidget(self.param_tabs, 0, 0, 1, 3)

        self.tabs.addTab(self.page_params, "3) Parameters")
        self.tabs.setTabToolTip(2, "Select variables to extract (Flow, Depth, etc.)")

        # Reuse same tooltips for parameter sub-tabs as they correspond to the same types
        for i, t in enumerate(TYPES):
            if t in id_tooltips:
                self.param_tabs.setTabToolTip(i, id_tooltips[t])

        # Section 4: Units
        self.page_units = QtWidgets.QWidget()
        fu = QtWidgets.QFormLayout(self.page_units)
        self.units_label = QtWidgets.QLabel()
        fu.addRow(self.units_label)
        self.assume_flow = QtWidgets.QComboBox()
        self.assume_flow.addItems(["", "cfs", "cms", "mgd", "gpm", "l/s"])
        self.assume_flow.setCurrentText("cfs")
        self.assume_flow.setToolTip("Units assumed for flow in inputs")
        self.assume_depth = QtWidgets.QComboBox()
        self.assume_depth.addItems(["", "ft", "m", "in", "cm"])
        self.assume_depth.setCurrentText("ft")
        self.assume_depth.setToolTip("Units assumed for depth in inputs")
        self.assume_head = QtWidgets.QComboBox()
        self.assume_head.addItems(["", "ft", "m", "in", "cm"])
        self.assume_head.setCurrentText("ft")
        self.assume_head.setToolTip("Units assumed for head in inputs")
        self.assume_vel = QtWidgets.QComboBox()
        self.assume_vel.addItems(["", "ft/s", "m/s"])
        self.assume_vel.setCurrentText("ft/s")
        self.assume_vel.setToolTip("Units assumed for velocity in inputs")
        self.to_flow = QtWidgets.QComboBox()
        self.to_flow.addItems(["", "cfs", "cms", "mgd", "gpm", "l/s"])
        self.to_flow.setCurrentText("cfs")
        self.to_flow.setToolTip("Convert flow to this unit")
        self.to_depth = QtWidgets.QComboBox()
        self.to_depth.addItems(["", "ft", "m", "in", "cm"])
        self.to_depth.setCurrentText("ft")
        self.to_depth.setToolTip("Convert depth to this unit")
        self.to_head = QtWidgets.QComboBox()
        self.to_head.addItems(["", "ft", "m", "in", "cm"])
        self.to_head.setCurrentText("ft")
        self.to_head.setToolTip("Convert head to this unit")
        self.to_vel = QtWidgets.QComboBox()
        self.to_vel.addItems(["", "ft/s", "m/s"])
        self.to_vel.setCurrentText("ft/s")
        self.to_vel.setToolTip("Convert velocity to this unit")
        fu.addRow("Assume flow", self.assume_flow)
        fu.addRow("Assume depth", self.assume_depth)
        fu.addRow("Assume head", self.assume_head)
        fu.addRow("Assume velocity", self.assume_vel)
        fu.addRow("To flow", self.to_flow)
        fu.addRow("To depth", self.to_depth)
        fu.addRow("To head", self.to_head)
        fu.addRow("To velocity", self.to_vel)

        self.tabs.addTab(self.page_units, "4) Units")
        self.tabs.setTabToolTip(3, "Configure unit conversions")

        # Section 5: Output
        self.page_output = QtWidgets.QWidget()
        fo = QtWidgets.QGridLayout(self.page_output)
        fo.setVerticalSpacing(4)
        fo.setHorizontalSpacing(8)
        fo.setColumnStretch(1, 1)
        fo.setColumnStretch(3, 1)
        self.out_format = QtWidgets.QComboBox()
        self.out_format.addItems(["tsf", "dat", "csv"])
        self.out_format.setToolTip("Output file format")
        self.combine = QtWidgets.QComboBox()
        self.combine.addItem("Separate files per parameter", "sep")
        self.combine.addItem("Combine parameters per element", "com")
        self.combine.addItem("Merge IDs across input files", "across")
        self.combine.setToolTip("How to group parameters into files")
        self.output_dir = QtWidgets.QLineEdit()
        self.output_dir.setClearButtonEnabled(True)
        self.output_dir.setToolTip("Directory where output files are written")
        btn_out = QtWidgets.QPushButton("Browse…")
        btn_out.clicked.connect(self._choose_output_dir)
        btn_out.setToolTip("Select output directory")
        outrow = QtWidgets.QHBoxLayout()
        outrow.setSpacing(6)
        outrow.addWidget(self.output_dir)
        outrow.addWidget(btn_out)
        self.prefix = QtWidgets.QLineEdit()
        self.prefix.setClearButtonEnabled(True)
        self.prefix.setToolTip("Prefix added to filenames")
        self.suffix = QtWidgets.QLineEdit()
        self.suffix.setClearButtonEnabled(True)
        self.suffix.setToolTip("Suffix added to filenames")
        self.template = QtWidgets.QLineEdit()
        self.template.setClearButtonEnabled(True)
        self.template.setToolTip("Filename pattern for output files")
        self.template_label = QtWidgets.QLabel("Pattern")
        self.preview_box = QtWidgets.QTextEdit()
        self.preview_box.setReadOnly(True)
        self.preview_box.setFixedHeight(120)
        self.preview_box.setToolTip("Preview of planned filenames")
        r = 0
        fo.addWidget(QtWidgets.QLabel("Format"), r, 0)
        fo.addWidget(self.out_format, r, 1)
        fo.addWidget(QtWidgets.QLabel("Combine"), r, 2)
        fo.addWidget(self.combine, r, 3)
        r += 1
        fo.addWidget(QtWidgets.QLabel("Output dir"), r, 0)
        fo.addLayout(outrow, r, 1, 1, 3)
        r += 1
        fo.addWidget(QtWidgets.QLabel("Prefix"), r, 0)
        fo.addWidget(self.prefix, r, 1)
        fo.addWidget(QtWidgets.QLabel("Suffix"), r, 2)
        fo.addWidget(self.suffix, r, 3)
        r += 1
        self.template_group = QtWidgets.QGroupBox("Filename template")
        tpl = QtWidgets.QFormLayout(self.template_group)
        tpl.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        tpl.addRow(self.template_label, self.template)
        fo.addWidget(self.template_group, r, 0, 1, 4)
        r += 1
        fo.addWidget(QtWidgets.QLabel("Planned filenames (preview)"), r, 0)
        fo.addWidget(self.preview_box, r, 1, 1, 3)

        self.tabs.addTab(self.page_output, "5) Output")
        self.tabs.setTabToolTip(4, "Set output format and file naming")

        # Wire actions
        self.btn_discover.clicked.connect(lambda: self._start_discover_ids(auto=False))
        self.btn_paste.clicked.connect(self._paste_ids)
        self.btn_run.clicked.connect(lambda: self._run(plan_only=False))
        self.btn_preview.clicked.connect(self._preview)
        self.btn_open_dir.clicked.connect(self._open_output_dir)
        self.btn_cancel.clicked.connect(self._cancel)

        # Restore some settings
        last_dir = self.settings.value("last_dir", "", type=str)
        if last_dir and os.path.isdir(last_dir):
            self.output_dir.setText(self.settings.value("output_dir", last_dir))

        # Timer to update preview when templates/format change
        self._preview_timer = QtCore.QTimer(self)
        self._preview_timer.setInterval(400)
        self._preview_timer.setSingleShot(True)
        for w in [
            self.out_format,
            self.combine,
            self.output_dir,
            self.prefix,
            self.suffix,
            self.template,
        ]:
            if isinstance(w, QtWidgets.QComboBox):
                w.currentTextChanged.connect(lambda _=None: self._preview_timer.start())
            else:
                w.textChanged.connect(lambda _=None: self._preview_timer.start())

        self.out_format.currentTextChanged.connect(self._update_template_placeholder)
        self.out_format.currentTextChanged.connect(self._update_template_fields)
        self.combine.currentIndexChanged.connect(self._update_template_placeholder)
        self.combine.currentIndexChanged.connect(self._update_template_fields)
        self._update_template_placeholder()
        self._update_template_fields()

        self._update_id_counts()

    # ------------- Helpers -------------

    def _current_template_default(self) -> str:
        fmt = self.out_format.currentText()
        mode = self.combine.currentData()
        if fmt in ("dat", "csv"):
            ext = fmt
            return f"{{prefix}}{{short}}{{id}}{{suffix}}.{ext}"
        if mode == "com":
            return "{prefix}{type}{id}{suffix}.tsf"
        return "{prefix}{type}{id}{param}{suffix}.tsf"

    def _update_template_placeholder(self, *_):
        fmt = self.out_format.currentText()
        mode = self.combine.currentData()
        default = self._current_template_default()
        self.template.setPlaceholderText(default)
        if fmt in ("dat", "csv"):
            ext = fmt
            self.template_label.setText(f"{ext.upper()} pattern")
            self.template.setToolTip(
                f"Filename pattern for .{ext} outputs. Add separators manually if "
                f"desired, e.g. '{{prefix}}_{{short}}_{{id}}{{suffix}}.{ext}'."
            )
        else:
            if mode == "com":
                self.template_label.setText("TSF combined pattern")
                self.template.setToolTip(
                    "Filename pattern when parameters are combined into one .tsf file. "
                    "Add separators manually if desired, e.g. "
                    "'{prefix}_{type}_{id}{suffix}.tsf'."
                )
            else:
                self.template_label.setText("TSF Pattern")
                self.template.setToolTip(
                    "Filename pattern when each parameter has its own .tsf file. Add "
                    "separators manually if desired, e.g. "
                    "'{prefix}_{type}_{id}_{param}{suffix}.tsf'."
                )

    def _update_template_fields(self, *_):
        self.template.setText(self._current_template_default())

    def _plan_output_paths(self, st: SelectionState) -> List[str]:
        planned_all: List[str] = []
        for f in st.files:
            outdir_root = st.output_dir or os.path.dirname(f)
            for t in TYPES:
                ids = st.ids_by_type.get(t, [])
                params = st.params_by_type.get(t, [])
                if not ids or not params:
                    continue
                planned = plan_elements(
                    f,
                    t,
                    ids,
                    params,
                    st.out_format,
                    st.combine_mode,
                    outdir_root,
                    st.prefix,
                    st.suffix,
                    st.dat_template,
                    st.tsf_template_sep,
                    st.tsf_template_com,
                    st.param_short,
                )
                planned_all.extend(planned)
        return planned_all

    def _confirm_output_overwrite(self, planned: List[str], out_format: str) -> bool:
        if not planned or not out_format:
            return True

        ext = f".{out_format.lower()}"
        seen_dirs = []
        seen_set = set()
        for path in planned:
            parent = Path(path).parent.resolve()
            if parent not in seen_set:
                seen_set.add(parent)
                seen_dirs.append(parent)

        conflicts: List[Path] = []
        for directory in seen_dirs:
            if not directory.exists():
                continue
            try:
                has_match = any(
                    child.is_file() and child.suffix.lower() == ext
                    for child in directory.iterdir()
                )
            except (PermissionError, FileNotFoundError, OSError):  # pragma: no cover - defensive
                has_match = False
            if has_match:
                conflicts.append(directory)

        if not conflicts:
            return True

        display = [str(p) for p in conflicts[:10]]
        if len(conflicts) > 10:
            display.append("…")
        message = [
            f"Existing {ext} files were found in these folders:",
            *[f" - {d}" for d in display],
            "Continuing may overwrite them. Do you want to proceed?",
        ]
        choice = QtWidgets.QMessageBox.question(
            self,
            "Existing output files",
            "\n".join(message),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        return choice == QtWidgets.QMessageBox.Yes

    def dragEnterEvent(
        self, event: QtGui.QDragEnterEvent
    ) -> None:  # pragma: no cover - GUI
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile() and url.toLocalFile().lower().endswith(".out"):
                    event.acceptProposedAction()
                    return
        super().dragEnterEvent(event)

    def dragMoveEvent(
        self, event: QtGui.QDragMoveEvent
    ) -> None:  # pragma: no cover - GUI
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile() and url.toLocalFile().lower().endswith(".out"):
                    event.acceptProposedAction()
                    return
        super().dragMoveEvent(event)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:  # pragma: no cover - GUI
        paths = []
        for url in event.mimeData().urls():
            if url.isLocalFile():
                p = url.toLocalFile()
                if p.lower().endswith(".out"):
                    paths.append(p)
        if paths:
            self.file_list.add_files(paths)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def _choose_files(self):
        start = self.settings.value("last_dir", "")
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select SWMM .out files", start, "SWMM .out (*.out)"
        )
        if paths:
            self.file_list.add_files(paths)
            self.settings.setValue("last_dir", os.path.dirname(paths[0]))

    def _choose_output_dir(self):
        start = self.settings.value("output_dir", self.settings.value("last_dir", ""))
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select output directory", start
        )
        if path:
            self.output_dir.setText(path)
            self.settings.setValue("output_dir", path)

    def _open_output_dir(self):
        path = self.output_dir.text().strip()
        if path and os.path.isdir(path):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))

    def _start_discover_ids(self, auto: bool = False):
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not files:
            for t in TYPES:
                self.id_lists[t].set_items([])
            self._update_id_counts()
            return
        inc = self.include_edit.text().strip()
        exc = self.exclude_edit.text().strip()
        union = self.union_combo.currentIndex() == 0

        # UI: show spinner initially
        self.btn_discover.setEnabled(False)
        self.discover_progress.setVisible(True)
        self.discover_progress.setRange(0, 0)

        # Try to build worker (regex could be invalid)
        try:
            self.discover_worker = DiscoverWorker(files, inc, exc, union)
        except re.error as rex:
            # Bad regex — reset UI and tell user
            self.discover_progress.setRange(0, 1)
            self.discover_progress.setVisible(False)
            self.btn_discover.setEnabled(True)
            QtWidgets.QMessageBox.critical(self, "Invalid regex", str(rex))
            return
        except Exception as e:
            self.discover_progress.setRange(0, 1)
            self.discover_progress.setVisible(False)
            self.btn_discover.setEnabled(True)
            QtWidgets.QMessageBox.critical(
                self, "Discovery setup failed", f"{e.__class__.__name__}: {e}"
            )
            return

        # Make progress determinate when updates arrive
        def on_prog(done: int, total: int):
            self.discover_progress.setRange(0, total or 1)
            self.discover_progress.setValue(done)

        def on_finished(res: Dict[str, List[str]]):
            for t in TYPES:
                self.id_lists[t].set_items(res.get(t, []))
                lst = self.param_lists.get(t)
                if lst and lst.list.count() == 0 and files:
                    lst.set_items(list_possible_params(files[0], t))
            self._update_id_counts()
            self.discover_progress.setRange(0, 1)
            self.discover_progress.setVisible(False)
            self.btn_discover.setEnabled(True)
            if not auto:
                QtWidgets.QMessageBox.information(
                    self,
                    "IDs discovered",
                    "Review each tab and check the IDs you want.",
                )

        def on_failed(msg: str):
            self.discover_progress.setRange(0, 1)
            self.discover_progress.setVisible(False)
            self.btn_discover.setEnabled(True)
            QtWidgets.QMessageBox.critical(self, "Discovery failed", msg)

        self.discover_worker.progress.connect(on_prog)
        self.discover_worker.finished.connect(on_finished)
        self.discover_worker.failed.connect(on_failed)
        self.discover_worker.start()

    def _detect_units(self):
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not files:
            self.units_label.setText("")
            return
        f0 = Path(files[0])
        rpt = f0.with_suffix(".rpt")
        if not rpt.exists():
            cands = list(f0.parent.glob("*.rpt"))
            if cands:
                rpt = cands[0]
        detected: Dict[str, str] = {}
        if rpt.exists():
            try:
                with open(rpt, "r", errors="ignore") as fh:
                    for line in fh:
                        ul = line.strip().upper()
                        if ul.startswith("FLOW UNITS"):
                            if "CFS" in ul:
                                detected["flow"] = "cfs"
                            elif "CMS" in ul:
                                detected["flow"] = "cms"
                            elif "MGD" in ul:
                                detected["flow"] = "mgd"
                            elif "GPM" in ul:
                                detected["flow"] = "gpm"
                            elif "LPS" in ul or "L/S" in ul:
                                detected["flow"] = "l/s"
                        elif ul.startswith("LENGTH UNITS"):
                            if "FEET" in ul or "FT" in ul:
                                val = "ft"
                            elif "METERS" in ul or "M" in ul:
                                val = "m"
                            elif "INCH" in ul:
                                val = "in"
                            elif "CENTIM" in ul or "CM" in ul:
                                val = "cm"
                            else:
                                val = ""
                            if val:
                                detected["depth"] = val
                                detected["head"] = val
                        elif ul.startswith("VELOCITY UNITS"):
                            if "FT/S" in ul or "FT/SEC" in ul or "FPS" in ul:
                                detected["velocity"] = "ft/s"
                            elif "M/S" in ul or "MPS" in ul:
                                detected["velocity"] = "m/s"
            except Exception:
                pass
        if detected:
            self.units_label.setText(
                "Detected: "
                + ", ".join(f"{k} {v}" for k, v in detected.items())
                + " (override if needed)"
            )
            if detected.get("flow"):
                self.assume_flow.setCurrentText(detected["flow"])
            if detected.get("depth"):
                self.assume_depth.setCurrentText(detected["depth"])
                self.assume_head.setCurrentText(detected["head"])
                if "velocity" not in detected:
                    detected["velocity"] = (
                        "ft/s" if detected["depth"] == "ft" else "m/s"
                    )
            if detected.get("velocity"):
                self.assume_vel.setCurrentText(detected["velocity"])
        else:
            self.units_label.setText("Detected: none")
        # mirror assumes into target units by default
        self.to_flow.setCurrentText(self.assume_flow.currentText())
        self.to_depth.setCurrentText(self.assume_depth.currentText())
        self.to_head.setCurrentText(self.assume_head.currentText())
        self.to_vel.setCurrentText(self.assume_vel.currentText())

    def _update_id_counts(self):
        counts = []
        total = 0
        for t in TYPES:
            lst = self.id_lists.get(t)
            c = len(lst.selected()) if lst else 0
            counts.append(f"{t.title()}s: {c}")
            total += c
        self.id_count_label.setText(" | ".join(counts) + f" | Total: {total}")

    def _paste_ids(self):
        text, ok = QtWidgets.QInputDialog.getMultiLineText(
            self,
            "Paste IDs",
            "One ID per line (use type:ID to specify type, else use the active tab's type):",
            "",
        )
        if not ok or not text.strip():
            return
        active_type = TYPES[self.id_tabs.currentIndex()]
        pasted: List[Tuple[str, str]] = []
        for line in text.splitlines():
            s = line.strip()
            if not s:
                continue
            if ":" in s:
                t, i = s.split(":", 1)
            else:
                t, i = active_type, s
            w = self.id_lists.get(t)
            if not w:
                continue
            # add item and select it
            it = QtWidgets.QListWidgetItem(i)
            it.setToolTip(i)
            it.setCheckState(QtCore.Qt.Checked)
            w.list.addItem(it)
            pasted.append((t, i))
        self._update_id_counts()

        # Validate pasted IDs against selected out files
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if files and pasted:
            needed_types = {t for t, _ in pasted}
            cache: Dict[Tuple[str, str], set] = {}
            missing: Dict[str, Dict[str, List[str]]] = {}
            resolved_details: List[Tuple[str, Path]] = []
            resolved_parents: List[str] = []
            display_paths: Dict[str, str] = {}
            for f in files:
                resolved = Path(f).resolve()
                resolved_details.append((f, resolved))
                resolved_parents.append(str(resolved.parent))
                display_paths[f] = str(resolved)
            common_root = ""
            used_relative = False
            if resolved_parents:
                try:
                    common_root = os.path.commonpath(resolved_parents)
                except ValueError:
                    common_root = ""
            if common_root:
                for original, resolved in resolved_details:
                    rel = os.path.relpath(str(resolved), common_root)
                    if rel and rel != "." and not rel.startswith(".."):
                        display_paths[original] = rel
                        used_relative = True
            for f in files:
                for t in needed_types:
                    cache[(f, t)] = set(discover_ids(f, t))
            for f in files:
                for t, i in pasted:
                    if i not in cache.get((f, t), set()):
                        key = display_paths.get(f, f)
                        missing.setdefault(key, {}).setdefault(t, []).append(i)
            if missing:
                lines = ["Some IDs were not found in the selected files:"]
                if used_relative and common_root:
                    lines.append(f"(Paths relative to {common_root})")
                for f, by_type in missing.items():
                    parts = []
                    for t, ids in by_type.items():
                        parts.append(f"{t}: {', '.join(ids)}")
                    lines.append(f"{f}: " + "; ".join(parts))
                QtWidgets.QMessageBox.warning(self, "IDs not found", "\n".join(lines))

    def _gather_state(self) -> SelectionState:
        st = SelectionState()
        st.files = [
            self.file_list.item(i).text() for i in range(self.file_list.count())
        ]
        if not st.files:
            raise RuntimeError("No input files selected.")

        for t in TYPES:
            st.ids_by_type[t] = self.id_lists[t].selected()
            st.params_by_type[t] = self.param_lists[t].selected()

        st.include_regex = self.include_edit.text().strip()
        st.exclude_regex = self.exclude_edit.text().strip()
        st.union_mode = self.union_combo.currentIndex() == 0

        # Units
        st.assume_units = {
            "flow": self.assume_flow.currentText(),
            "depth": self.assume_depth.currentText(),
            "head": self.assume_head.currentText(),
            "velocity": self.assume_vel.currentText(),
        }
        st.to_units = {
            "flow": self.to_flow.currentText(),
            "depth": self.to_depth.currentText(),
            "head": self.to_head.currentText(),
            "velocity": self.to_vel.currentText(),
        }

        # Output
        st.out_format = self.out_format.currentText()
        st.combine_mode = self.combine.currentData()
        st.output_dir = self.output_dir.text().strip()
        p = self.prefix.text().strip()
        s = self.suffix.text().strip()
        if p and not p.endswith("_"):
            p += "_"
        if s and not s.startswith("_"):
            s = "_" + s
        st.prefix = p
        st.suffix = s
        st.template = self.template.text().strip()
        st.dat_template = ""
        st.tsf_template_sep = ""
        st.tsf_template_com = ""
        if st.out_format in ("dat", "csv"):
            st.dat_template = st.template
        elif st.out_format == "tsf":
            if st.combine_mode == "com":
                st.tsf_template_com = st.template
            else:
                st.tsf_template_sep = st.template
        return st

    def _preview(self):
        try:
            st = self._gather_state()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Missing inputs", str(e))
            return
        self.preview_box.clear()
        # We don't need a thread for planning; it's fast
        try:
            planned_all = self._plan_output_paths(st)
        except FilenameTemplateError as e:
            QtWidgets.QMessageBox.warning(self, "Invalid template", str(e))
            return
        if not self._confirm_output_overwrite(planned_all, st.out_format):
            return
        self.preview_box.setPlainText(
            "\n".join(
                planned_all[:500]
                + (["… (truncated)"] if len(planned_all) > 500 else [])
            )
        )

    def _run(self, plan_only: bool):
        try:
            st = self._gather_state()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Missing inputs", str(e))
            return

        # Require at least one element and parameter selection
        has_selection = any(
            st.ids_by_type.get(t) and st.params_by_type.get(t) for t in TYPES
        )
        if not has_selection:
            self.log.appendPlainText(
                "Please select at least one element and parameter before running."
            )
            return

        # Param discovery on demand if lists are empty
        for t in TYPES:
            lst = self.param_lists[t]
            if lst.list.count() == 0 and st.files:
                # discover from first file
                lst.set_items(list_possible_params(st.files[0], t))

        planned_all = self._plan_output_paths(st)
        if not self._confirm_output_overwrite(planned_all, st.out_format):
            return

        self.log.clear()
        import numpy
        import pandas

        msg = [
            f"numpy={numpy.__version__}",
            f"pandas={pandas.__version__}",
        ]
        try:
            import swmmtoolbox as s

            try:
                from importlib.metadata import version

                swmm_ver = version("swmm-toolbox")
            except Exception:
                swmm_ver = getattr(s, "__version__", "unknown")
            msg.insert(0, f"swmmtoolbox={swmm_ver}")
        except Exception as e:
            msg.insert(0, f"swmmtoolbox import failed: {e}")
        self.log.appendPlainText("Versions: " + " ".join(msg))
        self.btn_run.setEnabled(False)
        self.btn_preview.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.progress.setValue(0)
        self.time_label.setText("Runtime: 00:00:00   ETA: --:--:--")
        self._start_time = time.monotonic()
        self._progress_done = 0
        self._progress_total = 0
        self._timer.start()

        self.worker = Worker(st, plan_only)
        self.worker.msg.connect(lambda m: self.log.appendPlainText(m))

        def on_prog(done, total, ctx):
            pct = int(done * 100 / max(total, 1))
            self.progress.setValue(pct)
            self.progress.setFormat(
                f"{pct}% — {Path(ctx.get('file','')).name} → {ctx.get('type','')}:{ctx.get('id','')} {ctx.get('param','')}"
            )
            self._progress_done = done
            self._progress_total = total

        self.worker.progress.connect(on_prog)

        def on_ok(paths: List[str]):
            self.log.appendPlainText(
                f"Completed. {len(paths)} {'planned' if plan_only else 'files written'}"
            )
            if not plan_only and st.combine_mode == "across":
                self.log.appendPlainText(
                    "Combined outputs generated in 'combined' subfolder."
                )
            self.log.appendPlainText(completion_art())
            self.btn_run.setEnabled(True)
            self.btn_preview.setEnabled(True)
            self.btn_cancel.setEnabled(False)
            self.progress.setValue(100)
            self._progress_done = self._progress_total
            self._timer.stop()
            self._update_time()

        self.worker.finished_ok.connect(on_ok)

        def on_fail(msg: str):
            self.log.appendPlainText("ERROR: " + msg)
            self.btn_run.setEnabled(True)
            self.btn_preview.setEnabled(True)
            self.btn_cancel.setEnabled(False)
            self._timer.stop()
            self._update_time()

        self.worker.failed.connect(on_fail)
        self.worker.start()

    def _fmt_secs(self, secs: float) -> str:
        secs = int(secs)
        return f"{secs // 3600:02}:{secs % 3600 // 60:02}:{secs % 60:02}"

    def _update_time(self) -> None:
        if self._start_time is None:
            return
        elapsed = time.monotonic() - self._start_time
        eta = "--:--:--"
        if self._progress_total > 0:
            if 0 < self._progress_done < self._progress_total:
                remaining = (
                    elapsed
                    * (self._progress_total - self._progress_done)
                    / self._progress_done
                )
                eta = self._fmt_secs(remaining)
            elif self._progress_done >= self._progress_total:
                eta = "00:00:00"
        runtime = self._fmt_secs(elapsed)
        self.time_label.setText(f"Runtime: {runtime}   ETA: {eta}")

    def _cancel(self):
        if hasattr(self, "worker"):
            self.worker.cancel()
            self.log.appendPlainText("Cancel requested…")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # pragma: no cover - GUI
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(event)
