import sqlite3

conn = sqlite3.connect('marketplace.sqlite')

c = conn.cursor()

c.execute("SELECT * FROM Shoe WHERE name OR description LIKE '%search_query%'")

print(c.fetchall)

conn.close()
