import os
import shutil
import json
import markdown2
from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QTabWidget, QTextBrowser,
    QLineEdit, QComboBox, QScrollArea, QFrame, QSplitter, QCheckBox
)
from PyQt5.QtCore import Qt
from app.db.db_manager import DBManager
from app.services.model_registry import ModelRegistry

class BrowseTab(QWidget):
    def __init__(self, base_path="prompts"):
        super().__init__()
        self.base_path = base_path
        self.selected_folder = None
        self.db = DBManager()
        self.registry = ModelRegistry()
        self.init_ui()
        self.load_tags()
        self.load_prompt_folders()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Filter Panel
        filter_layout = QHBoxLayout()
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Search by keyword")
        filter_layout.addWidget(QLabel("Keyword:"))
        filter_layout.addWidget(self.keyword_input)

        self.model_filter = QComboBox()
        self.model_filter.setEditable(True)
        self.model_filter.addItem("Any")
        self.refresh_model_filter()
        filter_layout.addWidget(QLabel("Model:"))
        filter_layout.addWidget(self.model_filter)

        self.include_response_check = QCheckBox("Search in responses")
        filter_layout.addWidget(self.include_response_check)

        self.model_refresh_button = QPushButton("↻")
        self.model_refresh_button.setToolTip("Refresh model list")
        self.model_refresh_button.clicked.connect(self.refresh_and_reload_model_filter)
        filter_layout.addWidget(self.model_refresh_button)

        self.apply_button = QPushButton("Apply Filters")
        self.apply_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(self.apply_button)

        main_layout.addLayout(filter_layout)

        # Splitter for tag list and folder list/content
        splitter = QSplitter(Qt.Horizontal)

        self.tag_list = QListWidget()
        self.tag_list.itemClicked.connect(self.filter_by_tag)
        splitter.addWidget(self.tag_list)

        self.folder_list = QListWidget()
        self.folder_list.itemClicked.connect(self.load_entry_data)
        splitter.addWidget(self.folder_list)
        splitter.setSizes([100, 300])

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

        # Compare Tab
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
        right_container = QWidget()
        right_container.setLayout(right_layout)
        splitter.addWidget(right_container)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def load_tags(self):
        self.tag_list.clear()
        for row in self.db.get_all_tags():
            tag = row["name"]
            item = QListWidgetItem(tag)
            item.setData(Qt.UserRole, tag)
            self.tag_list.addItem(item)

    def filter_by_tag(self, item):
        tag = item.data(Qt.UserRole)
        results = self.db.search_prompts(tags=[tag])
        self.load_prompt_folders(filtered_prompts=results)

    def load_prompt_folders(self, filtered_prompts=None):
        self.folder_list.clear()
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
                    metadata_path = os.path.join(full_path, "metadata.json")
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r', encoding='utf-8') as f:
                            try:
                                meta = json.load(f)
                                prompt_text = meta.get("prompt")
                                if prompt_text:
                                    result = self.db.search_prompts(keyword=prompt_text)
                                    if result:
                                        item.setData(1001, result[0]["id"])
                            except Exception:
                                pass
                    self.folder_list.addItem(item)

    def apply_filters(self):
        keyword = self.keyword_input.text().strip() or None
        tags = None
        model = self.model_filter.currentText()
        if model == "Any":
            model = None
        include_response = self.include_response_check.isChecked()
        results = self.db.search_prompts(
            keyword=keyword,
            tags=tags,
            start_date=None,
            end_date=None,
            include_response=include_response
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

        self.compare_layout.setAlignment(Qt.AlignLeft)
        while self.compare_layout.count():
            widget = self.compare_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        if not prompt_id:
            QMessageBox.warning(self, "Compare Disabled", "No prompt ID found for this entry.")
            return

        comparisons = self.db.get_model_responses(prompt_id)
        for resp in comparisons:
            section = QTextBrowser()
            section.setMinimumWidth(300)
            section.setStyleSheet("border: 1px solid #aaa; padding: 10px; margin: 10px;")
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

    def refresh_model_filter(self):
        self.model_filter.clear()
        self.model_filter.addItem("Any")
        models = self.registry.load_models()
        self.model_filter.addItems(sorted(models))

    def refresh_and_reload_model_filter(self):
        self.registry.refresh_registry()
        self.refresh_model_filter()
