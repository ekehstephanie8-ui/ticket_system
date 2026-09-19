import sqlite3

def init_db():
    connection = sqlite3.connect("tickets.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            date_created TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")