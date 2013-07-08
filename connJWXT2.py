import urllib2
import cookielib
import urllib
from BeautifulSoup import BeautifulSoup
import re
import os
import platform
# import subprocess

login = 'http://www.cdjwc.com/jiaowu/Login.aspx'
jw = 'http://www.cdjwc.com/jiaowu/JWXS/Default.aspx'
grates = 'http://www.cdjwc.com/jiaowu/JWXS/cjcx/jwxs_cjcx_like.aspx'

if 'connJWXT2.ini' in os.listdir(os.getcwd()):
	with open('connJWXT2.ini', 'r') as f:
		username, password = f.read().split('\n')
else:
	username = raw_input('Input your ID: \n')
	password = raw_input('Input your Password: \n')

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

login = urllib2.urlopen(login,urllib.urlencode(data))
c = urllib2.urlopen(grates)
with open('out.htm', 'w') as f:
	f.write(c.read())
with open('connJWXT2.ini', 'w') as f:
	f.write(username + '\n' + password)

if platform.system() == 'Windows':
	os.system('out.htm')
elif platform.system() == 'Linux':
	os.system('gnome-open out.htm')
