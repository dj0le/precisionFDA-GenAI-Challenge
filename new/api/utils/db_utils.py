import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime

DB_NAME = "document_metadata.db"

@contextmanager
def get_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        if conn:
            conn.close()


def create_document_store():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS document_store
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     filename TEXT,
                     file_hash TEXT UNIQUE,
                     upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

def insert_document_record(filename: str, file_hash: str):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO document_store (filename, file_hash) VALUES (?, ?)',
                         (filename, file_hash))
            file_id = cursor.lastrowid
            conn.commit()
            return file_id
        except sqlite3.IntegrityError:
            cursor.execute('SELECT id FROM document_store WHERE file_hash = ?', (file_hash,))
            existing_id = cursor.fetchone()
            raise ValueError(f"File already exists with ID: {existing_id[0]}")

def delete_document_record(file_id):
    with get_db() as conn:
        conn.execute('DELETE FROM document_store WHERE id = ?', (file_id,))
        conn.commit()
        return True

def get_all_documents():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id as file_id, filename, file_hash, upload_timestamp
            FROM document_store
            ORDER BY upload_timestamp DESC
        ''')
        return [dict(doc) for doc in cursor.fetchall()]

# completely reset all db data
def nuke_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
# if reset:
# nuke_db()

# Initialize the database tables
create_document_store()
