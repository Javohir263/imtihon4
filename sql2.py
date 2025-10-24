#!/usr/bin/env python3
import psycopg2
import sys
import getpass
import random
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "database": "shop_final",
    "user": "postgres",
    "password": "Java_0420"
}

# --- DB ulanish ---
def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("❌ Bazaga ulanishda xato:", e)
        sys.exit(1)

# --- Jadval yaratish ---
def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(100),
            role VARCHAR(20),
            balance NUMERIC(12,2) DEFAULT 0
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            price NUMERIC(10,2),
            quantity INT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            product_id INT REFERENCES products(id),
            quantity INT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            product_id INT REFERENCES products(id),
            quantity INT,
            total_price NUMERIC(10,2),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()

# --- Standart user va admin qo‘shish ---
def init_default_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO users (username, password, role, balance)
            VALUES 
            ('admin', 'admin123', 'admin', 0),
            ('user', 'user123', 'user', 200000)
        """)
        conn.commit()

    cur.execute("SELECT COUNT(*) FROM products;")
    if cur.fetchone()[0] == 0:
        default_products = [
            "Olma", "Banan", "Apelsin", "Pomidor", "Bodring",
            "Sut", "Non", "Tuxum", "Guruch", "Go‘sht",
            "Yog‘", "Choy", "Shakar", "Tuz", "Makaron"
        ]
        for name in default_products:
            price = random.randint(5000, 25000)
            cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s);",
                        (name, price, 20))
        conn.commit()
    cur.close()

# --- Login funksiyasi ---
def login(conn):
    cur = conn.cursor()
    print("\n=== Kirish ===")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()

    cur.execute("SELECT id, role, balance FROM users WHERE username=%s AND password=%s;", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        print("✅ Xush kelibsiz,", username)
        return {"id": user[0], "username": username, "role": user[1], "balance": float(user[2])}
    else:
        print("❌ Login yoki parol noto‘g‘ri.")
        return None

# --- Mahsulotlarni ko‘rish ---
def show_products(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, quantity FROM products ORDER BY id;")
    rows = cur.fetchall()
    print("\n📦 Mahsulotlar ro‘yxati:\n")
    for r in rows:
        print(f"{r[0]}. {r[1]} | Narx: {r[2]:,.0f} so'm | Miqdor: {r[3]} dona")
    cur.close()

# --- Admin: mahsulot qo‘shish ---
def add_product(conn):
    cur = conn.cursor()
    name = input("Mahsulot nomi: ")
    price = float(input("Narxi (so‘m): "))
    qty = int(input("Miqdori (dona): "))
    cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s,%s,%s);", (name, price, qty))
    conn.commit()
    cur.close()
    print("✅ Mahsulot qo‘shildi.")

# --- Admin: sotuvlar tarixi ---
def sales_report(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name, SUM(o.quantity), SUM(o.total_price)
        FROM orders o
        JOIN products p ON o.product_id = p.id
        GROUP BY p.name
        ORDER BY SUM(o.total_price) DESC;
    """)
    rows = cur.fetchall()
    print("\n💰 Sotuvlar tarixi:")
    if not rows:
        print("Hali sotuvlar yo‘q.")
    else:
        for r in rows:
            print(f"{r[0]} | Sotilgan: {int(r[1])} dona | Jami: {int(r[2]):,} so‘m")
    cur.close()

# --- User: savatga qo‘shish ---
def add_to_cart(conn, user_id):
    show_products(conn)
    pid = int(input("\nMahsulot ID: "))
    qty = int(input("Miqdor: "))
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM products WHERE id=%s;", (pid,))
    prod = cur.fetchone()
    if not prod:
        print("❌ Bunday mahsulot yo‘q.")
        return
    if qty > prod[0]:
        print("❌ Yetarli mahsulot yo‘q.")
        return
    cur.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s,%s,%s);", (user_id, pid, qty))
    conn.commit()
    cur.close()
    print("✅ Savatga qo‘shildi.")

# --- User: savatni ko‘rish ---
def view_cart(conn, user_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name, c.quantity, p.price, (c.quantity*p.price)
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s;
    """, (user_id,))
    rows = cur.fetchall()
    if not rows:
        print("\n🧺 Savat bo‘sh.")
    else:
        print("\n🧺 Savat:")
        total = 0
        for r in rows:
            print(f"{r[0]} | {r[1]} dona × {r[2]:,.0f} = {r[3]:,.0f} so‘m")
            total += r[3]
        print(f"💵 Jami: {total:,.0f} so‘m")
    cur.close()

# --- User: xaridni amalga oshirish ---
def checkout(conn, user):
    cur = conn.cursor()
    cur.execute("""
        SELECT c.product_id, p.name, c.quantity, p.price, (c.quantity*p.price)
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s;
    """, (user['id'],))
    rows = cur.fetchall()

    if not rows:
        print("🛒 Savat bo‘sh.")
        cur.close()
        return

    total = sum([float(r[4]) for r in rows])
    print(f"💰 Umumiy summa: {total:,.0f} so‘m")
    if total > user['balance']:
        print("❌ Balansingiz yetarli emas.")
        return

    for r in rows:
        pid, name, qty, price, _ = r
        cur.execute("UPDATE products SET quantity = quantity - %s WHERE id=%s;", (qty, pid))
        cur.execute("""
            INSERT INTO orders (user_id, product_id, quantity, total_price)
            VALUES (%s,%s,%s,%s);
        """, (user['id'], pid, qty, qty * price))

    cur.execute("UPDATE users SET balance = balance - %s WHERE id=%s;", (total, user['id']))
    cur.execute("DELETE FROM cart WHERE user_id=%s;", (user['id'],))
    conn.commit()
    cur.close()
    print("✅ Xarid muvaffaqiyatli amalga oshirildi!")

# --- Admin panel ---
def admin_menu(conn, user):
    while True:
        print("""
--- ADMIN PANEL ---
1) Mahsulotlarni ko‘rish
2) Mahsulot qo‘shish
3) Sotuvlar tarixi
4) Chiqish
        """)
        ch = input("Tanlov: ")
        if ch == "1":
            show_products(conn)
        elif ch == "2":
            add_product(conn)
        elif ch == "3":
            sales_report(conn)
        elif ch == "4":
            break
        else:
            print("❌ Noto‘g‘ri tanlov.")

# --- User panel ---
def user_menu(conn, user):
    while True:
        print(f"""
--- USER PANEL --- (balans: {user['balance']:,.0f} so‘m)
1) Mahsulotlarni ko‘rish
2) Savatga qo‘shish
3) Savatni ko‘rish
4) Xaridni amalga oshirish
5) Chiqish
        """)
        ch = input("Tanlov: ")
        if ch == "1":
            show_products(conn)
        elif ch == "2":
            add_to_cart(conn, user['id'])
        elif ch == "3":
            view_cart(conn, user['id'])
        elif ch == "4":
            checkout(conn, user)
        elif ch == "5":
            break
        else:
            print("❌ Noto‘g‘ri tanlov.")

# --- Asosiy ---
def main():
    conn = connect_db()
    create_tables(conn)
    init_default_data(conn)

    print("=== SHOP TERMINAL TIZIMIGA XUSH KELIBSIZ ===")
    user = login(conn)
    if not user:
        return

    if user['role'] == 'admin':
        admin_menu(conn, user)
    else:
        user_menu(conn, user)

    conn.close()

if __name__ == "__main__":
    main()
