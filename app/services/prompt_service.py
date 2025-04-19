import os
from datetime import datetime
from app.db.db_manager import DBManager


class PromptService:
    def __init__(self, db_path="data/prompt_index.db"):
        self.db = DBManager(db_path)

    def create_prompt(self, text, response, model_name, tags=None):
        prompt_id = self.db.add_prompt(text, tags)
        self.db.add_response(prompt_id, model_name, response)
        return prompt_id

    def update_prompt(self, prompt_id, new_text=None, new_tags=None):
        # For now we only support tag updates via full replace
        if new_text:
            self.db.conn.execute(
                "UPDATE Prompt SET text = ?, created_at = ? WHERE id = ?",
                (new_text, datetime.now().isoformat(), prompt_id)
            )
            self.db.conn.commit()

        if new_tags:
            self.db.conn.execute("DELETE FROM PromptTag WHERE prompt_id = ?", (prompt_id,))
            self.db.conn.commit()
            self.db._link_tags_to_prompt(new_tags, prompt_id)

    def get_prompt_by_id(self, prompt_id):
        return self.db.get_prompt_by_id(prompt_id)

    def get_comparison_responses(self, prompt_id):
        return self.db.get_model_responses(prompt_id)

    def search_prompts(self, keyword=None, tags=None, model=None, include_response=False):
        # Currently `model` is not a direct filter, can extend DBManager for that
        return self.db.search_prompts(keyword, tags, include_response=include_response)

    def get_all_tags(self):
        return [row["name"] for row in self.db.get_all_tags()]

    def close(self):
        self.db.close()
