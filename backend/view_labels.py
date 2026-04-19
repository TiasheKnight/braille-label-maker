#!/usr/bin/env python3
import sqlite3

def view_labels():
    conn = sqlite3.connect('labels.db')
    c = conn.cursor()
    c.execute("SELECT id, english, braille, braille_dots, mode, timestamp FROM labels ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    print("Labels Database Contents:")
    print("=" * 80)
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"English: {row[1]}")
        print(f"Braille: {row[2]}")
        print(f"Braille Dots: {row[3]}")
        print(f"Mode: {row[4]}")
        print(f"Timestamp: {row[5]}")
        print("-" * 40)

if __name__ == "__main__":
    view_labels()