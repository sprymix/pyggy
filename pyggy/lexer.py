#!/usr/bin/python
#
# lexer.py
#	Implements a lexer using precomputed dfa tables.
#

import string
from util import printable
from errors import *

# XXX some constants that must agree with the grammar constants.
# this kis kinda poor right now.  fixme
TOK_ERR = "#ERR#"


class lexer :
	"""
The lexer which returns tokens when token() is called
Pass in a lexer specification consistent of:
     a dfa transition table (indexed by state and character class)
     an acceptance table (indexed by state)
     a list of start state tuples with start states for unanchored and
		anchored lexing.
     a list of actions to be performed, indexed by acceptance number
     a list of actions to be performed in each state when EOF is encountered
     a hash table mapping characters to character class indexes.
Also pass in a list of args for the reader.

When acceptance is reached, an action is called as:

    actionfunc(self) :
        actioncode

self refers to the lexer class.  The action code must return a token
to be returned to the caller of token(), or None if no token is
to be returned (and lexing is to continue).  When the actionfuncis
called, self.value is a string of the characters that have been lexed.
The actionfunc can alter self.value if it wishes to change the
tokens value.


The following methods are meant to be callable from actions:
    PUSHSTATE(statenum) -
       push a new start state on the start state stack
    POPSTATE() -
       return to the previous start state
    PUSHBACK(charlist) -
       push all the characters in the list back on to the input
       stream so that they will be encountered by the lexer when
       lexing continues.
    ENQUEUE(tok, charlist) -
       push a single token and an associated list of characters
       onto the token queue so that the token is returned AFTER
       the currently returned token and before any other tokens
       are lexed.  This can be used to return several tokens
       (ie. several DEDENTS in python) from a single action.

This class can be subclassed to provide lexers on different inputs.
The subclass must provide nextch() and PUSHBACK() methods.
	"""

	# members:
	#	state - the current state of the DFA
	#	startstack - a stack of start state indexes into starts[].  The
	#			top element specifies the current start state for the
	#			next DFA.
	#   starts - an array of tuples of start states.  Tuple specifies
	#			the normal start state as well as the start-of-line start
	#			state.  This array is indexed by the top of the startstack
	#	startofline - true if we're starting a new line when we start lexing
	#	tokqueue - queue of tokens to return before further lexing

	def __init__(self, lexspec) :
		self.rows,self.acc,self.starts,self.actions,self.eofactions,self.chr2ccl = lexspec

		self.startstack = [0]

		assert len(self.rows) == len(self.acc)
		self.tokqueue = []
		self.startofline = 1

	def setinputstr(self, str) :
		self.input = None
		self.buf = list(str)
		self.readbuf()

	def setinput(self, fname) :
		"""
		Set input to come from fname.

		The setinput() and readbuf() methods implement the input reader.
		Override these at will.
		"""
		import sys

		self.fname = fname
		if fname == '-' :
			self.input = sys.stdin
			self.bufsize = 1
		else :
			self.input = file(fname)
			self.bufsize = 1024
		self.readbuf()
		
	def readbuf(self) :
		"fill up the self.buf buffer."
		if self.input :
			self.buf = list(self.input.read(self.bufsize))
		if self.buf == [] :
			self.curch = None
		else :
			self.curch = self.buf[0]

	def nextch(self) :
		"calculate the next character of input"
		self.buf[0:1] = []
		if self.buf == [] :
			self.readbuf()
		else :
			self.curch = self.buf[0]

	def PUSHBACK(self, backupdata) :
		"put data back on the input stream"
		self.buf[0:0] = list(backupdata)
		self.curch = self.buf[0]

	def ENQUEUE(self, tok, data) :
		"enqueue a token to be returned in the future before lexing more"
		self.tokqueue.append((tok, data),)

	def getstartstate(self) :
		"""
		give the start state for starting to lex the next word
		based on whether we're at the start of a line and whats
		on the top of the start state stack.
		"""
		startstate = self.startstack[-1]
		return self.starts[startstate][self.startofline]

	def PUSHSTATE(self, startstateno) :
		"pus a new start state on the stack"
		if startstateno < 0 or startstateno >= len(self.starts) :
			raise ApiError("bad start state")
		self.startstack.append(startstateno)

	def POPSTATE(self) :
		"pop the current start state from the stack"
		if len(self.startstack) <= 1 :
			raise ApiErro("popping empty start state stack")
		val = self.startstack[-1]
		self.startstack[-1:] = []
		return val

	def token(self) :
		"lex out another token"
		# loop until we have something to return.
		while 1 :
			# if we have enqueued tokens, use them first
			if self.tokqueue != [] :
				tok,self.value = self.tokqueue[0]
				self.tokqueue[0:1] = []
				return tok

			# run the EOF action for this state
			if self.curch == None :
				self.value = "<<EOF>>"
				act = self.eofactions[self.startstack[-1]]
				if act != None :
					tok = act(self)
					if tok != None :
						return tok
				else :
					return
				continue

			# keep reading until acceptance
			state = self.getstartstate()
			lastacc = 0
			backupdata = []
			tokdata = ""
			while 1 :
				#print " ", state, printable(self.curch), self.acc[state]
				nextstate = 0
				if self.curch != None :
					ccl = self.chr2ccl[self.curch]
					nextstate = self.rows[state][ccl]
				if nextstate == 0 :
					break
				tokdata += self.curch

				# be prepared to backup if we're leaving an accepting state
				# keep track of characters we will push back
				if len(self.acc[state]) :
					lastacc = state
					backupdata = []
				backupdata.append(self.curch)

				state = nextstate
				self.nextch()

			# return the first acceptance or -1
			tok = None
			if len(self.acc[state]) > 0 :
				acc = self.acc[state][0]
			elif lastacc :
				# backup to a previous accepting state
				tokdata = tokdata[:-len(backupdata)]
				self.PUSHBACK(backupdata)
				acc = self.acc[lastacc][0]
			else :
				acc = None
				tok = TOK_ERR
				if self.curch != None :
					tokdata += self.curch
				self.nextch()

			# XXX this will be set wrong if a PUSHBACK is called.
			# What is the solution here?  Document bug?  Allow PUSHBACK
			# to specifie the startofline value?
			self.startofline = (tokdata[-1] == '\n')

			# perform the action
			self.value = tokdata
			if tok == None :
				tok = self.actions[acc](self)
			if tok != None :
				#print tok, acc, self.startstack, self.value
				return tok
		# end while loop

