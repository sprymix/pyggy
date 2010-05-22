#!/usr/bin/python

import pyggy

# instantiate a lexer and a parser
l,ltab = pyggy.getlexer("test3.pyl")
p,ptab = pyggy.getparser("test3.pyg")
l.setinput("-")
p.setlexer(l)

# parse the input
tree = p.parse()
if tree == None :
	print "error!"
else :
	print pyggy.proctree(tree, ptab)
	# uncomment if you have dotty
	#pyggy.glr.dottree(tree)

