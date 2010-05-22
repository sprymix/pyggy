#!/usr/bin/python
#
# pylly.py
#	Frontend for generating a lexer from a pyl specification file.
#

import sys
import getopt

from errors import *
import helpers

# for lexing/parsing the spec
import srgram
import glr
import lexer

import pylly_lextab
from pylly_lextab import lexspec
import pylly_gramtab
gt = pylly_gramtab

# post processing
import dfa

# generate an action function for a regexp pattern.
def genfunc(f, name, re, code) :
	f.write("\n# action %s for pattern \"%s\"\n" % (name, re))
	f.write("def action%s(self) :\n" % name)
	if code != None :
		for line in code.split('\n') :
			f.write("\t%s\n" % line)
	else :
		f.write("\tpass\n")

# generate a lexer spec file.
def gen(fname, d) :
	f = file(fname, 'w')
	f.write("#\n# This file was automatically generated.\n\n")

	# spit out the start states
	f.write("# Start state names\n")
	for k,v in gt.statenums.items() :
		f.write("%s = %s\n" % (k,v))
	f.write("\n")

	# write out the action functions
	acttab = ["None"]
	for idx in range(1, len(gt.actions)) :
		act = gt.actions[idx]
		re = gt.relist[idx]
		genfunc(f, "%d" % idx, re, act)
		acttab.append("action%d" % idx)
	f.write("\n")

	# write out the eof action functions
	eoftab = []
	for idx in range(len(gt.eofacts)) :
		act = gt.eofacts[idx]
		if act :
			genfunc(f, "eof%d" % idx, "<<EOF>>", act)
			eoftab.append("actioneof%d" % idx)
		else :
			eoftab.append("None")
	f.write("\n")

	d.write(f)
	f.write("actions = [%s]\n" % ", ".join(acttab))
	f.write("eofactions = [%s]\n" % ", ".join(eoftab))
	f.write("\nlexspec = (rows,acc,starts,actions,eofactions,chr2uccl)\n")
			
	# write out the global code
	f.write("\n")
	f.write(gt.globcode)
	f.write("\n")
	f.close()


# take the data we collected, generate a dfa and write its table out
def postproc(outfname, debug = 0) :
	machlist = []
	for idx in range(len(gt.statemachs)) :
		unanch,anch = gt.statemachs[idx]
		if anch == None :
			mach = unanch
		else :
			mach = gt.n.dualmach(unanch, anch)
		if mach == None :
			# XXX use state name not number
			raise SpecError("No regular expressions for state %d!" % idx)
		machlist.append((mach, unanch),)
		if debug >= 3 :
			# XXX this is flawed.  the NFA dot printer doesnt work
			# properly for the dualmach() joined machines because
			# their states are not strictly sequential!  This will
			# print extra nodes not really in the NFA!
			gt.n.dot(mach)
	d = dfa.dfa(machlist, gt.relist)

	# XXX flag to sanity to specify debug level?
	printfull = (debug >= 1)
	d.sanity(printfull)
	if debug >= 2 :
		shownfa,showccl = 0,0
		if debug >= 3 :
			shownfa,showccl = 1,1
		d.dot(shownfa, showccl)

	gen(outfname, d)


# parse a spec file fname and generate lexer spec in outfname
# Debug levels less than 10 show information about the constructed lexer.
# Higher debug levels show internal data.
def parsespec(fname, outfname, debug = 0) :
	l = lexer.lexer(lexspec)
	l.setinput(fname)
	g = srgram.SRGram(gt.gramspec)
	p = glr.GLR(g)
	p.setlexer(l)

	try :
		tree = p.parse()
		if debug >= 10 :
			glr.dottree(tree)
		helpers.proctree(tree, gt)
	except ParseError,e :
		raise SpecError("%s:%d: parse error at %r" % (fname, pylly_lextab.lineno, e.str))
	except Error,e :
		raise InternalError("unexpected exception %r" % e)
	postproc(outfname, debug)


def usage(progname) :
	print "usage:  %s [-d debuglevel] infile.pyl outfile.py"
	sys.exit(1)

def main() :
	try :
		opts,args = getopt.getopt(sys.argv[1:], "d:h")
	except getopt.GetoptError :
		usage(sys.argv[0])

	if len(args) != 2 :
		usage(sys.argv[0])

	debug = 0
	for opt,arg in opts :
		if opt == "-d" :
			debug = int(arg)
		elif opt == "-h" :
			usage(sys.argv[0])
	try :
		parsespec(args[0], args[1], debug)
	except Error,e :
		print e.args[0]

if __name__ == "__main__" :
	main()

