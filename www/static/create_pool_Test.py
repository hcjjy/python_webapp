import asyncio
from aiomysql import create_pool


loop = asyncio.get_event_loop()

pool = None
async def go():
	global pool
	pool = await create_pool(host='127.0.0.1', port=3306,
                           user='root', password='root',
                           db='JC', loop=loop)

async def go2():
	global pool
	async with pool.get() as conn:
		async with conn.cursor() as cur:
			await cur.execute("insert into User(id,name) values(121,'hqh');")
			value = await cur.fetchone()
			await conn.commit()
			print(value)

async def goAll():
	await go()
	await go2()
loop.run_until_complete(goAll())