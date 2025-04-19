import os
import json
from pathlib import Path
from app.db.db_manager import DBManager

EXPORT_DIR = Path("dist")
PROMPTS_DIR = EXPORT_DIR / "prompts"
DATA_DIR = EXPORT_DIR / "data"
TEMPLATE_DIR = Path("scripts/templates")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ font-family: sans-serif; background: #f8f8f8; padding: 2rem; }}
    h1 {{ color: #333; }}
    .model {{ margin-top: 2rem; padding: 1rem; background: #fff; border: 1px solid #ddd; }}
  </style>
</head>
<body>
  <h1>{prompt}</h1>
  {responses}
  <p><a href="../index.html">← Back to index</a></p>
</body>
</html>
"""

RESPONSE_BLOCK = """
<div class="model">
  <h2>{model}</h2>
  <pre>{content}</pre>
  <small><i>{timestamp}</i></small>
</div>
"""

INDEX_HTML_HEADER = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Reply Index</title>
  <style>
    body {{ font-family: sans-serif; padding: 2rem; }}
    ul {{ list-style: none; }}
  </style>
</head>
<body>
  <h1>AI Reply Index</h1>
  <ul>
"""
INDEX_HTML_FOOTER = """
  </ul>
</body>
</html>
"""


def export():
    db = DBManager()
    EXPORT_DIR.mkdir(exist_ok=True)
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    prompts = db.fetch_prompts()
    index_lines = []
    export_data = []

    for i, prompt in enumerate(prompts):
        prompt_id = prompt["id"]
        prompt_text = prompt["text"]
        slug = f"{i:03d}_" + "_".join(prompt_text[:40].lower().split())
        folder = PROMPTS_DIR / slug
        folder.mkdir(exist_ok=True)

        # Get model responses
        responses = db.get_model_responses(prompt_id)
        html_responses = "\n".join([
            RESPONSE_BLOCK.format(
                model=r["model"],
                content=r["content"],
                timestamp=r["created_at"]
            ) for r in responses
        ])

        # Save HTML page
        html = HTML_TEMPLATE.format(title=prompt_text, prompt=prompt_text, responses=html_responses)
        with open(folder / "index.html", "w", encoding="utf-8") as f:
            f.write(html)

        # Save raw data
        prompt_dict = {
            "id": prompt_id,
            "text": prompt_text,
            "created_at": prompt["created_at"],
            "tags": db.get_tags_for_prompt(prompt_id),
            "responses": [dict(r) for r in responses]
        }
        with open(folder / "data.json", "w", encoding="utf-8") as f:
            json.dump(prompt_dict, f, indent=2)
        export_data.append(prompt_dict)

        index_lines.append(f"<li><a href=\"prompts/{slug}/index.html\">{prompt_text}</a></li>")

    # Write index.html
    with open(EXPORT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(INDEX_HTML_HEADER + "\n".join(index_lines) + INDEX_HTML_FOOTER)

    # Write global JSON
    with open(DATA_DIR / "all_prompts.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)

    print(f"✅ Export complete: {len(prompts)} prompts written to {EXPORT_DIR}/")


if __name__ == "__main__":
    export()
