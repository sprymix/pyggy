#!/usr/bin/python

import pyggy

l,tab = pyggy.getlexer("test1.pyl")
l.setinput("-")
while 1 :
	x = l.token()
	if x is None :
		break
	print x, l.value

