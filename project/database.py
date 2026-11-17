import sqlite3
DB_NAME = 'uns.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS uns(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    region TEXT NOT NULL, 
    un TEXT NOT NULL,
    rating INTEGER DEFAULT 0,
    address Text not Null,
    Ft Text not Null)""")

    conn.commit()
    conn.close()

def add_university(region, un, rating, address, Ft):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO UNS (region, un, rating, address, Ft) 
    VALUES (?, ?, ?, ?, ?)
    """, (region, un, rating, address, Ft))

    conn.commit()
    conn.close()

def get_all_uns():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT region, un, rating, address, Ft
    FROM UNS
    ORDER BY id
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

# create_table()
# add_book('어린왕자', '생택쥐페리')
# add_book('데미안', '헤르만헤세')
# print(get_all_books())

def update_rating(id, rating):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""UPDATE uns SET rating = ? WHERE id = ?
    """,(rating, id))

    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed

# print(update_rating(1, 4))
# print(get_all_books())


def delete_university(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM uns WHERE id = ?
    """,(id,))

    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed

def search_uns(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT id, region, un, rating, address, Ft 
    FROM uns 
    WHERE title LIKE ? 
    ORDER BY id
    """, (f"%{keyword}%",))

    rows = cursor.fetchall()
    conn.close()
    return rows