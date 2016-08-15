#!/usr/bin/env python3
#-*- coding:utf-8-*-
'globalvar config file'
__autor__ = 'myth'

import config_default
#数据库连接池
__pool = None

class Dict(dict):
	'''
	Simple dict but suppport access as x.y style.
	'''
	def __init__(self,names = (),values = (),**kw):
		super(Dict,self).__init__(**kw)
		#zip([seql, ...])接受一系列可迭代对象作为参数，将对象中对应的元素打包成一个个tuple（元组），然后返回由这些tuples组成的list（列表）。
        # 若传入参数的长度不等，则返回list的长度和参数中长度最短的对象相同。
		for k,v in zip(names,values):
			self[k] = v
			
	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			return AttributeError(r"'Dict' object has no attribute '%s'" %key)
		
	def __setattr__(self,key,value):
		self[key] = value
		
def merge(defaults, override):
	r = {}
	for k,v in defaults.items():
		if k in override:
			if isinstance(v,dict):
				r[k] = merge(v,override[k])
			else:
				r[k] = override[k]
		else:
			r[k] = v
	return r
	
def toDict(d):
	D = Dict()
	for k,v in d.items():
		D[k] = toDict(v) if isinstance(v,dict) else v
	return D

configs = config_default.configs
try:
	import config_override
	configs = merge(configs,config_override.configs)
except ImportError:
	pass

configs = toDict(configs)













	