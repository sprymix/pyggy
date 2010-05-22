# -----------------------------------------------------------------------------
# ply_calc.py
#
# A simple calculator with variables -- using pylly lexer
#
# derived from calc.py from the PLY web page.
# example of using a PyLly lexer with PLY.
# -----------------------------------------------------------------------------

import sys

# build the lexer
import pyggy
l,lexer = pyggy.getlexer("ply_calc.pyl")
tokens = lexer.tokens

# Parsing rules

precedence = (
	('left','PLUS','MINUS'),
	('left','TIMES','DIVIDE'),
	('right','UMINUS'),
	)

# dictionary of names
names = { }

def p_statement_assign(t):
	'statement : NAME EQUALS expression'
	names[t[1]] = t[3]

def p_statement_expr(t):
	'statement : expression'
	print t[1]

def p_expression_binop(t):
	'''expression : expression PLUS expression
				  | expression MINUS expression
				  | expression TIMES expression
				  | expression DIVIDE expression'''
	if t[2] == '+'  : t[0] = t[1] + t[3]
	elif t[2] == '-': t[0] = t[1] - t[3]
	elif t[2] == '*': t[0] = t[1] * t[3]
	elif t[3] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
	'expression : MINUS expression %prec UMINUS'
	t[0] = -t[2]

def p_expression_group(t):
	'expression : LPAREN expression RPAREN'
	t[0] = t[2]

def p_expression_number(t):
	'expression : NUMBER'
	t[0] = t[1]

def p_expression_name(t):
	'expression : NAME'
	try:
		t[0] = names[t[1]]
	except LookupError:
		print "Undefined name '%s'" % t[1]
		t[0] = 0

def p_error(t):
	print "Syntax error at '%s'" % t.value

import yacc
yacc.yacc()

while 1:
	sys.stdout.write("calc > ")
	line = sys.stdin.readline()
	if line == "" :
		break
	
	l.setinputstr(line)
	yacc.parse(lexer=l)

