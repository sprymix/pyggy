#!/usr/bin/env python

from distutils.core import setup
import vers

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(name = "pyggy",
	version = vers.version,
	author = "Tim Newsham",
	author_email = "newsham@lava.net",
	description = "Lexer and GLR parser generator",
	url = "http://www.lava.net/~newsham/pyggy/",
	packages = ['pyggy'],
	cmdclass = {'build_py': build_py})
