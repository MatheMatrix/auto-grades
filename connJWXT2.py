# -*- coding: utf-8 -*-

import urllib2
import cookielib
import urllib
from BeautifulSoup import BeautifulSoup
import re
import os
import platform
import ConfigParser
# import subprocess

def GetUsers():
	'''Get usres info from connJWXT2.ini
	if not exist, return {}
	'''

	cf = ConfigParser.ConfigParser()
	if 'connJWXT2.ini' in os.listdir(os.getcwd()):
		cf.read('connJWXT2.ini')
	else:
		return {}
	secs = cf.sections()
	general = dict(cf.items('General'))
	users = dict(cf.items('Users'))
	general.update(users)
	return general

def WriteUsers(num, data):
	'''Write user's information to connJWXT2.ini
	asume:
	num likes: 3
	data likes: {'user3':'012345678', 'pass3':'impassword'}
	'''
	cf = ConfigParser.ConfigParser()
	if 'connJWXT2.ini' in os.listdir(os.getcwd()):
		with open('connJWXT2.ini', 'r+') as f:
			cf.read('connJWXT2.ini')
			cf.set('General', 'users', num)
			cf.set('Users', 'user'+str(num), data['user'+str(num)])
			cf.set('Users', 'pass'+str(num), data['pass'+str(num)])
			cf.write(f)
	else:
		with open('connJWXT2.ini', 'w') as f:
			cf.read('connJWXT2.ini')
			cf.add_section('General')
			cf.set('General', 'users', num)
			cf.add_section('Users')
			cf.set('Users', 'user'+str(num), data['user'+str(num)])
			cf.set('Users', 'pass'+str(num), data['pass'+str(num)])
			cf.write(f)

data = GetUsers()
if len(data) == 0:
	print('本地暂无用户数据保存，请输入新数据: ')
	username = raw_input('输入你的学号然后按下回车键: \n')
	password = raw_input('输入你的教务处密码然后按下回车键: \n')
	data['users'] = 1
	data['user1'] = username
	data['pass1'] = password
	WriteUsers(1, data)
else:
	print('已有 {0} 个用户的数据，选择其中一个来查询（输入后按下回车键）: '.format(int(data['users'])))
	for i in range(1, int(data['users']) + 1):
		print('{0}. {1}'.format(i, data['user' + str(i)]))
	print('{0}. 输入一份新的数据'.format(i + 1, ))
	choice = raw_input('输入 \'1\' 或者别的数字（输入后按下回车键）: ')
	if choice == str(i + 1):
		username = raw_input('输入你的学号然后按下回车键: \n')
		password = raw_input('输入你的教务处密码然后按下回车键:  \n')
		data['users'] = i + 1
		data['user' + str(i + 1)] = username
		data['pass' + str(i + 1)] = password
		WriteUsers(i + 1, data)
	else:
		username = data['user' + str(choice)]
		password = data['pass' + str(choice)]

login = 'http://www.cdjwc.com/jiaowu/Login.aspx'
jw = 'http://www.cdjwc.com/jiaowu/JWXS/Default.aspx'
grates = 'http://www.cdjwc.com/jiaowu/JWXS/cjcx/jwxs_cjcx_like.aspx'

content = urllib.urlopen(login).read()

soup = BeautifulSoup(content)
viewstate	= str(soup.findAll(id = re.compile('__VIEWSTATE'))).split()[-2]
eventvali	= str(soup.findAll(id = re.compile('__EVENTVALIDATION'))).split()[-2]
# cmdok		= str(soup.findAll(id = re.compile('cmdok')))

viewstate	= viewstate.split('=')[-1][1:][:-1]
eventvali	= eventvali.split('=')[-1][1:][:-1]

data = {
	'__VIEWSTATE'		: viewstate,
	'__EVENTVALIDATION'	: eventvali,
	'Account'	: username,
	'PWD'		: password,
	'cmdok'		: ''
}

cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)
urllib2.install_opener(opener)

print('正在登录...'.decode('utf-8'))
login = urllib2.urlopen(login,urllib.urlencode(data))
c = urllib2.urlopen(grates)
print('正在从教务处获得数据...')
with open('out.htm', 'w') as f:
	f.write(c.read())
if platform.system() == 'Windows':
	print('正在打开成绩查询页面...')
	os.system('out.htm')
elif platform.system() == 'Linux':
	os.system('gnome-open out.htm')
