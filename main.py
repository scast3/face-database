import pg8000
import getpass
import json
from datetime import datetime
from face_rec import capture_images, face_recognition
# Face Recognition Database
# Using webcam, will recognize faces from a face database
# Hope to use this in a potential security project

# Function to insert data into the PostgreSQL database
def insert_data(conn, name, image_data):
    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        other_attributes = {'status': 'new'}

        cursor.execute("""
            INSERT INTO face_recognition.person_info (person_name, image_data, other_attributes, created_at)
            VALUES (%s, %s, %s::jsonb, %s)
        """, (name, image_data, json.dumps(other_attributes), timestamp))
        conn.commit()
        print("Data inserted successfully!")
    except pg8000.Error as e:
        print(f"Error inserting data: {e}")


# Function to access the database
def search(db):
    
    while True:
        choice = input('Search by face ID (F) or by name (N)?: ')
        if choice == 'F' or choice == 'f':
            id = input('Enter face ID: ')
            search_by_id(db, id) # implement this later
            break
        elif choice == 'N' or choice == 'n':
            name = input('Enter name (first and last): ')
            search_by_name(db, name) # implement this later
            break
        else:
            print('Invalid choice. Try again.')
        print(' ')

# searches a face based on the id
def search_by_id(db, id):
    cursor = db.cursor()
    query = """SELECT person_id, person_name, created_at 
               FROM person_info
               WHERE person_id = %s
               ORDER BY created_at"""
    try:
        cursor.execute(query, (id, ))
        resultset = cursor.fetchall()
        return resultset

    except pg8000.Error as e:
        print("Database error\n")
        return []

def search_by_name(db, name):
    cursor = db.cursor()
    query = """SELECT person_id, person_name, created_at 
               FROM person_info
               WHERE person_id = %s
               ORDER BY created_at"""
    try:
        cursor.execute(query, (name, ))
        resultset = cursor.fetchall()
        return resultset

    except pg8000.Error as e:
        print("Database error\n")
        return []

def alter(db):
    while True:
        choice = input('Add attributes (A), delete face (D)')
        if choice == 'A' or 'a':
            id = input('Enter face ID:')
            add_attribute(db, id, attribute) # fix
        elif choice == 'D' or choice == 'd':
            id = input('Enter face ID:')
            delete(db, id)

# adds an attribute
def add_attribute(db, id, attribute):
    cursor = db.cursor()
    query = """UPDATE person_info
                SET other_attributes = %s
                WHERE person_id = %s """
    try:
        cursor.execute(query, (attribute, id))
        db.commit()
        print(f'Altered attributes of: {id}')
    except pg8000.Error as e:
        db.rollback()
        print("Face does not exist (invalid face id), or not properly implemented.")
        print('Details: ' + id)
        print(e)

# deletes a face based on the face id
def delete(db, id):
    cursor = db.cursor()
    query = "DELETE FROM person_info WHERE person_id = %s"
    try:
        cursor.execute(query, (id, ))
        db.commit()
        print('Delete face: ' + str(id))
    except pg8000.Error as e:
        db.rollback()
        print("Face does not exist (invalid face id), or not properly implemented.")
        print('Details: ' + id)
        print(e)

# Connect to PostgreSQL database
def get_connection() -> pg8000.Connection:
    # Get the username and password
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    # Connect to the database
    credentials = {
        'user': username,
        'password': password,
        'database': 'faces',
        'port': 5432,
        'host': 'localhost'
    }
    try:
        db = pg8000.connect(**credentials)
        db.autocommit = False
        return db
    except pg8000.Error as e:
        print(f'Authentication failed for user "{username}" (error: {e})\n')
        return None


# Main function to initiate the process
    
def main():
    # connect to the database. Loop until we get a db object.
    # This tells us that the user has successfully logged in.
    while True:
        db = get_connection()
        if db is not None:
            break

    # main loop
    while True:
        choice = input('Capture New Face (N)\nFace Recognition (R)\nSearch Database (S)\nAlter Database (A)\nQuit (Q)\n')
        if choice == 'N' or choice == 'n':
            capture_images(db)
        elif choice == 'F' or choice == 'f':
            face_recognition(db)
        elif choice == 'S' or choice == 's':
            search(db)
        elif choice == 'A' or choice == 'a':
            alter(db)
        elif (choice == 'Q' or choice == 'q'):
            print("Ending Session ... ")
            break
        else:
            print("Invalid choice. Try again.")
        print(" ")


if __name__ == "__main__":
    main()
