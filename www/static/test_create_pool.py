#!/usr/bin/env python3
#-*- coding:utf-8-*-
'create_pool_Test.py'
__autor__ = 'myth'

import asyncio
#!/usr/bin/env python3
#-*- coding:utf-8-*-
'create_pool_Test.py'
__autor__ = 'myth'
#help http://aiomysql.readthedocs.io/en/stable/pool.html
from aiomysql import create_pool


loop = asyncio.get_event_loop()


async def go(loop):
	global pool
	pool = await create_pool(host='127.0.0.1', port=3306,
					   user='root', password='root',
					   db='JC', loop=loop)
	conn = await pool.acquire()
	async with conn.cursor() as cur:
		await cur.execute("insert into User(name) values('hqh1');")
		value = cur.rowcount
		print(value)
		await conn.commit()
	pool.release(conn)
	pool.close()
	await pool.wait_closed()
	

loop.run_until_complete(go(loop))
# pool.close()
# loop.run_until_complete(pool.wait_closed())
loop.close()

# import asyncio
# import aiomysql


# loop = asyncio.get_event_loop()


# @asyncio.coroutine
# def test_example():
    # pool = yield from aiomysql.create_pool(host='127.0.0.1', port=3306,
                                           # user='root', password='root',
                                           # db='JC', loop=loop)
    # with (yield from pool) as conn:
        # cur = yield from conn.cursor()
        # yield from cur.execute("select* from User")
        # r = yield from cur.fetchall()
        # print(r)
    # pool.close()
    # yield from pool.wait_closed()

# loop.run_until_complete(test_example())


# import asyncio
# import aiomysql

# loop = asyncio.get_event_loop()

# @asyncio.coroutine
# def funcrud(loop):
    # yield from test_example(loop)
    # global pool
    # with (yield from pool) as conn:
        # cur = yield from conn.cursor()
        # yield from cur.execute("select* from User")
        # r = yield from cur.fetchall()
        # print(r)
    # pool.close()
    # yield from pool.wait_closed()
# @asyncio.coroutine
# def test_example(loop):
    # global pool
    # pool = yield from aiomysql.create_pool(host='localhost', port=3306,
                                           # user='root', password='root',
                                           # db='JC', loop=loop)

# loop.run_until_complete(funcrud(loop))
# loop.close()










