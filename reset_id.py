import sqlite3

conn = sqlite3.connect('database.db')
conn.execute("DELETE FROM sqlite_sequence WHERE name='Students';")
conn.commit()
conn.close()

print("Student ID counter has been reset!")
