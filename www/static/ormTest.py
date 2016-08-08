#!/usr/bin/env python3
#http://www.liaoxuefeng.com/article/001432619295115c918a094d8954bd493037b03d27bf9a9000 -*- coding:utf-8 -*-
'ormTest.py'
__autor__ ='myth'

from orm import *
import asyncio

# class User(Model):
	# __table__ = 'User'
	# id = IntegerField('id',True)
	# name = StringField('name')

# user = User(id = 132,name = 'aaa')
loop = asyncio.get_event_loop()
kw ={'user':'root','password':'root','db':'JC'}

loop.run_until_complete(create_pool(loop,**kw))



#tasks = [user.insert()]
#loop = asyncio.get_event_loop()
#loop.run_until_complete(user.insert())#(aysncio.wait(tasks))

# async def main():
	# await asyncio.wait([user.insert()])

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
#loop.run_forever()
#loop.close()

#python ormTest.py