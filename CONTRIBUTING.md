# 🤝 Contributing to AI Reply Index

Thank you for your interest in contributing to **AI Reply Index**! This project is a hybrid of a desktop app and an open repository for collecting well-formatted AI prompts and responses from a wide range of models. All contributions help grow a reliable benchmark archive for the AI community.

---

## 🧰 Use the App for Contributions

We require that contributors **use the AI Reply Index app** to ensure a consistent format for all entries. The app:
- Generates folder structures automatically
- Formats Markdown using `mdformat`
- Tags models and metadata properly
- Supports drag-and-drop for DOCX input
- Supports multiple response versions per prompt

Install the app using [these instructions](./app/README.md) before proceeding.

---

## 📌 Contribution Checklist

Here’s how to add your prompt + responses to the index:

1. **Fork the repository**
2. **Clone it locally**

   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-reply-index.git
   cd ai-reply-index
   ```

3. **Install the app**
   - With Poetry:
     ```bash
     poetry install
     ```

4. **Run the app**
   ```bash
   python app/main.py
   ```

5. **Use the "New Entry" tab** to input:
   - The prompt
   - The model name
   - The AI response
   - Optional tags
   - Choose to save as Markdown + JSON

6. **Verify folder output** under `prompts/`
   Each entry folder should include:
   ```bash
   prompts/YYYY-MM-DD_slug/
   ├── prompt.md
   ├── MODEL_NAME.md
   └── metadata.json
   ```

7. **Commit your prompt folder**
   ```bash
   git checkout -b add-my-prompt
   git add prompts/2025-04-19_my_test_prompt/
   git commit -m "Add: AI response to my_test_prompt using Claude"
   git push origin add-my-prompt
   ```

8. **Submit a Pull Request**
   - Title your PR clearly
   - Mention the models used and what the prompt tests

---

## 🧪 Tips for High-Quality Entries

✅ Use meaningful prompt slugs  
✅ Add clear tags (e.g., `reasoning`, `ethics`, `summarization`)  
✅ Test multiple models on the same prompt  
✅ Prefer Markdown-friendly input  
✅ Avoid long preambles in model replies (trim where needed)

---

## 📦 Static Site Export (Optional)

If you'd like to preview your contribution as an HTML archive:

```bash
python scripts/export_static_site.py
```

HTML will be generated to `dist/index.html` for easy sharing.

---

## 📄 License

All contributions are licensed under the [MIT License](./LICENSE). By submitting a pull request, you agree that your contributions will be included under this license.

---

Let’s build a transparent, open-source AI prompt archive — one entry at a time. Thank you! 🙏

