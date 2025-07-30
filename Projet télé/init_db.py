import sqlite3

conn = sqlite3.connect('teles.db')
cur = conn.cursor()

def creer_table_si_absente(self):
    self.conn.execute("""
        CREATE TABLE IF NOT EXISTS teles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE,
            etat TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            etage TEXT DEFAULT 'RDC',
            salle TEXT
        )
    """)
    self.conn.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_tele TEXT,
            date TEXT,
            action TEXT,
            FOREIGN KEY(nom_tele) REFERENCES teles(nom)
        )
    """)
    self.conn.commit()
conn.commit()
conn.close()