import os
import json

class ConfigManager:
    def __init__(self):
        self.config_path = os.path.join("data", "config.json")
        self.default_config = {
            "theme": "light",
            "save_path": "prompts"
        }
        os.makedirs("data", exist_ok=True)
        self._ensure_config()

    def _ensure_config(self):
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.default_config, f, indent=2)

    def load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_config(self, config_data):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)

    def get_theme(self):
        return self.load_config().get("theme", "light")

    def set_theme(self, theme):
        config = self.load_config()
        config["theme"] = theme
        self.save_config(config)

    def get_save_path(self):
        return self.load_config().get("save_path", "prompts")

    def set_save_path(self, path):
        config = self.load_config()
        config["save_path"] = path
        self.save_config(config)
