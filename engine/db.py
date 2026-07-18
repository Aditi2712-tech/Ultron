import sqlite3

connection = sqlite3.connect("Ultron.db")
cursor = connection.cursor()

cursor.execute(
    "INSERT INTO contacts (name, mobile_no, email) VALUES (?, ?, ?)",
    ("Jahnavi", "9441430621", None)   # <-- change name and number here
)

connection.commit()
connection.close()
print("Contact added")