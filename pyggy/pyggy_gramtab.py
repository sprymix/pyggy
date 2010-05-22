
# This file was generated automatically

# action 0 for: [(0) gram -> line], [(1) gram -> line gram]
def action0(kids) :
	return kids

# action 1 for: [(2) line -> precoper idlist TOK_END]
def action1(kids) :
	prec = kids[0]
	for id in kids[1] :
	        if prec == "%left" :
	                leftlist.append(id)
	                preclist.append(id)
	        elif prec == "%right" :
	                rightlist.append(id)
	                preclist.append(id)
	        elif prec == "%nonassoc" :
	                nonassoclist.append(id)
	                preclist.append(id)
	        elif prec == "%gt" :
	                preclist.append(id)
	        elif prec == "%pref" :
	                preflist.append(id)
	        else :
	                raise InternalError("cant happen")
	

# action 2 for: [(3) line -> TOK_REL TOK_ID precoper TOK_ID TOK_END]
def action2(kids) :
	prec = kids[2]
	if prec == "%left" :
	        name = "left"
	elif prec == "%right" :
	        name = "right"
	elif prec == "%nonassoc" :
	        name = "nonassoc"
	elif prec == "%gt" :
	        name = "gt"
	elif prec == "%pref" :
	        name = "pref"
	else :
	        raise InternalError("cant happen")
	rellist.append((kids[1],name,kids[3]),)
	

# action 3 for: [(4) line -> TOK_ID TOK_DERIVES rhslist TOK_END]
def action3(kids) :
			# process the AST's we built up for the RHS's
	global start
	sym = procrhslist(kids[0], kids[2])
	if start is None :
	        start = sym
	

# action 4 for: [(5) line -> TOK_CODE TOK_SRCCODE]
def action4(kids) :
	global globcode
	globcode += kids[1]
	

# action 5 for: [(6) precoper -> TOK_LEFT]
def action5(kids) :
	return kids[0]
	

# action 6 for: [(7) precoper -> TOK_RIGHT]
def action6(kids) :
	return kids[0]
	

# action 7 for: [(8) precoper -> TOK_NONASSOC]
def action7(kids) :
	return kids[0]
	

# action 8 for: [(9) precoper -> TOK_PREF]
def action8(kids) :
	return kids[0]
	

# action 9 for: [(10) precoper -> TOK_GT]
def action9(kids) :
	return kids[0]
	

# action 10 for: [(11) rhslist -> optprec rhsellist optcode]
def action10(kids) :
	return [Rhs(*kids)]
	

# action 11 for: [(12) rhslist -> rhslist TOK_ALT optprec rhsellist optcode]
def action11(kids) :
	kids[0].append(Rhs(*kids[2:]))
	return kids[0]
	

# action 12 for: [(13) optcode -> TOK_SRCCODE]
def action12(kids) :
	return kids[0]
	

# action 13 for: [(14) optcode ->]
def action13(kids) :
	return
	

# action 14 for: [(15) rhsellist -> rhsellist rhsel]
def action14(kids) :
	kids[0].append(kids[1])
	return kids[0]
	

# action 15 for: [(16) rhsellist ->]
def action15(kids) :
	return []
	

# action 16 for: [(17) rhsel -> TOK_ID]
def action16(kids) :
	return RhsEl(kids[0])
	

# action 17 for: [(18) rhsel -> TOK_OPAREN rhslist TOK_CPAREN]
def action17(kids) :
	return RhsEl(kids[1], 'list')
	

# action 18 for: [(19) rhsel -> rhsel TOK_STAR]
def action18(kids) :
	return RhsEl(kids[0], '*')
	

# action 19 for: [(20) rhsel -> rhsel TOK_PLUS]
def action19(kids) :
	return RhsEl(kids[0], '+')
	

# action 20 for: [(21) rhsel -> rhsel TOK_OPTIONAL]
def action20(kids) :
	return RhsEl(kids[0], '?')
	

# action 21 for: [(22) idlist -> idlist TOK_ID]
def action21(kids) :
	kids[0].append(kids[1])
	return kids[0]
	

# action 22 for: [(23) idlist ->]
def action22(kids) :
	return []
	

# action 23 for: [(24) optprec -> TOK_PREC TOK_OPAREN TOK_ID TOK_CPAREN]
def action23(kids) :
	return kids[2]
	

# action 24 for: [(25) optprec ->]
def action24(kids) :
	return None
	
goto = {(0, 'TOK_REL'): 7, (0, 'TOK_RIGHT'): 8, (18, 'TOK_ALT'): 24, (14, 'TOK_LEFT'): 4, (28, 'TOK_CPAREN'): 36, (20, 'TOK_ID'): 27, (31, 12): 38, (31, 11): 38, (24, 'TOK_PREC'): 17, (0, 10): 11, (0, 8): 11, (0, 9): 11, (0, 2): 10, (0, 3): 10, (0, 0): 9, (0, 1): 9, (0, 6): 11, (0, 7): 11, (0, 4): 10, (0, 5): 10, (0, 'TOK_PREF'): 6, (0, 'TOK_NONASSOC'): 5, (26, 'TOK_OPAREN'): 31, (24, 24): 29, (24, 25): 29, (14, 'TOK_GT'): 2, (31, 'TOK_PREC'): 17, (3, 'TOK_DERIVES'): 13, (37, 'TOK_ID'): 30, (16, 'TOK_END'): 21, (38, 'TOK_CPAREN'): 43, (10, 'TOK_RIGHT'): 8, (34, 'TOK_STAR'): 41, (10, 'TOK_REL'): 7, (10, 4): 10, (10, 5): 10, (10, 6): 11, (10, 7): 11, (0, 'TOK_CODE'): 1, (10, 1): 15, (10, 2): 10, (10, 3): 10, (10, 8): 11, (10, 9): 11, (10, 10): 11, (26, 20): 34, (26, 21): 34, (26, 17): 34, (26, 18): 34, (26, 19): 34, (26, 13): 33, (26, 14): 33, (10, 'TOK_NONASSOC'): 5, (37, 'TOK_SRCCODE'): 32, (10, 'TOK_PREF'): 6, (18, 'TOK_END'): 25, (11, 23): 16, (11, 22): 16, (26, 'TOK_ID'): 30, (27, 'TOK_END'): 35, (10, 'TOK_LEFT'): 4, (34, 'TOK_PLUS'): 40, (13, 'TOK_PREC'): 17, (19, 16): 26, (37, 13): 42, (37, 14): 42, (26, 'TOK_SRCCODE'): 32, (37, 21): 34, (37, 20): 34, (37, 17): 34, (37, 19): 34, (37, 18): 34, (19, 15): 26, (16, 'TOK_ID'): 22, (10, 'TOK_GT'): 2, (34, 'TOK_OPTIONAL'): 39, (31, 25): 19, (7, 'TOK_ID'): 14, (10, 'TOK_CODE'): 1, (13, 12): 18, (17, 'TOK_OPAREN'): 23, (13, 11): 18, (23, 'TOK_ID'): 28, (0, 'TOK_ID'): 3, (13, 25): 19, (13, 24): 19, (31, 24): 19, (1, 'TOK_SRCCODE'): 12, (29, 16): 37, (29, 15): 37, (0, 'TOK_LEFT'): 4, (14, 'TOK_RIGHT'): 8, (38, 'TOK_ALT'): 24, (14, 6): 20, (14, 7): 20, (14, 8): 20, (14, 9): 20, (14, 10): 20, (37, 'TOK_OPAREN'): 31, (14, 'TOK_PREF'): 6, (14, 'TOK_NONASSOC'): 5, (10, 0): 15, (0, 'TOK_GT'): 2, (10, 'TOK_ID'): 3}
action = {(43, 'TOK_OPAREN'): [('reduce', ('rhsel', 3, 18))], (39, 'TOK_SRCCODE'): [('reduce', ('rhsel', 2, 21))], (33, 'TOK_END'): [('reduce', ('rhslist', 3, 11))], (41, 'TOK_END'): [('reduce', ('rhsel', 2, 19))], (0, 'TOK_REL'): [('shift', 7)], (39, 'TOK_END'): [('reduce', ('rhsel', 2, 21))], (9, '$EOF$'): [('accept', None)], (25, 'TOK_CODE'): [('reduce', ('line', 4, 4))], (4, 'TOK_ID'): [('reduce', ('precoper', 1, 6))], (13, 'TOK_CPAREN'): [('reduce', ('optprec', 0, 25))], (38, 'TOK_CPAREN'): [('shift', 43)], (31, 'TOK_CPAREN'): [('reduce', ('optprec', 0, 25))], (18, 'TOK_ALT'): [('shift', 24)], (21, 'TOK_LEFT'): [('reduce', ('line', 3, 2))], (14, 'TOK_LEFT'): [('shift', 4)], (28, 'TOK_CPAREN'): [('shift', 36)], (26, 'TOK_ALT'): [('reduce', ('optcode', 0, 14))], (20, 'TOK_ID'): [('shift', 27)], (42, 'TOK_END'): [('reduce', ('rhslist', 5, 12))], (24, 'TOK_PREC'): [('shift', 17)], (31, 'TOK_END'): [('reduce', ('optprec', 0, 25))], (13, 'TOK_ID'): [('reduce', ('optprec', 0, 25))], (10, 'TOK_CODE'): [('shift', 1)], (17, 'TOK_OPAREN'): [('shift', 23)], (8, 'TOK_END'): [('reduce', ('precoper', 1, 7))], (24, 'TOK_END'): [('reduce', ('optprec', 0, 25))], (0, 'TOK_PREF'): [('shift', 6)], (36, 'TOK_CPAREN'): [('reduce', ('optprec', 4, 24))], (34, 'TOK_END'): [('reduce', ('rhsellist', 2, 15))], (0, 'TOK_NONASSOC'): [('shift', 5)], (26, 'TOK_OPAREN'): [('shift', 31)], (19, 'TOK_CPAREN'): [('reduce', ('rhsellist', 0, 16))], (21, 'TOK_GT'): [('reduce', ('line', 3, 2))], (14, 'TOK_GT'): [('shift', 2)], (31, 'TOK_PREC'): [('shift', 17)], (37, 'TOK_CPAREN'): [('reduce', ('optcode', 0, 14))], (43, 'TOK_STAR'): [('reduce', ('rhsel', 3, 18))], (3, 'TOK_DERIVES'): [('shift', 13)], (29, 'TOK_SRCCODE'): [('reduce', ('rhsellist', 0, 16))], (19, 'TOK_ID'): [('reduce', ('rhsellist', 0, 16))], (25, 'TOK_RIGHT'): [('reduce', ('line', 4, 4))], (37, 'TOK_ID'): [('shift', 30)], (36, 'TOK_ALT'): [('reduce', ('optprec', 4, 24))], (36, 'TOK_OPAREN'): [('reduce', ('optprec', 4, 24))], (16, 'TOK_END'): [('shift', 21)], (12, 'TOK_ID'): [('reduce', ('line', 2, 5))], (40, 'TOK_PLUS'): [('reduce', ('rhsel', 2, 20))], (43, 'TOK_ALT'): [('reduce', ('rhsel', 3, 18))], (12, 'TOK_LEFT'): [('reduce', ('line', 2, 5))], (0, 'TOK_RIGHT'): [('shift', 8)], (10, 'TOK_RIGHT'): [('shift', 8)], (34, 'TOK_STAR'): [('shift', 41)], (43, 'TOK_SRCCODE'): [('reduce', ('rhsel', 3, 18))], (35, 'TOK_RIGHT'): [('reduce', ('line', 5, 3))], (30, 'TOK_PLUS'): [('reduce', ('rhsel', 1, 17))], (35, 'TOK_REL'): [('reduce', ('line', 5, 3))], (41, 'TOK_OPAREN'): [('reduce', ('rhsel', 2, 19))], (13, 'TOK_SRCCODE'): [('reduce', ('optprec', 0, 25))], (10, 'TOK_REL'): [('shift', 7)], (40, 'TOK_ID'): [('reduce', ('rhsel', 2, 20))], (30, 'TOK_SRCCODE'): [('reduce', ('rhsel', 1, 17))], (6, 'TOK_ID'): [('reduce', ('precoper', 1, 9))], (30, 'TOK_CPAREN'): [('reduce', ('rhsel', 1, 17))], (32, 'TOK_END'): [('reduce', ('optcode', 1, 13))], (25, 'TOK_REL'): [('reduce', ('line', 4, 4))], (2, 'TOK_END'): [('reduce', ('precoper', 1, 10))], (0, 'TOK_CODE'): [('shift', 1)], (43, 'TOK_PLUS'): [('reduce', ('rhsel', 3, 18))], (24, 'TOK_ALT'): [('reduce', ('optprec', 0, 25))], (34, 'TOK_ALT'): [('reduce', ('rhsellist', 2, 15))], (22, 'TOK_ID'): [('reduce', ('idlist', 2, 22))], (30, 'TOK_OPAREN'): [('reduce', ('rhsel', 1, 17))], (42, 'TOK_ALT'): [('reduce', ('rhslist', 5, 12))], (30, 'TOK_ID'): [('reduce', ('rhsel', 1, 17))], (31, 'TOK_OPAREN'): [('reduce', ('optprec', 0, 25))], (39, 'TOK_OPTIONAL'): [('reduce', ('rhsel', 2, 21))], (36, 'TOK_SRCCODE'): [('reduce', ('optprec', 4, 24))], (40, 'TOK_CPAREN'): [('reduce', ('rhsel', 2, 20))], (21, 'TOK_NONASSOC'): [('reduce', ('line', 3, 2))], (24, 'TOK_OPAREN'): [('reduce', ('optprec', 0, 25))], (26, 'TOK_END'): [('reduce', ('optcode', 0, 14))], (12, 'TOK_GT'): [('reduce', ('line', 2, 5))], (29, 'TOK_ID'): [('reduce', ('rhsellist', 0, 16))], (19, 'TOK_SRCCODE'): [('reduce', ('rhsellist', 0, 16))], (10, '$EOF$'): [('reduce', ('gram', 1, 0))], (35, '$EOF$'): [('reduce', ('line', 5, 3))], (34, 'TOK_OPAREN'): [('reduce', ('rhsellist', 2, 15))], (5, 'TOK_ID'): [('reduce', ('precoper', 1, 8))], (31, 'TOK_ALT'): [('reduce', ('optprec', 0, 25))], (41, 'TOK_STAR'): [('reduce', ('rhsel', 2, 19))], (40, 'TOK_OPTIONAL'): [('reduce', ('rhsel', 2, 20))], (35, 'TOK_PREF'): [('reduce', ('line', 5, 3))], (10, 'TOK_NONASSOC'): [('shift', 5)], (37, 'TOK_SRCCODE'): [('shift', 32)], (10, 'TOK_PREF'): [('shift', 6)], (21, 'TOK_ID'): [('reduce', ('line', 3, 2))], (39, 'TOK_PLUS'): [('reduce', ('rhsel', 2, 21))], (29, 'TOK_CPAREN'): [('reduce', ('rhsellist', 0, 16))], (39, 'TOK_CPAREN'): [('reduce', ('rhsel', 2, 21))], (25, 'TOK_PREF'): [('reduce', ('line', 4, 4))], (33, 'TOK_ALT'): [('reduce', ('rhslist', 3, 11))], (25, 'TOK_NONASSOC'): [('reduce', ('line', 4, 4))], (18, 'TOK_END'): [('shift', 25)], (11, 'TOK_END'): [('reduce', ('idlist', 0, 23))], (30, 'TOK_OPTIONAL'): [('reduce', ('rhsel', 1, 17))], (36, 'TOK_END'): [('reduce', ('optprec', 4, 24))], (39, 'TOK_ID'): [('reduce', ('rhsel', 2, 21))], (25, '$EOF$'): [('reduce', ('line', 4, 4))], (1, 'TOK_SRCCODE'): [('shift', 12)], (12, 'TOK_RIGHT'): [('reduce', ('line', 2, 5))], (27, 'TOK_END'): [('shift', 35)], (24, 'TOK_ID'): [('reduce', ('optprec', 0, 25))], (34, 'TOK_ID'): [('reduce', ('rhsellist', 2, 15))], (24, 'TOK_CPAREN'): [('reduce', ('optprec', 0, 25))], (10, 'TOK_LEFT'): [('shift', 4)], (35, 'TOK_LEFT'): [('reduce', ('line', 5, 3))], (29, 'TOK_OPAREN'): [('reduce', ('rhsellist', 0, 16))], (34, 'TOK_PLUS'): [('shift', 40)], (13, 'TOK_PREC'): [('shift', 17)], (41, 'TOK_OPTIONAL'): [('reduce', ('rhsel', 2, 19))], (30, 'TOK_ALT'): [('reduce', ('rhsel', 1, 17))], (21, 'TOK_PREF'): [('reduce', ('line', 3, 2))], (40, 'TOK_STAR'): [('reduce', ('rhsel', 2, 20))], (12, 'TOK_REL'): [('reduce', ('line', 2, 5))], (34, 'TOK_CPAREN'): [('reduce', ('rhsellist', 2, 15))], (35, 'TOK_NONASSOC'): [('reduce', ('line', 5, 3))], (21, 'TOK_CODE'): [('reduce', ('line', 3, 2))], (19, 'TOK_END'): [('reduce', ('rhsellist', 0, 16))], (26, 'TOK_SRCCODE'): [('shift', 32)], (32, 'TOK_ALT'): [('reduce', ('optcode', 1, 13))], (30, 'TOK_STAR'): [('reduce', ('rhsel', 1, 17))], (40, 'TOK_ALT'): [('reduce', ('rhsel', 2, 20))], (37, 'TOK_END'): [('reduce', ('optcode', 0, 14))], (39, 'TOK_OPAREN'): [('reduce', ('rhsel', 2, 21))], (16, 'TOK_ID'): [('shift', 22)], (25, 'TOK_LEFT'): [('reduce', ('line', 4, 4))], (12, '$EOF$'): [('reduce', ('line', 2, 5))], (10, 'TOK_GT'): [('shift', 2)], (35, 'TOK_GT'): [('reduce', ('line', 5, 3))], (34, 'TOK_OPTIONAL'): [('shift', 39)], (41, 'TOK_PLUS'): [('reduce', ('rhsel', 2, 19))], (40, 'TOK_OPAREN'): [('reduce', ('rhsel', 2, 20))], (12, 'TOK_NONASSOC'): [('reduce', ('line', 2, 5))], (12, 'TOK_PREF'): [('reduce', ('line', 2, 5))], (41, 'TOK_ID'): [('reduce', ('rhsel', 2, 19))], (4, 'TOK_END'): [('reduce', ('precoper', 1, 6))], (39, 'TOK_ALT'): [('reduce', ('rhsel', 2, 21))], (7, 'TOK_ID'): [('shift', 14)], (42, 'TOK_CPAREN'): [('reduce', ('rhslist', 5, 12))], (40, 'TOK_SRCCODE'): [('reduce', ('rhsel', 2, 20))], (33, 'TOK_CPAREN'): [('reduce', ('rhslist', 3, 11))], (29, 'TOK_ALT'): [('reduce', ('rhsellist', 0, 16))], (23, 'TOK_ID'): [('shift', 28)], (0, 'TOK_ID'): [('shift', 3)], (35, 'TOK_CODE'): [('reduce', ('line', 5, 3))], (13, 'TOK_END'): [('reduce', ('optprec', 0, 25))], (31, 'TOK_ID'): [('reduce', ('optprec', 0, 25))], (8, 'TOK_ID'): [('reduce', ('precoper', 1, 7))], (25, 'TOK_GT'): [('reduce', ('line', 4, 4))], (43, 'TOK_END'): [('reduce', ('rhsel', 3, 18))], (39, 'TOK_STAR'): [('reduce', ('rhsel', 2, 21))], (41, 'TOK_CPAREN'): [('reduce', ('rhsel', 2, 19))], (26, 'TOK_ID'): [('shift', 30)], (29, 'TOK_END'): [('reduce', ('rhsellist', 0, 16))], (21, 'TOK_REL'): [('reduce', ('line', 3, 2))], (15, '$EOF$'): [('reduce', ('gram', 2, 1))], (0, 'TOK_LEFT'): [('shift', 4)], (13, 'TOK_ALT'): [('reduce', ('optprec', 0, 25))], (21, 'TOK_RIGHT'): [('reduce', ('line', 3, 2))], (5, 'TOK_END'): [('reduce', ('precoper', 1, 8))], (14, 'TOK_RIGHT'): [('shift', 8)], (38, 'TOK_ALT'): [('shift', 24)], (43, 'TOK_OPTIONAL'): [('reduce', ('rhsel', 3, 18))], (19, 'TOK_OPAREN'): [('reduce', ('rhsellist', 0, 16))], (34, 'TOK_SRCCODE'): [('reduce', ('rhsellist', 2, 15))], (26, 'TOK_CPAREN'): [('reduce', ('optcode', 0, 14))], (24, 'TOK_SRCCODE'): [('reduce', ('optprec', 0, 25))], (12, 'TOK_CODE'): [('reduce', ('line', 2, 5))], (36, 'TOK_ID'): [('reduce', ('optprec', 4, 24))], (37, 'TOK_OPAREN'): [('shift', 31)], (41, 'TOK_ALT'): [('reduce', ('rhsel', 2, 19))], (11, 'TOK_ID'): [('reduce', ('idlist', 0, 23))], (25, 'TOK_ID'): [('reduce', ('line', 4, 4))], (19, 'TOK_ALT'): [('reduce', ('rhsellist', 0, 16))], (14, 'TOK_PREF'): [('shift', 6)], (14, 'TOK_NONASSOC'): [('shift', 5)], (37, 'TOK_ALT'): [('reduce', ('optcode', 0, 14))], (6, 'TOK_END'): [('reduce', ('precoper', 1, 9))], (32, 'TOK_CPAREN'): [('reduce', ('optcode', 1, 13))], (21, '$EOF$'): [('reduce', ('line', 3, 2))], (0, 'TOK_GT'): [('shift', 2)], (40, 'TOK_END'): [('reduce', ('rhsel', 2, 20))], (31, 'TOK_SRCCODE'): [('reduce', ('optprec', 0, 25))], (43, 'TOK_ID'): [('reduce', ('rhsel', 3, 18))], (22, 'TOK_END'): [('reduce', ('idlist', 2, 22))], (2, 'TOK_ID'): [('reduce', ('precoper', 1, 10))], (10, 'TOK_ID'): [('shift', 3)], (43, 'TOK_CPAREN'): [('reduce', ('rhsel', 3, 18))], (35, 'TOK_ID'): [('reduce', ('line', 5, 3))], (41, 'TOK_SRCCODE'): [('reduce', ('rhsel', 2, 19))], (30, 'TOK_END'): [('reduce', ('rhsel', 1, 17))], (13, 'TOK_OPAREN'): [('reduce', ('optprec', 0, 25))]}
semactions = [action0, action0, action1, action2, action3, action4, action5, action6, action7, action8, action9, action10, action11, action12, action13, action14, action15, action16, action17, action18, action19, action20, action21, action22, action23, action24]
gramspec = (goto, action, semactions)

from errors import *
	
	# data collected when processing the parse.  
globcode = ""
gram = []							# list of lhs,rhs
actions = []						# list of funcs idxs
preclist = []						# ordered list of precedences
preflist = []						# ordered list of prefs
leftlist = []						# ordered list of left assocs
rightlist = []						# ordered list of right assocs
nonassoclist = []					# ordered list of nonassocs
tagged = dict()						# maps tag name to list of tagged prods
rellist = []						# list of prec relattionships
funcs = ["return kids"]				# list of action functions
internalcnt = 0						# counter for internal names
start = None						# start symbol

	# this should probably be a parameter
useleft = 1 						# use left recursion in internal rules

	# XXX in the future it would be nice to have a hash table lookup
	# of all the funcs so that we can only add the functions that we
	# need, but reuse any functions that are identical.  especially
	# for the internal functions (default, list building, optional, etc).
	# for now we just hard wire in the default rule and dont worry
	# about duplicate code for the rest.
	
	# helpers
class RhsEl :
        def __init__(self, el, type=None) :
                self.el = el
                self.type = type
class Rhs :
        def __init__(self, prec, ellist, code) :
                self.prec = prec
                self.ellist = ellist
                self.code = code

def get_intname(name, type) :
        global internalcnt
        internalcnt += 1
        return "%s.%s%d" % (name, type, internalcnt)
	
def addprod(lhs, prec, rhs, code) :
        "Add a new production to the grammar"
        prodno = len(gram)
        gram.append((lhs,rhs),)

		# add the action code
        actidx = 0
        if code is not None :
                actidx = len(funcs)
                funcs.append(code)
        actions.append(actidx)

		# add the precedence
        if prec :
                if not prec in tagged :
                        tagged[prec] = []
                if not prodno in tagged[prec] :
                        tagged[prec].append(prodno)

def procrhsel(lhs, el) :
        "return the rhs element, possibly creating internal productions."
        if el.type == '*' :
			# clos -> nothing | clos el
                nel = procrhsel(lhs, el.el)
                nlhs = get_intname(lhs, "clos")
                if useleft :
                        addprod(nlhs, None, [], "return []")
                        addprod(nlhs, None, [nlhs, nel], "kids[0].append(kids[1])\nreturn kids[0]")
                else :
                        addprod(nlhs, None, [], "return []")
                        addprod(nlhs, None, [nel, nlhs], "kids[1][0:0] = kids[0]\nreturn kids[1]")
                return nlhs
        elif el.type == '+' :
			# clos -> el| clos el
                nel = procrhsel(lhs, el.el)
                nlhs = get_intname(lhs, "posclos")
                if useleft :
                        addprod(nlhs, None, [nel], "return [kids[0]]")
                        addprod(nlhs, None, [nlhs, nel], "kids[0].append(kids[1])\nreturn kids[0]")
                else :
                        addprod(nlhs, None, [nel], "return [kids[0]]")
                        addprod(nlhs, None, [nel, nlhs], "kids[1][0:0] = kids[0]\nreturn kids[0]")
                return nlhs
        elif el.type == '?' :
			# opt = none | el
                nel = procrhsel(lhs, el.el)
                nlhs = get_intname(lhs, "opt")
                addprod(nlhs, None, [], "return")
                addprod(nlhs, None, [nel], "return kids[0]")
                return nlhs
        elif el.type == 'list' :
                return procrhslist(get_intname(lhs, "list"), el.el)
        elif el.type is None :
                return el.el
        else :
                raise InternalError("cant happen")

def procrhslist(lhs, rhslist) :
        "add productions for each lhs->rhs in rhslist"
        for rhs in rhslist :
                l = []
                for el in rhs.ellist :
                        l.append(procrhsel(lhs, el))
                addprod(lhs, rhs.prec, l, rhs.code)
        return lhs



