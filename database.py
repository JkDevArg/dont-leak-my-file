import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='documents.db'):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS documents
                            (uuid TEXT PRIMARY KEY,
                             name TEXT,
                             date TEXT)''')

    def insert_document(self, uuid, name):
        date = datetime.now().isoformat()
        self.conn.execute("INSERT INTO documents VALUES (?, ?, ?)",
                         (uuid, name, date))
        self.conn.commit()

    def check_leak(self, uuid):
        cursor = self.conn.execute("SELECT * FROM documents WHERE uuid=?", (uuid,))
        return cursor.fetchone() is not None