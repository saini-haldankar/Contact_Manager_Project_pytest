import sqlite3


def get_connection(db_name="contacts.db"):
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_name="contacts.db"):
    connection = get_connection(db_name)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        )
    """)

    connection.commit()
    connection.close()
