import pandas as pd
import sqlite3
import os
import logging

log = logging.getLogger(__name__)


def init_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            query             TEXT,
            title             TEXT,
            author            TEXT,
            first_publish_year INTEGER,
            isbn              TEXT,
            language          TEXT,
            subject           TEXT,
            edition_count     INTEGER,
            fetched_at        TEXT,
            PRIMARY KEY (title, query)
