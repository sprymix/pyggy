#!/usr/bin/python
#
# srgram.py
#	Implements a class for encapsulating Shift-Reduce tables.
#

# Directions on how to drive an LR parser suitable for passing to a 
# shift-reduce parser.
class SRGram :
	def __init__(self, srspec) :
		self.gototab,self.acttab,self.func = srspec
		self.start = 0

	def action(self, state, tok) :
		if self.acttab.has_key((state,tok),) :
			return self.acttab[state,tok]
		return []
		
	def goto(self, state, prodno) :
		if self.gototab.has_key((state,prodno),) :
			return self.gototab[state,prodno]
		return None

	def reducefunc(self, prodno, kids) :
		if self.func[prodno] == None :
			return kids
		return self.func[prodno](kids)

