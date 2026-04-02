import sqlite3

# ─────────────────────────────────
# CONNECTION
# ─────────────────────────────────

def create_connection():
    conn = sqlite3.connect("myapp.db")
    return conn


# ─────────────────────────────────
# CREATE TABLE
# ─────────────────────────────────

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name        TEXT    NOT NULL,
            deadline         TEXT    NOT NULL,
            difficulty_rating INTEGER DEFAULT 5,
            is_done          INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# ─────────────────────────────────
# SAVE DATA
# ─────────────────────────────────

def add_task(task_name, deadline, difficulty_rating=5):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (task_name, deadline, difficulty_rating)
        VALUES (?, ?, ?)
    """, (task_name, deadline, difficulty_rating))

    conn.commit()
    conn.close()


# ─────────────────────────────────
# READ DATA
# ─────────────────────────────────

def get_all_tasks():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tasks ORDER BY deadline ASC
    """)
    tasks = cursor.fetchall()

    conn.close()
    return tasks


# ─────────────────────────────────
# UPDATE DATA
# ─────────────────────────────────

def mark_task_done(task_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks SET is_done = 1 WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# ─────────────────────────────────
# PROGRESS
# ─────────────────────────────────

def get_progress():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE is_done = 1")
    done = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0
    return int((done / total) * 100)


# ─────────────────────────────────
# RUN WHEN APP STARTS
# ─────────────────────────────────

create_tables()
