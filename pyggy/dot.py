#!/usr/bin/python
#
# dot.py
#	A helper class for calling the "dotty" program to display graphs.
#
# To use these functions you should have "dotty" in your path.
#

import os
import time

# A class for making a dot file and displaying it
#
# Setting debug to 1 will prevent the dot file from being erased.
class dot :
	def __init__(self, name) :
		self.__start(name)
		self.debug = 0

	def __start(self, name) :
		self.fname = name + str(os.getpid()) + ".dot"
		self.f = file(self.fname, "w")
		self.f.write("digraph %s {\n" % name)

	def add(self, str) :
		self.f.write(str + "\n")

	def end(self) :
		if self.f != None  :
			self.f.write("}\n")
			self.f.close()
			self.f = None

	def show(self) :
		assert self.fname != None
		self.end()
		# yah yah, dont call this with user provided data
		os.system("dotty \"%s\"" % self.fname)
		if not self.debug :
			# give dot some time to read the file (dotty may return
			# immediately in cygwin)
			time.sleep(1)
			os.remove(self.fname)
		self.fname = None

