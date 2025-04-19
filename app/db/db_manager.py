import os
import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_path="data/prompt_index.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with open("app/db/schema.sql", "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def add_prompt(self, text, tags=None):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO Prompt (text, created_at, tags) VALUES (?, ?, ?)",
            (text, datetime.now().isoformat(), ",".join(tags or []))
        )
        self.conn.commit()
        return cur.lastrowid

    def get_or_create_model(self, model_name):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM Model WHERE name = ?", (model_name,))
        row = cur.fetchone()
        if row:
            return row["id"]
        cur.execute("INSERT INTO Model (name) VALUES (?)", (model_name,))
        self.conn.commit()
        return cur.lastrowid

    def add_response(self, prompt_id, model_name, content):
        model_id = self.get_or_create_model(model_name)
        self.conn.execute(
            "INSERT INTO Response (prompt_id, model_id, content, created_at) VALUES (?, ?, ?, ?)",
            (prompt_id, model_id, content, datetime.now().isoformat())
        )
        self.conn.commit()

    def fetch_prompts(self):
        return self.conn.execute("SELECT * FROM Prompt ORDER BY created_at DESC").fetchall()

    def fetch_responses_for_prompt(self, prompt_id):
        return self.conn.execute("""
            SELECT m.name AS model, r.content, r.created_at
            FROM Response r
            JOIN Model m ON r.model_id = m.id
            WHERE r.prompt_id = ?
            ORDER BY r.created_at
        """, (prompt_id,)).fetchall()

    def close(self):
        self.conn.close()
