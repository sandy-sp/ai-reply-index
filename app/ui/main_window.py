from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from ui.new_entry_tab import NewEntryTab
from ui.browse_tab import BrowseTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Reply Index")
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()

        self.new_entry_tab = NewEntryTab()
        self.browse_tab = BrowseTab()

        self.tabs.addTab(self.new_entry_tab, "New Entry")
        self.tabs.addTab(self.browse_tab, "Browse/Edit")

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        container.setLayout(layout)

        self.setCentralWidget(container)
