#!/usr/bin/env python3
"""Insert example rows into labels.db if the table is still sparse."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "labels.db")

braille_patterns = {
    "a": [1, 0, 0, 0, 0, 0],
    "b": [1, 1, 0, 0, 0, 0],
    "c": [1, 0, 0, 1, 0, 0],
    "d": [1, 0, 0, 1, 1, 0],
    "e": [1, 0, 0, 0, 1, 0],
    "f": [1, 1, 0, 1, 0, 0],
    "g": [1, 1, 0, 1, 1, 0],
    "h": [1, 1, 0, 0, 1, 0],
    "i": [0, 1, 0, 1, 0, 0],
    "j": [0, 1, 0, 1, 1, 0],
    "k": [1, 0, 1, 0, 0, 0],
    "l": [1, 1, 1, 0, 0, 0],
    "m": [1, 0, 1, 1, 0, 0],
    "n": [1, 0, 1, 1, 1, 0],
    "o": [1, 0, 1, 0, 1, 0],
    "p": [1, 1, 1, 1, 0, 0],
    "q": [1, 1, 1, 1, 1, 0],
    "r": [1, 1, 1, 0, 1, 0],
    "s": [0, 1, 1, 1, 0, 0],
    "t": [0, 1, 1, 1, 1, 0],
    "u": [1, 0, 1, 0, 0, 1],
    "v": [1, 1, 1, 0, 0, 1],
    "w": [0, 1, 0, 1, 1, 1],
    "x": [1, 0, 1, 1, 0, 1],
    "y": [1, 0, 1, 1, 1, 1],
    "z": [1, 0, 1, 0, 1, 1],
    " ": [0, 0, 0, 0, 0, 0],
}


def encode_to_braille(text: str):
    unicode_braille = ""
    braille_dots = ""
    for char in text.lower():
        if char not in braille_patterns:
            continue
        bits = braille_patterns[char]
        dot_nums = [i + 1 for i, b in enumerate(bits) if b]
        val = sum(1 << (i - 1) for i in dot_nums)
        unicode_braille += chr(0x2800 + val)
        dots = "-".join(str(i + 1) for i, b in enumerate(bits) if b)
        if braille_dots:
            braille_dots += " "
        braille_dots += dots
    return unicode_braille, braille_dots


EXAMPLES = [
    ("hello", "voice", "2026-04-08 10:20:00"),
    ("coffee mug", "image", "2026-04-08 16:45:00"),
    ("welcome home", "voice", "2026-04-10 09:00:00"),
    ("exit sign", "image", "2026-04-10 11:30:00"),
    ("thank you", "voice", "2026-04-12 08:15:00"),
    ("office door", "image", "2026-04-14 13:00:00"),
    ("library", "voice", "2026-04-15 17:20:00"),
    ("kitchen", "image", "2026-04-16 12:00:00"),
    ("first aid", "voice", "2026-04-17 09:45:00"),
    ("restroom", "image", "2026-04-18 14:10:00"),
]


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS labels
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              english TEXT NOT NULL,
              braille TEXT NOT NULL,
              braille_dots TEXT NOT NULL,
              mode TEXT NOT NULL,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"""
    )
    c.execute("SELECT COUNT(*) FROM labels")
    count = c.fetchone()[0]
    if count >= 8:
        print(f"labels.db already has {count} row(s); skip seeding (delete rows to reseed).")
        conn.close()
        return

    for english, mode, ts in EXAMPLES:
        braille, dots = encode_to_braille(english)
        c.execute(
            "INSERT INTO labels (english, braille, braille_dots, mode, timestamp) VALUES (?, ?, ?, ?, ?)",
            (english, braille, dots, mode, ts),
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(EXAMPLES)} example label(s) into {DB_PATH}")


if __name__ == "__main__":
    main()
