import os
import json
import markdown2
from app.db.db_manager import DBManager
from datetime import datetime

class ExportService:
    def __init__(self, db_path="data/prompt_index.db"):
        self.db = DBManager(db_path)

    def export_markdown(self, prompt_id, output_folder):
        prompt = self.db.get_prompt_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with ID {prompt_id} not found.")

        text = prompt["text"]
        date = prompt["created_at"].split("T")[0]
        slug = "_".join(text[:40].lower().split())
        folder_name = f"{date}_{slug}"
        export_path = os.path.join(output_folder, folder_name)
        os.makedirs(export_path, exist_ok=True)

        # Export prompt
        with open(os.path.join(export_path, "prompt.md"), 'w', encoding='utf-8') as f:
            f.write(f"# Prompt\n\n{text}\n")

        # Export responses
        responses = self.db.get_model_responses(prompt_id)
        for r in responses:
            model_slug = r["model"].replace("/", "_")
            filename = os.path.join(export_path, f"{model_slug}.md")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Response from {r['model']}\n\n{r['content']}\n")

        # Export metadata
        metadata = {
            "prompt": text,
            "tags": [tag["name"] for tag in self.db.get_tags_for_prompt(prompt_id)],
            "date": date,
            "responses": [dict(r) for r in responses],
            "created_at": prompt["created_at"]
        }
        with open(os.path.join(export_path, "metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        return export_path

    def export_html_site(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        prompts = self.db.search_prompts()

        index_entries = []
        for prompt in prompts:
            folder = self.export_markdown(prompt["id"], output_dir)
            index_entries.append(f"<li><a href='{os.path.basename(folder)}/index.html'>{prompt['text'][:60]}</a></li>")

            # Generate HTML for each folder
            md_path = os.path.join(folder, "prompt.md")
            html_body = ""
            if os.path.exists(md_path):
                with open(md_path, 'r', encoding='utf-8') as f:
                    html_body += markdown2.markdown(f.read())
            for file in os.listdir(folder):
                if file.endswith(".md") and file != "prompt.md":
                    with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
                        html_body += markdown2.markdown(f.read())

            html = f"""
            <!DOCTYPE html>
            <html lang='en'>
            <head><meta charset='UTF-8'><title>{prompt['text'][:30]}</title></head>
            <body>{html_body}</body>
            </html>
            """
            with open(os.path.join(folder, "index.html"), 'w', encoding='utf-8') as f:
                f.write(html)

        # Generate root index.html
        index_html = f"""
        <!DOCTYPE html>
        <html lang='en'>
        <head><meta charset='UTF-8'><title>Prompt Index</title></head>
        <body>
        <h1>All Prompts</h1>
        <ul>{''.join(index_entries)}</ul>
        </body>
        </html>
        """
        with open(os.path.join(output_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(index_html)

        print(f"✅ Exported static site to {output_dir}")
