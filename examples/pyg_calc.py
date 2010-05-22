
"""
pgy_calc.py
	A simple calculator with variables

based on calc.py from the PLY web page.
"""

import sys
import pyggy

# build the lexer and parser
l,ltab = pyggy.getlexer("pyg_calc.pyl")
p,ptab = pyggy.getparser("pyg_calc.pyg")
p.setlexer(l)

while 1:
	sys.stdout.write("calc > ")
	line = sys.stdin.readline()
	if line == "" :
		break
	
	l.setinputstr(line)
	try :
		tree = p.parse()
	except pyggy.ParseError,e :
		print "parse error at '%s'" % e.str
		continue
	pyggy.proctree(tree, ptab)

