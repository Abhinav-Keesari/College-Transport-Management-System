import csv
import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Drop the existing table
cursor.execute("DROP TABLE IF EXISTS busdetails")
conn.commit()

# Create the new table
cursor.execute("""
CREATE TABLE IF NOT EXISTS busdetails (
    ROLL_NO TEXT PRIMARY KEY,
    NAME TEXT,
    GENDER TEXT,
    BUS_NO TEXT,
    BUS_ROUTE TEXT,
    SEMESTER INTEGER,
    VALID_UPTO TEXT,
    PHONE_NO TEXT,
    SEAT_NO INTEGER
)
""")

# Read data from busdetails.csv and insert into busdetails table
with open("busdetails.csv", "r") as file:
    reader = csv.reader(file)
    headers = next(reader)  # skip the headers
    for row in reader:
        cursor.execute("""
        INSERT INTO busdetails (ROLL_NO, NAME, GENDER, BUS_NO, BUS_ROUTE, SEMESTER, VALID_UPTO, PHONE_NO, SEAT_NO)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)


# Commit the changes
conn.commit()

# Close the connection
conn.close()