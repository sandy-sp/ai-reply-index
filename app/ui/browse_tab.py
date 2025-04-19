import os
import shutil
import json
import markdown2
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QTabWidget, QTextBrowser,
    QLineEdit, QComboBox, QDateEdit, QScrollArea, QFrame
)
from PyQt5.QtCore import QDate, Qt
from app.db.db_manager import DBManager

class BrowseTab(QWidget):
    def __init__(self, base_path="prompts"):
        super().__init__()
        self.base_path = base_path
        self.selected_folder = None
        self.db = DBManager()
        self.init_ui()
        self.load_prompt_folders()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # === Filter Panel ===
        filter_layout = QHBoxLayout()

        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Search by keyword")
        filter_layout.addWidget(QLabel("Keyword:"))
        filter_layout.addWidget(self.keyword_input)

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Comma-separated tags")
        filter_layout.addWidget(QLabel("Tags:"))
        filter_layout.addWidget(self.tag_input)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.end_date)

        self.model_filter = QComboBox()
        self.model_filter.setEditable(True)
        self.model_filter.addItem("Any")
        for model in self.db.get_all_models():
            self.model_filter.addItem(model["name"])
        filter_layout.addWidget(QLabel("Model:"))
        filter_layout.addWidget(self.model_filter)

        self.apply_button = QPushButton("Apply Filters")
        self.apply_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(self.apply_button)

        main_layout.addLayout(filter_layout)

        # === Main Panel ===
        content_layout = QHBoxLayout()

        self.folder_list = QListWidget()
        self.folder_list.itemClicked.connect(self.load_entry_data)
        content_layout.addWidget(self.folder_list, 2)

        right_layout = QVBoxLayout()
        self.entry_tabs = QTabWidget()

        # Edit Tab
        self.edit_tab = QWidget()
        edit_layout = QVBoxLayout()
        self.prompt_display = QTextEdit()
        edit_layout.addWidget(QLabel("Prompt:"))
        edit_layout.addWidget(self.prompt_display)

        self.response_display = QTextEdit()
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

        # Preview Tab
        self.preview_tab = QWidget()
        preview_layout = QVBoxLayout()
        self.preview_browser = QTextBrowser()
        preview_layout.addWidget(self.preview_browser)
        self.preview_tab.setLayout(preview_layout)
        self.entry_tabs.addTab(self.preview_tab, "Preview")

        # Comparison Tab
        self.compare_tab = QWidget()
        compare_layout = QVBoxLayout()
        self.compare_area = QScrollArea()
        self.compare_area.setWidgetResizable(True)
        self.compare_content = QFrame()
        self.compare_layout = QHBoxLayout()
        self.compare_content.setLayout(self.compare_layout)
        self.compare_area.setWidget(self.compare_content)
        compare_layout.addWidget(self.compare_area)
        self.compare_tab.setLayout(compare_layout)
        self.entry_tabs.addTab(self.compare_tab, "Compare")

        right_layout.addWidget(self.entry_tabs)
        content_layout.addLayout(right_layout, 5)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def load_prompt_folders(self, filtered_prompts=None):
        self.folder_list.clear()
        folders = []

        if filtered_prompts:
            for prompt in filtered_prompts:
                folder_slug = prompt["created_at"].split("T")[0] + "_" + "_".join(prompt["text"][:40].lower().split())
                folder_path = os.path.join(self.base_path, folder_slug)
                if os.path.exists(folder_path):
                    item = QListWidgetItem(folder_slug)
                    item.setData(1000, folder_path)
                    item.setData(1001, prompt["id"])
                    self.folder_list.addItem(item)
        else:
            if not os.path.exists(self.base_path):
                return
            for folder in sorted(os.listdir(self.base_path)):
                full_path = os.path.join(self.base_path, folder)
                if os.path.isdir(full_path):
                    item = QListWidgetItem(folder)
                    item.setData(1000, full_path)
                    self.folder_list.addItem(item)

    def apply_filters(self):
        keyword = self.keyword_input.text().strip() or None
        tags = [t.strip() for t in self.tag_input.text().split(",") if t.strip()]
        tags = tags if tags else None
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        model = self.model_filter.currentText()
        if model == "Any":
            model = None

        results = self.db.search_prompts(
            keyword=keyword,
            tags=tags,
            start_date=start_date,
            end_date=end_date
        )

        self.load_prompt_folders(filtered_prompts=results)

    def load_entry_data(self, item):
        folder_path = item.data(1000)
        prompt_id = item.data(1001)
        self.selected_folder = folder_path

        metadata_path = os.path.join(folder_path, "metadata.json")
        if not os.path.exists(metadata_path):
            return

        with open(metadata_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.prompt_display.setText(data.get("prompt", ""))
        self.response_display.setText(data.get("response", ""))

        markdown_text = f"# Prompt\n\n{data.get('prompt', '')}\n\n# Response\n\n{data.get('response', '')}"
        html = markdown2.markdown(markdown_text)
        self.preview_browser.setHtml(html)

        # Load model comparisons
        self.compare_layout.setAlignment(Qt.AlignLeft)
        while self.compare_layout.count():
            widget = self.compare_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        if prompt_id:
            comparisons = self.db.get_model_responses(prompt_id)
            for resp in comparisons:
                section = QTextBrowser()
                section.setMinimumWidth(300)
                text = f"<h3>{resp['model']}</h3><p><i>{resp['created_at']}</i></p><hr><p>{resp['content']}</p>"
                section.setHtml(text)
                self.compare_layout.addWidget(section)

    def save_updates(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "No Entry Selected", "Please select an entry to update.")
            return

        updated_data = {
            "prompt": self.prompt_display.toPlainText(),
            "response": self.response_display.toPlainText()
        }

        metadata_path = os.path.join(self.selected_folder, "metadata.json")
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                original = json.load(f)
        except FileNotFoundError:
            original = {}

        original.update(updated_data)
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(original, f, indent=2)

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
