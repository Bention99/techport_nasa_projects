import sqlite3
import logging
from pathlib import Path
from log_handling import write_info_log
from api_request_details import call_api_project_details
from progress_bar import print_progress_bar

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
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'projects'
    """)

    table_exists = cur.fetchone() is not None

    if table_exists:
        write_info_log("Table 'projects' already exists. Skipping creation.")
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id      INTEGER PRIMARY KEY,
                last_updated    TEXT NOT NULL,
                favorited       INTEGER NOT NULL,
                detailed_funding INTEGER NOT NULL,
                title           TEXT,
                destinationType TEXT
            )
        """)
        conn.commit()
        write_info_log("Table 'projects' created.")

    conn.close()

def upsert_project(cur, project, project_details):
    project_id = project["projectId"]
    dest_type = ", ".join(project_details.get("destinationType") or [])

    cur.execute("SELECT 1 FROM projects WHERE project_id = ?", (project_id,)) 
    exists = cur.fetchone() is not None

    cur.execute("""
        INSERT INTO projects (project_id, last_updated, favorited, detailed_funding, title, destinationType)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(project_id) DO UPDATE SET
            last_updated = excluded.last_updated,
            favorited = excluded.favorited,
            detailed_funding = excluded.detailed_funding,
            title            = excluded.title,
            destinationType  = excluded.destinationType
    """, (
        project["projectId"],
        project["lastUpdated"],
        int(project["favorited"]),
        int(project["detailedFunding"]),
        project_details["title"],
        dest_type,
    ))

    if exists: 
        write_info_log(f"Project {project_id} -> UPDATED in 'projects'") 
    else: 
        write_info_log(f"Project {project_id} -> INSERTED into 'projects'")

def insert_into_db(data):

    projects = data.get("projects", [])
    total = len(projects)

    conn = get_connection()
    cur = conn.cursor()

    inserted = 0
    updated = 0

    print_progress_bar(0, total, prefix='Progress:', suffix='Complete', length=50)

    for i, project in enumerate(projects, start=1):
        project_details = call_api_project_details(project["projectId"])

        cur.execute("SELECT 1 FROM projects WHERE project_id = ?", (project["projectId"],))
        exists = cur.fetchone() is not None

        upsert_project(cur, project, project_details)

        if exists:
            updated += 1
        else:
            inserted += 1

        print_progress_bar(i, total, prefix='Progress:', suffix='Complete', length=50)

    conn.commit()
    conn.close()

    write_info_log(f"Upsert finished: {inserted} inserted, {updated} updated.")
