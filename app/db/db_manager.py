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
        prompt_id = cur.lastrowid
        self.conn.commit()
        if tags:
            self._link_tags_to_prompt(tags, prompt_id)
        return prompt_id

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

    def search_prompts(self, keyword=None, tags=None, start_date=None, end_date=None):
        sql = "SELECT DISTINCT p.* FROM Prompt p"
        joins = []
        conditions = ["1=1"]
        params = []

        if tags:
            joins.append("JOIN PromptTag pt ON p.id = pt.prompt_id")
            joins.append("JOIN Tag t ON t.id = pt.tag_id")
            tag_placeholders = ",".join(["?"] * len(tags))
            conditions.append(f"t.name IN ({tag_placeholders})")
            params.extend(tags)

        if keyword:
            conditions.append("p.text LIKE ?")
            params.append(f"%{keyword}%")

        if start_date and end_date:
            conditions.append("p.created_at BETWEEN ? AND ?")
            params.append(start_date)
            params.append(end_date)

        if joins:
            sql += " " + " ".join(joins)
        sql += " WHERE " + " AND ".join(conditions) + " ORDER BY p.created_at DESC"

        return self.conn.execute(sql, params).fetchall()

    def get_prompt_by_id(self, prompt_id):
        return self.conn.execute("SELECT * FROM Prompt WHERE id = ?", (prompt_id,)).fetchone()

    def get_model_responses(self, prompt_id):
        return self.conn.execute("""
            SELECT m.name AS model, r.content, r.created_at
            FROM Response r
            JOIN Model m ON r.model_id = m.id
            WHERE r.prompt_id = ?
            ORDER BY r.created_at
        """, (prompt_id,)).fetchall()

    def get_all_tags(self):
        return self.conn.execute("SELECT name FROM Tag ORDER BY name").fetchall()

    def get_all_models(self):
        return self.conn.execute("SELECT name FROM Model ORDER BY name").fetchall()

    def get_tags_for_prompt(self, prompt_id):
        return self.conn.execute("""
            SELECT t.name FROM Tag t
            JOIN PromptTag pt ON t.id = pt.tag_id
            WHERE pt.prompt_id = ?
        """, (prompt_id,)).fetchall()

    def _link_tags_to_prompt(self, tags, prompt_id):
        cur = self.conn.cursor()
        for tag in tags:
            tag = tag.strip()
            if not tag:
                continue
            cur.execute("SELECT id FROM Tag WHERE name = ?", (tag,))
            row = cur.fetchone()
            if row:
                tag_id = row["id"]
            else:
                cur.execute("INSERT INTO Tag (name) VALUES (?)", (tag,))
                tag_id = cur.lastrowid
            cur.execute("INSERT OR IGNORE INTO PromptTag (prompt_id, tag_id) VALUES (?, ?)", (prompt_id, tag_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
