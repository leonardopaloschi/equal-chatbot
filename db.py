"""
This module initializes a SQLite database with two tables: 'webpages' and 'visited'.

The 'webpages' table stores webpage information including URL, content, and sentiment score.
The 'visited' table keeps track of URLs that have been processed.

The database file is named 'database.sqlite'.
"""

import sqlite3

with sqlite3.connect('database.sqlite') as conn:
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS webpages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            url TEXT, 
            content TEXT, 
            sentiment REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visited (
            url TEXT PRIMARY KEY
        )
    ''')

    conn.commit()
    