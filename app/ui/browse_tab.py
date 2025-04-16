import os
import shutil
import markdown2
from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QTabWidget, QTextBrowser
)
from services.file_manager import FileManager

class BrowseTab(QWidget):
    def __init__(self, base_path="prompts"):
        super().__init__()
        self.base_path = base_path
        self.selected_folder = None
        self.init_ui()
        self.load_prompt_folders()

    def init_ui(self):
        layout = QHBoxLayout()

        self.folder_list = QListWidget()
        self.folder_list.itemClicked.connect(self.load_entry_data)
        layout.addWidget(self.folder_list, 2)

        right_layout = QVBoxLayout()
        self.entry_tabs = QTabWidget()

        # Edit tab
        self.edit_tab = QWidget()
        edit_layout = QVBoxLayout()
        self.prompt_display = QTextEdit()
        self.prompt_display.setPlaceholderText("Prompt will appear here...")
        edit_layout.addWidget(QLabel("Prompt:"))
        edit_layout.addWidget(self.prompt_display)

        self.response_display = QTextEdit()
        self.response_display.setPlaceholderText("Response will appear here...")
        edit_layout.addWidget(QLabel("Response:"))
        edit_layout.addWidget(self.response_display)

        self.save_button = QPushButton("Update Entry")
        self.save_button.clicked.connect(self.save_updates)
        edit_layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Delete Entry")
        self.delete_button.clicked.connect(self.delete_entry)
        edit_layout.addWidget(self.delete_button)

        self.edit_tab.setLayout(edit_layout)
        self.entry_tabs.addTab(self.edit_tab, "Edit")

        # Preview tab
        self.preview_tab = QWidget()
        preview_layout = QVBoxLayout()
        self.preview_browser = QTextBrowser()
        preview_layout.addWidget(self.preview_browser)
        self.preview_tab.setLayout(preview_layout)
        self.entry_tabs.addTab(self.preview_tab, "Preview")

        right_layout.addWidget(self.entry_tabs)
        layout.addLayout(right_layout, 5)
        self.setLayout(layout)

    def load_prompt_folders(self):
        self.folder_list.clear()
        if not os.path.exists(self.base_path):
            return

        for folder in sorted(os.listdir(self.base_path)):
            full_path = os.path.join(self.base_path, folder)
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

            # Markdown preview
            markdown_text = f"# Prompt\n\n{data.get('prompt', '')}\n\n# Response\n\n{data.get('response', '')}"
            html = markdown2.markdown(markdown_text)
            self.preview_browser.setHtml(html)
        else:
            self.prompt_display.setText("")
            self.response_display.setText("")
            self.preview_browser.setHtml("")

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
        self.load_prompt_folders()

    def delete_entry(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "No Entry Selected", "Please select an entry to delete.")
            return

        folder_name = os.path.basename(self.selected_folder)
        confirm = QMessageBox.question(
            self, "Delete Entry",
            f"Are you sure you want to delete '{folder_name}'? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            shutil.rmtree(self.selected_folder)
            self.selected_folder = None
            self.load_prompt_folders()
            self.prompt_display.clear()
            self.response_display.clear()
            self.preview_browser.clear()
            QMessageBox.information(self, "Deleted", f"Entry '{folder_name}' deleted.")
