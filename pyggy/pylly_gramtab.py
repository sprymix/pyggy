
# This file was generated automatically

# action 0 for: [(0) spec -> sect spec], [(1) spec -> sect]
def action0(kids) :
	return kids

# action 1 for: [(2) sect -> TOK_DEFS TOK_INDENT deflist TOK_DEDENT]
def action1(kids) :
			# defs are already processed
	return
	

# action 2 for: [(3) sect -> TOK_SRCCODE]
def action2(kids) :
	global globcode
	globcode += kids[0]
	

# action 3 for: [(4) sect -> statelist TOK_INDENT rulelist TOK_DEDENT]
def action3(kids) :
	states = kids[0]
	rules = kids[2]
	for idx in xrange(len(states)) :
	        copy = (idx != len(states) - 1)
	        st = states[idx]
	        for pat,code in rules :
	                addrule(st, pat, code, copy)
	

# action 4 for: [(5) statelist -> TOK_IDENT]
def action4(kids) :
	return [addstate(kids[0])]
	

# action 5 for: [(6) statelist -> statelist TOK_COMMA TOK_IDENT]
def action5(kids) :
	kids[0].append(addstate(kids[2]))
	return kids[0]
	

# action 6 for: [(7) deflist -> TOK_IDENT TOK_QUOTE regexp TOK_QUOTE TOK_EOL]
def action6(kids) :
	name = kids[0]
	mach,str = kids[2]
	namedmachines[name] = mach
	

# action 7 for: [(8) deflist -> deflist TOK_IDENT TOK_QUOTE regexp TOK_QUOTE TOK_EOL]
def action7(kids) :
	name = kids[1]
	mach,str = kids[3]
	namedmachines[name] = mach
	

# action 8 for: [(9) rulelist -> TOK_QUOTE rulepat TOK_QUOTE TOK_SRCCODE]
def action8(kids) :
	rule = kids[1],kids[3]
	return [rule]
	

# action 9 for: [(10) rulelist -> rulelist TOK_QUOTE rulepat TOK_QUOTE TOK_SRCCODE]
def action9(kids) :
	rule = kids[2],kids[4]
	kids[0].append(rule)
	return kids[0]
	

# action 10 for: [(11) rulepat -> optanchor regexp]
def action10(kids) :
	anch = kids[0]
	mach,str = kids[1]
	if anch :
	        str = "^" + str
	return mach,anch,str,0
	

# action 11 for: [(12) rulepat -> TOK_EOFEOF]
def action11(kids) :
	return None,None,"<<EOF>>",1
	

# action 12 for: [(13) optanchor -> TOK_ANCHOR]
def action12(kids) :
	return 1
	

# action 13 for: [(14) optanchor ->]
def action13(kids) :
	return  0
	

# action 14 for: [(15) regexp -> regexp TOK_POSCLOS]
def action14(kids) :
	mach,str = kids[0]
	return n.posclosmach(mach), str+"+"
	

# action 15 for: [(16) regexp -> regexp TOK_STARCLOS]
def action15(kids) :
	mach,str = kids[0]
	return n.starclosmach(mach), str+"*"
	

# action 16 for: [(17) regexp -> regexp TOK_OPTIONAL]
def action16(kids) :
	mach,str = kids[0]
	return n.optmach(mach), str+"?"
	

# action 17 for: [(18) regexp -> regexp TOK_ALT regexp]
def action17(kids) :
	mach,str = kids[0]
	mach2,str2 = kids[2]
	return n.altmach(mach, mach2), str+"|"+str2
	

# action 18 for: [(19) regexp -> regexp regexp]
def action18(kids) :
	mach,str = kids[0]
	mach2,str2 = kids[1]
	return n.catmach(mach, mach2), str+str2
	

# action 19 for: [(20) regexp -> TOK_OPAREN regexp TOK_CPAREN]
def action19(kids) :
	return kids[1]
	

# action 20 for: [(21) regexp -> TOK_IDENT]
def action20(kids) :
	name = kids[0]
	str = "{%s}" % name
	if not name in namedmachines :
	        raise SpecError("There is no pattern named %s" % kids[0])
	mach = n.copymach(namedmachines[name])
	return mach,str
	

# action 21 for: [(22) regexp -> cclass]
def action21(kids) :
	chclass,str = kids[0]
	return n.singmach(chclass),str
	

# action 22 for: [(23) regexp -> TOK_CHAR]
def action22(kids) :
	chclass,str = [kids[0]], printable(kids[0])
	return n.singmach(chclass),str
	

# action 23 for: [(24) regexp -> TOK_WILDCARD]
def action23(kids) :
	return n.singmach(wildclass), "."
	

# action 24 for: [(25) cclass -> TOK_OBRACKET optinvert ranges TOK_CBRACKET]
def action24(kids) :
	inv = kids[1]
	rstr,cset = kids[2]
	str = "[%s%s]" % (["","^"][inv], rstr)
	return cset2list(cset, inv), str
	

# action 25 for: [(26) optinvert -> TOK_INVERT]
def action25(kids) :
	return 1
	

# action 26 for: [(27) optinvert ->]
def action26(kids) :
	return 0
	

# action 27 for: [(28) ranges -> range]
def action27(kids) :
	return kids[0]
	

# action 28 for: [(29) ranges -> ranges range]
def action28(kids) :
	str,cs = kids[0]
	str2,cs2 = kids[1]
	return str+str2, csetunion(cs, cs2)
	

# action 29 for: [(30) range -> TOK_CHAR]
def action29(kids) :
	str = printable(kids[0])
	r = [ord(kids[0])]
	return str, list2cset(r)
	

# action 30 for: [(31) range -> TOK_CHAR TOK_DASH TOK_CHAR]
def action30(kids) :
	str = "%s-%s" %  (printable(kids[0]), printable(kids[2]))
	min,max = ord(kids[0]), ord(kids[2])
	if min > max :
	        raise SpecError("bad character range %s" % str)
	r = range(min, max+1)
	return str, list2cset(r)
	

# action 31 for: [(32) range -> TOK_CCALNUM]
def action31(kids) :
	r = range(0x30,0x3a) + range(0x41,0x5b) + range(0x61,0x7b)
	return kids[0], list2cset(r)
	

# action 32 for: [(33) range -> TOK_CCALPHA]
def action32(kids) :
	r = range(0x41,0x5b) + range(0x61,0x7b)
	return kids[0], list2cset(r)
	

# action 33 for: [(34) range -> TOK_CCBLANK]
def action33(kids) :
	r = [0x09, 0x20]
	return kids[0], list2cset(r)
	

# action 34 for: [(35) range -> TOK_CCCNTRL]
def action34(kids) :
	r = range(0x00,0x20) + range(0x7f,0x80)
	return kids[0], list2cset(r)
	

# action 35 for: [(36) range -> TOK_CCDIGIT]
def action35(kids) :
	r = range(0x30,0x3a)
	return kids[0], list2cset(r)
	

# action 36 for: [(37) range -> TOK_CCGRAPH]
def action36(kids) :
	r = range(0x21,0x7f)
	return kids[0], list2cset(r)
	

# action 37 for: [(38) range -> TOK_CCLOWER]
def action37(kids) :
	r = range(0x61,0x7b)
	return kids[0], list2cset(r)
	

# action 38 for: [(39) range -> TOK_CCPRINT]
def action38(kids) :
	r = range(0x20,0x7f)
	return kids[0], list2cset(r)
	

# action 39 for: [(40) range -> TOK_CCPUNCT]
def action39(kids) :
	r = range(0x21,0x30) + range(0x3a, 0x41) + range(0x5b, 0x61) + \
	        range(0x7b, 0x7f)
	return kids[0], list2cset(r)
	

# action 40 for: [(41) range -> TOK_CCSPACE]
def action40(kids) :
	r = range(0x09,0x0e) + range(0x20,0x21)
	return kids[0], list2cset(r)
	

# action 41 for: [(42) range -> TOK_CCUPPER]
def action41(kids) :
	r = range(0x41,0x5b)
	return kids[0], list2cset(r)
	

# action 42 for: [(43) range -> TOK_CCXDIGIT]
def action42(kids) :
	r = range(0x30,0x3a) + range(0x41, 0x47) + range(0x61, 0x67)
	return kids[0], list2cset(r)
	
goto = {(83, 'TOK_WILDCARD'): 29, (60, 'TOK_OBRACKET'): 27, (64, 'TOK_IDENT'): 26, (31, 15): 55, (80, 'TOK_CCSPACE'): 76, (0, 'TOK_DEFS'): 1, (50, 'TOK_POSCLOS'): 59, (31, 23): 58, (31, 22): 58, (31, 21): 58, (31, 20): 58, (31, 17): 57, (31, 16): 56, (42, 'TOK_WILDCARD'): 29, (31, 25): 35, (31, 24): 58, (51, 'TOK_OPAREN'): 28, (42, 15): 55, (85, 'TOK_CHAR'): 25, (42, 20): 58, (42, 21): 58, (42, 22): 58, (42, 23): 58, (42, 16): 56, (42, 17): 57, (31, 'TOK_WILDCARD'): 29, (24, 11): 43, (42, 24): 58, (42, 25): 35, (24, 12): 43, (24, 13): 22, (83, 17): 57, (83, 16): 56, (83, 23): 58, (80, 'TOK_CCPRINT'): 74, (83, 21): 58, (83, 20): 58, (45, 'TOK_CCCNTRL'): 70, (83, 25): 35, (83, 24): 58, (60, 'TOK_OPAREN'): 28, (63, 'TOK_QUOTE'): 88, (12, 'TOK_IDENT'): 18, (83, 15): 55, (60, 'TOK_WILDCARD'): 29, (32, 'TOK_IDENT'): 26, (64, 17): 57, (80, 'TOK_CCBLANK'): 69, (64, 22): 58, (14, 'TOK_EOFEOF'): 20, (83, 'TOK_OBRACKET'): 27, (27, 'TOK_INVERT'): 44, (34, 'TOK_ALT'): 51, (14, 'TOK_ANCHOR'): 19, (10, 9): 15, (10, 10): 15, (31, 'TOK_OPAREN'): 28, (58, 'TOK_STARCLOS'): 54, (30, 'TOK_IDENT'): 26, (51, 19): 85, (51, 17): 85, (51, 16): 84, (51, 23): 86, (51, 22): 86, (51, 21): 86, (51, 20): 86, (51, 25): 35, (31, 'TOK_OBRACKET'): 27, (42, 'TOK_OPAREN'): 28, (62, 'TOK_IDENT'): 26, (80, 'TOK_CCCNTRL'): 70, (51, 15): 83, (83, 'TOK_OPAREN'): 28, (60, 24): 58, (56, 'TOK_OPTIONAL'): 52, (60, 22): 58, (47, 'TOK_CPAREN'): 82, (60, 20): 58, (60, 21): 58, (60, 16): 56, (60, 17): 57, (60, 15): 55, (39, 'TOK_IDENT'): 26, (48, 'TOK_ALT'): 51, (80, 42): 92, (80, 43): 92, (86, 'TOK_OPTIONAL'): 52, (80, 41): 92, (39, 'TOK_CHAR'): 25, (28, 'TOK_WILDCARD'): 29, (30, 'TOK_STARCLOS'): 54, (80, 'TOK_CBRACKET'): 91, (46, 'TOK_WILDCARD'): 29, (64, 'TOK_OBRACKET'): 27, (40, 'TOK_ALT'): 51, (62, 'TOK_CHAR'): 25, (46, 16): 56, (46, 17): 57, (80, 33): 92, (46, 20): 58, (46, 21): 58, (46, 22): 58, (46, 23): 58, (28, 22): 50, (46, 25): 35, (28, 20): 50, (28, 21): 50, (28, 18): 49, (28, 19): 48, (28, 16): 47, (28, 17): 48, (28, 15): 46, (30, 'TOK_CHAR'): 25, (18, 'TOK_QUOTE'): 36, (46, 15): 55, (47, 'TOK_ALT'): 51, (32, 'TOK_CHAR'): 25, (24, 'TOK_EOFEOF'): 20, (48, 'TOK_CPAREN'): 82, (51, 'TOK_OBRACKET'): 27, (5, 5): 6, (5, 4): 5, (80, 40): 92, (5, 6): 6, (5, 1): 8, (5, 0): 8, (5, 3): 5, (5, 2): 5, (80, 34): 92, (80, 35): 92, (80, 32): 92, (62, 23): 58, (80, 38): 92, (80, 39): 92, (80, 36): 92, (80, 37): 92, (86, 'TOK_POSCLOS'): 59, (50, 'TOK_OPTIONAL'): 52, (38, 'TOK_ALT'): 51, (85, 'TOK_IDENT'): 26, (28, 'TOK_OBRACKET'): 27, (50, 'TOK_WILDCARD'): 29, (80, 30): 92, (80, 31): 92, (64, 'TOK_STARCLOS'): 54, (14, 11): 21, (46, 'TOK_OBRACKET'): 27, (14, 13): 22, (14, 14): 22, (45, 'TOK_CCUPPER'): 77, (46, 'TOK_OPAREN'): 28, (0, 'TOK_SRCCODE'): 3, (61, 'TOK_ALT'): 51, (28, 'TOK_OPAREN'): 28, (80, 'TOK_CCGRAPH'): 72, (79, 'TOK_DASH'): 90, (21, 'TOK_QUOTE'): 37, (48, 15): 55, (60, 'TOK_ALT'): 51, (48, 24): 58, (48, 25): 35, (16, 'TOK_WILDCARD'): 29, (48, 16): 56, (48, 17): 57, (48, 22): 58, (48, 23): 58, (48, 20): 58, (48, 21): 58, (34, 'TOK_WILDCARD'): 29, (84, 'TOK_OPAREN'): 28, (24, 14): 22, (46, 'TOK_CPAREN'): 82, (50, 'TOK_CHAR'): 25, (62, 'TOK_QUOTE'): 88, (45, 'TOK_CCPUNCT'): 75, (34, 24): 58, (34, 25): 35, (34, 20): 58, (34, 21): 58, (34, 22): 58, (34, 23): 58, (34, 16): 56, (34, 17): 57, (50, 'TOK_STARCLOS'): 54, (34, 15): 55, (30, 'TOK_QUOTE'): 53, (84, 'TOK_OBRACKET'): 27, (36, 'TOK_CHAR'): 25, (86, 'TOK_IDENT'): 26, (16, 15): 30, (14, 12): 21, (32, 'TOK_QUOTE'): 53, (45, 31): 81, (64, 'TOK_OPTIONAL'): 52, (16, 24): 34, (16, 25): 35, (48, 'TOK_WILDCARD'): 29, (16, 18): 33, (16, 19): 32, (16, 16): 31, (16, 17): 32, (16, 22): 34, (16, 23): 34, (16, 20): 34, (16, 21): 34, (16, 'TOK_OBRACKET'): 27, (64, 'TOK_CHAR'): 25, (48, 'TOK_OPAREN'): 28, (22, 'TOK_IDENT'): 26, (84, 23): 58, (84, 20): 58, (84, 21): 58, (84, 16): 56, (84, 17): 57, (84, 24): 58, (84, 25): 35, (34, 'TOK_OBRACKET'): 27, (42, 'TOK_ALT'): 51, (84, 15): 55, (39, 'TOK_OPTIONAL'): 52, (32, 16): 56, (84, 'TOK_WILDCARD'): 29, (64, 'TOK_QUOTE'): 88, (34, 'TOK_OPAREN'): 28, (31, 'TOK_ALT'): 51, (58, 'TOK_POSCLOS'): 59, (48, 'TOK_OBRACKET'): 27, (83, 22): 58, (33, 'TOK_ALT'): 51, (86, 16): 56, (30, 'TOK_OPTIONAL'): 52, (86, 17): 57, (16, 'TOK_OPAREN'): 28, (47, 'TOK_OPAREN'): 28, (86, 20): 58, (61, 16): 56, (45, 35): 81, (38, 'TOK_WILDCARD'): 29, (32, 'TOK_ALT'): 51, (80, 'TOK_CCXDIGIT'): 78, (61, 25): 35, (61, 24): 58, (61, 21): 58, (61, 20): 58, (61, 23): 58, (61, 22): 58, (61, 17): 57, (16, 'TOK_IDENT'): 26, (40, 'TOK_OBRACKET'): 27, (61, 15): 55, (9, 'TOK_IDENT'): 13, (22, 'TOK_CHAR'): 25, (61, 'TOK_WILDCARD'): 29, (86, 15): 55, (45, 'TOK_CCXDIGIT'): 78, (15, 'TOK_DEDENT'): 23, (40, 'TOK_OPAREN'): 28, (7, 'TOK_IDENT'): 11, (58, 'TOK_OPTIONAL'): 52, (0, 'TOK_IDENT'): 2, (38, 15): 55, (80, 'TOK_CCALNUM'): 67, (38, 24): 58, (38, 25): 35, (38, 16): 56, (38, 17): 57, (47, 'TOK_OBRACKET'): 27, (38, 20): 58, (38, 21): 58, (38, 22): 58, (38, 23): 58, (47, 23): 58, (47, 22): 58, (47, 21): 58, (47, 20): 58, (38, 'TOK_OBRACKET'): 27, (47, 17): 57, (47, 16): 56, (47, 25): 35, (47, 24): 58, (47, 15): 55, (30, 15): 55, (30, 16): 56, (46, 'TOK_ALT'): 51, (80, 'TOK_CCLOWER'): 73, (61, 'TOK_OPAREN'): 28, (45, 'TOK_CHAR'): 79, (40, 'TOK_WILDCARD'): 29, (36, 'TOK_IDENT'): 26, (40, 15): 55, (61, 'TOK_OBRACKET'): 27, (40, 16): 56, (40, 17): 57, (40, 22): 58, (40, 23): 58, (40, 20): 58, (40, 21): 58, (40, 24): 58, (40, 25): 35, (47, 'TOK_WILDCARD'): 29, (42, 'TOK_OBRACKET'): 27, (38, 'TOK_OPAREN'): 28, (28, 'TOK_IDENT'): 26, (46, 'TOK_IDENT'): 26, (51, 'TOK_WILDCARD'): 29, (80, 'TOK_CCDIGIT'): 71, (90, 'TOK_CHAR'): 94, (6, 'TOK_INDENT'): 10, (42, 'TOK_POSCLOS'): 59, (85, 'TOK_OBRACKET'): 27, (61, 'TOK_OPTIONAL'): 52, (60, 'TOK_STARCLOS'): 54, (15, 'TOK_QUOTE'): 24, (60, 'TOK_CHAR'): 25, (85, 'TOK_OPAREN'): 28, (51, 'TOK_CHAR'): 25, (6, 'TOK_COMMA'): 9, (50, 'TOK_ALT'): 51, (38, 'TOK_OPTIONAL'): 52, (47, 'TOK_OPTIONAL'): 52, (42, 'TOK_STARCLOS'): 54, (85, 'TOK_WILDCARD'): 29, (61, 'TOK_QUOTE'): 88, (80, 'TOK_CCPUNCT'): 75, (31, 'TOK_CHAR'): 25, (83, 'TOK_STARCLOS'): 54, (51, 24): 86, (83, 'TOK_CHAR'): 25, (5, 'TOK_IDENT'): 2, (85, 21): 58, (85, 20): 58, (85, 23): 58, (85, 22): 58, (85, 17): 57, (85, 16): 56, (85, 25): 35, (85, 24): 58, (41, 'TOK_ALT'): 51, (85, 15): 55, (42, 'TOK_CHAR'): 25, (64, 'TOK_WILDCARD'): 29, (86, 'TOK_CHAR'): 25, (45, 'TOK_CCLOWER'): 73, (62, 'TOK_OPAREN'): 28, (80, 'TOK_CHAR'): 79, (42, 'TOK_IDENT'): 26, (55, 'TOK_STARCLOS'): 54, (80, 'TOK_CCALPHA'): 68, (83, 'TOK_IDENT'): 26, (63, 'TOK_ALT'): 51, (32, 'TOK_OBRACKET'): 27, (39, 'TOK_OPAREN'): 28, (39, 'TOK_OBRACKET'): 27, (32, 'TOK_OPAREN'): 28, (34, 'TOK_OPTIONAL'): 52, (11, 'TOK_QUOTE'): 16, (64, 24): 58, (64, 25): 35, (64, 16): 56, (60, 25): 35, (62, 'TOK_OBRACKET'): 27, (64, 23): 58, (64, 20): 58, (64, 21): 58, (30, 'TOK_OPAREN'): 28, (64, 15): 55, (60, 23): 58, (31, 'TOK_IDENT'): 26, (53, 'TOK_EOL'): 87, (51, 'TOK_IDENT'): 26, (62, 15): 55, (62, 16): 56, (62, 17): 57, (46, 'TOK_STARCLOS'): 54, (62, 20): 58, (62, 21): 58, (62, 22): 58, (12, 'TOK_DEDENT'): 17, (62, 24): 58, (62, 25): 35, (30, 'TOK_WILDCARD'): 29, (39, 15): 55, (84, 'TOK_OPTIONAL'): 52, (32, 'TOK_WILDCARD'): 29, (60, 'TOK_IDENT'): 26, (39, 25): 35, (39, 24): 58, (39, 23): 58, (39, 22): 58, (39, 21): 58, (39, 20): 58, (39, 17): 57, (39, 16): 56, (32, 24): 58, (32, 25): 35, (45, 'TOK_CCALNUM'): 67, (32, 17): 57, (32, 22): 58, (32, 23): 58, (32, 20): 58, (32, 21): 58, (39, 'TOK_WILDCARD'): 29, (32, 15): 55, (28, 'TOK_CHAR'): 25, (64, 'TOK_OPAREN'): 28, (46, 'TOK_CHAR'): 25, (34, 'TOK_QUOTE'): 53, (34, 'TOK_POSCLOS'): 59, (45, 'TOK_CCDIGIT'): 71, (30, 17): 57, (50, 'TOK_CPAREN'): 82, (30, 20): 58, (30, 21): 58, (30, 22): 58, (30, 23): 58, (30, 24): 58, (30, 25): 35, (86, 'TOK_OPAREN'): 28, (62, 'TOK_WILDCARD'): 29, (66, 'TOK_SRCCODE'): 89, (7, 8): 12, (7, 7): 12, (36, 'TOK_OBRACKET'): 27, (84, 'TOK_CHAR'): 25, (50, 'TOK_OPAREN'): 28, (45, 'TOK_CCBLANK'): 69, (38, 'TOK_IDENT'): 26, (0, 2): 5, (0, 3): 5, (0, 0): 4, (0, 1): 4, (0, 6): 6, (0, 4): 5, (0, 5): 6, (46, 'TOK_OPTIONAL'): 52, (30, 'TOK_OBRACKET'): 27, (50, 'TOK_OBRACKET'): 27, (61, 'TOK_IDENT'): 26, (36, 'TOK_OPAREN'): 28, (45, 'TOK_CCALPHA'): 68, (5, 'TOK_SRCCODE'): 3, (50, 15): 55, (45, 'TOK_CCSPACE'): 76, (50, 24): 58, (50, 25): 35, (50, 20): 58, (36, 'TOK_WILDCARD'): 29, (40, 'TOK_IDENT'): 26, (50, 23): 58, (50, 16): 56, (50, 17): 57, (34, 'TOK_STARCLOS'): 54, (48, 'TOK_CHAR'): 25, (49, 'TOK_ALT'): 51, (45, 'TOK_CCPRINT'): 74, (55, 'TOK_OPTIONAL'): 52, (47, 'TOK_IDENT'): 26, (16, 'TOK_CHAR'): 25, (37, 'TOK_SRCCODE'): 65, (34, 'TOK_CHAR'): 25, (36, 15): 60, (36, 22): 64, (36, 23): 64, (36, 20): 64, (36, 21): 64, (36, 18): 63, (36, 19): 62, (36, 16): 61, (36, 17): 62, (50, 'TOK_IDENT'): 26, (36, 24): 64, (36, 25): 35, (27, 27): 45, (27, 26): 45, (34, 'TOK_IDENT'): 26, (45, 29): 80, (45, 28): 80, (10, 'TOK_QUOTE'): 14, (45, 30): 81, (22, 'TOK_OBRACKET'): 27, (30, 'TOK_ALT'): 51, (80, 'TOK_CCUPPER'): 77, (86, 24): 58, (86, 25): 35, (64, 'TOK_POSCLOS'): 59, (45, 41): 81, (45, 40): 81, (45, 43): 81, (45, 42): 81, (45, 37): 81, (45, 36): 81, (45, 39): 81, (45, 38): 81, (45, 33): 81, (45, 32): 81, (47, 'TOK_CHAR'): 25, (45, 34): 81, (31, 'TOK_OPTIONAL'): 52, (49, 'TOK_CPAREN'): 82, (86, 21): 58, (88, 'TOK_EOL'): 93, (86, 'TOK_WILDCARD'): 29, (60, 'TOK_QUOTE'): 88, (42, 'TOK_OPTIONAL'): 52, (48, 'TOK_IDENT'): 26, (39, 'TOK_ALT'): 51, (86, 22): 58, (83, 'TOK_OPTIONAL'): 52, (22, 'TOK_OPAREN'): 28, (43, 'TOK_QUOTE'): 66, (62, 'TOK_ALT'): 51, (45, 'TOK_CCGRAPH'): 72, (40, 'TOK_CHAR'): 25, (86, 23): 58, (60, 'TOK_OPTIONAL'): 52, (61, 'TOK_CHAR'): 25, (22, 'TOK_WILDCARD'): 29, (64, 'TOK_ALT'): 51, (31, 'TOK_QUOTE'): 53, (5, 'TOK_DEFS'): 1, (84, 'TOK_IDENT'): 26, (50, 21): 58, (50, 22): 58, (1, 'TOK_INDENT'): 7, (28, 24): 50, (38, 'TOK_STARCLOS'): 54, (28, 25): 35, (33, 'TOK_QUOTE'): 53, (46, 24): 58, (28, 23): 50, (84, 22): 58, (38, 'TOK_CHAR'): 25, (86, 'TOK_OBRACKET'): 27, (24, 'TOK_ANCHOR'): 19, (86, 'TOK_STARCLOS'): 54, (22, 24): 42, (22, 25): 35, (22, 16): 39, (22, 17): 40, (22, 18): 41, (22, 19): 40, (22, 20): 42, (22, 21): 42, (22, 22): 42, (22, 23): 42, (22, 15): 38}
action = {(67, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 32))], (83, 'TOK_WILDCARD'): [('shift', 29)], (65, 'TOK_QUOTE'): [('reduce', ('rulelist', 4, 9))], (60, 'TOK_OBRACKET'): [('shift', 27)], (26, 'TOK_STARCLOS'): [('reduce', ('regexp', 1, 21))], (35, 'TOK_CHAR'): [('reduce', ('regexp', 1, 22))], (92, 'TOK_CBRACKET'): [('reduce', ('ranges', 2, 29))], (77, 'TOK_CCUPPER'): [('reduce', ('range', 1, 42))], (64, 'TOK_IDENT'): [('shift', 26)], (80, 'TOK_CCSPACE'): [('shift', 76)], (0, 'TOK_DEFS'): [('shift', 1)], (86, 'TOK_OPTIONAL'): [('shift', 52)], (54, 'TOK_QUOTE'): [('reduce', ('regexp', 2, 16))], (77, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 42))], (68, 'TOK_CCUPPER'): [('reduce', ('range', 1, 33))], (42, 'TOK_WILDCARD'): [('shift', 29)], (51, 'TOK_OBRACKET'): [('shift', 27)], (51, 'TOK_OPAREN'): [('shift', 28)], (58, 'TOK_WILDCARD'): [('reduce', ('regexp', 2, 19))], (56, 'TOK_QUOTE'): [('reduce', ('regexp', 2, 19))], (69, 'TOK_CBRACKET'): [('reduce', ('range', 1, 34))], (85, 'TOK_CHAR'): [('shift', 25)], (72, 'TOK_CCLOWER'): [('reduce', ('range', 1, 37))], (31, 'TOK_WILDCARD'): [('shift', 29)], (3, 'TOK_IDENT'): [('reduce', ('sect', 1, 3))], (35, 'TOK_STARCLOS'): [('reduce', ('regexp', 1, 22))], (25, 'TOK_ALT'): [('reduce', ('regexp', 1, 23))], (80, 'TOK_CCPRINT'): [('shift', 74)], (45, 'TOK_CCCNTRL'): [('shift', 70)], (60, 'TOK_OPAREN'): [('shift', 28)], (26, 'TOK_CHAR'): [('reduce', ('regexp', 1, 21))], (78, 'TOK_CBRACKET'): [('reduce', ('range', 1, 43))], (63, 'TOK_QUOTE'): [('shift', 88)], (71, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 36))], (12, 'TOK_IDENT'): [('shift', 18)], (44, 'TOK_CHAR'): [('reduce', ('optinvert', 1, 26))], (27, 'TOK_CCCNTRL'): [('reduce', ('optinvert', 0, 27))], (60, 'TOK_WILDCARD'): [('shift', 29)], (32, 'TOK_IDENT'): [('shift', 26)], (92, 'TOK_CCALPHA'): [('reduce', ('ranges', 2, 29))], (80, 'TOK_CCBLANK'): [('shift', 69)], (78, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 43))], (54, 'TOK_OPTIONAL'): [('reduce', ('regexp', 2, 16))], (44, 'TOK_CCXDIGIT'): [('reduce', ('optinvert', 1, 26))], (14, 'TOK_EOFEOF'): [('shift', 20)], (73, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 38))], (73, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 38))], (94, 'TOK_CCPUNCT'): [('reduce', ('range', 3, 31))], (83, 'TOK_OBRACKET'): [('shift', 27)], (68, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 33))], (27, 'TOK_INVERT'): [('shift', 44)], (34, 'TOK_ALT'): [('shift', 51)], (51, 'TOK_WILDCARD'): [('shift', 29)], (90, 'TOK_CHAR'): [('shift', 94)], (13, 'TOK_INDENT'): [('reduce', ('statelist', 3, 6))], (31, 'TOK_OPAREN'): [('shift', 28)], (58, 'TOK_STARCLOS'): [('shift', 54)], (30, 'TOK_IDENT'): [('shift', 26)], (24, 'TOK_OBRACKET'): [('reduce', ('optanchor', 0, 14))], (69, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 34))], (24, 'TOK_OPAREN'): [('reduce', ('optanchor', 0, 14))], (57, 'TOK_ALT'): [('reduce', ('regexp', 2, 19))], (13, 'TOK_COMMA'): [('reduce', ('statelist', 3, 6))], (31, 'TOK_OBRACKET'): [('shift', 27)], (58, 'TOK_CHAR'): [('reduce', ('regexp', 2, 19))], (42, 'TOK_OPAREN'): [('shift', 28)], (76, 'TOK_CHAR'): [('reduce', ('range', 1, 41))], (62, 'TOK_IDENT'): [('shift', 26)], (47, 'TOK_IDENT'): [('shift', 26)], (80, 'TOK_CCALPHA'): [('shift', 68)], (75, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 40))], (83, 'TOK_OPAREN'): [('shift', 28)], (29, 'TOK_CPAREN'): [('reduce', ('regexp', 1, 24))], (92, 'TOK_CCGRAPH'): [('reduce', ('ranges', 2, 29))], (56, 'TOK_OPTIONAL'): [('shift', 52)], (47, 'TOK_CPAREN'): [('shift', 82)], (92, 'TOK_CHAR'): [('reduce', ('ranges', 2, 29))], (75, 'TOK_CCALNUM'): [('reduce', ('range', 1, 40))], (81, 'TOK_CCPUNCT'): [('reduce', ('ranges', 1, 28))], (39, 'TOK_IDENT'): [('shift', 26)], (67, 'TOK_CHAR'): [('reduce', ('range', 1, 32))], (75, 'TOK_CCLOWER'): [('reduce', ('range', 1, 40))], (48, 'TOK_ALT'): [('shift', 51)], (70, 'TOK_CCLOWER'): [('reduce', ('range', 1, 35))], (69, 'TOK_CCPRINT'): [('reduce', ('range', 1, 34))], (68, 'TOK_CCBLANK'): [('reduce', ('range', 1, 33))], (59, 'TOK_QUOTE'): [('reduce', ('regexp', 2, 15))], (24, 'TOK_WILDCARD'): [('reduce', ('optanchor', 0, 14))], (81, 'TOK_CCDIGIT'): [('reduce', ('ranges', 1, 28))], (76, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 41))], (39, 'TOK_CHAR'): [('shift', 25)], (73, 'TOK_CHAR'): [('reduce', ('range', 1, 38))], (92, 'TOK_CCSPACE'): [('reduce', ('ranges', 2, 29))], (28, 'TOK_WILDCARD'): [('shift', 29)], (14, 'TOK_OPAREN'): [('reduce', ('optanchor', 0, 14))], (4, '$EOF$'): [('accept', None)], (80, 'TOK_CBRACKET'): [('shift', 91)], (58, 'TOK_IDENT'): [('reduce', ('regexp', 2, 19))], (81, 'TOK_CCALNUM'): [('reduce', ('ranges', 1, 28))], (46, 'TOK_WILDCARD'): [('shift', 29)], (55, 'TOK_OBRACKET'): [('reduce', ('regexp', 2, 19))], (79, 'TOK_CCLOWER'): [('reduce', ('range', 1, 30))], (40, 'TOK_ALT'): [('shift', 51)], (62, 'TOK_CHAR'): [('shift', 25)], (78, 'TOK_CCPRINT'): [('reduce', ('range', 1, 43))], (69, 'TOK_CCSPACE'): [('reduce', ('range', 1, 34))], (19, 'TOK_WILDCARD'): [('reduce', ('optanchor', 1, 13))], (55, 'TOK_OPAREN'): [('reduce', ('regexp', 2, 19))], (24, 'TOK_ANCHOR'): [('shift', 19)], (57, 'TOK_CPAREN'): [('reduce', ('regexp', 2, 19))], (92, 'TOK_CCPRINT'): [('reduce', ('ranges', 2, 29))], (76, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 41))], (74, 'TOK_CCUPPER'): [('reduce', ('range', 1, 39))], (71, 'TOK_CCALPHA'): [('reduce', ('range', 1, 36))], (30, 'TOK_CHAR'): [('shift', 25)], (18, 'TOK_QUOTE'): [('shift', 36)], (14, 'TOK_OBRACKET'): [('reduce', ('optanchor', 0, 14))], (34, 'TOK_CHAR'): [('shift', 25)], (94, 'TOK_CCXDIGIT'): [('reduce', ('range', 3, 31))], (47, 'TOK_ALT'): [('shift', 51)], (32, 'TOK_CHAR'): [('shift', 25)], (29, 'TOK_ALT'): [('reduce', ('regexp', 1, 24))], (78, 'TOK_CCSPACE'): [('reduce', ('range', 1, 43))], (24, 'TOK_EOFEOF'): [('shift', 20)], (48, 'TOK_CPAREN'): [('shift', 82)], (67, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 32))], (78, 'TOK_CCALPHA'): [('reduce', ('range', 1, 43))], (68, 'TOK_CCALNUM'): [('reduce', ('range', 1, 33))], (26, 'TOK_IDENT'): [('reduce', ('regexp', 1, 21))], (84, 'TOK_ALT'): [('reduce', ('regexp', 3, 18))], (82, 'TOK_STARCLOS'): [('reduce', ('regexp', 3, 20))], (50, 'TOK_OPTIONAL'): [('shift', 52)], (86, 'TOK_POSCLOS'): [('shift', 59)], (82, 'TOK_QUOTE'): [('reduce', ('regexp', 3, 20))], (86, 'TOK_CPAREN'): [('reduce', ('regexp', 3, 18))], (38, 'TOK_ALT'): [('shift', 51)], (72, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 37))], (55, 'TOK_WILDCARD'): [('reduce', ('regexp', 2, 19))], (19, 'TOK_OPAREN'): [('reduce', ('optanchor', 1, 13))], (72, 'TOK_CCALNUM'): [('reduce', ('range', 1, 37))], (78, 'TOK_CCLOWER'): [('reduce', ('range', 1, 43))], (27, 'TOK_CCUPPER'): [('reduce', ('optinvert', 0, 27))], (85, 'TOK_IDENT'): [('shift', 26)], (59, 'TOK_OPTIONAL'): [('reduce', ('regexp', 2, 15))], (38, 'TOK_OPAREN'): [('shift', 28)], (28, 'TOK_OBRACKET'): [('shift', 27)], (69, 'TOK_CCALPHA'): [('reduce', ('range', 1, 34))], (41, 'TOK_QUOTE'): [('reduce', ('rulepat', 2, 11))], (64, 'TOK_STARCLOS'): [('shift', 54)], (46, 'TOK_OBRACKET'): [('shift', 27)], (45, 'TOK_CCUPPER'): [('shift', 77)], (46, 'TOK_OPAREN'): [('shift', 28)], (64, 'TOK_CHAR'): [('shift', 25)], (87, 'TOK_DEDENT'): [('reduce', ('deflist', 5, 7))], (61, 'TOK_ALT'): [('shift', 51)], (79, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 30))], (28, 'TOK_OPAREN'): [('shift', 28)], (50, 'TOK_POSCLOS'): [('shift', 59)], (14, 'TOK_WILDCARD'): [('reduce', ('optanchor', 0, 14))], (80, 'TOK_CCGRAPH'): [('shift', 72)], (79, 'TOK_CCPRINT'): [('reduce', ('range', 1, 30))], (78, 'TOK_CCBLANK'): [('reduce', ('range', 1, 43))], (19, 'TOK_OBRACKET'): [('reduce', ('optanchor', 1, 13))], (73, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 38))], (52, 'TOK_ALT'): [('reduce', ('regexp', 2, 17))], (81, 'TOK_CCLOWER'): [('reduce', ('ranges', 1, 28))], (69, 'TOK_CCBLANK'): [('reduce', ('range', 1, 34))], (91, 'TOK_QUOTE'): [('reduce', ('cclass', 4, 25))], (25, 'TOK_CPAREN'): [('reduce', ('regexp', 1, 23))], (79, 'TOK_CCALNUM'): [('reduce', ('range', 1, 30))], (17, 'TOK_IDENT'): [('reduce', ('sect', 4, 2))], (44, 'TOK_CCPUNCT'): [('reduce', ('optinvert', 1, 26))], (70, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 35))], (71, 'TOK_CHAR'): [('reduce', ('range', 1, 36))], (35, 'TOK_IDENT'): [('reduce', ('regexp', 1, 22))], (79, 'TOK_DASH'): [('shift', 90)], (21, 'TOK_QUOTE'): [('shift', 37)], (60, 'TOK_ALT'): [('shift', 51)], (78, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 43))], (72, 'TOK_CCALPHA'): [('reduce', ('range', 1, 37))], (16, 'TOK_WILDCARD'): [('shift', 29)], (39, 'TOK_QUOTE'): [('reduce', ('rulepat', 2, 11))], (79, 'TOK_CCBLANK'): [('reduce', ('range', 1, 30))], (27, 'TOK_CCPUNCT'): [('reduce', ('optinvert', 0, 27))], (34, 'TOK_WILDCARD'): [('shift', 29)], (84, 'TOK_OPAREN'): [('shift', 28)], (81, 'TOK_CCPRINT'): [('reduce', ('ranges', 1, 28))], (71, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 36))], (75, 'TOK_CCBLANK'): [('reduce', ('range', 1, 40))], (92, 'TOK_CCBLANK'): [('reduce', ('ranges', 2, 29))], (46, 'TOK_CPAREN'): [('shift', 82)], (50, 'TOK_CHAR'): [('shift', 25)], (62, 'TOK_QUOTE'): [('shift', 88)], (45, 'TOK_CCPUNCT'): [('shift', 75)], (69, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 34))], (58, 'TOK_CPAREN'): [('reduce', ('regexp', 2, 19))], (68, 'TOK_CHAR'): [('reduce', ('range', 1, 33))], (79, 'TOK_CCALPHA'): [('reduce', ('range', 1, 30))], (94, 'TOK_CCCNTRL'): [('reduce', ('range', 3, 31))], (8, '$EOF$'): [('reduce', ('spec', 2, 0))], (50, 'TOK_STARCLOS'): [('shift', 54)], (75, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 40))], (30, 'TOK_QUOTE'): [('shift', 53)], (91, 'TOK_CHAR'): [('reduce', ('cclass', 4, 25))], (84, 'TOK_OBRACKET'): [('shift', 27)], (36, 'TOK_CHAR'): [('shift', 25)], (86, 'TOK_IDENT'): [('shift', 26)], (92, 'TOK_CCDIGIT'): [('reduce', ('ranges', 2, 29))], (93, 'TOK_DEDENT'): [('reduce', ('deflist', 6, 8))], (81, 'TOK_CCSPACE'): [('reduce', ('ranges', 1, 28))], (32, 'TOK_QUOTE'): [('shift', 53)], (64, 'TOK_OPTIONAL'): [('shift', 52)], (52, 'TOK_CPAREN'): [('reduce', ('regexp', 2, 17))], (48, 'TOK_WILDCARD'): [('shift', 29)], (59, 'TOK_STARCLOS'): [('reduce', ('regexp', 2, 15))], (44, 'TOK_CCUPPER'): [('reduce', ('optinvert', 1, 26))], (25, 'TOK_OBRACKET'): [('reduce', ('regexp', 1, 23))], (70, 'TOK_CCALPHA'): [('reduce', ('range', 1, 35))], (77, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 42))], (16, 'TOK_OBRACKET'): [('shift', 27)], (70, 'TOK_CCSPACE'): [('reduce', ('range', 1, 35))], (0, 'TOK_SRCCODE'): [('shift', 3)], (82, 'TOK_CHAR'): [('reduce', ('regexp', 3, 20))], (48, 'TOK_OPAREN'): [('shift', 28)], (91, 'TOK_STARCLOS'): [('reduce', ('cclass', 4, 25))], (81, 'TOK_CCALPHA'): [('reduce', ('ranges', 1, 28))], (22, 'TOK_IDENT'): [('shift', 26)], (55, 'TOK_CPAREN'): [('reduce', ('regexp', 2, 19))], (57, 'TOK_OPAREN'): [('reduce', ('regexp', 2, 19))], (56, 'TOK_IDENT'): [('reduce', ('regexp', 2, 19))], (75, 'TOK_CBRACKET'): [('reduce', ('range', 1, 40))], (72, 'TOK_CCPRINT'): [('reduce', ('range', 1, 37))], (34, 'TOK_OBRACKET'): [('shift', 27)], (42, 'TOK_ALT'): [('shift', 51)], (79, 'TOK_CCSPACE'): [('reduce', ('range', 1, 30))], (17, 'TOK_DEFS'): [('reduce', ('sect', 4, 2))], (39, 'TOK_OPTIONAL'): [('shift', 52)], (78, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 43))], (54, 'TOK_IDENT'): [('reduce', ('regexp', 2, 16))], (69, 'TOK_CCLOWER'): [('reduce', ('range', 1, 34))], (81, 'TOK_CCBLANK'): [('reduce', ('ranges', 1, 28))], (17, '$EOF$'): [('reduce', ('sect', 4, 2))], (70, 'TOK_CCPRINT'): [('reduce', ('range', 1, 35))], (84, 'TOK_WILDCARD'): [('shift', 29)], (64, 'TOK_QUOTE'): [('shift', 88)], (34, 'TOK_OPAREN'): [('shift', 28)], (31, 'TOK_ALT'): [('shift', 51)], (84, 'TOK_CPAREN'): [('reduce', ('regexp', 3, 18))], (58, 'TOK_POSCLOS'): [('shift', 59)], (70, 'TOK_CCALNUM'): [('reduce', ('range', 1, 35))], (76, 'TOK_CCUPPER'): [('reduce', ('range', 1, 41))], (57, 'TOK_OBRACKET'): [('reduce', ('regexp', 2, 19))], (74, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 39))], (72, 'TOK_CCUPPER'): [('reduce', ('range', 1, 37))], (72, 'TOK_CCSPACE'): [('reduce', ('range', 1, 37))], (48, 'TOK_OBRACKET'): [('shift', 27)], (91, 'TOK_OPTIONAL'): [('reduce', ('cclass', 4, 25))], (33, 'TOK_ALT'): [('shift', 51)], (77, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 42))], (25, 'TOK_WILDCARD'): [('reduce', ('regexp', 1, 23))], (67, 'TOK_CCUPPER'): [('reduce', ('range', 1, 32))], (30, 'TOK_OPTIONAL'): [('shift', 52)], (16, 'TOK_OPAREN'): [('shift', 28)], (3, 'TOK_SRCCODE'): [('reduce', ('sect', 1, 3))], (94, 'TOK_CCSPACE'): [('reduce', ('range', 3, 31))], (91, 'TOK_IDENT'): [('reduce', ('cclass', 4, 25))], (47, 'TOK_OPAREN'): [('shift', 28)], (74, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 39))], (76, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 41))], (83, 'TOK_CPAREN'): [('reduce', ('regexp', 3, 18))], (29, 'TOK_OPAREN'): [('reduce', ('regexp', 1, 24))], (3, 'TOK_DEFS'): [('reduce', ('sect', 1, 3))], (73, 'TOK_CCUPPER'): [('reduce', ('range', 1, 38))], (35, 'TOK_QUOTE'): [('reduce', ('regexp', 1, 22))], (38, 'TOK_WILDCARD'): [('shift', 29)], (72, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 37))], (54, 'TOK_CHAR'): [('reduce', ('regexp', 2, 16))], (67, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 32))], (55, 'TOK_ALT'): [('reduce', ('regexp', 2, 19))], (68, 'TOK_CCLOWER'): [('reduce', ('range', 1, 33))], (31, 'TOK_OPTIONAL'): [('shift', 52)], (40, 'TOK_OBRACKET'): [('shift', 27)], (9, 'TOK_IDENT'): [('shift', 13)], (22, 'TOK_CHAR'): [('shift', 25)], (61, 'TOK_WILDCARD'): [('shift', 29)], (85, 'TOK_QUOTE'): [('reduce', ('regexp', 3, 18))], (81, 'TOK_CCCNTRL'): [('reduce', ('ranges', 1, 28))], (56, 'TOK_CHAR'): [('reduce', ('regexp', 2, 19))], (45, 'TOK_CCXDIGIT'): [('shift', 78)], (15, 'TOK_DEDENT'): [('shift', 23)], (82, 'TOK_POSCLOS'): [('reduce', ('regexp', 3, 20))], (40, 'TOK_OPAREN'): [('shift', 28)], (68, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 33))], (86, 'TOK_QUOTE'): [('reduce', ('regexp', 3, 18))], (80, 'TOK_CCDIGIT'): [('shift', 71)], (27, 'TOK_CCXDIGIT'): [('reduce', ('optinvert', 0, 27))], (74, 'TOK_CHAR'): [('reduce', ('range', 1, 39))], (58, 'TOK_OPTIONAL'): [('shift', 52)], (0, 'TOK_IDENT'): [('shift', 2)], (52, 'TOK_WILDCARD'): [('reduce', ('regexp', 2, 17))], (3, '$EOF$'): [('reduce', ('sect', 1, 3))], (80, 'TOK_CCALNUM'): [('shift', 67)], (92, 'TOK_CCXDIGIT'): [('reduce', ('ranges', 2, 29))], (29, 'TOK_OBRACKET'): [('reduce', ('regexp', 1, 24))], (70, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 35))], (82, 'TOK_IDENT'): [('reduce', ('regexp', 3, 20))], (47, 'TOK_OBRACKET'): [('shift', 27)], (80, 'TOK_CCXDIGIT'): [('shift', 78)], (86, 'TOK_CHAR'): [('shift', 25)], (38, 'TOK_OBRACKET'): [('shift', 27)], (70, 'TOK_CBRACKET'): [('reduce', ('range', 1, 35))], (94, 'TOK_CCUPPER'): [('reduce', ('range', 3, 31))], (81, 'TOK_CCGRAPH'): [('reduce', ('ranges', 1, 28))], (77, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 42))], (27, 'TOK_CHAR'): [('reduce', ('optinvert', 0, 27))], (74, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 39))], (46, 'TOK_ALT'): [('shift', 51)], (80, 'TOK_CCLOWER'): [('shift', 73)], (61, 'TOK_OPAREN'): [('shift', 28)], (70, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 35))], (45, 'TOK_CHAR'): [('shift', 79)], (35, 'TOK_OPTIONAL'): [('reduce', ('regexp', 1, 22))], (79, 'TOK_CBRACKET'): [('reduce', ('range', 1, 30))], (68, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 33))], (40, 'TOK_WILDCARD'): [('shift', 29)], (36, 'TOK_IDENT'): [('shift', 26)], (26, 'TOK_OPTIONAL'): [('reduce', ('regexp', 1, 21))], (58, 'TOK_QUOTE'): [('reduce', ('regexp', 2, 19))], (73, 'TOK_CCLOWER'): [('reduce', ('range', 1, 38))], (79, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 30))], (61, 'TOK_OBRACKET'): [('shift', 27)], (50, 'TOK_IDENT'): [('shift', 26)], (64, 'TOK_POSCLOS'): [('shift', 59)], (17, 'TOK_SRCCODE'): [('reduce', ('sect', 4, 2))], (29, 'TOK_WILDCARD'): [('reduce', ('regexp', 1, 24))], (59, 'TOK_IDENT'): [('reduce', ('regexp', 2, 15))], (75, 'TOK_CCPRINT'): [('reduce', ('range', 1, 40))], (47, 'TOK_WILDCARD'): [('shift', 29)], (42, 'TOK_OBRACKET'): [('shift', 27)], (86, 'TOK_STARCLOS'): [('shift', 54)], (69, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 34))], (71, 'TOK_CCUPPER'): [('reduce', ('range', 1, 36))], (28, 'TOK_IDENT'): [('shift', 26)], (72, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 37))], (46, 'TOK_IDENT'): [('shift', 26)], (14, 'TOK_ANCHOR'): [('shift', 19)], (7, 'TOK_IDENT'): [('shift', 11)], (94, 'TOK_CCBLANK'): [('reduce', ('range', 3, 31))], (35, 'TOK_POSCLOS'): [('reduce', ('regexp', 1, 22))], (6, 'TOK_INDENT'): [('shift', 10)], (25, 'TOK_OPAREN'): [('reduce', ('regexp', 1, 23))], (76, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 41))], (85, 'TOK_OBRACKET'): [('shift', 27)], (73, 'TOK_CCSPACE'): [('reduce', ('range', 1, 38))], (87, 'TOK_IDENT'): [('reduce', ('deflist', 5, 7))], (61, 'TOK_OPTIONAL'): [('shift', 52)], (29, 'TOK_QUOTE'): [('reduce', ('regexp', 1, 24))], (23, 'TOK_DEFS'): [('reduce', ('sect', 4, 4))], (75, 'TOK_CCALPHA'): [('reduce', ('range', 1, 40))], (25, 'TOK_POSCLOS'): [('reduce', ('regexp', 1, 23))], (35, 'TOK_OPAREN'): [('reduce', ('regexp', 1, 22))], (26, 'TOK_OBRACKET'): [('reduce', ('regexp', 1, 21))], (67, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 32))], (60, 'TOK_STARCLOS'): [('shift', 54)], (15, 'TOK_QUOTE'): [('shift', 24)], (26, 'TOK_OPAREN'): [('reduce', ('regexp', 1, 21))], (60, 'TOK_CHAR'): [('shift', 25)], (78, 'TOK_CHAR'): [('reduce', ('range', 1, 43))], (26, 'TOK_QUOTE'): [('reduce', ('regexp', 1, 21))], (59, 'TOK_ALT'): [('reduce', ('regexp', 2, 15))], (35, 'TOK_OBRACKET'): [('reduce', ('regexp', 1, 22))], (23, '$EOF$'): [('reduce', ('sect', 4, 4))], (79, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 30))], (94, 'TOK_CCALPHA'): [('reduce', ('range', 3, 31))], (71, 'TOK_CCBLANK'): [('reduce', ('range', 1, 36))], (73, 'TOK_CCALNUM'): [('reduce', ('range', 1, 38))], (85, 'TOK_OPAREN'): [('shift', 28)], (51, 'TOK_CHAR'): [('shift', 25)], (19, 'TOK_IDENT'): [('reduce', ('optanchor', 1, 13))], (70, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 35))], (73, 'TOK_CCPRINT'): [('reduce', ('range', 1, 38))], (6, 'TOK_COMMA'): [('shift', 9)], (40, 'TOK_QUOTE'): [('reduce', ('rulepat', 2, 11))], (81, 'TOK_CBRACKET'): [('reduce', ('ranges', 1, 28))], (50, 'TOK_ALT'): [('shift', 51)], (68, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 33))], (69, 'TOK_CHAR'): [('reduce', ('range', 1, 34))], (38, 'TOK_OPTIONAL'): [('shift', 52)], (71, 'TOK_CCPRINT'): [('reduce', ('range', 1, 36))], (47, 'TOK_OPTIONAL'): [('shift', 52)], (69, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 34))], (42, 'TOK_STARCLOS'): [('shift', 54)], (55, 'TOK_IDENT'): [('reduce', ('regexp', 2, 19))], (29, 'TOK_OPTIONAL'): [('reduce', ('regexp', 1, 24))], (85, 'TOK_WILDCARD'): [('shift', 29)], (61, 'TOK_QUOTE'): [('shift', 88)], (56, 'TOK_CPAREN'): [('reduce', ('regexp', 2, 19))], (73, 'TOK_CCBLANK'): [('reduce', ('range', 1, 38))], (89, 'TOK_DEDENT'): [('reduce', ('rulelist', 5, 10))], (80, 'TOK_CCPUNCT'): [('shift', 75)], (58, 'TOK_OBRACKET'): [('reduce', ('regexp', 2, 19))], (75, 'TOK_CCUPPER'): [('reduce', ('range', 1, 40))], (31, 'TOK_CHAR'): [('shift', 25)], (52, 'TOK_QUOTE'): [('reduce', ('regexp', 2, 17))], (94, 'TOK_CCDIGIT'): [('reduce', ('range', 3, 31))], (26, 'TOK_WILDCARD'): [('reduce', ('regexp', 1, 21))], (77, 'TOK_CCLOWER'): [('reduce', ('range', 1, 42))], (91, 'TOK_ALT'): [('reduce', ('cclass', 4, 25))], (38, 'TOK_STARCLOS'): [('shift', 54)], (78, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 43))], (83, 'TOK_STARCLOS'): [('shift', 54)], (44, 'TOK_CCGRAPH'): [('reduce', ('optinvert', 1, 26))], (20, 'TOK_QUOTE'): [('reduce', ('rulepat', 1, 12))], (67, 'TOK_CBRACKET'): [('reduce', ('range', 1, 32))], (26, 'TOK_ALT'): [('reduce', ('regexp', 1, 21))], (83, 'TOK_CHAR'): [('shift', 25)], (79, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 30))], (71, 'TOK_CCSPACE'): [('reduce', ('range', 1, 36))], (73, 'TOK_CCALPHA'): [('reduce', ('range', 1, 38))], (70, 'TOK_CCBLANK'): [('reduce', ('range', 1, 35))], (35, 'TOK_WILDCARD'): [('reduce', ('regexp', 1, 22))], (5, 'TOK_IDENT'): [('shift', 2)], (38, 'TOK_QUOTE'): [('reduce', ('rulepat', 2, 11))], (54, 'TOK_CPAREN'): [('reduce', ('regexp', 2, 16))], (14, 'TOK_IDENT'): [('reduce', ('optanchor', 0, 14))], (24, 'TOK_CHAR'): [('reduce', ('optanchor', 0, 14))], (76, 'TOK_CBRACKET'): [('reduce', ('range', 1, 41))], (94, 'TOK_CCPRINT'): [('reduce', ('range', 3, 31))], (41, 'TOK_ALT'): [('shift', 51)], (42, 'TOK_CHAR'): [('shift', 25)], (84, 'TOK_QUOTE'): [('reduce', ('regexp', 3, 18))], (44, 'TOK_CCPRINT'): [('reduce', ('optinvert', 1, 26))], (64, 'TOK_WILDCARD'): [('shift', 29)], (56, 'TOK_ALT'): [('reduce', ('regexp', 2, 19))], (14, 'TOK_CHAR'): [('reduce', ('optanchor', 0, 14))], (24, 'TOK_IDENT'): [('reduce', ('optanchor', 0, 14))], (30, 'TOK_OBRACKET'): [('shift', 27)], (62, 'TOK_OPAREN'): [('shift', 28)], (80, 'TOK_CHAR'): [('shift', 79)], (82, 'TOK_ALT'): [('reduce', ('regexp', 3, 20))], (76, 'TOK_CCALPHA'): [('reduce', ('range', 1, 41))], (52, 'TOK_OPAREN'): [('reduce', ('regexp', 2, 17))], (27, 'TOK_CCLOWER'): [('reduce', ('optinvert', 0, 27))], (2, 'TOK_COMMA'): [('reduce', ('statelist', 1, 5))], (42, 'TOK_IDENT'): [('shift', 26)], (55, 'TOK_STARCLOS'): [('shift', 54)], (58, 'TOK_OPAREN'): [('reduce', ('regexp', 2, 19))], (74, 'TOK_CCALNUM'): [('reduce', ('range', 1, 39))], (91, 'TOK_CPAREN'): [('reduce', ('cclass', 4, 25))], (25, 'TOK_QUOTE'): [('reduce', ('regexp', 1, 23))], (83, 'TOK_IDENT'): [('shift', 26)], (77, 'TOK_CHAR'): [('reduce', ('range', 1, 42))], (63, 'TOK_ALT'): [('shift', 51)], (67, 'TOK_CCALPHA'): [('reduce', ('range', 1, 32))], (32, 'TOK_OBRACKET'): [('shift', 27)], (29, 'TOK_POSCLOS'): [('reduce', ('regexp', 1, 24))], (39, 'TOK_OPAREN'): [('shift', 28)], (76, 'TOK_CCBLANK'): [('reduce', ('range', 1, 41))], (39, 'TOK_OBRACKET'): [('shift', 27)], (32, 'TOK_OPAREN'): [('shift', 28)], (34, 'TOK_OPTIONAL'): [('shift', 52)], (78, 'TOK_CCALNUM'): [('reduce', ('range', 1, 43))], (44, 'TOK_CCSPACE'): [('reduce', ('optinvert', 1, 26))], (82, 'TOK_CPAREN'): [('reduce', ('regexp', 3, 20))], (94, 'TOK_CCGRAPH'): [('reduce', ('range', 3, 31))], (81, 'TOK_CCUPPER'): [('reduce', ('ranges', 1, 28))], (11, 'TOK_QUOTE'): [('shift', 16)], (2, 'TOK_INDENT'): [('reduce', ('statelist', 1, 5))], (55, 'TOK_CHAR'): [('reduce', ('regexp', 2, 19))], (62, 'TOK_OBRACKET'): [('shift', 27)], (54, 'TOK_ALT'): [('reduce', ('regexp', 2, 16))], (67, 'TOK_CCBLANK'): [('reduce', ('range', 1, 32))], (30, 'TOK_OPAREN'): [('shift', 28)], (31, 'TOK_IDENT'): [('shift', 26)], (94, 'TOK_CHAR'): [('reduce', ('range', 3, 31))], (53, 'TOK_EOL'): [('shift', 87)], (25, 'TOK_OPTIONAL'): [('reduce', ('regexp', 1, 23))], (79, 'TOK_CCUPPER'): [('reduce', ('range', 1, 30))], (57, 'TOK_QUOTE'): [('reduce', ('regexp', 2, 19))], (19, 'TOK_CHAR'): [('reduce', ('optanchor', 1, 13))], (51, 'TOK_IDENT'): [('shift', 26)], (67, 'TOK_CCPRINT'): [('reduce', ('range', 1, 32))], (78, 'TOK_CCUPPER'): [('reduce', ('range', 1, 43))], (46, 'TOK_STARCLOS'): [('shift', 54)], (77, 'TOK_CCALNUM'): [('reduce', ('range', 1, 42))], (64, 'TOK_OBRACKET'): [('shift', 27)], (12, 'TOK_DEDENT'): [('shift', 17)], (30, 'TOK_WILDCARD'): [('shift', 29)], (94, 'TOK_CBRACKET'): [('reduce', ('range', 3, 31))], (76, 'TOK_CCPRINT'): [('reduce', ('range', 1, 41))], (84, 'TOK_OPTIONAL'): [('shift', 52)], (92, 'TOK_CCPUNCT'): [('reduce', ('ranges', 2, 29))], (32, 'TOK_WILDCARD'): [('shift', 29)], (60, 'TOK_IDENT'): [('shift', 26)], (75, 'TOK_CCSPACE'): [('reduce', ('range', 1, 40))], (44, 'TOK_CCALPHA'): [('reduce', ('optinvert', 1, 26))], (70, 'TOK_CCUPPER'): [('reduce', ('range', 1, 35))], (72, 'TOK_CCBLANK'): [('reduce', ('range', 1, 37))], (44, 'TOK_CCLOWER'): [('reduce', ('optinvert', 1, 26))], (69, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 34))], (67, 'TOK_CCSPACE'): [('reduce', ('range', 1, 32))], (59, 'TOK_CPAREN'): [('reduce', ('regexp', 2, 15))], (23, 'TOK_SRCCODE'): [('reduce', ('sect', 4, 4))], (45, 'TOK_CCALNUM'): [('shift', 67)], (86, 'TOK_ALT'): [('reduce', ('regexp', 3, 18))], (71, 'TOK_CBRACKET'): [('reduce', ('range', 1, 36))], (39, 'TOK_WILDCARD'): [('shift', 29)], (59, 'TOK_CHAR'): [('reduce', ('regexp', 2, 15))], (57, 'TOK_WILDCARD'): [('reduce', ('regexp', 2, 19))], (73, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 38))], (27, 'TOK_CCALNUM'): [('reduce', ('optinvert', 0, 27))], (91, 'TOK_POSCLOS'): [('reduce', ('cclass', 4, 25))], (44, 'TOK_CCBLANK'): [('reduce', ('optinvert', 1, 26))], (74, 'TOK_CCLOWER'): [('reduce', ('range', 1, 39))], (27, 'TOK_CCDIGIT'): [('reduce', ('optinvert', 0, 27))], (28, 'TOK_CHAR'): [('shift', 25)], (64, 'TOK_OPAREN'): [('shift', 28)], (46, 'TOK_CHAR'): [('shift', 25)], (34, 'TOK_QUOTE'): [('shift', 53)], (76, 'TOK_CCSPACE'): [('reduce', ('range', 1, 41))], (34, 'TOK_POSCLOS'): [('shift', 59)], (45, 'TOK_CCDIGIT'): [('shift', 71)], (52, 'TOK_OBRACKET'): [('reduce', ('regexp', 2, 17))], (50, 'TOK_CPAREN'): [('shift', 82)], (82, 'TOK_WILDCARD'): [('reduce', ('regexp', 3, 20))], (86, 'TOK_OPAREN'): [('shift', 28)], (62, 'TOK_WILDCARD'): [('shift', 29)], (85, 'TOK_ALT'): [('reduce', ('regexp', 3, 18))], (44, 'TOK_CCCNTRL'): [('reduce', ('optinvert', 1, 26))], (66, 'TOK_SRCCODE'): [('shift', 89)], (68, 'TOK_CBRACKET'): [('reduce', ('range', 1, 33))], (44, 'TOK_CCALNUM'): [('reduce', ('optinvert', 1, 26))], (36, 'TOK_OBRACKET'): [('shift', 27)], (79, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 30))], (84, 'TOK_CHAR'): [('shift', 25)], (69, 'TOK_CCALNUM'): [('reduce', ('range', 1, 34))], (92, 'TOK_CCALNUM'): [('reduce', ('ranges', 2, 29))], (52, 'TOK_CHAR'): [('reduce', ('regexp', 2, 17))], (50, 'TOK_OPAREN'): [('shift', 28)], (45, 'TOK_CCBLANK'): [('shift', 69)], (91, 'TOK_WILDCARD'): [('reduce', ('cclass', 4, 25))], (25, 'TOK_CHAR'): [('reduce', ('regexp', 1, 23))], (59, 'TOK_OPAREN'): [('reduce', ('regexp', 2, 15))], (74, 'TOK_CCPRINT'): [('reduce', ('range', 1, 39))], (92, 'TOK_CCUPPER'): [('reduce', ('ranges', 2, 29))], (77, 'TOK_CBRACKET'): [('reduce', ('range', 1, 42))], (38, 'TOK_IDENT'): [('shift', 26)], (70, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 35))], (44, 'TOK_CCDIGIT'): [('reduce', ('optinvert', 1, 26))], (27, 'TOK_CCBLANK'): [('reduce', ('optinvert', 0, 27))], (67, 'TOK_CCLOWER'): [('reduce', ('range', 1, 32))], (46, 'TOK_OPTIONAL'): [('shift', 52)], (45, 'TOK_CCLOWER'): [('shift', 73)], (52, 'TOK_IDENT'): [('reduce', ('regexp', 2, 17))], (25, 'TOK_STARCLOS'): [('reduce', ('regexp', 1, 23))], (35, 'TOK_ALT'): [('reduce', ('regexp', 1, 22))], (59, 'TOK_OBRACKET'): [('reduce', ('regexp', 2, 15))], (72, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 37))], (71, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 36))], (50, 'TOK_OBRACKET'): [('shift', 27)], (74, 'TOK_CCSPACE'): [('reduce', ('range', 1, 39))], (61, 'TOK_IDENT'): [('shift', 26)], (89, 'TOK_QUOTE'): [('reduce', ('rulelist', 5, 10))], (55, 'TOK_QUOTE'): [('reduce', ('regexp', 2, 19))], (75, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 40))], (27, 'TOK_CCALPHA'): [('reduce', ('optinvert', 0, 27))], (76, 'TOK_CCLOWER'): [('reduce', ('range', 1, 41))], (36, 'TOK_OPAREN'): [('shift', 28)], (69, 'TOK_CCUPPER'): [('reduce', ('range', 1, 34))], (45, 'TOK_CCALPHA'): [('shift', 68)], (5, 'TOK_SRCCODE'): [('shift', 3)], (58, 'TOK_ALT'): [('reduce', ('regexp', 2, 19))], (67, 'TOK_CCALNUM'): [('reduce', ('range', 1, 32))], (57, 'TOK_CHAR'): [('reduce', ('regexp', 2, 19))], (45, 'TOK_CCSPACE'): [('shift', 76)], (74, 'TOK_CCALPHA'): [('reduce', ('range', 1, 39))], (76, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 41))], (74, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 39))], (36, 'TOK_WILDCARD'): [('shift', 29)], (40, 'TOK_IDENT'): [('shift', 26)], (27, 'TOK_CCSPACE'): [('reduce', ('optinvert', 0, 27))], (34, 'TOK_STARCLOS'): [('shift', 54)], (76, 'TOK_CCALNUM'): [('reduce', ('range', 1, 41))], (48, 'TOK_CHAR'): [('shift', 25)], (91, 'TOK_OBRACKET'): [('reduce', ('cclass', 4, 25))], (49, 'TOK_ALT'): [('shift', 51)], (67, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 32))], (26, 'TOK_POSCLOS'): [('reduce', ('regexp', 1, 21))], (82, 'TOK_OBRACKET'): [('reduce', ('regexp', 3, 20))], (45, 'TOK_CCPRINT'): [('shift', 74)], (59, 'TOK_WILDCARD'): [('reduce', ('regexp', 2, 15))], (29, 'TOK_IDENT'): [('reduce', ('regexp', 1, 24))], (73, 'TOK_CBRACKET'): [('reduce', ('range', 1, 38))], (74, 'TOK_CCBLANK'): [('reduce', ('range', 1, 39))], (91, 'TOK_OPAREN'): [('reduce', ('cclass', 4, 25))], (55, 'TOK_OPTIONAL'): [('shift', 52)], (30, 'TOK_STARCLOS'): [('shift', 54)], (80, 'TOK_CCCNTRL'): [('shift', 70)], (16, 'TOK_CHAR'): [('shift', 25)], (27, 'TOK_CCPRINT'): [('reduce', ('optinvert', 0, 27))], (77, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 42))], (37, 'TOK_SRCCODE'): [('shift', 65)], (42, 'TOK_POSCLOS'): [('shift', 59)], (50, 'TOK_WILDCARD'): [('shift', 29)], (68, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 33))], (65, 'TOK_DEDENT'): [('reduce', ('rulelist', 4, 9))], (34, 'TOK_IDENT'): [('shift', 26)], (68, 'TOK_CCSPACE'): [('reduce', ('range', 1, 33))], (54, 'TOK_OPAREN'): [('reduce', ('regexp', 2, 16))], (75, 'TOK_CCPUNCT'): [('reduce', ('range', 1, 40))], (10, 'TOK_QUOTE'): [('shift', 14)], (22, 'TOK_OBRACKET'): [('shift', 27)], (30, 'TOK_ALT'): [('shift', 51)], (80, 'TOK_CCUPPER'): [('shift', 77)], (56, 'TOK_OBRACKET'): [('reduce', ('regexp', 2, 19))], (94, 'TOK_CCLOWER'): [('reduce', ('range', 3, 31))], (72, 'TOK_CCXDIGIT'): [('reduce', ('range', 1, 37))], (77, 'TOK_CCALPHA'): [('reduce', ('range', 1, 42))], (29, 'TOK_CHAR'): [('reduce', ('regexp', 1, 24))], (83, 'TOK_ALT'): [('reduce', ('regexp', 3, 18))], (77, 'TOK_CCSPACE'): [('reduce', ('range', 1, 42))], (47, 'TOK_CHAR'): [('shift', 25)], (32, 'TOK_ALT'): [('shift', 51)], (16, 'TOK_IDENT'): [('shift', 26)], (49, 'TOK_CPAREN'): [('shift', 82)], (71, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 36))], (88, 'TOK_EOL'): [('shift', 93)], (86, 'TOK_WILDCARD'): [('shift', 29)], (60, 'TOK_QUOTE'): [('shift', 88)], (68, 'TOK_CCPRINT'): [('reduce', ('range', 1, 33))], (72, 'TOK_CBRACKET'): [('reduce', ('range', 1, 37))], (71, 'TOK_CCLOWER'): [('reduce', ('range', 1, 36))], (81, 'TOK_CHAR'): [('reduce', ('ranges', 1, 28))], (42, 'TOK_OPTIONAL'): [('shift', 52)], (48, 'TOK_IDENT'): [('shift', 26)], (82, 'TOK_OPTIONAL'): [('reduce', ('regexp', 3, 20))], (39, 'TOK_ALT'): [('shift', 51)], (73, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 38))], (29, 'TOK_STARCLOS'): [('reduce', ('regexp', 1, 24))], (56, 'TOK_OPAREN'): [('reduce', ('regexp', 2, 19))], (27, 'TOK_CCGRAPH'): [('reduce', ('optinvert', 0, 27))], (77, 'TOK_CCPRINT'): [('reduce', ('range', 1, 42))], (82, 'TOK_OPAREN'): [('reduce', ('regexp', 3, 20))], (74, 'TOK_CBRACKET'): [('reduce', ('range', 1, 39))], (83, 'TOK_OPTIONAL'): [('shift', 52)], (23, 'TOK_IDENT'): [('reduce', ('sect', 4, 4))], (57, 'TOK_IDENT'): [('reduce', ('regexp', 2, 19))], (22, 'TOK_OPAREN'): [('shift', 28)], (94, 'TOK_CCALNUM'): [('reduce', ('range', 3, 31))], (75, 'TOK_CHAR'): [('reduce', ('range', 1, 40))], (43, 'TOK_QUOTE'): [('shift', 66)], (54, 'TOK_OBRACKET'): [('reduce', ('regexp', 2, 16))], (62, 'TOK_ALT'): [('shift', 51)], (45, 'TOK_CCGRAPH'): [('shift', 72)], (40, 'TOK_CHAR'): [('shift', 25)], (77, 'TOK_CCBLANK'): [('reduce', ('range', 1, 42))], (61, 'TOK_CHAR'): [('shift', 25)], (93, 'TOK_IDENT'): [('reduce', ('deflist', 6, 8))], (22, 'TOK_WILDCARD'): [('shift', 29)], (71, 'TOK_CCALNUM'): [('reduce', ('range', 1, 36))], (85, 'TOK_CPAREN'): [('reduce', ('regexp', 3, 18))], (56, 'TOK_WILDCARD'): [('reduce', ('regexp', 2, 19))], (79, 'TOK_CHAR'): [('reduce', ('range', 1, 30))], (64, 'TOK_ALT'): [('shift', 51)], (31, 'TOK_QUOTE'): [('shift', 53)], (5, 'TOK_DEFS'): [('shift', 1)], (78, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 43))], (74, 'TOK_CCGRAPH'): [('reduce', ('range', 1, 39))], (1, 'TOK_INDENT'): [('shift', 7)], (81, 'TOK_CCXDIGIT'): [('reduce', ('ranges', 1, 28))], (26, 'TOK_CPAREN'): [('reduce', ('regexp', 1, 21))], (33, 'TOK_QUOTE'): [('shift', 53)], (70, 'TOK_CHAR'): [('reduce', ('range', 1, 35))], (71, 'TOK_CCDIGIT'): [('reduce', ('range', 1, 36))], (92, 'TOK_CCLOWER'): [('reduce', ('ranges', 2, 29))], (83, 'TOK_QUOTE'): [('reduce', ('regexp', 3, 18))], (25, 'TOK_IDENT'): [('reduce', ('regexp', 1, 23))], (38, 'TOK_CHAR'): [('shift', 25)], (86, 'TOK_OBRACKET'): [('shift', 27)], (75, 'TOK_CCCNTRL'): [('reduce', ('range', 1, 40))], (72, 'TOK_CHAR'): [('reduce', ('range', 1, 37))], (35, 'TOK_CPAREN'): [('reduce', ('regexp', 1, 22))], (54, 'TOK_WILDCARD'): [('reduce', ('regexp', 2, 16))], (5, '$EOF$'): [('reduce', ('spec', 1, 1))], (60, 'TOK_OPTIONAL'): [('shift', 52)], (84, 'TOK_IDENT'): [('shift', 26)], (68, 'TOK_CCALPHA'): [('reduce', ('range', 1, 33))], (42, 'TOK_QUOTE'): [('reduce', ('rulepat', 2, 11))], (92, 'TOK_CCCNTRL'): [('reduce', ('ranges', 2, 29))]}
semactions = [action0, action0, action1, action2, action3, action4, action5, action6, action7, action8, action9, action10, action11, action12, action13, action14, action15, action16, action17, action18, action19, action20, action21, action22, action23, action24, action25, action26, action27, action28, action29, action30, action31, action32, action33, action34, action35, action36, action37, action38, action39, action40, action41, action42]
gramspec = (goto, action, semactions)

import array

import nfa
import dfa
from util import printable
from errors import *

	# precomputed
wildclass = map(chr, range(0,10) + range(11,256))

	# information we parsed and analyzed, most of these variables
	# are used externally when we're done.
n = nfa.nfa()
globcode = "" 			# top-level code we emit
namedmachines = dict()	# set of machines indexed by name
statenums = dict()		# set of state nums indexed by name, and the count

			# indexed by starting state
eofacts = []			# actions on eof, indexed by state
statemachs = []			# two machines (anchored and unanchored) per state

			# indexed by machine number.
actions = [None]		# list of actions (code) to perform on acceptance
relist = [None]			# list of regular expressions we're matching



	# helper functions
def addrule(state, pat, code, usecopy) :
        "add a regexp rule or an eof rule in a given start state"
        global statemachs, actions, relist
        mach,anch,str,eof = pat
        if eof :
                if eofacts[state] != None :
				# XXX use state name in error
                        raise SpecError("Duplicate EOF action in state %d" % state)
                eofacts[state] = code
        else :
                if usecopy :
                        mach = n.copymach(mach)
			# XXX this makes lots of duplicate rules.  We can
			# share the same action with all rules that share the same pattern
                ruleno = len(relist)
                n.setaccept(mach, ruleno)
                actions.append(code)
                relist.append(str)
                statemachs[state][anch] = n.dualmach(statemachs[state][anch], mach)

def addstate(name) :
        "add a start state with the given name"
        if name not in statenums :
                statenums[name] = len(statenums)
                eofacts.append(None)
                statemachs.append([None,None])
        return statenums[name]

def list2cset(l) :
        "return a cset based on a list"
        s = array.array('b', [0] * 256)
        for n in l :
                s[n] = 1
        return s

def cset2list(cs, inv) :
        "return a list based on a cset, invert if requested"
        set = []
        for i in xrange(256) :
                if cs[i] != inv :
                        set.append(chr(i))
        return set

def csetunion(r1, r2) :
        """
        given two lists of values, return a new list that is the union
        The ranges are altered in the process
        """
        for n in xrange(256) :
                r1[n] |= r2[n]
        return r1


