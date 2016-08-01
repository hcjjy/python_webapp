#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'orm.py'
__autor__ ='myth'

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

class Field(object):
	def __init__(self,name,column_type,primary_key,default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default
		
	def __str__(self):
		return '<%s, %s:%s>' %(self.__class__.__name__,self.column_type,self.name)
		