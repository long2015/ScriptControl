#!/usr/bin/env python
# -*- coding: utf-8 -*-

lang = {
	'newscript' : u'新建',
	'editscript' : u'修改',
	'loadscript' : u'加载',
	'runscript' : u'运行',
	'record' : u'录制',
	'snapscreen' : u'截屏',
	'login' : u'登录',
	'about' : u'关于',
	'quit' : u'退出',
	'commandlists' : u'命令列表',
}

def tr(key):
	try:
		value = lang[key]
	except KeyError, e:
		return key
	
	return value
