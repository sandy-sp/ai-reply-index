import os
import json

class ModelRegistry:
    def __init__(self):
        self.registry_path = os.path.join("data", "model_tags.json")
        os.makedirs("data", exist_ok=True)
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump({"models": [], "tags": []}, f)

    def load_registry(self):
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_registry(self, data):
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_models(self):
        return self.load_registry().get("models", [])

    def load_tags(self):
        return self.load_registry().get("tags", [])

    def save_model(self, model):
        registry = self.load_registry()
        if model not in registry["models"]:
            registry["models"].append(model)
            self.save_registry(registry)

    def save_tags(self, new_tags):
        registry = self.load_registry()
        for tag in new_tags:
            if tag not in registry["tags"]:
                registry["tags"].append(tag)
        self.save_registry(registry)
