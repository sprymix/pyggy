#!/usr/bin/python
#
# slrgram.py
#	Implements functions for building SLR(1) parsing tables
#

from util import printable
import dot

debug = 0

# XXX we should think about using the python set class.

# Add an item to a set represented as a list of items.
# The items must have a __eq__ method
# return the index of the item that was added or already existed
def setadd(set, item) :
	if item in set :
		return set.index(item)
	else :
		set.append(item)
		return len(set) - 1

# add items from set2 into set.
def setaddset(set, set2) :
	for x in set2 :
		setadd(set, x)

# set = set union (add - excl).  Return true if the set grew.
def setsubunion(set, add, excl) :
	changed = 0
	for el in add :
		if not el in excl and not el in set :
			set.append(el)
			changed = 1
	return changed


STARTSYM = "$STARTSYM$"
EOF = "$EOF$"

# The LR(0) state machine for a grammar with restrictions:
#    gram - a list of productions in the form [lhs, [rhslist]]
#    conflict - a dictionary indexed by two productions which specifies
#        the conflict relation between them (ie. "left", "right", "nonassoc"
#        or "gt").  The conflict table should be completely filled out
#        (ie. transitive closure over "gt" should be represented explicitely).
#    followrestrict - a set of symbols that cannot follow each production.
#
# We compute the state machine where each state represents a set of LR(0) items.
# Each state is given a number, starting at 0 for the start state.
# We constuct tables:
#    allsyms[]  - a list of symbols.  Their indices represent them
#    symno[]    - hash table mapping symbols to numbers. XXX deprecate this!
#    nonterms[] - table indexed by symbol numbers specifying if the symbol
#                 is a nonterminal
#    derives[]  - a list of production numbers that each derive each symbol,
#                 indexed by symbol number
#
#    goto[]     - hash table indexed by (statenumber,tr) where tr is
#                 either a terminal or a production number.  The value
#                 is the next state to transition to.
class lr0gram :
	def __init__(self, start, gram, conflict, followrestrict) :
		self.conflict = conflict
		self.gram = gram + [(STARTSYM, [start, EOF])]
		self.folrest = followrestrict + []

		# itemtable is a list of items as (prodno,pos).  itemtable indices
		#   are used to represents items.
		# states is a list of itemsets.  State numbers index states[]
		self.itemtab = []
		self.states = []
		self.goto = None

		self.allsyms = self.syms()
		self.symno = self.symnos()
		self.nonterm = self.nonterms()

		# derives[symno] - list of productions that derive that sym 
		self.derives = [[] for idx in range(len(self.allsyms))]
		for prodno in range(len(self.gram)) :
			lhs = self.gram[prodno][0]
			self.derives[self.symno[lhs]].append(prodno)

		self.makedfa(len(self.gram) - 1)

	# given indexes to two productions (ie. A -> aB, and B -> b) and a position
	# within the first production (ie 1 for the B in A -> aB), return true
	# if expansion of the second production is illegal within the first
	# production due to precedence and associativity rules.
	def hasconflict(self, prod1, pos, prod2) :
		if not self.conflict.has_key((prod1,prod2),) :
			return 0
		rel = self.conflict[prod1,prod2]
		lastpos = len(self.gram[prod1][1]) - 1
		return (rel == "gt") or \
			(pos == 0 and (rel == "right" or rel == "nonassoc")) or \
			(pos == lastpos and (rel == "left" or rel == "nonassoc"))

	# compute symbols in the grammar
	def syms(self) :
		syms = []
		for prod in self.gram :
			setadd(syms, prod[0])
			for rhssym in prod[1] :
				setadd(syms, rhssym)
		syms.sort()
		return syms

	# compute numbers for each symbol in the grammar
	def symnos(self) :
		# make table to get symbol number from symbol
		symno = dict()
		for idx in range(len(self.allsyms)) :
			symno[self.allsyms[idx]] = idx
		return symno

	# compute nonterminals in the grammar
	def nonterms(self) :
		nonterm = [0 for idx in range(len(self.allsyms))]
		for prod in self.gram :
			nonterm[self.symno[prod[0]]] = 1
		return nonterm

	# return a vector of one integer per symbol specifying if that
	# symbol can derive the empty string.
	def nullable(self) :
		# repeat until convergence.
		# For better performance we could find SCC's in the dependency graph
		# and only converge over each SCC.
		symno = self.symno
		nul = [0 for idx in range(len(self.allsyms))]
		converged = 0
		iter = 0
		while not converged :
			iter += 1
			converged = 1
			for prod in self.gram :
				nidx = symno[prod[0]]
				if not nul[nidx] :
					# we're null if all of the RHS is NULL
					for rhsel in prod[1] :
						if not nul[symno[rhsel]] :
							break
					else :
						nul[nidx] = 1
						converged = 0
		if debug :
			print "nullable iters", iter
		return nul

	# compute the first sets for each symbol. 
	# Note: when computing first sets, we do NOT follow epsilons!  This means
	# that first(ABC) does not include follows(C) if nullable(ABC).
	def first(self, nul) :
		# repeat until convergence.
		# For better performance we could find SCC's in the dependency graph
		# and only converge over each SCC.
		nonterm = self.nonterm
		symno = self.symno
		fir = []
		for idx in range(len(self.allsyms)) :
			sym = self.allsyms[idx]
			if nonterm[idx] :
				fir.append([])
			else :
				fir.append([sym])
			
		converged = 0
		iter = 0
		while not converged :
			iter += 1
			converged = 1
			for prod in self.gram :
				# go through RHS adding first info until we hit a nonnullable
				cur = prod[0]
				cursymno = symno[cur]
				for rhsel in prod[1] :
					rhselno = symno[rhsel]
					if nonterm[rhselno] :
						# everything in first[rhselno] is also in first[cursymno]
						for x in fir[rhselno] :
							if x not in fir[cursymno] :
								fir[cursymno].append(x)
								converged = 0
					else :
						if rhsel not in fir[cursymno] :
							fir[cursymno].append(rhsel)
							converged = 0
					if not nul[rhselno] :
						break
		for el in fir :
			el.sort()
		if debug :
			print "first iters:", iter
		return fir

	# compute the follows sets for each production
	def follows(self, nul, fir) :
		# we're going to compute the following:
		#    fol[prodno]  - follow set for a production
		#
		# in the process we'll use:
		#    fir[sym]     - the first set for a symbol w/o following epsilons
		#    nul[sym]     - wether symbol can derive epsilon
		#    derives[sym] - list of productions that derive that sym 

		# repeat until convergence.
		fol = [[] for idx in range(len(self.gram))]
		symno = self.symno
		converged = 0
		iter = 0
		while not converged :
			iter += 1
			converged = 1

			for prodno in range(len(self.gram)) :
				prod = self.gram[prodno]

				# walk backwards through the rhs adding follows
				rhs = self.gram[prodno][1]
				folset = fol[prodno][:]
				for idx in range(len(rhs)) :
					pos = len(rhs) - idx - 1
					cur = rhs[pos]
					cursymno = symno[cur]
					for prodno2 in self.derives[cursymno] :
						# follows of all productions deriving cursym include 
						# folset unless they were explicitely disallowed by a 
						# "does not follow" restriction.
						if not self.hasconflict(prodno, pos, prodno2) :
							if setsubunion(fol[prodno2], folset, self.folrest[prodno2]) :
								#print prodno2, "add", folset, "to", self.gram[prodno2], "because", self.gram[prodno][0], "->", self.gram[prodno][1][:pos] + [self.gram[prodno2][1]] + self.gram[prodno][1][pos+1:]
								converged = 0
					# next folset is first(cursym) + (folset if sym is nullable)
					if not nul[cursymno] :
						folset = []
					setsubunion(folset, fir[cursymno], [])

		for el in fol :
			el.sort()
		if debug :
			print "follows iters:", iter
		return fol

	# see if we have this item in our table yet, and if not, add it.
	# return the index of the item in our itemtab.
	def makeitem(self, prodno, pos) :
		prod = self.gram[prodno]
		if pos >= len(prod[1]) :
			pos = -1
		item = (prodno,pos)
		return setadd(self.itemtab, item)

	# Return a printable string for an item.
	def itemstr(self, itnum) :
		prodno,pos = self.itemtab[itnum]
		prod = self.gram[prodno]
		str = "(%d) %s ->" % (prodno, prod[0])
		for idx in range(len(prod[1])) :
			if idx == pos :
				str += " ."
			str += " " + prod[1][idx]
		if pos == -1 :
			str += " ."
		return str

	# Add all predicted items to the current itemset
	def itemsetclosure(self, itset) :
		# add items for all predicted symbols.
		symno = self.symno
		for itnum in itset :
			prodno,pos = self.itemtab[itnum]
			if pos != -1 :
				predsym = self.gram[prodno][1][pos]
				for prodno2 in self.derives[symno[predsym]] :
					if not self.hasconflict(prodno, pos, prodno2) :
						setadd(itset, self.makeitem(prodno2, 0))
		itset.sort()

	def findstate(self, itemset) :
		if len(itemset) == 0 :
			return -1
		self.itemsetclosure(itemset)
		return setadd(self.states, itemset)

	# compute the LR0 states and the goto[] transitions.
	# We build up a table of states in self.states.  Each state
	#   represents a set of items (represented as a sorted list of item nums).
	# And a goto table which is a hash table indexed by (statenum,termsym)
	#   or (statenum,prodnum)
	#
	# note: There are no transitions on non-terminals (as is traditional)
	# but rather on production numbers.  This facilitates disambiguation
	# based on priorities.
	def makedfa(self, startprod) :
		# make the starting state
		set0 = []
		set0.append(self.makeitem(startprod, 0))
		self.findstate(set0)

		# compute terminals we transition on
		term = []
		for sym in self.allsyms :
			if sym != EOF and not self.nonterm[self.symno[sym]] :
				term.append(sym)

		# keep adding transitions from the known states until done.
		self.goto = dict()
		idx = 0
		while idx < len(self.states) :
			curset = self.states[idx]

			# compute transitions for each terminal (except EOF)
			for sym in term :
				nextset = []
				for itnum in curset :
					prodno,pos = self.itemtab[itnum]
					if pos != -1 and sym == self.gram[prodno][1][pos] :
						nextset.append(self.makeitem(prodno, pos + 1))
				if nextset != [] :
					self.goto[idx,sym] = self.findstate(nextset)

			# compute transitions for each production
			for prodno2 in range(len(self.gram)) :
				lhs = self.gram[prodno2][0]
				nextset = []
				for itnum in curset :
					prodno,pos = self.itemtab[itnum]
					if pos != -1 and lhs == self.gram[prodno][1][pos] and \
							not self.hasconflict(prodno, pos, prodno2) :
						nextset.append(self.makeitem(prodno, pos + 1))
				if nextset != [] :
					self.goto[idx,prodno2] = self.findstate(nextset)

			idx += 1
		# end loop over each state

	# string for a production
	def prodstr(self, prodno, quoted = 0, bracketted=1) :
		str = ""
		if bracketted :
			str += "["
		str += "(%d) %s ->" % (prodno, self.gram[prodno][0])
		for el in self.gram[prodno][1] :
			str += " "
			str += printable(el, quoted)
		if bracketted :
			str += "]"
		return str

	def dot(self) :
		d = dot.dot("LR0")
		for idx in range(len(self.states)) :
			label = "State %d" % idx
			for itnum in self.states[idx] :
				label += "\\n" + self.itemstr(itnum)
			d.add("    %d [label=\"%s\",shape=box];" % (idx, label))

			# make names for transitions to each next state
			name = ["" for st in range(len(self.states))]
			for (st,tr),ns in self.goto.items() :
				if st != idx :
					continue
				if name[ns] != "" :
					name[ns] += ", "
				if isinstance(tr, str) :
					name[ns] += printable(tr, 1)
				else :
					name[ns] += self.prodstr(tr, 1)

			# print all transitions that have names
			for ns in range(len(name)) :
				if name[ns] != "" :
					d.add("    %d -> %d [label=\"%s\"];" % (idx, ns, name[ns]))
		d.end()
		d.show()
			
	def printtab(self) :
		print "Shifts"
		for idx in range(len(self.states)) :
			print "State %3d:" % idx,
			for (st,tr),ns in self.goto.items() :
				if st != idx :
					continue
				if isinstance(tr, str) :
					name = printable(tr)
				else :
					name = self.prodstr(tr)
				print "  on %s goto %d" % (name, ns)
			print
		print

# An SLR grammar with some conflict resolution
# Takes in the same arguments as an lr0gram and builds up a table 
# of shift-reduce actions:
#    action[] - indexed by (state number, symbol), and gives a list
#               of actions in the form:
#                    ("shift", nextstate)
#                    ("reduce", (lhs sym, rhs length, production number))
#                    ("accept", None)
class slrgram : 
	def __init__(self, start, gram, conflict, followrestrict) :
		self.lr0 = lr0gram(start, gram, conflict, followrestrict)
		self.maketabs(debug)

	# helper for debug output
	def _printbools(self, title, boollist, names, val = 1) :
		print title + ":",
		for idx in range(len(names)) :
			if (boollist[idx] != 0) == val :
				print names[idx],
		print

	# helper for debug output
	def _printsets(self, title, setlist, names) :
		print title + ":"
		for idx in range(len(names)) :
			if setlist[idx] != [] :
				print "  %s:" % str(names[idx]),
				for el in setlist[idx] :
					print el,
				print

	def addaction(self, st, sym, act) :
		if not self.action.has_key((st,sym),) :
			self.action[st,sym] = []
		self.action[st,sym].append(act)

	# return a list of the productions that caused an action
	def actionprods(self, state, sym, action, follows) :
		prods = []
		for itnum in self.lr0.states[state] :
			prodno,pos = self.lr0.itemtab[itnum]
			if pos == -1 :
				if action[0] == "reduce" and sym in follows[prodno] :
					prods.append(prodno)
			else :
				if action[0] == "shift" and self.lr0.gram[prodno][1][pos] == sym :
					prods.append(prodno)
		return prods

	# return true if we can eliminate the action caused by actprods[idx]
	# because all other actions are preferred.  Also return a second
	# boolean that specifies wether some precedences came into play.
	def caneliminate(self, actprod, idx) :
		cnt,prefcnt = 0,0
		for idx2 in range(len(actprod)) :
			if idx == idx2 :
				continue
			for prod2 in actprod[idx2] :
				for prod1 in actprod[idx] :
					cnt += 1
					if self.lr0.conflict.has_key((prod2,prod1),) and \
							self.lr0.conflict[prod2,prod1] == "pref" :
						prefcnt += 1
		return (prefcnt == cnt), (prefcnt > 0)

	def maketabs(self, printprops = 0) :
		# compute some properties of the grammar
		symno = self.lr0.symno
		nonterm = self.lr0.nonterm
		nul = self.lr0.nullable()
		first = self.lr0.first(nul)
		follows = self.lr0.follows(nul, first)
		self.follows = follows
		if printprops :
			self._printbools("Nonterminals", nonterm, self.lr0.allsyms)
			self._printbools("Terminals", nonterm, self.lr0.allsyms, 0)
			self._printbools("Nullables", nul, self.lr0.allsyms)
			self._printsets("First", first, self.lr0.allsyms)
			self._printsets("Follows", follows, self.lr0.gram)
			print

		# get shifts from goto table transitions on terminals
		self.action = dict()
		for (st,tr),ns in self.lr0.goto.items() :
			if not isinstance(tr, str) :
				continue
			self.addaction(st, tr, ("shift", ns))

		# get reductions from itemsets for each state
		for idx in range(len(self.lr0.states)) :
			for itnum in self.lr0.states[idx] :
				prodno,pos = self.lr0.itemtab[itnum]
				lhs,rhs = self.lr0.gram[prodno]
				lhsno = symno[lhs]
				if pos == -1 :
					for sym in follows[prodno] :
						self.addaction(idx, sym, ("reduce", (lhs, len(rhs), prodno)))
				elif rhs[pos] == EOF :
					self.addaction(idx, EOF, ("accept", None))

		# resolve conflicts using the "pref" relation
		for (st,sym),actlist in self.action.items() :
			if len(actlist) < 2 :
				continue
			actprods = []
			for act in actlist :
				actprods.append(self.actionprods(st, sym, act, follows))

			# keep eliminating actions when other actions are preferred
			somepref = 0
			while len(actlist) > 1 :
				actlist2 = []
				actprods2 = []
				for idx in range(len(actlist)) :
					elim,sp = self.caneliminate(actprods, idx)
					if not elim :
						somepref = somepref or sp
						actlist2.append(actlist[idx])
						actprods2.append(actprods[idx])
					#else : print "eliminate %s on %s in state %d" % (actlist[idx], sym, st)
				if actlist == actlist2 :
					break
				actlist = actlist2
				actprods = actprods2
			self.action[st,sym] = actlist
			if somepref :
				print "Warning - preferences in state %d could not eliminate ambiguity" % st

	def printtab(self, full = 0) :
		if full :
			print "Grammar:"
			for idx in range(len(self.lr0.gram)) :
				print " ", self.lr0.prodstr(idx, bracketted=0)

		nstates = len(self.lr0.states)
		ambig = 0
		for idx in range(len(self.lr0.states)) :
			if full :
				print "State %d:" % idx
				for itnum in self.lr0.states[idx] :
					prodno,pos = self.lr0.itemtab[itnum]
					print "  ", self.lr0.itemstr(itnum), "   ", 
					if pos == -1 :
						print "follows:", self.follows[prodno],
					print

				# print gotos of productions
				for (st,tr),ns in self.lr0.goto.items() :
					if st != idx or isinstance(tr, str) :
						continue
					name = self.lr0.prodstr(tr)
					print "      on %s: goto %s" % (name, ns)

			# print actions and count ambiguities
			for (st,tr),actions in self.action.items() :
				if st != idx :
					continue
				if len(actions) > 1 :
					ambig += len(actions) - 1
					pref = "! "
				else :
					pref = ""
				if full :
					for act in actions :
						print "      %son %s: %s %s" % (pref, tr, act[0], act[1])
			if full :
				print
		if ambig :
			print "%d Ambiguities" % ambig

	# write out tables needed for parsing
	def write(self, f) :
		f.write('goto = %s\n' % self.lr0.goto)
		f.write('action = %s\n' % self.action)

