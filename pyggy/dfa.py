#!/usr/bin/python
#
# dfa.py
#	Routines for building a DFA from multiple NFA's.
#

import string

from util import printable
from nfa import *
import dot

class dfa :
	def __init__(self, machlist, relist) :
		self.relist = relist

		self.maxchar = 255
		self.dfastate = []
		self.rows = None
		self.acc = None
		self.nfa = machlist[0][0].nfa
		self.uccls = None
		self.chr2uccl = None
		self.uniqueccls()
		self.convertnfa(machlist)
		# XXX maybe perform DFA minimization some day?

	# Lookup a DFA state corresponding to a (sorted) set of NFA states.
	# If no DFA state yet exists, create one to represent the set.
	#
	# Each DFA state is represented by an integer and the acceptance set.
	# A table indexed by DFA state number holds the NFA state set and
	# the acceptance set for each dfa state.
	#
	# XXX a bunch of time is wasted in this function.  Need to make it
	# more efficient somehow.  A hash lookup would help.
	def GetDFAState(self, stateset) :
		for idx in range(len(self.dfastate)) :
			# find state.
			# XXX Linear search should be replaced by a hashed lookup
			# we can compute the hash while computing epsilonclosure .
			set2,accset = self.dfastate[idx]
			if stateset == set2 :
				break
		else :
			# nothing found, create a new DFA state for this set.
			idx = len(self.dfastate)

			# compute the acceptance for this dfa state
			accset = []
			for s in stateset :
				if self.nfa.states[s][3] != NOACCEPT :
					accset.append(self.nfa.states[s][3])
			self.dfastate.append((stateset, accset),)
		return idx

	# If nfa state nstate is not yet marked, mark it and append it to set
	def markandappend(self, nstate, set) :
		# I tried to make this faster but since the lists are often
		# small, going more complicated doesnt buy much.
		if not nstate in set :
			set.append(nstate)
	
	# Given a set of marked NFA states (possibly with duplicates), compute the
	# epsilon closure of the set (ie. all states reachable from those 
	# states without consuming any input) and then lookup the DFA state
	# which represents that set of NFA states.  If no such state exists,
	# create it.
	#
	# The input set nstates is destroyed by this call, and the marked
	# states are all unmarked.
	# 
	# This algorithm is taken directly from flex since it was quite elegant.
	def ClosureMarkedAndGetDFAState(self, nstates) :
		# add anything reachable via epsilon from something in workset,
		# if its not yet marked.
		for s in nstates :
			trset,next1,next2,acc = self.nfa.states[s]
			if trset == EPSILON :
				if next1 != NOSTATE :
					self.markandappend(next1, nstates)
				if next2 != NOSTATE :
					self.markandappend(next2, nstates)
		# unmark all the marked states:  we no longer have to do this
		# with our current markandappend routine.  If we change marking
		# we will have to unmark states here.

		# sort and lookup or create a dfa state for this set
		nstates.sort()
		return self.GetDFAState(nstates)

	# Perform closure and return DFA state represented by the closed set.
	# This function takes an unmarked set of nfa states (possibly with
	# duplicates).  
	# See the comments for ClosureMarkedAndGetDFAState() for more details.
	def ClosureAndGetDFAState(self, nstates) :
		# start of with states, mark them all
		workset = []
		for s in nstates :
			self.markandappend(s, workset)
		return self.ClosureMarkedAndGetDFAState(workset)

	# return the dfa state reachable from state via transitions on ucclval.
	def trans(self, state, uccl) :
		transet = []
		stateset,accset = self.dfastate[state]
		for s in stateset :
			trset,next1,next2,acc = self.nfa.states[s]
			if trset in uccl :
				self.markandappend(next1, transet)
		return self.ClosureMarkedAndGetDFAState(transet)

	# compute all transitions from a dfa state represented as set of nfa states
	def alltrans(self, dstate) :
		res = []
		for uccl in self.uccls :
			dstate2 = self.trans(dstate, uccl)
			res.append(dstate2)
		return res

	# compute the non-overlapping character classes required by our lexer.
	def uniqueccls(self) :
		# compute the set of ccl's that contain each character and
		# make a uccl for that set.
		uccls = []
		chr2uccl = dict()
		for cval in range(0, self.maxchar + 1) :
			set = []
			for ccl in range(len(self.nfa.chset)) :
				if self.nfa.chsetcontains(ccl, cval) :
					set.append(ccl)
			if not set in uccls :
				idx = len(uccls)
				uccls.append(set)
			else :
				idx = uccls.index(set)
			chr2uccl[chr(cval)] = idx
		self.uccls = uccls
		self.chr2uccl = chr2uccl

	# Given an NFA machine, return a transition table for an equivalent
	# DFA machine, and a list of acceptances for each state.
	# machnoanchor specifies the start state when not starting at the
	# beginning of a line.  It may be None.
	def convertnfa(self, machlist) :
		errstate = self.ClosureAndGetDFAState([])
		assert errstate == 0

		# Build all start states
		starts = []
		for mach,machnoanchor in machlist :
			start1 = errstate
			if machnoanchor != None :
				start1 = self.ClosureAndGetDFAState([machnoanchor.start])
			start2 = self.ClosureAndGetDFAState([mach.start])
			starts.append((start1, start2),)
		
		# Create transitions from each state
		rows = []
		acc = []
		idx = 0
		while idx < len(self.dfastate) :
			sset,accset = self.dfastate[idx]
			row = self.alltrans(idx)
			rows.append(row)
			acc.append(accset)
			idx += 1
		self.rows = rows
		self.acc = acc
		self.starts = starts

	# display graph using dot
	def dot(self, shownfastates = 0, showccls = 0) :
		if showccls :
			# make names for the character classes so we dont repeat this often
			cclname = ["" for idx in range(len(self.uccls))]
			ch = 0
			while ch < self.maxchar + 1 :
				minch = ch
				curccl = self.chr2uccl[chr(ch)]
				while ch < self.maxchar + 1 and self.chr2uccl[chr(ch)] == curccl :
					ch += 1
				maxch = ch - 1
				if cclname[curccl] != "" :
					cclname[curccl] += ", "
				cclname[curccl] += printable(chr(minch), 1)
				if minch < maxch :
					cclname[curccl] += "-" + printable(chr(maxch), 1)

		d = dot.dot("dfa")
		for idx in range(1, len(self.rows)) :
			xtra = ""
			name = "%d" % idx
			if shownfastates :
				name += ": %s" % self.dfastate[idx][0]
			if len(self.acc[idx]) > 0 :
				name += " acc%s" % self.acc[idx]
				xtra += ", color=red"
			cnt = 0
			for s1,s2 in self.starts :
				if idx == s1 or idx == s2 :
					xtra += ", color=red"
				if idx == s1 :
					name += "\\nstart %d" % cnt
				if idx == s2 :
					name += "\\nstart ^%d" % cnt
				cnt += 1
			d.add("    n%d [label=\"%s\"%s];" % (idx, name, xtra))

			# make one arc to each reachable next state
			# this graph most accurately portrays the table we build, but
			# is sometimes hard to read.  perhaps we should have an option
			# for collecting the character classes for the edge into a single
			# character class and then converting that to a string.
			for ns in range(1, len(self.rows)) :
				ccls = []
				for ccl in range(len(self.rows[idx])) :
					if self.rows[idx][ccl] == ns :
						ccls.append(ccl)
				if ccls == [] :
					continue

				name = ""
				if showccls : # build up name out of each ccl
					for ccl in ccls :
						if name != "" :
							name += "\\n"
						name += "%d: %s" % (ccl, cclname[ccl])
				else : # build up name out of the combined ccl
					ch = 0
					while ch < self.maxchar + 1 :
						minch = ch
						while ch < self.maxchar + 1 and self.chr2uccl[chr(ch)] in ccls :
							ch += 1
						maxch = ch - 1
						if maxch < minch :
							ch += 1
							continue
						if name != "" :
							name += ", "
						name += printable(chr(minch), 1)
						if maxch > minch :
							name += "-" + printable(chr(maxch), 1)
				d.add("    n%d -> n%d [label=\"%s\"];" % (idx, ns, name))
		d.show()

	# warn of any ambiguities and backup potentials
	def sanity(self, printfull = 1) :
		for idx in range(len(self.starts)) :
			s1,s2 = self.starts[idx]
			if len(self.acc[s1]) > 0 or len(self.acc[s2]) > 0 :
				print "Removing acceptance of the empty string from starstate %d!" % idx
				self.acc[s1] = []
				self.acc[s2] = []

		ambig = 0
		for idx in range(len(self.rows)) :
			r = self.rows[idx]
			accset = self.acc[idx]
			doprint = 0
			if len(accset) > 1 :
				if printfull :
					print "ambiguous accept in state %d:" % idx
					doprint = 1
				ambig += 1
			if len(accset) > 0 :
				nonacc = []
				for ns in r :
					if ns and len(self.acc[ns]) == 0 :
						if not ns in nonacc :
							nonacc.append(ns)
				if len(nonacc) > 0 and printfull :
					print "backing up may be necessary from %d to: %s" % (idx, nonacc)
					doprint = 1
			if doprint :
				for a in accset :
					print "  pattern %d: %s" % (a, self.relist[a])
					# XXX would be nice to print the rules that we would
					# be backing up from!
		if ambig > 0 :
			print "%d ambiguities exist in the lexer." % ambig

	# write the tables for the machine out to fname
	def write(self, f) :
		f.write('rows = [ \n')
		for r in self.rows :
			f.write("  %s,\n" % r)
		f.write("]\n")
		f.write('acc = %s\n' % self.acc)
		f.write('starts = %s\n' % self.starts)
		f.write('chr2uccl = %s\n' % self.chr2uccl)

