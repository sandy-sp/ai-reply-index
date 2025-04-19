# 🧠 AI Reply Index

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)](https://riverbankcomputing.com/software/pyqt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](./LICENSE)

**AI Reply Index** is a local-first desktop app that helps you **log, organize, and compare AI prompts and responses** across different models. Whether you're testing GPT-4 vs Claude or benchmarking multiple models for the same prompt, this tool makes it effortless — and GitHub-style clean.

---

## 🚀 Purpose

This tool was born from a simple but powerful idea:

> “What if we could store our prompts like code commits — with their responses, models, and metadata — and compare them neatly, locally, and version-style?”

That’s exactly what **AI Reply Index** does:
- Record prompts and their responses
- Track which model gave which answer
- Organize them in clean folder structures or a database
- Compare them side-by-side
- Export as Markdown, JSON, or full HTML site

---

## ✨ Features

- 📝 Add new prompt + model response
- 📂 Organize by folders, tags, and metadata
- 🧠 Compare responses from multiple models
- 🎨 Dark mode & theming
- 🔍 Keyword, tag, and model-based search
- 🗃️ SQLite-powered filtering (optional)
- 📦 Static HTML export (`dist/index.html`)
- ✅ Works offline, no cloud dependency

---

## 🖼 Example

Prompt folder structure:

```
prompts/
└── 2025_hello_world_prompt/
    ├── metadata.json
    ├── prompt.md
    └── gpt4.md
```

Sample metadata:

```json
{
  "prompt": "Explain recursion to a 10-year-old.",
  "model": "gpt-4",
  "response": "Imagine looking into a mirror...",
  "tags": ["explanation", "beginner", "recursion"],
  "date": "2025-04-17"
}
```

Multiple models? No problem:

```
2025_hello_world_prompt/
├── prompt.md
├── gpt4.md
├── claude.md
├── llama3.md
```

---

## 📦 Installation

```bash
git clone https://github.com/sandy-sp/ai-reply-index.git
cd ai-reply-index

# With poetry
poetry install

# Or with pip
pip install -r requirements.txt
```

---

## ▶️ How to Use

```bash
python app/main.py
```

- Use the **New Entry** tab to add a prompt + response
- Use the **Browse/Edit** tab to:
  - Filter entries by model, tag, or keyword
  - Compare responses visually
  - Edit or delete entries

---

## 🌐 Static Site Export

Generate a full HTML archive of all your prompts + responses:

```bash
python scripts/export_static_site.py
```

Output is written to the `dist/` directory with:
- `index.html` for navigation
- One folder per prompt with HTML and JSON

---

## ⚙️ Config

Stored in `data/config.json`:

```json
{
  "theme": "dark",
  "save_path": "prompts",
  "use_database": true,
  "database_path": "data/prompt_index.db"
}
```

---

## 🛠 Tech Stack

- [Python 3.12](https://www.python.org/)
- [PyQt5](https://riverbankcomputing.com/software/pyqt/)
- [SQLite](https://sqlite.org/)
- [Markdown2](https://github.com/trentm/python-markdown2)

---

## 📄 License

MIT © [@sandy-sp](https://github.com/sandy-sp) — free to use, modify, and distribute.

---

## 🙌 Acknowledgements

Built with ❤️ to make AI prompt testing and logging more structured, efficient, and beautiful.

```

---
