import sqlite3

conn = sqlite3.connect("Ultron.db")
cur = conn.cursor()

cur.execute("UPDATE contacts SET mobile_no = REPLACE(REPLACE(mobile_no, ' ', ''), '-', '')")
cur.execute("DELETE FROM contacts WHERE name = 'First Name'")
conn.commit()

cur.execute("SELECT * FROM contacts")
for row in cur.fetchall():
    print(row)

conn.close()