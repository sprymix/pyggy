#!/usr/bin/python
#
# util.py
#	Helper functions which dont properly belong to any one file.
#

# return a printable representation of a string
def printable(str, quoted = 0, escspace = 1) :
	str2 = ""
	for ch in str :
		if ch == '\n' or ch == '\\' or ch == '\0' or ch == '\r' or \
				ch == '\b' or ch == '\t' :
			if quoted :
				str2 += '\\'

			if ch == '\n' :
				str2 += '\\n'
			elif ch == '\\' :
				str2 += '\\'
			elif ch == '\r' :
				str2 += '\\r'
			elif ch == '\b' :
				str2 += '\\b'
			elif ch == '\0' :
				str2 += '\\0'
			elif ch == '\t' :
				str2 += '\\t'
		elif (ch < ' ' or ch > '~') or (ch == ' ' and escspace) :
			if quoted :
				str2 += '\\'
			str2 += "\\x%02x" % ord(ch)
		else :
			if quoted and ch == '"' :
				str2 += '\\'
			str2 += ch
	return str2

def minof(a, b) :
	if a < b :
		return a
	return b

def maxof(a, b) :
	if a < b :
		return b
	return a

