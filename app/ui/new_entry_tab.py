import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt
from services.model_registry import ModelRegistry
from services.file_manager import FileManager

class NewEntryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.registry = ModelRegistry()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here")
        layout.addWidget(QLabel("Prompt:"))
        layout.addWidget(self.prompt_input)

        self.model_selector = QComboBox()
        self.model_selector.setEditable(True)
        self.model_selector.addItems(self.registry.load_models())
        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.model_selector)

        self.response_input = QTextEdit()
        self.response_input.setPlaceholderText("Paste the model's response here")
        layout.addWidget(QLabel("Response:"))
        layout.addWidget(self.response_input)

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Comma-separated tags")
        layout.addWidget(QLabel("Tags (optional):"))
        layout.addWidget(self.tags_input)

        self.use_markdown = QCheckBox("Save as Markdown")
        self.use_markdown.setChecked(True)
        self.use_json = QCheckBox("Save as JSON")
        self.use_json.setChecked(True)
        format_layout = QHBoxLayout()
        format_layout.addWidget(self.use_markdown)
        format_layout.addWidget(self.use_json)
        layout.addLayout(format_layout)

        self.save_button = QPushButton("Save Entry")
        self.save_button.clicked.connect(self.save_entry)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_entry(self):
        prompt = self.prompt_input.toPlainText().strip()
        model = self.model_selector.currentText().strip()
        response = self.response_input.toPlainText().strip()
        tags = [tag.strip() for tag in self.tags_input.text().split(',') if tag.strip()]

        if not prompt or not response or not model:
            QMessageBox.warning(self, "Missing Info", "Please fill in the prompt, model, and response.")
            return

        today = datetime.now().strftime('%Y-%m-%d')
        slug = "_".join(prompt[:40].lower().split())
        folder_name = os.path.join("prompts", f"{today}_{slug}")

        os.makedirs(folder_name, exist_ok=True)

        file_manager = FileManager(folder_name)
        if self.use_markdown.isChecked():
            file_manager.save_markdown(prompt, model, response)
        if self.use_json.isChecked():
            file_manager.save_json(prompt, model, response, tags, today)

        self.registry.save_model(model)
        self.registry.save_tags(tags)

        QMessageBox.information(self, "Success", f"Entry saved to {folder_name}")
        self.prompt_input.clear()
        self.response_input.clear()
        self.tags_input.clear()
