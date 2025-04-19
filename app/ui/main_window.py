from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QAction, QFileDialog, QMenuBar
)
from ui.new_entry_tab import NewEntryTab
from ui.browse_tab import BrowseTab
from services.config import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Reply Index")
        self.setMinimumSize(800, 600)
        self.config = ConfigManager()
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        self.tabs = QTabWidget()

        save_path = self.config.get_save_path()
        self.new_entry_tab = NewEntryTab(base_path=save_path)
        self.browse_tab = BrowseTab(base_path=save_path)

        self.tabs.addTab(self.new_entry_tab, "New Entry")
        self.tabs.addTab(self.browse_tab, "Browse/Edit")

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.init_menu()

    def init_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")

        theme_toggle = QAction("Toggle Dark Mode", self)
        theme_toggle.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_toggle)

        path_action = QAction("Set Save Directory", self)
        path_action.triggered.connect(self.set_save_path)
        settings_menu.addAction(path_action)

    def apply_theme(self):
        theme = self.config.get_theme()
        if theme == "dark":
            try:
                with open("assets/style.qss", 'r') as f:
                    self.setStyleSheet(f.read())
            except FileNotFoundError:
                pass
        else:
            self.setStyleSheet("")

    def toggle_theme(self):
        current = self.config.get_theme()
        new_theme = "dark" if current == "light" else "light"
        self.config.set_theme(new_theme)
        self.apply_theme()

    def set_save_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        if directory:
            self.config.set_save_path(directory)
            self.new_entry_tab.base_path = directory
            self.browse_tab.base_path = directory
            self.browse_tab.load_prompt_folders()
