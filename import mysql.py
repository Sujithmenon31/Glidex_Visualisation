import mysql.connector

# Database credentials
host = '127.0.0.1'
user = 'root'
password = ''
database = 'glidex'
try:
    # Establish the connection
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    if connection.is_connected():
        print(f"Successfully connected to the database '{database}'")

        # Create a cursor object
        cursor = connection.cursor()

        # Execute a query to retrieve all table names
        cursor.execute("SHOW TABLES")

        # Fetch all table names
        tables = cursor.fetchall()

        # Print the tables
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        else:
            print("No tables found in the database.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the cursor and connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
    
