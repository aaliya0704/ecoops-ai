from datetime import datetime
import sqlite3

DB_FILE = "ecoops_audit.db"


def init_db():
    """Creates a local SQLite file and sets up a clean data table

    to permanently log every software task our AI manages.
    """
    # FIX: Implemented context manager 'with' pattern for auto-closing channels safely
    with sqlite3.connect(DB_FILE, check_same_thread=False) as conn:
        cursor = conn.cursor()

        # Define our data columns using standard SQL commands
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                engineering_team TEXT NOT NULL,
                ai_classification TEXT NOT NULL,
                scheduled_hour INTEGER NOT NULL,
                carbon_saved_pct REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        # Connections using context managers automatically commit updates
    print("📁 Database System: Audit logs table initialized successfully.")


def log_task(task_name: str, team: str, classification: str, hour: int, savings: float):
    """Inserts a newly processed task snapshot record straight into our permanent local file."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # FIX: Enforced clean context manager pattern with multi-thread configurations enabled
    with sqlite3.connect(DB_FILE, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO task_logs (task_name, engineering_team, ai_classification, scheduled_hour, carbon_saved_pct, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (task_name, team, classification, hour, savings, current_time),
        )


def get_all_logs():
    """Fetches every single historic record stored inside our database table."""
    # FIX: Enforced clean context manager pattern with multi-thread configurations enabled
    with sqlite3.connect(DB_FILE, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT task_name, engineering_team, ai_classification, scheduled_hour, carbon_saved_pct, timestamp FROM task_logs ORDER BY id DESC"
        )
        rows = cursor.fetchall()
        return rows


# Automatically run the initializer once when this file is referenced
init_db()
