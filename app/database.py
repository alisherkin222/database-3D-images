import asyncpg

async def get_connection():
    return await asyncpg.connect(
        user='alisherka',
        password='secret',
        database='defects',
        host='localhost'
    )
