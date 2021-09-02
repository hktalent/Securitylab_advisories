#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests as requestsSs
import urllib3,re,os,os.path

urllib3.disable_warnings()
requestsSs.packages.urllib3.disable_warnings()

requests = requestsSs.session()
myTime=(13, 15)

url="https://securitylab.github.com/advisories/"
r1 = requests.get(url,verify=False,timeout=myTime)
szStr = r1.text

myR=r'<a href="\/advisories\/([^"\/]+)?'

a=re.findall(myR,szStr)
s9="<header class=\"post-header"
s0="</main>"
for k in a:
	try:
		szU1=url+k+"/"
		print("\nstart "+szU1)
		szJsonF="j/"+k+".md"
		if os.path.exists(szJsonF):
			continue
		r1 = requests.get(szU1,verify=False,timeout=myTime)
		szStr = r1.text
		if None == szStr:
			continue

		n1=szStr.index(s9)
		n2=szStr.index(s0)
		ss1=str.encode(szStr)[n1:n2]
		if None != ss1 and 0 < len(ss1):
			f=open(szJsonF,"wb")
			f.write(ss1)
			f.close()
			print(k + " is ok")
		else:
			print(k + " not get " + szStr)
	except Exception as e:
		print(k + " is error ")
		print(e)
		continue