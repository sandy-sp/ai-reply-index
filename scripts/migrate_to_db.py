import os
import json
from datetime import datetime
from app.db.db_manager import DBManager

def load_metadata(folder_path):
    try:
        with open(os.path.join(folder_path, "metadata.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def migrate_all_entries(prompts_path="prompts", db_path="data/prompt_index.db"):
    db = DBManager(db_path)

    if not os.path.exists(prompts_path):
        print(f"[!] No prompt folder found at {prompts_path}")
        return

    count = 0
    for folder in os.listdir(prompts_path):
        full_path = os.path.join(prompts_path, folder)
        if not os.path.isdir(full_path):
            continue

        metadata = load_metadata(full_path)
        if not metadata:
            print(f"[-] Skipping '{folder}': No metadata.json")
            continue

        prompt_text = metadata.get("prompt", "").strip()
        if not prompt_text:
            print(f"[-] Skipping '{folder}': Empty prompt")
            continue

        tags = metadata.get("tags", [])
        prompt_id = db.add_prompt(prompt_text, tags)

        model = metadata.get("model", "unknown").strip()
        response = metadata.get("response", "").strip()

        if response:
            db.add_response(prompt_id, model, response)
            print(f"[+] Imported: '{folder}' as Prompt ID {prompt_id}")
            count += 1
        else:
            print(f"[-] Skipping '{folder}': No response")

    print(f"\n✅ Migration complete: {count} entries imported.")
    db.close()

if __name__ == "__main__":
    migrate_all_entries()
