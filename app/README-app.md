# ai-reply-index-app

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Qt](https://img.shields.io/badge/PyQt5-GUI-green?logo=qt)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **A personal prompt+response indexing tool with multi-model comparison, tagging, and export-ready logging.**

---

## 🧠 What is ai-reply-index?

`ai-reply-index` is a local GUI tool built using PyQt5 to help you **record, organize, and compare AI prompts and responses** across different models (e.g., GPT-4, Claude, etc.). It’s like GitHub for your conversations — local-first, structured, and exportable.

---

## ✨ Features

- ✅ New prompt + response entry form
- ✅ Compare responses from multiple models side-by-side
- ✅ Tag prompts and filter by topic
- ✅ Dark mode & theme toggle
- ✅ Browse, preview, and edit entries
- ✅ Markdown and JSON saving
- ✅ SQLite backend (optional but powerful)

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/yourname/ai-reply-index.git
cd ai-reply-index
```

### 2. Install dependencies
```bash
poetry install
# or
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app/main.py
```

---

## 🖥️ Screenshots

> *(Place screenshots here: Browse Tab, New Entry Tab, Compare Tab, Tag Sidebar)*

---

## 📁 Folder Structure

```bash
prompts/
├── 2025_hello_world_prompt/
│   ├── metadata.json
│   ├── prompt.md
│   └── gpt4.md
```

---

## 🧩 Configuration

Default config is stored in `data/config.json`:
```json
{
  "theme": "dark",
  "save_path": "prompts",
  "use_database": true,
  "database_path": "data/prompt_index.db"
}
```

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## 🙌 Acknowledgements

Built with ❤️ by [@sandy-sp](https://github.com/sandy-sp)
