# ui/browse_tab.py
import os
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox
)
from services.file_manager import FileManager

class BrowseTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_folder = None
        self.init_ui()
        self.load_prompt_folders()

    def init_ui(self):
        layout = QHBoxLayout()

        self.folder_list = QListWidget()
        self.folder_list.itemClicked.connect(self.load_entry_data)
        layout.addWidget(self.folder_list, 2)

        right_layout = QVBoxLayout()

        self.prompt_display = QTextEdit()
        self.prompt_display.setPlaceholderText("Prompt will appear here...")
        right_layout.addWidget(QLabel("Prompt:"))
        right_layout.addWidget(self.prompt_display)

        self.response_display = QTextEdit()
        self.response_display.setPlaceholderText("Response will appear here...")
        right_layout.addWidget(QLabel("Response:"))
        right_layout.addWidget(self.response_display)

        self.save_button = QPushButton("Update Entry")
        self.save_button.clicked.connect(self.save_updates)
        right_layout.addWidget(self.save_button)

        layout.addLayout(right_layout, 5)
        self.setLayout(layout)

    def load_prompt_folders(self):
        self.folder_list.clear()
        if not os.path.exists("prompts"):
            return

        for folder in sorted(os.listdir("prompts")):
            full_path = os.path.join("prompts", folder)
            if os.path.isdir(full_path):
                item = QListWidgetItem(folder)
                item.setData(1000, full_path)
                self.folder_list.addItem(item)

    def load_entry_data(self, item):
        folder_path = item.data(1000)
        self.selected_folder = folder_path
        manager = FileManager(folder_path)
        data = manager.load_entry()

        if data:
            self.prompt_display.setText(data.get("prompt", ""))
            self.response_display.setText(data.get("response", ""))
        else:
            self.prompt_display.setText("")
            self.response_display.setText("")

    def save_updates(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "No Entry Selected", "Please select an entry to update.")
            return

        updated_data = {
            "prompt": self.prompt_display.toPlainText(),
            "response": self.response_display.toPlainText()
        }

        manager = FileManager(self.selected_folder)
        original = manager.load_entry() or {}
        original.update(updated_data)
        manager.update_entry(original)

        QMessageBox.information(self, "Updated", "Entry successfully updated.")
