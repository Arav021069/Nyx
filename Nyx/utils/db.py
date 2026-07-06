import sqlite3

conn = sqlite3.connect("Nyx.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


def save_message(
        session_id,
        role: str,
        content: str
):

    cursor.execute(
        """
        INSERT INTO messages (
            session_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (session_id, role, content)
    )

    conn.commit()


def load_messages(session_id):

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE session_id = ?
        ORDER BY id
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    messages = []

    for role, content in rows:

        messages.append({
            "role": role,
            "content": content
        })

    return messages
