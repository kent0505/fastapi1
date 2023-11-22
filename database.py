import aiosqlite

async def create_tables():
    async with aiosqlite.connect("test.db") as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS categories (
            id    INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS blogs (
            id          INTEGER PRIMARY KEY,
            title       TEXT NOT NULL,
            category_id INTEGER
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS contents (
            id      INTEGER PRIMARY KEY,
            title   TEXT,
            image   INTEGER,
            blog_id INTEGER
        )''')
        await db.commit()

# USER
async def get_username(username: str):
    async with aiosqlite.connect("test.db") as db:
        cur = await db.execute("SELECT * FROM users WHERE username = ?", (username,))
        username = await cur.fetchone()
    return username

async def get_user(id: int):
    async with aiosqlite.connect("test.db") as db:
        cur = await db.execute("SELECT * FROM users WHERE id = ?", (id,))
        user = await cur.fetchone()
    return user

async def get_users():
    async with aiosqlite.connect("test.db") as db:
        cur =   await db.execute("SELECT * FROM users")
        users = await cur.fetchall()
    return users

async def create_user(username: str, hashed: str):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        await db.commit()

async def update_user(username: str, password: str, id: int):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("UPDATE users SET username = ?, password = ? WHERE id = ?", (username, password, id))
        await db.commit()

async def delete_user(id: int):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("DELETE FROM users WHERE id =?", (id,))
        await db.commit()

# CATEGORY
async def get_category(id: int):
    async with aiosqlite.connect("test.db") as db:
        curr =     await db.execute("SELECT * FROM categories WHERE id = ?", (id,))
        category = await curr.fetchone()
    return category

async def get_categories():
    async with aiosqlite.connect("test.db") as db:
        cur =   await db.execute("SELECT * FROM categories")
        categories = await cur.fetchall()
    return categories

async def add_category(title: str):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("INSERT INTO categories (title) VALUES (?)", (title,))
        await db.commit()

async def update_category(id: int, title: str):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("UPDATE categories SET title = ? WHERE id = ?", (title, id))
        await db.commit()

async def delete_category(id: int):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("DELETE FROM categories WHERE id = ?", (id,))
        await db.commit()

# BLOG
async def get_blog(blog_id: int):
    async with aiosqlite.connect("test.db") as db:
        curr = await db.execute("SELECT * FROM blogs WHERE id = ?", (blog_id,))
        blog = await curr.fetchone()
    return blog

async def get_blogs():
    async with aiosqlite.connect("test.db") as db:
        cur =   await db.execute("SELECT * FROM blogs")
        blogs = await cur.fetchall()
    return blogs

async def add_blog(title: str, category_id: int):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("INSERT INTO blogs (title, category_id) VALUES (?, ?)", (title, category_id))
        await db.commit()

async def update_blog(id: int, title: str, category_id: int):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("UPDATE blogs SET title = ?, category_id = ? WHERE id = ?", (title, category_id, id))
        await db.commit()

async def delete_blog(id: int):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("DELETE FROM blogs WHERE id = ?", (id,))
        await db.execute("DELETE FROM contents WHERE blog_id = ?", (id,))
        await db.commit()

# CONTENT
async def get_content(id: int):
    async with aiosqlite.connect("test.db") as db:
        curr =    await db.execute("SELECT * FROM contents WHERE id = ?", (id,))
        content = await curr.fetchone()
    return content

async def get_contents(blog_id: int):
    async with aiosqlite.connect("test.db") as db:
        cur =      await db.execute("SELECT * FROM contents WHERE blog_id = ?", (blog_id,))
        contents = await cur.fetchall()
    return contents

async def add_content(title: str, image: int, blog_id: int):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("INSERT INTO contents (title, image, blog_id) VALUES (?, ?, ?)", (title, image, blog_id))
        await db.commit()

async def update_content(id: int, title: str):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("UPDATE contents SET title = ? WHERE id = ?", (title, id))
        await db.commit()

async def delete_content(id: int):
    async with aiosqlite.connect("test.db") as db:
        await db.execute("DELETE FROM contents WHERE id = ?", (id,))
        await db.commit()