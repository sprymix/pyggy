#!/usr/bin/python

import pyggy

def singleexprstr(kids) :
	if len(kids) == 1 :
		return kids[0].sym[1]
	else :
		return "(%s %s %s)" % (exprstr(kids[0]), kids[1].sym[1], exprstr(kids[2]))

def exprstr(e) :
	res = []
	for p in e.possibilities :
		res.append(singleexprstr(p.elements))
	if len(res) == 1 :
		return res[0]
	else :
		return "[%s]" % " or ".join(res)
	
# instantiate the lexer and parser
l,ltab = pyggy.getlexer("test2.pyl")
p,ptab = pyggy.getparser("test2.pyg")
l.setinput("-")
p.setlexer(l)

# parse the input
tree = p.parse()
if tree == None :
	print "error!"
else :
	print "parse done: ", exprstr(tree)
	# if you have dot, try uncommenting the following
	#pyggy.glr.dottree(tree)

