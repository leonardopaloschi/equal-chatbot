import sqlite3

with sqlite3.connect('database.sqlite') as conn:
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS webpages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, url text, content text, sentiment real)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS visited
                     (url text PRIMARY KEY)''')

    conn.commit()