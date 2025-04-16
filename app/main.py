import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

class AIReplyIndexApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Reply Index - Prompt Logger")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here")
        layout.addWidget(QLabel("Prompt:"))
        layout.addWidget(self.prompt_input)

        self.model_selector = QComboBox()
        self.model_selector.setEditable(True)
        self.model_selector.addItems(["chatgpt-4", "claude-3", "gemini"])
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
        model = self.model_selector.currentText().strip().lower()
        response = self.response_input.toPlainText().strip()
        tags = [tag.strip() for tag in self.tags_input.text().split(',') if tag.strip()]

        if not prompt or not response or not model:
            QMessageBox.warning(self, "Missing Info", "Please fill in the prompt, model, and response.")
            return

        today = datetime.now().strftime('%Y-%m-%d')
        slug = "_".join(prompt[:40].lower().split())
        folder_name = f"prompts/{today}_{slug}"

        os.makedirs(folder_name, exist_ok=True)

        if self.use_markdown.isChecked():
            with open(f"{folder_name}/prompt.md", 'w', encoding='utf-8') as f:
                f.write(f"## Prompt:\n{prompt}\n")
            with open(f"{folder_name}/{model}.md", 'w', encoding='utf-8') as f:
                f.write(f"## Response from {model}:\n{response}\n")

        if self.use_json.isChecked():
            metadata = {
                "prompt": prompt,
                "model": model,
                "response": response,
                "tags": tags,
                "date": today
            }
            with open(f"{folder_name}/metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)

        QMessageBox.information(self, "Success", f"Entry saved to {folder_name}")
        self.prompt_input.clear()
        self.response_input.clear()
        self.tags_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AIReplyIndexApp()
    window.show()
    sys.exit(app.exec_())
