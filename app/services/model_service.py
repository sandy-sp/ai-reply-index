import os
import json
from huggingface_hub import HfApi
from app.db.db_manager import DBManager

class ModelService:
    def __init__(self):
        self.registry_path = os.path.join("data", "model_tags.json")
        self.db = DBManager()
        self.api = HfApi()
        os.makedirs("data", exist_ok=True)
        self._ensure_registry_file()

        self.commercial_models = [
            {"name": "ChatGPT", "provider": "OpenAI"},
            {"name": "Claude", "provider": "Anthropic"},
            {"name": "Gemini", "provider": "Google"},
            {"name": "Mistral", "provider": "Mistral.ai"},
            {"name": "Groq", "provider": "Groq"}
        ]

    def _ensure_registry_file(self):
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump({"models": [], "tags": []}, f)

    def _load_registry(self):
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_registry(self, data):
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def get_models(self):
        return self._load_registry().get("models", [])

    def add_model(self, model_name):
        registry = self._load_registry()
        if model_name not in registry["models"]:
            registry["models"].append(model_name)
            self._save_registry(registry)
        self.db.get_or_create_model(model_name)

    def preload_commercial_models(self):
        for model in self.commercial_models:
            self.add_model(model["name"])

    def fetch_huggingface_models(self, limit=50):
        hf_models = self.api.list_models(
            filter="text-generation", sort="downloads", limit=limit, full=False
        )
        for model in hf_models:
            name = model.modelId
            if name:
                self.add_model(name)

    def refresh_all_models(self):
        self.preload_commercial_models()
        self.fetch_huggingface_models()
        print("✅ Model registry updated.")

