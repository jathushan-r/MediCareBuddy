import mysql.connector
import json

# Replace these with your MySQL server and database information
host = "localhost"
user = "root"
password = "abcd1234"
database = "rasachats"

# Connect to the MySQL database
conn = mysql.connector.connect(host=host, user=user, password=password, database=database)

if conn.is_connected():
    print("connected")
    cursor = conn.cursor()

    # Replace 'your_table_name' with the name of the table you want to query
    table_name = 'events'

    # Query to describe the table and retrieve column information
    query = f"SELECT data FROM {table_name} WHERE type_name IN ('user', 'bot')"

    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()

    # Display the column information
    for row in results:
        json_data = json.loads(row[0])
        # Access the "text" field
        text_value, event = json_data["text"], json_data["event"]
        print(event+': ' + text_value)

    # Close the cursor and connection
    cursor.close()
    conn.close()
else:
    print("Unable to connect to the MySQL server")

