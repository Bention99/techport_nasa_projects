import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "techport.db"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    #conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id      INTEGER PRIMARY KEY,
            last_updated    TEXT NOT NULL,
            favorited       INTEGER NOT NULL,
            detailed_funding INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def upsert_project(project):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO projects (project_id, last_updated, favorited, detailed_funding)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(project_id) DO UPDATE SET
            last_updated = excluded.last_updated,
            favorited = excluded.favorited,
            detailed_funding = excluded.detailed_funding
    """, (
        project["projectId"],
        project["lastUpdated"],
        int(project["favorited"]),
        int(project["detailedFunding"]),
    ))

    conn.commit()
    conn.close()