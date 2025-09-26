import sqlite3

conn = sqlite3.connect('test.db')
cur = conn.cursor()

s1 = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
"""
s12="""
insert into users(name,age) 
values ('ali1',21),('ali2',12);
"""

s2="SELECT * FROM users"
conn.commit()

# cur.execute(s1)
cur.executescript(s12)
# print("bajarildi")
rows = cur.fetchall()
print(rows)
for row in rows:
    print(row)

cur.close()
conn.close()