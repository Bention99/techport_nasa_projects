import sqlite3
import logging
from pathlib import Path
from log_handling import write_info_log
from api_request_details import call_api_project_details
from progress_bar import print_progress_bar
from user_input import projects_amount

DB_PATH = Path(__file__).parent / "data" / "techport.db"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
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
                destinationType TEXT,
                start_date      TEXT,
                end_date        TEXT,
                start_year      INTEGER,
                end_year        INTEGER,
                status          TEXT,
                release_status  TEXT,
                view_count      INTEGER,
                description     TEXT
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
        INSERT INTO projects (
            project_id,
            last_updated,
            favorited,
            detailed_funding,
            title,
            destinationType,
            start_date,
            end_date,
            start_year,
            end_year,
            status,
            release_status,
            view_count,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(project_id) DO UPDATE SET
            last_updated     = excluded.last_updated,
            favorited        = excluded.favorited,
            detailed_funding = excluded.detailed_funding,
            title            = excluded.title,
            destinationType  = excluded.destinationType,
            start_date       = excluded.start_date,
            end_date         = excluded.end_date,
            start_year       = excluded.start_year,
            end_year         = excluded.end_year,
            status           = excluded.status,
            release_status   = excluded.release_status,
            view_count       = excluded.view_count,
            description      = excluded.description
    """, (
        project["projectId"],
        project["lastUpdated"],
        int(project["favorited"]),
        int(project["detailedFunding"]),
        project_details["title"],
        dest_type,
        project_details.get("startDate"),
        project_details.get("endDate"),
        project_details.get("startYear"),
        project_details.get("endYear"),
        project_details.get("status"),
        project_details.get("releaseStatus"),
        project_details.get("viewCount"),
        project_details.get("description"),
    ))

    if exists: 
        write_info_log(f"Project {project_id} -> UPDATED in 'projects'") 
    else: 
        write_info_log(f"Project {project_id} -> INSERTED into 'projects'")

def insert_into_db(data):

    projects = data.get("projects", [])
    total = len(projects)

    projects_sorted = sorted(
    projects,
    key=lambda p: p["lastUpdated"],
    reverse=True
    )

    amount = projects_amount(total)
    cutted_projects = projects_sorted[:amount]

    conn = get_connection()
    cur = conn.cursor()

    inserted = 0
    updated = 0

    print_progress_bar(0, amount, prefix='Progress:', suffix='Complete', length=50)

    for i, project in enumerate(cutted_projects, start=1):
        project_details = call_api_project_details(project["projectId"])

        cur.execute("SELECT 1 FROM projects WHERE project_id = ?", (project["projectId"],))
        exists = cur.fetchone() is not None

        upsert_project(cur, project, project_details)

        if exists:
            updated += 1
        else:
            inserted += 1

        print_progress_bar(i, amount, prefix='Progress:', suffix='Complete', length=50)

    conn.commit()
    conn.close()

    write_info_log(f"Upsert finished: {inserted} inserted, {updated} updated.")
