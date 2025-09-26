import psycopg2
conn = psycopg2.connect(
    dbname="categoris",
    user="catigoris",
    password="Java_0420",
    host="localhost", #127.0.0.1
    port="5432"
)
cur = conn.cursor()
sql1 = '''
select * from categories
'''

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

# Malumot qo‘shish

cur.execute(sql1)
s = cur.fetchall()
print(s)
for item in s:
    print(item[0],item[1])

conn.commit()
cur.close()
conn.close()
