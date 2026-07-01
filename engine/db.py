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