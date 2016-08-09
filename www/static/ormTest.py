#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'ormTest.py'
__autor__ ='myth'

from orm import *
import asyncio

class User(Model):
	__table__ = 'User'
	id = IntegerField('id',True)
	name = StringField('name')

loop = asyncio.get_event_loop()
kw ={'host':'localhost','port':3306,'user':'root','password':'root','db':'JC'}

#查询测试
@asyncio.coroutine
def test_findAll(loop):
	global __pool
	yield from create_pool(loop,**kw)
	#yield from User.findAll('id = 111',[],**{'limit':(1,2)})

	# with(yield from __pool) as conn:
		# cur = yield from conn.cursor()
		# yield from cur.execute("select* from User;")#insert into User(id,name) values(1,'hh');")
		# value = yield from cur.fetchall()
		# print(value)
	
	__pool.close()
	yield from __pool.wait_closed()

user = User(id = 1,name = 'aaa')

loop.run_until_complete(test_findAll(loop))
# __pool.close()
# loop.run_until_complete(__pool.wait_closed())
# loop.close()


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
