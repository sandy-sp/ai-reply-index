-- schema.sql

CREATE TABLE IF NOT EXISTS Prompt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Model (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Response (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,
    model_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_html TEXT,
    content_plaintext TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (prompt_id) REFERENCES Prompt(id),
    FOREIGN KEY (model_id) REFERENCES Model(id)
);

-- Normalized Tags Table
CREATE TABLE IF NOT EXISTS Tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS PromptTag (
    prompt_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (prompt_id, tag_id),
    FOREIGN KEY (prompt_id) REFERENCES Prompt(id),
    FOREIGN KEY (tag_id) REFERENCES Tag(id)
);
