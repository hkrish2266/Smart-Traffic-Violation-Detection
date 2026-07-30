import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create database connection
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()


def save_violation(number_plate,rider_image,vehicle_image,plate_image, violation):

    query = """
    INSERT INTO violations
    (number_plate,rider_image,vehicle_image,plate_image, violation)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        number_plate, rider_image, vehicle_image, plate_image, violation
    )

    cursor.execute(query, values)
    conn.commit()

    print("Saved:", number_plate)


def close_connection():
    cursor.close()
    conn.close()