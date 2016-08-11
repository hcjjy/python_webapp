#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'orm.py'
__autor__ ='myth'

import config
import asyncio,logging
import aiomysql

def log(sql,args=()):
	logging.info('SQL: %s' %sql)


#创建连接池

@asyncio.coroutine
def create_pool(loop,**kw):
	logging.info('create database connection pool...')
	config.__pool = yield from aiomysql.create_pool(
	# host='127.0.0.1', port=3306,
    # user='root', password='root',
    # db='JC', loop=loop
	host = kw.get('host','localhost'),
	port = kw.get('port',3306),
	user = kw['user'],
	password = kw['password'],
	db = kw['db'],
	maxsize = kw.get('maxsize',10),
	minsize = kw.get('minisize',1),
	loop = loop
	)

#Select函数
@asyncio.coroutine
def select(sql,args,size=None):
	log(sql,args)
	with (yield from config.__pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?','%s'),args or ())
		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()
		yield from cur.close()
		logging.info('rows returned: %s' %len(rs))
		return rs

#Insert,Update,Delete函数
@asyncio.coroutine
def execute(sql,args):
	log(sql)
	with (yield from config.__pool) as conn:
		try:
			cur = yield from conn.cursor(aiomysql.DictCursor)
			yield from cur.execute(sql.replace('?','%s'),args)
			affected = cur.rowcount
			yield from conn.commit()
		except BaseException as e:
			yield from conn.rollback()
			raise
		return affected

#create args as num
def create_args_string(num):
	L = []
	for n in range(num):
		L.append('?')
	return ', '.join(L)

#class Field
class Field(object):
	def __init__(self,name,column_type,primary_key,default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default
		
	def __str__(self):
		return '<%s, %s::%s>' %(self.__class__.__name__,self.column_type,self.name)

#Field subclass => StringField
class StringField(Field):
	def __init__(self,name = None,primary_key = False,default = None, ddl = 'varchar(100)'):
		super().__init__(name,ddl,primary_key,default) #super(StringField,self)

#Field subclass => IntegerField
class IntegerField(Field):
	def __init__(self,name = None,primary_key = False,default = None, ddl = 'int'):
		super().__init__(name,ddl,primary_key,default)
	
#metaclass ModelMetaclass
class ModelMetaclass(type):
	def __new__(cls,name,bases,attrs):
		#排除Model类本身:
		if name =='Model':
			return type.__new__(cls,name,bases,attrs)
		#获取table名称:
		tableName = attrs.get('__table__',None) or name
		logging.info('found model :%s (table: %s)' %(name,tableName))
		#获取所有的Field和主键名：
		mappings = dict()
		fields = []
		primaryKey = None
		for k,v in attrs.items():
			if isinstance(v,Field):
				logging.info('found mapping:%s ==> %s' %(k,v))
				mappings[k] = v
				if v.primary_key:
					#找到主键:
					if primaryKey:
						raise RuntimeError('Duplicate primary key for field: %s' % k)
					primaryKey = k
				else:
					fields.append(k)
		if not primaryKey:
			raise RuntimeError('Primary key not found.')
		for k in mappings.keys():
			attrs.pop(k)
		escaped_fields = list(map(lambda f: '`%s`' %f,fields))
		attrs['__mappings__'] = mappings #保存属性和列的映射关系
		attrs['__table__'] = tableName #保存表名
		attrs['__primary_key__'] = primaryKey #主键属性名
		attrs['__fields__'] = fields #除主键外的属性名
		#构造默认的select,insert,update和delete语句:
		attrs['__select__'] = 'select `%s`, %s from `%s`' %(primaryKey,', '.join(escaped_fields),tableName)
		attrs['__insert__'] = 'insert into `%s` (%s,`%s`) values(%s)' %(tableName,', '.join(escaped_fields),primaryKey,create_args_string(len(escaped_fields) + 1))
		attrs['__update__'] = 'update `%s` set %s where `%s` = ?' %(tableName, ', '.join(map(lambda f: '`%s`=?' %(f),fields)),primaryKey)#mappings.get(f).name 
		attrs['__delete__'] = 'delete from `%s` where `%s` =?' %(tableName,primaryKey)
		return type.__new__(cls,name,bases,attrs)
				
#baseclass Model
class Model(dict, metaclass=ModelMetaclass):
	def __init__(self, **kw):
		super(Model,self).__init__(**kw)
		
	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" %key)
	
	def __setattr__(self,key,value):
		self[key] = value
	
	def getValue(self,key):
		return getattr(self,key,None)
		
	def getValueOrDefault(self,key):
		value = getattr(self,key,None)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				loggin.debug('using default value for %s: %s' %(key,str(value)))
				setattr(self,key,value)
		return value
	
	@classmethod
	async def findAll(cls, where = None, args = None, **kw):
		' find objects by where clause. '
		sql = [cls.__select__]
		if where:
			sql.append('where')
			sql.append(where)
		if args is None:
			args = []
		orderBy = kw.get('orderBy',None)
		if orderBy:
			sql.append('order by')
			sql.append(orderBy)
		limit = kw.get('limit',None)
		if limit is not None:
			sql.append('limit')
			if isinstance(limit,int):
				sql.append('?')
				args.append(limit)
			elif isinstance(limit,tuple) and len(limit) == 2:
				sql.append('?,?')
				args.extend(limit)
			else:
				raise ValueError('Invalid limit value: %s' % str(limit))
		rs = await select(' '.join(sql),args)
		#print(rs)#Q2
		return [cls(**r) for r in rs]
	
	@classmethod
	async def findNumber(cls,selectField = '*',where = None,args = None):
		' find number by select and where'
		sql = ['select count(%s) _num_ from `%s`' %(selectField,cls.__table__)]
		if where:
			sql.append('where')
			sql.append(where)
		rs = await select(' '.join(sql),args)
		if len(rs) == 0:
			return None
		return rs[0]['_num_']

	@classmethod
	async def find(cls,pk):
		'find object by primary key. '
		rs = await select('%s where `%s`=?' %(cls.__select__,cls.__primary_key__),[pk],1)
		if len(rs) == 0:
			return None
		return cls(**rs[0])
	
	async def insert(self):
		args = list(map(self.getValueOrDefault,self.__fields__))
		args.append(self.getValueOrDefault(self.__primary_key__))
		rows = await execute(self.__insert__,args)
		if rows != 1:
			logging.warn('failed to insert rocord: affected rows: %s' % rows)
			
	async def update(self):
		args = list(map(self.getValue,self.__fields__))
		args.append(self.getValue(self.__primary_key__))
		rows = await execute(self.__update__,args)
		if rows != 1:
			logging.warn('failed to update by primary key: affected rows: %s' % rows)
	
	async def remove(self):
		args =[self.getValue(self.__primary_key__)]
		rows = await execute(self.__delete__,args)
		if rows != 1:
			logging.warn('failed to remove by primary key: affected rows: %s' % rows)
			
			
			
			
			
	

# class User(Model):
	# __table__ = 'User'
	# id = IntegerField('id',True)
	# name = StringField('name')

# loop = asyncio.get_event_loop()
# kw ={'host':'localhost','port':3306,'user':'root','password':'root','db':'JC'}

# #测试连接池
# @asyncio.coroutine
# def test_pool(loop):
	# global __pool
	# yield from create_pool(loop,**kw)
	# with(yield from __pool) as conn:
		# cur = yield from conn.cursor()
		# yield from cur.execute("insert into User(id,name) values(%s,%s)",[None,'kfc']);#("select* from User;")
		# value = yield from cur.fetchall()
		# print(value)
	# # __pool.close()
	# # yield from __pool.wait_closed()

# #测试查询
# @asyncio.coroutine
# def test_findAll(loop):
	# global __pool
	# yield from create_pool(loop,**kw)
	# users = yield from User.findAll("name= 'aaa'",**{'limit': (0,5)})
	# print(users)
	# # __pool.close()
	# # yield from __pool.wait_closed()

# @asyncio.coroutine
# def test_findNumber(loop):
	# global __pool
	# yield from create_pool(loop,**kw)
	# num = yield from User.findNumber('name',"name = 'aaa'")
	# print(num)
	# # __pool.close()
	# # yield from __pool.wait_closed()

# @asyncio.coroutine
# def test_find(loop):
	# global __pool
	# yield from create_pool(loop,**kw)
	# user = yield from User.find(123)
	# print(user)
	# # __pool.close()
	# # yield from __pool.wait_closed()

# #测试插入
# @asyncio.coroutine
# def test_insert(loop):
	# global __pool
	# user = User(name = 'aaa')
	# yield from create_pool(loop,**kw)
	# yield from user.insert()
	# print('insert')
	# # __pool.close()
	# # yield from __pool.wait_closed()

# #测试更新
# @asyncio.coroutine
# def test_update(loop):
	# global __pool
	# user = User(id = 111,name = 'fff')
	# print(user)
	# yield from create_pool(loop,**kw)
	# yield from user.update()
	# print('update')
	# # __pool.close()
	# # yield from __pool.wait_closed()

# #测试删除
# @asyncio.coroutine
# def test_delete(loop):
	# global __pool
	# user = User(id = 5)
	# yield from create_pool(loop,**kw)
	# yield from user.remove()
	# print('delete')
	# # __pool.close()
	# # yield from __pool.wait_closed()


# tasks = [test_pool(loop),test_delete(loop),test_update(loop),test_insert(loop),test_findAll(loop),test_findNumber(loop),test_find(loop)]
# loop.run_until_complete(asyncio.wait(tasks))
# __pool.close()
# loop.run_until_complete(__pool.wait_closed())
# loop.close()

# #创建表的mysql语句
# # create table User(
	# # id int not null auto_increment primary key,
	# # name varchar(20) not null
# # )engine = InnoDB;

# # create table Book(
	# # id int not null auto_increment primary key,
	# # name varchar(20) not null,
	# # user_id int not null,
	# # foreign key foreignName(user_id) 
	# # references User(id)
# # )engine = InnoDB;

