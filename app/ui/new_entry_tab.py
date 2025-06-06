import os
import re
import json
import tempfile
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDropEvent
from app.services.prompt_service import PromptService
from app.services.model_service import ModelService
import html2text
import pypandoc
from docx2md import do_convert
import mdformat

class MarkdownTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def insertFromMimeData(self, source):
        if source.hasHtml():
            html = source.html()
            markdown = html2text.html2text(html)
            self.insertPlainText(markdown)
        elif source.hasText():
            text = source.text()
            if text.startswith('<?xml') or '<w:document' in text:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                        tmp.write(text.encode('utf-8'))
                        tmp_path = tmp.name
                    markdown = pypandoc.convert_file(tmp_path, 'gfm')
                except Exception:
                    markdown = do_convert(tmp_path, use_md_table=True)
                self.insertPlainText(markdown)
            else:
                super().insertFromMimeData(source)
        else:
            super().insertFromMimeData(source)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().endswith(".docx"):
                    event.acceptProposedAction()
                    return
        super().dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(".docx"):
                    try:
                        markdown = pypandoc.convert_file(file_path, 'gfm')
                    except Exception:
                        markdown = do_convert(file_path, use_md_table=True)
                    self.insertPlainText(markdown)
                    event.acceptProposedAction()
                    return
        super().dropEvent(event)

class NewEntryTab(QWidget):
    def __init__(self, base_path="prompts"):
        super().__init__()
        self.base_path = base_path
        self.prompt_service = PromptService()
        self.model_service = ModelService()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.prompt_input = MarkdownTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here")
        layout.addWidget(QLabel("Prompt:"))
        layout.addWidget(self.prompt_input)

        self.model_selector = QComboBox()
        self.model_selector.setEditable(True)
        self.refresh_model_list()
        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.model_selector)

        self.refresh_button = QPushButton("Refresh Models")
        self.refresh_button.clicked.connect(self.refresh_and_reload_models)
        layout.addWidget(self.refresh_button)

        self.response_input = MarkdownTextEdit()
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

    def refresh_model_list(self):
        self.model_selector.clear()
        models = self.model_service.get_models()
        self.model_selector.addItems(sorted(models))

    def refresh_and_reload_models(self):
        self.model_service.refresh_all_models()
        self.refresh_model_list()
        QMessageBox.information(self, "Models Updated", "Model list refreshed from external sources.")

    def save_entry(self):
        prompt = self.prompt_input.toPlainText().strip()
        model = self.model_selector.currentText().strip()
        sanitized_model = re.sub(r'[^\w\-]', '_', model)
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

            formatted_prompt_md = mdformat.text(prompt_md)
            formatted_response_md = mdformat.text(response_md)

            with open(os.path.join(folder_name, "prompt.md"), 'w', encoding='utf-8') as f:
                f.write(formatted_prompt_md)

            with open(os.path.join(folder_name, f"{sanitized_model}.md"), 'w', encoding='utf-8') as f:
                f.write(formatted_response_md)

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

        self.prompt_service.create_prompt(prompt, response, model, tags)

        QMessageBox.information(self, "Success", f"Entry saved to {folder_name}")
        self.prompt_input.clear()
        self.response_input.clear()
        self.tags_input.clear()
