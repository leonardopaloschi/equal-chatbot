import sqlite3

# Establish a connection to the database
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

# Variables for testing purposes
url = "https://example.com"
content = "Sample content"

try:
    # Verify the values before executing the query
    print("URL:", url)
    print("Content:", content)

    # Execute the INSERT statement
    cursor.execute("INSERT INTO webpages (url, content) VALUES (?, ?);", (url, content))

    # Commit the changes to the database
    conn.commit()
    print("Insertion successful!")
except Exception as e:
    print("Error:", e)

# Close the cursor and connection
cursor.close()
conn.close()