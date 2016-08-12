#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'Model.py'
__autor__ ='myth'

import time,uuid
from orm import Model,StringField,BooleanField,FloatField,TextField

def next_id():
	return ''
	
class User(Model):
	__table__ = 'users'
	
	id = StringField(primary_key = True, default = next_id, ddl = 'varchar(50)')
	email = StringField(ddl = 'varchar(50)')
	passwd = StringField(ddl = 'varchar(50)')
	admin = BooleanField()
	name = StringField(ddl = 'varchar(50)')
	image = StringField(ddl = 'varchar(50)')
	create_at = FloatField(default = time.time)
	
class Blog(Model):
	__table__ = 'blogs'
	
	id = StringField(primary_key = True, default = next_id, ddl = 'varchar(50)')
	