#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'ormTest.py'
__autor__ ='myth'

import config
from orm import *
import asyncio

class User(Model):
	__table__ = 'User'
	id = IntegerField('id',True)
	name = StringField('name')

loop = asyncio.get_event_loop()
kw ={'host':'localhost','port':3306,'user':'root','password':'root','db':'JC'}

#测试连接池
@asyncio.coroutine
def test_pool(loop):
	yield from create_pool(loop,**kw)
	with(yield from config.__pool) as conn:
		cur = yield from conn.cursor()
		yield from cur.execute("insert into User(id,name) values(%s,%s)",[None,'kfc']);#("select* from User;")
		value = yield from cur.fetchall()
		print(value)
	# __pool.close()
	# yield from __pool.wait_closed()

#测试查询
@asyncio.coroutine
def test_findAll(loop):
	yield from create_pool(loop,**kw)
	users = yield from User.findAll("name= 'aaa'",**{'limit': (0,5)})
	print(users)
	# __pool.close()
	# yield from __pool.wait_closed()

@asyncio.coroutine
def test_findNumber(loop):
	yield from create_pool(loop,**kw)
	num = yield from User.findNumber('name',"name = 'aaa'")
	print(num)
	# __pool.close()
	# yield from __pool.wait_closed()

@asyncio.coroutine
def test_find(loop):
	yield from create_pool(loop,**kw)
	user = yield from User.find(123)
	print(user)
	# __pool.close()
	# yield from __pool.wait_closed()

#测试插入
@asyncio.coroutine
def test_insert(loop):
	user = User(name = 'aaa')
	yield from create_pool(loop,**kw)
	yield from user.insert()
	print('insert')
	# __pool.close()
	# yield from __pool.wait_closed()

#测试更新
@asyncio.coroutine
def test_update(loop):
	user = User(id = 111,name = 'fff')
	print(user)
	yield from create_pool(loop,**kw)
	yield from user.update()
	print('update')
	# __pool.close()
	# yield from __pool.wait_closed()

#测试删除
@asyncio.coroutine
def test_delete(loop):
	user = User(id = 5)
	yield from create_pool(loop,**kw)
	yield from user.remove()
	print('delete')
	# __pool.close()
	# yield from __pool.wait_closed()


tasks = [test_pool(loop),test_delete(loop),test_update(loop),test_insert(loop),test_findAll(loop),test_findNumber(loop),test_find(loop)]
loop.run_until_complete(asyncio.wait(tasks))
config.__pool.close()
loop.run_until_complete(config.__pool.wait_closed())
loop.close()

#创建表的mysql语句
# create table User(
	# id int not null auto_increment primary key,
	# name varchar(20) not null
# )engine = InnoDB;

# create table Book(
	# id int not null auto_increment primary key,
	# name varchar(20) not null,
	# user_id int not null,
	# foreign key foreignName(user_id) 
	# references User(id)
# )engine = InnoDB;

#Q1：with as的用法
#Q2：print(rs)输出格式异常
#Q3: 全局变量调用出错
#Q4: (@asyncio.coroutine,yield from)和(aysnc,await)使用和异同点
#Q5: mysql select args的使用,limit的用法
#Q6: 创建table主键设置了auto_increment，但是实际情况是在插入重复的时候无法自动+1
#Q7: 无法直接使用import my.py(自定义模块)

#R1：http://blog.kissdata.com/2014/05/23/python-with.html
#R2: cur = yield from conn.cursor(aiomysql.DictCursor)让返回的格式为由若干个dict元素组成的list类型，
#cur = yield from conn.cursor()返回的格式为由若干个tuple元素的tuple类型。
#R3: for example：(虽然config只会导入(执行)一次，但是main.py还是需要写import config,不然调用config.x会无法识别config)
# config.py:
# x = 0   # Default value of the 'x' configuration setting
# print('i'm config.py,just be imported once.')

# mod.py:
# import config
# config.x = 1
# print('import config')

# main.py:
# import config
# import mod
# print(config.x)
#R4: 暂时没有解决
#R5: args可以放置limit的值比如5(5代表只选择前5个结果)或者(0,5)(代表从第一个元素开始，选择连续的5个结果)
#'select * from User limit 0,5;'
#R6: 理解错误，auto_increment不是在插入重复的时候自动加1，而是可以在插入的时候不写主键，主键自动生成，生成规则如下:
#max(id)+1开始计数，可以alter table User auto_increment=值，改变开始计数值，但是如果值小于max(id)，设置无效，按max(id)+1计数。
#R7: 因为导入时python搜索路径没有当前路径，可作如下修改：控制台:1.import sys	2.sys.path.append(当前路径)


