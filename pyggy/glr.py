#/usr/bin/python
"""
glr.py
	Implements a shift-reduce parser using rekers' parsing algorithm.

GLR parsing algorithm from
  J. G. Rekers, "Parser Generator for Interactive Environments"
  page 31 section 1.5.1 Algorithm of the parser with improved sharing
and is based on Tomita parsing.
"""

import dot
from util import printable
from errors import *

class prevlink :
	"a link to a previous stacknode.  Each link has an associated symnode tree"
	def __init__(self, prev, tree) :
		self.prev = prev
		self.tree = tree

class stacknode :
	"""
	a stacknode represents a parse state and has links to previous states
	in the tomita stack.
	"""
	def __init__(self, links, state) :
		self.links = links
		self.state = state

class symnode :
	"""
	A symnode represents a parsed symbol.  If the parse is ambiguous
	there may be multiple possibilities.  Each possibility points to 
	a rulenode.
	cover is expressed as (startpos,endpos+1), if the cover is empty
		the two values will be identical. If a single symbol is
		covered, the cover will be (pos,pos+1).
	note: the cover of each possibility will always be identical
	"""
	def __init__(self, sym, possibilities, cover) :
		self.sym = sym
		self.possibilities = possibilities
		self.cover = cover

class rulenode :
	"""
	A rulenode represents a single parse for a grammar production.  It has
	as many elements as there are items on the right hand side of the 
	production.  The cover is an integer range (min,max+1) of what input 
	symbols this rule node covers.  
	"""
	def __init__(self, rule, elements, cover) :
		self.rule = rule
		self.elements = elements
		self.cover = cover

def findbystate(set, state) :
	"find a node with the same state in set and return it"
	for p in set :
		if p.state == state :
			return p

def findlinkbyprev(p, prev) :
	"find a link that points to prev and return that link"
	for l in p.links :
		if l.prev == prev :
			return l

def dottree_rec(d, sym, rules, syms, printcover) :
	"helper for dottree()"
	if syms.has_key(sym) :
		return
	syms[sym] = 1

	name = str(sym.sym)
	if printcover :
		if sym.cover :
			name += "  cover %d,%d" % sym.cover
	d.add("    sym_%d [label=\"%s\", color=red];" % (hash(sym), printable(name, 1, 0)))
	for p in sym.possibilities :
		d.add("    sym_%d -> rule_%d;" % (hash(sym), hash(p)))
		if not rules.has_key(p) :
			rules[p] = 1
			name = str(p.rule)
			if printcover :
				if p.cover :
					name += "  cover %d,%d" % p.cover
			d.add("    rule_%d [label=\"%s\"];" % (hash(p), printable(name, 1, 0)))
			for e in p.elements :
				d.add("    rule_%d -> sym_%s;" % (hash(p), hash(e)))
				dottree_rec(d, e, rules, syms, printcover)

def dottree(tree, printcover = 0) :
	"""
	print out a tree (rooted with a symnode) graphically
	if printcover is true, print the cover of each node.
	"""
	if tree == None :
		return
	d = dot.dot("ParseTree")
	d.add("    start -> sym_%s;" % hash(tree))
	dottree_rec(d, tree, dict(), dict(), printcover)
	d.end()
	d.show()

def dotstack_rec(d, node, visited, heads) :
	"dotstack helper"
	if visited.has_key(node) :
		return
	visited[node] = 1

	if node in heads :
		color = ",color=red"
	else :
		color = ""
	d.add("    node_%d [label=\"%s\"%s];" % (hash(node), node.state, color))
	for l in node.links :
		d.add("    node_%d -> node_%d [label=\"%s\"];" % (hash(node), 
				hash(l.prev), l.tree.sym))
		dotstack_rec(d, l.prev, visited, heads)

def dotstack(heads) :
	"print out a tomita stack graphically"
	d = dot.dot("ParseStacks")
	visited = dict()
	for h in heads :
		dotstack_rec(d, h, visited, heads)
	d.end()
	d.show()

def pathsatdepth(p, n, l = None, usedl = 0) :
	"""
	starting at p return the list of all nodes that are n hops away along 
	with the paths used to reach them.  If l is specified, only return 
	paths that make use of that particular link
	"""
	if n <= 0 :
		if l == None or usedl :
			path = []
			return [(p, path)]
		else :
			return []
	else :
		retset = []
		for link in p.links :
			set = pathsatdepth(link.prev, n - 1, l, usedl or l == link)
			for el in set :
				path = el[1]
				path.append(link.tree)
			retset += set
		return retset

class GLR :
	"""
	The generalized LR parser engine.
	"""
	def __init__(self, gram) :
		# here are our member variables
		self.grammar = gram

		self.accepting_parser = None
		self.active_parsers = []
		self.actors = []
		self.errtoken = None
		self.position = 0
		self.rulenodes = []
		self.shifters = []
		self.symbolnodes = []
		self.token = None
		self.lexer = None

	def setlexer(self, lex) :
		"set the lexer"
		self.lexer = lex

	def parse(self) :
		"run the parser using the grammar and lexer previously set"
		self.rulenodes = []
		self.symbolnodes = []
		self.accepting_parser = None
		self.errtoken = None
		p = stacknode([], self.grammar.start)
		self.active_parsers = [p]
		self.position = 0
		while not self.accepting_parser and not self.errtoken :
			self.token = self.lexer.token()
			if self.token is None :
				self.token = "$EOF$"
			self.tokval = self.lexer.value
			self.position += 1
			#print [p.state for p in self.active_parsers], self.token, self.tokval
			self.parseword()

		if self.accepting_parser :
			assert len(self.accepting_parser.links) == 1
			return self.accepting_parser.links[0].tree
		else :
			assert self.errtoken
			raise ParseError(self.tokval, self.errtoken)
		return None

	def parseword(self) :
		"handle an input token"
		self.actors = self.active_parsers[:]
		self.shifters = []
		self.rulenodes = []
		self.symbolnodes = []
		while self.actors :
			p = self.actors.pop()
			self.actor(p)
		self.shifter()

	def actor(self, p) :
		"handle a single active node"
		for action,actarg in self.grammar.action(p.state, self.token) :
			if action == "shift" :
				shiftstate = actarg
				self.shifters.append((p, shiftstate),)
			elif action == "reduce" :
				reduction = actarg
				self.do_reductions(p, reduction)
			elif action == "accept" :
				self.accepting_parser = p
			else :
				raise InternalError("Illegal action: %s" % action)

	def do_reductions(self, p, reduction) :
		"perform a reduction on an active node along all possible paths"
		sym,redlen,prodno = reduction
		for p2,kids in pathsatdepth(p, redlen) :
			self.reducer(p2, self.grammar.goto(p2.state, prodno), reduction, kids)

	def reducer(self, p_, state, reduction, kids) :
		"perform a single reduction"
		#print "reduce", state
		if state == None : 
			# goto transition was filtered because of priority conflict.
			return

		sym,redlen,prodno = reduction
		#newkids = self.grammar.reducefunc(prodno, kids)
		newkids = kids
		rulenode = self.get_rulenode(reduction, kids, newkids)
		p = findbystate(self.active_parsers, state)
		if p :
			link = findlinkbyprev(p, p_)
			if link :
				self.add_rulenode(link.tree, rulenode)
			else :
				n = self.get_symbolnode(sym, rulenode)
				link = prevlink(p_, n)
				p.links.append(link)
				for p2 in self.active_parsers :
					if p2 in self.actors :
						continue

					# do any new reductions possible through the link
					for action,actarg in self.grammar.action(p2.state, self.token) :
						if action == "reduce" :
							reduction = actarg
							self.do_limited_reductions(p2, reduction, link)
		else :
			# crate new node and add it after p_
			n = self.get_symbolnode(sym, rulenode)
			link = prevlink(p_, n)
			p = stacknode([link], state)
			self.active_parsers.append(p)
			self.actors.append(p)

	def do_limited_reductions(self, p, reduction, link) :
		"do a reduction through all paths from p through link"
		sym,redlen,prodno = reduction
		for p2,kids in pathsatdepth(p, redlen, link) :
			self.reducer(p2, self.grammar.goto(p2.state, prodno), reduction, kids)

	def shifter(self) :
		"perform all shifts"
		# make a symbol node representing the token we're shifting
		n = symnode((self.token, self.tokval), [], (self.position,self.position+1))
		self.active_parsers = []
		for p_,state2 in self.shifters :
			#print "shift", state2
			p = findbystate(self.active_parsers, state2)
			link = prevlink(p_, n)
			if p :
				p.links.append(link)
			else :
				p = stacknode([link], state2)
				self.active_parsers.append(p)
		if self.active_parsers == [] :
			self.errtoken = self.token

	def get_rulenode(self, r, kids, newkids) :
		for n in self.rulenodes :
			if n.rule == r and n.elements == newkids :
				break
		else :
			n = rulenode(r, newkids, self.cover(kids))
			self.rulenodes.append(n)
		return n

	def cover(self, kids) :
		"return the range of input symbols covered by kids"
		if len(kids) > 0 :
			return kids[0].cover[0], kids[-1].cover[1]
		else :
			# epsilon - empty cover at position.
			return self.position,self.position

	def add_rulenode(self, symbolnode, rulenode) :
		if rulenode not in symbolnode.possibilities :
			symbolnode.possibilities.append(rulenode)

	def get_symbolnode(self, s, rulenode) :
		for n in self.symbolnodes :
			if n.sym == s and n.cover == rulenode.cover :
				self.add_rulenode(n, rulenode)
				break
		else :
			n = symnode(s, [rulenode], rulenode.cover)
			self.symbolnodes.append(n)
		return n

