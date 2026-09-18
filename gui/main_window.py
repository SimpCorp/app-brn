from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem, 
    QHeaderView, QFrame, QButtonGroup
)
from PyQt6.QtCore import Qt
from core.vpn_scanner import scan_installed_vpn_clients, scan_active_network_adapters
from core.extension_scanner import scan_browser_extensions
from gui.styles import LIGHT_THEME, DARK_THEME

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brindavan Endpoint Audit")
        self.resize(1020, 640)
        self.is_dark_mode = True

        self.init_ui()
        self.apply_theme()
        self.load_audit_data()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)

        # Header Frame
        header = QFrame()
        header.setObjectName("HeaderBar")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(28, 18, 28, 18)

        text_vbox = QVBoxLayout()
        title = QLabel("Brindavan Endpoint Audit")
        title.setObjectName("HeaderTitle")
        subtitle = QLabel("Administrative discovery of installed VPN clients, virtual adapters, and browser add-ons")
        subtitle.setObjectName("HeaderSubtitle")
        text_vbox.addWidget(title)
        text_vbox.addWidget(subtitle)

        self.theme_btn = QPushButton("Light Mode")
        self.theme_btn.setObjectName("ThemeBtn")
        self.theme_btn.clicked.connect(self.toggle_theme)

        header_layout.addLayout(text_vbox)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_btn)
        main_layout.addWidget(header)

        # Segmented Control Bar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(28, 0, 28, 0)

        seg_box = QFrame()
        seg_box.setObjectName("SegmentContainer")
        seg_layout = QHBoxLayout(seg_box)
        seg_layout.setContentsMargins(4, 4, 4, 4)
        seg_layout.setSpacing(4)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.tab_vpn_btn = QPushButton("VPNs & Network Adapters")
        self.tab_vpn_btn.setObjectName("SegmentBtn")
        self.tab_vpn_btn.setCheckable(True)
        self.tab_vpn_btn.setChecked(True)
        self.btn_group.addButton(self.tab_vpn_btn, 0)

        self.tab_ext_btn = QPushButton("Browser Extensions")
        self.tab_ext_btn.setObjectName("SegmentBtn")
        self.tab_ext_btn.setCheckable(True)
        self.btn_group.addButton(self.tab_ext_btn, 1)

        seg_layout.addWidget(self.tab_vpn_btn)
        seg_layout.addWidget(self.tab_ext_btn)

        self.btn_group.idClicked.connect(self.switch_tab)

        self.refresh_btn = QPushButton("Refresh Scan")
        self.refresh_btn.setObjectName("ActionBtn")
        self.refresh_btn.clicked.connect(self.load_audit_data)

        toolbar.addWidget(seg_box)
        toolbar.addStretch()
        toolbar.addWidget(self.refresh_btn)
        main_layout.addLayout(toolbar)

        # Content Stack
        self.stack = QStackedWidget()
        self.stack.setContentsMargins(28, 0, 28, 20)

        # Tab 1: VPN & Adapters Table
        self.vpn_table = QTableWidget()
        self.vpn_table.setColumnCount(3)
        self.vpn_table.setHorizontalHeaderLabels(["Entity Type", "Software / Adapter Name", "Status & Install Location"])
        self.vpn_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.vpn_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.vpn_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.vpn_table.verticalHeader().setVisible(False)
        self.vpn_table.setShowGrid(False)
        self.vpn_table.setAlternatingRowColors(True)

        # Tab 2: Browser Extensions Table
        self.ext_table = QTableWidget()
        self.ext_table.setColumnCount(5)
        self.ext_table.setHorizontalHeaderLabels(["Browser", "Extension Name", "Version", "Internal ID", "Storage Path"])
        self.ext_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.ext_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.ext_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.ext_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        self.ext_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.ext_table.verticalHeader().setVisible(False)
        self.ext_table.setShowGrid(False)
        self.ext_table.setAlternatingRowColors(True)

        self.stack.addWidget(self.vpn_table)
        self.stack.addWidget(self.ext_table)
        main_layout.addWidget(self.stack)

    def switch_tab(self, index):
        self.stack.setCurrentIndex(index)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_btn.setText("Light Mode" if self.is_dark_mode else "Dark Mode")
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(DARK_THEME if self.is_dark_mode else LIGHT_THEME)

    def load_audit_data(self):
        # 1. Populate VPNs & Interfaces
        self.vpn_table.setRowCount(0)
        clients = scan_installed_vpn_clients()
        adapters = scan_active_network_adapters()

        for c in clients:
            r = self.vpn_table.rowCount()
            self.vpn_table.insertRow(r)
            self.vpn_table.setItem(r, 0, QTableWidgetItem("Desktop Client"))
            self.vpn_table.setItem(r, 1, QTableWidgetItem(c["name"]))
            self.vpn_table.setItem(r, 2, QTableWidgetItem(c["location"]))

        for a in adapters:
            r = self.vpn_table.rowCount()
            self.vpn_table.insertRow(r)
            self.vpn_table.setItem(r, 0, QTableWidgetItem("Virtual Tunnel"))
            self.vpn_table.setItem(r, 1, QTableWidgetItem(a["interface"]))
            self.vpn_table.setItem(r, 2, QTableWidgetItem(f"{a['status']} ({a['speed']})"))

        # 2. Populate Browser Extensions
        self.ext_table.setRowCount(0)
        extensions = scan_browser_extensions()

        for ext in extensions:
            r = self.ext_table.rowCount()
            self.ext_table.insertRow(r)
            self.ext_table.setItem(r, 0, QTableWidgetItem(ext["browser"]))
            self.ext_table.setItem(r, 1, QTableWidgetItem(ext["name"]))
            self.ext_table.setItem(r, 2, QTableWidgetItem(ext["version"]))
            self.ext_table.setItem(r, 3, QTableWidgetItem(ext["id"]))
            self.ext_table.setItem(r, 4, QTableWidgetItem(ext["path"]))
