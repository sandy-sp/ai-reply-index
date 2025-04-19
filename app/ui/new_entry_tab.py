import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt
from app.db.db_manager import DBManager

class NewEntryTab(QWidget):
    def __init__(self, base_path="prompts"):
        super().__init__()
        self.base_path = base_path
        self.db = DBManager()
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
        self.model_selector.addItems([m["name"] for m in self.db.get_all_models()])
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
        folder_name = os.path.join(self.base_path, f"{today}_{slug}")

        os.makedirs(folder_name, exist_ok=True)

        if self.use_markdown.isChecked():
            prompt_md = f"# Prompt\n\n{prompt}\n"
            response_md = f"# Response from {model}\n\n{response}\n"
            with open(os.path.join(folder_name, "prompt.md"), 'w', encoding='utf-8') as f:
                f.write(prompt_md)
            with open(os.path.join(folder_name, f"{model}.md"), 'w', encoding='utf-8') as f:
                f.write(response_md)

        if self.use_json.isChecked():
            data = {
                "prompt": prompt,
                "model": model,
                "response": response,
                "tags": tags,
                "date": today
            }
            with open(os.path.join(folder_name, "metadata.json"), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        prompt_id = self.db.add_prompt(prompt, tags)
        self.db.add_response(prompt_id, model, response)

        QMessageBox.information(self, "Success", f"Entry saved to {folder_name}")
        self.prompt_input.clear()
        self.response_input.clear()
        self.tags_input.clear()
