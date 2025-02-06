import os
import sqlite3
from contextlib import contextmanager

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

""" This section is for creating and maintaining the database that stores document metadata. This metadata is useful for general information about what is available in the rag system, to check if a document already exists in the rag database, and for easily deleting documents from the vector db if no longer needed. This is not the rag vector db"""

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


"""This section is for the chat implementation, and creates a database that tracks relevant data such as the session id, and chat history, so that the llm can use it in context and maintain an ongoing conversation with the user"""

def create_chat_history_store():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS chat_history_store
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     session_id TEXT,
                     user_query TEXT,
                     llm_response TEXT,
                     sources TEXT,
                     processing_time INT,
                     tokens INT,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')


def insert_chat_history(session_id, user_query, llm_response, sources, processing_time, tokens):
    with get_db() as conn:
        conn.execute('INSERT INTO chat_history_store (session_id, user_query, llm_response, sources, processing_time, tokens) VALUES (?, ?, ?, ?, ?, ?)',
            (session_id, user_query, llm_response, sources, processing_time, tokens))
        conn.commit()


def get_chat_history(session_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_query, llm_response FROM chat_history_store WHERE session_id = ? ORDER BY created_at', (session_id,))
        messages = []
        for row in cursor.fetchall():
            messages.extend([
            {"role": "human", "content": row['user_query']},
            {"role": "ai", "content": row['llm_response']}
            ])
        return messages


""" testing utility to delete all database data if needed"""
def nuke_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
# if reset:
# nuke_db()

# Initialize the database tables
create_document_store()
create_chat_history_store()
