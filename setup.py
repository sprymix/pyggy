#!/usr/bin/env python

from distutils.core import setup
import vers

setup(name = "pyggy",
	version = vers.version,
	author = "Tim Newsham",
	author_email = "newsham@lava.net",
	description = "Lexer and GLR parser generator",
	url = "http://www.lava.net/~newsham/pyggy/",
	packages = ['pyggy'])

