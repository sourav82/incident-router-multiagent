import sqlite3
from typing import List, Dict
import os
import logging

#DB_PATH = "./vectordb/kb.sqlite3"
DB_PATH = os.path.join(os.getcwd(), "vectordb", "kb.sqlite3")

def fetch_kb_articles() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM kb_articles")
    rows = cursor.fetchall()

    logging.info(f"Number of KB rows fetched: {len(rows)}")

    conn.close()

    return [dict(row) for row in rows]