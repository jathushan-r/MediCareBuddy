import mysql.connector
import json
import datetime
import csv

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

    # columns want to select
    columns = 'sender_id','type_name','timestamp', 'intent_name','data'

    # Query to describe the table and retrieve column information
    query = f"SELECT sender_id,type_name,timestamp, intent_name,data FROM {table_name} WHERE type_name IN ('user', 'bot')"

    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()

    # # Display the column information
    # for row in results:
    #     json_data = json.loads(row[4])
    #     # Access the "text" field
    #     text_value, event = json_data["text"], json_data["event"]
    #     # print(event+': ' + text_value)
    #     dt_object = datetime.datetime.fromtimestamp(row[2])
    #     date = dt_object.date()
    #     time = dt_object.time()
    #     print(row[0], row[1], date,time,row[3],text_value)

    with open('output.csv', 'w', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header row
        csv_writer.writerow(["sender_id", "type_name", "date", "time", "intent_name", "data"])

        for row in results:
            json_data = json.loads(row[4])
            text_value, event = json_data["text"], json_data["event"]
            dt_object = datetime.datetime.fromtimestamp(row[2])
            date = dt_object.date()
            time = dt_object.time()

            # Write the data to the CSV file
            csv_writer.writerow([row[0], row[1], date, time, row[3], text_value])

    print("Data has been written to output.csv")

    # # Close the cursor and connection
    cursor.close()
    conn.close()
else:
    print("Unable to connect to the MySQL server")

