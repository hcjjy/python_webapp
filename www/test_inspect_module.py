#!/usr/bin/env python3
#-*- coding:utf-8-*-
'test_inspect_module.py'
__autor__ = 'myth'

import inspect
#获取函数传递值中的可变参数或命名关键字参数(不包含设置缺省值的)名称列表：
def get_required_kw_args(fn):
    args = []
    #inspect.signature(fn)：表示fn函数的调用签名及其返回注释，为函数提供一个Parameter对象存储参数集合。
    #inspect.signature(fn).parameters：参数名与参数对象的有序映射。
    params = inspect.signature(fn).parameters
    print(params)
    for name, param in params.items():  #.items()返回一个由tuple(此处包含name, parameters object)组成的list。
        #inspect.Parameter.kind：描述参数值对应到传参列表(有固定的5种方式，KEYWORD_ONLY表示值为“可变参数或命名关键字参数”)的方式。
        #inspect.Parameter.default：参数的缺省值，如果没有则属性被设置为 Parameter.empty。
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

#获取函数传递值中的可变参数或命名关键字参数(全部的)名称列表：
def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

#判断函数传递值中是否存在关键字参数：
def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        #VAR_KEYWORD表示值为关键字参数。
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

#判断函数传递值中是否包含“request”参数，若有则返回True：
def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        #传递值中包含名为'request'的参数则跳出本次循环(不执行本次循环中的后续语句，但还是接着for循环)，found赋值为True：
        if name == 'request':
            found = True
            continue
        #VAR_POSITIONAL表示值为可变参数。
        #传递值中包含参数名为'request'的参数，且参数值对应到传参列表方式不是“可变参数、关键字命名参数、关键字参数”中的任意一种，则抛出异常：
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
        print(param.kind)
    return found

def testFun(a,b,request,*args,kwOnly,**kw):
	pass
print(get_required_kw_args(testFun))
print(get_named_kw_args(testFun))
print(has_var_kw_arg(testFun))
print(has_request_arg(testFun))







