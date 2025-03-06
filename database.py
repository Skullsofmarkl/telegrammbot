import aiosqlite
from config import DB_NAME

async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_score (user_id INTEGER PRIMARY KEY, score INTEGER DEFAULT 0)''')
        await db.commit()

async def update_score(user_id, increment=False, reset=False):
    async with aiosqlite.connect(DB_NAME) as db:
        if reset:
            await db.execute('INSERT OR REPLACE INTO quiz_score (user_id, score) VALUES (?, 0)', (user_id,))
        elif increment:
            await db.execute('INSERT INTO quiz_score (user_id, score) VALUES (?, 1) ON CONFLICT(user_id) DO UPDATE SET score = score + 1', (user_id,))
        await db.commit()

async def get_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM quiz_score WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            return results[0] if results else 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()