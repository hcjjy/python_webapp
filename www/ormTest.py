#!usr/bin/env python3
#-*- coding:utf-8 -*-
'ormTest.py'
__autor__ = 'myth'

import config
from orm import *
import asyncio
from model import User, Blog, Comment

loop = asyncio.get_event_loop()
kw ={'host':'localhost','port':3306,'user':'root','password':'root','db':'JC'}

#测试查询
@asyncio.coroutine
def test_findAll(loop):
	yield from create_pool(loop,**kw)
	users = yield from User.findAll("name = 'aaa'",**{'limit':(0,5)})
	print(users)

@asyncio.coroutine
def test_findNumber(loop):
	yield from create_pool(loop,**kw)
	num = yield from User.findNumber('name',"name = 'aaa'")
	print(num)

@asyncio.coroutine
def test_find(loop):
	yield from create_pool(loop,**kw)
	user = yield from User.find('123')
	print(user)

#测试插入
@asyncio.coroutine
def test_insert(loop):
	user = User(id = '111',name = 'aaa',email='test2@example.com', passwd='1234567890', image='about:blank')
	yield from create_pool(loop,**kw)
	yield from user.insert()
	print('insert')

#测试更新
@asyncio.coroutine
def test_update(loop):
	user = User(id = '111',name = 'fff')
	yield from create_pool(loop,**kw)
	yield from user.update()
	print('update')

#测试删除
@asyncio.coroutine
def test_delete(loop):
	user = User(id = '5')
	yield from create_pool(loop,**kw)
	yield from user.remove()
	print('delete')
	

tasks = [test_delete(loop),test_update(loop),test_insert(loop),test_findAll(loop),test_findNumber(loop),test_find(loop)]
loop.run_until_complete(asyncio.wait(tasks))
config.__pool.close()
loop.run_until_complete(config.__pool.wait_closed())
loop.close()
