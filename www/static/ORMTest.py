#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'ORMTest.py'
__autor__ ='myth'

import logging;logging.basicConfig(level = logging.INFO)
import asyncio,os,json,time
from datetime import datetime
from aiohttp import web

#创建连接池__pool
@asyncio.coroutine
def create_pool(loop,**kw):
	logging.info('create database connection pool...')
	global __pool
	__pool = yield from aiomysql.create_pool(
	host = kw.get('host','localhost'),
	port = kw.get('port','3306'),
	user = kw['user'],
	password = kw['password'],
	db = kw['db'],
	charset = kw.get('charset','utf-8'),
	autocommit = kw.get('charset',True),
	maxsize = kw.get('maxsize',10),
	minsize = kw.get('minisize',1),
	loop = loop
	)
	
#Select函数
@asyncio.coroutine
def select(sql,args,size=None):
	log(sql,args)
	global __pool
	with (yield from __pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?','%s'),args or ())
		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()
		yield from cur.close()
		logging.info('rows returned: %s' %len(rs))
		return rs

#Insert,Update,Delete函数 1.what is difference cursor carry args?2.what are args?
@asyncio.coroutine
def execute(sql,args):
	log(sql)
	with (yield from __pool) as conn:
		try:
			cur = yield from conn.cursor()
			yield from cur.execute(sql.replace('?','%s'),args)
			affected = cur.rowcount
			yield from cur.close()
		except BaseException as e:
			raise
		return affected

#ORM
#定义User对象
# from orm import Model, StringField, IntegerField

# class User(Model):
	# __table__ = 'users'
	# id = IntegerField(primary_key = True)
	# name = StringField()

a = 10
b = 20
c = (a<b and a or b)
print(c)














