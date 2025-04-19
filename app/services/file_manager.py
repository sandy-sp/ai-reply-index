import os
import json
from datetime import datetime

class FileManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def save_markdown(self, prompt, model, response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        prompt_md = (
            f"# Prompt\n"
            f"> Timestamp: {timestamp}\n\n"
            f"```text\n{prompt}\n```\n"
        )

        response_md = (
            f"# Response from {model}\n\n"
            f"```text\n{response}\n```\n"
        )

        with open(os.path.join(self.folder_path, "prompt.md"), 'w', encoding='utf-8') as f:
            f.write(prompt_md)

        with open(os.path.join(self.folder_path, f"{model}.md"), 'w', encoding='utf-8') as f:
            f.write(response_md)

    def save_json(self, prompt, model, response, tags, date):
        data = {
            "prompt": prompt,
            "model": model,
            "response": response,
            "tags": tags,
            "date": date,
            "created_at": datetime.now().isoformat()
        }
        with open(os.path.join(self.folder_path, "metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_entry(self):
        try:
            with open(os.path.join(self.folder_path, "metadata.json"), 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def update_entry(self, updated_data):
        with open(os.path.join(self.folder_path, "metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2)
