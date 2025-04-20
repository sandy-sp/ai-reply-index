# 🧠 AI Reply Index

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](./LICENSE)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)](https://riverbankcomputing.com/software/pyqt/)
[![Markdown](https://img.shields.io/badge/Format-Markdown-blue?logo=markdown)](https://daringfireball.net/projects/markdown/)

---

## ✨ What is AI Reply Index?

**AI Reply Index** is a local-first desktop application and GitHub-based open repository designed to help you log, organize, and share **AI prompts and their responses**. Whether you're experimenting with ChatGPT, Claude, Gemini, or open-source LLMs — this tool enables you to preserve and compare the outputs in a neat, versioned format.

Inspired by the idea:
> "What if we could log AI prompts like code commits — with full versioning, metadata, and model comparisons?"

This repo is both:
- 🛠 A **tool** (the PyQt5 app) to help format and log your prompt-response data
- 📚 A **repository** where the global community can contribute and explore prompt use-cases

---

## 🗂 Repository Structure

```bash
ai-reply-index/
├── app/                # PyQt5 GUI app to create and manage prompt entries
├── prompts/            # Saved entries in folder-based Markdown format
├── data/               # App configuration, model registry, database
├── scripts/            # Utility scripts (export, migration, etc.)
├── README.md           # ← You are here
├── app/README.md       # App-specific documentation
└── CONTRIBUTING.md     # Contribution guidelines
```

Each entry is stored like this:

```
prompts/
└── 2025-04-19_example_prompt/
    ├── prompt.md
    ├── Gemini.md
    └── metadata.json
```

---

## 🧩 Why Use the App?

To contribute to this repository, we ask that you **use the official AI Reply Index desktop app**. It ensures:
- ✅ Consistent formatting (Markdown, metadata, JSON)
- 📄 Proper folder naming conventions
- 🧠 Automatic model tagging and filtering
- 🖼 Support for DOCX + formatting

This reduces friction for reviewers and improves the overall quality of the shared prompts.

---

## 🛠️ How to Contribute

1. **Fork this repository**
2. **Install the app** following [app/README.md](./app/README.md)
3. **Create entries using the app**
4. **Verify folder contents** (prompt.md, response, metadata.json)
5. **Submit a pull request** with your prompt folder under `/prompts/`

See: [CONTRIBUTING.md](./CONTRIBUTING.md) for the full contribution checklist.

---

## 📖 Example Use-Cases

- 🧪 Test the same prompt on GPT-4, Claude, Gemini, etc.
- 🏷️ Organize responses with searchable tags and metadata
- 📊 Compare model behavior across domains
- 📦 Export a static HTML archive of your prompt logs

---

## 📄 License

MIT © [@sandy-sp](https://github.com/sandy-sp) — open for anyone to use, modify, and contribute.

---

## 💬 Join the Prompt Archive Revolution

Help us build the world's cleanest, most collaborative AI prompt + response index.
Contribute your experiments, your insights, your edge cases — and let's learn from each other.

> _"Prompts are the new code — it's time we treat them that way."_

