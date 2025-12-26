# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class HelpDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, version="4.0"):
        super().__init__(parent)
        self.setWindowTitle("Help & About")
        self.resize(700, 500)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        layout = QtWidgets.QVBoxLayout(self)
        
        # Tab Widget
        self.tabs = QtWidgets.QTabWidget()
        layout.addWidget(self.tabs)
        
        # --- Tab 1: Usage Guide ---
        self.tab_usage = QtWidgets.QWidget()
        usage_layout = QtWidgets.QVBoxLayout(self.tab_usage)
        self.txt_usage = QtWidgets.QTextBrowser()
        self.txt_usage.setOpenExternalLinks(True)
        self.txt_usage.setHtml(self._get_usage_html())
        usage_layout.addWidget(self.txt_usage)
        self.tabs.addTab(self.tab_usage, "Usage Guide")
        
        # --- Tab 2: About ---
        self.tab_about = QtWidgets.QWidget()
        about_layout = QtWidgets.QVBoxLayout(self.tab_about)
        self.txt_about = QtWidgets.QTextBrowser()
        self.txt_about.setOpenExternalLinks(True)
        self.txt_about.setHtml(self._get_about_html(version))
        about_layout.addWidget(self.txt_about)
        self.tabs.addTab(self.tab_about, "About")
        
        # Close Button
        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
        btn_box.rejected.connect(self.close)
        layout.addWidget(btn_box)

    def _get_usage_html(self):
        return """
        <style>
            body { font-family: 'Segoe UI', sans-serif; color: #E0E0E0; background-color: #2D2D2D; }
            h2 { color: #5B9BD5; margin-top: 5px; }
            h3 { color: #9E9E9E; margin-bottom: 5px; }
            ul { margin-left: -20px; }
            li { margin-bottom: 5px; }
            b { color: #DCDCDC; }
            .step { color: #80C0FF; font-weight: bold; }
        </style>
        <h2>SWMM Timeseries Extractor Usage</h2>
        
        <p>This tool extracts time series data from SWMM binary output files (<code>.out</code>) into standard formats like CSV, DAT, or TSF.</p>
        
        <h3><span class="step">1. Sources</span></h3>
        <p>Drag and drop <code>.out</code> files into the list or use the <b>Add .out files</b> button. The application will automatically scan the files to discover available IDs and object types.</p>
        
        <h3><span class="step">2. IDs</span></h3>
        <p>Select the object type (Node, Link, Subcatchment, etc.) from the dropdown. 
        <ul>
            <li>Use the search bar to filter IDs.</li>
            <li>Click <b>All</b> to select all matching IDs, or manually check specific ones.</li>
            <li>Toggle between <b>Union</b> (all IDs found in any file) or <b>Intersection</b> (only IDs common to all files).</li>
        </ul>
        </p>

        <h3><span class="step">3. Parameters</span></h3>
        <p>Select the variables you wish to extract (e.g., Depth, Flow, Rainfall). You can also override output units here (e.g., convert CFS to GPM).</p>
        
        <h3><span class="step">4. Options</span></h3>
        <p>Configure file naming and formats:
        <ul>
            <li><b>Format:</b> Choose TSF, DAT, or CSV.</li>
            <li><b>Combine inputs:</b> Choose how to group the data (separate files per parameter, or combined files).</li>
            <li><b>Start / End Time:</b> Optional duration filter.</li>
        </ul>
        </p>

        <h3><span class="step">5. Output & Run</span></h3>
        <p>Select the destination folder. Click <b>Run</b> to start the extraction. A progress bar will show the status.</p>
        """

    def _get_about_html(self, version):
        return f"""
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; color: #E0E0E0; }}
            h1 {{ color: #5B9BD5; }}
            h3 {{ color: #9E9E9E; }}
            p {{ line-height: 1.4; }}
            .highlight {{ color: #FFD700; }}
        </style>
        <div align="center">
            <h1>Timeseries Extractor</h1>
            <p><b>Version:</b> {version}</p>
            <p>A unified tool for extracting hydraulic and hydrologic data from SWMM model results.</p>
        </div>
        
        <hr>
        
        <h3>Credits & Acknowledgements</h3>
        <p><b>Developer:</b> Ross Volkwein</p>
        <p>Developed with the assistance of <b>AI Coding Assistants</b>.</p>
        
        <h3>Core Technology</h3>
        <p>This application relies heavily on the open-source <a href="https://github.com/timcera/swmmtoolbox" style="color: #80C0FF;">swmmtoolbox</a> library created by <b>Tim Cera</b>.</p>
        <p>We gratefully acknowledge Tim Cera's work in making SWMM binary file parsing accessible to the Python community.</p>
        """
