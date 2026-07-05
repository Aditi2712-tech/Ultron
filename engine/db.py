import csv
import sqlite3

connection = sqlite3.connect("Ultron.db")
cursor = connection.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)


# query = r"INSERT INTO sys_command VALUES (null, 'VS Code3', 'code')"
# cursor.execute(query)
# connection.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null, 'YouTube', 'https://www.youtube.com/')"
# cursor.execute(query)
# connection.commit()

# query = "DELETE FROM sys_command WHERE name = ?"
# cursor.execute(query, ('Microsoft Edge',))
# connection.commit()


# Create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')



# # Specify the column indices you want to import (0-based index)
# # Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute('''
#     INSERT INTO contacts (id, name, mobile_no)
#     VALUES (NULL, ?, ?);
# ''', tuple(selected_data))
        

# Delete duplicate contacts based on mobile number
cursor.execute('''
DELETE FROM contacts
WHERE id NOT IN (
    SELECT MIN(id)
    FROM contacts
    GROUP BY mobile_no
)
''')

connection.commit()

query = 'aditi'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()
print(results[0][0])


# Commit changes and close connection
connection.commit()
connection.close()






































# # Check duplicates first
# cursor.execute("SELECT name, path, COUNT(*) FROM sys_command GROUP BY name, path HAVING COUNT(*) > 1")
# print("Duplicates found:", cursor.fetchall())

# # Delete duplicates, keep the first (lowest id)
# cursor.execute("""
#     DELETE FROM sys_command
#     WHERE id NOT IN (
#         SELECT MIN(id)
#         FROM sys_command
#         GROUP BY name, path
#     )
# """)
# connection.commit()
# print(f"Deleted {cursor.rowcount} duplicate(s)")

# # Verify result
# cursor.execute("SELECT * FROM sys_command")
# print("Remaining rows:", cursor.fetchall())

# connection.close()