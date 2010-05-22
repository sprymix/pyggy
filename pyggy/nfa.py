#!/usr/bin/python
#
# nfa.py
#	Construction kit for building up NFAs for regular expressions.
#

import dot
import string
import array

from util import printable,minof,maxof

# Constants
EPSILON = 0
NOSTATE = 0
NOACCEPT = 0
nchars = 256


# A sub-machine of an NFA.  We store all states sequentially, so
# the min and max completely determines the set of states. 
class nfamach :
	def __init__(self, nfa, start, end, min, max) :
		assert end == NOSTATE or nfa.states[end][0] == EPSILON
		self.nfa = nfa
		self.start = start
		self.end = end
		self.min = min
		self.max = max


# Like Flex, we build an NFA with each node having either one or two
# epsilon transitions out, or having a single non-epsilon transition out.
#
# Each node is represented by an index (its node number) and a tuple:
#   (transition character set, next state1, next state2, accept index)
# If transition character set is not epsilon, next state2 is not used.
#
# transition character refers to an index into a table of all sets.
#
# This is the first cut, efficiency is sacrified for simplicity.
# Ideally we'd use efficient arrays of fixed type here.
class nfa :
	# variables
	#   self.states - list of [trset, ns1, ns2, acc] indexed by node number

	def __init__(self) :
		# make a dummy state for state zero == NOSTATE
		self.states = [None]

		self.chsethash = dict()
		self.chset = []
		self.getorcreateset([]) # make EPSILON set at index 0

	# Create or make a character set class.  chset should already be
	# in sorted order.  Register this set and return it.
	# We use an index to represent the set, and a hash table to lookup
	# a set by its members.  The hash is the length of the set which makes
	# comparisons simpler at the expense of unbalanced buckets.
	def getorcreateset(self, elements) :
		# find existing character class and return it
		hash = len(elements)
		if self.chsethash.has_key(hash) :
			for idx in self.chsethash[hash] :
				if self.chset[idx] == elements :
					return idx
		else :
			self.chsethash[hash] = []

		# no match, make a new one
		idx = len(self.chset)
		self.chset.append(elements)
		self.chsethash[hash].append(idx)
		return idx

	# return a printable name for the character set
	# this is inefficient but who cares?
	def chsetname(self, ccl, quoted = 0) :
		if ccl == EPSILON :
			return "epsilon"
		set = []
		idx = 0
		while idx < 256 :
			if self.chsetcontains(ccl, idx) :
				start = idx
				idx += 1
				while idx < 256 and self.chsetcontains(ccl, idx) :
					idx += 1
				if idx > start + 1 :
					set.append("%s-%s" % (printable(chr(start), quoted), printable(chr(idx - 1), quoted)))
				else :
					set.append("%s" % printable(chr(start), quoted))
			idx += 1
		return string.join(set, ", ")

	# Does character set contain trchr?
	def chsetcontains(self, ccl, chrval) :
		return chr(chrval) in self.chset[ccl]

	# print out the graph for mach, or the entire graph if mach not given
	def dot(self, mach) :
		d = dot.dot("nfa")
		d.add("    rankdir = LR;");
		for idx in range(mach.min, mach.max + 1) :
			trset, tr1, tr2, acc = self.states[idx]
			name = "%d" % idx
			if acc != NOACCEPT :
				name = "accept %d" % acc
			extra = ""
			if idx == mach.start :
				extra = ",color=red"
			d.add("    n%d [label=\"%s\"%s];" % (idx, name, extra))

			name = self.chsetname(trset, 1)
			if tr1 != NOSTATE :
				d.add("    n%d -> n%d [label=\"%s\"];" % (idx, tr1, name))
			if tr2 != NOSTATE :
				d.add("    n%d -> n%d [label=\"%s\"];" % (idx, tr2, name))
		d.end()
		d.show()
			
	# Adds a new state with an out transition on trset
	# returns:	integer - the node number
	def addstate(self, trset) :
		self.states.append([trset, NOSTATE, NOSTATE, NOACCEPT])
		return len(self.states) - 1

	# Adds a transition out
	# returns:  None
	def addtran(self, idx, next) :
		trset,next1,next2,acc = self.states[idx]
		assert next2 == NOSTATE and (trset == EPSILON or next1 == NOSTATE)
		if next1 == NOSTATE :
			self.states[idx][1] = next
		else :
			self.states[idx][2] = next

	# return a singleton machine
	def singmach(self, chset) :
		setnum = self.getorcreateset(chset)
		start = self.addstate(setnum)
		end = self.addstate(EPSILON)
		self.addtran(start, end)
		return nfamach(self, start, end, start, end)

	# Concatenates two machines.  Mach1 is optional (may be None)
	def catmach(self, mach1, mach2) :
		if mach1 == None :
			return mach2
		self.addtran(mach1.end, mach2.start)
		return nfamach(self, mach1.start, mach2.end, 
						minof(mach1.min, mach2.min), 
						maxof(mach1.max, mach2.max))

	# Accept either mach1 or mach2.  Mach1 is optional (may be None)
	def altmach(self, mach1, mach2) :
		if mach1 == None :
			return mach2
		start = self.addstate(EPSILON)
		end = self.addstate(EPSILON)
		self.addtran(start, mach1.start)
		self.addtran(start, mach2.start)
		self.addtran(mach1.end, end)
		self.addtran(mach2.end, end)
		return nfamach(self, start, end, 
						minof(mach1.min, mach2.min), end)

	# positive closure of mach.  Alters the input machine.
	def posclosmach(self, mach) :
		trset,next1,next2,acc = self.states[mach.end]
		if next1 == NOSTATE or next2 == NOSTATE :
			self.addtran(mach.end, mach.start)
			return mach
		end = self.addstate(EPSILON)
		self.addtran(mach.end, end)
		self.addtran(end, mach.start)
		mach.end = end
		return mach

	# make a machine optional.  Alters the input machine
	def optmach(self, mach) :
		start = self.addstate(EPSILON)
		end = self.addstate(EPSILON)
		self.addtran(start, mach.start)
		self.addtran(mach.end, end)
		self.addtran(start, end)
		return nfamach(self, start, end, mach.min, end)

	# optional closre of mach.  Alters the input machine
	def starclosmach(self, mach) :
		mach = self.posclosmach(mach)		# modifies mach
		return self.optmach(mach)

	def setaccept(self, mach, accno) :
		assert self.states[mach.end][3] == NOACCEPT
		self.states[mach.end][3] = accno

	# copy a machine
	# all states in the machine are sequential.
	def copymach(self, mach) :
		assert mach.min != NOSTATE and mach.max != NOSTATE and mach.start != NOSTATE and mach.end != NOSTATE
		off = len(self.states) - mach.min
		for idx in range(mach.min, mach.max + 1) :
			trchr,ns1,ns2,acc = self.states[idx]
			assert acc == NOACCEPT
			if ns1 != NOSTATE :
				ns1 += off
			if ns2 != NOSTATE :
				ns2 += off
			self.states.append([trchr, ns1, ns2, acc],)
		return nfamach(self, mach.start + off, mach.end + off, mach.min + off, mach.max + off)

	# start from the same start state and then go off into one of the
	# machines (but do not rejoin when done).  
	# Mach1 is optional (may be None).
	# This primative does not build a machine with a single end state!
	def dualmach(self, mach1, mach2) :
		if mach1 == None :
			return mach2
		start = self.addstate(EPSILON)
		self.addtran(start, mach1.start)
		self.addtran(start, mach2.start)
		return nfamach(self, start, NOSTATE,
						minof(mach1.min, mach2.min), start)

