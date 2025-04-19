import os
import json
from huggingface_hub import HfApi
from app.db.db_manager import DBManager

class ModelRegistry:
    def __init__(self):
        self.registry_path = os.path.join("data", "model_tags.json")
        os.makedirs("data", exist_ok=True)
        self._ensure_file()
        self.db = DBManager()
        self.api = HfApi()

        self.COMMERCIAL_MODELS = [
            {"name": "ChatGPT", "provider": "OpenAI"},
            {"name": "Claude", "provider": "Anthropic"},
            {"name": "Gemini", "provider": "Google"},
            {"name": "Mistral", "provider": "Mistral.ai"},
            {"name": "Groq", "provider": "Groq"}
        ]

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

    def preload_commercial_models(self):
        for entry in self.COMMERCIAL_MODELS:
            name = entry["name"]
            self.save_model(name)
            self.db.get_or_create_model(name)

    def fetch_huggingface_models(self, limit=50):
        hf_models = self.api.list_models(filter="text-generation", sort="downloads", limit=limit)
        for model in hf_models:
            name = model.modelId
            if name:
                self.save_model(name)
                self.db.get_or_create_model(name)

    def refresh_registry(self):
        self.preload_commercial_models()
        self.fetch_huggingface_models()
        print("✅ Model registry updated from commercial and Hugging Face sources.")
