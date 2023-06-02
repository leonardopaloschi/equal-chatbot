import sqlite3

def get_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    # Retrieve data from the table
    table_name = 'your_table'
    cursor.execute(f"SELECT * FROM webpages;")
    data = cursor.fetchall()

    # Specify the output text file
    output_file = 'output.txt'

    texts = []

    # Write the data to the text file
    with open(output_file, 'w') as file:
        for row in data:
            texts.append(row[2])

    # Close the database connection
    conn.close()

    print(f"The contents of the '{table_name}' table have been written to '{output_file}'.")

    return texts