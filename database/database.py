import mysql.connector

# Establish a MySQL database connection
def create_mysql_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sql677",
        database="hospitaldb"
    )
    return connection

def insert_user(username, firstname,lastname,age,phone, password):
    try:
        connection = create_mysql_connection()
        cursor = connection.cursor()

        # Insert user data into the user table
        query = "INSERT INTO user (username, firstname,lastname,age,phone, password) VALUES (%s, %s, %s,%s, %s,%s)"
        values = (username, firstname,lastname,age,phone, password)
        cursor.execute(query, values)

        # Commit the changes to the database
        connection.commit()

    except mysql.connector.Error as error:
        # Handle any errors here
        print("Error: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_all_users():
    try:
        connection = create_mysql_connection()
        cursor = connection.cursor()

        # Fetch all users from the user table
        query = "SELECT * FROM user"
        cursor.execute(query)

        # Fetch all rows as a list of dictionaries
        users = []
        for row in cursor.fetchall():
            user = {
                "username": row[0],
                "firstname": row[1],
                "lastname": row[2],
                "age": row[3],
                "phone": row[4],
                "password": row[5]
            }
            users.append(user)

        return users

    except mysql.connector.Error as error:
        # Handle any errors here
        print("Error: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_user(username):
    try:
        connection = create_mysql_connection()
        cursor = connection.cursor()

        # Retrieve a user by username from the user table
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (username,))

        # Fetch the user as a dictionary
        user = {}
        for row in cursor.fetchall():
            user = {
                "username": row[0],
                "firstname": row[1],
                "lastname": row[2],
                "age": row[3],
                "phone": row[4],
                "password": row[5]
            }
            break  # Assuming username is unique

        return user

    except mysql.connector.Error as error:
        # Handle any errors here
        print("Error: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_user(username, updates):
    try:
        connection = create_mysql_connection()
        cursor = connection.cursor()

        # Update user data in the user table
        query = "UPDATE user SET name = %s, password = %s WHERE username = %s"
        values = (updates["name"], updates["password"], username)
        cursor.execute(query, values)

        # Commit the changes to the database
        connection.commit()

    except mysql.connector.Error as error:
        # Handle any errors here
        print("Error: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_user(username):
    try:
        connection = create_mysql_connection()
        cursor = connection.cursor()

        # Delete a user by username from the user table
        query = "DELETE FROM user WHERE username = %s"
        cursor.execute(query, (username,))

        # Commit the changes to the database
        connection.commit()

    except mysql.connector.Error as error:
        # Handle any errors here
        print("Error: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
