import sqlite3
import asyncio

async def users(id):
    with sqlite3.connect("database.db") as c:
        check = c.execute("SELECT id FROM users WHERE id = ?", (id,)).fetchone()
        if check is None:
            c.execute("INSERT INTO users VALUES(?)", (id,))
        else:
            pass

async def all_user():
    with sqlite3.connect('database.db') as c:
        all = c.execute("SELECT * FROM users").fetchall()
        return len(all)