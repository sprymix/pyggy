#!/usr/bin/python

# A parser for ansi C

import sys
import os
import pprint

def preprocess(fname) :
	"cheap preprocess"
	os.system("gcc -E '%s' >'%s.e'" % (fname, fname))
	return fname + '.e'

def parse(fname, lexonly) :
	import pyggy
	l,ltab = pyggy.getlexer("ansic.pyl")
	p,ptab = pyggy.getparser("ansic.pyg")
	p.setlexer(l)
	l.setinput(preprocess(fname))

	if lexonly :
		while 1 :
			tok = l.token()
			if tok is None :
				break
			print tok, l.value
			if tok == "#ERR#" :
				print "error at %s:%d" % (lextab.fname, lextab.lineno)
				break
	else :
		# parse the input
		tree = p.parse()
		if tree == None :
			print "error at %s:%d near %s" % (lextab.fname, lextab.lineno,
				l.value)
		else :
			print "displaying tree"
			#print tree
			#pyggy.glr.dottree(tree)
			t = pyggy.proctree(tree, ptab)
			pprint.pprint(t)
	print "done"

def usage(prog) :
	print "usage:  %s [-lpz] fname" % prog
	print "\t-l\t\tlex only\n"
	print "\t-p\t\tprofile\n"
	print "\t-z\t\tdrop to pdb on error\n"
	sys.exit(1)

def main() :
	from getopt import getopt, GetoptError

	try :
		opts,args = getopt(sys.argv[1:], "lpz")
	except GetoptError :
		usage(sys.argv[0])

	if len(args) != 1 :
		usage(sys.argv[0])

	lexonly = 0
	prof = 0
	for opt,arg in opts :
		if opt == "-l" :
			lexonly = 1
		if opt == "-p" :
			prof = 1
		if opt == "-z" :
			import traceback
			def _pdbinfo(type, value, tb) :
        			import pdb
        			traceback.print_exception(type, value, tb)
        			print
        			pdb.pm()
			sys.excepthook = _pdbinfo
		else :
			raise "cant happen"

	if prof :
		import profile
		profile.run("parse(args[0], lexonly")
	else :
		parse(args[0], lexonly)

if __name__ == "__main__" :
	main()

