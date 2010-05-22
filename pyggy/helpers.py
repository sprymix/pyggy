
"""
The helpers in this file are exported directly under the pyggy package.
The provide easy access to parser and lexer construction.
"""

import glr
from errors import *

def _mtime(fname) :
	import os
	return os.stat(fname)[8]

def _import(name) :
	if name[-3:] == ".py" :
		name = name[:-3]
	exec "import " + name
	return eval(name)

def generate(fname, targ, debug=0, forcegen=0) :
	"""
	Generate tables from a grammar or lexer spec file.
	"""
	import os.path
	if forcegen or not os.path.exists(targ) or _mtime(targ) < _mtime(fname) :
		print "generating %s from %s" % (targ, fname)
		if fname[-4:] == ".pyl" :
			import pylly
			pylly.parsespec(fname, targ, debug=debug)
		elif fname[-4:] == ".pyg" :
			import pyggy
			pyggy.parsespec(fname, targ, debug=debug)
		else :
			raise ApiError("bad spec filename %s" % fname)

def getlexer(specfname, debug=0, forcegen=0) :
	"""
	Generate a lexer table, construct a lexer for lexing fname and return it.
	Both the lexer and the generated module are returned.
	"""
	import lexer

	if specfname[-4:] != ".pyl" :
		raise ApiError("bad spec filename %s" % specfname)
	tab = specfname[:-4] + "_lextab.py"
	generate(specfname, tab, debug=debug, forcegen=forcegen)
	l = _import(tab)
	return lexer.lexer(l.lexspec), l

def getparser(specfname, debug=0, forcegen=0) :
	"""
	Generate a parser table, construct a parser and return it.
	The parser and the generated module are returned.
	"""
	import srgram
	import glr

	if specfname[-4:] != ".pyg" :
		raise ApiError("bad spec filename %s" % specfname)
	tab = specfname[:-4] + "_gramtab.py"
	generate(specfname, tab, debug=debug, forcegen=forcegen)
	gram = _import(tab)
	g = srgram.SRGram(gram.gramspec)
	p = glr.GLR(g)
	return p, gram

class TreeProc :
	def __init__(self, gram, allowambig=0) :
		self.gram = gram
		self.allowambig = allowambig

	def proctree(self, t) :
		if isinstance(t, glr.symnode) :
			# eliminate uneeded possibilities
			if self.allowambig :
				t.possibilities = map(self.proctree, t.possibilities)
				return t
			elif len(t.possibilities) > 1 :
				raise AmbigParseError("ambiguous parse of %s" % t.sym)
			elif len(t.possibilities) == 1 :
				return self.proctree(t.possibilities[0])
			else :
				# for terminals, return the token value
				return t.sym[1]
		elif isinstance(t, glr.rulenode) :
			# return the result of the semantic action performed on the 
			# children.
			kids = map(self.proctree, t.elements)
			sym,redlen,prodno = t.rule
			return self.gram.semactions[prodno](kids)
		else :
			raise ApiError("Illegal node in tree: %s" % t.__class__)
		
def proctree(t, gram, allowambig=0) :
	"""
	Process the parsed tree, executing the semantic actions
	associated with each production.
	If allowambig is specified, symbol nodes, which can contain
	several possible parses, are left in place.  Otherwise symbol
	nodes are removed, and an exception is thrown if an ambiguous
	parse is detected.

	The original parse tree is altered in the process and should
	not be used after this function is run.
	XXX we can fix that if we have to, but probably not worth it.
	"""
	p = TreeProc(gram, allowambig=allowambig)
	return p.proctree(t)

