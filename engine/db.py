import sqlite3


connection = sqlite3.connect("Ultron.db")
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)


query = "INSERT INTO sys_command VALUES (null, 'Microsoft Edge', 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs')"
cursor.execute(query)
connection.commit()
