#!/usr/bin/python
"""
pyggy.py
	Front end for the grammar spec file parser.
"""

import sys
import getopt

from errors import *
import helpers

# for parsing
import lexer
import srgram
import glr

# import our parsing table
import pyggy_lextab
import pyggy_gramtab
gt = pyggy_gramtab

# for generating a new parse table
import slrgram


def addtagged(name, prodno) :
	if not name in gt.tagged :
		gt.tagged[name] = []
	if not prodno in gt.tagged[name] :
		gt.tagged[name].append(prodno)

def addconflict_int(conflict, p1, r, p2) :
	if (p1,p2) in conflict :
		if conflict[p1,p2] != r :
			raise SpecError("Changing relationship between %d and %d from %s to %s" % (p1, p2, r, conflict[p1,p2]))
		return 0
	else :
		conflict[p1,p2] = r
		return 1

def addconflict(conflict, p1, r, p2) :
	"""
	Add relationship "p1 r p2" to the conflict table.
	Perform transitive closure for "gt" and "pref" relations.
	"""
	if addconflict_int(conflict, p1, r, p2) and r in ["gt", "pref" ] :
		for (p3,p4),r2 in conflict.items() :
			# p3==p2:  (p1 > p2) and (p2 > p4) --> (p1 > p4)
			if p3 == p2 and r2 == r :
				addconflict_int(conflict, p1, r, p4)
			# p4==p1:  (p3 > p1) and (p1 > p2) --> (p3 > p2)
			if p1 == p4 and r2 == r :
				addconflict_int(conflict, p3, r, p2)

def setprodprec(prodprec, prodno, prec, assoc) :
	"set the precedence/assoc of a production, complain if already set."
	v = [prec,assoc]
	if prodprec[prodno] != None :
		if prodprec[prodno] != v :
			raise SpecError("Changing priority of [%s -> %s] from %s to %s" % \
				(gt.gram[prodno][0], gt.gram[prodno][1], prodprec[prodno], v))
	else :
		prodprec[prodno] = v

def printprec(tabs, conflict) :
	print "Conflict relations: "
	for (p1,p2),r in conflict.items() :
		print "  %s %s %s" % (tabs.lr0.prodstr(p1), r, tabs.lr0.prodstr(p2))
	print

def addconflict_self(conflict, l, rel) :
	"add (prod rel prod) to conflicts for each member of list"
	for tag in l :
		if tag in gt.tagged :
			for prodno in gt.tagged[tag] :
				for prodno2 in gt.tagged[tag] :
					addconflict(conflict, prodno, rel, prodno2)
					addconflict(conflict, prodno2, rel, prodno)

def addconflict_decreasing(conflict, l, rel) :
	"Add decreasing priority items to the conflict list"
	# each member is less than the last
	last = []
	for tag in l :
		if tag in gt.tagged :
			for prodno in gt.tagged[tag] :
				for lastprod in last :
					addconflict(conflict, lastprod, rel, prodno)
			if gt.tagged[tag] != [] :
				last = gt.tagged[tag]

def postproc(conflict, debug) :
	"take the data structures we built up and generate parsing tables"
	# find nonterminals and symbols
	allsyms = []
	for lhs,rhs in gt.gram :
		for el in rhs :
			if not el in allsyms :
				allsyms.append(el)
	
	# tag all productions that contain a tag in their rhs.
	unused = []
	unrefed = []
	allused = []
	for tag in gt.leftlist + gt.rightlist + gt.nonassoclist + gt.preclist + gt.preflist :
		if not tag in allused :
			allused.append(tag)
		for prodno in range(len(gt.gram)) :
			if tag in gt.gram[prodno][1] :
				addtagged(tag, prodno)
		if not tag in gt.tagged and not tag in unused :
			unused.append(tag)
	for tag1,r,tag2 in gt.rellist :
		if not tag1 in allused :
			allused.append(tag1)
		if not tag2 in allused :
			allused.append(tag2)
	for tag in gt.tagged.keys() :
		if not tag in allused and not tag in unrefed:
			unrefed.append(tag)
	if unused != [] :
		print "Warning: unused precedence tags:", " ".join(unused)
	if unrefed != [] :
		print "Warning: unreferenced tags:", " ".join(unrefed)

	# fill up the conflict table with relations from tagged lists
	addconflict_self(conflict, gt.leftlist, "left")
	addconflict_self(conflict, gt.rightlist, "right")
	addconflict_self(conflict, gt.nonassoclist, "nonassoc")
	addconflict_decreasing(conflict, gt.preclist, "gt")
	addconflict_decreasing(conflict, gt.preflist, "pref")

	# add all explicitely stated relations
	for tag1,r,tag2 in gt.rellist :
		for prod1 in gt.tagged[tag1] :
			for prod2 in gt.tagged[tag2] :
				addconflict(conflict, prod1, r, prod2)

def gen(fname, tabs) :
	f = file(fname, "w")
	f.write('\n# This file was generated automatically\n')

	# emit all the actions
	for idx in range(len(gt.funcs)) :
		prods = ""
		for idx2 in range(len(gt.gram)) :
			if gt.actions[idx2] == idx :
				if prods != "" :
					prods += ", "
				prods += tabs.lr0.prodstr(idx2)
		f.write("\n# action %d for: %s\n" % (idx, prods))
		f.write("def action%d(kids) :\n" % idx)
		for line in gt.funcs[idx].split('\n') :
			f.write("\t%s\n" % line)

	tabs.write(f)
	f.write("semactions = [%s]\n" % ", ".join(map(lambda n : "action%d" % n, gt.actions)))

	f.write("gramspec = (goto, action, semactions)\n")

	# write out the global code
	f.write("\n")
	f.write(gt.globcode)
	f.write("\n")
	f.close()

def parsespec(fname, outfname, debug = 0) :
	"""
	Parse the spec file, generate parsing tables and write it out.

	Debug levels less than 10 are for showing data about the parsed spec file
	levels 10 and higher are for showing internal data.
	"""
	l = lexer.lexer(pyggy_lextab.lexspec)
	l.setinput(fname)
	g = srgram.SRGram(gt.gramspec)
	p = glr.GLR(g)
	p.setlexer(l)

	try :
		tree = p.parse()
		# print the parse tree of the spec file
		if debug >= 11 :
			printcover = (debug >= 12)
			glr.dottree(tree, printcover)
		helpers.proctree(tree, gt)
	except ParseError,e :
		raise SpecError("%s:%d: parse error at %r" % (fname, pyggy_lextab.lineno, e.str))
	except Error,e :
		raise InternalError("unexpected exception %r" % e)


	# process the parsed data
	conflict = dict()
	followsrestrict = [[] for idx in range(len(gt.gram))]
	postproc(conflict, debug)

	# generate tables
	if debug >= 2 :
		slrgram.debug = 1
	tabs = slrgram.slrgram(gt.start, gt.gram, conflict, followsrestrict)

	# print out information about the grammar, more if debug is set.
	if debug >= 2 :
		printprec(tabs, conflict)
	printfull = (debug >= 1)
	tabs.printtab(printfull)
	if debug >= 3 : # show the lr0 state machine
		tabs.lr0.dot()

	gen(outfname, tabs)




def usage(progname) :
	print "usage:  %s [-d debuglevel] infile.pyg outfile.py"
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

